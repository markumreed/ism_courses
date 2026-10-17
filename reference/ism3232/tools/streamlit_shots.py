"""Screenshot a running Streamlit app's two tabs with headless Chrome.

A one-shot `google-chrome --headless --screenshot` captures Streamlit's loading
skeleton, because the page draws over a websocket. This drives Chrome over the
DevTools protocol instead: load, wait in real time, capture, click the second
tab, capture again.

usage: python streamlit_shots.py URL OUT_PREFIX
writes OUT_PREFIX_chat.png and OUT_PREFIX_staff.png (needs the websockets package)
"""

import asyncio
import base64
import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import websockets

url, prefix = sys.argv[1], sys.argv[2]
chrome = subprocess.Popen(
    [
        "google-chrome",
        "--headless=new",
        "--disable-gpu",
        "--remote-debugging-port=9333",
        "--window-size=1280,1400",
        "--user-data-dir=/tmp/claude-1000/cdp-profile",
        "about:blank",
    ],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
try:
    for _ in range(50):
        try:
            targets = json.load(urllib.request.urlopen("http://127.0.0.1:9333/json"))
            page = next(t for t in targets if t["type"] == "page")
            break
        except (OSError, StopIteration, ValueError):
            time.sleep(0.3)

    async def main():
        ws = await websockets.connect(page["webSocketDebuggerUrl"], max_size=50_000_000)
        counter = {"id": 0}

        async def call(method, **params):
            counter["id"] += 1
            await ws.send(
                json.dumps({"id": counter["id"], "method": method, "params": params})
            )
            while True:
                msg = json.loads(await ws.recv())
                if msg.get("id") == counter["id"]:
                    return msg.get("result", {})

        async def shot(name):
            data = await call(
                "Page.captureScreenshot", format="png", captureBeyondViewport=True
            )
            images[name] = base64.b64decode(data["data"])

        await call("Page.enable")
        await call("Page.navigate", url=url)
        await asyncio.sleep(8)
        await shot("chat")
        await call(
            "Runtime.evaluate",
            expression="document.querySelectorAll('[role=tab]')[1].click()",
        )
        await asyncio.sleep(3)
        await shot("staff")
        await ws.close()

    images = {}
    asyncio.run(main())
    for name, image in images.items():
        Path(f"{prefix}_{name}.png").write_bytes(image)
finally:
    chrome.terminate()
