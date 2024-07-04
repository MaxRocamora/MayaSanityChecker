# ----------------------------------------------------------------------------------------
# Maya Sanity Checker / Maximiliano Rocamora
# https://github.com/MaxRocamora/SanityChecker
# ----------------------------------------------------------------------------------------
import contextlib
from PySide2.QtWidgets import QTreeWidgetItem
from PySide2.QtGui import QColor

import maya.cmds as cmds

from sanityChecker.resources.resources import Icons
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')


class MayaNodeTreeItem(QTreeWidgetItem):
    item_type = 'node'

    def __init__(self, parent: QTreeWidgetItem = None, name: str = '', *args):
        """Maya Node Tree Item for Sanity Checker."""
        super().__init__(parent, *args)
        self._name = name
        self.setText(0, name)
        self.setIcon(0, self.icon())
        self.setTextColor(0, QColor(235, 235, 235))

    def name(self):
        """Returns name of this node."""
        return self._name

    def icon(self):
        """Returns icon for this node."""
        return Icons.widget_node

    def callback_selected(self):
        """Callback when this node is selected."""
        log.info(f'Node Selected: {self.name()}')
        with contextlib.suppress(ValueError, AttributeError):
            cmds.select(self.name())
