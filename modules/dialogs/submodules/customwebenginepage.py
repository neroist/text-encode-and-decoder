"""
from https://www.pythonguis.com/faq/qwebengineview-open-links-new-window/
"""

from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
from PyQt5.QtWidgets import QMainWindow

class CustomWebEnginePage(QWebEnginePage):
    """
    Custom WebEnginePage to customize how we handle link navigation
    """
    # Store external windows.
    external_windows = []

    def acceptNavigationRequest(self, url,  _type, isMainFrame):
        if _type == QWebEnginePage.NavigationTypeLinkClicked:

            window = QMainWindow(self.parent())
            w = QWebEngineView(window)
            w.setUrl(url)
            window.setCentralWidget(w)
            window.show()


            # Keep reference to external window, so it isn't garbage collected.
            self.external_windows.append(window)
            return False

        return super().acceptNavigationRequest(url,  _type, isMainFrame)