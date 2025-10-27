import { AlertCircle, CheckCircle, AlertTriangle, Info, Copy, Eye, Lightbulb } from 'lucide-react';

const SEVERITY_CONFIG = {
  error: {
    icon: AlertCircle,
    bgColor: 'bg-red-100 dark:bg-red-900/20',
    textColor: 'text-red-800 dark:text-red-300',
    badgeColor: 'bg-red-500 text-white',
    borderColor: 'border-red-300 dark:border-red-700',
    label: 'Error',
  },
  warning: {
    icon: AlertTriangle,
    bgColor: 'bg-yellow-100 dark:bg-yellow-900/20',
    textColor: 'text-yellow-800 dark:text-yellow-300',
    badgeColor: 'bg-yellow-500 text-white',
    borderColor: 'border-yellow-300 dark:border-yellow-700',
    label: 'Warning',
  },
  suggestion: {
    icon: Lightbulb,
    bgColor: 'bg-green-100 dark:bg-green-900/20',
    textColor: 'text-green-800 dark:text-green-300',
    badgeColor: 'bg-green-500 text-white',
    borderColor: 'border-green-300 dark:border-green-700',
    label: 'Suggestion',
  },
  info: {
    icon: Info,
    bgColor: 'bg-blue-100 dark:bg-blue-900/20',
    textColor: 'text-blue-800 dark:text-blue-300',
    badgeColor: 'bg-blue-500 text-white',
    borderColor: 'border-blue-300 dark:border-blue-700',
    label: 'Info',
  },
};

function ResultsPanel({ diagnostics, onApplyFix, onJumpToLine }) {
  const handleCopyMessage = (message) => {
    navigator.clipboard.writeText(message);
  };

  const getSeverityConfig = (severity) => {
    return SEVERITY_CONFIG[severity] || SEVERITY_CONFIG.info;
  };

  const groupedDiagnostics = diagnostics.reduce((acc, diagnostic) => {
    const key = diagnostic.severity;
    if (!acc[key]) acc[key] = [];
    acc[key].push(diagnostic);
    return acc;
  }, {});

  const summary = {
    error: groupedDiagnostics.error?.length || 0,
    warning: groupedDiagnostics.warning?.length || 0,
    suggestion: groupedDiagnostics.suggestion?.length || 0,
    info: groupedDiagnostics.info?.length || 0,
  };

  return (
    <div className="h-full bg-white dark:bg-gray-900 border-l border-gray-200 dark:border-gray-700 flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-gray-200 dark:border-gray-700">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
          Review Results
        </h2>
        
        {/* Summary */}
        <div className="flex flex-wrap gap-2">
          {summary.error > 0 && (
            <span className="px-2 py-1 text-xs font-medium bg-red-100 dark:bg-red-900/20 text-red-800 dark:text-red-300 rounded">
              {summary.error} Error{summary.error > 1 ? 's' : ''}
            </span>
          )}
          {summary.warning > 0 && (
            <span className="px-2 py-1 text-xs font-medium bg-yellow-100 dark:bg-yellow-900/20 text-yellow-800 dark:text-yellow-300 rounded">
              {summary.warning} Warning{summary.warning > 1 ? 's' : ''}
            </span>
          )}
          {summary.suggestion > 0 && (
            <span className="px-2 py-1 text-xs font-medium bg-green-100 dark:bg-green-900/20 text-green-800 dark:text-green-300 rounded">
              {summary.suggestion} Suggestion{summary.suggestion > 1 ? 's' : ''}
            </span>
          )}
          {summary.info > 0 && (
            <span className="px-2 py-1 text-xs font-medium bg-blue-100 dark:bg-blue-900/20 text-blue-800 dark:text-blue-300 rounded">
              {summary.info} Info
            </span>
          )}
        </div>
      </div>

      {/* Results List */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {diagnostics.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-gray-500 dark:text-gray-400">
            <CheckCircle className="w-16 h-16 mb-4 text-green-500" />
            <p className="text-lg font-medium">No issues found!</p>
            <p className="text-sm mt-2">Your code looks great.</p>
          </div>
        ) : (
          diagnostics.map((diagnostic, index) => {
            const config = getSeverityConfig(diagnostic.severity);
            const Icon = config.icon;

            return (
              <div
                key={index}
                className={`border ${config.borderColor} ${config.bgColor} rounded-lg p-4 transition-all hover:shadow-md`}
              >
                {/* Header */}
                <div className="flex items-start justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <Icon className={`w-5 h-5 ${config.textColor}`} />
                    <span className={`px-2 py-0.5 text-xs font-bold ${config.badgeColor} rounded`}>
                      {config.label}
                    </span>
                  </div>
                  <div className="text-xs text-gray-500 dark:text-gray-400">
                    Line {diagnostic.line}
                    {diagnostic.column && `, Col ${diagnostic.column}`}
                  </div>
                </div>

                {/* Message */}
                <p className={`text-sm ${config.textColor} font-medium mb-2`}>
                  {diagnostic.message}
                </p>

                {/* Rule ID */}
                {diagnostic.ruleId && (
                  <p className="text-xs text-gray-600 dark:text-gray-400 mb-2">
                    Rule: <code className="bg-gray-200 dark:bg-gray-700 px-1 py-0.5 rounded">{diagnostic.ruleId}</code>
                  </p>
                )}

                {/* Confidence */}
                {diagnostic.confidence && (
                  <p className="text-xs text-gray-600 dark:text-gray-400 mb-2">
                    Confidence: <span className="font-medium">{diagnostic.confidence}</span>
                  </p>
                )}

                {/* Actions */}
                <div className="flex gap-2 mt-3">
                  <button
                    onClick={() => onJumpToLine(diagnostic.line)}
                    className="flex items-center gap-1 px-3 py-1 text-xs bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 rounded transition-colors"
                    aria-label={`Jump to line ${diagnostic.line}`}
                  >
                    <Eye className="w-3 h-3" />
                    View
                  </button>
                  
                  {diagnostic.fix && (
                    <button
                      onClick={() => onApplyFix(diagnostic)}
                      className="flex items-center gap-1 px-3 py-1 text-xs bg-green-600 hover:bg-green-700 text-white rounded transition-colors"
                      aria-label="Apply suggested fix"
                    >
                      <CheckCircle className="w-3 h-3" />
                      Apply Fix
                    </button>
                  )}
                  
                  <button
                    onClick={() => handleCopyMessage(diagnostic.message)}
                    className="flex items-center gap-1 px-3 py-1 text-xs bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 rounded transition-colors"
                    aria-label="Copy message"
                  >
                    <Copy className="w-3 h-3" />
                    Copy
                  </button>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}

export default ResultsPanel;
