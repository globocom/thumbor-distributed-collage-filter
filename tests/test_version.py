#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of thumbor-distributed-collage-filter.
# https://github.com/globocom/thumbor-distributed-collage-filter

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2018, Globo.com <thumbor@corp.globo.com>

from preggy import expect

from thumbor_distributed_collage_filter import __version__
from tests.base import TestCase


class VersionTestCase(TestCase):
    def test_has_proper_version(self):
        expect(__version__).not_to_be_empty()
