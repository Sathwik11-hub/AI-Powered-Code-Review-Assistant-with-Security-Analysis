# Contributing to AI Code Review Assistant

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/AI-Powered-Code-Review-Assistant-with-Security-Analysis.git
   cd AI-Powered-Code-Review-Assistant-with-Security-Analysis
   ```

3. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload
```

## Commit Message Format

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, missing semicolons, etc.)
- **refactor**: Code refactoring
- **perf**: Performance improvements
- **test**: Adding or updating tests
- **chore**: Maintenance tasks
- **security**: Security improvements

### Examples

```
feat(editor): add syntax highlighting for Go language

Added support for Go language syntax highlighting in the Monaco
editor component. Updated language selector to include Go option.

Closes #123
```

```
fix(backend): resolve flake8 timeout issue

Increased subprocess timeout from 5s to 10s to prevent premature
termination of flake8 checks on larger files.

Fixes #456
```

```
security(scanner): update Bandit to v1.7.6

Updated Bandit dependency to address CVE-2023-XXXXX.
```

## Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new features
3. **Run linters and tests**:
   ```bash
   # Frontend
   cd frontend
   npm run lint
   npm test
   npm run build
   
   # Backend
   cd backend
   flake8 .
   black --check .
   pytest
   ```

4. **Ensure security scans pass**:
   ```bash
   # Python
   cd backend
   bandit -r .
   safety check
   
   # JavaScript
   cd frontend
   npm audit
   ```

5. **Push to your fork** and submit a pull request
6. **Ensure CI checks pass**
7. **Request review** from maintainers

## Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)
- [ ] Manual testing completed

## Security
- [ ] No new security vulnerabilities introduced
- [ ] Security scans pass (Bandit, Semgrep, npm audit)
- [ ] Sensitive data is not exposed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added/updated
- [ ] All tests pass

## Screenshots (if applicable)
Add screenshots for UI changes

## Related Issues
Closes #(issue number)
```

## Code Style Guidelines

### Python
- Follow [PEP 8](https://pep8.org/)
- Use [Black](https://black.readthedocs.io/) for formatting
- Use type hints where appropriate
- Maximum line length: 100 characters
- Docstrings for all public functions

### JavaScript/React
- Use ESLint recommended rules
- Use Prettier for formatting
- Prefer functional components with hooks
- Use meaningful variable names
- Add JSDoc comments for complex functions

### General
- Write self-documenting code
- Keep functions small and focused
- Follow DRY (Don't Repeat Yourself)
- Add comments for complex logic only
- Prefer clarity over cleverness

## Testing Guidelines

### Frontend Tests
- Use React Testing Library
- Test user interactions, not implementation
- Aim for 80%+ code coverage
- Mock external dependencies

### Backend Tests
- Use pytest
- Test edge cases
- Mock external services
- Test error handling

### Example Test
```python
def test_python_reviewer_detects_eval():
    code = "result = eval(user_input)"
    diagnostics = run_python_review(code)
    
    assert len(diagnostics) > 0
    assert any(d['ruleId'] == 'security/no-eval' for d in diagnostics)
    assert any(d['severity'] == 'error' for d in diagnostics)
```

## Security Guidelines

1. **Never commit secrets** (API keys, passwords, tokens)
2. **Sanitize user input** in all reviewers
3. **Use subprocess timeouts** to prevent DoS
4. **Validate file paths** to prevent directory traversal
5. **Keep dependencies updated**
6. **Run security scans** before submitting PR

## Adding a New Language Reviewer

1. Create `backend/reviewers/{language}_reviewer.py`
2. Implement `run_{language}_review(code: str) -> List[Dict]`
3. Add language to the router in `backend/app.py`
4. Update language selector in `frontend/src/components/Sidebar.jsx`
5. Add tests in `backend/tests/test_{language}_reviewer.py`
6. Update README.md

## Documentation

- Update README for user-facing changes
- Add inline comments for complex code
- Update API documentation for endpoint changes
- Include examples where helpful

## Questions?

- Open an issue with the `question` label
- Check existing issues and discussions
- Reach out to maintainers

## License

By contributing, you agree that your contributions will be licensed under the project's MIT License.

## Recognition

Contributors will be recognized in:
- GitHub contributors page
- Release notes for significant contributions
- README acknowledgments section

Thank you for contributing! 🎉
