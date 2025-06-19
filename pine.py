import sys
import configparser
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget,
    QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QInputDialog
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

# Read config.ini
config = configparser.ConfigParser()
config.read('config.ini')
homepage = config['Browser']['Homepage']
name = config['App']['Name']
mode = config['App']['Mode']
debug = config['Developer']['Debug']

class BrowserTab(QWidget):
    def __init__(self, url):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(url))

        # Navigation bar
        nav_bar = QHBoxLayout()
        self.url_bar = QLineEdit()
        self.url_bar.setText(url)
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        back_btn = QPushButton('<')
        back_btn.clicked.connect(self.browser.back)
        forward_btn = QPushButton('>')
        forward_btn.clicked.connect(self.browser.forward)
        reload_btn = QPushButton('Reload')
        reload_btn.clicked.connect(self.browser.reload)

        nav_bar.addWidget(back_btn)
        nav_bar.addWidget(forward_btn)
        nav_bar.addWidget(reload_btn)
        nav_bar.addWidget(self.url_bar)

        self.layout.addLayout(nav_bar)
        self.layout.addWidget(self.browser)

        # Update URL bar when page changes
        self.browser.urlChanged.connect(self.update_url_bar)

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith('http'):
            url = 'http://' + url
        self.browser.setUrl(QUrl(url))

    def update_url_bar(self, qurl):
        self.url_bar.setText(qurl.toString())

class TabbedBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{name} (Pine engine v.01)")
        self.setGeometry(100, 100, 1200, 800)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        # Toolbar with New Tab button
        toolbar = QWidget()
        toolbar_layout = QHBoxLayout()
        new_tab_btn = QPushButton("New Tab")
        new_tab_btn.clicked.connect(self.open_new_tab_dialog)
        toolbar_layout.addWidget(new_tab_btn)
        toolbar_layout.addStretch()
        toolbar.setLayout(toolbar_layout)

        # Layout for toolbar + tabs
        main_layout = QVBoxLayout()
        main_layout.addWidget(toolbar)
        main_layout.addWidget(self.tabs)
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.add_new_tab(homepage, 'Homepage')

        # Optional: Double-click tab bar to open new tab
        self.tabs.tabBarDoubleClicked.connect(self.on_tab_doubleclick)

    def add_new_tab(self, url, label):
        new_tab = BrowserTab(url)
        i = self.tabs.addTab(new_tab, label)
        self.tabs.setCurrentIndex(i)

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def on_tab_doubleclick(self, index):
        # Double-click empty area to open a new tab
        if index == -1:
            self.add_new_tab(homepage, "New Tab")

    def open_new_tab_dialog(self):
        url, ok1 = QInputDialog.getText(self, "New Tab", "Enter website URL:")
        if ok1 and url:
            tab_name, ok2 = QInputDialog.getText(self, "New Tab", "Enter tab name:")
            if ok2 and tab_name:
                self.add_new_tab(url, tab_name)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("pine.png"))  # Set your pine tree icon here
    window = TabbedBrowser()
    window.show()
    sys.exit(app.exec_())
