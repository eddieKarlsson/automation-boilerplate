from enum import Enum, auto

class UnitTypes(Enum):
    """Class to represent the different types of units / phases, must correspond to
    the table in excel under _configs"""
    
    PHASE = 'Phase'
    LINE_UNIT = 'Line Unit'
    TANK_UNIT = 'Tank Unit'