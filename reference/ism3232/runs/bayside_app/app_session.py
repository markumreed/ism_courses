"""Drive bayside_app/app.py with Streamlit's AppTest and the real course model,
and print what a customer and a staff member would see.

Run from the repository root with Ollama running:
    python reference/ism3232/runs/bayside_app/app_session.py
The app is copied to a temporary folder first, so no bayside.db lands in the repo.
"""

import os
import shutil
import sys
import tempfile
from pathlib import Path

from streamlit.testing.v1 import AppTest

APP = Path(
    sys.argv[1] if len(sys.argv) > 1 else "reference/ism3232/bayside_app"
).resolve()
work = Path(tempfile.mkdtemp(prefix="bayside-session-"))
for path in APP.glob("*.py"):
    shutil.copy(path, work)
shutil.copy(APP / "schema.sql", work)
os.chdir(work)
sys.path.insert(0, str(work))

import database

app = AppTest.from_file(str(work / "app.py"), default_timeout=300)
app.run()
for message in [
    "Has A101 shipped yet?",
    "Please change the address on order A102 to 9 Pine Street, Tampa",
]:
    app.chat_input[0].set_value(message).run()
for chat in app.chat_message:
    print(f"{chat.name}: {chat.markdown[0].value}")
waiting = database.waiting_requests("bayside.db")
print(
    "Staff tab, waiting:",
    [(r["number"], r["order_id"], r["new_address"]) for r in waiting],
)
if waiting:
    app.button(key=f"approve{waiting[0]['number']}").click().run()
    print("Staff tab notice:", app.success[0].value)
print("A102 address now:", database.find_order("bayside.db", "A102")["address"])
app.chat_input[0].set_value("What happened to request 1?").run()
print(f"user: {app.chat_message[-2].markdown[0].value}")
print(f"assistant: {app.chat_message[-1].markdown[0].value}")
