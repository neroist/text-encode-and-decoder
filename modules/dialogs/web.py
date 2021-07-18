from PyQt5.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QVBoxLayout,
    QLineEdit,
    QWidget,
    QMessageBox,
    QPushButton
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

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
        _.setFont(QFont("Segoe UI", 9))
        layout.addWidget(_)

        self.website = QLineEdit(self)
        self.website.setPlaceholderText(self.tr("eg. www.example.com"))
        self.website.setFont(QFont("Segoe UI", 9))
        layout.addWidget(self.website)

        __okay = QPushButton(self.tr("OK"), self)
        __okay.setFont(font := QFont("Segoe UI", 10))

        __cancel = QPushButton(self.tr("Cancel"), self)
        __cancel.setFont(font)

        buttonbox = QDialogButtonBox(Qt.Horizontal, self)
        buttonbox.addButton(__okay, QDialogButtonBox.AcceptRole)
        buttonbox.addButton(__cancel, QDialogButtonBox.RejectRole)
        layout.addWidget(buttonbox)

        buttonbox.accepted.connect(self.set_text)
        buttonbox.rejected.connect(self.reject)

    def test_url(self, url: str):
        try:
            get = requests.get(url)
            get.raise_for_status()

        except ConnectionError as err:
            a = QMessageBox.critical(
                self,
                "Connection Error",
                "There was an error connecting to the URL/URN provided.",
                QMessageBox.Ok
            )

            return None

        except InvalidURL:
            a = QMessageBox.critical(
                self,
                "Invalid URL/URN",
                "The URL or URN provided was invalid.",
                QMessageBox.Ok
            )

            return None

        except MissingSchema as err:
            a = QMessageBox.critical(
                self,
                "Missing Schema",
                err.__doc__,
                QMessageBox.Ok
            )

            return None

        except InvalidSchema as err:
            a = QMessageBox.critical(
                self,
                "Invalid Schema",
                f"The \"website\" {self.website.text} has an invalid schema.",
                QMessageBox.Ok
            )

            return None

        except HTTPError as err:
            a = QMessageBox.critical(
                self,
                "HTTP Error",
                f"{err.__doc__}\n{str(err)}",
                QMessageBox.Ok
            )

            return None

        except Exception as err:
            a = QMessageBox.critical(
                self,
                "Error",
                err.__doc__,
                QMessageBox.Ok
            )

        return get.text

    def set_text(self):
        # noinspection PyBroadException
        try:
            gt = requests.get("https://" + self.website.text())
            txt = gt.text
        except:
            txt = self.test_url(self.website.text())

            if txt is None:
                return
        else:
            self.inputwidget.appendPlainText(txt)
            self.accept()

# supports urns as well as urls
# catches all errors raised when trying to send a GET request to the given url/urn