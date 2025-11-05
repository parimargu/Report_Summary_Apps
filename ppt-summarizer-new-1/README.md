# 📊 PowerPoint Content Summarization Application

An AI-powered Streamlit application that extracts and summarizes financial data from PowerPoint presentations using Groq LLM.

## 🎯 Features

- **📤 File Upload**: Support for .ppt and .pptx files (up to 5MB)
- **📝 Content Extraction**: Automatic extraction of text and tables from slides
- **🤖 AI Summaries**: Generate intelligent summaries of table data using Groq LLM
- **🎨 Responsive UI**: Clean, two-panel layout with slide navigation
- **🔍 Financial Focus**: Specialized analysis of Loan Default Rate and Net Rate metrics
- **⚡ Production Ready**: Modular architecture with comprehensive error handling

## 🏗️ Architecture

```
ppt-summarizer/
├── app.py                      # Main Streamlit application
├── config.yaml                 # Configuration file
├── prompt_template.txt         # LLM prompt template
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (create from .env.example)
├── modules/
│   ├── config_manager.py      # Configuration loader
│   ├── file_parser.py         # PowerPoint parsing
│   ├── content_extractor.py   # Content extraction
│   ├── llm_service.py         # Groq LLM integration
│   ├── ui_renderer.py         # Streamlit UI components
│   └── logger.py              # Logging configuration
├── tests/                      # Unit tests
└── sample_data/               # Sample presentations
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Groq API key ([Get one here](https://console.groq.com))

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ppt-summarizer
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your GROQ_API_KEY
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Access the app**
   Open your browser to `http://localhost:8501`

## 📖 Usage

### 1. Upload a Presentation

- Click "Browse files" or drag-and-drop a .pptx file
- Supported formats: .ppt, .pptx
- Maximum file size: 5MB

### 2. Navigate Slides

- Use the slide selector dropdown
- Click Previous/Next buttons
- View text content in the left panel
- View tables in the right panel

### 3. Generate Summaries

- Click "🤖 Generate AI Summary" under any table
- Wait for the AI to analyze the data
- View the summary below the table
- Summaries highlight:
  - Key metrics and trends
  - Risk indicators
  - Negative values
  - Abnormal patterns

## ⚙️ Configuration

### config.yaml

Main configuration file containing:

```yaml
app:
  name: "PowerPoint Content Summarization"
  max_file_size_mb: 5
  supported_formats: [".ppt", ".pptx"]

llm:
  model_name: "llama-3.1-70b-versatile"
  temperature: 0.3
  max_tokens: 1024
  max_retries: 3

logging:
  level: "INFO"
  file: "app.log"
```

### Environment Variables

Create a `.env` file with:

```bash
GROQ_API_KEY=your_api_key_here
```

Optional overrides:
```bash
LLM_MODEL_NAME=llama-3.1-70b-versatile
LLM_TEMPERATURE=0.3
LOG_LEVEL=INFO
```

## 🧪 Testing

### Run All Tests

```bash
pytest tests/ -v
```

### Run with Coverage

```bash
pytest tests/ -v --cov=modules --cov-report=html
```

### Run Specific Test File

```bash
pytest tests/test_file_parser.py -v
```

## 📊 Prompt Engineering

The application uses a sophisticated prompt template (`prompt_template.txt`) that includes:

- **Role-based prompting**: Financial analyst persona
- **Few-shot examples**: Sample analyses demonstrating desired output
- **Clear instructions**: Specific focus on key metrics
- **Structured output**: Bullet-point format for readability

### Customizing the Prompt

Edit `prompt_template.txt` to customize:
- Analysis focus areas
- Output format
- Example demonstrations
- Risk indicators

## 🔧 Development

### Module Structure

- **config_manager.py**: Loads and manages configuration
- **file_parser.py**: Validates and parses PowerPoint files
- **content_extractor.py**: Extracts text and tables from slides
- **llm_service.py**: Interfaces with Groq API
- **ui_renderer.py**: Renders Streamlit UI components
- **logger.py**: Centralized logging setup

### Adding New Features

1. Create feature module in `modules/`
2. Add tests in `tests/`
3. Update configuration in `config.yaml`
4. Document in README

### Code Quality

```bash
# Format code
black modules/ tests/ app.py

# Lint code
flake8 modules/ tests/ app.py

# Type checking
mypy modules/
```

## 📝 Logging

Logs are written to both console and `app.log`:

- **DEBUG**: Detailed diagnostic information
- **INFO**: General informational messages
- **WARNING**: Warning messages
- **ERROR**: Error messages
- **CRITICAL**: Critical errors

View logs:
```bash
tail -f app.log
```

## 🔒 Security

- API keys are stored in environment variables
- No secrets in code or configuration files
- File size limits prevent DoS attacks
- Input validation on all uploaded files

## 🐛 Troubleshooting

### API Key Not Found

```
Error: GROQ_API_KEY must be set
```

**Solution**: Create `.env` file with your Groq API key

### File Upload Fails

```
Error: File size exceeds maximum
```

**Solution**: Compress presentation or reduce image quality

### Summary Generation Timeout

```
Error: API timeout
```

**Solution**: Check internet connection, API will automatically retry

### Module Import Errors

```
ModuleNotFoundError: No module named 'groq'
```

**Solution**: Run `pip install -r requirements.txt`

## 📈 Performance

- **File Processing**: < 5 seconds for typical presentations
- **Summary Generation**: 5-10 seconds per table
- **Concurrent Requests**: Supports async operations
- **Memory Usage**: Efficient streaming for large files

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 👥 Support

For issues, questions, or contributions:
- Create an issue on GitHub
- Contact the development team
- Check documentation in `docs/`

## 🙏 Acknowledgments

- **Groq**: For providing the LLM API
- **Streamlit**: For the web application framework
- **python-pptx**: For PowerPoint parsing capabilities

## 📚 Additional Resources

- [Groq Documentation](https://console.groq.com/docs)
- [Streamlit Documentation](https://docs.streamlit.io)
- [python-pptx Documentation](https://python-pptx.readthedocs.io)

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Status**: Production Ready ✅
