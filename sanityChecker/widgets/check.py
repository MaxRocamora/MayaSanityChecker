# ----------------------------------------------------------------------------------------
# Maya Sanity Checker / Maximiliano Rocamora
# https://github.com/MaxRocamora/SanityChecker
# ----------------------------------------------------------------------------------------
from PySide2.QtWidgets import QTreeWidgetItem
from PySide2.QtGui import QColor

from sanityChecker.libs.enums import Status
from sanityChecker.widgets.maya_node import MayaNodeTreeItem
from sanityChecker.resources.resources import Icons
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')


class CheckTreeItem(QTreeWidgetItem):
    item_type = 'check'

    def __init__(self, parent: QTreeWidgetItem = None, name: str = '', check='', *args):
        """Check Tree Item for Sanity Checker."""
        super().__init__(parent, *args)
        self._name = name
        self._check = check
        self.setText(0, name)
        self.setIcon(0, check.stand_by_icon())
        self.setTextColor(0, QColor(235, 235, 235))

    def name(self):
        """Returns name of this check."""
        return self._name

    @property
    def check(self):
        """Returns check object for this widget."""
        return self._check

    def status(self):
        """Returns status of this check."""
        return self.check.status()

    def get_children(self):
        """Returns children widgets (checks)."""
        return [self.child(i) for i in range(self.childCount())]

    def callback_selected(self):
        """Callback when this check is selected."""
        log.info(f'Check Selected: {self.check.name()}')

    def run(self):
        """Run checks inside this category groups."""
        log.info(f'Running Check: {self.name()}')
        self.reset_state()
        self.check.run()
        self.format_widget()

    def fix(self):
        """Run checks inside this category groups."""
        if not self.check.has_autofix():
            log.warning(f'{self.check.name()} must be fixed manually')
            return

        self.run()
        self.check.fix()
        self.run()
        self.format_widget()

    def format_widget(self):
        """Visually format widget based on status."""
        self.setIcon(0, self.check.status_icon())

        if self.check.status() == Status.FAIL:
            log.warning(self.check.status_message())

            log.hint('-' * 50)
            for node in self.check.nodes():
                log.hint(node.name())

            log.hint('-' * 50)
            self.setText(0, '{} ({})'.format(self.name(), len(self.check.nodes())))
            self.setTextColor(0, QColor(255, 50, 50, 255))

            for node in self.check.nodes():
                self.addChild(MayaNodeTreeItem(self, name=node.name()))

        else:
            self.setText(0, self.name())
            self.setTextColor(0, QColor(230, 255, 230))
            self._remove_all_children()

    def show_hint(self):
        """Shows hint for this check."""
        log.hint('-' * 50)
        log.hint(self.check.fix_hint())
        log.hint('-' * 50)

    def reset_state(self):
        """Resets css state and check state."""
        self.setIcon(0, Icons.widget_check)
        self.setText(0, self.name())
        self.setIcon(0, self.check.stand_by_icon())
        self.setTextColor(0, QColor(235, 235, 235))
        self._remove_all_children()

    def _remove_all_children(self):
        for child in self.get_children():
            self.removeChild(child)
