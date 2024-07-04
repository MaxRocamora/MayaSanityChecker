# ----------------------------------------------------------------------------------------
# Maya Sanity Checker / Maximiliano Rocamora
# https://github.com/MaxRocamora/SanityChecker
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds

from PySide2.QtCore import Qt
from PySide2 import QtUiTools
from PySide2.QtWidgets import QMenu, QAction, QMainWindow, QTreeWidgetItem
from PySide2.QtGui import QCursor

from sanityChecker.libs.tree_controller import TreeController
from sanityChecker.resources.loader_maya import get_maya_window
from sanityChecker.resources.resources import Icons, PIXMAP, ui_style_button
from sanityChecker.resources.logger import sanity_stream_logger
from sanityChecker.resources.log_widget import QtLogger
from sanityChecker.libs.enums import severity_colors, SeverityLevels, Status
from sanityChecker.version import __qt__, version, app_name, ui_file


log = sanity_stream_logger('SanityChecker')


class SanityChecker(QMainWindow):
    def __init__(self, parent=get_maya_window()):
        """Main Qt App for Sanity Checker.."""
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setObjectName(__qt__)
        self.ui = QtUiTools.QUiLoader().load(ui_file)
        self.setFixedSize(self.ui.maximumWidth(), self.ui.maximumHeight())
        self.setCentralWidget(self.ui)
        self.move(parent.geometry().center() - self.ui.geometry().center())
        self.setWindowIcon(Icons.app)
        self.setWindowTitle(' '.join([app_name, version]))
        self.show()

        self.loggers = QtLogger(self, self.ui.log_layout, [log])
        self.tree_controller = TreeController(self.ui.main_tree)
        self.set_connections_and_css()
        self.clear_ui()

    def set_connections_and_css(self):
        """Sets connections for UI elements."""
        self.ui.main_tree.itemClicked.connect(self.item_clicked)
        self.ui.main_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.main_tree.customContextMenuRequested.connect(self.open_menu)
        self.ui.btn_run_selected.clicked.connect(self.run_category_button)
        self.ui.btn_clear.clicked.connect(self.clear_ui)
        ui_style_button(self.ui, self.ui.btn_run_selected, Icons.button_run)
        ui_style_button(self.ui, self.ui.btn_clear, Icons.button_clear)
        self.ui.pb_error_level.setVisible(0)

    def clear_ui(self):
        """Resets visual state for groups and checks."""
        self.tree_controller.clear_tree()
        self._set_Icons_for_checks('stand_by')
        self.ui.grp_category.setTitle('Category')
        self.ui.lbl_failed_nodes.setText('0')
        log.info(' '.join([app_name, version]))
        log.hint('Select your category, open context menu and select [Run]')

    def run_category_button(self):
        """Runs selected category."""
        item = self.ui.main_tree.selectedItems()
        if not item:
            log.warning('Select a category first')
            return

        if item[0].item_type == 'category':
            self.run_category(item[0])
        else:
            item[0].run()

    def item_clicked(self, item: QTreeWidgetItem, column):
        """Click callback on tree widgets."""
        self.ui.lbl_check_name.setText('Check Name')
        self.ui.lbl_check_level.setText('0')
        self.ui.pb_error_level.setVisible(0)
        self.ui.te_error_description.clear()
        if item.item_type == 'category':
            self.ui.grp_category.setTitle(item.name())
        if item.item_type == 'check':
            self.ui.lbl_check_name.setText(item.check.name())
            self.ui.lbl_check_level.setText(str(item.check.level()))
            self.ui.te_error_description.setText(item.check.description())
            self._set_style_progress_bar(item.check.level())
        item.callback_selected()

    def _set_style_progress_bar(self, value: int):
        """Sets color of check error level bar."""
        if value <= 0:
            return

        css = (
            """QProgressBar::chunk {
                background-color: rgb({color});
                margin: 5px; border-radius: 1px;
            }."""
        ).replace('{color}', severity_colors.get(value, '0, 255, 255'))

        self.ui.pb_error_level.setValue(value)
        self.ui.pb_error_level.setStyleSheet(css)
        self.ui.pb_error_level.setVisible(1)

    def open_menu(self, QPoint):
        """Opens right click menu."""
        item = self.ui.main_tree.selectedItems()[0]
        self.menu = QMenu()

        if item.item_type == 'category':
            action_run_category = QAction(
                Icons.button_run, 'Run Checks on this Category', self.menu
            )
            self.menu.addAction(action_run_category)
            action_run_category.triggered.connect(lambda: self.run_category(item))
            self.menu.addSeparator()

        if item.item_type == 'group':
            action_run_group = QAction(
                Icons.button_run, 'Run Checks on this Group', self.menu
            )
            self.menu.addAction(action_run_group)
            action_run_group.triggered.connect(lambda: item.run())
            self.menu.addSeparator()

        if item.item_type == 'check':
            action_run_check = QAction(Icons.button_run, 'Run this Check', self.menu)
            self.menu.addAction(action_run_check)
            action_run_check.triggered.connect(lambda: item.run())
            self.menu.addSeparator()

            action_fix_check = QAction(
                Icons.menu_fix, 'Fix && Re-Run this check', self.menu
            )
            self.menu.addAction(action_fix_check)
            action_fix_check.triggered.connect(lambda: item.fix())
            self.menu.addSeparator()

            action_show_hint = QAction(Icons.menu_hint, 'Show Hint', self.menu)
            self.menu.addAction(action_show_hint)
            action_show_hint.triggered.connect(lambda: item.show_hint())
            self.menu.addSeparator()

        self.menu.popup(QCursor.pos())

    def run_category(self, item: QTreeWidgetItem):
        """Runs a complete category."""
        log.process('-' * 50)
        failed_nodes = 0
        self._set_Icons_for_checks('pass')
        item.run()

        # flag Icons for failed checks
        for group in item.get_children():
            for check_widget in group.get_children():
                if check_widget.status() != Status.PASS:
                    failed_nodes += 1
                    if check_widget.check.level() == SeverityLevels.CRITICAL.value:
                        self.ui.lbl_icon_1.setPixmap(PIXMAP['fail'])
                    if check_widget.check.level() == SeverityLevels.HIGH.value:
                        self.ui.lbl_icon_2.setPixmap(PIXMAP['fail'])
                    if check_widget.check.level() == SeverityLevels.MODERATE.value:
                        self.ui.lbl_icon_3.setPixmap(PIXMAP['fail'])

        self.ui.lbl_failed_nodes.setText(str(failed_nodes))

    def _set_Icons_for_checks(self, icon_name: str):
        """Sets Icons for check icon status."""
        self.ui.lbl_icon_1.setPixmap(PIXMAP[icon_name])
        self.ui.lbl_icon_2.setPixmap(PIXMAP[icon_name])
        self.ui.lbl_icon_3.setPixmap(PIXMAP[icon_name])

    def closeEvent(self, event):  # noqa: D102
        self.loggers.close()
        self.close()


# ----------------------------------------------------------------------------------------
# MAIN
# ----------------------------------------------------------------------------------------


def load():
    """Load sanity checker UI."""
    if cmds.window(__qt__, q=1, ex=1):
        cmds.deleteUI(__qt__)
    SanityChecker()
