# ----------------------------------------------------------------------------------------
# Maya Sanity Checker / Maximiliano Rocamora
# https://github.com/MaxRocamora/SanityChecker
#
# ----------------------------------------------------------------------------------------
import typing
import maya.cmds as cmds

if typing.TYPE_CHECKING:
    from sanityChecker.libs.check import Check


class MayaNode:
    def __init__(self, maya_node: str, error: str, level: int):
        """Represents a Failed Maya Node."""
        self._name = maya_node
        self.error = error
        self.level = level
        self.long_name = cmds.ls(maya_node, long=1)

    def name(self):
        """Return Maya Node Name."""
        return self._name

    def __str__(self):
        """Return Maya Node Name."""
        return self._name

    def __repr__(self):
        """Return Maya Node Name."""
        return self._name


class FlagNodes:
    def __init__(self, check: 'Check'):
        """List of flagged nodes."""
        self.check = check
        self._nodes = []

    def __iter__(self):
        """Iterate over flagged nodes."""
        return iter(self._nodes)

    def __len__(self):
        """Return number of flagged nodes."""
        return len(self._nodes)

    def __getitem__(self, index):
        """Get flagged node by index."""
        return self._nodes[index]

    def __str__(self):
        """Return string representation of flagged nodes."""
        return f'{self._check_name} - {len(self)} nodes flagged.'

    def __repr__(self):
        """Return string representation of flagged nodes."""
        return f'{self._check_name} - {len(self)} nodes flagged.'

    def __bool__(self):
        """Return True if there are flagged nodes."""
        return bool(self._nodes)

    def add(self, node: str):
        """Add a flagged node to the list."""
        self._nodes.append(MayaNode(node, self.check.description(), self.check.level()))

    def clear(self):
        """Clear flagged nodes."""
        self._nodes = []
