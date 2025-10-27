"""
Tests for Python code reviewer
"""
import pytest
from reviewers.python_reviewer import run_python_review

def test_detect_eval_usage():
    """Test that eval() usage is detected"""
    code = """
result = eval(user_input)
print(result)
"""
    diagnostics = run_python_review(code, enable_security=True)
    
    # Should detect eval usage
    eval_issues = [d for d in diagnostics if 'eval' in d.get('message', '').lower()]
    assert len(eval_issues) > 0
    assert any(d['severity'] == 'error' for d in eval_issues)

def test_detect_exec_usage():
    """Test that exec() usage is detected"""
    code = """
exec(user_code)
"""
    diagnostics = run_python_review(code, enable_security=True)
    
    # Should detect exec usage
    exec_issues = [d for d in diagnostics if 'exec' in d.get('message', '').lower()]
    assert len(exec_issues) > 0

def test_syntax_error_detection():
    """Test that syntax errors are caught"""
    code = """
def broken_function(
    print("missing closing parenthesis")
"""
    diagnostics = run_python_review(code, enable_security=False)
    
    # Should detect syntax error
    syntax_errors = [d for d in diagnostics if d.get('ruleId') == 'syntax-error']
    assert len(syntax_errors) > 0
    assert syntax_errors[0]['severity'] == 'error'

def test_clean_code():
    """Test that clean code produces minimal issues"""
    code = """
def calculate_sum(numbers):
    return sum(numbers)


result = calculate_sum([1, 2, 3, 4, 5])
print(result)
"""
    diagnostics = run_python_review(code, enable_security=True)
    
    # Clean code should have no critical security errors
    security_errors = [d for d in diagnostics if d['severity'] == 'error' and 'security' in d.get('ruleId', '')]
    assert len(security_errors) == 0

def test_empty_code():
    """Test handling of empty code"""
    diagnostics = run_python_review("", enable_security=True)
    
    # Empty code should not crash
    assert isinstance(diagnostics, list)
