

from input import paste_text, backspace


import os
from dotenv import load_dotenv
import uvicorn

load_dotenv()

PAIR_TOKEN=os.getenv("PAIR_TOKEN", "")

from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse

app = FastAPI()

BASE_DIR = Path(__file__).parent

@app.get("/")
async def index():
    print("index.html")
    return FileResponse(BASE_DIR / "index.html")

@app.get("/cert.pem")
async def cert():
    print("cert.pem")
    return FileResponse(
        BASE_DIR / "ssl" / "cert.pem",
        media_type="application/x-pem-file",
        filename="cert.pem",
    )


import hashlib
import hmac
import secrets



import asyncio



PING_INTERVAL = 30

async def ping_task(websocket: WebSocket):
    try:
        while True:
            await asyncio.sleep(PING_INTERVAL)

            await websocket.send_json({
                "type": "ping"
            })
    except Exception:
        pass




@app.websocket("/ws")
async def ws(websocket: WebSocket):
    await websocket.accept()

    # Generate a random challenge (nonce)
    nonce = secrets.token_hex(32)

    # Send challenge to the client
    await websocket.send_json({
        "type": "challenge",
        "nonce": nonce,
    })

    # Receive client's response
    auth = await websocket.receive_json()

    if auth.get("type") != "auth":
        await websocket.close(code=1008)
        return

    # Calculate expected HMAC
    expected = hmac.new(
        PAIR_TOKEN.encode(),
        nonce.encode(),
        hashlib.sha256,
    ).hexdigest()

    # Verify response
    if not hmac.compare_digest(
        auth.get("response", ""),
        expected,
    ):
        await websocket.send_json({
            "type": "auth_failed",
        })
        await websocket.close(code=1008)
        return

    # Authentication successful
    await websocket.send_json({
        "type": "auth_ok",
    })

    # Process authenticated messages

    # Start heartbeat only after successful authentication
    ping = asyncio.create_task(ping_task(websocket))

    try:

        while True:
            message = await websocket.receive_json()


            msg_id = message.get("id")
            msg_type = message.get("type")

            if msg_type == "text":
                text = message.get("text", "")

                print(text)


                paste_text(text)


                await websocket.send_json({
                    "id": msg_id,
                    "type": "text",
                    "status": "ok",
                    "text": text,
                })



            elif msg_type == "backspace":


                print("backspace")


                backspace()


                await websocket.send_json({
                    "id": msg_id,
                    "type": "backspace",
                    "status": "ok"
                })        


            elif msg_type == "ping":
                await websocket.send_json({
                    "id": msg_id,
                    "type": "pong",
                })

    except WebSocketDisconnect:
        pass

    finally:
        ping.cancel()










if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "56391")),
        ssl_certfile="ssl/cert.pem",
        ssl_keyfile="ssl/key.pem",
        reload=True,      # Development only
    )