# Content Generation Agent 📝

![image](https://github.com/user-attachments/assets/190717c6-dc0f-48f4-8d41-984ce02afeed)

A powerful AI-powered content generation platform built with CrewAI and Gemini, featuring automated research and professional writing capabilities.

## 🌟 Features

- **AI-Powered Content Creation**: Utilizes multiple AI agents for research and writing
- **Multiple Content Types**: Support for blog posts, articles, research papers, and technical guides
- **Audience Targeting**: Customizable content for different audience types
- **Professional Formatting**: Automatic PDF and Markdown export options
- **User-Friendly Interface**: Clean and intuitive Streamlit-based UI
- **Advanced Controls**: Adjustable creativity levels and word count limits

## 📸 Screenshots

### Main Interface
![image](https://github.com/user-attachments/assets/f0e8ce96-254b-49a8-bd24-446b5ee02190)
*The main dashboard with content configuration options*

### Content Generation Process
![image](https://github.com/user-attachments/assets/a9f5a913-988b-4107-b5ac-93f9a4a4bfcd)
*Real-time progress tracking during content generation*

### Generated Content
![image](https://github.com/user-attachments/assets/b1cdb553-03b5-45da-bddd-081b16f07db8)

![image](https://github.com/user-attachments/assets/1cf7d81f-7294-4af2-8a3f-ff84abf1c64d)
*Example of generated content with download options*

### Dowloaded PDF
![image](https://github.com/user-attachments/assets/d3c58390-7b4c-4534-a3f4-0781df7b5145)


## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Gemini API key
- Serper API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/kakarlapudiakhilvarma1/Content-Generation-Agent.git
cd content-generation-agent
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
   - Create a `.env` file in the root directory
   - Add your API keys:
```env
GEMINI_API_KEY=your_gemini_api_key_here
SERPER_API_KEY=your_serper_api_key_here
```

4. Run the application:
```bash
streamlit run src/main.py  #Make sure you are in 'src' directory
```

## 🏗 Project Structure

```plaintext
content-generation-agent/
├── .env
├── requirements.txt
└── src/
    ├── __init__.py
    ├── main.py
    ├── utils/
    │   ├── __init__.py
    │   ├── pdf_generator.py
    │   └── api_checker.py
    └── agents/
        ├── __init__.py
        └── content_crew.py
```

## 💻 Usage

1. Launch the application
2. Enter your Gemini API key if not already configured
3. Configure your content settings:
   - Enter the topic
   - Select content type
   - Choose target audience
   - Adjust advanced settings if needed
4. Click "Generate Content"
5. Wait for the AI agents to complete their tasks
6. Download your content in PDF or Markdown format

## ⚙️ Configuration Options

| Setting | Description | Options |
|---------|-------------|----------|
| Content Type | Type of content to generate | Blog Post, Article, Research Paper, Technical Guide |
| Target Audience | Intended audience | General, Technical, Business, Academic |
| Creativity Level | AI creativity setting | 0.0 - 1.0 |
| Word Count | Content length | 500 - 5000 words |

## 🤖 AI Agents

### Research Analyst Agent
- Conducts comprehensive topic research
- Gathers relevant statistics and data
- Verifies sources and citations

### Content Writer Agent
- Creates engaging content
- Maintains professional tone
- Ensures proper formatting
- Incorporates research findings

## 📄 Generated Content Features

- Professional formatting
- Proper citations
- Source references
- Executive summaries
- Key insights
- Verified statistics

## 🛠 Technical Details

- **Frontend**: Streamlit
- **AI Framework**: CrewAI
- **Language Model**: Gemini
- **PDF Generation**: FPDF
- **Search Tool**: SerperDev

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Akhil** - [GitHub Profile](https://github.com/kakarlapudiakhilvarma1)

## 🙏 Acknowledgments

- CrewAI for the AI agent framework
- Google for the Gemini API
- Streamlit for the wonderful UI framework
- All contributors and supporters

## 📞 Support

For support, email kakarlapudiakhilvarma1@gmail.com or open an issue in the GitHub repository.
