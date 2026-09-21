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
        world.set_rule(FirstClown_to_SecondClown, lambda state: state.has(("LemonClownAccess"), world.player))

def set_all_location_rules(world: BKClownWorld) -> None:    
        
        for i in range(10):
                FruitLoc = world.get_location( f"Surprise {i} Fruit Child")
                set_rule(FruitLoc, lambda state, n = i: state.has_group("FruitProgressiveChild", world.player, count= n ))

        if world.options.LemonAdded:
                for i in range(10):
                    LemonLoc = world.get_location( f"Surprise {i} Lemonade Child")
                    set_rule(LemonLoc, lambda state, n = i: state.has_group("LemonadeProgressiveChild", world.player, count= n ) and
                            state.has("LemonClownAccess", world.player)
                            )



def set_completion_condition(world: BKClownWorld) -> None:

    world.set_completion_rule(lambda state: (
        state.has_group("FruitProgressiveChild", world.player, count=8) and
        state.has_group("LemonadeProgressiveChild", world.player, count=8) and
        state.has("LemonClownAccess", world.player)
    ) if world.options.LemonAdded else (
        state.has_group("FruitProgressiveChild", world.player, count=8) 
        ))