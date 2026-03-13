import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from core.orchestrator import ask
from database.data_access import (
    get_all_customers,
    get_all_products,
    get_sales_overview
)


st.set_page_config(
    page_title="NL2SQL",
    page_icon="📊",
    layout="centered"
)

st.title("NL2SQL")
st.markdown("Ask questions about the database in natural language and get answers instantly.")

st.divider()

with st.expander("📊 View Database"):
    st.subheader("Customers")
    customers = get_all_customers()
    st.dataframe(customers, use_container_width=True)

    st.subheader("Products")
    products = get_all_products()
    st.dataframe(products, use_container_width=True)

    st.subheader("Sales")
    sales = get_sales_overview()
    st.dataframe(sales, use_container_width=True)

st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

question = st.chat_input("Ask a question about the database...")

if question:
    with st.chat_message("user"):
        st.write(question)

    with st.spinner("Thinking..."):
        try:
            answer = ask(question, thread_id="user-session")
        except Exception as e:
            answer = "Something went wrong. Please try again."

    with st.chat_message("assistant"):
        st.write(answer)

    st.session_state.messages.append({"role": "user", "content": question})
    st.session_state.messages.append({"role": "assistant", "content": answer})