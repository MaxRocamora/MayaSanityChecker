# ----------------------------------------------------------------------------------------
# Maya Sanity Checker / Maximiliano Rocamora
# https://github.com/MaxRocamora/SanityChecker
# ----------------------------------------------------------------------------------------
from PySide2.QtWidgets import QTreeWidgetItem

from sanityChecker.libs.enums import Status
from sanityChecker.widgets.check import CheckTreeItem
from sanityChecker.resources.resources import Icons
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')


class GroupTreeItem(QTreeWidgetItem):
    item_type = 'group'

    def __init__(self, parent: QTreeWidgetItem, name: str, checks: list):
        """Group Tree Item for Sanity Checker."""
        super().__init__(parent)
        self._name = name
        self.setText(0, str(name))
        self.setIcon(0, self.icon())
        self.load_checks(checks)

    def load_checks(self, checks: list):
        """Load checks into the tree."""
        for check in checks:
            CheckTreeItem(self, name=check.name(), check=check)

    def category(self):
        """Returns category widget of this group."""
        return self.parent().name()

    def name(self):
        """Returns name of this category group."""
        return self._name

    def icon(self):
        """Returns icon for this category group."""
        return Icons.widget_group

    def callback_selected(self):
        """Callback when this category group is selected."""
        pass

    def get_children(self):
        """Returns children widgets (checks)."""
        return [self.child(i) for i in range(self.childCount())]

    def run(self):
        """Run checks inside this category groups."""
        _error = False
        self.setIcon(0, Icons.check)
        for check_widget in self.get_children():
            check_widget.run()
            if check_widget.status() == Status.FAIL:
                _error = True

        # if at least one check failed, set group icon to failed
        self.setIcon(0, Icons.failed) if _error else self.setIcon(0, Icons.passed)

    def fix(self):
        """Fix and re-run checks for this category group."""
        log.warning('Run & Fix must be called from a single check')

    def reset_state(self):
        """Resets css state and check state."""
        self.setIcon(0, self.icon())
        for check_widget in self.get_children():
            check_widget.reset_state()
