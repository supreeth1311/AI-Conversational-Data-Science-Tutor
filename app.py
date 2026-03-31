import streamlit as st
import google.generativeai as genai

from langchain.chains import ConversationChain
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

# ✅ Load API Key Securely
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    st.error("⚠️ Google GenAI API key is missing! Add it to `.env` file.")
    st.stop()

# ✅ Configure AI Model with Memory
genai.configure(api_key=API_KEY)
chat_model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=API_KEY)
memory = ConversationBufferMemory()
conversation = ConversationChain(llm=chat_model, memory=memory)

# ✅ Streamlit UI Setup
st.set_page_config(page_title="AI Data Science Tutor", layout="wide")
st.title("🤖 AI Data Science Tutor")
st.write("Ask me anything about **Data Science!** 📊")

# ✅ Store Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# ✅ Display Chat History
for message in st.session_state.messages:
    role = "👤 You" if message["role"] == "user" else "🤖 AI"
    st.markdown(f"**{role}:** {message['content']}")

# ✅ User Input
user_input = st.text_input("Ask a Data Science question...")

if user_input:
    # ✅ AI Response
    response = conversation.run(user_input)

    # ✅ Store and Display Chat
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "ai", "content": response})
    st.markdown(f"**🤖 AI:** {response}")

    st.rerun()
