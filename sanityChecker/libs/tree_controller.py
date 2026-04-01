# ----------------------------------------------------------------------------------------
# Maya Sanity Checker / Maximiliano Rocamora
# https://github.com/MaxRocamora/SanityChecker
# ----------------------------------------------------------------------------------------
try:
    from PySide2.QtWidgets import QTreeWidgetItemIterator, QTreeWidget
except ImportError:
    from PySide6.QtWidgets import QTreeWidgetItemIterator, QTreeWidget

from collections import defaultdict

from sanityChecker.widgets.category import CategoryTreeItem
from sanityChecker.libs.check_loader import check_loader
from sanityChecker.libs.enums import CategoryGroups
from sanityChecker.config.config import CHECKS
from sanityChecker.resources.logger import sanity_stream_logger


log = sanity_stream_logger('SanityChecker')


class TreeController:
    def __init__(self, tree: QTreeWidget):
        """Initialize the TreeController.

        Args:
            tree (QTreeWidget): The tree widget to control.
        """
        self.tree = tree
        self.tree.clear()

        # build base dict with categories and groups
        self.checks = {}
        for key in CHECKS.keys():
            self.checks[key] = {group.value: [] for group in CategoryGroups}

        # Load checks into each category/group
        loaded_checks = check_loader()
        loaded_names = {check.filename() for check in loaded_checks}
        self._startup_self_check(loaded_names)

        for check in loaded_checks:
            for key in CHECKS.keys():
                if check.filename() in CHECKS[key]:
                    self.checks[key][check.group()].append(check)

        # load categories into tree
        for key in CHECKS.keys():
            CategoryTreeItem(self.tree, name=key, checks=self.checks[key])

    def _startup_self_check(self, loaded_names: set[str]):
        """Log startup diagnostics for configured and loaded checks."""
        configured_total = 0
        unresolved = set()
        check_categories = defaultdict(set)

        for category, configured_checks in CHECKS.items():
            configured_total += len(configured_checks)
            for check_name in configured_checks:
                check_categories[check_name].add(category)
                if check_name not in loaded_names:
                    unresolved.add(check_name)

        log.info(
            f'Startup self-check | loaded={len(loaded_names)} '
            f'| configured_refs={configured_total}'
        )

        if unresolved:
            log.warning(
                f'Startup self-check | unresolved configured checks '
                f'({len(unresolved)}): {", ".join(sorted(unresolved))}'
            )
        else:
            log.done('Startup self-check | unresolved configured checks: 0')

    def clear_tree(self):
        """Clears all checks and groups from the tree."""
        it = QTreeWidgetItemIterator(self.tree, QTreeWidgetItemIterator.All)
        while it.value():
            if it.value().item_type == 'group':
                it.value().reset_state()
            it += 1
