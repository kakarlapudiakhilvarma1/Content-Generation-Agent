import streamlit as st
import os
from utils.api_checker import check_api_key
from utils.pdf_generator import markdown_to_pdf
from agents.content_crew import generate_content
import time

__import__('pysqlite3')
import sys

sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')


# Configure Streamlit page
st.set_page_config(
    page_title="AI Content Studio",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Directly embedded
st.markdown("""
    <style>
    .stApp {
        max-width: 100%;
        padding: 1rem;
    }

    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(120deg, #155799, #159957);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }

    .status-box {
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }

    .feature-box {
        border: 1px solid #e0e0e0;
        padding: 1.5rem;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }

    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f0f2f6;
        padding: 1rem;
        text-align: center;
        border-top: 1px solid #ddd;
        z-index: 100;
    }

    .footer-content {
        display: flex;
        justify-content: space-around;
        align-items: center;
        max-width: 1200px;
        margin: 0 auto;
    }

    .sidebar .stButton {
        width: 100%;
    }

    section[data-testid="stSidebar"] {
        position: fixed;
        left: 0;
        width: 300px !important;
        background-color: #f8f9fa;
        height: 100vh;
        overflow-y: auto;
        z-index: 99;
    }

    .main {
        margin-left: 300px;
        padding: 2rem;
        max-width: calc(100% - 300px);
    }

    .stTextInput input, .stSelectbox select, .stTextArea textarea {
        border-radius: 5px;
    }

    .stProgress > div > div {
        background-color: #159957;
    }

    .streamlit-expanderHeader {
        background-color: #f8f9fa;
        border-radius: 5px;
    }

    .streamlit-expanderContent {
        background-color: white;
        border-radius: 0 0 5px 5px;
    }

    .stButton > button {
        background-color: #159957;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        transition: background-color 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #0f7a3d;
    }

    .stDownloadButton > button {
        background-color: #155799;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        transition: background-color 0.3s ease;
    }

    .stDownloadButton > button:hover {
        background-color: #0e4276;
    }

    .main > div:last-child {
        margin-bottom: 60px;
    }

    @media (max-width: 768px) {
        section[data-testid="stSidebar"] {
            width: 100% !important;
            height: auto;
            position: relative;
        }
        
        .main {
            margin-left: 0;
            max-width: 100%;
            padding: 1rem;
        }
        
        .footer-content {
            flex-direction: column;
            gap: 0.5rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Check API key before proceeding
api_key = check_api_key()

# Rest of your main.py code remains the same...
# Header Section
st.markdown("""
    <div class="main-header">
        <h1>Content Generation Agent</h1>
        <p>Professional Content Research & Writing Platform</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.header("Content Configuration")
    
    # Project Settings
    with st.expander("📝 Project Settings", expanded=True):
        topic = st.text_area(
            "Content Topic",
            height=100,
            placeholder="Enter your topic or subject matter...",
            help="Be specific about your topic for better results"
        )
        
        content_type = st.selectbox(
            "Content Type",
            ["Blog Post", "Article", "Research Paper", "Technical Guide"],
            help="Select the type of content you want to generate"
        )
        
        target_audience = st.selectbox(
            "Target Audience",
            ["General", "Technical", "Business", "Academic"],
            help="Choose your intended audience"
        )

    # Advanced Settings
    with st.expander("⚙️ Advanced Settings"):
        temperature = st.slider(
            "Creativity Level",
            0.0, 1.0, 0.7,
            help="Higher values make the output more creative but less focused"
        )
        
        max_words = st.number_input(
            "Maximum Word Count",
            min_value=500,
            max_value=5000,
            value=1500,
            step=500,
            help="Set the maximum length of the generated content"
        )

    # Generate Button
    generate_button = st.button(
        "Generate Content",
        type="primary",
        use_container_width=True,
    )

# Main content area
if generate_button and topic:
    # Create columns for progress tracking
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("📊 Research in Progress")
    with col2:
        st.info("✍️ Writing in Progress")
    with col3:
        st.info("🔄 Finalizing Content")

    with st.spinner('Generating your content...'):
        try:
            # Add progress bar
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.1)
                progress_bar.progress(i + 1)
            
            result = generate_content(
                topic,
                content_type,
                target_audience,
                temperature,
                max_words
            )
            
            # Display results
            st.markdown("### Generated Content")
            with st.expander("View Content", expanded=True):
                st.markdown(result)
            
            # Create temporary file names
            temp_dir = "temp_files"
            os.makedirs(temp_dir, exist_ok=True)
            pdf_filename = os.path.join(temp_dir, f"{topic.lower().replace(' ', '_')}_{content_type.lower()}.pdf")
            
            try:
                # Convert to PDF
                markdown_to_pdf(result, pdf_filename, topic)
                
                # Download options
                col1, col2 = st.columns(2)
                with col1:
                    with open(pdf_filename, "rb") as pdf_file:
                        st.download_button(
                            label="Download as PDF",
                            data=pdf_file,
                            file_name=os.path.basename(pdf_filename),
                            mime="application/pdf"
                        )
                with col2:
                    st.download_button(
                        label="Download as Markdown",
                        data=result,
                        file_name=f"{topic.lower().replace(' ', '_')}_{content_type.lower()}.md",
                        mime="text/markdown"
                    )
            finally:
                # Clean up temporary files
                if os.path.exists(pdf_filename):
                    os.remove(pdf_filename)
                try:
                    os.rmdir(temp_dir)
                except OSError:
                    pass
            
            st.success("Content generated successfully! You can now download it in your preferred format.")
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.info("Please try again or contact support if the issue persists.")
elif generate_button:
    st.warning("Please enter a topic before generating content.")

# Fixed Footer
st.markdown("""
    <div class="footer">
        <div class="footer-content">
            <div>Built with ❤️ using CrewAI</div>
            <div>Powered by Gemini</div>
            <div>© Devloped by Akhil</div>
        </div>
    </div>
""", unsafe_allow_html=True)
