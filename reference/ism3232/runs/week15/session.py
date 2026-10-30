"""Drive the Bayside app in headless Chrome and save what a customer and a
staff member see: the chat, the waiting request, the approval, the orders
after it, the customer asking about it, and a refresh. The three screenshots
and the text come from this one session, and session.txt records each
screenshot's SHA-256 so a re-taken picture without its text fails a test.

usage: python session.py APP_COPY SESSION_TXT IMAGES_DIR
Nothing is written unless every step succeeds. Needs streamlit and websockets.
"""

import asyncio
import base64
import hashlib
import json
import socket
import sqlite3
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

import websockets

APP, SESSION, IMAGES = (Path(arg) for arg in sys.argv[1:4])
MESSAGES = [
    "Has A101 shipped yet?",
    "Please change the address on order A102 to 9 Pine Street, Tampa",
    "What happened to request 1?",
]
REPLY_TIMEOUT = 300
WIDTH, HEIGHT, SCALE = 1200, 1000, 2


class StepFailed(Exception):
    pass


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def wait_for_url(url, step, timeout=60):
    end = time.time() + timeout
    while time.time() < end:
        try:
            return urllib.request.urlopen(url).read()
        except OSError:
            time.sleep(0.5)
    raise StepFailed(step)


class Browser:
    """Just enough of Chrome's DevTools protocol for this session."""

    def __init__(self, ws):
        self.ws = ws
        self.count = 0

    async def call(self, method, **params):
        self.count += 1
        await self.ws.send(
            json.dumps({"id": self.count, "method": method, "params": params})
        )
        while True:
            message = json.loads(await self.ws.recv())
            if message.get("id") == self.count:
                return message.get("result", {})

    async def js(self, expression):
        result = await self.call(
            "Runtime.evaluate", expression=expression, returnByValue=True
        )
        return result.get("result", {}).get("value")

    async def wait_for(self, expression, step, timeout=60):
        end = time.time() + timeout
        while time.time() < end:
            if await self.js(expression):
                return
            await asyncio.sleep(0.5)
        raise StepFailed(step)

    async def screenshot(self):
        data = await self.call("Page.captureScreenshot", format="png")
        return base64.b64decode(data["data"])

    async def send(self, text, exchange):
        """Type a message into the chat box, press Enter, and wait for the reply."""
        await self.js(
            "document.querySelector('[data-testid=stChatInputTextArea]').focus()"
        )
        await self.call("Input.insertText", text=text)
        await asyncio.sleep(0.3)
        for kind in ("keyDown", "keyUp"):
            await self.call(
                "Input.dispatchKeyEvent",
                type=kind,
                key="Enter",
                code="Enter",
                windowsVirtualKeyCode=13,
                nativeVirtualKeyCode=13,
            )
        await self.wait_for(
            "document.querySelectorAll('[data-testid=stChatMessage]').length >= "
            f"{2 * exchange} && !document.querySelector('[data-testid=stSpinner]')",
            f"reply to {text!r}",
            REPLY_TIMEOUT,
        )
        await asyncio.sleep(1)

    async def open_tab(self, index):
        await self.js(f"document.querySelectorAll('[role=tab]')[{index}].click()")
        await self.wait_for(
            f"document.querySelectorAll('[role=tab]')[{index}]"
            ".getAttribute('aria-selected') == 'true'",
            f"tab {index}",
        )
        await asyncio.sleep(1)

    async def chat_lines(self):
        """Every chat message as 'You: …' or 'Sunny: …'. A message's own text
        starts with its avatar's icon name: face for the user."""
        messages = await self.js(
            "[...document.querySelectorAll('[data-testid=stChatMessage]')].map(m => "
            "[m.innerText.split('\\n')[0], "
            "m.querySelector('[data-testid=stChatMessageContent]').innerText])"
        )
        return [
            ("You: " if icon == "face" else "Sunny: ") + text.strip()
            for icon, text in messages
        ]

    async def texts(self, testid):
        return await self.js(
            f"[...document.querySelectorAll('[data-testid={testid}]')]"
            ".map(e => e.innerText.trim())"
        )


