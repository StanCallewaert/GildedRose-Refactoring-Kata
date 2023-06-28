# -*- coding: utf-8 -*-
"""Module that contains the GildedRose class and Item class fuctionality"""

class GildedRose:
    """Class that represents Gilded Rose Inn and the items it holds"""
    BRIE = "Aged Brie"
    BACKSTAGE_PASSES = "Backstage passes to a TAFKAL80ETC concert"
    SULFURAS = "Sulfuras, Hand of Ragnaros"
    CONJURED = "Conjured"

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        """Update the quality of all the items in the in according to specs in README.md"""
        for item in self.items:
            # Update the quality of the item according to the specs in README.md:
            # Quality of Brie increases instead of decreasing
            if item.name == GildedRose.BRIE:
                item.quality = self.change_quality_item_by_number(item=item, number=1)
            # Quality of backstage passes increases more closer to sell_in and 0 after sell_in
            elif item.name == GildedRose.BACKSTAGE_PASSES:
                if item.sell_in > 10:
                    item.quality = self.change_quality_item_by_number(item=item, number=1)
                elif item.sell_in > 5:
                    item.quality = self.change_quality_item_by_number(item=item, number=2)
                elif item.sell_in > 0:
                    item.quality = self.change_quality_item_by_number(item=item, number=3)
                else:
                    item.quality = 0
            # Quality of Sulfaras doesn't change
            elif item.name != GildedRose.SULFURAS:
                # Item degrades twice as fast once the sell by date passed
                degrade_twice_as_fast = item.sell_in <= 0
                number = -1

                # Quality of Conjured changes twice as fast as normal items
                if item.name == GildedRose.CONJURED:
                    number *= 2

                item.quality = self.change_quality_item_by_number(
                    item=item,
                    number=number,
                    degrade_twice_as_fast=degrade_twice_as_fast
                )

            # Update the sell_in of the item according to the specs in README.md
            if item.name != GildedRose.SULFURAS:
                item.sell_in -= 1

    def change_quality_item_by_number(self, item, number, degrade_twice_as_fast=False):
        """
        Change the quality by the number that is given as parameter (can be positive or negative).
        While changing the quality, the quality can't go over 50 or be negative (read README.md)
        """
        if degrade_twice_as_fast:
            number *= 2

        new_quality = item.quality + number

        # Quality can be minimum 0 and maximum 50
        if new_quality < 0:
            return 0
        if new_quality > 50:
            return 50

        return new_quality

class Item:
    """Class that represents a single Item (that can be held in the Gilded Rose Inn)"""
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "{self.name}, {self.sell_in}, {self.quality}"
