# ----------------------------------------------------------------------------------------
# Maya Sanity Checker / Maximiliano Rocamora
# https://github.com/MaxRocamora/SanityChecker
# ----------------------------------------------------------------------------------------
from PySide2.QtWidgets import QTreeWidgetItem
from PySide2 import QtGui

from sanityChecker.libs.enums import CategoryGroups
from sanityChecker.widgets.group import GroupTreeItem
from sanityChecker.resources.resources import Icons
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')


class CategoryTreeItem(QTreeWidgetItem):
    item_type = 'category'

    def __init__(self, parent: QTreeWidgetItem, name: str, checks: dict):
        """Category Tree Item for Sanity Checker."""
        super().__init__(parent)
        self.parent = parent
        self._name = name
        self.setText(0, name.upper())
        self.setIcon(0, self.icon())
        self.setBackgroundColor(0, QtGui.QColor(50, 50, 50))
        self.setExpanded(1)

        for group in CategoryGroups:
            GroupTreeItem(self, name=group.value, checks=checks[group.value])

    def name(self):
        """Returns name of this category."""
        return self._name

    def icon(self):
        """Returns icon for this category."""
        return Icons.widget_category

    def callback_selected(self):
        """Callback when this category is selected."""
        pass

    def get_children(self):
        """Returns children widgets (groups)."""
        return [self.child(i) for i in range(self.childCount())]

    def run(self):
        """Run checks inside this category groups."""
        log.info(f'Running Checks for {self.name()}')
        self.setIcon(0, Icons.check)
        for group_widget in self.get_children():
            group_widget.run()

        self.setIcon(0, self.icon())
        log.done('Category Checks Completed.')

    def fix(self):
        """Fix and re-run checks for this category."""
        log.warning('Run & Fix must be called from a single check')
