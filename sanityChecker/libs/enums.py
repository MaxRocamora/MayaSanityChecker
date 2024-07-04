# ----------------------------------------------------------------------------------------
# Maya Sanity Checker / Maximiliano Rocamora
# https://github.com/MaxRocamora/SanityChecker
# ----------------------------------------------------------------------------------------
from enum import Enum


class SeverityLevels(Enum):
    """Severity Levels Enums for Checks."""

    LOW = 25
    MODERATE = 50
    HIGH = 75
    CRITICAL = 100


# rgb color for progressBar UI
severity_colors = {
    SeverityLevels.LOW: '46, 134, 193',
    SeverityLevels.MODERATE: '230, 230, 0',
    SeverityLevels.HIGH: '255, 170, 0',
    SeverityLevels.CRITICAL: '255, 10, 10',
}


class CategoryGroups(Enum):
    """Groups Enums for Checks."""

    SCENE = 'scene'
    NODES = 'nodes'
    MESHES = 'meshes'
    NAMING = 'naming'
    MAPS = 'maps'


class Status(Enum):
    """Status Enums for Checks."""

    PASS = 'pass'
    FAIL = 'fail'
    STAND_BY = 'stand_by'
