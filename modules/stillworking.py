from PyQt5.QtWidgets import QMessageBox, QWidget

def stillworking(title: str = "Sorry", text: str = "I'm still working on this", parent: QWidget = None) -> None:
    """
    Display a "Still working" message.

    :param title: Message window title
    :param text: Message window text
    :param parent: Window parent widget

    :return: None
    """

    QMessageBox.information(parent, title, text, QMessageBox.Ok, QMessageBox.Ok)

# In a module because other modules need to use it