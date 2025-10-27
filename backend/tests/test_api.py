"""
Tests for API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "status" in response.json()

def test_status_endpoint():
    """Test status endpoint"""
    response = client.get("/api/status")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "features" in data
    assert data["status"] == "healthy"

def test_review_python_code():
    """Test Python code review endpoint"""
    request_data = {
        "filePath": "test.py",
        "language": "python",
        "code": "result = eval(user_input)",
        "preferences": {
            "selectedLanguages": ["python"],
            "enableSecurity": True,
            "enableLLM": False,
            "runOnSave": False
        }
    }
    
    response = client.post("/api/review", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert "diagnostics" in data
    assert isinstance(data["diagnostics"], list)
    
    # Should detect eval usage
    diagnostics = data["diagnostics"]
    assert len(diagnostics) > 0

def test_review_javascript_code():
    """Test JavaScript code review endpoint"""
    request_data = {
        "filePath": "test.js",
        "language": "javascript",
        "code": "const result = eval(userInput);",
        "preferences": {
            "selectedLanguages": ["javascript"],
            "enableSecurity": True,
            "enableLLM": False,
            "runOnSave": False
        }
    }
    
    response = client.post("/api/review", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert "diagnostics" in data
    assert len(data["diagnostics"]) > 0

def test_review_unsupported_language():
    """Test review with unsupported language"""
    request_data = {
        "filePath": "test.rs",
        "language": "rust",
        "code": "fn main() { println!(\"Hello\"); }",
        "preferences": {
            "selectedLanguages": ["rust"],
            "enableSecurity": False,
            "enableLLM": False,
            "runOnSave": False
        }
    }
    
    response = client.post("/api/review", json=request_data)
    assert response.status_code == 200
    data = response.json()
    # Should return info about unsupported language
    assert len(data["diagnostics"]) > 0

def test_security_scan_endpoint():
    """Test security scan endpoint"""
    request_data = {
        "filePath": "test.py",
        "language": "python",
        "code": "exec(user_code)",
        "preferences": {
            "selectedLanguages": ["python"],
            "enableSecurity": True,
            "enableLLM": False,
            "runOnSave": False
        }
    }
    
    response = client.post("/api/scan-security", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert "findings" in data
    assert "summary" in data
    assert isinstance(data["findings"], list)
