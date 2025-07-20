from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
import requests

class Updater(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        # Xray-core
        self.xray_core_layout = QVBoxLayout()
        self.xray_core_label = QLabel("xray-core")
        self.xray_core_version_label = QLabel("Current version: ?")
        self.xray_core_check_button = QPushButton("Check for updates")
        self.xray_core_check_button.clicked.connect(self.check_xray_core_update)
        self.xray_core_layout.addWidget(self.xray_core_label)
        self.xray_core_layout.addWidget(self.xray_core_version_label)
        self.xray_core_layout.addWidget(self.xray_core_check_button)
        self.layout.addLayout(self.xray_core_layout)

        # Xray-knife
        self.xray_knife_layout = QVBoxLayout()
        self.xray_knife_label = QLabel("xray-knife")
        self.xray_knife_version_label = QLabel("Current version: ?")
        self.xray_knife_check_button = QPushButton("Check for updates")
        self.xray_knife_check_button.clicked.connect(self.check_xray_knife_update)
        self.xray_knife_layout.addWidget(self.xray_knife_label)
        self.xray_knife_layout.addWidget(self.xray_knife_version_label)
        self.xray_knife_layout.addWidget(self.xray_knife_check_button)
        self.layout.addLayout(self.xray_knife_layout)

    def get_latest_release(self, repo):
        url = f"https://api.github.com/repos/{repo}/releases/latest"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()["tag_name"]
        except requests.exceptions.RequestException as e:
            return f"Error: {e}"

    def check_xray_core_update(self):
        latest_version = self.get_latest_release("XTLS/Xray-core")
        self.xray_core_version_label.setText(f"Latest version: {latest_version}")

    def check_xray_knife_update(self):
        latest_version = self.get_latest_release("XTLS/Xray-knife")
        self.xray_knife_version_label.setText(f"Latest version: {latest_version}")
