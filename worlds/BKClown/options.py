from dataclasses import dataclass

from Options import (
    Choice, 
    OptionGroup, 
    PerGameCommonOptions, 
    Range, 
    Toggle
)


class LemonadeAdded(Toggle):
    """
    Determines whether lemonade clown will be added for checks
    """
    display_name = "Lemonade Clown Toggle"

@dataclass
class BKClownOptions(PerGameCommonOptions):
    LemonAdded: LemonadeAdded