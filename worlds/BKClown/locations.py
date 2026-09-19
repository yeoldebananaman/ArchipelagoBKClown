from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import items

if TYPE_CHECKING:
    from .world import BKClownWorld

LOCATION_NAME_TO_ID = {
    "Surprise 0 Fruit Child": 100,
    "Surprise 0 Lemonade Child": 101,
    "Surprise 1 Fruit Child": 1,
    "Surprise 2 Fruit Child": 2,
    "Surprise 3 Fruit Child": 3,
    "Surprise 4 Fruit Child": 4,
    "Surprise 5 Fruit Child": 5,
    "Surprise 6 Fruit Child": 6,
    "Surprise 7 Fruit Child": 7,
    "Surprise 8 Fruit Child": 8,
    "Surprise 9 Fruit Child": 9,
    "Surprise 1 Lemonade Child": 150,
    "Surprise 2 Lemonade Child": 300,
    "Surprise 3 Lemonade Child": 450,
    "Surprise 4 Lemonade Child": 600,
    "Surprise 5 Lemonade Child": 750,
    "Surprise 6 Lemonade Child": 900,
    "Surprise 7 Lemonade Child": 1050,
    "Surprise 8 Lemonade Child": 1200,
    "Surprise 9 Lemonade Child": 6350
}
class BKClownLocation(Location):
    game = "BKClown"


def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}
    

def create_all_locations(world: BKClownWorld) -> None:
    create_regular_locations(world)
    create_events(world)



def create_regular_locations(world: BKClownWorld) -> None:
    FirstClown = world.get_region("FirstClown")
    FirstCheck = BKClownLocation(world.player, "Surprise 0 Fruit Child", world.location_name_to_id["Surprise 0 Fruit Child"], FirstClown)
    FirstClown.locations.append(FirstCheck)
    for i in range(9):
            beelatro = f"Surprise {i + 1} Fruit Child"
            loc = BKClownLocation(world.player,beelatro, world.location_name_to_id[beelatro], FirstClown)
            FirstClown.locations.append(loc)
    if world.options.LemonAdded:
        SecondClown = world.get_region("SecondClown")
        First2Check = BKClownLocation(world.player, "Surprise 0 Lemonade Child", world.location_name_to_id["Surprise 0 Lemonade Child"], SecondClown)
        SecondClown.locations.append(First2Check)
        for i in range(9):
                beelatro = f"Surprise {i + 1} Lemonade Child"
                loc = BKClownLocation(world.player,beelatro, world.location_name_to_id[beelatro], SecondClown)
                SecondClown.locations.append(loc)




def create_events(world: BKClownWorld) -> None:
    pass