from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool
import streamlit as st
import os
from dotenv import load_dotenv
from fpdf import FPDF
import markdown
import time
import re

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

# Configure Streamlit page
st.set_page_config(
    page_title="AI Content Studio",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
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
    /* Move sidebar to the left */
    section[data-testid="stSidebar"] {
        position: fixed;
        left: 0;
        width: 300px !important;
        background-color: #f8f9fa;
        height: 100vh;
        overflow-y: auto;
    }
    /* Adjust main content area */
    .main {
        margin-left: 300px;
        padding: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Check API key before proceeding
api_key = check_api_key()

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

def clean_html_tags(text):
    """Remove HTML tags and clean up the text for PDF generation"""
    # Remove HTML tags
    clean_text = re.sub(r'<[^>]+>', '', text)
    # Remove multiple newlines
    clean_text = re.sub(r'\n\s*\n', '\n\n', clean_text)
    # Remove special characters
    clean_text = clean_text.replace('&nbsp;', ' ').replace('&amp;', '&')
    return clean_text.strip()

class ContentPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'AI Content Studio - Generated Content', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(10)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        # Split body into paragraphs
        paragraphs = body.split('\n\n')
        for paragraph in paragraphs:
            if paragraph.strip():
                self.multi_cell(0, 10, paragraph.strip())
                self.ln(5)

def markdown_to_pdf(content, filename, topic):
    pdf = ContentPDF()
    pdf.add_page()
    
    # Clean and format the content
    clean_content = clean_html_tags(content)
    
    # Add title
    pdf.chapter_title(topic)
    
    # Add content
    pdf.chapter_body(clean_content)
    
    pdf.output(filename)

def generate_content(topic, content_type, target_audience, temperature, max_words):
    # Configure LLM with the API key from session state or environment
    api_key = os.getenv('GEMINI_API_KEY') or st.session_state.get('GEMINI_API_KEY')
    llm = LLM(model="gemini/gemini-1.5-flash", api_key=api_key)
    search_tool = SerperDevTool(n=10)

    # Research Analyst Agent
    senior_research_analyst = Agent(
        role="Senior Research Analyst",
        goal=f"Research and analyze {topic} for a {content_type} aimed at a {target_audience} audience.",
        backstory="""Expert research analyst with advanced skills in data synthesis and analysis.
                    Specialized in creating comprehensive research briefs with verified sources.""",
        llm=llm,
        tools=[search_tool],
        allow_delegation=False,
        verbose=True
    )

    # Content Writer Agent
    content_writer = Agent(
        role="Content Writer",
        goal=f"Create engaging {content_type} content while maintaining accuracy and professional tone.",
        backstory="""Professional content writer with expertise in creating engaging,
                    well-structured content for various audiences and formats.""",
        allow_delegation=False,
        llm=llm,
        verbose=True
    )

    # Research Task
    research_task = Task(
        description=f"""
            Conduct comprehensive research on {topic} considering:
            - Target audience: {target_audience}
            - Content type: {content_type}
            - Maximum length: {max_words} words
            
            Include:
            1. Latest developments and trends
            2. Expert insights and analysis
            3. Relevant statistics and data
            4. Credible source citations
        """,
        expected_output="""
            Detailed research report with:
            - Executive summary
            - Key findings and insights
            - Verified facts and statistics
            - Source citations and references
        """,
        agent=senior_research_analyst
    )

    # Writing Task
    writing_task = Task(
        description=f"""
            Create {content_type} content that:
            1. Matches {target_audience} audience expectations
            2. Maintains professional tone and clarity
            3. Incorporates research findings effectively
            4. Stays within {max_words} words
            5. Includes proper citations and references
        """,
        expected_output=f"""
            Professional {content_type} with:
            - Clear structure and formatting
            - Engaging yet informative tone
            - Proper source citations
            - References section
        """,
        agent=content_writer
    )

    # Create and execute crew
    crew = Crew(
        agents=[senior_research_analyst, content_writer],
        tasks=[research_task, writing_task],
        verbose=True
    )

    result = crew.kickoff(inputs={"topic": topic})
    return str(result)

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
            
            # Display results in a clean format
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
            
            # Success message
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