# -*- coding: utf-8 -*-
"""Module that contains the GildedRose class and Item class fuctionality"""

class GildedRose:
    """Class that represents Gilded Rose Inn and the items it holds"""

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        """Update the quality of all the items in the in according to specs in README.md"""
        for item in self.items:
            # Update the quality of the item according to the specs in README.md:
            # Quality of Brie increases instead of decreasing
            if item.name == Item.BRIE:
                item.change_quality_item_by_number(number=1)
            # Quality of backstage passes increases more closer to sell_in and 0 after sell_in
            elif item.name == Item.BACKSTAGE_PASSES:
                if item.sell_in > 10:
                    item.change_quality_item_by_number(number=1)
                elif item.sell_in > 5:
                    item.change_quality_item_by_number(number=2)
                elif item.sell_in > 0:
                    item.change_quality_item_by_number(number=3)
                else:
                    item.quality = 0
            # Quality of Sulfaras doesn't change
            elif item.name != Item.SULFURAS:
                # Item degrades twice as fast once the sell by date passed
                degrade_twice_as_fast = item.sell_in <= 0
                number = -1

                # Quality of Conjured changes twice as fast as normal items
                if item.name == Item.CONJURED:
                    number *= 2

                item.change_quality_item_by_number(
                    number=number,
                    degrade_twice_as_fast=degrade_twice_as_fast
                )

            # Update the sell_in of the item according to the specs in README.md
            if item.name != Item.SULFURAS:
                item.sell_in -= 1

class Item:
    """Class that represents a single Item (that can be held in the Gilded Rose Inn)"""
    BRIE = "Aged Brie"
    BACKSTAGE_PASSES = "Backstage passes to a TAFKAL80ETC concert"
    SULFURAS = "Sulfuras, Hand of Ragnaros"
    CONJURED = "Conjured"

    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in

        # Raise errors if quality is set negative or over 50
        if quality < 0:
            raise ValueError("Quality can't be negative")
        if quality > 50:
            raise ValueError("Quality can't be over 50")

        self.quality = quality

    def __repr__(self):
        return "{self.name}, {self.sell_in}, {self.quality}"

    def change_quality_item_by_number(self, number, degrade_twice_as_fast=False):
        """
        Change the quality by the number that is given as parameter (can be positive or negative).
        While changing the quality, the quality can't go over 50 or be negative (read README.md)
        """
        if degrade_twice_as_fast:
            number *= 2

        if 0 <= self.quality + number <= 50:
            self.quality += number
