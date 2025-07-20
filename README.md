# Reality Builder

Reality Builder is a native Windows desktop application that automates creating, testing, and deploying VLESS+Reality VPN configurations optimized for Iran’s DPI and SNI filtering.

## Features

*   **Server Configuration:** Easily generate `config.json` files for your VPS.
*   **IP Scanner:** Scan Cloudflare IPs to find the best one for your connection.
*   **Client Configuration:** Generate `vless://` URIs and QR codes for your client applications.
*   **Connection Tester:** Test your connection to the server using various methods.
*   **Deployment Automation:** Export an `install.sh` script to set up your VPS.
*   **Auto-Updater:** Check for new releases of `xray-core` and `xray-knife`.

## Screenshots

*   **Server Configuration:** [Screenshot of the Server Configuration tab]
*   **IP Scanner:** [Screenshot of the IP Scanner tab]
*   **Client Configuration:** [Screenshot of the Client Configuration tab]
*   **Connection Tester:** [Screenshot of the Connection Tester tab]
*   **Deployment:** [Screenshot of the Deployment tab]
*   **Updater:** [Screenshot of the Updater tab]

## Installation

1.  Download the latest `RealityBuilder-Setup.exe` from the [releases page](https://github.com/your-repo/reality-builder/releases).
2.  Run the installer and follow the instructions.

### Silent Install

To install the application silently, run the installer with the `/S` flag:

```
RealityBuilder-Setup.exe /S
```

## Usage

1.  **Server Configuration:** Fill in the server details in the "Server Config" tab.
2.  **IP Scanner (Optional):** Use the "IP Scanner" to find a good Cloudflare IP.
3.  **Client Configuration:** Generate the client URI and QR code in the "Client Config" tab.
4.  **Test Connection:** Test your connection in the "Test" tab.
5.  **Deploy:** Export the `install.sh` script from the "Deployment" tab and run it on your VPS.

## Troubleshooting

### Windows Defender/SmartScreen Prompts

Windows Defender or SmartScreen may show a warning when you run the installer or the application for the first time. This is because the application is not yet signed with a trusted certificate. To proceed, click on "More info" and then "Run anyway".

### Profiles File

The application stores all the profiles in a JSON file located at `%APPDATA%\RealityBuilder\profiles.json`.

## Building from Source

1.  Clone the repository:
    ```
    git clone https://github.com/your-repo/reality-builder.git
    ```
2.  Install the dependencies:
    ```
    pip install -r requirements.txt
    ```
3.  Run the application:
    ```
    python reality_builder/main.py
    ```
4.  To build the executable:
    ```
    python build.py
    ```
5.  To build the installer, you need to have [NSIS](https://nsis.sourceforge.io/Download) installed. Then, run the `makensis` command:
    ```
    makensis installer.nsi
    ```

## Code Signing

The executable is not currently signed. To avoid security warnings, it is recommended to sign the executable with an Authenticode/EV certificate.
