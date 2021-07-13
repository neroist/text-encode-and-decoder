import ctypes
import logging
import sys
import colorlog

from PyQt5.QtCore import (
    QSize,
    QRect
)
from PyQt5.QtGui import (
    QFont,
    QIcon,
    QGuiApplication
)
from PyQt5.QtWidgets import (
    QPushButton,
    QGridLayout,
    QComboBox,
    QPlainTextEdit,
    QApplication,
    QMainWindow,
    QSizePolicy,
    QSpacerItem,
    QWidget,
    QLabel,
    QAction,
    QMenu,
    QStatusBar,
    QMessageBox,
    QFileDialog,
    qApp
)

from modules import conversions
from modules.replace import ReplaceDialog


# global variables
with open("stylesheets/main.qss") as f:
    stylesheet = f.read()


# ----- functions -----
def decode(method: str, text: str) -> str:
    """
    Decode string by given method. Supported methods are: ascii85, base85, base64, base32, base16, and url.

    :param method: Method to decode text
    :param text: Text to decode
    :return: Decoded version of text
    """

    if text is None:
        return ""

    try:
        return conversions.decodings[method.lower().replace("-", '')](text)
    except Exception as err:
        logger.error(f'Ran into error encoding "{text}" through decryption method "{method}". Error: {err}')


def encode(method: str, text: str):
    """
    Encode string by given method. Supported methods are: ascii85, base85, base64, base32, base16, url, md5 hash, sha1,
    sha256, and sha512.

    :param method: Method to encode text
    :param text: Text to encode
    :return: Decoded version of text
    """

    if text is None:
        return ""

    if method == "MD5 hash":
        method = method.split(" ")[0]

    try:
        return conversions.encodings[method.lower().replace("-", '')](text)
    except Exception as err:
        logger.error(f'Ran into error decoding "{text}" through encryption method "{method}". Error: {err}')


# ----- logging setup -----
MISC = 1
logger = logging.getLogger(__name__)

log_colors = {
    'MISC': 'white',
    'DEBUG': 'green',
    'INFO': 'blue',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red'
}

formatter = colorlog.ColoredFormatter(
    fmt="%(log_color)s%(name)s [level %(levelno)s %(levelname)s %(asctime)s, line %(lineno)s] %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    log_colors=log_colors
)

handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)
handler.setLevel(MISC)

logger.addHandler(handler)
logging.addLevelName(MISC, 'MISC')
logger.setLevel(MISC)


