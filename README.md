
--------------------------------------------------

# To‑Do List Project — Phase 3 (Web API)

A structured, maintainable **To‑Do List Web API** built using **FastAPI**, following a clean layered architecture (Controller → Service → Repository → Database Model).  
Phase 3 of the project focuses on transforming the original CLI‑based system into a fully functional and extendable Web API.

This document explains the project structure, setup, API behavior, and the official **deprecation of the old CLI interface**.

---

## 1. Overview

The project provides a complete CRUD To‑Do List backend with:

- FastAPI‑based Web API  
- Pydantic schemas  
- Layered architecture  
- Filtering, sorting, and validation  
- Naive **Tehran‑time-based** datetime storage  
- Complete migration away from the old Python CLI tool (deprecated)

---

## 2. Why the CLI Is Being Deprecated

Based on the project instructions (Phase 3 documentation):

The original CLI was suitable for early rapid development, but it has limitations:

- Rigid and limited user interface  
- Difficult integration with external tools  
- Hard to maintain and extend  
- No standardized way for complex interactions  
- No automatic input/output documentation  
- No UI or web/mobile compatibility  

Phase 3 introduces a **standardized, extensible API** to support real-world usage and proper architecture decoupling.

### Deprecation ≠ Immediate removal

Deprecating a feature means:

- The feature **still exists and works**  
- But it is **no longer recommended**  
- A **new preferred system** exists (the API)  
- The old system **will be removed in the next release**  
- It is a controlled transition (not breaking systems abruptly)

---

## 3. Deprecation Plan for the CLI (From PDF)

Deprecation happens in **three phases**, and Phase 3 covers the first two:

### Phase 1 — Deprecation Notice

In this project:

- CLI is no longer a primary feature  
- Its usage is discouraged  
- New features are added **only** to the API  
- Warning messages or README notes indicate deprecation  

### Phase 2 — Transition Stage

- CLI remains functional but **frozen**  
- Users are encouraged to migrate to FastAPI  
- Documentation and examples focus on API usage  
- The codebase is prepared for future removal

### Phase 3 — Final Removal (Next Version)

(Not implemented in this phase but described in the PDF)

- All CLI files and folders will be removed  
- Project execution will be **API-only**  
- A new version without CLI will be released  

---

## 4. Project Architecture

A clean layered architecture:

- **Controllers**  
  Handle HTTP requests and return responses  

- **Services**  
  Business logic, validation, rule enforcement  

- **Repositories**  
  DB access, queries, CRUD operations  

- **Database Models**  
  ORM persistence layer (Task model)  

- **Schemas (Pydantic)**  
  Request/response validation and serialization  

This structure keeps responsibilities separated and ensures long-term maintainability.

---

## 5. Tehran Time Handling (Naive datetime strategy)

All datetime fields (e.g., `deadline`, `created_at`) follow:

- Stored in DB as **naive Tehran time**  
- Validated as naive datetime on input  
- Returned to clients formatted as:  
  `YYYY-MM-DD HH:MM`  
- No timezone offsets (`+03:30`) stored or returned

This ensures consistent comparisons and predictable behavior during deadline sorting and filtering.

---

## 6. API Endpoints (Summary)

### GET /tasks
Retrieve task list with optional:

- Filtering (e.g., completed/not completed)
- Sorting (`title`, `deadline`)
- Default sort: `title`

### POST /tasks
Create a new task  
Validates title + Tehran-time deadline

### GET /tasks/{task_id}
Retrieve a single task

### PUT /tasks/{task_id}
Update an existing task

### DELETE /tasks/{task_id}
Remove a task

All endpoints include automatic OpenAPI/Swagger documentation at:

http://localhost:8000/docs

---

## 7. Project Setup

### 1. Install dependencies
```
poetry install
```

### 2. Activate environment
```
poetry shell
```

### 3. Run the API
```
uvicorn todolist.main:app --reload
```

### 4. Open Swagger UI
Visit:
```
http://localhost:8000/docs
```

---

## 8. Directory Structure (Recommended)

```
todolist/
  controllers/
  services/
  repositories/
  models/
  schemas/
  db/
  main.py
```

---

## 9. CLI Status (Important)

The CLI is **officially deprecated**.

- Still exists (Phase 1 & 2 of deprecation)
- Works but **not recommended**
- Will be removed in the *next* release (Phase 3)

Users must interact with the system via:

http://localhost:8000/docs

---

## 10. Future Work

- Full CLI removal (Phase 3 – Removal)
- Add tests (pytest)
- Implement user authentication
- Add tagging and priority fields
- Move to proper timezone‑aware datetimes (optional future improvement)

---

## 11. Credits

Developed as part of **Software Engineering – Phase 3**.  
Features and documentation aligned with the official PDF instructions.

--------------------------------------------------

