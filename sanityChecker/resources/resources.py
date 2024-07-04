# ----------------------------------------------------------------------------------------
# Maya Sanity Checker / Maximiliano Rocamora
# https://github.com/MaxRocamora/SanityChecker
# ----------------------------------------------------------------------------------------
import os
from PySide2.QtGui import QIcon, QPixmap, QColor
from PySide2.QtCore import QSize
from PySide2.QtWidgets import QMainWindow, QPushButton, QGraphicsDropShadowEffect

# base folder for Icons
icon_path = os.path.join(os.path.dirname(__file__), 'icons')


class _Icons:
    def __init__(self):
        """Store all png Icons as QIcons into this class."""
        for icon_file in os.listdir(icon_path):
            key = os.path.splitext(icon_file)[0]
            setattr(self, key, QIcon(os.path.join(icon_path, icon_file)))


Icons = _Icons()

# store png in QPixmap for label widgets
PIXMAP = {
    'pass': QPixmap(os.path.join(icon_path, 'pass.png')),
    'fail': QPixmap(os.path.join(icon_path, 'fail.png')),
    'stand_by': QPixmap(os.path.join(icon_path, 'stand_by.png')),
}


def ui_style_button(ui: QMainWindow, button_widget: QPushButton, icon: QIcon):
    """Applies a style on given qt button."""
    button_widget.setIcon(icon)
    button_widget.setIconSize(QSize(22, 22))
    shadow = QGraphicsDropShadowEffect(ui)
    shadow.setBlurRadius(6)
    shadow.setOffset(3)
    shadow.setColor(QColor(0, 0, 0, 60))
    button_widget.setGraphicsEffect(shadow)
    button_widget.installEventFilter(ui)