# ----- application -----
class ConverterApplication(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(QRect(625, 350, 650, 600))
        self.setMinimumSize(QSize(650, 550))
        self.setStyleSheet(stylesheet)
        self.setWindowIcon(QIcon("icons/window icon.png"))
        self.setWindowTitle("Encryption and Decryption Tool")

        self.__widget = QWidget(self)

        self.gridLayout = QGridLayout(self.__widget)

        self.methodComboBox = QComboBox(self.__widget)
        self.methodComboBox.setFont(QFont("MS Shell Dlg 2", 11))
        self.methodComboBox.addItem("ASCII85")
        self.methodComboBox.addItem("Base85")
        self.methodComboBox.addItem("Base64")
        self.methodComboBox.addItem("Base32")
        self.methodComboBox.addItem("Base16")
        self.methodComboBox.addItem("Url")
        self.methodComboBox.addItem("MD5 hash")
        self.methodComboBox.addItem("SHA-1")
        self.methodComboBox.addItem("SHA-256")
        self.methodComboBox.addItem("SHA-512")
        # self.methodComboBox.addItem("Pig latin")
        self.methodComboBox.setMaxVisibleItems(4)
        self.methodComboBox.currentIndexChanged.connect(self.onComboBoxItemSelect)
        self.gridLayout.addWidget(self.methodComboBox, 5, 0, 1, 2)

        # Text edits for input and output. Plain text edits are used if the user wants to input a large amount of text.
        self.outputTextEdit = QPlainTextEdit(self.__widget)
        self.outputTextEdit.setFont(QFont("MS Shell Dlg 2", 12))
        self.outputTextEdit.setReadOnly(True)
        self.gridLayout.addWidget(self.outputTextEdit, 10, 0, 1, 2)

        self.inputTextEdit = QPlainTextEdit(self.__widget)
        self.inputTextEdit.setFont(QFont("MS Shell Dlg 2", 12))
        self.inputTextEdit.setAcceptDrops(True)
        self.gridLayout.addWidget(self.inputTextEdit, 1, 0, 1, 2)

        # ----- buttons -----
        self.encryptButton = QPushButton("Encrypt", self.__widget)
        self.encryptButton.setFont(QFont("MS Shell Dlg 2", 13))
        self.encryptButton.clicked.connect(self.encodeUserText)
        self.gridLayout.addWidget(self.encryptButton, 11, 0, 1, 1)

        self.decryptButton = QPushButton("Decrypt", self.__widget)
        self.decryptButton.setFont(QFont("MS Shell Dlg 2", 13))
        self.decryptButton.clicked.connect(self.decodeUserText)
        self.gridLayout.addWidget(self.decryptButton, 11, 1, 1, 1)

        # ----- labels -----
        self.inputLabel = QLabel("Text to encrypt/decrypt:", self.__widget)
        self.inputLabel.setFont(QFont("MS Shell Dlg 2", 14))
        self.gridLayout.addWidget(self.inputLabel, 0, 0, 1, 1)

        self.outputLabel = QLabel("Output:", self.__widget)
        self.outputLabel.setFont(QFont("MS Shell Dlg 2", 14))
        self.gridLayout.addWidget(self.outputLabel, 8, 0, 1, 1)

        self.methodLabel = QLabel("Method:", self.__widget)
        self.methodLabel.setFont(QFont("MS Shell Dlg 2", 14))
        self.gridLayout.addWidget(self.methodLabel, 3, 0, 1, 1)

        # ----- spacers -----
        spaceritem0 = QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.gridLayout.addItem(spaceritem0, 6, 0, 1, 2)

        spaceritem1 = QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.gridLayout.addItem(spaceritem1, 2, 0, 1, 2)

        # ----- actions -----
        _open = QAction(QIcon("icons/open file.png"), "", self)
        _open.setToolTip("Shortcut: Ctrl + O")
        _open.setShortcut("Ctrl+O")
        _open.setStatusTip("Open text file. The file's content will be appended to the input text edit.")
        _open.triggered.connect(self.__open_file_dialogue)

        _save = QAction(QIcon("icons/save.png"), "", self)
        _save.setToolTip("Shortcut: Ctrl + S")
        _save.setShortcut("Ctrl+S")
        _save.setStatusTip("Save the output's content to a text file.")
        _save.triggered.connect(self.__save_file_dialogue)

        _copy = QAction("&Copy", self)
        _copy.setShortcut("Alt+C")
        _copy.setStatusTip("Copy output text.")
        _copy.triggered.connect(lambda: QGuiApplication.clipboard().setText(self.outputTextEdit.toPlainText()))

        _paste = QAction("&Paste", self)
        _paste.setShortcut("Alt+V")
        _paste.setStatusTip(
            "Paste clipboard text to the input text edit. This will overwrite any data in the text edit.")
        _paste.triggered.connect(lambda: self.inputTextEdit.setPlainText(QGuiApplication.clipboard().text()))

        _cut = QAction("C&ut", self)
        _cut.setShortcut("Alt+X")
        _cut.setStatusTip("Cut (delete and copy) all text from the input text edit.")
        _cut.triggered.connect(self.__cut_text)

        _find = QAction("&Find", self)
        _find.setShortcut("Ctrl+F")

        _replace = QAction("&Replace", self)
        _replace.setShortcut("Ctrl+R")
        _replace.triggered.connect(lambda: ReplaceDialog(self.inputTextEdit, self.styleSheet(), self))

        _aboutqt = QAction("About Qt", self)
        _aboutqt.triggered.connect(lambda: QMessageBox.aboutQt(self, "About Qt"))

        _credits = QAction("Credits", self)
        _about = QAction("About", self)

        # ----- toolbar actions -----
        self._fullscreen = QAction(QIcon("icons/full screen.png"), "", self)
        self._fullscreen.setStatusTip("Enter full screen")
        self._fullscreen.setToolTip("Shortcut: Ctrl + F")
        self._fullscreen.setShortcut("Ctrl+F")
        self._fullscreen.triggered.connect(self.__fullScreen)

        self._home = QAction(QIcon("icons/home.png"), "", self)
        self._home.setStatusTip("Reset window geometry.")
        self._home.setToolTip("Shortcut: Alt + H")
        self._home.setShortcut("Alt+H")
        self._home.triggered.connect(lambda: self.setGeometry(QRect(625, 350, 650, 550)))

        _exit = QAction(QIcon("icons/exit.png"), "", self)
        _exit.setStatusTip("Exit application.")
        _exit.setToolTip("Shortcut: Ctrl + W")
        _exit.setShortcut("Ctrl+W")
        _exit.triggered.connect(qApp.quit)

        # menus
        editmenu = self.menuBar().addMenu("&Edit")
        helpmenu = self.menuBar().addMenu(QIcon("icons/i.jpg"), "&Help")

        fnr = QMenu("Find and Replace", self)
        fnr.addActions((_find, _replace))

        editmenu.addActions((_copy, _paste, _cut))
        editmenu.addSeparator()
        editmenu.addMenu(fnr)

        helpmenu.addActions((_aboutqt, _credits, _about))

        # ----- toolbar(s) -----
        optionbar = self.addToolBar("Window")
        filebar = self.addToolBar("File")

        filebar.addActions((_open, _save))
        optionbar.addActions((_exit, self._fullscreen, self._home))

        # ----- statusbar -----
        statusbar = QStatusBar(self)
        statusbar.setSizeGripEnabled(False)  # disable size grip, size grip icon is broken.

        self.setStatusBar(statusbar)

        # ----- window setup -----
        self.methodComboBox.setCurrentIndex(2)
        self.setCentralWidget(self.__widget)
        self.show()

    def encodeUserText(self) -> None:
        a = encode(b := self.methodComboBox.currentText(), c := self.inputTextEdit.toPlainText())
        logger.debug(f'Attempted to encode "{c}" by {b}. Result: {a}')

        self.outputTextEdit.setPlainText(a)

    def decodeUserText(self) -> None:
        a = decode(b := self.methodComboBox.currentText(), c := self.inputTextEdit.toPlainText())
        logger.debug(f'Attempted to decode "{c}" by {b}. Result: {a}')

        self.outputTextEdit.setPlainText(a)

    def onComboBoxItemSelect(self, index: int) -> None:
        # self.methodComboBox.itemText(<index>)
        logger.log(MISC, f'Method "{self.methodComboBox.itemText(index)}" has been selected.')

        if self.methodComboBox.itemText(index).lower() == "MD5 hash":
            self.decryptButton.setEnabled(False)
        else:
            if not self.decryptButton.isEnabled():
                self.decryptButton.setEnabled(True)

    def __cut_text(self):
        QGuiApplication.clipboard().setText(self.inputTextEdit.toPlainText())
        self.inputTextEdit.setPlainText("")

    def __open_file_dialogue(self) -> None:
        file, _ = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "",
            "All Files (*);;Text Files (*.txt)"
        )

        if file:
            try:
                with open(file) as f:
                    self.inputTextEdit.appendPlainText(f.read())
            except Exception as err:
                logger.error(f"Exception encountered when attempting to read file. Exception: {err}")
        else:
            return

    def __save_file_dialogue(self) -> None:
        file, _ = QFileDialog.getSaveFileName(
            "Save file",
            "",
            "Text Files (*.txt)"
        )

        if file:
            with open(file, 'w+') as f:
                f.write(self.outputTextEdit.toPlainText())
        else:
            return

    def __fullScreen(self) -> None:
        if self.isFullScreen():
            self.showNormal()
            self._fullscreen.setIcon(QIcon("icons/full screen.png"))
            self._fullscreen.setShortcut("Ctrl+F")
            self._fullscreen.setStatusTip("Enter full screen")
            self._fullscreen.setToolTip("Shortcut: Ctrl + F")
            self._home.setDisabled(False)
        else:
            self.showFullScreen()
            self._fullscreen.setIcon(QIcon("icons/exit full screen.png"))
            self._fullscreen.setShortcut('Esc')
            self._fullscreen.setStatusTip("Exit full screen")
            self._fullscreen.setToolTip("Shortcut: Esc")
            self._home.setDisabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(u"{}".format(__name__))
    # setting the AppUserModelID so our window icon also is our taskbar icon.
    # the AppUserModelID string has to be unicode as well.
    # info from https://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7

    ui = ConverterApplication()
    logger.info("Application started.")

    sys.exit(app.exec_())
