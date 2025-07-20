from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox
from reality_builder.core.xray import generate_uuid, generate_key_pair

class ServerConfig(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        # VPS IP
        self.ip_label = QLabel("VPS IP:")
        self.ip_input = QLineEdit()
        self.layout.addWidget(self.ip_label)
        self.layout.addWidget(self.ip_input)

        # Port
        self.port_label = QLabel("Port:")
        self.port_input = QLineEdit("443")
        self.layout.addWidget(self.port_label)
        self.layout.addWidget(self.port_input)

        # UUID
        self.uuid_label = QLabel("UUID:")
        self.uuid_input = QLineEdit()
        self.uuid_button = QPushButton("Generate UUID")
        self.uuid_button.clicked.connect(self.generate_uuid)
        self.layout.addWidget(self.uuid_label)
        self.layout.addWidget(self.uuid_input)
        self.layout.addWidget(self.uuid_button)

        # x25519 Key Pair
        self.key_pair_label = QLabel("x25519 Key Pair (Private Key):")
        self.key_pair_input = QLineEdit()
        self.public_key_label = QLabel("x25519 Key Pair (Public Key):")
        self.public_key_input = QLineEdit()
        self.key_pair_button = QPushButton("Generate Key Pair")
        self.key_pair_button.clicked.connect(self.generate_key_pair)
        self.layout.addWidget(self.key_pair_label)
        self.layout.addWidget(self.key_pair_input)
        self.layout.addWidget(self.public_key_label)
        self.layout.addWidget(self.public_key_input)
        self.layout.addWidget(self.key_pair_button)

        # SNI
        self.sni_label = QLabel("SNI:")
        self.sni_combo = QComboBox()
        self.sni_combo.addItems(["www.cloudflare.com", "assets.fastly.net", "www.wikipedia.org"])
        self.sni_combo.setEditable(True)
        self.layout.addWidget(self.sni_label)
        self.layout.addWidget(self.sni_combo)

        # Save Button
        self.save_button = QPushButton("Save config.json")
        self.layout.addWidget(self.save_button)

    def generate_uuid(self):
        self.uuid_input.setText(generate_uuid())

    def generate_key_pair(self):
        private_key, public_key = generate_key_pair()
        self.key_pair_input.setText(private_key)
        self.public_key_input.setText(public_key)
