"""
Tests for JavaScript code reviewer
"""
import pytest
from reviewers.js_reviewer import run_js_review

def test_detect_eval_usage():
    """Test that eval() usage is detected"""
    code = """
const userInput = getUserInput();
const result = eval(userInput);
console.log(result);
"""
    diagnostics = run_js_review(code, enable_security=True)
    
    # Should detect eval usage
    eval_issues = [d for d in diagnostics if 'eval' in d.get('message', '').lower()]
    assert len(eval_issues) > 0
    assert any(d['severity'] == 'error' for d in eval_issues)

def test_detect_innerHTML_usage():
    """Test that innerHTML usage is detected"""
    code = """
document.getElementById('content').innerHTML = userInput;
"""
    diagnostics = run_js_review(code, enable_security=True)
    
    # Should detect innerHTML usage (warning level is acceptable)
    innerHTML_issues = [d for d in diagnostics if 'innerHTML' in d.get('message', '').lower() or 'innerHTML' in d.get('ruleId', '')]
    assert len(innerHTML_issues) > 0

def test_detect_var_usage():
    """Test that var usage is detected (prefer let/const)"""
    code = """
var x = 10;
var name = 'test';
"""
    diagnostics = run_js_review(code, enable_security=False)
    
    # Should suggest using let/const
    var_issues = [d for d in diagnostics if 'var' in d.get('message', '').lower()]
    assert len(var_issues) > 0

def test_clean_code():
    """Test that clean code produces minimal issues"""
    code = """
const calculateSum = (numbers) => {
    return numbers.reduce((a, b) => a + b, 0);
};

const result = calculateSum([1, 2, 3, 4, 5]);
"""
    diagnostics = run_js_review(code, enable_security=True)
    
    # Clean code should have no critical errors
    errors = [d for d in diagnostics if d['severity'] == 'error']
    assert len(errors) == 0

def test_empty_code():
    """Test handling of empty code"""
    diagnostics = run_js_review("", enable_security=True)
    
    # Empty code should not crash
    assert isinstance(diagnostics, list)
