# 🔄 Migration Guide: CLI to Web API

This guide helps you migrate from the deprecated CLI interface to the new FastAPI-based Web API.

## 📊 Overview

| Feature | CLI (Deprecated) | Web API (Current) |
|---------|------------------|-------------------|
| **Status** | ⚠️ Deprecated | ✅ Active |
| **New Features** | ❌ No | ✅ Yes |
| **Performance** | Good | Better |
| **Documentation** | Manual | Auto-generated (Swagger/ReDoc) |
| **Integration** | Limited | Full REST API |

---

## 🚀 Quick Start with Web API

### 1. Start the API Server
```bash
poetry run python run_api.py

The server will start at `http://localhost:8000`

### 2. Access Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 3. Test the API

bash
curl http://localhost:8000/api/v1/projects

---

## 🔄 Feature Mapping: CLI → API

### **Project Operations**

| CLI Command | API Endpoint | Method |
|-------------|--------------|--------|
| Create Project | `POST /api/v1/projects` | POST |
| List Projects | `GET /api/v1/projects` | GET |
| Get Project | `GET /api/v1/projects/{id}` | GET |
| Update Project | `PUT /api/v1/projects/{id}` | PUT |
| Delete Project | `DELETE /api/v1/projects/{id}` | DELETE |

### **Task Operations**

| CLI Command | API Endpoint | Method |
|-------------|--------------|--------|
| Create Task | `POST /api/v1/tasks` | POST |
| List Tasks | `GET /api/v1/tasks` | GET |
| Get Task | `GET /api/v1/tasks/{id}` | GET |
| Update Task | `PUT /api/v1/tasks/{id}` | PUT |
| Delete Task | `DELETE /api/v1/tasks/{id}` | DELETE |
| Filter by Status | `GET /api/v1/tasks?status=doing` | GET |
| Filter by Project | `GET /api/v1/tasks?project_id={id}` | GET |

---

## 📝 Examples

### **1. Create a Project**

**CLI (Old):**

> Select operation: Create Project
> Enter project title: My Project
> Enter project description: A sample project

**API (New):**
bash
curl -X POST "http://localhost:8000/api/v1/projects" \
  -H "Content-Type: application/json" \
  -d '{
"title": "My Project",
"description": "A sample project"
  }'

**Response:**
json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "My Project",
  "description": "A sample project",
  "created_at": "2025-11-30T12:00:00",
  "updated_at": "2025-11-30T12:00:00"
}

---

### **2. Create a Task**

**CLI (Old):**

> Select operation: Create Task
> Select project: My Project
> Enter task title: Implement feature
> Enter description: Add new functionality
> Enter status (todo/doing/done): todo
> Enter deadline (optional): 2025-12-31

**API (New):**
bash
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -d '{
"title": "Implement feature",
"description": "Add new functionality",
"status": "todo",
"deadline": "2025-12-31",
"project_id": "550e8400-e29b-41d4-a716-446655440000"
  }'

---

### **3. List All Tasks**

**CLI (Old):**

> Select operation: List All Tasks

**API (New):**
bash
curl "http://localhost:8000/api/v1/tasks"

**Response:**
json
{
  "tasks": [
{
"id": "660e8400-e29b-41d4-a716-446655440001",
"title": "Implement feature",
"description": "Add new functionality",
"status": "todo",
"deadline": "2025-12-31",
"project_id": "550e8400-e29b-41d4-a716-446655440000",
"created_at": "2025-11-30T12:00:00",
"updated_at": "2025-11-30T12:00:00"
}
  ],
  "total": 1
}

---

### **4. Filter Tasks by Status**

**CLI (Old):**

> Select operation: Filter Tasks by Status
> Enter status: doing

**API (New):**
bash
curl "http://localhost:8000/api/v1/tasks?status=doing"

---

### **5. Update a Task**

**CLI (Old):**

> Select operation: Update Task
> Select task: Implement feature
> Enter new status: done

**API (New):**
bash
curl -X PUT "http://localhost:8000/api/v1/tasks/660e8400-e29b-41d4-a716-446655440001" \
  -H "Content-Type: application/json" \
  -d '{
"status": "done"
  }'

---

### **6. Delete a Project**

**CLI (Old):**

> Select operation: Delete Project
> Select project: My Project
> Confirm: yes

**API (New):**
bash
curl -X DELETE "http://localhost:8000/api/v1/projects/550e8400-e29b-41d4-a716-446655440000"

---

## 🎯 Advantages of Web API

### **1. Better Integration**
- Can be used by any programming language
- Easy integration with frontend frameworks (React, Vue, etc.)
- Mobile app support

### **2. Automatic Documentation**
- Interactive API docs at `/docs`
- Always up-to-date
- Try endpoints directly in browser

### **3. Better Error Handling**
- Consistent HTTP status codes
- Detailed error messages
- Validation feedback

### **4. Modern Architecture**
- RESTful design
- JSON-based communication
- Scalable and maintainable

### **5. Development Tools**
- Use Postman, Insomnia, or curl
- Browser-based testing
- Easy debugging

---

## 🔧 Migration Checklist

- [ ] Install dependencies: `poetry install`
- [ ] Start API server: `poetry run python run_api.py`
- [ ] Test with Swagger UI: http://localhost:8000/docs
- [ ] Update your automation scripts to use API endpoints
- [ ] Test all your use cases with the new API
- [ ] Update documentation and references
- [ ] Remove CLI usage from workflows

---

## 📚 Additional Resources

- **API Documentation**: http://localhost:8000/docs (when server is running)
- **ReDoc Documentation**: http://localhost:8000/redoc
- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Project Repository**: See README.md for more details

---

## ❓ FAQ

### **Q: Will the CLI be removed?**
A: Yes, in a future phase. For now, it still works but receives no updates.

### **Q: Can I use both CLI and API?**
A: Yes, they share the same database. However, we recommend migrating fully to the API.

### **Q: What if I find a bug in the API?**
A: Please report it through the project's issue tracker.

### **Q: How do I authenticate?**
A: Phase 3 doesn't include authentication. This will be added in Phase 4.

---

## 🆘 Need Help?

If you encounter issues during migration:
1. Check the API documentation at `/docs`
2. Review error messages in API responses
3. Check the project's issue tracker
4. Contact the development team

---

**Last Updated**: November 30, 2025  
**Version**: Phase 3 - Web API


---

## 🎯 **گام بعدی:**

حالا باید:
1. ✅ این فایل رو ذخیره کنی
2. ✅ تست کنی که CLI با Warning اجرا میشه
3. ✅ کامیت نهایی بزنی

آماده برای تست؟ 🚀