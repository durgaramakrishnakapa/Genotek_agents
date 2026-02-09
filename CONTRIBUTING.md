# Contributing to Genotek AI Lead Generation Platform

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/genotek-ai.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test thoroughly
6. Commit with clear messages
7. Push and create a Pull Request

## 📋 Development Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- Git

### Setup Steps
```bash
# Backend
pip install -r backend/requirements.txt
cp backend/config.example.py backend/config.py
# Add your API keys to config.py

# Frontend
cd frontend
npm install
```

## 🎯 What to Contribute

### High Priority
- Bug fixes
- Performance improvements
- Documentation improvements
- Test coverage

### Welcome Contributions
- New agent types
- UI/UX improvements
- Additional validation logic
- Analytics features

### Please Discuss First
- Major architectural changes
- New external dependencies
- Breaking changes

## 📝 Code Style

### Python
- Follow PEP 8
- Use type hints
- Add docstrings to functions
- Keep functions focused and small

```python
def search_projects(query: str, max_results: int = 10) -> List[Dict]:
    """
    Search for construction projects using SerperDev API.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return
        
    Returns:
        List of project dictionaries
    """
    pass
```

### TypeScript/React
- Use functional components
- Follow ESLint rules
- Use TypeScript types
- Keep components small and focused

```typescript
interface ProjectProps {
  project: Project;
  onSelect: (id: string) => void;
}

export function ProjectCard({ project, onSelect }: ProjectProps) {
  // Component logic
}
```

## 🧪 Testing

### Before Submitting
- Test your changes locally
- Run existing tests
- Add tests for new features
- Verify no console errors

### Running Tests
```bash
# Python tests
python -m pytest backend/tests/

# Frontend tests
cd frontend
npm test
```

## 📦 Commit Guidelines

Use conventional commits:

```
feat: add new hospital search query
fix: correct validation logic for dates
docs: update README with new features
style: format code according to PEP 8
refactor: simplify watchlist update logic
test: add tests for agent.py
chore: update dependencies
```

## 🔍 Pull Request Process

1. **Update Documentation**
   - Update README if needed
   - Add comments to complex code
   - Update API documentation

2. **Test Thoroughly**
   - All existing tests pass
   - New tests added for new features
   - Manual testing completed

3. **Clean Commits**
   - Squash unnecessary commits
   - Clear commit messages
   - No merge commits

4. **PR Description**
   - What changes were made
   - Why the changes were needed
   - How to test the changes
   - Screenshots if UI changes

### PR Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How to test these changes

## Screenshots (if applicable)
Add screenshots here

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added to complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests passing
```

## 🐛 Bug Reports

### Before Reporting
- Check existing issues
- Verify it's reproducible
- Test on latest version

### Bug Report Template
```markdown
**Describe the bug**
Clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What should happen

**Screenshots**
If applicable

**Environment**
- OS: [e.g., Windows 10]
- Python version: [e.g., 3.9]
- Node version: [e.g., 16.14]
- Browser: [e.g., Chrome 98]

**Additional context**
Any other relevant information
```

## 💡 Feature Requests

### Feature Request Template
```markdown
**Is your feature request related to a problem?**
Clear description of the problem

**Describe the solution you'd like**
What you want to happen

**Describe alternatives you've considered**
Other solutions you've thought about

**Additional context**
Any other relevant information
```

## 🔐 Security

### Reporting Security Issues
- **DO NOT** open public issues for security vulnerabilities
- Email: security@genotek.com
- Include detailed description
- Include steps to reproduce

### Security Best Practices
- Never commit API keys
- Use environment variables
- Validate all inputs
- Follow OWASP guidelines

## 📚 Documentation

### What to Document
- New features
- API changes
- Configuration options
- Complex algorithms

### Documentation Style
- Clear and concise
- Include examples
- Use proper formatting
- Keep up to date

## 🤝 Code Review

### As a Reviewer
- Be respectful and constructive
- Focus on code, not the person
- Explain your suggestions
- Approve when ready

### As an Author
- Respond to all comments
- Make requested changes
- Ask questions if unclear
- Thank reviewers

## 📞 Getting Help

- **Questions**: Open a discussion
- **Bugs**: Open an issue
- **Features**: Open a feature request
- **Security**: Email security@genotek.com

## 🎉 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation

## 📄 License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing to Genotek AI! 🚀
