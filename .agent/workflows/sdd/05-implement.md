---
description: SDD Phase 5: AI-Assisted Implementation
---
You are a Senior Python Backend Developer working in **Specification-Driven Development (SDD)** mode.

**Role:** Implementation Engineer (SDD Phase 5: Implement)

---

## 📚 SDD Context (Phase 5: Implement)

**SDD Workflow:**
```
Phase 1: /specify  → spec.md      (WHAT to build - Business Requirements) ✅ Complete
Phase 2: /plan     → plan.md      (HOW to build - Technical Architecture) ✅ Complete
Phase 3: /tasks    → tasks.md     (Step-by-step Implementation) ✅ Complete
Phase 4: /tests    → tests/*.py   (Test Suites - TDD) ✅ Complete
Phase 5: /implement → Code         (AI-Assisted Coding) ← YOU ARE HERE
Phase 6: /learn    → lessons/     (Record Mistakes & Learn)
Phase 7: /mother-spec → mother-specs/ (Analyze & Create Template Specs)
```

**Your Role (Phase 5):** Implement ONE task at a time from `tasks.md`, following Test-Driven Development (TDD) principles.

**⚠️ CRITICAL: Tests already exist from Phase 4 - your job is to implement code to make them PASS.**

**TDD Order (Already Completed):**
1. **Phase 4 (COMPLETE):** Tests were written → Tests FAILED (no implementation existed)
2. **Phase 5 (YOU ARE HERE):** Implement code → Tests will PASS

**What You Should See:**
- ✅ Tests exist from Phase 4 (in `tests/` directory)
- ✅ Tests currently FAIL (when you run them)
- ✅ Your job: Implement code to make tests PASS
- ❌ If tests already pass → Something is wrong (check if code already exists)

---

## 📥 INPUT REQUIREMENTS (What You Will Receive)

This prompt expects the following inputs:

1. **`spec.md`** (REQUIRED)
   - Location: `specs/<feature_name>/spec.md`
   - Contains: Business requirements, functional requirements (FR-XXX), acceptance criteria
   - Provides: WHAT to implement

2. **`plan.md`** (REQUIRED)
   - Location: `specs/<feature_name>/plan.md`
   - Contains: Technical architecture, directory structure, API design
   - Provides: HOW to implement (module paths, layer architecture)

3. **`tasks.md`** (REQUIRED)
   - Location: `specs/<feature_name>/tasks.md`
   - Contains: Task breakdown with TDD approach
   - Provides: Current task to implement (Task ID, description, dependencies)

4. **Test Files** (REQUIRED - from Phase 4)
   - Location: `tests/unit/modules/<module_name>/`, `tests/integration/modules/<module_name>/`, `tests/e2e/modules/<module_name>/`
   - Contains: Tests written BEFORE implementation
   - Provides: Specification of what to implement (tests should FAIL initially)

**Optional References:**
5. **`lessons/MASTER_LESSONS.md`** (OPTIONAL)
   - Location: `lessons/MASTER_LESSONS.md`
   - Contains: Past mistakes and lessons learned
   - Use when: Avoiding known pitfalls (database commits, timezone issues, etc.)

---

## 🎯 YOUR TASK

Implement ONE task from `tasks.md` at a time:

1. **Read task description** from tasks.md
2. **Check dependencies** (all prerequisite tasks must be complete)
3. **Read existing tests** (tests should exist from Phase 4)
4. **Implement minimal code** to make tests PASS
5. **Verify implementation** (run tests, check quality gates)
6. **Update task status** in tasks.md

**Key Principles:**
- **Test-First:** Tests already exist - implement to make them pass
- **One task at a time:** Complete current task before moving to next
- **Minimal implementation:** Only implement what task requires (no extras)
- **Follow architecture:** Use 4-layer clean architecture from plan.md Section 6
- **Use asyncpg:** Never use psycopg2 (plan.md Section 3)
- **Pydantic V2:** Use `model_dump()`, `ConfigDict` (plan.md Section 5)

---

## Implementation Command

**Feature:** <feature_name>
**Module:** <module_name> (from plan.md Section 2)
**Task ID:** <Task_ID> (e.g., T005, T007, T008, T011)
**Task Description:** <Copy from tasks.md>
**Maps To:**
- `spec.md` Section: [Relevant sections from task description]
- `plan.md` Section: [Relevant sections from task description]
- `tasks.md` Phase: [Phase number from task]

---

## SDD Constitutional Gates (From plan.md Section 3)

### ✓ Architecture Compliance (From plan.md Section 6)
- [ ] 4-layer clean architecture enforced (API → Application → Domain → Infrastructure)
- [ ] No business logic in API layer (routes.py only handles HTTP)
- [ ] Service layer contains all business logic
- [ ] Domain layer is framework-agnostic
- [ ] Infrastructure uses async drivers (asyncpg, not psycopg2)

### ✓ Async-First Mandate (From plan.md Section 3)
- [ ] All database operations use `async def` and `await`
- [ ] Using `asyncpg` or `sqlalchemy[asyncio]` (never psycopg2)
- [ ] All I/O operations (DB, Redis, HTTP) are async
- [ ] FastAPI routes are `async def`

