# Contributing to Automated Certificate Mailer

First off, thank you for considering contributing to this project! 🎉

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear title and description
- Steps to reproduce the problem
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)

### Suggesting Enhancements

Have an idea? Open an issue with:
- A clear description of the enhancement
- Why it would be useful
- Possible implementation approach

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes**:
   - Follow PEP 8 style guidelines
   - Add comments for complex logic
   - Update documentation if needed
3. **Test your changes**:
   - Test with `--dry-run` mode
   - Verify existing functionality still works
4. **Commit with clear messages**:
   - Use conventional commits (feat:, fix:, docs:, etc.)
5. **Push to your fork** and submit a pull request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/Automated-Certificate-Mailer.git
cd Automated-Certificate-Mailer

# Create a branch
git checkout -b feature/my-awesome-feature

# Set up test environment
cp config.example.py config.py
# Edit config.py with test credentials

# Test your changes
python send_emails2.py --dry-run --verbose
```

### Code Style

- Follow [PEP 8](https://pep8.org/)
- Maximum line length: 120 characters
- Use meaningful variable names
- Add docstrings to functions
- Comment complex logic

### Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Examples:
- `feat: add progress bar with ETA calculation`
- `fix: handle missing certificate files gracefully`
- `docs: update README with Docker instructions`

## Code of Conduct

- Be respectful and constructive
- Welcome newcomers and help them learn
- Focus on what is best for the community
- Show empathy towards other contributors

## Questions?

Feel free to open a discussion or reach out to the maintainers!

---

**Thank you for contributing!** 🙏
