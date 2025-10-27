"""
JavaScript/TypeScript code reviewer
"""
import subprocess
import tempfile
import os
import re
from typing import List, Dict, Any

def run_js_review(code: str, enable_security: bool = True) -> List[Dict[str, Any]]:
    """
    Run JavaScript/TypeScript code review
    
    Returns list of diagnostics
    """
    diagnostics = []
    
    # Pattern-based checks (fallback when eslint not available)
    diagnostics.extend(_check_dangerous_js_patterns(code))
    
    # Try to run eslint if available
    diagnostics.extend(_run_eslint(code))
    
    return diagnostics

def _check_dangerous_js_patterns(code: str) -> List[Dict[str, Any]]:
    """
    Check for dangerous JavaScript patterns using regex
    """
    diagnostics = []
    lines = code.split('\n')
    
    for line_num, line in enumerate(lines, start=1):
        # Check for eval()
        if re.search(r'\beval\s*\(', line):
            diagnostics.append({
                "severity": "error",
                "message": "Use of eval() is dangerous and should be avoided",
                "line": line_num,
                "column": line.index('eval') + 1 if 'eval' in line else 1,
                "ruleId": "security/detect-eval-with-expression",
                "confidence": "high"
            })
        
        # Check for innerHTML (XSS risk)
        if re.search(r'\.innerHTML\s*=', line):
            diagnostics.append({
                "severity": "warning",
                "message": "Direct use of innerHTML can lead to XSS vulnerabilities. Consider using textContent or sanitization.",
                "line": line_num,
                "column": line.index('innerHTML') + 1 if 'innerHTML' in line else 1,
                "ruleId": "security/detect-unsafe-innerHTML",
                "confidence": "medium"
            })
        
        # Check for == instead of ===
        if re.search(r'[^=!<>]==[^=]', line):
            col = re.search(r'[^=!<>]==[^=]', line).start() + 1
            diagnostics.append({
                "severity": "suggestion",
                "message": "Use === instead of == for type-safe comparison",
                "line": line_num,
                "column": col,
                "ruleId": "eqeqeq",
                "fix": line.replace('==', '===', 1)
            })
        
        # Check for var usage (prefer let/const)
        if re.search(r'\bvar\s+', line):
            diagnostics.append({
                "severity": "suggestion",
                "message": "Use 'let' or 'const' instead of 'var'",
                "line": line_num,
                "column": line.index('var') + 1 if 'var' in line else 1,
                "ruleId": "no-var",
            })
        
        # Check for console.log (should be removed in production)
        if re.search(r'\bconsole\.log\s*\(', line):
            diagnostics.append({
                "severity": "info",
                "message": "Remove console.log statements before production",
                "line": line_num,
                "column": line.index('console') + 1 if 'console' in line else 1,
                "ruleId": "no-console",
            })
    
    return diagnostics

def _run_eslint(code: str) -> List[Dict[str, Any]]:
    """
    Run ESLint on JavaScript code
    """
    diagnostics = []
    
    try:
        # Create temporary directory with package.json and .eslintrc
        with tempfile.TemporaryDirectory() as tmpdir:
            # Write code file
            code_file = os.path.join(tmpdir, 'check.js')
            with open(code_file, 'w') as f:
                f.write(code)
            
            # Write minimal package.json
            package_json = os.path.join(tmpdir, 'package.json')
            with open(package_json, 'w') as f:
                f.write('{"name": "temp", "version": "1.0.0"}')
            
            # Write .eslintrc
            eslintrc = os.path.join(tmpdir, '.eslintrc.json')
            with open(eslintrc, 'w') as f:
                f.write('''
                {
                  "env": {
                    "browser": true,
                    "es2021": true,
                    "node": true
                  },
                  "extends": "eslint:recommended",
                  "parserOptions": {
                    "ecmaVersion": "latest",
                    "sourceType": "module"
                  },
                  "rules": {}
                }
                ''')
            
            # Run eslint
            result = subprocess.run(
                ['npx', 'eslint', '--format', 'json', code_file],
                capture_output=True,
                text=True,
                timeout=15,
                cwd=tmpdir
            )
            
            # Parse JSON output
            import json
            try:
                data = json.loads(result.stdout)
                
                if data and len(data) > 0:
                    for message in data[0].get('messages', []):
                        severity_map = {
                            1: 'warning',
                            2: 'error'
                        }
                        
                        diagnostics.append({
                            "severity": severity_map.get(message.get('severity', 1), 'warning'),
                            "message": message.get('message', 'ESLint issue'),
                            "line": message.get('line', 1),
                            "column": message.get('column', 1),
                            "ruleId": f"eslint/{message.get('ruleId', 'unknown')}"
                        })
            
            except json.JSONDecodeError:
                pass
    
    except (FileNotFoundError, subprocess.TimeoutExpired):
        # eslint not available or timed out
        pass
    except Exception as e:
        # Silent failure
        pass
    
    return diagnostics
