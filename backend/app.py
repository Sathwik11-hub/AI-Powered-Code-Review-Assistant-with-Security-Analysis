from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging
import os
from reviewers.python_reviewer import run_python_review
from reviewers.js_reviewer import run_js_review

# Configure logging
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Code Review Assistant API",
    description="API for code review with security analysis",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class Preferences(BaseModel):
    selectedLanguages: List[str] = []
    enableSecurity: bool = True
    enableLLM: bool = False
    runOnSave: bool = False

class ReviewRequest(BaseModel):
    filePath: str
    language: str
    code: str
    preferences: Preferences

class Diagnostic(BaseModel):
    severity: str  # error, warning, suggestion, info
    message: str
    line: int
    column: Optional[int] = 1
    ruleId: Optional[str] = None
    fix: Optional[str] = None
    confidence: Optional[str] = None

class ReviewResponse(BaseModel):
    diagnostics: List[Diagnostic]

class SecurityFinding(BaseModel):
    severity: str
    message: str
    line: int
    column: int
    ruleId: str
    confidence: str

class SecurityScanResponse(BaseModel):
    findings: List[SecurityFinding]
    summary: Dict[str, int]

# Routes
@app.get("/")
async def root():
    return {"message": "AI Code Review Assistant API", "status": "running"}

@app.get("/api/status")
async def status():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "features": {
            "python_review": True,
            "javascript_review": True,
            "security_scan": True,
            "llm_enabled": bool(os.getenv("OPENAI_API_KEY"))
        }
    }

@app.post("/api/review", response_model=ReviewResponse)
async def review_code(request: ReviewRequest):
    """
    Analyze code and return diagnostics
    
    Supports multiple languages and configurable analysis options
    """
    logger.info(f"Reviewing {request.language} code: {request.filePath}")
    
    diagnostics = []
    
    try:
        # Route to language-specific reviewer
        if request.language == "python":
            diagnostics = run_python_review(
                request.code,
                enable_security=request.preferences.enableSecurity
            )
        elif request.language in ["javascript", "typescript"]:
            diagnostics = run_js_review(
                request.code,
                enable_security=request.preferences.enableSecurity
            )
        else:
            # Fallback for unsupported languages
            diagnostics = [{
                "severity": "info",
                "message": f"Language '{request.language}' is not yet supported for automated review",
                "line": 1,
                "column": 1,
                "ruleId": "unsupported-language"
            }]
        
        # Optional LLM enhancement
        if request.preferences.enableLLM and os.getenv("OPENAI_API_KEY"):
            from reviewers.llm_reviewer import enhance_with_llm
            diagnostics = enhance_with_llm(request.code, diagnostics, request.language)
        
        logger.info(f"Found {len(diagnostics)} diagnostics")
        return ReviewResponse(diagnostics=diagnostics)
        
    except Exception as e:
        logger.error(f"Error during review: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Review failed: {str(e)}")

@app.post("/api/scan-security", response_model=SecurityScanResponse)
async def scan_security(request: ReviewRequest):
    """
    Run security-specific scans using Semgrep, Bandit, etc.
    """
    logger.info(f"Running security scan on {request.language} code")
    
    findings = []
    
    try:
        if request.language == "python":
            from scanners.bandit_scanner import run_bandit_scan
            findings = run_bandit_scan(request.code)
        elif request.language in ["javascript", "typescript"]:
            from scanners.semgrep_scanner import run_semgrep_scan
            findings = run_semgrep_scan(request.code, request.language)
        
        # Calculate summary
        summary = {
            "critical": sum(1 for f in findings if f.get("severity") == "critical"),
            "high": sum(1 for f in findings if f.get("severity") == "high"),
            "medium": sum(1 for f in findings if f.get("severity") == "medium"),
            "low": sum(1 for f in findings if f.get("severity") == "low"),
        }
        
        logger.info(f"Security scan complete: {summary}")
        return SecurityScanResponse(findings=findings, summary=summary)
        
    except Exception as e:
        logger.error(f"Security scan error: {str(e)}")
        # Return empty results on error rather than failing
        return SecurityScanResponse(findings=[], summary={"critical": 0, "high": 0, "medium": 0, "low": 0})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