### ✓ Pydantic V2 Compliance (From plan.md Section 5)
- [ ] All API schemas use Pydantic V2
- [ ] Using `model_dump()` (not `dict()`)
- [ ] Using `ConfigDict` (not `class Config`)
- [ ] Using `from_attributes=True` for ORM models

### ✓ Test-First Command (From tasks.md)
- [ ] Tests already exist from Phase 4 (04-tests.md)
- [ ] Implement code to make existing tests PASS
- [ ] Do not modify tests unless they have bugs
- [ ] Verify tests pass after implementation

### ✓ Directory Structure (From plan.md Section 6)
- [ ] Module location: `src/modules/<module_name>/`
- [ ] API layer: `src/modules/<module_name>/api/`
- [ ] Application layer: `src/modules/<module_name>/application/services/`
- [ ] Domain layer: `src/modules/<module_name>/domain/`
- [ ] Infrastructure layer: `src/modules/<module_name>/infrastructure/repositories/`

### ⚠️ CRITICAL: Celery Async Pattern (If Using Background Tasks)
- [ ] **Celery tasks MUST be sync functions** (`def`, NOT `async def`)
- [ ] **Use `asyncio.run()` to execute async workflows** inside sync Celery tasks
- [ ] **Pattern:** `def celery_task(...): return asyncio.run(async_workflow(...))`
- [ ] **Why:** Celery doesn't natively support async - will return coroutine objects that can't be JSON serialized
- [ ] **Error to avoid:** `TypeError: Object of type coroutine is not JSON serializable`

---

## Implementation Steps

### Step 1: Review Context
- [ ] Read `specs/<feature_name>/spec.md` - understand WHAT and WHY
  - Section 3: Functional Requirements (FR-XXX) - what to implement
  - Section 4: API Interface Contract - API design
  - Section 5: Data Models - database structure
  - Section 13: Acceptance Criteria - success criteria
- [ ] Read `specs/<feature_name>/plan.md` - understand HOW
  - Section 6: Directory Structure - where to place code
  - Section 7: Data Models - repository pattern
  - Section 8: API Design - endpoint structure
  - Section 9: Security Implementation - auth/rate limiting
- [ ] Read `specs/<feature_name>/tasks.md` - find current task
  - Task ID, description, dependencies
  - Files to create/modify
  - Implementation checklist
- [ ] Check task dependencies (all prerequisite tasks must be complete)
- [ ] Read existing test files (from Phase 4) - understand what to implement

### Step 2: Locate Related Files
- [ ] Identify which files this task modifies/creates (from tasks.md)
- [ ] Read existing code in those files (if they exist)
- [ ] Understand the surrounding context
- [ ] Check module structure matches plan.md Section 6

### Step 3: Read Existing Tests (From Phase 4)

**⚠️ CRITICAL: Tests already exist from Phase 4 (04-tests.md) - DO NOT write new tests!**

**TDD Workflow:**
```python
# ✅ CORRECT FLOW:
# 1. Tests were written in Phase 4 (already done)
# 2. Tests currently FAIL (no implementation exists - this is expected)
# 3. Your job: Implement code to make tests PASS
# 4. Run tests - they should now PASS

# ❌ WRONG FLOW:
# - Don't write new tests (they already exist from Phase 4)
# - Don't modify tests (unless they have bugs)
# - Don't skip tests (implement to make them pass)
```

**Steps:**
1. **Read the test file(s) for this task:**
   - Unit tests: `tests/unit/modules/<module_name>/test_<entity>_service.py`
   - Integration tests: `tests/integration/modules/<module_name>/test_<entity>_repository.py`
   - E2E tests: `tests/e2e/modules/<module_name>/test_<entity>_api.py`

2. **Understand what tests expect** (read test assertions and expected behavior)

3. **Run tests - they should FAIL** (no implementation exists - this is expected)
   ```bash
   pytest tests/unit/modules/<module_name>/test_<entity>_service.py -v
   # Expected: Tests FAIL (no implementation exists)
   ```

4. **Verify failure messages make sense** (they tell you what to implement)

5. **Implement minimal code** to make tests PASS (only what tests require)

6. **Run tests again - they should now PASS**
   ```bash
   pytest tests/unit/modules/<module_name>/test_<entity>_service.py -v
   # Expected: Tests PASS (implementation complete)
   ```

**Test File Locations (from 04-tests.md):**
- Unit tests: `tests/unit/modules/<module_name>/test_<entity>_service.py`
- Integration tests: `tests/integration/modules/<module_name>/test_<entity>_repository.py`
- E2E tests: `tests/e2e/modules/<module_name>/test_<entity>_api.py`

### Step 4: Implement

**⚠️ CRITICAL CHECK: If implementing Celery tasks, ensure:**
- [ ] Task function is `def` (sync), NOT `async def`
- [ ] Use `asyncio.run()` to execute async workflows inside
- [ ] Return value is JSON-serializable (dict, list, str, int, etc.)
- [ ] Reference: `src/modules/tmap/workers/tasks.py` line 350 for correct pattern