def orders(db_file):
    conn = sqlite3.connect(db_file)
    rows = conn.execute(
        "SELECT order_id, status, address FROM orders ORDER BY order_id"
    ).fetchall()
    conn.close()
    return [f"{order_id} {status} {address}" for order_id, status, address in rows]


async def session(port, cdp):
    targets = json.loads(wait_for_url(f"http://127.0.0.1:{cdp}/json", "chrome"))
    page = next(t for t in targets if t["type"] == "page")
    async with websockets.connect(
        page["webSocketDebuggerUrl"], max_size=50_000_000
    ) as ws:
        b = Browser(ws)
        await b.call("Page.enable")
        await b.call(
            "Emulation.setDeviceMetricsOverride",
            width=WIDTH,
            height=HEIGHT,
            deviceScaleFactor=SCALE,
            mobile=False,
        )
        await b.call("Page.navigate", url=f"http://127.0.0.1:{port}/")
        await b.wait_for(
            "!!document.querySelector('[data-testid=stChatInputTextArea]')", "page"
        )
        await asyncio.sleep(1)
        shots, steps = {}, {}

        await b.send(MESSAGES[0], 1)
        await b.send(MESSAGES[1], 2)
        steps["chat"] = await b.chat_lines()
        shots["chat.png"] = await b.screenshot()

        await b.open_tab(1)
        steps["staff waiting"] = await b.texts("stText")
        if not steps["staff waiting"]:
            raise StepFailed("no waiting request: the model did not file the change")
        shots["staff_waiting.png"] = await b.screenshot()

        clicked = await b.js(
            "(() => { const b = [...document.querySelectorAll('button')]"
            ".find(b => b.innerText.trim() == 'Approve');"
            " if (b) { b.click(); return true } return false })()"
        )
        if not clicked:
            raise StepFailed("approve button")
        await b.wait_for("!!document.querySelector('[data-testid=stAlert]')", "notice")
        await b.open_tab(1)
        steps["staff approved"] = await b.texts("stAlert")
        shots["staff_approved.png"] = await b.screenshot()
        steps["orders"] = orders(APP / "bayside.db")

        await b.open_tab(0)
        await b.send(MESSAGES[2], 3)
        steps["chat after approval"] = (await b.chat_lines())[4:]

        await b.call("Page.reload")
        await b.wait_for(
            "!!document.querySelector('[data-testid=stChatInputTextArea]')", "reload"
        )
        await asyncio.sleep(2)
        count = await b.js(
            "document.querySelectorAll('[data-testid=stChatMessage]').length"
        )
        steps["after a refresh"] = [f"chat messages: {count}"]
        return steps, shots


def main():
    port, cdp = free_port(), free_port()
    profile = tempfile.mkdtemp(prefix="week15-chrome-")
    server = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "app.py",
            "--server.headless",
            "true",
            "--server.port",
            str(port),
            "--theme.base",
            "light",
            "--browser.gatherUsageStats",
            "false",
        ],
        cwd=APP,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    chrome = subprocess.Popen(
        [
            "google-chrome",
            "--headless=new",
            "--disable-gpu",
            f"--remote-debugging-port={cdp}",
            f"--window-size={WIDTH},{HEIGHT}",
            f"--user-data-dir={profile}",
            "about:blank",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        wait_for_url(f"http://127.0.0.1:{port}/_stcore/health", "streamlit")
        steps, shots = asyncio.run(session(port, cdp))
    except StepFailed as failed:
        print(f"session.py: step failed: {failed}")
        return 1
    finally:
        chrome.terminate()
        server.terminate()
    IMAGES.mkdir(parents=True, exist_ok=True)
    for name, data in shots.items():
        (IMAGES / name).write_bytes(data)
    steps["images"] = [
        f"{name} {hashlib.sha256(data).hexdigest()}" for name, data in shots.items()
    ]
    text = "# Week 15 session: Bayside app at 8b1b491, granite4.1:3b on the CPU, "
    text += "captured by session.py\n"
    for name, lines in steps.items():
        text += f"## {name}\n" + "\n".join(lines) + "\n"
    SESSION.write_text(text)
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
