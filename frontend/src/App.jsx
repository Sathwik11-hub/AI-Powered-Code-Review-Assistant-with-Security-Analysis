import { useState, useRef, useEffect } from 'react';
import CodeEditor from './components/Editor';
import Sidebar from './components/Sidebar';
import ResultsPanel from './components/ResultsPanel';
import './index.css';

const DEFAULT_CODE = `# Python example - try the code review!
def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total = total + num
    return total

# Security issue: eval() is dangerous
user_input = input("Enter expression: ")
result = eval(user_input)
print(result)
`;

function App() {
  const [code, setCode] = useState(DEFAULT_CODE);
  const [language, setLanguage] = useState('python');
  const [diagnostics, setDiagnostics] = useState([]);
  const [isReviewing, setIsReviewing] = useState(false);
  const [theme, setTheme] = useState('light');
  const [preferences, setPreferences] = useState({
    selectedLanguages: ['javascript', 'python'],
    enableSecurity: true,
    enableLLM: false,
    runOnSave: false,
  });

  const editorRef = useRef(null);

  // Apply theme to document
  useEffect(() => {
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [theme]);

  const handleRunReview = async () => {
    setIsReviewing(true);
    setDiagnostics([]);

    // Clear existing diagnostics
    if (editorRef.current) {
      editorRef.current.clearDiagnostics();
    }

    try {
      const response = await fetch('/api/review', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          filePath: 'untitled.' + (language === 'javascript' ? 'js' : language === 'python' ? 'py' : 'txt'),
          language,
          code,
          preferences,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setDiagnostics(data.diagnostics || []);

      // Apply diagnostics to editor
      if (editorRef.current && data.diagnostics) {
        editorRef.current.applyDiagnostics(data.diagnostics);
      }
    } catch (error) {
      console.error('Error running review:', error);
      setDiagnostics([
        {
          severity: 'error',
          message: `Failed to connect to backend: ${error.message}. Make sure the backend server is running on port 8000.`,
          line: 1,
          column: 1,
          ruleId: 'connection-error',
        },
      ]);
    } finally {
      setIsReviewing(false);
    }
  };

  const handleApplyFix = (diagnostic) => {
    if (!diagnostic.fix) return;

    // Simple fix application - in production, this would be more sophisticated
    const lines = code.split('\n');
    if (diagnostic.line > 0 && diagnostic.line <= lines.length) {
      lines[diagnostic.line - 1] = diagnostic.fix;
      setCode(lines.join('\n'));
    }
  };

  const handleJumpToLine = (line) => {
    // Monaco editor will handle the jump
    console.log(`Jumping to line ${line}`);
  };

  const handleThemeToggle = () => {
    setTheme(theme === 'dark' ? 'light' : 'dark');
  };

  return (
    <div className="flex h-screen bg-gray-100 dark:bg-gray-900">
      {/* Sidebar - 20% */}
      <div className="w-1/5 min-w-[250px]">
        <Sidebar
          preferences={preferences}
          onPreferencesChange={setPreferences}
          onRunReview={handleRunReview}
          theme={theme}
          onThemeToggle={handleThemeToggle}
          isReviewing={isReviewing}
        />
      </div>

      {/* Editor - 50% */}
      <div className="flex-1 flex flex-col">
        {/* Language Selector */}
        <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 p-2 flex items-center gap-2">
          <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
            Language:
          </label>
          <select
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            className="px-3 py-1 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm"
          >
            <option value="javascript">JavaScript</option>
            <option value="typescript">TypeScript</option>
            <option value="python">Python</option>
            <option value="java">Java</option>
            <option value="go">Go</option>
          </select>
          
          {isReviewing && (
            <span className="ml-4 text-sm text-blue-600 dark:text-blue-400 animate-pulse">
              Analyzing...
            </span>
          )}
        </div>

        {/* Editor */}
        <div className="flex-1 bg-white dark:bg-gray-800">
          <CodeEditor
            ref={editorRef}
            language={language}
            value={code}
            onChange={(value) => setCode(value || '')}
            theme={theme}
          />
        </div>
      </div>

      {/* Results Panel - 30% */}
      <div className="w-[30%] min-w-[300px]">
        <ResultsPanel
          diagnostics={diagnostics}
          onApplyFix={handleApplyFix}
          onJumpToLine={handleJumpToLine}
        />
      </div>
    </div>
  );
}

export default App;
