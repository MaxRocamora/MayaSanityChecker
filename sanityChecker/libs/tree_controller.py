# ----------------------------------------------------------------------------------------
# Maya Sanity Checker / Maximiliano Rocamora
# https://github.com/MaxRocamora/SanityChecker
# ----------------------------------------------------------------------------------------
from PySide2.QtWidgets import QTreeWidgetItemIterator, QTreeWidget

from sanityChecker.widgets.category import CategoryTreeItem
from sanityChecker.libs.check_loader import check_loader
from sanityChecker.libs.enums import CategoryGroups
from sanityChecker.config.config import CHECKS


class TreeController:
    def __init__(self, tree: QTreeWidget):
        """Handles qt tree operations."""
        self.tree = tree
        self.tree.clear()

        # build base dict with categories and groups
        self.checks = {}
        for key in CHECKS.keys():
            self.checks[key] = {group.value: [] for group in CategoryGroups}

        # Load checks into each category/group
        for check in check_loader():
            for key in CHECKS.keys():
                if check.filename() in CHECKS[key]:
                    self.checks[key][check.group()].append(check)

        # load categories into tree
        for key in CHECKS.keys():
            CategoryTreeItem(self.tree, name=key, checks=self.checks[key])

    def clear_tree(self):
        """Clears all checks and groups from the tree."""
        it = QTreeWidgetItemIterator(self.tree, QTreeWidgetItemIterator.All)
        while it.value():
            if it.value().item_type == 'group':
                it.value().reset_state()
            it += 1