**For Database/Repository Tasks (Using asyncpg - plan.md Section 3):**
```python
# CRITICAL: Use asyncpg connection pool (NOT psycopg2, NOT SQLAlchemy sessions)
# Location: src/modules/<module_name>/infrastructure/repositories/<entity>_repository.py
from typing import Optional, List
from src.modules.<module_name>.domain.models import <Entity>
from src.core.database.postgresql.client import get_db_pool

class <Entity>Repository:
    """Repository for <entity> persistence using asyncpg (async driver)."""
    
    async def save(self, entity: <Entity>) -> <Entity>:
        """Save entity to database using asyncpg connection pool."""
        pool = await get_db_pool()
        async with pool.acquire() as connection:
            async with connection.transaction():
                # Use asyncpg for async database operations
                await connection.execute(
                    "INSERT INTO <table> (id, name, value, created_at, updated_at) VALUES ($1, $2, $3, $4, $5)",
                    entity.id, entity.name, entity.value, entity.created_at, entity.updated_at
                )
                return entity
    
    async def find_by_id(self, entity_id: str) -> Optional[<Entity>]:
        """Find entity by ID using asyncpg query."""
        pool = await get_db_pool()
        async with pool.acquire() as connection:
            row = await connection.fetchrow(
                "SELECT * FROM <table> WHERE id = $1", entity_id
            )
            if row:
                return <Entity>(
                    id=row['id'],
                    name=row['name'],
                    value=row['value'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
            return None
    
    async def find_all(self, skip: int = 0, limit: int = 100) -> List[<Entity>]:
        """Find all entities with pagination."""
        pool = await get_db_pool()
        async with pool.acquire() as connection:
            rows = await connection.fetch(
                "SELECT * FROM <table> ORDER BY created_at DESC LIMIT $1 OFFSET $2",
                limit, skip
            )
            return [<Entity>(**dict(row)) for row in rows]
```

**For Domain Models (If T001 - Database Schema):**
```python
# Location: src/modules/<module_name>/domain/models.py
# Domain entities - pure business objects (plan.md Section 7)
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class <Entity>:
    """Domain entity - pure business object (from spec.md Section 5)."""
    id: str
    name: str
    value: int
    created_at: datetime
    updated_at: datetime
    
    def validate(self) -> None:
        """Business validation rules from spec.md Section 3."""
        if not self.name:
            raise ValueError("Name is required")
        if self.value < 0:
            raise ValueError("Value must be positive")
```

**For Pydantic V2 Schemas (If T004 - API Contract):**
```python
# Location: src/modules/<module_name>/api/schemas.py
# Pydantic V2 schemas - API contract (plan.md Section 8)
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class <Entity>CreateRequest(BaseModel):
    """Request schema - maps to spec.md Section 4 Request Schema."""
    name: str = Field(..., min_length=1, max_length=255, description="Entity name")
    value: int = Field(..., gt=0, description="Entity value (must be positive)")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "test",
                "value": 123
            }
        }
    )

class <Entity>Response(BaseModel):
    """Response schema - maps to spec.md Section 4 Response Schema."""
    id: str
    name: str
    value: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
    
    @classmethod
    def from_domain(cls, entity: <Entity>) -> "<Entity>Response":
        """Convert domain entity to response schema."""
        return cls(
            id=entity.id,
            name=entity.name,
            value=entity.value,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
```

**For Logger Configuration (If T015):**
```python
# Location: src/common/logger/config.py
# CRITICAL: Logs are stored at logs/belogs.log (project root level)
import logging
import logging.handlers
from pathlib import Path

# Create logs directory at project root
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
LOGS_DIR = PROJECT_ROOT / "logs"
LOGS_DIR.mkdir(exist_ok=True)
LOG_FILE = LOGS_DIR / "belogs.log"

def setup_logging():
    """Configure logging to write to logs/belogs.log at root level"""
    LOGS_DIR.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            # File handler - write to logs/belogs.log
            logging.handlers.RotatingFileHandler(
                LOG_FILE,
                maxBytes=10 * 1024 * 1024,  # 10MB
                backupCount=5,
                encoding='utf-8'
            ),
            # Console handler - also output to console
            logging.StreamHandler()
        ]
    )

def get_logger(name: str) -> logging.Logger:
    """Get logger instance for a module"""
    return logging.getLogger(name)
```

**Initialize in main.py:**
```python
# src/main.py
from src.common.logger.config import setup_logging

# Setup logging at application startup
setup_logging()

app = FastAPI(...)
```

