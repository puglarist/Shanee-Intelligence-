# Development Guide

Complete guide for contributing to Shanee Intelligence ecosystem development.

---

## Getting Started

### Prerequisites

- Git (for version control)
- Docker & Docker Compose (for local development)
- Node.js 18+ (for frontend work)
- Python 3.11+ (for backend work)
- Code editor (VS Code, JetBrains, etc.)

### Initial Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/puglarist/Shanee-Intelligence-
   cd Shanee-Intelligence-
   ```

2. **Create a development branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Start development environment**
   ```bash
   docker-compose up
   ```

4. **Access the services**
   - Frontend: http://localhost:5173
   - Backend: http://localhost:8000
   - API Docs: http://localhost:8000/docs

---

## Development Workflow

### 1. Find a Task

1. Browse `repo-tasks/` directory
2. Look for tasks with status "Planned" in current milestone
3. Check task dependencies
4. Read task objective and requirements

**Example task structure**:
```
# TASK ID: OME-001
## STATUS
Planned
## OBJECTIVE
Implement feature X
## REQUIREMENTS
- Requirement 1
- Requirement 2
```

### 2. Create a Feature Branch

```bash
# Create branch from latest main
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/TASK-ID-short-description
```

**Branch naming convention**:
- `feature/` - New features
- `fix/` - Bug fixes
- `refactor/` - Code refactoring
- `docs/` - Documentation
- `research/` - R&D work

### 3. Implement the Feature

#### Frontend (React)

```bash
cd frontend
npm install  # if needed
npm run dev
```

**Code style**:
- TypeScript strict mode
- ESLint configured
- Prettier for formatting
- Component-based architecture
- Props and hooks for state management

**File structure**:
```
src/
├── components/      # Reusable components
├── pages/          # Page components
├── hooks/          # Custom React hooks
├── services/       # API calls, utilities
├── styles/         # Global styles
└── types/          # TypeScript definitions
```

#### Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

**Code style**:
- Type hints required
- Pydantic models for validation
- Async/await for I/O
- Comprehensive docstrings
- Clear error handling

**File structure**:
```
backend/
├── main.py          # Application entry
├── models/          # Pydantic models
├── routes/          # API endpoints
├── services/        # Business logic
├── middleware/      # Request processing
└── tests/           # Unit tests
```

### 4. Test Your Changes

#### Frontend Testing

```bash
cd frontend
npm run type-check  # TypeScript check
npm run lint        # ESLint check
npm test            # Jest tests (if configured)
```

#### Backend Testing

```bash
cd backend
pytest               # Run tests
pytest -v           # Verbose output
pytest --cov        # Coverage report
```

#### Manual Testing

1. Test in browser for frontend changes
2. Test API endpoints in Swagger UI (`/docs`)
3. Verify error handling
4. Check performance with DevTools

### 5. Commit Your Changes

```bash
# Stage changes
git add .

# Commit with task reference
git commit -m "feat: Implement feature X (TASK-ID)

Description of changes:
- Change 1
- Change 2

Closes TASK-ID"
```

**Commit message format**:
- Type: feat, fix, refactor, docs, test, style
- Scope: optional, like (backend), (frontend)
- Subject: Clear, present tense
- Body: Details about the change
- Reference: Include task ID

### 6. Create a Pull Request

```bash
# Push your branch
git push origin feature/TASK-ID-description

# Create PR via GitHub web interface
```

**PR Template**:
```markdown
## Task
References TASK-ID

## Changes
- Change 1
- Change 2

## Testing
- [ ] Manual testing complete
- [ ] No regressions observed
- [ ] Error cases handled

## Documentation
- [ ] README updated (if needed)
- [ ] Code commented (if complex)
- [ ] Task status updated
```

### 7. Code Review

1. Address review comments
2. Make requested changes
3. Push updates to same branch
4. Respond to comments
5. Request re-review

### 8. Merge

Once approved:
1. Ensure all checks pass
2. Squash commits if needed (for clarity)
3. Merge to main branch
4. Delete feature branch
5. Update task status to "Completed"

---

## Code Standards

### TypeScript/JavaScript

```typescript
// Use strict types
interface User {
  id: string;
  name: string;
  email: string;
}

// Use const for immutability
const user: User = { id: '1', name: 'John', email: 'john@example.com' };

// Use async/await
async function fetchUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  return response.json();
}
```

### Python

```python
# Use type hints
from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id: str
    name: str
    email: str

# Use async functions
async def get_user(user_id: str) -> Optional[User]:
    result = await db.users.find_one({"id": user_id})
    return User(**result) if result else None

# Clear error handling
try:
    user = await get_user(user_id)
except Exception as e:
    logger.error(f"Failed to fetch user: {e}")
    raise HTTPException(status_code=500, detail="Internal server error")
```

### General Principles

1. **Clear naming**: Variables, functions, classes should be self-documenting
2. **Single responsibility**: Functions do one thing well
3. **DRY (Don't Repeat Yourself)**: Extract common patterns
4. **SOLID principles**: Apply where appropriate
5. **Error handling**: Explicit error messages and logging
6. **Documentation**: Code comments for "why", not "what"
7. **Testing**: Unit tests for critical logic

---

## Git Workflow

### Keeping Your Branch Updated

```bash
# Fetch latest changes
git fetch origin

# Rebase on main (preferred over merge)
git rebase origin/main

