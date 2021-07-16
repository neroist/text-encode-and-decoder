import ctypes
import logging
import sys
import colorlog

from PyQt5.QtCore import (
    QSize,
    QRect,
    QThread
)
from PyQt5.QtGui import (
    QFont,
    QIcon,
    QGuiApplication,
    QKeySequence
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
from modules.dialogs.replace import ReplaceDialog
from modules.dialogs.web import WebDialog
from modules.dialogs.find import FindDialog
from modules.stillworking import stillworking


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

        # prev font "MS Shell Dlg 2"

        tr = self.tr

        self.setGeometry(QRect(625, 350, 650, 600))
        self.setMinimumSize(QSize(650, 550))
        self.setStyleSheet(stylesheet)
        self.setWindowIcon(QIcon(u"icons/window icon.png"))
        self.setWindowTitle(tr("Encryption and Decryption Tool"))

        # window's central widget and the widget to place other widgets on
        # why? because some of the other widgets will not show if put directly on the main window
        self.__widget = QWidget(self)

        self.gridLayout = QGridLayout(self.__widget)

        self.methodComboBox = QComboBox(self.__widget)
        self.methodComboBox.setFont(QFont(u"Segoe UI", 11))
        self.methodComboBox.addItem(tr("ASCII85"))
        self.methodComboBox.addItem(tr("Base85"))
        self.methodComboBox.addItem(tr("Base64"))
        self.methodComboBox.addItem(tr("Base32"))
        self.methodComboBox.addItem(tr("Base16"))
        self.methodComboBox.addItem(tr("Url"))
        self.methodComboBox.addItem(tr("MD5 hash"))
        self.methodComboBox.addItem(tr("SHA-1"))
        self.methodComboBox.addItem(tr("SHA-256"))
        self.methodComboBox.addItem(tr("SHA-512"))
        self.methodComboBox.setMaxVisibleItems(4)
        self.methodComboBox.setCurrentIndex(2)
        self.methodComboBox.currentIndexChanged.connect(self.onComboBoxItemSelect)
        self.gridLayout.addWidget(self.methodComboBox, 5, 0, 1, 2)

        # Text edits for input and output. Plain text edits are used if the user wants to input a large amount of text.
        self.outputTextEdit = QPlainTextEdit(self.__widget)
        self.outputTextEdit.setFont(QFont(u"Segoe UI", 12))
        self.outputTextEdit.setReadOnly(True)
        self.gridLayout.addWidget(self.outputTextEdit, 10, 0, 1, 2)

        self.inputTextEdit = QPlainTextEdit(self.__widget)
        self.inputTextEdit.setFont(QFont(u"Segoe UI", 12))
        self.inputTextEdit.setAcceptDrops(True)
        self.gridLayout.addWidget(self.inputTextEdit, 1, 0, 1, 2)

        # ----- buttons -----
        self.encryptButton = QPushButton(tr("Encrypt"), self.__widget)
        self.encryptButton.setFont(QFont(u"Segoe UI", 12))
        self.encryptButton.clicked.connect(self.encodeUserText)
        self.gridLayout.addWidget(self.encryptButton, 11, 0, 1, 1)

        self.decryptButton = QPushButton(tr("Decrypt"), self.__widget)
        self.decryptButton.setFont(QFont("Segoe UI", 12))
        self.decryptButton.clicked.connect(self.decodeUserText)
        self.gridLayout.addWidget(self.decryptButton, 11, 1, 1, 1)

        # ----- labels -----
        self.inputLabel = QLabel(tr("Text to encrypt/decrypt:"), self.__widget)
        self.inputLabel.setFont(QFont(u"MS Shell Dlg 2", 16))
        self.gridLayout.addWidget(self.inputLabel, 0, 0, 1, 1)

        self.methodLabel = QLabel(tr("Method:"), self.__widget)
        self.methodLabel.setFont(QFont(u"MS Shell Dlg 2", 16))
        self.gridLayout.addWidget(self.methodLabel, 3, 0, 1, 1)

        self.outputLabel = QLabel(tr("Output:"), self.__widget)
        self.outputLabel.setFont(QFont(u"MS Shell Dlg 2", 16))
        self.gridLayout.addWidget(self.outputLabel, 8, 0, 1, 1)

        # ----- spacers -----
        spaceritem0 = QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.gridLayout.addItem(spaceritem0, 6, 0, 1, 2)

        spaceritem1 = QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.gridLayout.addItem(spaceritem1, 2, 0, 1, 2)

        # ----- actions -----

        _copy = QAction(tr("&Copy"), self)
        _copy.setShortcut(u"Alt+C")
        _copy.setStatusTip(tr("Copy output text."))
        _copy.triggered.connect(lambda: self.__copy_text)

        _paste = QAction(tr("&Paste"), self)
        _paste.setShortcut(u"Alt+V")
        _paste.setStatusTip(
            tr("Paste clipboard text to the input text edit. This will overwrite any data in the text edit."))
        _paste.triggered.connect(lambda: self.inputTextEdit.setPlainText(QGuiApplication.clipboard().text()))

        _cut = QAction(tr("C&ut"), self)
        _cut.setShortcut(u"Alt+X")
        _cut.setStatusTip(tr("Cut (delete and copy) all text from the input text edit."))
        _cut.triggered.connect(self.__cut_text)

        #find and replace submenu actions
        _find = QAction(tr("&Find"), self)
        _find.setShortcut(u"Ctrl+F")
        _find.triggered.connect(FindDialog(self).show)

        _replace = QAction(tr("&Replace"), self)
        _replace.setShortcut(u"Ctrl+R")
        _replace.triggered.connect(lambda: ReplaceDialog(self.inputTextEdit, self))

        _aboutqt = QAction(tr("About Qt"), self)
        _aboutqt.triggered.connect(lambda: QMessageBox.aboutQt(self, u"About Qt"))



        _credits = QAction(tr("Credits"), self)
        _credits.triggered.connect(lambda: stillworking(parent=self))
        
        _about = QAction(tr("About"), self)

        # ----- toolbar actions -----

        # windowbar actions
        self._fullscreen = QAction(QIcon("icons/full screen.png"), "", self)
        self._fullscreen.setStatusTip(tr("Enter full screen."))
        self._fullscreen.setToolTip(tr("Shortcut: Ctrl + F"))
        self._fullscreen.setShortcut(QKeySequence(u"Ctrl+F"))
        self._fullscreen.triggered.connect(self.__fullScreen)

        self._home = QAction(QIcon("icons/home.png"), "", self)
        self._home.setStatusTip(tr("Reset window geometry."))
        self._home.setToolTip(tr("Shortcut: Alt + H"))
        self._home.setShortcut(QKeySequence(u"Alt+H"))
        self._home.triggered.connect(lambda: self.setGeometry(QRect(625, 350, 650, 550)))

        _exit = QAction(QIcon("icons/exit.png"), "", self)
        _exit.setStatusTip(tr("Exit application."))
        _exit.setToolTip(tr("Shortcut: Ctrl + W"))
        _exit.setShortcut(QKeySequence(u"Ctrl+W"))
        _exit.triggered.connect(qApp.quit)

        # filebar actions
        _open = QAction(QIcon("icons/open file.png"), "", self)
        _open.setToolTip(tr("Shortcut: Ctrl + O"))
        _open.setShortcut(QKeySequence(u"Ctrl+O"))
        _open.setStatusTip(tr("Open text file. The file's content will be appended to the input text edit."))
        _open.triggered.connect(self.__open_file_dialogue)

        _save = QAction(QIcon("icons/save.png"), "", self)
        _save.setToolTip(tr("Shortcut: Ctrl + S"))
        _save.setShortcut(QKeySequence(u"Ctrl+S"))
        _save.setStatusTip(tr("Save the output's content to a text file."))
        _save.triggered.connect(self.__save_file_dialogue)


        # externalbar actions
        _web = QAction(QIcon("icons/web.png"), "", self)
        _web.setToolTip(tr("Shortcut: Ctrl + Alt + W"))
        _web.setShortcut(QKeySequence(u'Ctrl+Alt+W'))
        _web.setStatusTip(tr("Append a website's html code to the input text edit."))
        _web.triggered.connect(WebDialog(self.inputTextEdit, self).show)

        _speak = QAction(QIcon("icons/microphone.png"), "", self)
        _speak.setToolTip(tr("Shortcut: Ctrl + M or Alt + S"))
        _speak.setShortcuts((QKeySequence(u"Ctrl+M"), QKeySequence(u"Alt+S")))
        _speak.triggered.connect(lambda: stillworking(parent=self))

        # ----- menus -----
        editmenu = self.menuBar().addMenu(tr("&Edit"))
        helpmenu = self.menuBar().addMenu(QIcon(u"icons/i.jpg"), tr("&Help"))

        fnr = QMenu(tr("Find and Replace"), self)
        fnr.setFont(QFont("Segoe UI", 9))
        fnr.addActions((_find, _replace))

        editmenu.addActions((_copy, _paste, _cut))
        editmenu.setFont(QFont("Segoe UI", 9))
        editmenu.addSeparator()
        editmenu.addMenu(fnr)

        helpmenu.addActions((_aboutqt, _credits, _about))
        helpmenu.setFont(QFont("Segoe UI", 9))

        # ----- toolbar(s) -----
        windowbar = self.addToolBar(tr("Window Options"))
        filebar = self.addToolBar(tr("File Options"))
        externalbar = self.addToolBar(tr("Text Insertion Methods"))

        filebar.addActions((_open, _save))
        windowbar.addActions((_exit, self._fullscreen, self._home))
        externalbar.addActions((_web, _speak))

        # ----- statusbar -----
        statusbar = QStatusBar(self)
        statusbar.setSizeGripEnabled(False)  # disable size grip, size grip icon is broken.
        statusbar.setFont(QFont("Segoe UI", 9))
        statusbar.showMessage("© nonimportant All Rights Reserved")

        self.setStatusBar(statusbar)

        # ----- window setup -----
        self.setCentralWidget(self.__widget)
        self.show()

    def encodeUserText(self):
        a = encode(b := self.methodComboBox.currentText(), c := self.inputTextEdit.toPlainText())
        logger.debug(f'Attempted to encode "{c}" by {b}. Result: {a}')

        self.outputTextEdit.setPlainText(a)

    def decodeUserText(self):
        a = decode(b := self.methodComboBox.currentText(), c := self.inputTextEdit.toPlainText())
        logger.debug(f'Attempted to decode "{c}" by {b}. Result: {a}')

        self.outputTextEdit.setPlainText(a)

    def onComboBoxItemSelect(self, index: int):
        # self.methodComboBox.itemText(<index>)
        logger.log(MISC, f'Method "{self.methodComboBox.itemText(index)}" has been selected.')

        if self.methodComboBox.itemText(index).lower() == "MD5 hash":
            self.decryptButton.setEnabled(False)
        else:
            if not self.decryptButton.isEnabled():
                self.decryptButton.setEnabled(True)

    def __copy_text(self):
        try:
            QGuiApplication.clipboard().setText(self.outputTextEdit.toPlainText())
        except Exception as err:
            logger.error(f"An error was encountered while setting clipboard text. Error: {err}")

    def __cut_text(self):
        QGuiApplication.clipboard().setText(self.inputTextEdit.toPlainText())
        self.inputTextEdit.setPlainText("")

    def __open_file_dialogue(self):
        file, _ = QFileDialog.getOpenFileName(
            self,
            self.tr("Open File"),
            u"",
            self.tr("All Files (*);;Text Files (*.txt)")
        )

        if file:
            try:
                with open(file) as _f:
                    self.inputTextEdit.appendPlainText(_f.read())
            except Exception as err:
                logger.exception(f"Exception encountered when attempting to read file. Exception: {err}")
        else:
            return

    def __save_file_dialogue(self):
        file, _ = QFileDialog.getSaveFileName(
            self,
            self.tr("Save File As"),
            u"",
            self.tr("Text Files (*.txt)")
        )

        if file:
            with open(file, 'w+') as _f:
                _f.write(self.outputTextEdit.toPlainText())
        else:
            return

    def __fullScreen(self) -> None:
        tr = self.tr

        if self.isFullScreen():
            self.showNormal()
            self._fullscreen.setIcon(QIcon(u"icons/full screen.png"))
            self._fullscreen.setShortcut(u"Ctrl+F")
            self._fullscreen.setStatusTip(tr("Enter full screen"))
            self._fullscreen.setToolTip(tr("Shortcut: Ctrl + F"))
            self._home.setDisabled(False)
        else:
            self.showFullScreen()
            self._fullscreen.setIcon(QIcon(u"icons/exit full screen.png"))
            self._fullscreen.setShortcut(u'Esc')
            self._fullscreen.setStatusTip(tr("Exit full screen"))
            self._fullscreen.setToolTip(tr("Shortcut: Esc"))
            self._home.setDisabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("{}")
    # setting the AppUserModelID so our window icon also is our taskbar icon.
    # the AppUserModelID string has to be unicode as well.
    # info from https://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7

    ui = ConverterApplication()
    logger.info("Application started.")

    sys.exit(app.exec_())
