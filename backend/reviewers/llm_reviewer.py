"""
LLM-based code reviewer using OpenAI API

Provides AI-powered code explanations and fix suggestions
"""
import os
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

def enhance_with_llm(code: str, diagnostics: List[Dict[str, Any]], language: str) -> List[Dict[str, Any]]:
    """
    Enhance diagnostics with LLM-generated suggestions
    
    This is a stub implementation that can be extended with actual OpenAI API calls
    """
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        logger.warning("OPENAI_API_KEY not set, LLM enhancement disabled")
        return diagnostics
    
    try:
        # Import OpenAI client
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        # Only enhance high-severity issues to save API costs
        high_severity = [d for d in diagnostics if d.get('severity') in ['error', 'warning']]
        
        if len(high_severity) > 3:
            high_severity = high_severity[:3]  # Limit to 3 to control costs
        
        enhanced = []
        
        for diagnostic in high_severity:
            try:
                # Get code snippet around the issue
                lines = code.split('\n')
                line_num = diagnostic.get('line', 1) - 1
                start = max(0, line_num - 2)
                end = min(len(lines), line_num + 3)
                snippet = '\n'.join(lines[start:end])
                
                # Create prompt
                prompt = f"""You are a code review assistant. Analyze this {language} code snippet and the detected issue:

Issue: {diagnostic.get('message')}
Rule: {diagnostic.get('ruleId', 'unknown')}
Severity: {diagnostic.get('severity')}

Code snippet:
```{language}
{snippet}
```

Provide:
1. A brief explanation of why this is an issue (1-2 sentences)
2. A suggested fix (if applicable)
3. Confidence level (high/medium/low)

Keep your response concise and practical."""

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an expert code reviewer focused on security and best practices."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=200,
                    temperature=0.3
                )
                
                llm_response = response.choices[0].message.content
                
                # Append LLM explanation to diagnostic
                diagnostic['llm_explanation'] = llm_response
                enhanced.append(diagnostic)
                
            except Exception as e:
                logger.error(f"LLM enhancement failed for diagnostic: {str(e)}")
                enhanced.append(diagnostic)
        
        # Add remaining diagnostics unchanged
        remaining = [d for d in diagnostics if d not in high_severity]
        enhanced.extend(remaining)
        
        return enhanced
    
    except ImportError:
        logger.warning("OpenAI package not installed, LLM enhancement disabled")
        return diagnostics
    except Exception as e:
        logger.error(f"LLM enhancement failed: {str(e)}")
        return diagnostics

def get_llm_code_review(code: str, language: str) -> List[Dict[str, Any]]:
    """
    Get a complete code review from LLM
    
    This performs a general review without specific diagnostics
    """
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        return []
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        # Limit code length to avoid token limits
        if len(code) > 2000:
            code = code[:2000] + "\n# ... (code truncated)"
        
        prompt = f"""Review this {language} code for:
1. Security vulnerabilities
2. Performance issues
3. Best practice violations
4. Code quality improvements

Code:
```{language}
{code}
```

Provide specific findings with line numbers where possible."""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a senior software engineer performing a code review."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.5
        )
        
        # Parse response into diagnostics
        # This is a simplified parser - in production you'd want more sophisticated parsing
        review_text = response.choices[0].message.content
        
        # Return as a single info diagnostic for now
        return [{
            "severity": "info",
            "message": f"LLM Review: {review_text}",
            "line": 1,
            "column": 1,
            "ruleId": "llm-review"
        }]
    
    except Exception as e:
        logger.error(f"LLM code review failed: {str(e)}")
        return []
