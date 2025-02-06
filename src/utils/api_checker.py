import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def validate_api_key(api_key):
    """Validate API key format and length"""
    if not api_key:
        return False
    if not isinstance(api_key, str):
        return False
    if len(api_key.strip()) == 0:
        return False
    # Check if it matches basic Gemini API key format
    if not api_key.startswith('AI'):
        return False
    return True

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
                help="Get your API key from https://makersuite.google.com/app/apikey"
            )
            
            submitted = st.form_submit_button("Submit API Key")
            
            if submitted:
                if validate_api_key(input_api_key):
                    # Store in session state
                    st.session_state['GEMINI_API_KEY'] = input_api_key
                    # Also set it in environment for this session
                    os.environ['GEMINI_API_KEY'] = input_api_key
                    st.success("✅ API key successfully stored!")
                    # Rerun to update the page
                    st.rerun()
                else:
                    st.error("Invalid API key format. Please check your API key and try again.")
        
        # Stop further execution until API key is provided
        st.stop()
    
    return os.getenv('GEMINI_API_KEY') or st.session_state.get('GEMINI_API_KEY')
