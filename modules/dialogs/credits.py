import os

from modules.dialogs.submodules.customwebenginepage import CustomWebEnginePage

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QFont


class CreditsDialog(QDialog):
    def __init__(self, parent=None):
        super(CreditsDialog, self).__init__(parent)

        self.setWindowTitle("Credits")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        self.resize(800, 625)

        Layout = QVBoxLayout(self)

        self.central = QWebEngineView(self)
        self.central.setPage(CustomWebEnginePage(self))
        self.central.setUrl(
            QUrl.fromLocalFile(
                os.path.abspath(
                    os.path.join(
                        os.path.split(
                            os.path.split(
                                __file__
                            )[0]
                        )[0], "html/credits.html"
                    )
                )
            )
        )

        Layout.addWidget(self.central)

        button = QPushButton(self.tr("OK"), self)
        button.setFont(QFont("Segoe UI"))
        button.clicked.connect(self.accept)
        Layout.addWidget(button)

