import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI

# Retrieve the OpenRouter API key from Streamlit secrets
OPENROUTER_API_KEY = st.secrets["openrouter"]["API_KEY"]
if not OPENROUTER_API_KEY:
    st.error("⚠️ OpenRouter API key is missing!")
    st.stop()

# Function to create conversation model
def create_conversation(model_name):
    chat_model = ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
        model=model_name,  # Gemini model
    )
    memory = ConversationBufferMemory()
    return ConversationChain(llm=chat_model, memory=memory, verbose=True)

# Try Pro first, fallback to Flash if it fails
try:
    conversation = create_conversation("google/gemini-pro")  # Gemini Pro
except Exception as e:
    st.warning(f"⚠️ Pro model issue ({e}). Switching to Flash model...")
    conversation = create_conversation("google/gemini-flash-1.5")  # Gemini Flash

# Streamlit UI
st.set_page_config(page_title="AI Conversational Data Science Tutor", layout="wide")
st.title("🤖 AI Conversational Data Science Tutor")
st.write("Ask me anything about **Data Science!** 📊")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    role = "👤 You" if message["role"] == "user" else "🤖 AI"
    st.markdown(f"**{role}:** {message['content']}")

# User input
user_input = st.text_input("Ask a Data Science question...")

if user_input:
    try:
        # Use invoke() for OpenRouter
        response = conversation.invoke({"input": user_input})
        answer = response["response"] if isinstance(response, dict) else str(response)

        # Store and display
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "ai", "content": answer})
        st.markdown(f"**🤖 AI:** {answer}")

        st.rerun()

    except Exception as e:
        st.error(f"❌ Error: {e}")
