import streamlit as st
import google.generativeai as genai
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_google_genai import ChatGoogleGenerativeAI
from google.api_core.exceptions import ResourceExhausted

# Retrieve the API key from Streamlit secrets
GOOGLE_API_KEY = st.secrets["google"]["GEMINI_API_KEY"]
if not GOOGLE_API_KEY:
    st.error("⚠️ Google GenAI API key is missing in Streamlit secrets!")
    st.stop()

# Configure API key
genai.configure(api_key=GOOGLE_API_KEY)

# Function to create conversation model with fallback
def create_conversation(model_name):
    chat_model = ChatGoogleGenerativeAI(model=model_name, google_api_key=GOOGLE_API_KEY)
    memory = ConversationBufferMemory()
    return ConversationChain(llm=chat_model, memory=memory)

# Try Pro first, fallback to Flash if ResourceExhausted
try:
    conversation = create_conversation("gemini-1.5-pro-latest")
except ResourceExhausted:
    st.warning("⚠️ Pro model quota exhausted. Switching to Flash model...")
    conversation = create_conversation("gemini-1.5-flash-latest")

# ✅ Streamlit UI Setup
st.set_page_config(page_title="AI Conversational Data Science Tutor", layout="wide")
st.title("🤖 AI Conversational Data Science Tutor")
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
    try:
        # ✅ AI Response
        response = conversation.run(user_input)

        # ✅ Store and Display Chat
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "ai", "content": response})
        st.markdown(f"**🤖 AI:** {response}")

        st.rerun()

    except ResourceExhausted:
        st.error("❌ Both Pro and Flash models have hit quota limits. Try again later or upgrade billing.")
