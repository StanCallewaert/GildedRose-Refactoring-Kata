# -*- coding: utf-8 -*-
"""Module that contains the GildedRose class and Item class fuctionality"""

class GildedRose:
    """Class that represents Gilded Rose Inn and the items it holds"""

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        """Update the quality of all the items in the in according to specs in README.md"""
        for item in self.items:
            if item.name not in [Item.BRIE, Item.BACKSTAGE_PASSES]:
                if item.quality > 0:
                    if item.name != Item.SULFURAS:
                        item.quality = item.quality - 1
            else:
                if item.quality < 50:
                    item.quality = item.quality + 1
                    if item.name == Item.BACKSTAGE_PASSES:
                        if item.sell_in < 11:
                            if item.quality < 50:
                                item.quality = item.quality + 1
                        if item.sell_in < 6:
                            if item.quality < 50:
                                item.quality = item.quality + 1
            if item.name != Item.SULFURAS:
                item.sell_in = item.sell_in - 1
            if item.sell_in < 0:
                if item.name != Item.BRIE:
                    if item.name != Item.BACKSTAGE_PASSES:
                        if item.quality > 0:
                            if item.name != Item.SULFURAS:
                                item.quality = item.quality - 1
                    else:
                        item.quality = 0
                else:
                    if item.quality < 50:
                        item.quality = item.quality + 1

class Item:
    """Class that represents a single Item (that can be held in the Gilded Rose Inn)"""
    BRIE = "Aged Brie"
    BACKSTAGE_PASSES = "Backstage passes to a TAFKAL80ETC concert"
    SULFURAS = "Sulfuras, Hand of Ragnaros"

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
