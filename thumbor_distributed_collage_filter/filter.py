#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of thumbor-distributed-collage-filter.
# https://github.com/globocom/thumbor-distributed-collage-filter

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2018, Globo.com <thumbor@corp.globo.com>

# TODO: vertical distribution
# TODO: separator line between images
# TODO: custom alignment

import math
from os.path import abspath, dirname, isabs, join

import cv2
import numpy as np
import tornado.gen
from thumbor.filters import BaseFilter, filter_method
from thumbor.loaders import LoaderResult
from thumbor.point import FocalPoint
from thumbor.utils import logger
from libthumbor import CryptoURL


class Filter(BaseFilter):
    MAX_IMAGES = 4

    @filter_method(BaseFilter.String, BaseFilter.String, r'[^\)]+', async=True)
    @tornado.gen.coroutine
    def distributed_collage(self, callback, orientation, alignment, urls):
        self.callback = callback
        self.orientation = orientation
        self.alignment = alignment
        self.urls = urls.split('|')
        self.images = {}

        total = len(self.urls)
        if total > self.MAX_IMAGES:
            logger.error('filters.distributed_collage: Too many images to join')
            callback()
        elif total == 0:
            logger.error('filters.distributed_collage: No images to join')
            callback()
        else:
            self.urls = self.urls[:self.MAX_IMAGES]

            self.max_age = self.context.config.MAX_AGE

            self._calculate_dimensions()
            yield self._fetch_images()

            self.context.request.max_age = self.max_age

    def _calculate_dimensions(self):
        width = self.context.request.width or self.context.transformer.get_target_dimensions()[0]
        self.image_width = math.floor(width / len(self.urls))
        self.last_image_width = width - ((len(self.urls) - 1) * self.image_width)

    @tornado.gen.coroutine
    def _fetch_images(self):
        crypto = CryptoURL(key=self.context.server.security_key)

        image_ops = []
        if not hasattr(self.context.config, 'DISTRIBUTED_COLLAGE_FILTER_HTTP_LOADER'):
            self.context.config.DISTRIBUTED_COLLAGE_FILTER_HTTP_LOADER = 'thumbor.loaders.http_loader'
        self.context.modules.importer.import_item('DISTRIBUTED_COLLAGE_FILTER_HTTP_LOADER')
        loader = self.context.modules.importer.distributed_collage_filter_http_loader

        for i, url in enumerate(self.urls):
            width = self.image_width if i < len(self.urls) - 1 else self.last_image_width
            height = self.context.request.height or self.context.transformer.get_target_dimensions()[1]
            params = {
                'width': int(width),
                'height': int(height),
                'image_url': url,
                'smart': True,
                'halign': 'center',
                'valign': 'middle',
                'filters': ['quality(100)'],
            }
            thumbor_host = getattr(self.context.config, 'DISTRIBUTED_COLLAGE_FILTER_THUMBOR_SERVER_URL',
                '%s://%s' % (
                    self.context.request_handler.request.protocol,
                    self.context.request_handler.request.host,
                ),
            )
            encrypted_url = '%s%s' % (thumbor_host, crypto.generate(**params))
            image_ops.append(loader.load(self.context, encrypted_url))

        images = yield image_ops

        successful = all([image.successful for image in images])
        if not successful:
            logger.error('Retrieving at least one of the collaged images failed: %s' % (
                ', '.join([image.error for image in images if not image.successful]),
            ))
            self.callback()
            return

        max_age = min([self.get_max_age(image.metadata.get('Cache-Control'), self.max_age) for image in images])
        self.assembly_images(images)
        self.callback()

    def get_max_age(self, header, default):
        # 'max-age=86400,public'
        if header is None or 'max-age' not in header:
            return default

        return int(header.split(',')[0].split('=')[-1])

    def create_engine(self):
        try:
            return self.context.modules.engine.__class__(self.context)
        except Exception as err:
            logger.exception(err)

    def assembly_images(self, images):
        current_width = 0

        for image in images:
            buffer = image.buffer
            engine = self.create_engine()
            engine.load(buffer, None)

            self.engine.paste(engine, [current_width, 0], merge=True)
            current_width += self.image_width
