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

class SendLowWhenHigh(Toggle):
    """
    (Purely Gameplay Affected)\n 
    When toggled, if you get higher scores it will send all previous lower score checks alongside it.\n 
    (e.g: getting a score equal to 3 children will send the checks for scaring 1, 2, and 3 children as opposed to just sending the scaring 3 children check)
    """
    display_name = "SendLowChecksOnHighChecks"

@dataclass
class BKClownOptions(PerGameCommonOptions):
    LemonAdded: LemonadeAdded
    SLWH: SendLowWhenHigh