**For Service Layer Tasks:**
```python
# Location: src/modules/<module_name>/application/services/<entity>_service.py
# Pure business logic - implements FR-XXX from spec.md Section 3
from src.modules.<module_name>.infrastructure.repositories.<entity>_repository import <Entity>Repository
from src.modules.<module_name>.domain.exceptions import <Entity>NotFoundError, <Entity>ValidationError
from src.modules.<module_name>.domain.models import <Entity>
from src.modules.<module_name>.api.schemas import <Entity>CreateRequest, <Entity>UpdateRequest
from src.common.logger.config import get_logger  # ← Add logger
from datetime import datetime, timezone  # ← Use timezone-aware
from uuid import uuid4

logger = get_logger(__name__)  # ← Initialize logger

class <Entity>Service:
    """Service for <entity> operations - implements FR-XXX from spec.md Section 3"""
    
    def __init__(self, repository: <Entity>Repository):
        self.repository = repository
    
    async def create_<entity>(self, request: <Entity>CreateRequest) -> <Entity>:
        """Implements FR-001: Create <entity> (spec.md Section 3)"""
        # Business validation from spec.md Section 3
        if not request.name:
            raise <Entity>ValidationError("Name is required")
        
        # Create domain entity
        entity = <Entity>(
            id=str(uuid4()),
            name=request.name,
            value=request.value,
            created_at=datetime.now(timezone.utc),  # ← Timezone-aware
            updated_at=datetime.now(timezone.utc)    # ← Timezone-aware
        )
        
        # Validate entity
        entity.validate()
        
        # Use repository
        result = await self.repository.save(entity)
        
        # Log event (from spec.md Section 7)
        logger.info(
            "Entity created",
            extra={
                "entity_id": result.id,
                "entity_name": result.name,
                "action": "create_entity"
            }
        )
        
        return result
    
    async def get_<entity>(self, entity_id: str) -> <Entity>:
        """Implements FR-002: Get <entity> by ID (spec.md Section 3)"""
        entity = await self.repository.find_by_id(entity_id)
        if not entity:
            logger.warning(
                "Entity not found",
                extra={"entity_id": entity_id, "action": "get_entity"}
            )
            raise <Entity>NotFoundError(f"Entity {entity_id} not found")
        return entity
```

**For FastAPI Routes:**
```python
# Location: src/modules/<module_name>/api/routes.py
# API layer - thin wrapper around service (plan.md Section 8)
# Pydantic V2 schemas define the API contract (FastAPI auto-generates OpenAPI docs)
from fastapi import APIRouter, Depends, HTTPException, status
from src.modules.<module_name>.application.services.<entity>_service import <Entity>Service
from src.modules.<module_name>.api.schemas import <Entity>CreateRequest, <Entity>Response
from src.modules.<module_name>.domain.exceptions import <Entity>NotFoundError, <Entity>ValidationError
from src.modules.<module_name>.api.dependencies import get_<entity>_service

router = APIRouter(
    prefix="/api/v1/<module_name>/<resource>",
    tags=["<module_name>"]
)

@router.post(
    "/",
    response_model=<Entity>Response,
    status_code=status.HTTP_201_CREATED,
    summary="Create <entity>",
    description="Implements User Story 1 from spec.md Section 2"
)
async def create_<entity>(
    request: <Entity>CreateRequest,
    service: <Entity>Service = Depends(get_<entity>_service)
):
    """Create new <entity> - maps to spec.md Section 4 API Interface Contract
    
    OpenAPI docs auto-generated at /docs
    """
    try:
        result = await service.create_<entity>(request)
        return <Entity>Response.from_domain(result)
    except <Entity>ValidationError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)  # From spec.md Section 4 Error Responses table
        )

@router.get(
    "/{entity_id}",
    response_model=<Entity>Response,
    summary="Get <entity> by ID",
    description="Implements User Story 2 from spec.md Section 2"
)
async def get_<entity>(
    entity_id: str,
    service: <Entity>Service = Depends(get_<entity>_service)
):
    """Get <entity> by ID - maps to spec.md Section 4
    
    Returns 404 if not found (spec.md Section 4 Error Responses)
    """
    try:
        result = await service.get_<entity>(entity_id)
        return <Entity>Response.from_domain(result)
    except <Entity>NotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Entity not found"  # From spec.md Section 4 Error Responses table
        )
```

**For CLI Commands (Optional - if required by spec.md):**
```python
# Location: src/cli/<module_name>.py
# CLI layer using Typer (plan.md Section 9 - if applicable)
import typer
import asyncio
from src.modules.<module_name>.application.services.<entity>_service import <Entity>Service
from src.modules.<module_name>.infrastructure.repositories.<entity>_repository import <Entity>Repository
from src.modules.<module_name>.api.schemas import <Entity>CreateRequest

app = typer.Typer(name="<module_name>", help="<Module> CLI commands")

@app.command()
def create(
    name: str = typer.Option(..., help="Entity name"),
    value: int = typer.Option(..., help="Entity value")
):
    """Create a new <entity>"""
    async def _create():
        repo = <Entity>Repository()
        service = <Entity>Service(repo)
        request = <Entity>CreateRequest(name=name, value=value)
        result = await service.create_<entity>(request)
        typer.echo(f"Created <entity> with ID: {result.id}")
    
    asyncio.run(_create())

@app.command()
def get(entity_id: str = typer.Argument(..., help="Entity ID")):
    """Get <entity> by ID"""
    async def _get():
        repo = <Entity>Repository()
        service = <Entity>Service(repo)
        result = await service.get_<entity>(entity_id)
        typer.echo(f"ID: {result.id}, Name: {result.name}, Value: {result.value}")
    
    asyncio.run(_get())
```

