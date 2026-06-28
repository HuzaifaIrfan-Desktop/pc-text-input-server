#!/usr/bin/env -S uv run --script

import time
from dotenv import load_dotenv
import os
import uvicorn

load_dotenv()

while True:
    try:
        uvicorn.run(
            "main:app",
            host=os.getenv("HOST", "0.0.0.0"),
            port=int(os.getenv("PORT", "56391")),
            ssl_certfile="ssl/cert.pem",
            ssl_keyfile="ssl/key.pem",
        )
    except Exception as e:
        print(e)

    print("Restarting in 2 seconds...")
    time.sleep(2)