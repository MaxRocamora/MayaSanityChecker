# ----------------------------------------------------------------------------------------
# Maya Sanity Checker / Maximiliano Rocamora
# https://github.com/MaxRocamora/SanityChecker
#
# Check BaseClass
# Subclass this module to create a new check object.
# ----------------------------------------------------------------------------------------
from abc import abstractmethod
import maya.cmds as cmds

from sanityChecker.libs.enums import CategoryGroups, SeverityLevels, Status
from sanityChecker.libs.flag_node import FlagNodes
from sanityChecker.resources.resources import Icons

# To create a new CHECK, define this properties in the subclass.
name = 'default'
group = ''
description = 'error description'
level = SeverityLevels.CRITICAL
autofix = False
hint = 'Hint message on how to fix this error.'


class Check:
    def __init__(
        self,
        name: str,
        group: CategoryGroups,
        description: str,
        level: SeverityLevels,
        autofix: bool,
        hint: str,
    ):
        """Check BaseClass."""

        self._name = name
        self._group = group
        self._description = description
        self._level = level
        self._has_autofix = autofix
        self._fix_hint = hint
        self._nodes = FlagNodes(self)

    def __str__(self) -> str:
        """Returns check class name."""
        return f'Check Class {self.name()}'

    def name(self) -> str:
        """Returns name for this check."""
        return self._name

    def group(self) -> str:
        """Returns a string of witch parent group this check belongs to."""
        return self._group.value

    def description(self) -> str:
        """Returns error name for this check."""
        return self._description

    def fix_hint(self) -> str:
        """Returns fix hint for this check."""
        return self._fix_hint

    def level(self) -> int:
        """Returns error severity level for this check."""
        return self._level.value

    def has_autofix(self) -> bool:
        """Returns true if this error can be autofixed.

        If is set to True, this check need to have a fix() method.
        """
        return self._has_autofix

    def filename(self) -> str:
        """Returns the filename of the check."""
        return self.__module__.split('.')[-1]

    def nodes(self):
        """Returns a list of flagged nodes."""
        return self._nodes

    # ------------------------------------------------------------------------------------
    # Status Internal methods
    # ------------------------------------------------------------------------------------

    def status_message(self) -> str:
        """Returns message for ui title."""
        return f'{self.name()} Test {self.status()}! ({len(self._nodes)})'

    def status(self) -> str:
        """Returns waiting, passed, or failed string also used by .icon()."""
        return Status.PASS if not len(self.nodes()) else Status.FAIL

    def stand_by_icon(self) -> str:
        """Returns icon for this check."""
        return getattr(Icons, Status.STAND_BY.value)

    def status_icon(self) -> str:
        """Returns icon for this check."""
        return getattr(Icons, self.status().value)

    # ------------------------------------------------------------------------------------
    # Flagged Bad Nodes
    # ------------------------------------------------------------------------------------

    def add_failed_node(self, node: str):
        """Add a flagged node to the list."""
        self._nodes.add(node)

    def reset(self):
        """Clear flagged nodes."""
        self._nodes.clear()

    def nodes(self):
        """Returns a list of flagged nodes."""
        return self._nodes

    # ------------------------------------------------------------------------------------
    # Main Methods
    # ------------------------------------------------------------------------------------

    @abstractmethod
    def run(self) -> dict:
        """Performs scan of this check on maya scene/nodes.

        Note:
            Subclass this method on new checks.
        """
        self.reset()

        for node in cmds.ls(type='transform'):
            self.add_failed_node(node)

    def fix(self):
        """Perform technical fix on this check if possible.

        Note:
            Subclass this method on new checks for autofix.
        """
        pass
