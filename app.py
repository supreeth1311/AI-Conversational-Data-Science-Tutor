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
st.set_page_config(page_title="AI DS & Code Assistant", layout="centered")
st.title("🤖 AI Data Science/Code Assistant")

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
                # Select the appropriate system prompt based on user choice
                current_sys_instruction = sys_prompt_ds if option == "Data Science Tutor" else sys_prompt_code

                # Initialize the Gemini model with system instructions
                model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    system_instruction=current_sys_instruction
                )

                # Generate the content
                response = model.generate_content(user_prompt)

                # Check if the response was blocked or empty
                if response and response.text:
                    st.success("✅ Response Generated!")
                    st.markdown("---")
                    st.write(response.text)
                else:
                    st.error("❌ The model could not generate a response. This might be due to safety filters.")

            except Exception as e:
                st.error(f"🚨 An error occurred: {str(e)}")
    else:
        st.warning("⚠️ Please enter a valid query or Python code!")