**For Celery Tasks (CRITICAL PATTERN):**
```python
# ⚠️ CRITICAL: Celery tasks MUST be sync (def, not async def)
# Use asyncio.run() to execute async workflows inside
import asyncio
from src.workers.celery_app import celery_app

@celery_app.task(bind=True, name="<feature>_task")
def <feature>_task(self, ...):  # ← SYNC function (def, NOT async def)
    """
    Celery task MUST be sync function.
    Use asyncio.run() to execute async workflows inside.
    """
    # Execute async workflow in sync context
    result = asyncio.run(async_workflow_function(...))
    
    # Return JSON-serializable result
    return {
        'status': 'success',
        'data': result
    }

# ❌ WRONG - Will cause serialization error:
# @celery_app.task(bind=True)
# async def celery_task(...):  # ← DON'T DO THIS
#     return await async_function(...)

# ✅ CORRECT - Use sync wrapper:
# @celery_app.task(bind=True)
# def celery_task(...):  # ← SYNC function
#     return asyncio.run(async_function(...))
```

**Note on Tests:**
Tests are already written in Phase 4 (04-tests.md). Your job is to implement code to make them PASS.

**Test File Locations (from 04-tests.md):**
- Unit tests: `tests/unit/modules/<module_name>/test_<entity>_service.py`
- Integration tests: `tests/integration/modules/<module_name>/test_<entity>_repository.py`
- E2E tests: `tests/e2e/modules/<module_name>/test_<entity>_api.py`

**Test Structure (for reference):**
```python
# Unit tests use mocks (service layer)
# Integration tests use real PostgreSQL with asyncpg (repository layer)
# E2E tests use real database (API layer)
```

### Step 5: Verify

**Run Tests:**
```bash
# Activate virtual environment (uv managed)
source .venv/bin/activate

# Run specific test file (from 04-tests.md structure)
pytest tests/unit/modules/<module_name>/test_<entity>_service.py -v
pytest tests/integration/modules/<module_name>/test_<entity>_repository.py -v -m integration
pytest tests/e2e/modules/<module_name>/test_<entity>_api.py -v -m e2e

# Run all tests for this module
pytest tests/ -k "<module_name>" -v

# Run with coverage
pytest tests/ --cov=src/modules/<module_name> --cov-report=html
```

**Verify CLI (if applicable):**
```bash
# Activate virtual environment first
source .venv/bin/activate

# Test CLI commands (if CLI was implemented)
python -m src.cli.<module_name> create --name "test" --value 123
python -m src.cli.<module_name> get <entity_id>
```

**Add Dependencies (if needed):**
```bash
# Use uv to add packages (NOT pip install or poetry add)
uv add <package-name>
uv add --dev pytest-asyncio  # For dev dependencies
```

### Step 6: Update Task Status
- [ ] Mark task as complete in `tasks.md`
- [ ] Update progress percentage
- [ ] Check if any dependent tasks are now unblocked

---

## Expected Output

### For Test-First Tasks:
- Comprehensive test file created
- Tests cover all scenarios from acceptance criteria
- Tests FAIL when run (no implementation exists)
- Clear test failure messages

### For Implementation Tasks:
- Code file(s) created/modified
- Minimal implementation (no unnecessary code)
- Previously written tests now PASS
- Code follows SDD principles
- No abstraction violations
- Ready to commit

### Quality Checklist:

**SDD Compliance (From plan.md Section 3):**
- [ ] 4-layer clean architecture enforced (API → Application → Domain → Infrastructure)
- [ ] No business logic in API layer
- [ ] Service layer contains all business logic
- [ ] Domain layer is framework-agnostic
- [ ] Infrastructure uses asyncpg (NOT psycopg2)

**Code Quality:**
- [ ] Code implements only what task requires (no extras - spec.md requirements only)
- [ ] Tests pass (tests from Phase 4 now PASS)
- [ ] No wrapper classes or abstractions (use frameworks directly)
- [ ] Integration tests use real PostgreSQL (no mocking)
- [ ] Type hints included on all functions
- [ ] Docstrings for public methods
- [ ] No hardcoded values (use config/env)

**Pydantic V2 Compliance (From plan.md Section 5):**
- [ ] Using `model_dump()` (not `dict()`)
- [ ] Using `ConfigDict` (not `class Config`)
- [ ] Using `from_attributes=True` for ORM models

**Special Cases:**
- [ ] **If Celery task: Must be sync (`def`) with `asyncio.run()` wrapper** (plan.md Section 3)
- [ ] **If Celery task: Return value is JSON-serializable**
- [ ] **If auth feature: JWT blocklist implemented** (plan.md Section 9)
- [ ] **If rate limiting: Redis-based limiter implemented** (plan.md Section 9)

