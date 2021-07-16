from PyQt5.QtWidgets import (
    QDialog,
    QLabel,
    QGridLayout,
    QLineEdit,
    QDialogButtonBox,
    QWidget
)
from PyQt5.QtCore import Qt


class ReplaceDialog(QDialog):

    def __init__(self, inputWidget: QWidget, parent=None) -> None:
        super(ReplaceDialog, self).__init__(parent)

        self.resize(400, 150)
        self.setWindowTitle("Replace")

        self.gridLayout = QGridLayout(self)

        self._inputwidget = inputWidget

        self.withLabel = QLabel("With:", self)
        self.gridLayout.addWidget(self.withLabel, 1, 0)

        self.withLineEdit = QLineEdit(self)
        self.gridLayout.addWidget(self.withLineEdit, 0, 1)

        self.replaceLabel = QLabel("Replace:", self)
        self.gridLayout.addWidget(self.replaceLabel, 0, 0)

        self.replaceLineEdit = QLineEdit(self)
        self.gridLayout.addWidget(self.replaceLineEdit, 1, 1)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.gridLayout.addWidget(self.buttonBox, 3, 1)

        self.buttonBox.accepted.connect(self.__replace)
        self.buttonBox.rejected.connect(self.reject)

        self.show()

    def __replace(self):
        txt = self._inputwidget.toPlainText()

        if txt:
            txt = str(txt).replace(self.withLineEdit.text(), self.replaceLineEdit.text())
            self._inputwidget.setPlainText(txt)
        else:
            self.accept()

        self.accept()
