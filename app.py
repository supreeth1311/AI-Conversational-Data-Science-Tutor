import streamlit as st
from groq import Groq

# -----------------------
# Configure API Key
# -----------------------
client = Groq(api_key=st.secrets["groq"]["API_KEY"])

# -----------------------
# UI
# -----------------------
st.set_page_config(page_title="AI Tutor", layout="wide")
st.title("🤖 AI Data Science Tutor & Code Reviewer")

mode = st.selectbox(
    "Choose Mode:",
    ["Data Science Tutor 📊", "Code Reviewer 💻"]
)

# -----------------------
# Chat History
# -----------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------
# Input
# -----------------------
user_input = st.text_area("Enter your question or code:")
submit = st.button("Submit")

# -----------------------
# Process
# -----------------------
if submit and user_input.strip() != "":

    if mode == "Data Science Tutor 📊":
        prompt = f"Explain clearly with examples:\n{user_input}"
    else:
        prompt = f"Review this code, find errors and fix:\n{user_input}"

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        answer = response.choices[0].message.content

    except Exception as e:
        answer = f"⚠️ Error: {str(e)}"

    # Save messages
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "ai", "content": answer})

    st.rerun()

# -----------------------
# Display
# -----------------------
for msg in st.session_state.messages:
    role = "👤 You" if msg["role"] == "user" else "🤖 AI"
    st.markdown(f"**{role}:** {msg['content']}")
