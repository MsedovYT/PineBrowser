# Version 0.2 (PyQt6 port)
import sys
import random
import datetime
import configparser
import qdarkstyle
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget,
    QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QInputDialog, QLabel
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEngineUrlRequestInterceptor
from PyQt6.QtCore import QUrl, pyqtSignal
real_world_facts = [
    "The Eiffel Tower can be 15 cm taller during hot days.",
    "Honey never spoils and can last thousands of years.",
    "Bananas are berries, but strawberries are not.",
    "A group of flamingos is called a 'flamboyance'.",
    "Octopuses have three hearts.",
    "The human nose can detect about 1 trillion smells.",
    "Venus is the only planet that spins clockwise.",
    "A bolt of lightning contains enough energy to toast 100,000 slices of bread.",
    "The shortest war in history lasted 38 minutes (Anglo-Zanzibar War).",
    "The unicorn is the national animal of Scotland.",
    "Wombat poop is cube-shaped.",
    "There are more possible iterations of a game of chess than atoms in the observable universe.",
    "A day on Venus is longer than its year.",
    "Hot water can freeze faster than cold water (the Mpemba effect).",
    "The heart of a blue whale is as big as a small car.",
    "The inventor of the Frisbee was turned into a Frisbee after he died.",
    "Some turtles can breathe through their butts.",
    "The dot over the letter 'i' is called a tittle.",
    "The longest place name in the world is 85 letters long (in New Zealand).",
    "Mosquitoes are attracted to people who just ate bananas.",
    "A group of crows is called a murder.",
    "Sloths can hold their breath longer than dolphins can.",
    "The first alarm clock could only ring at 4 a.m.",
    "The hashtag symbol is technically called an octothorpe.",
    "A jiffy is an actual unit of time: 1/100th of a second.",
    "The inventor of the microwave appliance received only $2 for his discovery.",
    "The world’s largest desert is not the Sahara, but Antarctica.",
    "A snail can sleep for three years.",
    "The fingerprints of a koala are so similar to humans that they can taint crime scenes.",
    "The tongue of a blue whale weighs as much as an elephant.",
    "The only letter that doesn’t appear in any U.S. state name is Q.",
    "The total weight of all ants on Earth is about the same as all humans.",
    "Some cats are allergic to humans.",
    "Cows have best friends and can become stressed if separated.",
    "The inventor of the Rubik’s Cube couldn’t solve it for over a month.",
    "The moon has moonquakes.",
    "The hottest chili pepper in the world is so hot it could kill you.",
    "A group of porcupines is called a prickle.",
    "The world’s oldest toy is a stick.",
    "The wood frog can hold its pee for up to eight months.",
    "The inventor of the Pringles can is buried in one.",
    "A group of owls is called a parliament.",
    "There are more fake flamingos in the world than real ones.",
    "The longest English word without a true vowel is 'rhythms'.",
    "Alaska is the state with the highest percentage of people who walk to work.",
    "The first computer mouse was made of wood.",
    "A sheep, a duck, and a rooster were the first passengers in a hot air balloon.",
    "The inventor of the telephone, Alexander Graham Bell, never phoned his wife or mother because they were both deaf.",
    "A jiffy is an actual unit of time: 1/100th of a second.",
    "The world’s largest grand piano was built by a 15-year-old in New Zealand.",
    "The inventor of the Super Soaker was a NASA engineer.",
    "The inventor of Vaseline ate a spoonful of it every morning.",
    "The first oranges weren’t orange.",
    "The first ever VCR, made in 1956, was the size of a piano.",
    "Chewing gum boosts concentration.",
    "The first product to have a barcode was Wrigley’s gum.",
    "The world’s largest snowflake on record was 15 inches across.",
    "A group of frogs is called an army.",
    "The inventor of the electric chair was a dentist.",
    "The world’s deepest postbox is in Susami Bay, Japan. It’s 10 meters underwater.",
    "The inventor of the match was paid only $15 for the patent.",
    "The world’s largest pyramid is not in Egypt, but in Mexico.",
    "The first person convicted of speeding was going 8 mph.",
    "The inventor of the ballpoint pen was denied a patent because it was thought to be an 'impossible' invention.",
    "The inventor of the sewing machine was inspired by a dream.",
    "The world’s largest rubber band ball weighs over 9,000 pounds.",
    "The inventor of the Popsicle was 11 years old.",
    "The world’s largest omelet weighed 6.8 tons.",
    "The inventor of the Slinky was a naval engineer.",
    "The world’s largest pizza was over 13,000 square feet.",
    "The inventor of the yo-yo was a Filipino immigrant.",
    "The world’s largest chocolate bar weighed over 12,000 pounds.",
    "The inventor of the hula hoop sold over 100 million hoops in two years.",
    "The world’s largest cupcake weighed over 2,000 pounds.",
    "The inventor of the skateboard was inspired by surfers.",
    "The world’s largest cookie weighed over 40,000 pounds.",
    "The inventor of the Frisbee was cremated and made into a Frisbee.",
    "The world’s largest rubber duck is over 60 feet tall.",
    "The inventor of the light bulb, Thomas Edison, was afraid of the dark.",
    "The world’s largest ice cream cone was over 9 feet tall.",
    "The inventor of the teddy bear was inspired by President Theodore Roosevelt.",
    "The world’s largest pumpkin weighed over 2,600 pounds.",
    "The inventor of the zipper was a Swedish-American engineer.",
    "The world’s largest sandwich weighed over 5,400 pounds.",
    "The inventor of the safety pin sold the patent for $400.",
    "The world’s largest hot dog was over 200 feet long.",
    "The inventor of the escalator called it the 'inclined elevator'.",
    "The world’s largest lollipop weighed over 7,000 pounds.",
    "The inventor of the credit card was inspired by a forgotten wallet.",
    "The world’s largest pancake was over 49 feet in diameter.",
    "The inventor of the shopping cart was a grocery store owner.",
    "The world’s largest carrot weighed over 20 pounds.",
    "The inventor of the paperclip was a Norwegian engineer.",
    "The world’s largest ice cream cake weighed over 12,000 pounds.",
    "The inventor of the stapler was inspired by King Louis XV of France.",
    "The world’s largest apple weighed over 4 pounds.",
    "The inventor of the paper bag machine was Margaret E. Knight.",
    "The world’s largest watermelon weighed over 350 pounds.",
    "The inventor of the typewriter was inspired by a blind friend.",
    "The world’s largest tomato weighed over 7 pounds.",
    "The inventor of the vacuum cleaner was a janitor.",
    "The world’s largest potato weighed over 18 pounds.",
    "The inventor of the dishwasher was a woman named Josephine Cochrane.",
]

