# AI-Powered Code Review Assistant with Security Analysis

A near-IDE experience for code review with integrated security scanning, linting, and AI-powered suggestions. Features a React frontend with Monaco Editor and a FastAPI backend running language-specific analyzers.

## Features

- 🎨 **Monaco Editor Integration**: Professional code editing experience with syntax highlighting
- 🔍 **Multi-Language Support**: JavaScript, TypeScript, Python, Java, Go
- 🛡️ **Security Scanning**: Integrated Semgrep, Bandit, npm audit, and safety checks
- 🤖 **AI-Powered Suggestions**: LLM-based code review and fix recommendations
- 📊 **Visual Diagnostics**: Red markers for errors, green markers for suggestions
- 🌲 **File Explorer**: Navigate project files like an IDE
- ⚡ **Real-time Analysis**: Run checks on save or on-demand
- ♿ **Accessible UI**: Keyboard navigation, ARIA labels, theme toggle

## Tech Stack

### Frontend
- **React** + **Vite**: Fast, modern React development
- **Tailwind CSS**: Utility-first styling
- **Monaco Editor**: VSCode's editor component
- **React Router**: Navigation

### Backend
- **FastAPI**: High-performance Python API framework
- **Uvicorn**: ASGI server
- **Language Tools**:
  - Python: flake8, bandit, pylint
  - JavaScript: ESLint, eslint-plugin-security
- **Security Scanners**:
  - Semgrep: Multi-language SAST
  - Bandit: Python security analysis
  - npm audit: JavaScript dependency scanning
  - safety: Python dependency scanning

### AI/LLM
- OpenAI API (optional): Code explanations and fix suggestions
- RAG support (optional): Context-aware recommendations

## Setup

### Prerequisites
- Node.js 18+ and npm
- Python 3.9+
- (Optional) OpenAI API key for LLM features

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will start on `http://localhost:5173`

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

The backend API will be available at `http://localhost:8000`

### Environment Variables

Create a `.env` file in the backend directory:

```env
OPENAI_API_KEY=your_api_key_here  # Optional, for LLM features
SEMGREP_RULES_PATH=./rules        # Optional, custom Semgrep rules
LOG_LEVEL=INFO
```

## Usage

1. **Start both servers** (frontend and backend)
2. **Open the app** in your browser at `http://localhost:5173`
3. **Select language** from the sidebar
4. **Write or paste code** in the editor
5. **Run analysis** by clicking "Review Code" or enable "Run on save"
6. **View results** in the right panel:
   - Red badges = Errors and security issues
   - Green badges = Suggestions and improvements
7. **Apply fixes** by clicking "Apply Fix" on suggestions

## API Endpoints

### POST /api/review
Analyze code and return diagnostics.

**Request:**
```json
{
  "filePath": "example.py",
  "language": "python",
  "code": "print('Hello')",
  "preferences": {
    "enableSecurity": true,
    "enableLLM": false,
    "selectedLanguages": ["python"]
  }
}
```

**Response:**
```json
{
  "diagnostics": [
    {
      "severity": "error",
      "message": "Line too long (90 > 79 characters)",
      "line": 5,
      "column": 80,
      "ruleId": "E501",
      "fix": null
    },
    {
      "severity": "suggestion",
      "message": "Consider using f-strings for formatting",
      "line": 3,
      "column": 10,
      "ruleId": "F521",
      "fix": "name = f'Hello {user}'"
    }
  ]
}
```

### POST /api/scan-security
Run security-specific scans.

**Request:**
```json
{
  "filePath": "app.js",
  "language": "javascript",
  "code": "eval(userInput)"
}
```

**Response:**
```json
{
  "findings": [
    {
      "severity": "error",
      "message": "Dangerous use of eval() with user input",
      "line": 1,
      "column": 1,
      "ruleId": "security/detect-eval-with-expression",
      "confidence": "high"
    }
  ],
  "summary": {
    "critical": 1,
    "high": 0,
    "medium": 0,
    "low": 0
  }
}
```

### GET /api/status
Health check endpoint.

## Development

### Running Tests

**Frontend:**
```bash
cd frontend
npm test
```

**Backend:**
```bash
cd backend
pytest
```

### Linting

**Frontend:**
```bash
cd frontend
npm run lint
npm run format
```

**Backend:**
```bash
cd backend
flake8 .
black .
```

### Quality Checks

Run all checks before committing:
```bash
cd frontend && npm run check
cd ../backend && pytest && flake8 .
```

## CI/CD

GitHub Actions automatically run on pull requests:
- Linting (ESLint, flake8)
- Tests (Jest, pytest)
- Security scans (Semgrep, Bandit, npm audit)
- Build verification

See `.github/workflows/ci.yml` for details.

## Security Considerations

⚠️ **Important Security Notes:**

1. **Sandboxing**: All code analysis runs in isolated subprocess with timeouts
2. **No Code Execution**: Backend only performs static analysis, no dynamic execution
3. **Privacy**: Code submitted for review is not stored permanently
4. **API Keys**: Keep your OpenAI API key secure in environment variables
5. **Dependencies**: Regularly update dependencies and run security scans

## Color Semantics

- 🔴 **Red**: Errors, security vulnerabilities, failing checks
- 🟢 **Green**: Suggestions, improvements, auto-fixable items
- 🟡 **Yellow**: Warnings
- 🔵 **Blue**: Informational

Colors are always paired with text labels and icons for accessibility.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - See LICENSE file for details.

## Roadmap

- [ ] Support for more languages (C++, Rust, Ruby)
- [ ] Advanced RAG with codebase indexing
- [ ] Collaborative review sessions
- [ ] Custom rule configuration UI
- [ ] Integration with GitHub/GitLab APIs
- [ ] Docker containerization
- [ ] VSCode extension

## Support

For issues, questions, or contributions, please open an issue on GitHub.