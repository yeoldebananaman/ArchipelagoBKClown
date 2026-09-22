from __future__ import annotations

from typing import TYPE_CHECKING


from BaseClasses import CollectionState
from rule_builder.rules import Has, HasAll, Rule
from worlds.generic.Rules import add_rule, set_rule


if TYPE_CHECKING:
    from .world import BKClownWorld


def set_all_rules(world: BKClownWorld) -> None:

    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: BKClownWorld) -> None:
    if world.options.LemonAdded:
        FirstClown_to_SecondClown = world.get_entrance("FirstClown to SecondClown")
        world.set_rule(FirstClown_to_SecondClown, Has("LemonClownAccess"))

def set_all_location_rules(world: BKClownWorld) -> None:    
        
        for i in range(10):
                FruitLoc = world.get_location( f"Surprise {i} Fruit Child")
                world.set_rule(FruitLoc, Has("FruitProgressiveChild", count=i))

        if world.options.LemonAdded:
                for i in range(10):
                    LemonLoc = world.get_location( f"Surprise {i} Lemonade Child")
                    world.set_rule(LemonLoc, Has("LemonadeProgressiveChild", count=i) | Has("LemonClownAccess"))



def set_completion_condition(world: BKClownWorld) -> None:
    if world.options.LemonAdded:
        world.set_completion_rule(
            Has("FruitProgressiveChild", count=8) |
            Has("LemonadeProgressiveChild", count=8) |
            Has("LemonClownAccess", world.player)
        )
    else:
        world.set_completion_rule(Has("FruitProgressiveChild", count=8))