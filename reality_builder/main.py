import sys
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit
from reality_builder.ui.server_config import ServerConfig
from reality_builder.ui.ip_scanner import IPScanner
from reality_builder.ui.client_config import ClientConfig
from reality_builder.ui.connection_tester import ConnectionTester
from reality_builder.ui.deployment import Deployment
from reality_builder.ui.updater import Updater

class RealityBuilder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reality Builder")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.stack = QStackedWidget()
        self.server_config = ServerConfig()
        self.ip_scanner = IPScanner(self.server_config)
        self.client_config = ClientConfig(self.server_config)
        self.connection_tester = ConnectionTester(self.server_config)
        self.deployment = Deployment(self.server_config)
        self.updater = Updater()
        self.stack.addWidget(self.server_config)
        self.stack.addWidget(self.ip_scanner)
        self.stack.addWidget(self.client_config)
        self.stack.addWidget(self.connection_tester)
        self.stack.addWidget(self.deployment)
        self.stack.addWidget(self.updater)
        self.layout.addWidget(self.stack)

        self.nav_layout = QHBoxLayout()
        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.prev_page)
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_page)
        self.theme_button = QPushButton("Toggle Theme")
        self.theme_button.clicked.connect(self.toggle_theme)
        self.nav_layout.addWidget(self.prev_button)
        self.nav_layout.addWidget(self.next_button)
        self.nav_layout.addWidget(self.theme_button)
        self.layout.addLayout(self.nav_layout)

        self.log_panel = QTextEdit()
        self.log_panel.setReadOnly(True)
        self.layout.addWidget(self.log_panel)

        self.dark_theme = False
        self.load_theme()

        # Redirect stdout and stderr
        sys.stdout = self.Stream(self.log_panel)
        sys.stderr = self.Stream(self.log_panel)

    class Stream:
        def __init__(self, text_widget):
            self.text_widget = text_widget

        def write(self, text):
            self.text_widget.append(text)

        def flush(self):
            pass

    def load_theme(self):
        theme = "dark" if self.dark_theme else "light"
        with open(f"reality_builder/assets/themes/{theme}.qss", "r") as f:
            self.setStyleSheet(f.read())

    def toggle_theme(self):
        self.dark_theme = not self.dark_theme
        self.load_theme()

    def prev_page(self):
        current_index = self.stack.currentIndex()
        if current_index > 0:
            self.stack.setCurrentIndex(current_index - 1)

    def next_page(self):
        current_index = self.stack.currentIndex()
        if current_index < self.stack.count() - 1:
            self.stack.setCurrentIndex(current_index + 1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RealityBuilder()
    window.show()
    sys.exit(app.exec_())
