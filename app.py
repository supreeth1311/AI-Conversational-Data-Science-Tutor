import streamlit as st
import google.generativeai as genai

# -----------------------
# Configure API Key
# -----------------------
genai.configure(api_key=st.secrets["gemini"]["API_KEY"])

# -----------------------
# Load Model
# -----------------------
model = genai.GenerativeModel("gemini-1.5-flash")

# -----------------------
# UI
# -----------------------
st.set_page_config(page_title="AI Tutor", layout="wide")
st.title("🤖 AI Data Science Tutor")
st.write("Ask me anything about Data Science 📊")

# -----------------------
# Chat History
# -----------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show old messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**👤 You:** {msg['content']}")
    else:
        st.markdown(f"**🤖 AI:** {msg['content']}")

# -----------------------
# Input
# -----------------------
user_input = st.text_input("Ask a question...")

if user_input:
    try:
        response = model.generate_content(user_input)
        answer = response.text
    except Exception as e:
        answer = "Error generating response. Check API key or internet."

    # Save chat
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "ai", "content": answer})

    st.rerun()
