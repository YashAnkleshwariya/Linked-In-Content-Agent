# app.py
import streamlit as st
from auth import authenticate_user, register_user, increment_usage
from crew import LinkedInContentCrew
from dashboard import show_admin_dashboard
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="LinkedIn AI Content Creator", layout="centered")

# --- SESSION STATE ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "role" not in st.session_state:
    st.session_state.role = None
if "email" not in st.session_state:
    st.session_state.email = None

# --- LOGIN / REGISTER SCREEN ---
if not st.session_state.authenticated:
    st.title("🔐 Login / Register")

    action = st.radio("Select action:", ["Login", "Register"], horizontal=True)
    email = st.text_input("Email or Username")
    password = st.text_input("Password", type="password")

    if action == "Register":
        if st.button("📝 Register"):
            ok, msg = register_user(email, password)
            st.info(msg)
    else:
        if st.button("🔓 Login"):
            ok, role = authenticate_user(email, password)
            if ok:
                st.session_state.authenticated = True
                st.session_state.role = role
                st.session_state.email = email
                st.success(f"Welcome, {email}!")
                st.rerun()
            else:
                st.error("Invalid credentials.")
    st.stop()

# --- SIDEBAR ---
st.sidebar.success(f"Logged in as: {st.session_state.email} ({st.session_state.role})")
if st.sidebar.button("🚪 Logout"):
    st.session_state.authenticated = False
    st.session_state.email = None
    st.session_state.role = None
    st.rerun()

# --- ADMIN DASHBOARD ---
if st.session_state.role == "admin":
    st.sidebar.subheader("⚙️ Admin Panel")
    if st.sidebar.button("Open Dashboard"):
        show_admin_dashboard()
        st.stop()

# --- MAIN USER INTERFACE ---
st.title("🚀 LinkedIn AI Content Creator (Gemini 2.5 Flash)")

with st.form("linkedin_form"):
    topic = st.text_input("💡 Post Topic", placeholder="How AI helps Quantum computing")
    audience = st.text_input("🎯 Target Audience", placeholder="e.g. startup founders, data scientists")
    tone = st.selectbox("🎭 Tone", ["Professional", "Friendly", "Inspirational", "Analytical"])
    length = st.selectbox("📏 Post Length", ["Short", "Medium", "Long"])
    hashtags = st.text_input("🏷️ Hashtags", placeholder="#AI, #Innovation")
    call_to_action = st.text_input("📣 Call to Action", placeholder="Follow me for more insights!")
    temperature = st.slider("🔥 Creativity", 0.3, 1.0, 0.7)
    submitted = st.form_submit_button("✨ Generate LinkedIn Post")

if submitted:
    if not topic.strip():
        st.error("Please enter a topic.")
    else:
        st.info("🤖 Generating content using Gemini 2.5 Flash...")
        crew = LinkedInContentCrew(topic, audience, tone, length, hashtags, call_to_action, temperature)
        with st.spinner("Please wait..."):
            result = crew.kickoff()
        increment_usage(st.session_state.email)
        st.success("✅ Post generated successfully!")

        st.subheader("📋 Strategy Brief")
        st.write(result.get("brief"))
        st.subheader("✍️ Draft Post")
        st.write(result.get("draft"))
        st.subheader("🔎 Final Edited Post")
        st.write(result.get("final_post"))

st.markdown("---")
st.markdown("Made with ❤️ using Google Gemini & Streamlit")
