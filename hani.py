import streamlit as st
from datetime import date
import base64

# User credentials
users = {
    "Honey": "dharu123",
    "Dharu": "honey123"
}

# Global message store
if "all_messages" not in st.session_state:
    st.session_state.all_messages = []

if "all_memories" not in st.session_state:
    st.session_state.all_memories = []

# Login state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Page design
st.set_page_config(page_title="Lover App 💌", layout="centered")
st.markdown("""
    <style>
    body {
        background: linear-gradient(to bottom right, #A9A17C, #D2B48C);
        color: #4B2E2E;
        font-family: 'Trebuchet MS', sans-serif;
    }
    .stTextInput > div > div > input {
        color: #4B2E2E;
    }
    .stButton>button {
        background-color: #A9A17C;
        color: #4B2E2E;
        border: none;
        padding: 10px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Login Page ---
if not st.session_state.logged_in:
    st.title("💌 Lover's Login")
    username = st.text_input("Name")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
        else:
            st.error("Incorrect name or password ❌")

# --- Lover App ---
else:
    st.title(f"Welcome, {st.session_state.username} 💞")
    tabs = st.tabs(["💬 Chat & Quotes", "🕰️ Memories"])

    # --- Chat Tab ---
    with tabs[0]:
        st.subheader("💬 Chat Box")
        message = st.text_input("Write a message to your love", key="chatbox")
        if st.button("Send Message"):
            receiver = "Dharu" if st.session_state.username == "Honey" else "Honey"
            st.session_state.all_messages.append({
                "sender": st.session_state.username,
                "receiver": receiver,
                "text": message
            })

        st.markdown("### 💖 Conversation")
        for msg in st.session_state.all_messages:
            if msg["sender"] == st.session_state.username or msg["receiver"] == st.session_state.username:
                st.markdown(f"**{msg['sender']} ➤** {msg['text']}")

        st.markdown("----")
        st.markdown("### 🌸 Lovely Quotes")
        st.write("💌 'You're my moon and stars.'")
        st.write("😂 'You're the cheese to my dosa.'")
        st.write("💖 'No WiFi needed, our hearts are already connected.'")

    # --- Memory Timeline Tab ---
    with tabs[1]:
        st.subheader("🕰️ Add a Special Memory")
        mem_date = st.date_input("Memory Date", date.today())
        mem_title = st.text_input("Memory Title")
        mem_note = st.text_area("Write your memory")
        mem_image = st.file_uploader("Upload an image (optional)", type=["jpg", "jpeg", "png"])

        if st.button("Save Memory"):
            image_data = None
            if mem_image:
                image_data = base64.b64encode(mem_image.read()).decode()
            st.session_state.all_memories.append({
                "date": mem_date,
                "title": mem_title,
                "note": mem_note,
                "image": image_data,
                "user": st.session_state.username
            })
            st.success("Memory saved 💝")

        st.markdown("---")
        st.markdown("## 💫 Timeline")
        for mem in sorted(st.session_state.all_memories, key=lambda x: x["date"]):
            if mem["user"] == st.session_state.username:
                st.markdown(f"### {mem['date']} — {mem['title']}")
                st.markdown(f"> {mem['note']}")
                if mem["image"]:
                    st.image(base64.b64decode(mem["image"]), use_column_width=True)
                st.markdown("---")
