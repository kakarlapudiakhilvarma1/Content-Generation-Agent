# Content-Generation-Agent ✍️

A professional content research and writing platform powered by CrewAI and Gemini LLM. This application leverages AI agents to generate high-quality, well-researched content for various purposes including blog posts, articles, research papers, and technical guides.

## 🌟 Features

- **Intelligent Content Generation**: Utilizes two specialized AI agents:
  - Senior Research Analyst for comprehensive research and fact-finding
  - Content Writer for creating engaging, well-structured content

- **Customizable Settings**:
  - Multiple content types (Blog Post, Article, Research Paper, Technical Guide)
  - Target audience selection
  - Adjustable creativity level
  - Configurable word count limits

- **Professional Output**:
  - Well-structured content with proper citations
  - Export options in both PDF and Markdown formats
  - Clean, professional formatting

- **User-Friendly Interface**:
  - Streamlit-based web interface
  - Progress tracking
  - Interactive configuration options
  - Responsive design

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- Gemini API key
- SerperDev API key (for research capabilities)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-content-studio.git
cd ai-content-studio
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your API keys:
```env
GEMINI_API_KEY=your_gemini_api_key_here
SERPER_API_KEY=your_serper_api_key_here
```

### Running the Application

1. Start the Streamlit server:
```bash
streamlit run app.py
```

2. Open your browser and navigate to `http://localhost:8501`

## 🛠️ Configuration Options

### Project Settings
- **Content Topic**: Specify your subject matter
- **Content Type**: Choose from various content formats
- **Target Audience**: Select your intended reader base

### Advanced Settings
- **Creativity Level**: Adjust the temperature (0.0 - 1.0)
- **Maximum Word Count**: Set content length (500 - 5000 words)

## 📝 Usage

1. Configure your project settings in the sidebar
2. Set advanced parameters if needed
3. Click "Generate Content"
4. Monitor the generation progress
5. Download the result in PDF or Markdown format

## 🧩 System Architecture

The application uses a two-agent system:
- **Research Agent**: Gathers and analyzes information
- **Writing Agent**: Transforms research into polished content

Both agents work together through CrewAI's orchestration to produce comprehensive, well-researched content.

## 🔐 Security

- API keys are stored securely in session state
- Temporary files are automatically cleaned up
- No data persistence between sessions

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [CrewAI](https://github.com/joaomdmoura/crewAI)
- Powered by Google's Gemini LLM
- Frontend developed with Streamlit

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For support or queries, please open an issue in the repository.

---
Developed with ❤️ by Akhil
