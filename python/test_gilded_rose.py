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
        self.assertEqual(
            items[0].quality,
            original_quality - delta_quality_before_sell_in*3,
            "Quality doesn't degrade exactly twice as fast after sell_in date. " + \
            "Quality degraded by " + str(delta_quality_before_sell_in) + " before sell in and " + \
            "by " + str(original_quality-delta_quality_before_sell_in-items[0].quality) + \
            " after sell in."
        )

    def test_quality_item_never_negative_quality(self):
        """Test if all kinds of items never have a negative quality"""

        # Create GildedRose instance with items that have different code flows
        items = [
            Item(name="Random item", sell_in=10, quality=1),
            Item(name=GildedRose.BRIE, sell_in=10, quality=1),
            Item(name=GildedRose.BACKSTAGE_PASSES, sell_in=10, quality=1),
            Item(name=GildedRose.SULFURAS, sell_in=10, quality=1),
            Item(name=GildedRose.CONJURED, sell_in=10, quality=1)
        ]
        gilded_rose = GildedRose(items)

        # Update quality of the items 10 times (should be enough to get negative quality)
        for _ in range(10):
            gilded_rose.update_quality()

        # Check if none of the items has a negative quality
        for item in items:
            self.assertGreaterEqual(
                item.quality,
                0,
                "Quality of " + item.name + " is negative. It is: " + str(item.quality)
            )

    def test_quality_brie_increases(self):
        """Test if quality of brie increases"""

        # Create GildedRose instance with a Brie item and update quality
        items = [Item(name=GildedRose.BRIE, sell_in=5, quality=1)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        # Check if Brie item increased its quality (quality = 2 compared to 1 orginally)
        self.assertEqual(items[0].quality, 2, "Quality of Brie didn't increase by one")

    def test_quality_item_is_never_over_fifty(self):
        """Test if all kinds of items never have a quality over 50"""

        # Create GildedRose instance with items that have different code flows
        items = [
            Item(name="Random item", sell_in=10, quality=49),
            Item(name=GildedRose.BRIE, sell_in=10, quality=49),
            Item(name=GildedRose.BACKSTAGE_PASSES, sell_in=10, quality=1),
            Item(name=GildedRose.SULFURAS, sell_in=10, quality=1),
            Item(name=GildedRose.CONJURED, sell_in=10, quality=1)
        ]
        gilded_rose = GildedRose(items)

        # Update quality of the items 10 times (should be enough to get quality over 50)
        for _ in range(10):
            gilded_rose.update_quality()

        # Check if none of the items has a quality over 50
        for item in items:
            self.assertLessEqual(
                item.quality,
                50,
                "Quality of " + item.name + " is over 50. It is: " + str(item.quality)
            )

    def test_sulfaras_unchanged_sell_in_and_quality(self):
        """Test if sell_in and quality remain unchanged when updating quality of Sulfaras"""

        # Create GildedRose instance with Sulfaras item and update quality
        items = [Item(name=GildedRose.SULFURAS, sell_in=5, quality=1)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        # Check if Sulfaras item didn't change its sell_in or quality
        self.assertEqual(items[0].sell_in, 5, "Sell_in of Sulfaras shouldn't change")
        self.assertEqual(items[0].quality, 1, "Quality of Sulfaras shouldn't change")

    def test_backstage_passes_quality_scheme(self):
        """
        Test if backstage passes:
        Quality increases by 2 when there are 10 days or less and 
        by 3 when there are 5 days or less but Quality drops to 0 after the concert
        """
        previous_quality = 1

        # Create GildedRose instance with Backstage item and update quality
        items = [Item(name=GildedRose.BACKSTAGE_PASSES, sell_in=11, quality=previous_quality)]
        gilded_rose = GildedRose(items)

        # Update quality when there are 11 days. Quality should increase by 1
        gilded_rose.update_quality()
        self.assertEqual(
            items[0].quality,
            previous_quality + 1,
            "Quality shouldn't change when sell_in is bigger than 10"
        )
        previous_quality = items[0].quality

        # Update quality when there are 10-6 days. Quality should increase by 2
        for _ in range(10, 5, -1):
            gilded_rose.update_quality()
            self.assertEqual(
                items[0].quality,
                previous_quality + 2,
                "Quality should increase by 2 when sell_in is from 10 to 6"
            )
            previous_quality = items[0].quality

        # Update quality when there are 5-0 days. Quality should increase by 3
        for _ in range(5, 0, -1):
            gilded_rose.update_quality()
            self.assertEqual(
                items[0].quality,
                previous_quality + 3,
                "Quality should increase by 3 when sell_in is from 5 to 0"
            )
            previous_quality = items[0].quality

        # Quality should become 0 after concert
        gilded_rose.update_quality()
        self.assertEqual(items[0].quality, 0, "Quality should become 0 after concert")

    def test_conjured_degrades_twice_as_fast(self):
        """Test if Conjured item degrades twice as fast as normal items"""

        # Create GildedRose instance with Conjured item
        items = [Item(name=GildedRose.CONJURED, sell_in=1, quality=10)]
        gilded_rose = GildedRose(items)

        # Update quality before sell_in
        gilded_rose.update_quality()

        # Check if quality degraded by 2 (10->8, twice as fast as normal items before sell_in)
        quality_degration_before_sell_in = items[0].quality
        self.assertEqual(
            quality_degration_before_sell_in,
            8,
            "Quality Conjured item doesn't degrade exactly twice as fast as normal items. " + \
            "Quality of Conjured item degraded from 10 to " + str(quality_degration_before_sell_in)
        )

        # Update quality after sell_in
        gilded_rose.update_quality()

        # Check if quality degraded by 4 (8->4, twice as fast as normal items after sell_in)
        quality_degration_after_sell_in = items[0].quality
        self.assertEqual(
            quality_degration_after_sell_in,
            4,
            "Quality Conjured item doesn't degrade exactly twice as fast as normal items. " + \
            "Quality of Conjured item degraded from " + str(quality_degration_before_sell_in) + \
            " to " + str(quality_degration_after_sell_in)
        )

if __name__ == '__main__':
    unittest.main()
