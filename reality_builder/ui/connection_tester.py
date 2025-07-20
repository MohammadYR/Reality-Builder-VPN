from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal
from reality_builder.core.xray import test_curl, test_probe, test_ping

class TestWorker(QThread):
    curl_done = pyqtSignal(str)
    probe_done = pyqtSignal(str)
    ping_done = pyqtSignal(str)

    def __init__(self, ip, port, sni):
        super().__init__()
        self.ip = ip
        self.port = port
        self.sni = sni

    def run(self):
        self.curl_done.emit(test_curl(self.ip, self.port, self.sni))
        self.probe_done.emit(test_probe(self.ip, self.port, self.sni))
        self.ping_done.emit(test_ping(self.ip))

class ConnectionTester(QWidget):
    def __init__(self, server_config):
        super().__init__()
        self.server_config = server_config
        self.layout = QVBoxLayout(self)

        # Test Button
        self.test_button = QPushButton("Test Connection")
        self.test_button.clicked.connect(self.start_tests)
        self.layout.addWidget(self.test_button)

        # Results
        self.results_layout = QVBoxLayout()
        self.layout.addLayout(self.results_layout)

        # Curl Test
        self.curl_layout = QHBoxLayout()
        self.curl_label = QLabel("Curl Test:")
        self.curl_status = QLabel("?")
        self.curl_layout.addWidget(self.curl_label)
        self.curl_layout.addWidget(self.curl_status)
        self.results_layout.addLayout(self.curl_layout)

        # xray-knife Probe Test
        self.probe_layout = QHBoxLayout()
        self.probe_label = QLabel("xray-knife Probe:")
        self.probe_status = QLabel("?")
        self.probe_layout.addWidget(self.probe_label)
        self.probe_layout.addWidget(self.probe_status)
        self.results_layout.addLayout(self.probe_layout)

        # Ping Test
        self.ping_layout = QHBoxLayout()
        self.ping_label = QLabel("Ping Test:")
        self.ping_status = QLabel("?")
        self.ping_layout.addWidget(self.ping_label)
        self.ping_layout.addWidget(self.ping_status)
        self.results_layout.addLayout(self.ping_layout)

    def start_tests(self):
        ip = self.server_config.ip_input.text()
        port = self.server_config.port_input.text()
        sni = self.server_config.sni_combo.currentText()

        self.curl_status.setText("?")
        self.probe_status.setText("?")
        self.ping_status.setText("?")

        self.test_worker = TestWorker(ip, port, sni)
        self.test_worker.curl_done.connect(self.update_curl_status)
        self.test_worker.probe_done.connect(self.update_probe_status)
        self.test_worker.ping_done.connect(self.update_ping_status)
        self.test_worker.start()

    def update_curl_status(self, status):
        self.curl_status.setText(status)

    def update_probe_status(self, status):
        self.probe_status.setText(status)

    def update_ping_status(self, status):
        self.ping_status.setText(status)
