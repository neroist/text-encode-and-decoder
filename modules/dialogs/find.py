from PyQt5.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLineEdit,
    QLabel,
    QVBoxLayout,
    QPushButton
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from modules import stillworking

class FindDialog(QDialog):
    def __init__(self, parent=None):
        super(FindDialog, self).__init__(parent)

        self.setWindowTitle("Find")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        layout = QVBoxLayout(self)

        label = QLabel("Find:", self)
        label.setFont(QFont("Segoe UI", 10))
        layout.addWidget(label)

        entry = QLineEdit(self)
        entry.setFont(QFont("Segoe UI", 9))
        layout.addWidget(entry)

        __k = QPushButton(self.tr("OK"), self)
        __k.setFont(font := QFont("Segoe UI"))

        __cancel = QPushButton(self.tr("Cancel"), self)
        __cancel.setFont(font)

        buttonbox = QDialogButtonBox(Qt.Horizontal, self)
        buttonbox.addButton(__k, QDialogButtonBox.AcceptRole)
        buttonbox.addButton(__cancel, QDialogButtonBox.RejectRole)
        buttonbox.accepted.connect(self.__find_and_highlight)
        buttonbox.rejected.connect(self.reject)
        layout.addWidget(buttonbox)

    def __find_and_highlight(self):
        stillworking.stillworking(parent=self)
        self.accept()
