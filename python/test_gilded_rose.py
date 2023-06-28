# -*- coding: utf-8 -*-
"""Unit test module for the functionality of the GildedRose and Item class"""
import unittest

from gilded_rose import Item, GildedRose


class GildedRoseTest(unittest.TestCase):
    """Class that is used to execute the test scenarios for GildedRose and Item class"""

    def test_quality_degrades_double_after_sell_in(self):
        """Test if quality degrades twice as fast after sell_in date. Specified in README.md"""
        original_quality = 10

        # Create GildedRose instance and update quality for a first time (before sell_in date)
        items = [Item(name="Random item", sell_in=1, quality=original_quality)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        # Save difference between quality before and after quality update (before sell_in date)
        # and update quality again (after sell_in date)
        delta_quality_before_sell_in = original_quality - items[0].quality
        gilded_rose.update_quality()

        # If quality degrades twice as fast after sell_in date, the orginal quality should be
        # reduced by the delta 3 times (1 time before sell_in date and 2 times after sell_in date)
        self.assertEqual(items[0].quality, original_quality - delta_quality_before_sell_in*3)


if __name__ == '__main__':
    unittest.main()
