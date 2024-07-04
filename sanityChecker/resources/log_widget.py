# ----------------------------------------------------------------------------------------
# Maya Sanity Checker / Maximiliano Rocamora
# https://github.com/MaxRocamora/SanityChecker
# ----------------------------------------------------------------------------------------
import contextlib
import logging

from PySide2.QtWidgets import QPlainTextEdit
from PySide2.QtGui import QFont

COLORS = {
    logging.DEBUG: 'yellow',
    logging.INFO: 'white',
    logging.WARNING: 'orange',
    logging.ERROR: 'red',
    logging.CRITICAL: 'purple',
    55: 'lime',  # DONE
    57: 'yellow',  # HINT
    65: '#5dade2',  # PROCESS / color pallette c5
}


class QtLogger(logging.Handler):
    def __init__(self, parent: type, layout_widget: type, loggers: list):  # noqa: D107
        super().__init__()
        """creates the log widget and parent the loggers to the layout widget provided

        Args:
            parent (QtMainWindow): qt MainWindow
            layout_widget (QtLayoutWidget): the layout container for the text widget
            loggers (list): list of stream_loggers
        """

        # create output display widget, attach it to the layout widget
        self.widget = QPlainTextEdit(parent)
        layout_widget.addWidget(self.widget)

        # add loggers handlers to the widget
        self.loggers = []
        for log in loggers:
            self.loggers.append(log)
            log.addHandler(self)

        # set font, css, message format
        font = QFont('nosuchfont')
        font.setStyleHint(font.Monospace)
        self.widget.setFont(font)
        self.widget.setStyleSheet(
            """
                border: 3px solid rgb(80, 80, 80);
                color: rgb(255, 255, 255);
                background-color: rgb(20, 20, 20);
                """
        )
        self.widget.setReadOnly(True)
        self.setFormatter(logging.Formatter('%(levelname)-7s | %(message)s'))

    def close(self):
        """Removes all handlers from this widget."""
        for logger in self.loggers:
            if logger is not None:
                logger.removeHandler(self.widget)

    def emit(self, record: logging.LogRecord):
        """Writes the message formatted, uses font color based on error level number.

        Args:
            record: (logger record)
        """
        color = COLORS.get(record.levelno, 'white')
        msg = self.format(record)
        s = f"""<font color = "{color}" > {msg} </font>"""
        with contextlib.suppress(RuntimeError):
            self.widget.appendHtml(s)

    def clear(self):
        """Clears widget text."""
        self.widget.clear()
