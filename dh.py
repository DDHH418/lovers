import streamlit as st
from datetime import date
import base64

# -----------------------------
# User login credentials
users = {
    "Honey": "dharu123",
    "Dharu": "honey123"
}

# -----------------------------
# Page setup and styles
st.set_page_config(page_title="Lover's App 💞", layout="centered")
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

# -----------------------------
# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "messages" not in st.session_state:
    st.session_state.messages = []
if "memories" not in st.session_state:
    st.session_state.memories = []

# -----------------------------
# Login Page
if not st.session_state.logged_in:
    st.title("💌 Lover's Login")
    username = st.text_input("Name")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
        else:
            st.error("Wrong name or password 😢")

# -----------------------------
# Lover Area: After Login
else:
    st.title(f"Welcome, {st.session_state.username} 💑")
    tabs = st.tabs(["💬 Chat & Quotes", "🕰️ Memory Timeline"])

    # -----------------------------
    # Chat & Quotes Tab
    with tabs[0]:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("❤️ Chat with Your Love")
            msg = st.text_input("Type your message")
            if st.button("Send"):
                # Send message to partner
                receiver = "Dharu" if st.session_state.username == "Honey" else "Honey"
                st.session_state.messages.append({
                    "sender": st.session_state.username,
                    "receiver": receiver,
                    "text": msg
                })

            # Display messages between the two
            st.markdown("### 💌 Conversation")
            for chat in st.session_state.messages:
                if (chat["sender"] == st.session_state.username and chat["receiver"] != st.session_state.username) or \
                   (chat["receiver"] == st.session_state.username and chat["sender"] != st.session_state.username):
                    st.markdown(f"❤️ **{chat['sender']}** ➤ {chat['text']}")

        with col2:
            st.subheader("📖 Lovely / Funny Quotes")
            st.markdown("""
            - *"You're my favorite hello and hardest goodbye 💘"*
            - *"You had me at 'Hello' 😍"*
            - *"Love is when you steal someone’s heart and they let you keep it 💝"*
            - *"You're the peanut butter to my jelly 🥜"*
            """)

    # -----------------------------
    # Memory Timeline Tab
    with tabs[1]:
        st.subheader("🕰️ Add a Memory")
        mem_date = st.date_input("Date", date.today())
        mem_title = st.text_input("Memory Title")
        mem_note = st.text_area("Write about your moment")
        mem_img = st.file_uploader("Upload a photo (optional)", type=["jpg", "jpeg", "png"])

        if st.button("Save Memory"):
            image_data = None
            if mem_img:
                image_data = base64.b64encode(mem_img.read()).decode("utf-8")
            st.session_state.memories.append({
                "date": mem_date,
                "title": mem_title,
                "note": mem_note,
                "image": image_data
            })
            st.success("Memory added to your love story 💌")

        st.markdown("---")
        st.subheader("🌸 Timeline Memories")
        for memory in sorted(st.session_state.memories, key=lambda x: x["date"]):
            st.markdown(f"### 📅 {memory['date']} - {memory['title']}")
            st.markdown(f"> {memory['note']}")
            if memory["image"]:
                st.image(base64.b64decode(memory["image"]), use_column_width=True)
            st.markdown("---")
