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
st.title("🤖 AI Data Science Tutor & Code Reviewer")

# Mode selection (RESTORED FEATURE ✅)
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

if st.button("Submit") and user_input:
    
    # 🎯 Prompt Engineering based on mode
    if mode == "Data Science Tutor 📊":
        prompt = f"""
        You are a helpful Data Science Tutor.
        Explain concepts clearly with examples.

        Question:
        {user_input}
        """
    else:
        prompt = f"""
        You are an expert Python Code Reviewer.
        Analyze the code, find errors, and suggest improvements.

        Code:
        {user_input}
        """

    try:
        response = model.generate_content(prompt)
        answer = response.text
    except Exception as e:
        answer = "⚠️ Error generating response. Check API key or internet."

    # Display messages
for msg in st.session_state.messages:
    role = "👤 You" if msg["role"] == "user" else "🤖 AI"
    st.markdown(f"**{role}:** {msg['content']}")


    # Save messages
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "ai", "content": answer})

    st.rerun()
