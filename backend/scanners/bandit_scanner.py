"""
Bandit security scanner wrapper
"""
import subprocess
import tempfile
import os
import json
from typing import List, Dict, Any

def run_bandit_scan(code: str) -> List[Dict[str, Any]]:
    """
    Run Bandit security scanner on Python code
    
    Returns list of security findings
    """
    findings = []
    
    try:
        # Write code to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        try:
            # Run bandit with JSON output
            result = subprocess.run(
                ['bandit', '-f', 'json', '-ll', temp_file],
                capture_output=True,
                text=True,
                timeout=15
            )
            
            # Parse JSON output
            data = json.loads(result.stdout)
            
            for issue in data.get('results', []):
                severity_map = {
                    'HIGH': 'error',
                    'MEDIUM': 'warning',
                    'LOW': 'info'
                }
                
                findings.append({
                    "severity": severity_map.get(issue.get('issue_severity', 'LOW'), 'info'),
                    "message": issue.get('issue_text', 'Security issue detected'),
                    "line": issue.get('line_number', 1),
                    "column": 1,
                    "ruleId": f"bandit/{issue.get('test_id', 'B000')}",
                    "confidence": issue.get('issue_confidence', 'MEDIUM').lower()
                })
        
        finally:
            os.unlink(temp_file)
    
    except FileNotFoundError:
        # Bandit not installed - return heuristic findings
        findings = _heuristic_python_security_check(code)
    except subprocess.TimeoutExpired:
        findings.append({
            "severity": "warning",
            "message": "Security scan timed out",
            "line": 1,
            "column": 1,
            "ruleId": "timeout",
            "confidence": "low"
        })
    except json.JSONDecodeError:
        pass
    except Exception as e:
        pass
    
    return findings

def _heuristic_python_security_check(code: str) -> List[Dict[str, Any]]:
    """
    Fallback heuristic security checks when Bandit is not available
    """
    findings = []
    lines = code.split('\n')
    
    dangerous_functions = {
        'eval': 'Use of eval() can execute arbitrary code',
        'exec': 'Use of exec() can execute arbitrary code',
        'compile': 'Use of compile() with untrusted input is dangerous',
        '__import__': 'Dynamic imports can be dangerous',
        'pickle.loads': 'Unpickling untrusted data can execute arbitrary code',
    }
    
    for line_num, line in enumerate(lines, start=1):
        for func, message in dangerous_functions.items():
            if func in line and not line.strip().startswith('#'):
                findings.append({
                    "severity": "error",
                    "message": message,
                    "line": line_num,
                    "column": line.index(func) + 1,
                    "ruleId": f"security/{func.replace('.', '-')}",
                    "confidence": "high"
                })
    
    return findings
