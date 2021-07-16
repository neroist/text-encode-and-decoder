from PyQt5.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QVBoxLayout,
    QLineEdit,
    QWidget,
    QMessageBox
)
from PyQt5.QtCore import Qt

import requests
from requests.exceptions import *

class WebDialog(QDialog):
    def __init__(self, inputWidget: QWidget, parent=None):
        super(WebDialog, self).__init__(parent)

        self.setWindowTitle("Enter Website URL")
        self.resize(500, 100)
        self.setMinimumSize(225, 100)
        self.setMaximumSize(500, 100)

        self.inputwidget = inputWidget

        layout = QVBoxLayout(self)

        _ = QLabel("Enter website URL:")
        layout.addWidget(_)

        self.website = QLineEdit(self)
        self.website.setPlaceholderText("eg. www.example.com")
        layout.addWidget(self.website)

        buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        layout.addWidget(buttonbox)
        buttonbox.accepted.connect(self.set_text)
        buttonbox.rejected.connect(self.reject)

    def set_text(self):
        try:
            get = requests.get(self.website.text())
            get.raise_for_status()

        except ConnectionError as err:
            a = QMessageBox.critical(
                self,
                "Error",
                "There was an error connecting to the URL provided.",
                QMessageBox.Ok
            )

            return

        except InvalidURL:
            a = QMessageBox.critical(
                self,
                "Error",
                "The URL provided was invalid.",
                QMessageBox.Ok
            )

            return

        except MissingSchema as err:
            a = QMessageBox.critical(
                self,
                "Error",
                err.__doc__,
                QMessageBox.Ok
            )

            return

        except HTTPError as err:
            a = QMessageBox.critical(
                self,
                "Error",
                str(err),
                QMessageBox.Ok
            )

            return

        self.inputwidget.appendPlainText(get.text)
        self.accept()