from adblockparser import AdblockRules
config = configparser.ConfigParser()
config.read('config.ini')
homepage = config['Browser']['Homepage']
name = config['App']['Name']
mode = config['App']['Mode']
debug = config['Developer']['Debug'] == "True"
username = config['User']['Username']
now = datetime.datetime.now()
current_time = now.strftime("%H:%M")
time = "Loading..."
if current_time > "12:00":
    time = "afternoon"
else:
    time = "morning"

# --------- Custom New Tab Page ----------
class CustomNewTabPage(QWidget):
    searchRequested = pyqtSignal(str)  # Signal to request a search

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        welcome_label = QLabel(f"Good {time}, {username}! ")
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(welcome_label)
        welcome_label = QLabel(f"Fun fact: {random.choice(real_world_facts)}")
        welcome_label.setStyleSheet("font-size: 11px; font-weight: bold;")
        layout.addWidget(welcome_label)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search the web...")
        layout.addWidget(self.search_bar)

        search_button = QPushButton("Search")
        search_button.clicked.connect(self.perform_search)
        layout.addWidget(search_button)

        self.setLayout(layout)

    def perform_search(self):
        query = self.search_bar.text()
        if query:
            url = f"https://www.perplexity.ai/search?q={query.replace(' ', '+')}"
            self.searchRequested.emit(url)  # Emit signal with search URL

# --------- Config and Adblock ----------


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

# --------- Browser Tab ----------
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

# --------- Main Browser Window ----------
class TabbedBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{name} (Pine engine v.0.2)")
        self.setGeometry(100, 100, 1200, 800)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        # Toolbar with New Tab button
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

        self.add_browser_tab(homepage, 'Homepage')
        self.tabs.tabBarDoubleClicked.connect(self.on_tab_doubleclick)
        if debug:
            print("Double Tap Event started and ended")

    def add_browser_tab(self, url, label):
        new_tab = BrowserTab(url)
        i = self.tabs.addTab(new_tab, label)
        self.tabs.setCurrentIndex(i)

    def add_custom_new_tab(self, label="New Tab"):
        new_tab = CustomNewTabPage()
        new_tab.searchRequested.connect(self.handle_new_tab_search)
        i = self.tabs.addTab(new_tab, label)
        self.tabs.setCurrentIndex(i)

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def on_tab_doubleclick(self, index):
        if index == -1:
            self.add_custom_new_tab("New Tab")

    def open_new_tab_dialog(self):
        self.add_custom_new_tab("New Tab")

    def handle_new_tab_search(self, url):
        self.add_browser_tab(url, "Search")
        # Optionally, close the custom new tab after search:
        self.tabs.removeTab(self.tabs.currentIndex() - 1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("pine.png"))

    # --- Adblock setup (after QApplication!) ---
    with open('easylist.txt', encoding='utf8') as f:
        raw_rules = [line.strip() for line in f if line.strip() and not line.startswith('!')]
    adblock_rules = AdblockRuleWrapper(raw_rules)
    adblocker = AdBlocker(adblock_rules)
    profile = QWebEngineProfile.defaultProfile()
    # PyQt6: Use setUrlRequestInterceptor (not setRequestInterceptor)
    profile.setUrlRequestInterceptor(adblocker)
    if debug:
        print("Adblocker initialized")

    window = TabbedBrowser()

    # Set initial theme
    if mode == "Dark":
        # qdarkstyle may not support PyQt6 out of the box; test or replace as needed
        try:
            app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt6'))
        except Exception as e:
            print("Could not load qdarkstyle for PyQt6:", e)
    elif mode == "Light":
        try:
            with open("light.qss", "r") as f:
                app.setStyleSheet(f.read())
        except Exception as e:
            print("Could not load light.qss, using default style.")
    elif mode == "Custom":
        try:
            with open("custom.qss", "r") as f:
                app.setStyleSheet(f.read())
        except Exception as e:
            print("Could not load custom.qss, using default style.")
    else:
        print("Invalid mode in config.ini")

    window.show()
    sys.exit(app.exec())