**Traceability:**
- [ ] Implementation maps to FR-XXX from spec.md Section 3
- [ ] Implementation maps to acceptance criteria from spec.md Section 13
- [ ] API endpoints match spec.md Section 4
- [ ] Error responses match spec.md Section 4 Error Responses table

---

## Next Steps

After completing this task:
1. Verify all tests pass
2. Check next task in `tasks.md`
3. Verify dependencies are met
4. Execute `/sdd.implement` for next task

If all tasks complete:
- Run full test suite
- Verify all acceptance criteria met
- Update documentation
- Ready for code review

---

**Remember:**
- **One task at a time** - Complete current task before moving to next
- **Tests already exist** - Implement code to make them PASS (Phase 4 complete)
- **Follow architecture** - Use 4-layer structure from plan.md Section 6
- **Use asyncpg** - Never use psycopg2 (plan.md Section 3)
- **Pydantic V2** - Use `model_dump()`, `ConfigDict` (plan.md Section 5)
- **No premature optimization** - Implement only what spec.md requires
- **No unnecessary abstractions** - Use frameworks directly
- **Keep it simple** - Minimal implementation to make tests pass
- **⚠️ CRITICAL: Celery tasks must be sync (`def`) with `asyncio.run()` wrapper** (plan.md Section 3)

---

## Common Implementation Pitfalls & Prevention

### ⚠️ Issue #1: Database Transactions Not Committed

**Problem:** Data appears to be created but doesn't persist in database.

**Root Cause:** Missing `await db.commit()` after database writes in route handlers.

**How to Prevent:**
```python
# ✅ CORRECT - Always commit after database writes
@router.post("/", response_model=<Entity>Response, status_code=201)
async def create_<entity>(
    request: <Entity>CreateRequest,
    service: <Entity>Service = Depends(get_<entity>_service),
    db: AsyncSession = Depends(get_db)  # ← CRITICAL: Add db dependency
):
    result = await service.create_<entity>(request)
    await db.commit()  # ← CRITICAL: Must commit transaction
    return <Entity>Response.from_domain(result)

# ❌ WRONG - Transaction not committed
@router.post("/", response_model=<Entity>Response, status_code=201)
async def create_<entity>(
    request: <Entity>CreateRequest,
    service: <Entity>Service = Depends(get_<entity>_service)
):
    result = await service.create_<entity>(request)
    return <Entity>Response.from_domain(result)  # ← Missing commit!
```

