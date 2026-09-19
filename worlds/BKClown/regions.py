from __future__ import annotations
from typing import TYPE_CHECKING
from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import BKClownWorld
def create_and_connect_regions(world: BKClownWorld) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: BKClownWorld) -> None:
    FirstClown = Region("FirstClown", world.player, world.multiworld)
    regions = [FirstClown]
    if world.options.LemonAdded:
        SecondClown = Region("SecondClown", world.player, world.multiworld)
        regions.append(SecondClown)


    world.multiworld.regions += regions


def connect_regions(world: BKClownWorld) -> None:
    if world.options.LemonAdded:
        FirstClown = world.get_region("FirstClown")
        SecondClown = world.get_region("SecondClown")

        FirstClown_to_SecondClown = Entrance(world.player, "FirstClown to SecondClown", parent=FirstClown)
        FirstClown.exits.append(FirstClown_to_SecondClown)
        FirstClown_to_SecondClown.connect(SecondClown)