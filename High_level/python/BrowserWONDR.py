import sys
from PyQt5.QtCore import QUrl, QEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QLineEdit, QTabWidget, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile

class BrowserTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.webview = QWebEngineView()
        self.layout.addWidget(self.webview)
        self.webview.load(QUrl("https://www.google.com"))
        
        #user agent
        self.profile = QWebEngineProfile.defaultProfile()
        self.profile.setHttpUserAgent("Mozilla/5.0 (Custom Browser; rv:90.0) Gecko/20100101 Firefox/90.0")

class CustomBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WONDRnet")
        self.setGeometry(100, 100, 1024, 768)
        
        # Create tab widget
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)
        
        # Create toolbar
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)
        
        # Navigation buttons
        self.back_btn = QPushButton("← Back")
        self.back_btn.clicked.connect(self.navigate_back)
        self.toolbar.addWidget(self.back_btn)
        
        self.forward_btn = QPushButton("Forward →")
        self.forward_btn.clicked.connect(self.navigate_forward)
        self.toolbar.addWidget(self.forward_btn)
        
        self.reload_btn = QPushButton("↻ Reload")
        self.reload_btn.clicked.connect(self.reload_page)
        self.toolbar.addWidget(self.reload_btn)
        
        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.toolbar.addWidget(self.url_bar)
        
        # New tab button
        self.new_tab_btn = QPushButton("+ Add Tab")
        self.new_tab_btn.clicked.connect(self.add_new_tab)
        self.tabs.setCornerWidget(self.new_tab_btn)
        
        # Add initial tab
        self.add_new_tab()
        
        # Block malicious sites (basic example)
        self.blocked_sites = [
            "example-malicious-site.com",
            "dangerous-website.org",
            "pornhub.com"
        ]
        
    def add_new_tab(self):
        tab = BrowserTab()
        index = self.tabs.addTab(tab, "New Tab")
        self.tabs.setCurrentIndex(index)
        
        tab.webview.urlChanged.connect(lambda q, browser_tab=tab: self.update_urlbar(q, browser_tab))
        tab.webview.titleChanged.connect(lambda title, browser_tab=tab: self.update_title(title, browser_tab))
        
    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
            
    def navigate_to_url(self):
        url = self.url_bar.text()
        current_tab = self.tabs.currentWidget().webview
        
        # Add https or http but try to insist https
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        # Check blocked sites
        if any(blocked in url for blocked in self.blocked_sites):
            current_tab.setHtml("<h1>BLOCKED</h1><p>This site is restricted by your browser security settings.</p>")
            return
            
        current_tab.load(QUrl(url))
        
    def navigate_back(self):
        current_tab = self.tabs.currentWidget().webview
        current_tab.back()
        
    def navigate_forward(self):
        current_tab = self.tabs.currentWidget().webview
        current_tab.forward()
        
    def reload_page(self):
        current_tab = self.tabs.currentWidget().webview
        current_tab.reload()
        
def fav_pages(self):
    current_tab = self.tabs.currentWidget().webview
    current_url = current_tab.url().toString()
    current_title = current_tab.title()
    
    # Add to favorites dictionary
    self.favorites[current_title] = current_url
        
    def update_urlbar(self, q, browser_tab):
        current_tab = self.tabs.currentWidget()
        if browser_tab == current_tab:
            self.url_bar.setText(q.toString())
            
    def update_title(self, title, browser_tab):
        index = self.tabs.indexOf(browser_tab)
        self.tabs.setTabText(index, title[:15] + '...' if len(title) > 15 else title)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = CustomBrowser()
    browser.show()
    sys.exit(app.exec_())
