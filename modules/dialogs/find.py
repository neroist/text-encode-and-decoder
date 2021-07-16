from PyQt5.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLineEdit,
    QLabel,
    QVBoxLayout
)
from PyQt5.QtCore import Qt

from modules import stillworking

class FindDialog(QDialog):
    def __init__(self, parent=None):
        super(FindDialog, self).__init__(parent)

        self.setWindowTitle("Find")

        layout = QVBoxLayout(self)

        label = QLabel("Find:", self)
        layout.addWidget(label)

        entry = QLineEdit(self)
        layout.addWidget(entry)

        buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        buttonbox.accepted.connect(self.__find_and_highlight)
        buttonbox.rejected.connect(self.reject)
        layout.addWidget(buttonbox)

    def __find_and_highlight(self):
        stillworking(parent=self)
        self.accept()

