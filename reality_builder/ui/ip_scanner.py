from PyQt5.QtWidgets import QWidget, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal
from reality_builder.core.xray import get_cloudflare_ips, scan_ip

class ScanWorker(QThread):
    result_ready = pyqtSignal(int, str, str, str)
    finished = pyqtSignal()

    def __init__(self, ips, port, sni):
        super().__init__()
        self.ips = ips
        self.port = port
        self.sni = sni

    def run(self):
        for i, ip in enumerate(self.ips):
            latency, packet_loss, status = scan_ip(ip, self.port, self.sni)
            self.result_ready.emit(i, latency, packet_loss, status)
        self.finished.emit()

class IPScanner(QWidget):
    def __init__(self, server_config):
        super().__init__()
        self.server_config = server_config
        self.layout = QVBoxLayout(self)

        # Scan Button
        self.scan_button = QPushButton("Scan Cloudflare IPs")
        self.scan_button.clicked.connect(self.start_scan)
        self.layout.addWidget(self.scan_button)

        # Results Table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(4)
        self.results_table.setHorizontalHeaderLabels(["IP", "Latency", "Packet Loss", "Whitelist Status"])
        self.layout.addWidget(self.results_table)

        # Use IP Button
        self.use_ip_button = QPushButton("Use Selected IP")
        self.use_ip_button.clicked.connect(self.use_selected_ip)
        self.layout.addWidget(self.use_ip_button)

    def start_scan(self):
        ips = get_cloudflare_ips()
        if not ips:
            # Handle error
            return

        self.results_table.setRowCount(len(ips))
        for i, ip in enumerate(ips):
            self.results_table.setItem(i, 0, QTableWidgetItem(ip))

        port = self.server_config.port_input.text()
        sni = self.server_config.sni_combo.currentText()

        self.scan_worker = ScanWorker(ips, port, sni)
        self.scan_worker.result_ready.connect(self.update_table)
        self.scan_worker.start()

    def update_table(self, row, latency, packet_loss, status):
        self.results_table.setItem(row, 1, QTableWidgetItem(latency))
        self.results_table.setItem(row, 2, QTableWidgetItem(packet_loss))
        self.results_table.setItem(row, 3, QTableWidgetItem(status))

    def use_selected_ip(self):
        selected_row = self.results_table.currentRow()
        if selected_row != -1:
            ip = self.results_table.item(selected_row, 0).text()
            self.server_config.ip_input.setText(ip)
