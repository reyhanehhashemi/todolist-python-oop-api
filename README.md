# 📋 ToDoList - Python OOP (In-Memory)

A CLI-based task management application built with Python and Object-Oriented Programming principles. This project demonstrates clean architecture, comprehensive testing, and modern Python development practices.

## 🎯 Project Overview

This is **Phase 1** of a multi-phase development project that implements an in-memory ToDoList system. The application allows users to manage projects and their associated tasks through a command-line interface.

### Development Approach
- **Incremental Development**: Each phase delivers a working product
- **Agile Methodology**: Rapid feedback and continuous delivery
- **Test-Driven Development**: Comprehensive test coverage ensuring reliability

## ✨ Features

### Task Management
- ✅ Create, Read, Update, Delete (CRUD) operations
- ✅ Task status tracking (`todo`, `doing`, `done`)
- ✅ Optional deadline support
- ✅ Title validation (max 30 characters)
- ✅ Description validation (max 150 characters)

### Project Management
- 📁 Multiple project support
- 📁 Project-task association
- 📁 Cascade delete (removing project deletes all associated tasks)
- 📁 Project name uniqueness validation
- 📁 Configurable project limit (`MAX_NUMBER_OF_PROJECT`)

### Data Persistence
- 💾 In-memory storage (Phase 1)
- 💾 Fast read/write operations
- 💾 Session-based data (resets on restart)

## 🏗️ Architecture

The project follows a clean, layered architecture:

src/todolist/
├── models/          # Domain models (Task, Project)
├── repositories/    # Data access layer (In-memory storage)
├── services/        # Business logic layer
└── main.py          # Application entry point


### Design Patterns
- **Repository Pattern**: Abstracts data storage
- **Service Layer**: Separates business logic from data access
- **Domain Model**: Rich domain objects with validation

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher
- Poetry (dependency management)

### Installation

```bash
# Clone the repository
git clone https://github.com/reyhanehhashemi/todolist-python-oop.git
cd todolist-python-oop

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

### Running the Application

```bash
# Run as module
poetry run python -m todolist

# Or if virtual environment is activated
python -m todolist
```

## 🧪 Testing

The project includes comprehensive test coverage with 42 automated tests.

### Run Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage report
poetry run pytest --cov=todolist --cov-report=html

# Run specific test file
poetry run pytest tests/test_task_service.py

# Run with verbose output
poetry run pytest -v
```

### Test Coverage

- **Overall Coverage**: 95%+ on core modules
- **Test Categories**:
  - Unit tests for models
  - Service layer tests
  - Repository tests
  - Integration tests

## 📦 Dependencies

### Production
- `python-dotenv`: Configuration management

### Development
- `pytest`: Testing framework
- `pytest-cov`: Coverage reporting

## 📐 Validation Rules

### Task Validation
| Field | Rule |
|-------|------|
| Title | Required, max 30 characters |
| Description | Required, max 150 characters |
| Status | Must be one of: `todo`, `doing`, `done` |
| Deadline | Optional, must be valid date if provided |

### Project Validation
| Field | Rule |
|-------|------|
| Name | Required, min 3 characters, must be unique |
| Description | Required, max 150 characters |
| Max Projects | Configurable via `MAX_NUMBER_OF_PROJECT` |

## 🎓 Learning Objectives

This project demonstrates:

1. **Object-Oriented Programming**
   - Encapsulation
   - Inheritance
   - Polymorphism
   - SOLID principles

2. **Clean Architecture**
   - Separation of concerns
   - Dependency injection
   - Repository pattern

3. **Modern Python Practices**
   - Type hints
   - Dataclasses
   - Context managers
   - Comprehensive docstrings

4. **Testing Best Practices**
   - Unit testing
   - Test fixtures
   - Mocking
   - Coverage analysis

5. **Development Workflow**
   - Git flow (main/develop branches)
   - Conventional commits
   - Dependency management with Poetry
   - CI/CD ready structure

## 🗺️ Roadmap

### ✅ Phase 1: In-Memory Storage (Current)
- Task and Project CRUD operations
- Input validation
- CLI interface
- Comprehensive testing

### 🔜 Phase 2: Database Persistence (Planned)
- SQLite/PostgreSQL integration
- Data migration support
- Advanced queries

### 🔜 Phase 3: Web API (Planned)
- RESTful API
- Authentication
- API documentation

### 🔜 Phase 4: Frontend (Planned)
- Web interface
- Real-time updates
- User dashboard

## 📝 Development Guidelines

### Code Style
- Follow **PEP 8** standards
- Use **type hints** throughout
- Write **descriptive docstrings**
- Keep functions **small and focused**

### Commit Messages
Follow conventional commit format:
feat: add new feature
fix: bug fix
docs: documentation update
test: add or update tests
refactor: code refactoring
chore: maintenance tasks


### Branch Strategy
- `main`: Production-ready code
- `develop`: Development branch
- `feature/*`: New features
- `fix/*`: Bug fixes

## 🤝 Contributing

This is an educational project. Contributions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is part of the Software Engineering course at AUT (Amirkabir University of Technology).

## 👥 Author

**Reyhaneh Hashemi**
- GitHub: [@reyhanehhashemi](https://github.com/reyhanehhashemi)

## 🙏 Acknowledgments

- Course: Software Engineering - AUT
- Date: October 2025
- Project: ToDoList Python OOP Implementation

---

**Note**: This is Phase 1 of the project focusing on in-memory storage. Future phases will add database persistence, web API, and frontend capabilities.
