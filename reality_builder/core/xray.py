import subprocess
import requests

def generate_uuid():
    """Generates a UUID using xray-core."""
    try:
        result = subprocess.run(["xray", "uuid"], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except FileNotFoundError:
        return "xray not found. Please make sure it's in your PATH."
    except subprocess.CalledProcessError as e:
        return f"Error generating UUID: {e.stderr}"

def generate_key_pair():
    """Generates an x25519 key pair using xray-core."""
    try:
        result = subprocess.run(["xray", "x25519"], capture_output=True, text=True, check=True)
        # The output contains private key and public key on separate lines
        lines = result.stdout.strip().split("\n")
        private_key = lines[0].split(": ")[1]
        public_key = lines[1].split(": ")[1]
        return private_key, public_key
    except FileNotFoundError:
        return "xray not found. Please make sure it's in your PATH.", ""
    except subprocess.CalledProcessError as e:
        return f"Error generating key pair: {e.stderr}", ""
    except IndexError:
        return "Error parsing xray output.", ""

def get_cloudflare_ips():
    """Fetches the list of Cloudflare IPv4 addresses."""
    try:
        response = requests.get("https://www.cloudflare.com/ips-v4")
        response.raise_for_status()
        return response.text.strip().split("\n")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Cloudflare IPs: {e}")
        return []

def scan_ip(ip, port, sni):
    """Scans a single IP using xray-knife."""
    try:
        command = [
            "xray-knife", "scan", "reality",
            "--address", f"{ip}:{port}",
            "--server-name", sni,
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        # This is a placeholder. The actual output of xray-knife needs to be parsed.
        return "OK", "0%", "Yes"
    except FileNotFoundError:
        return "xray-knife not found", "", ""
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip()}", "", ""

def test_curl(ip, port, sni):
    """Tests the connection using curl."""
    try:
        command = ["curl", "--resolve", f"{sni}:{port}:{ip}", f"https://{sni}", "-I"]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return "✅" if "HTTP/2 200" in result.stdout else "❌"
    except (FileNotFoundError, subprocess.CalledProcessError):
        return "❌"

def test_probe(ip, port, sni):
    """Tests the connection using xray-knife probe."""
    try:
        command = ["xray-knife", "probe", "--address", f"{ip}:{port}", "--server-name", sni]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return "✅" if "Handshake success" in result.stdout else "❌"
    except (FileNotFoundError, subprocess.CalledProcessError):
        return "❌"

def test_ping(ip):
    """Tests the connection using ping."""
    try:
        command = ["ping", "-c", "4", ip]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return "✅" if "0% packet loss" in result.stdout else "❌"
    except (FileNotFoundError, subprocess.CalledProcessError):
        return "❌"
