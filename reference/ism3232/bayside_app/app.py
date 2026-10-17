# app.py
# Author: [Your Name]

import streamlit as st

from agent import SupportChatbot
from database import (
    all_orders,
    approve_request,
    create_tables,
    product_names,
    reject_request,
    restock,
    status_report,
    waiting_requests,
)
from fallback_model import FallbackModel
from keyword_model import KeywordModel
from ollama_model import OllamaModel
from settings import DB_FILE, INSTRUCTIONS, MODEL_NAME
from tools import BaysideTools

COURSE_MODEL = "Course model, keyword rules if it is down"
KEYWORDS_ONLY = "Keyword rules only (no AI)"


def make_model(choice):
    """Return the model the sidebar asks for."""
    if choice == KEYWORDS_ONLY:
        return KeywordModel()
    return FallbackModel(OllamaModel(MODEL_NAME), KeywordModel())


def show(text):
    """Write text in the page. A $ is escaped so Streamlit does not read it as math."""
    st.markdown(text.replace("$", "\\$"))


create_tables(DB_FILE)
st.title("Bayside Outfitters")
choice = st.sidebar.radio("Model", [COURSE_MODEL, KEYWORDS_ONLY])

if "bot" not in st.session_state:
    tools = BaysideTools(DB_FILE)
    st.session_state.bot = SupportChatbot("Sunny", INSTRUCTIONS, tools, KeywordModel())
bot = st.session_state.bot
bot.model = make_model(choice)

chat_tab, staff_tab = st.tabs(["Chat", "Staff"])

with chat_tab:
    for message in bot.history:
        if message["role"] != "tool":
            with st.chat_message(message["role"]):
                show(message["content"])
    user_message = st.chat_input(
        "Ask Sunny about an order, stock, or an address change"
    )
    if user_message:
        with st.spinner("Sunny is thinking..."):
            bot.respond(user_message)
        st.rerun()

with staff_tab:
    if "notice" in st.session_state:
        st.success(st.session_state.notice)
        del st.session_state.notice

    st.subheader("Waiting for approval")
    waiting = waiting_requests(DB_FILE)
    if waiting == []:
        st.write("Nothing is waiting.")
    for request in waiting:
        number = request["number"]
        text_col, approve_col, reject_col = st.columns([4, 1, 1])
        text_col.write(
            f"Request {number}: {request['order_id']} to {request['new_address']}"
        )
        if approve_col.button("Approve", key=f"approve{number}"):
            st.session_state.notice = approve_request(DB_FILE, number)
            st.rerun()
        if reject_col.button("Reject", key=f"reject{number}"):
            st.session_state.notice = reject_request(DB_FILE, number)
            st.rerun()

    st.subheader("Orders")
    st.dataframe(all_orders(DB_FILE))

    st.subheader("Orders by status")
    st.dataframe(status_report(DB_FILE))

    st.subheader("Restock a product")
    with st.form("restock"):
        name = st.selectbox("Product", product_names(DB_FILE))
        stock = st.number_input("New stock", min_value=0, step=1)
        if st.form_submit_button("Save"):
            restock(DB_FILE, name, int(stock))
            st.session_state.notice = f"The {name} now has {int(stock)} in stock."
            st.rerun()
