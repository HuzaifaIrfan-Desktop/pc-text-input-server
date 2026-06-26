
import time


import os
from dotenv import load_dotenv

load_dotenv()

HOST=os.getenv("HOST", "")
PORT=os.getenv("PORT", "")

CREATED_ON=os.getenv("CREATED_ON", "")
PAIR_TOKEN=os.getenv("PAIR_TOKEN", "")

SECRET_KEY=os.getenv("CREATED_ON", "")
CERT_FINGERPRINT=os.getenv("CREATED_ON", "")

print("Starting REST API Post Input Test...")

import requests

from pathlib import Path

cert_path = Path(__file__).parent / "ssl" / "cert.pem"



base_url = f"https://{HOST}:{PORT}"


headers = {
    "Authorization": f"Bearer {PAIR_TOKEN}",
    "Content-Type": "application/json",
}




time.sleep(2)  # Pauses the script for exactly 2 seconds

url=f"{base_url}/paste_text"


data = {
    "text": "你好世界"
}

response = requests.post(url, json=data, headers=headers, verify=str(cert_path))

print(response.status_code)
print(response.text)



time.sleep(2)  # Pauses the script for exactly 2 seconds


url=f"{base_url}/backspace"

data = {
    "count": 1
}

response = requests.post(url, json=data, headers=headers, verify=str(cert_path))

print(response.status_code)
print(response.text)

