# Contributing to ChatProxy Platform

First off, thank you for considering contributing to ChatProxy Platform! 🎉

## Code of Conduct

This project and everyone participating in it is governed by respect, kindness, and professionalism. Please treat all contributors with respect.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates.

**When submitting a bug report, include:**
- Clear title and description
- Steps to reproduce the issue
- Expected vs actual behavior
- Screenshots if applicable
- System information:
  ```bash
  check_system.bat  # Run this and include the report
  ```
- Service logs:
  ```bash
  docker logs [service-name] --tail 50
  ```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:
- Clear title and description
- Use case and motivation
- Expected behavior
- Alternative solutions considered
- Impact on existing functionality

### Pull Requests

**Before submitting a pull request:**

1. **Fork the repository** and create your branch from `main`
2. **Test your changes** thoroughly:
   ```bash
   check_system.bat  # Verify system health
   ```
3. **Update documentation** if you changed functionality
4. **Follow existing code style** (see below)
5. **Write clear commit messages**

**Pull Request Process:**

1. Update the README.md with details of changes if needed
2. Update the documentation in `docs/` folder if applicable
3. The PR will be merged once you have approval from maintainers

## Development Setup

### Prerequisites
- Windows 10/11
- Docker Desktop
- Python 3.x
- Node.js 18+ (for service development)
- Git

### Initial Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/ThankGodForChatProxyPlatform.git
   cd ThankGodForChatProxyPlatform
   ```

2. **Check system prerequisites:**
   ```bash
   check_system.bat
   ```

3. **Follow deployment plan:**
   - See [DEPLOYMENT_PLAN.md](DEPLOYMENT_PLAN.md)

### Development Workflow

**Start services in development mode:**

```bash
# Auth Service (with hot reload)
cd auth-service
npm install
npm run dev

# Accounting Service (with hot reload)
cd accounting-service
npm install
npm run dev

# Flowise Proxy (with hot reload)
cd flowise-proxy-service-py
pip install -r requirements.txt
uvicorn app.main:app --reload

# Bridge UI (with hot reload)
cd bridge
npm install
npm run dev
```

### Code Style

**JavaScript/TypeScript:**
- Use Prettier for formatting
- Follow ESLint rules
- Use TypeScript for type safety
- Async/await over callbacks

**Python:**
- Follow PEP 8 style guide
- Use type hints
- Use FastAPI best practices
- Format with Black

**General:**
- Clear, descriptive variable names
- Comment complex logic
- Write self-documenting code
- Keep functions small and focused

### Testing

**Before submitting PR, ensure:**

1. **All services start successfully:**
   ```bash
   check_system.bat
   ```

2. **Manual testing:**
   - Login as admin, teacher, and student
   - Test chatflow interaction
   - Verify credit tracking
   - Check token refresh (wait 50+ minutes)

3. **Service-specific tests:**
   ```bash
   # Auth Service
   cd auth-service
   npm test

   # Accounting Service
   cd accounting-service
   npm test

   # Flowise Proxy
   cd flowise-proxy-service-py
   pytest
   ```

### Documentation

**Update documentation when:**
- Adding new features
- Changing API endpoints
- Modifying configuration
- Adding dependencies
- Changing deployment process

**Documentation files:**
- `README.md` - Main overview
- `DEPLOYMENT_PLAN.md` - Installation guide
- `SETUP_GUIDE.md` - Configuration reference
- `docs/SERVICE_ARCHITECTURE.md` - Architecture details
- Service-specific README files

## Project Structure

### Key Directories

```
├── bridge/                  # Frontend (React + TypeScript)
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── store/          # State management
│   │   └── api/            # API client
│   └── tests/              # Frontend tests
│
├── auth-service/           # Authentication service
│   ├── src/
│   │   ├── auth/           # Auth logic
│   │   ├── routes/         # API routes
│   │   └── services/       # Business logic
│   └── tests/              # Backend tests
│
├── accounting-service/     # Credit management
│   ├── src/
│   │   ├── controllers/
│   │   ├── services/
│   │   └── models/
│   └── tests/
│
└── flowise-proxy-service-py/  # Integration layer
    ├── app/
    │   ├── api/            # API routes
    │   ├── services/       # Business logic
    │   └── models/         # Data models
    └── tests/
```

### Important Files

- `.env` files - Configuration (never commit!)
- `docker-compose.yml` - Service orchestration
- `package.json` / `requirements.txt` - Dependencies
- `tsconfig.json` - TypeScript config
- `jest.config.js` / `pytest.ini` - Test config

## Commit Message Guidelines

**Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, missing semicolons, etc
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `perf`: Performance improvement
- `test`: Adding missing tests
- `chore`: Maintenance

**Examples:**
```
feat(auth): add password reset functionality

Implement email-based password reset flow with JWT tokens

Closes #123

---

fix(bridge): resolve token refresh race condition

Background token refresh was failing when multiple tabs were open

---

docs: update installation guide for Windows 11

Added troubleshooting section for Docker Desktop on Windows 11
```

## Areas Needing Contribution

### High Priority
- [ ] Automated backup system
- [ ] SSL/HTTPS configuration
- [ ] Comprehensive test suite
- [ ] CI/CD pipeline
- [ ] Performance optimization

### Medium Priority
- [ ] Email notification system
- [ ] Advanced analytics
- [ ] User activity logging
- [ ] API rate limiting
- [ ] Mobile responsive improvements

### Documentation
- [ ] Video tutorials
- [ ] API documentation (Swagger/OpenAPI)
- [ ] Deployment to cloud providers
- [ ] Troubleshooting guide expansion
- [ ] Multi-language support

## Questions?

- Check [DEPLOYMENT_PLAN.md](DEPLOYMENT_PLAN.md) for setup help
- Run `check_system.bat` for diagnostics
- Review [docs/SERVICE_ARCHITECTURE.md](docs/SERVICE_ARCHITECTURE.md) for architecture
- Open an issue for questions

## Recognition

Contributors will be recognized in:
- README.md acknowledgments section
- Release notes
- Project documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to ChatProxy Platform!** 🙏

*Made with ❤️ by the community*
