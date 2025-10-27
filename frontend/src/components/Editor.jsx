import { useRef, useEffect, forwardRef, useImperativeHandle } from 'react';
import Editor from '@monaco-editor/react';

/**
 * Monaco Editor component with diagnostic markers support
 * 
 * Diagnostics format:
 * {
 *   severity: 'error' | 'warning' | 'suggestion' | 'info',
 *   message: string,
 *   line: number,
 *   column: number,
 *   ruleId: string,
 *   fix?: string
 * }
 * 
 * Red markers: errors and security issues
 * Green markers: suggestions and improvements
 */
const CodeEditor = forwardRef(({ language, value, onChange, theme }, ref) => {
  const editorRef = useRef(null);
  const monacoRef = useRef(null);
  const decorationsRef = useRef([]);

  useImperativeHandle(ref, () => ({
    applyDiagnostics: (diagnostics) => {
      if (!monacoRef.current || !editorRef.current) return;

      const monaco = monacoRef.current;
      const editor = editorRef.current;
      const model = editor.getModel();
      
      if (!model) return;

      // Convert diagnostics to Monaco markers
      const markers = diagnostics.map(diagnostic => {
        let severity;
        switch (diagnostic.severity) {
          case 'error':
            severity = monaco.MarkerSeverity.Error;
            break;
          case 'warning':
            severity = monaco.MarkerSeverity.Warning;
            break;
          case 'suggestion':
          case 'info':
            severity = monaco.MarkerSeverity.Info;
            break;
          default:
            severity = monaco.MarkerSeverity.Info;
        }

        return {
          severity,
          message: diagnostic.message,
          startLineNumber: diagnostic.line,
          startColumn: diagnostic.column || 1,
          endLineNumber: diagnostic.line,
          endColumn: (diagnostic.column || 1) + 1,
          source: diagnostic.ruleId || 'code-review',
        };
      });

      // Set markers on the model
      monaco.editor.setModelMarkers(model, 'code-review-assistant', markers);

      // Create decorations for visual indicators
      const newDecorations = diagnostics.map(diagnostic => {
        const isError = diagnostic.severity === 'error';
        const isSuggestion = diagnostic.severity === 'suggestion' || diagnostic.severity === 'info';

        return {
          range: new monaco.Range(
            diagnostic.line,
            diagnostic.column || 1,
            diagnostic.line,
            (diagnostic.column || 1) + 10
          ),
          options: {
            isWholeLine: false,
            className: isError ? 'error-line-decoration' : 'suggestion-line-decoration',
            glyphMarginClassName: isError ? 'error-glyph' : 'suggestion-glyph',
            glyphMarginHoverMessage: { value: diagnostic.message },
            hoverMessage: { 
              value: `**${diagnostic.ruleId || 'Review'}**: ${diagnostic.message}${
                diagnostic.fix ? `\n\n💡 Suggested fix available` : ''
              }` 
            },
            minimap: {
              color: isError ? '#ff0000' : '#00ff00',
              position: monaco.editor.MinimapPosition.Inline,
            },
          },
        };
      });

      // Apply decorations
      decorationsRef.current = editor.deltaDecorations(decorationsRef.current, newDecorations);
    },
    
    clearDiagnostics: () => {
      if (!monacoRef.current || !editorRef.current) return;
      
      const monaco = monacoRef.current;
      const editor = editorRef.current;
      const model = editor.getModel();
      
      if (model) {
        monaco.editor.setModelMarkers(model, 'code-review-assistant', []);
        decorationsRef.current = editor.deltaDecorations(decorationsRef.current, []);
      }
    },
  }));

  const handleEditorDidMount = (editor, monaco) => {
    editorRef.current = editor;
    monacoRef.current = monaco;

    // Define custom CSS for decorations
    const style = document.createElement('style');
    style.innerHTML = `
      .error-line-decoration {
        background-color: rgba(255, 0, 0, 0.1);
        border-bottom: 2px wavy red;
      }
      .suggestion-line-decoration {
        background-color: rgba(0, 255, 0, 0.05);
        border-bottom: 1px dashed green;
      }
      .error-glyph {
        background: red;
        width: 5px !important;
        margin-left: 3px;
      }
      .suggestion-glyph {
        background: green;
        width: 5px !important;
        margin-left: 3px;
      }
    `;
    document.head.appendChild(style);

    // Configure editor options
    editor.updateOptions({
      minimap: { enabled: true },
      scrollBeyondLastLine: false,
      fontSize: 14,
      lineNumbers: 'on',
      renderWhitespace: 'selection',
      automaticLayout: true,
      tabSize: 2,
      insertSpaces: true,
    });
  };

  return (
    <Editor
      height="100%"
      language={language}
      value={value}
      onChange={onChange}
      theme={theme === 'dark' ? 'vs-dark' : 'vs-light'}
      onMount={handleEditorDidMount}
      options={{
        selectOnLineNumbers: true,
        roundedSelection: false,
        readOnly: false,
        cursorStyle: 'line',
        automaticLayout: true,
      }}
    />
  );
});

CodeEditor.displayName = 'CodeEditor';

export default CodeEditor;
