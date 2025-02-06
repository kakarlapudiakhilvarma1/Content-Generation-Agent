import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_api_key():
    """Check if Gemini API key exists in environment variables or session state"""
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key and 'GEMINI_API_KEY' not in st.session_state:
        # Create a form for API key input
        st.warning("⚠️ Gemini API key not found in environment variables")
        
        with st.form("api_key_form"):
            input_api_key = st.text_input(
                "Please enter your Gemini API key:",
                type="password",
                help="Your API key will be stored securely in the session state"
            )
            
            submitted = st.form_submit_button("Submit API Key")
            
            if submitted and input_api_key:
                # Store in session state
                st.session_state['GEMINI_API_KEY'] = input_api_key
                # Also set it in environment for this session
                os.environ['GEMINI_API_KEY'] = input_api_key
                st.success("✅ API key successfully stored!")
                # Rerun to update the page
                st.rerun()
            elif submitted:
                st.error("Please enter an API key")
        
        # Stop further execution until API key is provided
        st.stop()
    
    return os.getenv('GEMINI_API_KEY') or st.session_state.get('GEMINI_API_KEY')