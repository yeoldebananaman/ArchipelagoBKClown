from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import BKClownWorld

ITEM_NAME_TO_ID = {
    "FruitProgressiveChild": 1,
    "LemonadeProgressiveChild": 2,
    "FruitPunchForEveryone": 3,
    "LemonClownAccess": 4
}

DEFAULT_ITEM_CLASSIFICATIONS = {
    "FruitProgressiveChild": ItemClassification.progression,
    "LemonadeProgressiveChild": ItemClassification.progression,
    "LemonClownAccess": ItemClassification.progression, 
    "FruitPunchForEveryone": ItemClassification.filler
}


class BKClownItem(Item):
    game = "BKClown"


def get_random_filler_item_name(world: BKClownWorld) -> str:
    return "FruitPunchForEveryone"


def create_item_with_correct_classification(world: BKClownWorld, name: str) -> BKClownItem:
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]
    return BKClownItem(name, classification, ITEM_NAME_TO_ID[name], world.player)


def create_all_items(world: BKClownWorld) -> None:
    itempool: list[Item] = []
    for i in range(9):
        if i == 0:
            pass
        else:
            itempool.append(world.create_item("FruitProgressiveChild"))
    if world.options.LemonAdded:
        for i in range(9):
            itempool.append(world.create_item("LemonadeProgressiveChild"))
        itempool.append(world.create_item("LemonClownAccess"))

    number_of_items = len(itempool)

    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))

    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]
    world.multiworld.itempool += itempool
