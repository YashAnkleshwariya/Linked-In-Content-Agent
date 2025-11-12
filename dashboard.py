# dashboard.py
import streamlit as st
from auth import get_all_users

def show_admin_dashboard():
    st.title("🧑‍💼 Admin Dashboard")
    st.write("Welcome, Admin! Below is an overview of all registered users.")

    users = get_all_users()
    if not users:
        st.info("No registered users yet.")
        return

    st.subheader("👥 Registered Users")
    st.table(users)
