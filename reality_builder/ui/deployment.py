from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit, QFileDialog

class Deployment(QWidget):
    def __init__(self, server_config):
        super().__init__()
        self.server_config = server_config
        self.layout = QVBoxLayout(self)

        # Export Button
        self.export_button = QPushButton("Export install.sh")
        self.export_button.clicked.connect(self.export_script)
        self.layout.addWidget(self.export_button)

        # Script Preview
        self.script_preview = QTextEdit()
        self.script_preview.setReadOnly(True)
        self.layout.addWidget(self.script_preview)

    def export_script(self):
        script = self.generate_script()
        self.script_preview.setText(script)

        file_path, _ = QFileDialog.getSaveFileName(self, "Save install.sh", "", "Shell Scripts (*.sh)")
        if file_path:
            with open(file_path, "w") as f:
                f.write(script)

    def generate_script(self):
        private_key = self.server_config.key_pair_input.text()
        uuid = self.server_config.uuid_input.text()
        port = self.server_config.port_input.text()

        return f"""
#!/bin/bash

# Update and install necessary packages
apt update
apt install -y curl socat

# Install xray-core
bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install

# Create xray configuration file
cat > /usr/local/etc/xray/config.json <<EOF
{{
  "log": {{
    "loglevel": "warning"
  }},
  "inbounds": [
    {{
      "listen": "0.0.0.0",
      "port": {port},
      "protocol": "vless",
      "settings": {{
        "clients": [
          {{
            "id": "{uuid}",
            "level": 0
          }}
        ],
        "decryption": "none"
      }},
      "streamSettings": {{
        "network": "tcp",
        "security": "reality",
        "realitySettings": {{
          "show": false,
          "dest": "www.cloudflare.com:443",
          "xver": 0,
          "serverNames": [
            "www.cloudflare.com"
          ],
          "privateKey": "{private_key}",
          "minClientVer": "",
          "maxClientVer": "",
          "maxTimeDiff": 60000,
          "shortIds": [
            ""
          ]
        }}
      }}
    }}
  ],
  "outbounds": [
    {{
      "protocol": "freedom",
      "tag": "direct"
    }},
    {{
      "protocol": "blackhole",
      "tag": "blocked"
    }}
  ]
}}
EOF

# Restart xray service
systemctl restart xray
"""
