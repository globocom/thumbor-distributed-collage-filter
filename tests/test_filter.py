#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file is part of thumbor-distributed-collage-filter.
# https://github.com/globocom/thumbor-distributed-collage-filter

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com thumbor@googlegroups.com

from preggy import expect

from tests.base import BaseTestCase


CONFIDENCE_LEVEL = 0.95


class DistributedCollageFilterTestCase(BaseTestCase):
    urls = (
        "800px-Guido-portrait-2014.jpg",
        "800px-Katherine_Maher.jpg",
        "Giunchedi%2C_Filippo_January_2015_01.jpg",
        "800px-Christophe_Henner_-_June_2016.jpg",
        "800px-Coffee_berries_1.jpg",
        "800px-A_small_cup_of_coffee.JPG",
        "513px-Coffee_beans_-_ziarna_kawy",
    )

    def get_filtered(self, filter_string, width=300, height=200):
        response = self.fetch(
            "/unsafe/%dx%d/filters:quality(99):distributed_collage(horizontal,smart,%s)/distributed_collage_fallback.png"
            % (
                width,
                height,
                filter_string,
            ),
            method="GET",
        )
        expect(response.code).to_equal(200)

        eng = self.get_engine(response.body)
        return eng.image

    def test_fallback_when_have_not_enough_images(self):
        image = self.get_filtered("")
        expected = self.get_fixture("distributed_collage_fallback.png")
        ssim = self.get_ssim(image, expected)
        expect(ssim).to_equal(1)

    def test_with_one_image(self):
        image = self.get_filtered("|".join(self.urls[:1]))
        expected = self.get_fixture("distributed_collage_1i.png")
        ssim = self.get_ssim(image, expected)
        expect(ssim).to_be_greater_than(CONFIDENCE_LEVEL)

    def test_with_two_images(self):
        image = self.get_filtered("|".join(self.urls[:2]))
        expected = self.get_fixture("distributed_collage_2i.png")
        ssim = self.get_ssim(image, expected)
        expect(ssim).to_be_greater_than(CONFIDENCE_LEVEL)

    def test_with_three_images(self):
        image = self.get_filtered("|".join(self.urls[:3]))
        expected = self.get_fixture("distributed_collage_3i.png")
        ssim = self.get_ssim(image, expected)
        expect(ssim).to_be_greater_than(CONFIDENCE_LEVEL)

    def test_with_four_images(self):
        image = self.get_filtered("|".join(self.urls[:4]))
        expected = self.get_fixture("distributed_collage_4i.png")
        ssim = self.get_ssim(image, expected)
        expect(ssim).to_be_greater_than(0.89)

    def test_with_four_images_and_zero_size(self):
        image = self.get_filtered("|".join(self.urls[:4]), width=0, height=0)
        expected = self.get_fixture("distributed_collage_4i.png")
        ssim = self.get_ssim(image, expected)
        expect(ssim).to_be_greater_than(0.89)

    def test_with_two_images_centered_when_no_feature_detected(self):
        image = self.get_filtered("|".join(self.urls[4:6]))
        expected = self.get_fixture("distributed_collage_2i_centered.png")
        ssim = self.get_ssim(image, expected)
        expect(ssim).to_be_greater_than(CONFIDENCE_LEVEL)

    def test_with_two_images_of_different_heights(self):
        image = self.get_filtered("|".join(self.urls[5:]), width=200, height=200)
        expected = self.get_fixture("distributed_collage_2i_diff_heights.png")
        ssim = self.get_ssim(image, expected)
        expect(ssim).to_be_greater_than(CONFIDENCE_LEVEL)

    def test_show_fallback_when_exceed_the_maximun_of_four_images(self):
        image = self.get_filtered("%s|%s" % ("|".join(self.urls[:4]), self.urls[1]))
        expected = self.get_fixture("distributed_collage_fallback.png")
        ssim = self.get_ssim(image, expected)
        expect(ssim).to_be_greater_than(CONFIDENCE_LEVEL)
