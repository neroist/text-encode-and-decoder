from PyQt5.QtWidgets import (
    QDialog,
    QLabel,
    QGridLayout,
    QLineEdit,
    QDialogButtonBox,
    QWidget,
    QPushButton
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class ReplaceDialog(QDialog):

    def __init__(self, inputWidget: QWidget, parent=None) -> None:
        super(ReplaceDialog, self).__init__(parent)

        self.setWindowTitle(self.tr("Replace"))
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.resize(400, 150)


        self.gridLayout = QGridLayout(self)

        self._inputwidget = inputWidget

        replaceLabel = QLabel(self.tr("Replace:"), self)
        replaceLabel.setFont(font := QFont("Segoe UI", 10))
        self.gridLayout.addWidget(replaceLabel, 0, 0)

        self.replaceLineEdit = QLineEdit(self)
        self.replaceLineEdit.setFont(font)
        self.gridLayout.addWidget(self.replaceLineEdit, 1, 1)

        # -----------

        withLabel = QLabel(self.tr("With:"), self)
        withLabel.setFont(font)
        self.gridLayout.addWidget(withLabel, 1, 0)

        self.withLineEdit = QLineEdit(self)
        self.withLineEdit.setFont(font)
        self.gridLayout.addWidget(self.withLineEdit, 0, 1)

        # ----------- button box buttons -----------

        __ok = QPushButton(self.tr("OK"), self)
        __ok.setFont(buttonboxfont := QFont("Segoe UI"))

        __cancel = QPushButton(self.tr("Cancel"), self)
        __cancel.setFont(buttonboxfont)

        buttonBox = QDialogButtonBox(self)
        buttonBox.setOrientation(Qt.Horizontal)
        buttonBox.addButton(__ok, QDialogButtonBox.AcceptRole)
        buttonBox.addButton(__cancel, QDialogButtonBox.RejectRole)
        self.gridLayout.addWidget(buttonBox, 3, 1)

        buttonBox.accepted.connect(self.__replace)
        buttonBox.rejected.connect(self.reject)

        self.show()

    def __replace(self):
        txt = self._inputwidget.toPlainText()

        if txt:
            txt = str(txt).replace(self.withLineEdit.text(), self.replaceLineEdit.text())
            self._inputwidget.setPlainText(txt)
        else:
            self.accept()

        self.accept()
