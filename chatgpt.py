import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QPushButton, QAction, QToolBar, QTabWidget, QTabBar, QFrame
from PyQt5.QtWebEngineWidgets import QWebEngineView


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('BharatBrowser')
        self.setGeometry(100, 100, 1200, 800)
        
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('https://www.google.com'))

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        self.tabs = QTabWidget()
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.open_new_tab)
        self.tabs.currentChanged.connect(self.update_url_bar)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        self.init_ui()
        
    def init_ui(self):
        # Set window icon
        self.setWindowIcon(QIcon('D:/code playground/web browser/browser.png'))  # Replace with your logo file path

        # Navigation buttons
        navtb = QToolBar("Navigation")
        self.addToolBar(navtb)

        back_btn = QAction('Back', self)
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navtb.addAction(back_btn)

        forward_btn = QAction('Forward', self)
        forward_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(forward_btn)

        reload_btn = QAction('Reload', self)
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addAction(reload_btn)

        home_btn = QAction('Home', self)
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        navtb.addSeparator()

        navtb.addWidget(self.url_bar)

        go_btn = QPushButton('Go')
        go_btn.clicked.connect(self.navigate_to_url)
        navtb.addWidget(go_btn)

        new_tab_btn = QPushButton('+')
        new_tab_btn.clicked.connect(self.open_new_tab)
        navtb.addWidget(new_tab_btn)

        # Set initial tab
        self.tabs.addTab(self.browser, "New Tab")
        self.setCentralWidget(self.tabs)

        # Styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2E2E2E;
            }
            QToolBar {
                background-color: #4B4B4B;
                spacing: 10px;
                padding: 5px;
            }
            QLineEdit {
                max-width: 600px;
                padding: 5px;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #5C5C5C;
                border: none;
                padding: 5px 10px;
                border-radius: 5px;
                color: white;
            }
            QPushButton:hover {
                background-color: #7D7D7D;
            }
            QPushButton:pressed {
                background-color: #999999;
            }
        """)

    def navigate_to_url(self):
        url = self.url_bar.text()
        if '.' in url and ' ' not in url:
            if not url.startswith('http'):
                url = 'http://' + url
        else:
            url = 'https://www.google.com/search?q=' + url
        self.tabs.currentWidget().setUrl(QUrl(url))

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl('https://www.google.com'))

    def open_new_tab(self, i=-1):
        browser = QWebEngineView()
        browser.setUrl(QUrl('https://www.google.com'))
        i = self.tabs.addTab(browser, "New Tab")
        self.tabs.setCurrentIndex(i)
        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_tab_title(browser))

    def close_current_tab(self, i):
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)

    def update_tab_title(self, browser):
        i = self.tabs.indexOf(browser)
        if i != -1:
            self.tabs.setTabText(i, browser.page().title())

    def update_url_bar(self, i):
        qurl = self.tabs.currentWidget().url()
        self.url_bar.setText(qurl.toString())
        self.update_tab_title(self.tabs.currentWidget())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())