# If conflicts, resolve then:
git rebase --continue
```

### Interactive Rebase

```bash
# Squash commits before PR
git rebase -i origin/main

# Mark commits as 'squash' to combine
# or 'reword' to change messages
```

### Stashing Changes

```bash
# Save work temporarily
git stash

# List stashes
git stash list

# Apply stash
git stash pop
```

---

## Task Management

### Updating Task Status

1. Open task file (e.g., `repo-tasks/features/F1-TASK-NAME.md`)
2. Update STATUS field:
   ```markdown
   ## STATUS
   In Progress
   ```
3. Commit change in same PR as implementation
4. Close task when merged

**Status values**:
- Planned
- Researching
- In Progress
- Testing
- Optimizing
- Blocked
- Completed

### Tracking Progress

1. Update task file with implementation notes
2. Link to PR in task description
3. Document any blockers
4. Update completion percentage

---

## Documentation

### Code Comments

Good comments explain **why**, not **what**:

```typescript
// Bad: Explains what the code does
const x = user.age >= 18;

// Good: Explains why
// Users must be 18+ to accept terms of service
const isEligibleForTerms = user.age >= 18;
```

### Function Documentation

```typescript
/**
 * Validates user email format
 * @param email - Email to validate
 * @returns true if valid email format
 */
function validateEmail(email: string): boolean {
  // Implementation
}
```

### API Documentation

FastAPI auto-generates docs from docstrings:

```python
@app.get("/users/{user_id}")
async def get_user(user_id: str) -> User:
    """
    Get user by ID
    
    Args:
        user_id: The ID of the user to retrieve
        
    Returns:
        User object with all fields
        
    Raises:
        HTTPException: If user not found (404)
    """
```

### Task Documentation

Update task files as you work:

```markdown
## OBJECTIVE
[Original objective]

## PROGRESS
- [x] Subtask 1
- [x] Subtask 2
- [ ] Subtask 3

## NOTES
- Implementation detail 1
- Implementation detail 2
- PR: #123
```

---

## Debugging

### Frontend Debugging

1. **Browser DevTools**
   - Console tab for errors
   - Network tab for API calls
   - React DevTools extension

2. **VS Code Debugging**
   ```json
   {
     "version": "0.2.0",
     "configurations": [
       {
         "type": "chrome",
         "request": "launch",
         "name": "Launch Chrome",
         "url": "http://localhost:5173",
         "webRoot": "${workspaceFolder}/frontend"
       }
     ]
   }
   ```

### Backend Debugging

1. **Logging**
   ```python
   import logging
   logger = logging.getLogger(__name__)
   logger.debug(f"Debug info: {variable}")
   ```

2. **VS Code Debugging**
   ```json
   {
     "name": "Python: FastAPI",
     "type": "python",
     "request": "launch",
     "module": "uvicorn",
     "args": ["main:app", "--reload"],
     "jinja": true
   }
   ```

3. **API Debugging**
   - Use Swagger UI at `/docs`
   - Use ReDoc at `/redoc`
   - Use curl or Postman for manual tests

---

## Performance Optimization

### Frontend

- Use React DevTools Profiler
- Check bundle size with `npm run build`
- Lazy load pages with React.lazy
- Memoize expensive computations
- Optimize images and assets

### Backend

- Use FastAPI performance monitoring
- Profile with cProfile
- Monitor database query performance
- Implement caching strategies
- Use async for I/O operations

---

## Security Best Practices

### Secrets Management

Never commit secrets:
```bash
# Use environment variables
API_KEY=secret_key npm start

# Or .env.local (in .gitignore)
cat .env.local
```

### Input Validation

Always validate user input:
```typescript
// Frontend
if (!email.includes('@')) {
  setError('Invalid email');
  return;
}

// Backend
class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
```

### Authentication

- Never store passwords in plaintext
- Use HTTPS in production
- Implement CSRF protection
- Use secure cookies
- Validate tokens server-side

---

## Continuous Improvement

### Code Review Checklist

- [ ] Code is clear and well-structured
- [ ] Types are correct (TypeScript/Python)
- [ ] No hardcoded values
- [ ] Error handling is appropriate
- [ ] Tests cover key functionality
- [ ] No console.logs in production code
- [ ] Documentation is accurate
- [ ] No security issues

### Common Issues

**Issue**: Tests failing locally but passing in CI  
**Solution**: Ensure consistent test environment, check Node/Python versions

**Issue**: Merge conflicts  
**Solution**: Communicate with team, rebase strategically, use merge tools

**Issue**: Large PR hard to review  
**Solution**: Break into smaller PRs, rebase to clean up commit history

---

## Getting Help

1. **Documentation**: Check README.md and docs/ folder
2. **GitHub Issues**: Look for similar issues
3. **Team Communication**: Ask in Discord/discussions
4. **Code Comments**: Reference similar implementations
5. **Research Tasks**: Read relevant research in repo-tasks/research/

---

## Quick Commands

```bash
# Setup
git clone [repo] && cd Shanee-Intelligence-
docker-compose up

# Development
git checkout -b feature/name
# ... make changes ...
git commit -m "feat: description"
git push origin feature/name

# Cleanup
git remote prune origin    # Clean up remote branches
git gc                     # Garbage collection
git clean -fd              # Remove untracked files

# Debugging
docker-compose logs -f     # Stream logs
docker-compose restart     # Restart services
docker-compose down        # Stop services
```

---

**Last Updated**: 2024-05-29  
**Version**: 1.0
