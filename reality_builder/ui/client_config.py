from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
import qrcode
from io import BytesIO

class ClientConfig(QWidget):
    def __init__(self, server_config):
        super().__init__()
        self.server_config = server_config
        self.layout = QVBoxLayout(self)

        # VLESS URI
        self.uri_label = QLabel("VLESS URI:")
        self.uri_output = QTextEdit()
        self.uri_output.setReadOnly(True)
        self.layout.addWidget(self.uri_label)
        self.layout.addWidget(self.uri_output)

        # Copy URI Button
        self.copy_uri_button = QPushButton("Copy to Clipboard")
        self.layout.addWidget(self.copy_uri_button)

        # QR Code
        self.qr_label = QLabel()
        self.layout.addWidget(self.qr_label)

        # Save QR Code Button
        self.save_qr_button = QPushButton("Save QR Code")
        self.save_qr_button.clicked.connect(self.save_qr_code)
        self.layout.addWidget(self.save_qr_button)

        # Generate Button
        self.generate_button = QPushButton("Generate")
        self.generate_button.clicked.connect(self.generate)
        self.layout.addWidget(self.generate_button)

        self.copy_uri_button.clicked.connect(self.copy_uri)

    def generate(self):
        # This is where the VLESS URI will be generated
        # For now, it's just a placeholder
        uri = self.generate_vless_uri()
        self.uri_output.setText(uri)
        self.generate_qr_code(uri)

    def generate_vless_uri(self):
        uuid = self.server_config.uuid_input.text()
        server = self.server_config.ip_input.text()
        port = self.server_config.port_input.text()
        sni = self.server_config.sni_combo.currentText()
        public_key = self.server_config.public_key_input.text()
        # This is a simplified example. A proper implementation would need to handle all the reality-opts.
        uri = f"vless://{uuid}@{server}:{port}?security=reality&sni={sni}&publicKey={public_key}&type=tcp#reality"
        return uri

    def generate_qr_code(self, uri):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(uri)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Convert the image to a format that can be displayed in PyQt
        buffer = BytesIO()
        img.save(buffer, "PNG")
        pixmap = QPixmap()
        pixmap.loadFromData(buffer.getvalue(), "PNG")
        self.qr_label.setPixmap(pixmap)
        self.qr_image = img

    def copy_uri(self):
        QApplication.clipboard().setText(self.uri_output.toPlainText())

    def save_qr_code(self):
        if hasattr(self, 'qr_image'):
            file_path, _ = QFileDialog.getSaveFileName(self, "Save QR Code", "", "PNG Images (*.png)")
            if file_path:
                self.qr_image.save(file_path)
