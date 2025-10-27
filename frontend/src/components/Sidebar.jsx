import { useState } from 'react';
import { FolderTree, Settings, Sun, Moon, Play, Save } from 'lucide-react';

const LANGUAGES = [
  { id: 'javascript', label: 'JavaScript', ext: '.js' },
  { id: 'typescript', label: 'TypeScript', ext: '.ts' },
  { id: 'python', label: 'Python', ext: '.py' },
  { id: 'java', label: 'Java', ext: '.java' },
  { id: 'go', label: 'Go', ext: '.go' },
];

const SAMPLE_FILES = [
  { name: 'src', type: 'folder', children: [
    { name: 'index.js', type: 'file', language: 'javascript' },
    { name: 'utils.py', type: 'file', language: 'python' },
    { name: 'App.jsx', type: 'file', language: 'javascript' },
  ]},
  { name: 'tests', type: 'folder', children: [
    { name: 'test_utils.py', type: 'file', language: 'python' },
  ]},
  { name: 'README.md', type: 'file', language: 'markdown' },
];

function Sidebar({ preferences, onPreferencesChange, onRunReview, theme, onThemeToggle, isReviewing }) {
  const [showSettings, setShowSettings] = useState(false);

  const handleLanguageToggle = (langId) => {
    const newLanguages = preferences.selectedLanguages.includes(langId)
      ? preferences.selectedLanguages.filter(id => id !== langId)
      : [...preferences.selectedLanguages, langId];
    
    onPreferencesChange({ ...preferences, selectedLanguages: newLanguages });
  };

  const handleToggle = (key) => {
    onPreferencesChange({ ...preferences, [key]: !preferences[key] });
  };

  const FileTreeItem = ({ item, depth = 0 }) => (
    <div style={{ marginLeft: `${depth * 12}px` }} className="py-1">
      <div className="flex items-center gap-2 px-2 py-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer">
        {item.type === 'folder' ? (
          <>
            <FolderTree className="w-4 h-4 text-blue-500" />
            <span className="text-sm">{item.name}</span>
          </>
        ) : (
          <>
            <div className="w-4 h-4 flex items-center justify-center text-xs text-gray-500">📄</div>
            <span className="text-sm">{item.name}</span>
          </>
        )}
      </div>
      {item.children && item.children.map((child, idx) => (
        <FileTreeItem key={idx} item={child} depth={depth + 1} />
      ))}
    </div>
  );

  return (
    <div className="h-full bg-gray-50 dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white">AI Code Review</h2>
        <div className="flex gap-2">
          <button
            onClick={onThemeToggle}
            className="p-2 hover:bg-gray-200 dark:hover:bg-gray-600 rounded"
            aria-label="Toggle theme"
          >
            {theme === 'dark' ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
          </button>
          <button
            onClick={() => setShowSettings(!showSettings)}
            className="p-2 hover:bg-gray-200 dark:hover:bg-gray-600 rounded"
            aria-label="Settings"
          >
            <Settings className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Actions */}
      <div className="p-4 border-b border-gray-200 dark:border-gray-700 space-y-2">
        <button
          onClick={onRunReview}
          disabled={isReviewing}
          className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          aria-label="Run code review"
        >
          <Play className="w-4 h-4" />
          {isReviewing ? 'Reviewing...' : 'Run Review'}
        </button>
      </div>

      {/* Settings Panel */}
      {showSettings && (
        <div className="p-4 border-b border-gray-200 dark:border-gray-700 space-y-4">
          <div>
            <h3 className="text-sm font-semibold mb-2 text-gray-900 dark:text-white">Languages</h3>
            <div className="space-y-2">
              {LANGUAGES.map(lang => (
                <label key={lang.id} className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={preferences.selectedLanguages.includes(lang.id)}
                    onChange={() => handleLanguageToggle(lang.id)}
                    className="rounded"
                  />
                  <span className="text-sm text-gray-700 dark:text-gray-300">{lang.label}</span>
                </label>
              ))}
            </div>
          </div>

          <div>
            <h3 className="text-sm font-semibold mb-2 text-gray-900 dark:text-white">Features</h3>
            <div className="space-y-2">
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={preferences.enableSecurity}
                  onChange={() => handleToggle('enableSecurity')}
                  className="rounded"
                />
                <span className="text-sm text-gray-700 dark:text-gray-300">Security Scan</span>
              </label>
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={preferences.enableLLM}
                  onChange={() => handleToggle('enableLLM')}
                  className="rounded"
                />
                <span className="text-sm text-gray-700 dark:text-gray-300">LLM Suggestions</span>
              </label>
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={preferences.runOnSave}
                  onChange={() => handleToggle('runOnSave')}
                  className="rounded"
                />
                <span className="text-sm text-gray-700 dark:text-gray-300">Run on Save</span>
              </label>
            </div>
          </div>
        </div>
      )}

      {/* File Explorer */}
      <div className="flex-1 overflow-y-auto p-4">
        <h3 className="text-sm font-semibold mb-2 text-gray-900 dark:text-white flex items-center gap-2">
          <FolderTree className="w-4 h-4" />
          Files
        </h3>
        <div className="text-gray-700 dark:text-gray-300">
          {SAMPLE_FILES.map((item, idx) => (
            <FileTreeItem key={idx} item={item} />
          ))}
        </div>
      </div>
    </div>
  );
}

export default Sidebar;
