# Contributing to Digital Psychological Intervention System

Thank you for your interest in contributing to the Digital Psychological Intervention System! This document provides guidelines and information for contributors.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct:

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive feedback
- Respect privacy and confidentiality concerns
- Remember that this project deals with sensitive mental health topics

## Getting Started

### Development Setup

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/digital-psychological-intervention-system.git
   cd digital-psychological-intervention-system
   ```
3. **Install dependencies**:
   ```bash
   # Backend dependencies
   cd backend
   npm install
   
   # Frontend dependencies
   cd ../frontend
   npm install
   ```
4. **Set up environment variables** (see .env.example files)
5. **Run the development servers**

### Development Workflow

1. **Create a feature branch**: `git checkout -b feature/your-feature-name`
2. **Make your changes** following our coding standards
3. **Write tests** for new functionality
4. **Run tests** to ensure everything works
5. **Commit your changes** with descriptive messages
6. **Push to your fork** and create a Pull Request

## Coding Standards

### Frontend (React/TypeScript)

- Use TypeScript for type safety
- Follow React hooks patterns
- Use Material-UI components consistently
- Implement responsive design
- Write unit tests with Jest and React Testing Library

### Backend (Node.js/Express)

- Use async/await for asynchronous operations
- Implement proper error handling
- Follow RESTful API conventions
- Write comprehensive API documentation
- Implement proper logging

### General Guidelines

- Write clear, self-documenting code
- Add comments for complex logic
- Follow consistent naming conventions
- Keep functions small and focused
- Implement proper error handling

## Testing

### Frontend Testing
```bash
cd frontend
npm test
```

### Backend Testing
```bash
cd backend
npm test
```

### Integration Testing
```bash
npm run test:integration
```

## Security Considerations

Given the sensitive nature of mental health data:

- **Never commit sensitive data** (API keys, passwords, etc.)
- **Implement proper data encryption**
- **Follow HIPAA compliance guidelines** where applicable
- **Validate all user inputs**
- **Use secure authentication methods**

## Documentation

- Update documentation when adding new features
- Include inline code comments
- Write clear commit messages
- Update API documentation for backend changes

## Pull Request Guidelines

### Before Submitting

- [ ] Code follows project style guidelines
- [ ] Tests pass locally
- [ ] Documentation is updated
- [ ] No sensitive data is included
- [ ] Changes are tested thoroughly

### Pull Request Template

When creating a Pull Request, please include:

1. **Description** of changes
2. **Type of change** (bug fix, feature, documentation, etc.)
3. **Testing** performed
4. **Screenshots** (if applicable)
5. **Related issues** (if any)

## Issue Guidelines

### Bug Reports

Include:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Screenshots (if applicable)

### Feature Requests

Include:
- Clear description of the feature
- Use case and rationale
- Proposed implementation (if any)
- Impact on existing functionality

## Community Guidelines

### Mental Health Sensitivity

- Use appropriate, non-stigmatizing language
- Respect cultural and regional differences
- Consider accessibility in all features
- Prioritize user privacy and confidentiality

### Communication

- Be respectful in all interactions
- Provide constructive feedback
- Help newcomers get started
- Ask for help when needed

## Recognition

Contributors will be recognized in:
- Project README
- Release notes
- Contributor wall (if implemented)

## Questions?

- Create an issue for technical questions
- Join our community discussions
- Contact the maintainers directly

Thank you for contributing to making mental health support more accessible!
