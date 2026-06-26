


import os
from dotenv import load_dotenv
import uvicorn

load_dotenv()

from pathlib import Path

from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse

app = FastAPI()

BASE_DIR = Path(__file__).parent

@app.get("/")
async def index():
    return FileResponse(BASE_DIR / "index.html")

@app.get("/cert.pem")
async def cert():
    return FileResponse(
        BASE_DIR / "ssl" / "cert.pem",
        media_type="application/x-pem-file",
        filename="cert.pem",
    )


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()

    try:
        while True:
            text = await ws.receive_text()

            print(text)

            # TODO:
            # paste into focused application

            await ws.send_text("OK")

    except Exception:
        print("Disconnected")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "56391")),
        ssl_certfile="ssl/cert.pem",
        ssl_keyfile="ssl/key.pem",
        reload=True,      # Development only
    )