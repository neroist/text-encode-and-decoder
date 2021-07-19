"""
from https://www.pythonguis.com/faq/qwebengineview-open-links-new-window/
"""

from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
from PyQt5.QtGui import QDesktopServices

class CustomWebEnginePage(QWebEnginePage):
    """
    Custom WebEnginePage to customize how we handle link navigation
    """

    def acceptNavigationRequest(self, url,  _type, isMainFrame):
        if _type == QWebEnginePage.NavigationTypeLinkClicked:

            # Send the URL to the system default URL handler.
            QDesktopServices.openUrl(url)
            return False

        return super().acceptNavigationRequest(url,  _type, isMainFrame)