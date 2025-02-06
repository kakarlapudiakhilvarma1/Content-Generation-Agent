from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def validate_api_key(api_key):
    """Validate that API key exists and has the correct format"""
    if not api_key:
        raise ValueError("Gemini API key is missing. Please check your .env file or session state.")
    if not isinstance(api_key, str):
        raise ValueError("API key must be a string.")
    if len(api_key.strip()) == 0:
        raise ValueError("API key cannot be empty.")
    return api_key.strip()

def generate_content(topic, content_type, target_audience, temperature, max_words):
    try:
        # Get and validate API key
        api_key = os.getenv('GEMINI_API_KEY')
        api_key = validate_api_key(api_key)

        # Configure LLM with validated API key
        llm = LLM(
            model="gemini/gemini-pro",  # Updated to use the correct model name
            api_key=api_key,
            temperature=temperature
        )
        
        # Initialize search tool with error handling
        try:
            search_tool = SerperDevTool(n=10)
        except Exception as e:
            raise Exception(f"Failed to initialize search tool: {str(e)}")

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

    except ValueError as ve:
        raise Exception(f"API Key Error: {str(ve)}")
    except Exception as e:
        raise Exception(f"Content Generation Error: {str(e)}")
