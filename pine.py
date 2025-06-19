import sys
import configparser
import qdarkstyle
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget,
    QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QInputDialog
)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor

from adblockparser import AdblockRules


# Read config.ini
config = configparser.ConfigParser()
config.read('config.ini')
homepage = config['Browser']['Homepage']
name = config['App']['Name']
mode = config['App']['Mode']
debug = config['Developer']['Debug'] == "True"

class AdBlocker(QWebEngineUrlRequestInterceptor):
    def __init__(self, adblock_rules):
        super().__init__()
        self.adblock_rules = adblock_rules

    def interceptRequest(self, info):
        url = info.requestUrl().toString()
        if self.adblock_rules.should_block(url):
            info.block(True)

class AdblockRuleWrapper:
    def __init__(self, rules):
        self.rules = AdblockRules(rules)
    def should_block(self, url):
        return self.rules.should_block(url)

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
        if debug:
            print("Added navigation bar")

        self.layout.addLayout(nav_bar)
        self.layout.addWidget(self.browser)

        # Update URL bar when page changes
        self.browser.urlChanged.connect(self.update_url_bar)

    def navigate_to_url(self):
        url = self.url_bar.text().strip()
        if not url:
            return
        # Prefer https:// for bare domains
        if not (url.startswith('http://') or url.startswith('https://')):
            url = 'https://' + url
        self.browser.setUrl(QUrl(url))
        if debug:
            print(f"Navigated to {url}")

    def update_url_bar(self, qurl):
        self.url_bar.setText(qurl.toString())

class TabbedBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{name} (Pine engine v.0.2)")
        self.setGeometry(100, 100, 1200, 800)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        # Toolbar with New Tab button and Settings menu
        toolbar = QWidget()
        self.toolbar_layout = QHBoxLayout()
        new_tab_btn = QPushButton("New Tab")
        new_tab_btn.clicked.connect(self.open_new_tab_dialog)
        self.toolbar_layout.addWidget(new_tab_btn)




        self.toolbar_layout.addStretch()
        toolbar.setLayout(self.toolbar_layout)

        # Layout for toolbar + tabs
        main_layout = QVBoxLayout()
        main_layout.addWidget(toolbar)
        main_layout.addWidget(self.tabs)
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.add_new_tab(homepage, 'Homepage')
        self.tabs.tabBarDoubleClicked.connect(self.on_tab_doubleclick)
        if debug:
            print("Double Tap Event started and ended")

    def add_new_tab(self, url, label):
        new_tab = BrowserTab(url)
        i = self.tabs.addTab(new_tab, label)
        self.tabs.setCurrentIndex(i)

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def on_tab_doubleclick(self, index):
        if index == -1:
            self.add_new_tab(homepage, "New Tab")

    def open_new_tab_dialog(self):
        url, ok1 = QInputDialog.getText(self, "New Tab", "Enter website URL:")
        if ok1 and url:
            tab_name, ok2 = QInputDialog.getText(self, "New Tab", "Enter tab name:")
            if ok2 and tab_name:
                self.add_new_tab(url, tab_name)
            if debug:
                print(f"Added new tab with contents {url}, {tab_name}")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("pine.png"))

    # --- Adblock setup (after QApplication!) ---
    with open('easylist.txt', encoding='utf8') as f:
        raw_rules = [line.strip() for line in f if line.strip() and not line.startswith('!')]
    adblock_rules = AdblockRuleWrapper(raw_rules)
    adblocker = AdBlocker(adblock_rules)
    profile = QWebEngineProfile.defaultProfile()
    profile.setRequestInterceptor(adblocker)
    if debug:
        print("Adblocker initialized")

    window = TabbedBrowser()

    # Set initial theme
    if mode == "Dark":
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    elif mode == "Light":
        try:
            with open("light.qss", "r") as f:
                app.setStyleSheet(f.read())
        except Exception as e:
            print("Could not load light.qss, using default style.")
    else:
        print("Invalid mode in config.ini")

    window.show()
    sys.exit(app.exec_())
