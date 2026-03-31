import streamlit as st
import google.generativeai as genai
import os

# Securely fetch API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("❌ API Key is missing! Set GOOGLE_API_KEY in your environment or Streamlit Secrets.")
else:
    genai.configure(api_key=GOOGLE_API_KEY)

# -----------------------
# System Prompts
# -----------------------
sys_prompt_ds = """You are a helpful AI Tutor for Data Science.
Students will ask you doubts related to various topics in data science.
You are expected to reply in as much detail as possible.
Make sure to take examples while explaining a concept.
In case a student asks any question outside the data science scope,
politely decline and tell them to ask the question from the data science domain only."""

sys_prompt_code = """You are a professional AI Code Reviewer.
Users will submit Python code, and you should:
1. Analyze it for potential bugs, errors, and inefficiencies.
2. Provide a fixed version of the code.
3. Explain the necessary changes and improvements.
4. Do not provide assistance for non-Python code.
"""

# -----------------------
# UI
# -----------------------
st.set_page_config(page_title="AI Assistant", layout="centered")
st.title("🤖 AI Data Science & Code Assistant")

option = st.selectbox("Choose your assistant:", ["Data Science Tutor", "Code Reviewer"])

user_prompt = st.text_area("Enter your query or Python code:", height=200)

btn_click = st.button("Generate Answer")

# -----------------------
# MAIN LOGIC
# -----------------------
if btn_click:
    if user_prompt.strip():
        with st.spinner("Generating response... Please wait."):
            try:
                # 1. Select prompt
                current_instruction = sys_prompt_ds if option == "Data Science Tutor" else sys_prompt_code

                # 2. Use the latest 2026 model: gemini-3-flash-preview
                # Using system_instruction parameter is the proper way to set the persona
                model = genai.GenerativeModel(
                    model_name="gemini-3-flash-preview",
                    system_instruction=current_instruction
                )

                # 3. Generate response
                response = model.generate_content(user_prompt)

                if response and response.text:
                    st.success("✅ Response Generated!")
                    st.markdown("---")
                    st.markdown(response.text)
                else:
                    st.error("❌ Empty response. This can happen if the safety filters block the prompt.")

            except Exception as e:
                # Catching specific 404/model errors to give better feedback
                if "404" in str(e):
                    st.error("🚨 Model not found. Please ensure you are using 'gemini-3-flash-preview' or 'gemini-3.1-pro-preview'.")
                else:
                    st.error(f"🚨 An error occurred: {str(e)}")
    else:
        st.warning("⚠️ Please enter a valid query or Python code!")