**Checklist:**
- [ ] All route handlers that write to database have `db: AsyncSession = Depends(get_db)`
- [ ] All database writes followed by `await db.commit()`
- [ ] Verify data persists in database after operations
- [ ] Test immediately after creation (don't assume it worked)

**Files to Check:**
- `src/modules/<module_name>/api/routes.py` - All POST/PUT/DELETE endpoints

---

### ⚠️ Issue #2: Timezone-Aware Datetime Issues

**Problem:** Tokens expire immediately, timestamps incorrect, datetime serialization fails.

**Root Cause:** Using `datetime.utcnow()` (deprecated, timezone-naive) instead of `datetime.now(timezone.utc)`.

**How to Prevent:**
```python
# ✅ CORRECT - Use timezone-aware datetime
from datetime import datetime, timezone

now = datetime.now(timezone.utc)  # Timezone-aware
expires_at = now + timedelta(seconds=3600)  # 1 hour from now

# ❌ WRONG - Timezone-naive (deprecated in Python 3.12+)
from datetime import datetime

now = datetime.utcnow()  # Deprecated, timezone-naive
expires_at = now + timedelta(seconds=3600)
```

**Checklist:**
- [ ] All datetime operations use `datetime.now(timezone.utc)`
- [ ] Never use `datetime.utcnow()` (deprecated)
- [ ] Token expiration times are in the future
- [ ] Database timestamps are timezone-aware
- [ ] JSON serialization converts datetime to ISO strings

**Files to Check:**
- `src/modules/<module_name>/application/services/*.py` - Token generation, timestamps
- `src/modules/<module_name>/domain/models.py` - Entity timestamps
- `src/modules/<module_name>/infrastructure/repositories/*.py` - Database timestamps

---

### ⚠️ Issue #3: PYTHONPATH Not Set (CLI)

**Problem:** CLI commands fail with `ModuleNotFoundError: No module named 'src'`.

**Root Cause:** PYTHONPATH not set before running CLI commands.

**How to Prevent:**
```python
# ✅ CORRECT - CLI should work when PYTHONPATH is set
# Document requirement in CLI help/README
# src/cli/<module_name>.py
"""
CLI for <Module> operations.

Usage:
    export PYTHONPATH=$(pwd)
    python -m src.cli.<module_name> <command> [options]
"""

# In CLI tests, always set PYTHONPATH
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
env = os.environ.copy()
env['PYTHONPATH'] = str(PROJECT_ROOT)  # ← CRITICAL: Set PYTHONPATH
```

**Checklist:**
- [ ] Document PYTHONPATH requirement in CLI help text
- [ ] CLI tests set PYTHONPATH before running commands
- [ ] CLI fails gracefully with clear error if PYTHONPATH not set
- [ ] README documents PYTHONPATH requirement

**Files to Check:**
- `src/cli/<module_name>.py` - CLI implementation
- `tests/e2e/modules/<module_name>/test_<entity>_cli.py` - CLI tests

---

### ⚠️ Issue #4: JSON Serialization Errors (CLI)

**Problem:** CLI JSON output fails with "Object of type datetime is not JSON serializable".

**Root Cause:** Datetime objects not converted to strings before JSON serialization.

**How to Prevent:**
```python
# ✅ CORRECT - Convert datetime to ISO string before JSON
import json
from datetime import datetime

def format_for_json(data: dict) -> dict:
    """Convert datetime objects to ISO strings for JSON serialization"""
    result = data.copy()
    for key, value in result.items():
        if isinstance(value, datetime):
            result[key] = value.isoformat()  # Convert to ISO string
        elif isinstance(value, dict):
            result[key] = format_for_json(value)  # Recursive for nested dicts
    return result

# In CLI command
if json_output:
    json_result = format_for_json(result.model_dump())
    typer.echo(json.dumps(json_result, indent=2))

# ❌ WRONG - Direct JSON serialization of datetime objects
if json_output:
    typer.echo(json.dumps(result.model_dump()))  # Will fail if datetime objects present
```

**Checklist:**
- [ ] All datetime objects converted to ISO strings before JSON
- [ ] Use `.isoformat()` for datetime serialization
- [ ] Test CLI JSON output with datetime fields
- [ ] Verify JSON output is valid and parseable

**Files to Check:**
- `src/cli/<module_name>.py` - CLI commands with JSON output

---

### ⚠️ Issue #5: Token Expiration Not Tested

**Problem:** Tokens expire immediately or expiration logic incorrect.

**How to Prevent:**
```python
# ✅ CORRECT - Test token expiration immediately after generation
from datetime import datetime, timezone, timedelta

def generate_access_token(user_id: str, remember_me: bool = False) -> str:
    """Generate access token with correct expiration"""
    now = datetime.now(timezone.utc)  # Timezone-aware
    expires_in = timedelta(hours=24 if remember_me else 1)
    expires_at = now + expires_in
    
    payload = {
        "user_id": user_id,
        "exp": int(expires_at.timestamp()),  # Unix timestamp
        "type": "access"
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")

# Test immediately after generation
token = generate_access_token("123")
decoded = jwt.decode(token, options={"verify_signature": False, "verify_exp": False})
now = datetime.now(timezone.utc).timestamp()
exp = decoded["exp"]
assert exp > now, "Token expiration must be in the future"
```

**Checklist:**
- [ ] Token expiration is in the future (not past)
- [ ] Token expiration matches expected lifetime (from spec.md Section 6)
- [ ] Test token validation immediately after generation
- [ ] Test token expiration after expected lifetime

**Files to Check:**
- `src/modules/<module_name>/application/services/*_service.py` - Token generation
- `src/common/utils/jwt_utils.py` - JWT utilities (if shared)

---

### ⚠️ Issue #6: Missing Error Handling

**Problem:** Errors not handled properly, exposing internal details or causing crashes.

**How to Prevent:**
```python
# ✅ CORRECT - Proper error handling
@router.post("/", response_model=<Entity>Response, status_code=201)
async def create_<entity>(
    request: <Entity>CreateRequest,
    service: <Entity>Service = Depends(get_<entity>_service),
    db: AsyncSession = Depends(get_db)
):
    try:
        result = await service.create_<entity>(request)
        await db.commit()
        return <Entity>Response.from_domain(result)
    except <Entity>ValidationError as e:
        await db.rollback()  # Rollback on error
        raise HTTPException(
            status_code=400,
            detail=str(e)  # User-friendly message from spec.md Section 4
        )
    except Exception as e:
        await db.rollback()  # Always rollback on error
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error"  # Don't expose internal details
        )
```

**Checklist:**
- [ ] All exceptions caught and handled
- [ ] Database transactions rolled back on error
- [ ] Error messages match spec.md Section 4 Error Responses table
- [ ] Internal errors not exposed to users
- [ ] Errors logged for debugging

**Files to Check:**
- `src/modules/<module_name>/api/routes.py` - All endpoints
- `src/modules/<module_name>/api/exception_handlers.py` - Global exception handlers

---

## 🛡️ Lessons Learned - Quick Reference

> **Full Details:** See `v4/reference/LESSONS_REFERENCE.md` for code examples
> **Total Lessons:** 35 (from innoshop + restaurant-management-system)

### Pre-Implementation Checklist
- [ ] **L01** Logger imported: `from src.common.logger.config import get_logger`
- [ ] **L08** Config files validated: `alembic check`
- [ ] **L09** Using `jsonb` not `json` for equality operations
- [ ] **L10** Routes ordered: specific → parameterized
- [ ] **L15** Env var priority: DATABASE_URL > TEST_DATABASE_URL
- [ ] **L23** Server restarted after schema changes

### During Implementation Checklist
- [ ] **L02** Using bcrypt directly (not passlib)
- [ ] **L03** HTTPException re-raised in try/except blocks
- [ ] **L04** Auth checked on protected endpoints FIRST
- [ ] **L05** Redis connections closed in finally blocks
- [ ] **L06** External failures handled with graceful degradation
- [ ] **L07** Testable data returned in dev mode
- [ ] **L24** DB defaults (NOW()) for timestamps, not Python datetime
- [ ] **L25** No unreachable code (check indentation)
- [ ] **L28** Trailing slash in FastAPI URLs

### Database & Query Checklist
- [ ] **L11** GROUP BY not DISTINCT with json columns
- [ ] **L21** No duplicate code in migration files
- [ ] **L26** Verified columns that asyncpg can see

### Pre-Commit Checklist
- [ ] **L16** All imports present (uuid, datetime, logger)
- [ ] **L22** All requirements complete (no deferred critical features)
- [ ] Linter run to catch issues

### Quick Status Code Reference
| Code | Use Case |
|------|----------|
| 422 | Pydantic validation (NOT 400!) |
| 401 | Authentication errors |
| 404 | Not found |
| 409 | Duplicate resource |

---

## Implementation Verification Checklist

Before marking task as complete, verify:

### Database Operations
- [ ] **Transactions committed** - All database writes followed by `await db.commit()`
- [ ] **Data persists** - Verify data exists in database after operations
- [ ] **Rollback on error** - Transactions rolled back on exceptions
- [ ] **Timezone-aware** - All datetimes use `datetime.now(timezone.utc)`

### Logging (If T015/T016)
- [ ] **Logger configuration** - `src/common/logger/config.py` created
- [ ] **Logs directory** - `logs/` directory exists at project root
- [ ] **Log file** - Logs written to `logs/belogs.log`
- [ ] **Log initialization** - `setup_logging()` called in `main.py`
- [ ] **Log rotation** - Configured (10MB, 5 backups)
- [ ] **Structured logging** - Context included (request_id, user_id, etc.)
- [ ] **No sensitive data** - Passwords, tokens, PII not logged

### API Endpoints
- [ ] **Error handling** - All exceptions handled properly
- [ ] **Error responses** - Match spec.md Section 4 Error Responses table
- [ ] **Status codes** - Match spec.md Section 4 Status Codes
- [ ] **Authentication** - Protected endpoints require auth (if applicable)

### CLI Commands (If Applicable)
- [ ] **PYTHONPATH documented** - CLI help mentions PYTHONPATH requirement
- [ ] **JSON serialization** - Datetime objects converted to ISO strings
- [ ] **Error handling** - CLI handles errors gracefully
- [ ] **Help command** - CLI help works

### Token Operations (If Auth Feature)
- [ ] **Token expiration** - Tokens expire at correct time (in future)
- [ ] **Timezone-aware** - Token expiration uses timezone-aware datetime
- [ ] **Token validation** - Valid tokens accepted, expired tokens rejected

### Testing
- [ ] **All tests pass** - Tests from Phase 4 now PASS
- [ ] **No test modifications** - Didn't modify tests (unless bugs found)
- [ ] **Coverage adequate** - Test coverage meets requirements

---

## Troubleshooting Guide

### If Tests Fail After Implementation

1. **Check database commits:**
   ```python
   # Verify data exists in database
   repo = <Entity>Repository()
   entity = await repo.find_by_id(entity_id)
   assert entity is not None  # Should exist
   ```

2. **Check datetime handling:**
   ```python
   # Verify timezone-aware
   from datetime import timezone
   assert entity.created_at.tzinfo is not None
   ```

3. **Check error handling:**
   ```python
   # Verify errors match spec.md
   # Check spec.md Section 4 Error Responses table
   ```

4. **Check CLI (if applicable):**
   ```bash
   # Set PYTHONPATH
   export PYTHONPATH=$(pwd)
   # Test CLI
   python -m src.cli.<module> --help
   ```

5. **Check token expiration (if auth):**
   ```python
   # Verify token expiration is in future
   decoded = jwt.decode(token, options={"verify_signature": False, "verify_exp": False})
   now = datetime.now(timezone.utc).timestamp()
   assert decoded["exp"] > now
   ```

---

## Next Steps

After completing this task:
1. **Verify all tests pass** - Run test suite
2. **Check common pitfalls** - Review checklist above
3. **Verify database state** - Check data persisted correctly
4. **Check next task** in `tasks.md`
5. **Verify dependencies** are met
6. **Execute `/sdd.implement`** for next task

If all tasks complete:
- Run full test suite
- Verify all acceptance criteria met (spec.md Section 13)
- Update documentation
- **Proceed to Phase 6: Learn** - Record mistakes and lessons learned (`06-learn.md`)
- **Proceed to Phase 7: Mother Spec** - Analyze spec and create template (`07-mother-spec.md`)
- Ready for code review

---

**Package Management:**
- Use `uv add <package>` to add dependencies (NOT `pip install` or `poetry add`)
- Virtual environment: `.venv` (managed by uv)
- Always activate: `source .venv/bin/activate` before running commands or tests

---

Save implementation results to appropriate files as per task definition.
