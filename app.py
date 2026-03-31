import streamlit as st
import google.generativeai as genai

# -----------------------
# Google Gemini API Key
# -----------------------
GEMINI_API_KEY = st.secrets["gemini"]["API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)

# -----------------------
# Load Model
# -----------------------
model = genai.GenerativeModel("gemini-1.5-flash")

# -----------------------
# Streamlit UI # ----------------------- 
st.set_page_config(page_title="AI Conversational Data Science Tutor", layout="wide") 
st.title("🤖 AI Conversational Data Science Tutor ")
st.write("Ask me anything about **Data Science!** 📊")

# -----------------------
# Chat History
# -----------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    role = "👤 You" if msg["role"] == "user" else "🤖 AI"
    st.markdown(f"**{role}:** {msg['content']}")

# -----------------------
# User Input
# -----------------------
user_input = st.text_input("Ask a Data Science question...")

if user_input:
    # Generate response from Gemini
    response = model.generate_content(user_input)
    answer = response.text

    # Store messages
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "ai", "content": answer})

    # Display response
    st.markdown(f"**🤖 AI:** {answer}")
    st.rerun()
