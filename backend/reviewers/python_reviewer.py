"""
Python code reviewer using flake8, bandit, and AST analysis
"""
import ast
import subprocess
import tempfile
import os
from typing import List, Dict, Any

def run_python_review(code: str, enable_security: bool = True) -> List[Dict[str, Any]]:
    """
    Run Python code review with multiple tools
    
    Returns list of diagnostics with format:
    {
        "severity": "error" | "warning" | "suggestion" | "info",
        "message": str,
        "line": int,
        "column": int,
        "ruleId": str,
        "fix": Optional[str]
    }
    """
    diagnostics = []
    
    # AST-based security checks
    diagnostics.extend(_check_dangerous_patterns(code))
    
    # Run flake8 if available
    diagnostics.extend(_run_flake8(code))
    
    # Run bandit for security if enabled
    if enable_security:
        diagnostics.extend(_run_bandit(code))
    
    return diagnostics

def _check_dangerous_patterns(code: str) -> List[Dict[str, Any]]:
    """
    Check for dangerous patterns using AST analysis
    """
    diagnostics = []
    
    try:
        tree = ast.parse(code)
        
        for node in ast.walk(tree):
            # Check for eval() usage
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id == 'eval':
                    diagnostics.append({
                        "severity": "error",
                        "message": "Use of eval() is dangerous and should be avoided",
                        "line": node.lineno,
                        "column": node.col_offset + 1,
                        "ruleId": "security/no-eval",
                        "confidence": "high"
                    })
                
                # Check for exec() usage
                if isinstance(node.func, ast.Name) and node.func.id == 'exec':
                    diagnostics.append({
                        "severity": "error",
                        "message": "Use of exec() is dangerous and should be avoided",
                        "line": node.lineno,
                        "column": node.col_offset + 1,
                        "ruleId": "security/no-exec",
                        "confidence": "high"
                    })
            
            # Check for inefficient patterns
            if isinstance(node, ast.For):
                # Check for list concatenation in loop (inefficient)
                for child in ast.walk(node):
                    if isinstance(child, ast.AugAssign) and isinstance(child.op, ast.Add):
                        diagnostics.append({
                            "severity": "suggestion",
                            "message": "Consider using list comprehension or append() instead of concatenation in loop",
                            "line": child.lineno,
                            "column": child.col_offset + 1,
                            "ruleId": "performance/loop-concat",
                        })
                        break
    
    except SyntaxError as e:
        diagnostics.append({
            "severity": "error",
            "message": f"Syntax error: {str(e)}",
            "line": e.lineno or 1,
            "column": e.offset or 1,
            "ruleId": "syntax-error"
        })
    
    return diagnostics

def _run_flake8(code: str) -> List[Dict[str, Any]]:
    """
    Run flake8 linter on code
    """
    diagnostics = []
    
    try:
        # Write code to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        try:
            # Run flake8
            result = subprocess.run(
                ['flake8', '--format=%(row)d:%(col)d:%(code)s:%(text)s', temp_file],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # Parse output
            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue
                
                parts = line.split(':', 3)
                if len(parts) >= 4:
                    row, col, code, message = parts
                    
                    # Determine severity based on code
                    severity = "warning"
                    if code.startswith('E'):
                        severity = "error"
                    elif code.startswith('W'):
                        severity = "warning"
                    elif code.startswith('F'):
                        severity = "error"
                    
                    diagnostics.append({
                        "severity": severity,
                        "message": message.strip(),
                        "line": int(row),
                        "column": int(col),
                        "ruleId": f"flake8/{code}"
                    })
        
        finally:
            os.unlink(temp_file)
    
    except FileNotFoundError:
        # flake8 not installed
        pass
    except subprocess.TimeoutExpired:
        diagnostics.append({
            "severity": "warning",
            "message": "flake8 check timed out",
            "line": 1,
            "column": 1,
            "ruleId": "timeout"
        })
    except Exception as e:
        # Silent failure for linter issues
        pass
    
    return diagnostics

def _run_bandit(code: str) -> List[Dict[str, Any]]:
    """
    Run bandit security scanner on code
    """
    diagnostics = []
    
    try:
        # Write code to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        try:
            # Run bandit
            result = subprocess.run(
                ['bandit', '-f', 'json', temp_file],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # Parse JSON output
            import json
            try:
                data = json.loads(result.stdout)
                
                for finding in data.get('results', []):
                    severity_map = {
                        'HIGH': 'error',
                        'MEDIUM': 'warning',
                        'LOW': 'info'
                    }
                    
                    diagnostics.append({
                        "severity": severity_map.get(finding.get('issue_severity', 'LOW'), 'info'),
                        "message": finding.get('issue_text', 'Security issue detected'),
                        "line": finding.get('line_number', 1),
                        "column": 1,
                        "ruleId": f"bandit/{finding.get('test_id', 'unknown')}",
                        "confidence": finding.get('issue_confidence', 'MEDIUM').lower()
                    })
            
            except json.JSONDecodeError:
                pass
        
        finally:
            os.unlink(temp_file)
    
    except FileNotFoundError:
        # bandit not installed
        pass
    except subprocess.TimeoutExpired:
        pass
    except Exception as e:
        pass
    
    return diagnostics
