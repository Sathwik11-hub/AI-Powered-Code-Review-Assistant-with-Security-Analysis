"""
Semgrep security scanner wrapper
"""
import subprocess
import tempfile
import os
import json
from typing import List, Dict, Any

def run_semgrep_scan(code: str, language: str = "javascript") -> List[Dict[str, Any]]:
    """
    Run Semgrep security scanner on code
    
    Returns list of security findings
    """
    findings = []
    
    try:
        # Determine file extension
        ext_map = {
            'javascript': '.js',
            'typescript': '.ts',
            'python': '.py',
            'java': '.java',
            'go': '.go'
        }
        ext = ext_map.get(language, '.txt')
        
        # Write code to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix=ext, delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        try:
            # Run semgrep with security rules
            result = subprocess.run(
                ['semgrep', '--config=auto', '--json', temp_file],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Parse JSON output
            data = json.loads(result.stdout)
            
            for issue in data.get('results', []):
                # Map semgrep severity to our severity levels
                severity = issue.get('extra', {}).get('severity', 'WARNING')
                severity_map = {
                    'ERROR': 'error',
                    'WARNING': 'warning',
                    'INFO': 'info'
                }
                
                findings.append({
                    "severity": severity_map.get(severity, 'warning'),
                    "message": issue.get('extra', {}).get('message', 'Security issue detected'),
                    "line": issue.get('start', {}).get('line', 1),
                    "column": issue.get('start', {}).get('col', 1),
                    "ruleId": f"semgrep/{issue.get('check_id', 'unknown')}",
                    "confidence": "high"
                })
        
        finally:
            os.unlink(temp_file)
    
    except FileNotFoundError:
        # Semgrep not installed - return heuristic findings
        findings = _heuristic_js_security_check(code) if language in ['javascript', 'typescript'] else []
    except subprocess.TimeoutExpired:
        findings.append({
            "severity": "warning",
            "message": "Semgrep scan timed out",
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

def _heuristic_js_security_check(code: str) -> List[Dict[str, Any]]:
    """
    Fallback heuristic security checks for JavaScript when Semgrep is not available
    """
    findings = []
    lines = code.split('\n')
    
    dangerous_patterns = {
        'eval(': 'Use of eval() can execute arbitrary code',
        'innerHTML': 'Direct use of innerHTML can lead to XSS vulnerabilities',
        'document.write': 'document.write can lead to XSS vulnerabilities',
        'dangerouslySetInnerHTML': 'dangerouslySetInnerHTML can lead to XSS if not properly sanitized',
        'new Function(': 'Creating functions from strings can be dangerous',
    }
    
    for line_num, line in enumerate(lines, start=1):
        for pattern, message in dangerous_patterns.items():
            if pattern in line and not line.strip().startswith('//'):
                findings.append({
                    "severity": "warning" if pattern != 'eval(' else "error",
                    "message": message,
                    "line": line_num,
                    "column": line.index(pattern) + 1,
                    "ruleId": f"security/{pattern.replace('(', '').replace('.', '-')}",
                    "confidence": "medium"
                })
    
    return findings

def parse_semgrep_output(json_str: str) -> List[Dict[str, Any]]:
    """
    Parse Semgrep JSON output into our diagnostic format
    
    This can be used with external semgrep runs
    """
    findings = []
    
    try:
        data = json.loads(json_str)
        
        for issue in data.get('results', []):
            severity = issue.get('extra', {}).get('severity', 'WARNING')
            severity_map = {
                'ERROR': 'error',
                'WARNING': 'warning',
                'INFO': 'info'
            }
            
            findings.append({
                "severity": severity_map.get(severity, 'warning'),
                "message": issue.get('extra', {}).get('message', 'Security issue'),
                "line": issue.get('start', {}).get('line', 1),
                "column": issue.get('start', {}).get('col', 1),
                "ruleId": f"semgrep/{issue.get('check_id', 'unknown')}",
                "confidence": "high"
            })
    
    except json.JSONDecodeError:
        pass
    
    return findings
