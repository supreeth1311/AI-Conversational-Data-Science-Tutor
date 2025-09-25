import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# -----------------------
# Hugging Face API Key
# -----------------------
HF_API_KEY = st.secrets["huggingface"]["API_KEY"]

# -----------------------
# Load Model
# -----------------------
model_name = "mosaicml/mpt-7b-instruct"  # Free instruction-following model
tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=HF_API_KEY)
model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=HF_API_KEY)

# Optional: use GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# -----------------------
# Streamlit UI
# -----------------------
st.set_page_config(page_title="AI Conversational Data Science Tutor", layout="wide")
st.title("🤖 AI Conversational Data Science Tutor (Hugging Face)")
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
    # Encode input and generate response
    inputs = tokenizer(user_input, return_tensors="pt").to(device)
    outputs = model.generate(**inputs, max_new_tokens=200)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Store messages in session
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "ai", "content": answer})

    # Display AI response
    st.markdown(f"**🤖 AI:** {answer}")
    st.rerun()
