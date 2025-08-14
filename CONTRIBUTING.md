# Contributing to Intelligent Engine Maintenance Assistant

Thank you for your interest in contributing to this project! This guide will help you get started.

## 🌟 Ways to Contribute

- **Code**: Bug fixes, new features, performance improvements
- **Documentation**: Tutorials, API docs, usage examples  
- **Data**: Additional synthetic datasets, validation data
- **Testing**: Writing tests, reporting bugs, testing edge cases
- **Community**: Answering questions, code reviews, discussions

## 🚀 Getting Started

### 1. Set Up Development Environment

```bash
# Fork and clone the repository
git clone https://github.com/yourusername/intelligent-engine-maintenance-assistant.git
cd intelligent-engine-maintenance-assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Add your Google AI Studio API key to .env

# Initialize database
python initialize_db.py
```

### 2. Development Workflow

1. **Create a branch**: `git checkout -b feature/your-feature-name`
2. **Make changes**: Follow coding standards (see below)
3. **Test locally**: Run tests and ensure they pass
4. **Commit**: Use conventional commit messages
5. **Push**: `git push origin feature/your-feature-name`
6. **Pull Request**: Create PR with clear description

## 📋 Development Guidelines

### Code Style
- **Python**: Follow PEP 8, use `black` for formatting
- **Line Length**: Maximum 88 characters (black default)
- **Import Order**: Use `isort` for consistent import ordering
- **Type Hints**: Use type hints for all functions
- **Docstrings**: Use Google-style docstrings

Example function:
```python
def process_maintenance_record(
    record: Dict[str, Any], 
    vehicle_id: str
) -> MaintenanceResult:
    """Process a maintenance record and return structured result.

    Args:
        record: Raw maintenance record dictionary
        vehicle_id: Unique vehicle identifier

    Returns:
        MaintenanceResult: Processed maintenance information

    Raises:
        ValidationError: If record format is invalid
    """
    pass
```

### Testing Standards
- **Coverage**: Maintain >90% test coverage
- **Types**: Unit tests, integration tests, end-to-end tests
- **Naming**: Test function names should describe what they test
- **Fixtures**: Use pytest fixtures for common test data

### Documentation
- **README**: Keep updated with new features
- **API Docs**: Document all public functions
- **Examples**: Provide usage examples for new features
- **Changelogs**: Update CHANGELOG.md for significant changes

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html

# Run specific test file  
python -m pytest tests/test_rag_pipeline.py -v
```

### Writing Tests
- Place tests in `tests/` directory
- Mirror source structure in test structure
- Use descriptive test names
- Test both happy path and edge cases

## 🐛 Reporting Issues

### Bug Reports
Use the bug report template and include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Relevant logs or error messages

### Feature Requests  
Use the feature request template and include:
- Clear description of the proposed feature
- Use case and motivation
- Potential implementation approach
- Any related issues or discussions

## 📝 Commit Guidelines

Use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New features
- `fix:` Bug fixes  
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding or modifying tests
- `chore:` Other changes (dependencies, etc.)

Examples:
```
feat: add support for multi-modal document processing
fix: resolve vector search timeout issue
docs: update API documentation for new endpoints
test: add integration tests for RAG pipeline
```

## 🔄 Pull Request Process

1. **Branch**: Create from `main` branch
2. **Commits**: Use conventional commit format
3. **Tests**: Ensure all tests pass
4. **Documentation**: Update relevant docs
5. **Description**: Provide clear PR description

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
- [ ] Tests pass locally
- [ ] Added tests for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

## 🏆 Recognition

Contributors will be:
- Listed in README.md acknowledgments
- Featured in release notes for significant contributions  
- Invited to join the maintainers team for sustained contributions

## 💬 Community Guidelines

- **Be respectful**: Treat all community members with respect
- **Be constructive**: Provide helpful, actionable feedback
- **Be collaborative**: Work together to improve the project
- **Be patient**: Remember that everyone is learning

## 📞 Getting Help

- **GitHub Discussions**: General questions and discussions
- **Issues**: Bug reports and feature requests
- **Email**: [maintainer@email.com] for sensitive matters

Thank you for contributing to making trucking maintenance smarter and more efficient! 🚚✨
