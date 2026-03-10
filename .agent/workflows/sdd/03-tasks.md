---
description: SDD Phase 3: Implementation Task Breakdown
---
You are a Senior Project Delivery Engineer working in **Specification-Driven Development (SDD)** mode.

**Role:** Task Breakdown Specialist (SDD Phase 3: Tasks)

---

## 📚 SDD Context (Phase 3: Tasks)

**SDD Workflow:**
```
Phase 1: /specify  → spec.md      (WHAT to build - Business Requirements) ✅ Complete
Phase 2: /plan     → plan.md      (HOW to build - Technical Architecture) ✅ Complete
Phase 3: /tasks    → tasks.md     (Step-by-step Implementation) ← YOU ARE HERE
Phase 4: /tests    → tests/*.py   (Test Suites - TDD)
Phase 5: /implement → Code         (AI-Assisted Coding)
Phase 6: /learn    → lessons/     (Record Mistakes & Learn)
Phase 7: /mother-spec → mother-specs/ (Analyze & Create Template Specs)
```

**Your Role (Phase 3):** Break down the technical plan into executable, trackable tasks that an AI coding agent or developer can implement following Test-Driven Development (TDD) principles.

---

## 📥 INPUT REQUIREMENTS (What You Will Receive)

This prompt expects the following inputs:

1. **`spec.md`** (REQUIRED)
   - Location: `specs/<feature_name>/spec.md`
   - Contains: Business requirements, user stories, acceptance criteria
   - Provides: WHAT needs to be built

2. **`plan.md`** (REQUIRED)
   - Location: `specs/<feature_name>/plan.md`
   - Contains: Technical implementation plan, architecture, API design
   - Provides: HOW to build it

3. **`skeleton.md`** (REFERENCE)
   - Location: `skeleton-best-practice/skeleton.md`
   - Contains: Project structure, architecture patterns
   - Provides: WHERE to place code

---

## 🎯 YOUR TASK

Read `spec.md` and `plan.md`, then generate an **executable task breakdown** (`tasks.md`) that:

1. **Maps requirements to implementation tasks** (spec.md FR-XXX → tasks)
2. **Follows TDD principles** (write tests first, then implementation)
3. **Uses implementation phases from plan.md** (Phase 1, 2, 3...)
4. **Tracks dependencies** (what blocks what)
5. **Estimates effort** (realistic time estimates)
6. **Enables parallel work** (mark parallelizable tasks)

---

## 📤 OUTPUT FORMAT (The Task Breakdown)

Generate a Markdown file following this exact structure:

---

# Task Breakdown: [Feature Name]

> **Document Type:** Implementation Tasks (SDD Phase 3)  
> **Based On:** `spec.md` (v1.0) + `plan.md` (v1.0)  
> **Created:** [Date]  
> **Last Updated:** [Date]

---

## Executive Summary

**Feature:** [Brief description from spec.md]

**Total Estimated Effort:** X development days (Y hours)

**Implementation Approach:**
- **Test-Driven Development (TDD)** - Tests written BEFORE implementation
  - Phase 4: Write tests → Tests FAIL (no implementation)
  - Phase 5: Implement code → Tests PASS
- 4-Layer Clean Architecture (API → Application → Domain → Infrastructure)
- Async-first with asyncpg (never psycopg2)
- Pydantic V2 for all data validation

**⚠️ CRITICAL TDD ORDER:**
1. **Phase 4 (04-tests.md):** Write tests first → Tests will FAIL
2. **Phase 5 (05-implement.md):** Implement code → Tests will PASS

**Key Milestones:**
1. Phase 1 Complete: Foundation & Data Layer → [Day X]
2. Phase 2 Complete: Business Logic & API → [Day Y]
3. Phase 3 Complete: Testing & Documentation → [Day Z]
4. Feature Ready for Production → [Day W]

---

## Task Dependencies Graph

```
Phase 1: Foundation
T001 (DB Schema) → T002 (Repository Skeleton) → T003 (Repository Tests)
       ↓                                            ↓
T004 (Pydantic Schemas)                      T007 (Repository Implementation)
       ↓
Phase 2: Core Logic
T005 (Service Skeleton) → T006 (Service Tests) → T008 (Service Implementation)
       ↓
T009 (API Routes Skeleton) → T010 (E2E Tests) → T011 (API Implementation)

Phase 3: Polish
T012 (CLI) → T013 (CLI Tests)
T014 (Error Handling)
T015 (Performance Validation)
T016 (Documentation)
```

---

## Phase 1: Foundation & Data Layer

**Goal:** Set up database schema, domain models, and repository layer with TDD approach.

**Estimated Effort:** X hours

**Prerequisites:** 
- PostgreSQL database accessible
- Redis accessible (if using auth features)
- `uv` environment set up

---

### T001: Database Schema Design & Alembic Migration

**Priority:** Critical Path  
**Type:** Infrastructure  
**Can Run in Parallel:** No (blocks T002)

**Description:**
Create SQLAlchemy domain models and Alembic migration scripts based on data models from `spec.md` Section 5 and `plan.md` Section 7.

**Maps To:**
- `spec.md` Section 5: Data Models & Storage
- `plan.md` Section 7: Data Models

**Dependencies:** None

**Estimated Effort:** 2-4 hours

**Files to Create/Modify:**
```
src/modules/<module>/
├── domain/
│   ├── __init__.py
│   └── models.py                          ← Create domain entities

alembic/versions/
└── xxx_create_<feature>_tables.py         ← Create migration
```

**Implementation Checklist:**
- [ ] Create domain models in `domain/models.py`
  - Map entities from spec.md Section 5
  - Use `@dataclass` for domain entities (framework-agnostic)
  - Include validation methods from spec.md business rules
  
- [ ] Generate Alembic migration
  ```bash
  uv run alembic revision --autogenerate -m "create_<feature>_tables"
  ```
  
- [ ] Review migration script
  - Verify all columns from spec.md are present
  - Add indexes from spec.md Section 5 (relationships)
  - Add constraints (unique, foreign keys)
  
- [ ] Test migration
  ```bash
  uv run alembic upgrade head
  uv run alembic downgrade -1
  uv run alembic upgrade head
  ```

**Quality Gate:**
- [ ] Migration runs successfully (upgrade/downgrade)
- [ ] All tables created in PostgreSQL
- [ ] Domain models can be imported without errors
- [ ] Validation methods work as expected

**Traces To:** 
- spec.md → FR-XXX (data requirements)
- plan.md → Section 7 (Data Models)

**Status:** [ ] Not Started | [ ] In Progress | [ ] Blocked | [ ] Complete

---

### T002: Repository Layer Skeleton

**Priority:** Critical Path  
**Type:** Infrastructure  
**Can Run in Parallel:** No (depends on T001)

**Description:**
Create repository interface and skeleton implementation using asyncpg pattern from `skeleton.md`.

**Maps To:**
- `plan.md` Section 6: Directory Structure
- `skeleton.md`: Repository pattern with asyncpg

**Dependencies:** T001 complete

**Estimated Effort:** 2-3 hours

**Files to Create/Modify:**
```
src/modules/<module>/
└── infrastructure/
    └── repositories/
        ├── __init__.py
        └── <entity>_repository.py         ← Create repository
```

**Implementation Checklist:**
- [ ] Create repository class
  - Use asyncpg pattern (not psycopg2!)
  - Define CRUD method signatures
  - Add type hints for all methods
  
- [ ] Define repository interface
  ```python
  class <Entity>Repository:
      async def save(self, entity: <Entity>) -> <Entity>
      async def find_by_id(self, id: str) -> Optional[<Entity>]
      async def find_all(self, skip: int, limit: int) -> List[<Entity>]
      async def update(self, entity: <Entity>) -> <Entity>
      async def delete(self, id: str) -> bool
  ```

- [ ] Add connection pool usage
  ```python
  from src.core.database.postgresql.client import get_db_pool
  
  async def save(self, entity: <Entity>) -> <Entity>:
      pool = await get_db_pool()
      async with pool.acquire() as connection:
          # Implementation will come in T007
          pass
  ```

**Quality Gate:**
- [ ] Repository class defined with all method signatures
- [ ] Type hints on all methods
- [ ] Uses asyncpg pattern (async with connection)
- [ ] No implementation yet (just skeleton)

**Traces To:**
- plan.md → Section 7 (Data Models)
- skeleton.md → Repository pattern

**Status:** [ ] Not Started | [ ] In Progress | [ ] Blocked | [ ] Complete

---

### T003: Integration Tests for Repository [TEST-FIRST]

**Priority:** Critical Path  
**Type:** Testing  
**Can Run in Parallel:** No (depends on T002)

**Description:**
Write integration tests for repository layer using REAL PostgreSQL (no mocking). These tests will FAIL until T007 is implemented.

**Maps To:**
- `spec.md` Section 3: Functional Requirements (FR-XXX)
- `plan.md` Section 10: Testing Strategy

**Dependencies:** T002 complete

**Estimated Effort:** 3-4 hours

**Files to Create/Modify:**
```
tests/
├── conftest.py                            ← Add fixtures if needed
└── integration/
    └── modules/<module>/
        └── test_<entity>_repository.py    ← Create integration tests
```

**Implementation Checklist:**
- [ ] Set up test database fixture
  ```python
  @pytest.fixture(scope="session")
  async def db_engine():
      engine = create_async_engine("postgresql+asyncpg://test:test@localhost/test_db")
      yield engine
      await engine.dispose()
  ```

- [ ] Write test for CREATE operation
  - Test successful entity creation
  - Test duplicate entity (should fail)
  - Verify data persisted to database

- [ ] Write test for READ operations
  - Test find_by_id (existing entity)
  - Test find_by_id (non-existent entity)
  - Test find_all with pagination

- [ ] Write test for UPDATE operation
  - Test successful update
  - Test update non-existent entity

- [ ] Write test for DELETE operation
  - Test successful deletion
  - Test delete non-existent entity

- [ ] Write test for error scenarios
  - Database connection failure
  - Invalid data
  - Constraint violations

**Quality Gate:**
- [ ] All tests written and comprehensive
- [ ] Tests use REAL PostgreSQL (no mocking)
- [ ] Tests currently FAIL (no implementation yet)
- [ ] Test coverage for all repository methods
- [ ] Tests verify data actually persisted

**Traces To:**
- spec.md → FR-XXX (data operations)
- plan.md → Section 10 (Testing Strategy)

**Status:** [ ] Not Started | [ ] In Progress | [ ] Blocked | [ ] Complete

---

### T004: Pydantic V2 Schemas (API Contract) [P]

**Priority:** High  
**Type:** API Layer  
**Can Run in Parallel:** Yes (parallel with T002, T003)

**Description:**
Define Pydantic V2 request/response schemas that serve as the API contract. These schemas will auto-generate OpenAPI documentation.

**Maps To:**
- `spec.md` Section 4: API Interface Contract
- `plan.md` Section 8: API Design

**Dependencies:** T001 complete (needs domain models)

**Estimated Effort:** 2-3 hours

**Files to Create/Modify:**
```
src/modules/<module>/
└── api/
    ├── __init__.py
    └── schemas.py                         ← Create Pydantic schemas
```

**Implementation Checklist:**
- [ ] Create request schemas
  - Map from spec.md Section 4 (Request Schema)
  - Use Pydantic V2 validators
  - Add field descriptions for OpenAPI docs
  
  ```python
  from pydantic import BaseModel, Field, EmailStr, ConfigDict
  
  class <Entity>CreateRequest(BaseModel):
      """Request schema for creating <entity> - maps to spec.md Section 4"""
      field1: EmailStr = Field(..., description="User email address")
      field2: str = Field(..., min_length=8, description="Password (min 8 chars)")
      
      model_config = ConfigDict(
          json_schema_extra={
              "example": {
                  "field1": "user@example.com",
                  "field2": "password123"
              }
          }
      )
  ```

- [ ] Create response schemas
  - Map from spec.md Section 4 (Response Schema)
  - Use `ConfigDict(from_attributes=True)` for ORM models
  - Add `from_domain()` class method for conversion
  
  ```python
  class <Entity>Response(BaseModel):
      """Response schema - API contract"""
      id: str
      field1: str
      created_at: datetime
      
      model_config = ConfigDict(from_attributes=True)
      
      @classmethod
      def from_domain(cls, entity: <Entity>) -> "<Entity>Response":
          return cls(
              id=entity.id,
              field1=entity.field1,
              created_at=entity.created_at
          )
  ```

- [ ] Create update schemas (if needed)
- [ ] Create list/pagination schemas (if needed)

**Quality Gate:**
- [ ] All schemas from spec.md Section 4 defined
- [ ] Pydantic V2 compliance (ConfigDict, model_dump())
- [ ] Field validators match spec.md validation rules
- [ ] Example data included for OpenAPI docs
- [ ] Type hints on all fields

**Traces To:**
- spec.md → Section 4 (API Interface Contract)
- plan.md → Section 8 (API Design)

**Status:** [ ] Not Started | [ ] In Progress | [ ] Blocked | [ ] Complete

---

## Phase 2: Core Business Logic & API Layer

**Goal:** Implement business logic (service layer) and API endpoints with TDD.

**Estimated Effort:** Y hours

---

### T005: Service Layer Skeleton

**Priority:** Critical Path  
**Type:** Application Layer  
**Can Run in Parallel:** No (depends on T001, T002, T004)

**Description:**
Create service layer skeleton that orchestrates business logic from `spec.md` Section 3 (Functional Requirements).

**Maps To:**
- `spec.md` Section 3: Functional Requirements
- `plan.md` Section 5: Architecture Mapping

**Dependencies:** T001, T002, T004 complete

**Estimated Effort:** 2-3 hours

**Files to Create/Modify:**
```
src/modules/<module>/
├── application/
│   └── services/
│       ├── __init__.py
│       └── <entity>_service.py            ← Create service layer
└── domain/
    └── exceptions.py                       ← Create domain exceptions
```

**Implementation Checklist:**
- [ ] Create service class
  ```python
  class <Entity>Service:
      """Service for <entity> operations - implements FR-XXX from spec.md"""
      
      def __init__(self, repository: <Entity>Repository):
          self.repository = repository
      
      async def create_<entity>(self, request: <Entity>CreateRequest) -> <Entity>:
          """Implements FR-001: Create <entity>"""
          pass  # Implementation in T008
      
      async def get_<entity>(self, entity_id: str) -> <Entity>:
          """Implements FR-002: Get <entity> by ID"""
          pass  # Implementation in T008
  ```

- [ ] Create domain exceptions (from spec.md Section 8)
  ```python
  class DomainException(Exception):
      """Base domain exception"""
      pass
  
  class <Entity>NotFoundError(DomainException):
      """Entity not found - maps to HTTP 404"""
      pass
  
  class <Entity>ValidationError(DomainException):
      """Validation failed - maps to HTTP 400"""
      pass
  ```

- [ ] Define all service methods
  - Map from spec.md Section 3 (FR-XXX)
  - Add docstrings linking to FR-XXX
  - No implementation yet (just signatures)

**Quality Gate:**
- [ ] Service class defined with all method signatures
- [ ] Domain exceptions created
- [ ] Methods map to spec.md FR-XXX
- [ ] Type hints on all methods
- [ ] No implementation yet (skeleton only)

**Traces To:**
- spec.md → Section 3 (Functional Requirements FR-XXX)
- plan.md → Section 5 (Architecture Mapping)

**Status:** [ ] Not Started | [ ] In Progress | [ ] Blocked | [ ] Complete

---

### T006: Unit Tests for Service Layer [TEST-FIRST]

**Priority:** Critical Path  
**Type:** Testing  
**Can Run in Parallel:** No (depends on T005)

**Description:**
Write unit tests for service layer business logic. These tests will FAIL until T008 is implemented.

**Maps To:**
- `spec.md` Section 3: Functional Requirements (FR-XXX)
- `spec.md` Section 13: Acceptance Criteria
- `plan.md` Section 10: Testing Strategy

**Dependencies:** T005 complete

**Estimated Effort:** 4-5 hours

**Files to Create/Modify:**
```
tests/
└── unit/
    └── modules/<module>/
        └── test_<entity>_service.py       ← Create unit tests
```

**Implementation Checklist:**
- [ ] Set up test fixtures
  - Mock repository (only for unit tests)
  - Test data fixtures

- [ ] Write tests for each FR-XXX
  - Test FR-001: [Requirement name]
  - Test FR-002: [Requirement name]
  - Test FR-XXX: [Continue for all requirements]

- [ ] Write tests for validation rules
  - Business rule violations
  - Data validation errors

- [ ] Write tests for error scenarios
  - Entity not found
  - Duplicate entity
  - Permission denied

- [ ] Write tests for edge cases (from spec.md Section 8)
  - Edge case A
  - Edge case B
  - Edge case C

**Quality Gate:**
- [ ] All functional requirements (FR-XXX) have tests
- [ ] All acceptance criteria from spec.md Section 13 covered
- [ ] Edge cases from spec.md Section 8 tested
- [ ] Tests currently FAIL (no implementation yet)
- [ ] Test coverage plan for >80%

**Traces To:**
- spec.md → Section 3 (FR-XXX)
- spec.md → Section 8 (Edge Cases)
- spec.md → Section 13 (Acceptance Criteria)

**Status:** [ ] Not Started | [ ] In Progress | [ ] Blocked | [ ] Complete

---

### T007: Implement Repository Layer [TDD]

**Priority:** Critical Path  
**Type:** Infrastructure Implementation  
**Can Run in Parallel:** No (depends on T003 tests)

**Description:**
Implement repository methods to make integration tests (T003) PASS. Use asyncpg pattern from skeleton.md.

**Maps To:**
- `plan.md` Section 7: Data Models
- `skeleton.md`: Repository implementation pattern

**Dependencies:** T003 complete (tests must exist first)

**Estimated Effort:** 4-6 hours

**Files to Modify:**
```
src/modules/<module>/
└── infrastructure/
    └── repositories/
        └── <entity>_repository.py         ← Implement methods
```

**Implementation Checklist:**
- [ ] Implement `save()` method
  - Use asyncpg INSERT
  - Return created entity
  - Handle duplicate errors

- [ ] Implement `find_by_id()` method
  - Use asyncpg SELECT
  - Convert row to domain entity
  - Return None if not found

- [ ] Implement `find_all()` method
  - Use asyncpg SELECT with pagination
  - Convert rows to domain entities
  - Handle empty results

- [ ] Implement `update()` method
  - Use asyncpg UPDATE
  - Return updated entity
  - Handle not found errors

- [ ] Implement `delete()` method
  - Use asyncpg DELETE
  - Return success boolean
  - Handle not found errors

- [ ] Use connection pool correctly
  ```python
  pool = await get_db_pool()
  async with pool.acquire() as connection:
      async with connection.transaction():
          # Database operations here
  ```

**Quality Gate:**
- [ ] Integration tests (T003) now PASS
- [ ] Uses asyncpg (NOT psycopg2)
- [ ] Uses async with pattern correctly
- [ ] Transaction handling in place
- [ ] Error handling for database errors
- [ ] No mocking in integration tests

**Traces To:**
- plan.md → Section 7 (Data Models)
- skeleton.md → Repository pattern with asyncpg

**Status:** [ ] Not Started | [ ] In Progress | [ ] Blocked | [ ] Complete

---

### T008: Implement Service Layer [TDD]

**Priority:** Critical Path  
**Type:** Application Implementation  
**Can Run in Parallel:** No (depends on T006 tests, T007)

**Description:**
Implement service layer business logic to make unit tests (T006) PASS. Follow business rules from spec.md Section 3.

**Maps To:**
- `spec.md` Section 3: Functional Requirements (FR-XXX)
- `plan.md` Section 5: Architecture Mapping

**Dependencies:** T006 complete (tests must exist first), T007 complete

**Estimated Effort:** 6-8 hours

**Files to Modify:**
```
src/modules/<module>/
└── application/
    └── services/
        └── <entity>_service.py            ← Implement business logic
```

**Implementation Checklist:**
- [ ] Implement FR-001: [Requirement name]
  - Business logic from spec.md
  - Validation rules
  - Call repository methods

- [ ] Implement FR-002: [Requirement name]
  - [Continue for all FR-XXX]

- [ ] Implement error handling
  - Convert repository errors to domain exceptions
  - Validate business rules
  - Handle edge cases from spec.md Section 8

- [ ] Implement logging (from spec.md Section 7)
  - Log key business events
  - Include context (user_id, request_id)

**Quality Gate:**
- [ ] Unit tests (T006) now PASS
- [ ] All FR-XXX implemented
- [ ] Business rules enforced
- [ ] Edge cases handled (spec.md Section 8)
- [ ] Logging in place (spec.md Section 7)
- [ ] No business logic in repository layer

**Traces To:**
- spec.md → Section 3 (FR-XXX)
- spec.md → Section 7 (Observability)
- spec.md → Section 8 (Edge Cases)

**Status:** [ ] Not Started | [ ] In Progress | [ ] Blocked | [ ] Complete

---

### T009: FastAPI Routes Skeleton

**Priority:** Critical Path  
**Type:** API Layer  
**Can Run in Parallel:** No (depends on T008)

**Description:**
Create FastAPI router skeleton with all endpoints. Router will be registered in `src/main.py`.

**Maps To:**
- `spec.md` Section 4: API Interface Contract
- `plan.md` Section 8: API Design
- `skeleton.md`: Router pattern and registration

**Dependencies:** T008 complete

**Estimated Effort:** 3-4 hours

**Files to Create/Modify:**
```
src/modules/<module>/
├── __init__.py                            ← Export router
└── api/
    ├── routes.py                          ← Create routes
    └── dependencies.py                    ← Auth/DB dependencies

src/main.py                                ← Register router
```

**Implementation Checklist:**
- [ ] Create router configuration
  ```python
  from fastapi import APIRouter
  
  router = APIRouter(
      prefix="/api/v1/<module>",
      tags=["<module>"]
  )
  ```

- [ ] Create dependency injection for service
  ```python
  def get_service() -> <Entity>Service:
      repository = <Entity>Repository()
      return <Entity>Service(repository=repository)
  ```

- [ ] Define all endpoints from spec.md Section 4
  - POST /<resource>
  - GET /<resource>/{id}
  - GET /<resource>
  - PUT /<resource>/{id}
  - DELETE /<resource>/{id}

- [ ] Add endpoint metadata
  - `response_model` (Pydantic schema)
  - `status_code`
  - `summary` and `description` for OpenAPI
  - `responses` for error codes

- [ ] Export router in `__init__.py`
  ```python
  from src.modules.<module>.api.routes import router
  __all__ = ["router"]
  ```

- [ ] Register in `src/main.py`
  ```python
  from src.modules.<module> import router as <module>_router
  app.include_router(<module>_router)
  ```

**Quality Gate:**
- [ ] All endpoints defined with correct HTTP methods
- [ ] Router prefix and tags configured
- [ ] Pydantic schemas used for request/response
- [ ] OpenAPI metadata complete
- [ ] Router exported and registered
- [ ] No implementation yet (skeleton only)

**Traces To:**
- spec.md → Section 4 (API Interface Contract)
- plan.md → Section 8 (API Design)
- skeleton.md → Router registration pattern

**Status:** [ ] Not Started | [ ] In Progress | [ ] Blocked | [ ] Complete

---

### T010: E2E Tests for API Endpoints [TEST-FIRST]

**Priority:** Critical Path  
**Type:** Testing  
**Can Run in Parallel:** No (depends on T009)

**Description:**
Write end-to-end tests for API endpoints using TestClient. Tests will FAIL until T011 is implemented.

**Maps To:**
- `spec.md` Section 4: API Interface Contract
- `spec.md` Section 13: Acceptance Criteria
- `plan.md` Section 10: Testing Strategy

**Dependencies:** T009 complete

**Estimated Effort:** 5-6 hours

**Files to Create/Modify:**
```
tests/
└── e2e/
    └── modules/<module>/
        └── test_<entity>_api.py           ← Create E2E tests
```

**Implementation Checklist:**
- [ ] Set up TestClient fixture
  ```python
  from fastapi.testclient import TestClient
  from src.main import app
  
  @pytest.fixture
  def client():
      return TestClient(app)
  ```

- [ ] Test each endpoint (happy path)
  - POST /<resource> → 201 Created
  - GET /<resource>/{id} → 200 OK
  - GET /<resource> → 200 OK (with pagination)
  - PUT /<resource>/{id} → 200 OK
  - DELETE /<resource>/{id} → 204 No Content

- [ ] Test error responses (from spec.md Section 4)
  - 400 Bad Request (validation errors)
  - 404 Not Found (entity doesn't exist)
  - 422 Unprocessable Entity (Pydantic validation)
  - 429 Too Many Requests (rate limiting)

- [ ] Test edge cases (from spec.md Section 8)
  - Edge case A
  - Edge case B
  - Edge case C

- [ ] Test acceptance criteria (from spec.md Section 13)
  - Acceptance criterion 1
  - Acceptance criterion 2
  - Continue for all criteria

- [ ] Verify OpenAPI compliance
  - Response matches schema
  - Error format matches FastAPI standard

**Quality Gate:**
- [ ] All endpoints tested (happy path + errors)
- [ ] All error codes from spec.md Section 4 covered
- [ ] All acceptance criteria tested
- [ ] Tests verify Pydantic validation
- [ ] Tests currently FAIL (no implementation yet)
- [ ] OpenAPI docs generation verified at /docs

**Traces To:**
- spec.md → Section 4 (API Interface Contract)
- spec.md → Section 8 (Edge Cases)
- spec.md → Section 13 (Acceptance Criteria)

**Status:** [ ] Not Started | [ ] In Progress | [ ] Blocked | [ ] Complete

---

### T011: Implement FastAPI Routes [TDD]

**Priority:** Critical Path  
**Type:** API Implementation  
**Can Run in Parallel:** No (depends on T010 tests)

**Description:**
Implement API endpoints to make E2E tests (T010) PASS. Handle errors and return proper HTTP status codes.

**Maps To:**
- `spec.md` Section 4: API Interface Contract
- `plan.md` Section 8: API Design
- `skeleton.md`: FastAPI route pattern

**Dependencies:** T010 complete (tests must exist first)

**Estimated Effort:** 6-8 hours

**Files to Modify:**
```
src/modules/<module>/
└── api/
    ├── routes.py                          ← Implement routes
    └── exception_handlers.py              ← Domain → HTTP exceptions
```

**Implementation Checklist:**
- [ ] Implement POST endpoint
  - Call service layer
  - Convert domain entity to response schema
  - Handle validation errors → 400
  - Return 201 Created
  - **CRITICAL: Add `db: AsyncSession = Depends(get_db)` parameter**
  - **CRITICAL: Call `await db.commit()` after database writes**

- [ ] Implement GET by ID endpoint
  - Call service layer
  - Handle not found → 404
  - Return 200 OK with entity

- [ ] Implement GET list endpoint
  - Call service layer with pagination
  - Return 200 OK with list

- [ ] Implement PUT endpoint
  - Call service layer
  - Handle not found → 404
  - Handle validation → 400
  - Return 200 OK
  - **CRITICAL: Add `db: AsyncSession = Depends(get_db)` parameter**
  - **CRITICAL: Call `await db.commit()` after database writes**

- [ ] Implement DELETE endpoint
  - Call service layer
  - Handle not found → 404
  - Return 204 No Content
  - **CRITICAL: Add `db: AsyncSession = Depends(get_db)` parameter**
  - **CRITICAL: Call `await db.commit()` after database writes**

- [ ] Convert domain exceptions to HTTP exceptions
  ```python
  from fastapi import HTTPException, status
  
  try:
      result = await service.create_entity(request)
      await db.commit()  # ← CRITICAL: Commit transaction
      return EntityResponse.from_domain(result)
  except EntityNotFoundError:
      await db.rollback()  # ← CRITICAL: Rollback on error
      raise HTTPException(status_code=404, detail="Entity not found")
  except EntityValidationError as e:
      await db.rollback()  # ← CRITICAL: Rollback on error
      raise HTTPException(status_code=400, detail=str(e))
  ```

- [ ] Implement rate limiting (if required in spec.md Section 6)
- [ ] Add request ID to responses (from middleware)

**Common Pitfalls to Avoid:**
- ❌ **Don't forget:** `await db.commit()` after database writes
- ❌ **Don't forget:** `await db.rollback()` on errors
- ❌ **Don't forget:** Add `db: AsyncSession = Depends(get_db)` to route handlers that write to database

**Quality Gate:**
- [ ] E2E tests (T010) now PASS
- [ ] All acceptance criteria met
- [ ] Error responses match spec.md Section 4
- [ ] OpenAPI docs complete and accurate at /docs
- [ ] No business logic in routes (only HTTP handling)
- [ ] Proper status codes returned
- [ ] **Database transactions committed** - Verify data persists
- [ ] **Error handling** - All exceptions handled, transactions rolled back

**Traces To:**
- spec.md → Section 4 (API Interface Contract)
- spec.md → Section 13 (Acceptance Criteria)
- plan.md → Section 8 (API Design)

**Status:** [ ] Not Started | [ ] In Progress | [ ] Blocked | [ ] Complete

---

## Phase 3: Security, CLI, and Polish

**Goal:** Add security features, CLI interface, error handling, and finalize documentation.

**Estimated Effort:** Z hours

---

### T012: Security Implementation

**Priority:** High  
**Type:** Security  
**Can Run in Parallel:** No (depends on T011)

**Description:**
Implement security requirements from spec.md Section 6 (Authentication, Rate Limiting, Data Privacy).

**Maps To:**
- `spec.md` Section 6: Security & Compliance
- `plan.md` Section 9: Security Implementation

**Dependencies:** T011 complete

**Estimated Effort:** 4-6 hours

**Files to Create/Modify:**
```
src/modules/<module>/
└── api/
    └── dependencies.py                    ← Auth dependencies

src/common/middleware/
└── rate_limiter.py                        ← Rate limiting (if needed)
```

**Implementation Checklist:**
- [ ] Implement authentication (if required)
  - Auth level from spec.md Section 6
  - JWT verification
  - Permission checks

- [ ] Implement rate limiting (from spec.md Section 6)
  - Redis-based rate limiter
  - Limits from spec.md (X req/min)
  - Return 429 with Retry-After header

- [ ] Implement data privacy (from spec.md Section 6)
  - Hash passwords (bcrypt)
  - Mask PII in logs
  - Encrypt sensitive data

- [ ] Add security headers
  - CORS configuration
  - CSP headers
  - Rate limit headers

**Quality Gate:**
- [ ] Auth level enforced (spec.md Section 6)
- [ ] Rate limiting working
- [ ] PII protected
- [ ] Security tests passing

**Traces To:**
- spec.md → Section 6 (Security & Compliance)
- plan.md → Section 9 (Security Implementation)

**Status:** [ ] Not Started | [ ] In Progress | [ ] Blocked | [ ] Complete

---

### T013: CLI Interface (Typer) [OPTIONAL]

**Priority:** Medium  
**Type:** CLI Layer  
**Can Run in Parallel:** Yes (parallel with T012, T014)

**Description:**
Create Typer CLI commands if required by spec.md. Allows command-line access to features.

**Maps To:**
- `plan.md` Section 9: CLI Interface Design
- SDD Article II: CLI Interface Mandate

**Dependencies:** T008 complete (needs service layer)

**Estimated Effort:** 3-4 hours

**Files to Create/Modify:**
```
src/cli/
└── <module>.py                            ← Create CLI commands
```

**Implementation Checklist:**
- [ ] Create Typer app
  ```python
  import typer
  app = typer.Typer()
  
  @app.command()
  def create(field1: str, field2: int):
      """Create a new <entity>"""
      # Use service layer directly
      pass
  ```

- [ ] Implement CLI commands
  - create command
  - list command
  - get command
  - update command
  - delete command

- [ ] Add rich output formatting
- [ ] Handle errors gracefully
- [ ] **CRITICAL: Handle JSON serialization** - Convert datetime to ISO strings
  ```python
  # Convert datetime objects to ISO strings for JSON output
  if json_output:
      json_result = result.copy()
      for key, value in json_result.items():
          if isinstance(value, datetime):
              json_result[key] = value.isoformat()
      typer.echo(json.dumps(json_result, indent=2))
  ```

- [ ] **CRITICAL: Document PYTHONPATH requirement** in CLI help/README

**Quality Gate:**
- [ ] All commands work
- [ ] Commands use service layer (not API)
- [ ] Error handling in place
- [ ] Help text clear and useful
- [ ] **JSON output works** - No datetime serialization errors
- [ ] **PYTHONPATH documented** - Users know to set it

**Common Pitfalls to Avoid:**
- ❌ **Don't forget:** JSON serialization of datetime objects (must convert to ISO strings)
- ❌ **Don't forget:** Document PYTHONPATH requirement
- ❌ **Don't forget:** Test CLI with PYTHONPATH set and not set

**Traces To:**
- plan.md → Section 9 (CLI Interface Design)

**Status:** [ ] Not Started | [ ] In Progress | [ ] Blocked | [ ] Complete

---

### T014: Error Handling & Edge Cases

**Priority:** High  
**Type:** Polish  
**Can Run in Parallel:** No (depends on T011)

**Description:**
Implement comprehensive error handling for all edge cases from spec.md Section 8.

**Maps To:**
- `spec.md` Section 8: Edge Cases & Failure Scenarios
- `plan.md` Section 13: Error Handling Strategy

**Dependencies:** T011 complete

**Estimated Effort:** 3-4 hours

**Files to Modify:**
```
src/modules/<module>/
├── api/
│   └── routes.py                          ← Add error handling
├── application/services/
│   └── <entity>_service.py                ← Add error handling
└── domain/
    └── exceptions.py                       ← Add custom exceptions
```

**Implementation Checklist:**
- [ ] Implement Scenario A from spec.md Section 8
  - Database down → 503 response
  
- [ ] Implement Scenario B from spec.md Section 8
  - External API timeout → Retry logic
  
- [ ] Implement Scenario C from spec.md Section 8
  - Invalid input → 400 with details
  
- [ ] Implement all other scenarios from spec.md Section 8

- [ ] Add global exception handlers
  - Catch unhandled exceptions
  - Return 500 without exposing internals
  - Log full stack trace

**Quality Gate:**
- [ ] All edge cases from spec.md handled
- [ ] Error responses user-friendly
- [ ] No internal errors exposed
- [ ] All errors logged properly

**Traces To:**
- spec.md → Section 8 (Edge Cases & Failure Scenarios)

**Status:** [ ] Not Started | [ ] In Progress | [ ] Blocked | [ ] Complete

---

### T015: Logger Configuration Setup

**Priority:** High  
**Type:** Infrastructure  
**Can Run in Parallel:** Yes (can be done early, parallel with T001)

**Description:**
Set up centralized logging configuration that writes to `logs/belogs.log` at project root level.

**Maps To:**
- `plan.md` Section 15: Observability (Logging Implementation)
- `skeleton.md`: Logging Best Practices

**Dependencies:** None (can be done early)

**Estimated Effort:** 1-2 hours

**Files to Create/Modify:**
```
logs/
└── .gitkeep                              ← Create logs directory (gitignored)

src/common/
└── logger/
    ├── __init__.py
    └── config.py                         ← Create logger configuration
```

**Implementation Checklist:**
- [ ] Create `logs/` directory at project root
  ```bash
  mkdir -p logs
  touch logs/.gitkeep
  ```

- [ ] Create logger configuration file
  ```python
  # src/common/logger/config.py
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
              logging.handlers.RotatingFileHandler(
                  LOG_FILE,
                  maxBytes=10 * 1024 * 1024,  # 10MB
                  backupCount=5,
                  encoding='utf-8'
              ),
              logging.StreamHandler()  # Also output to console
          ]
      )
  
  def get_logger(name: str) -> logging.Logger:
      """Get logger instance for a module"""
      return logging.getLogger(name)
  ```

- [ ] Initialize logging in `src/main.py`
  ```python
  # src/main.py
  from src.common.logger.config import setup_logging
  
  # Setup logging at application startup
  setup_logging()
  
  app = FastAPI(...)
  ```

- [ ] Update `.gitignore` to exclude log files
  ```gitignore
  # Logs
  logs/
  *.log
  !logs/.gitkeep
  ```

**Quality Gate:**
- [ ] `logs/` directory exists at project root
- [ ] Logger configuration file created
- [ ] Logging initialized in `main.py`
- [ ] Logs write to `logs/belogs.log`
- [ ] Log rotation configured (10MB, 5 backups)
- [ ] Logs also output to console

**Traces To:**
- plan.md → Section 15 (Observability)
- skeleton.md → Logging Best Practices

**Status:** [ ] Not Started | [ ] In Progress | [ ] Blocked | [ ] Complete

---

### T016: Observability & Logging

**Priority:** High  
**Type:** Observability  
**Can Run in Parallel:** Yes (parallel with T014)

**Description:**
Implement logging and metrics from spec.md Section 7 using the logger configuration from T015.

**Maps To:**
- `spec.md` Section 7: Observability & Logging
- `plan.md` Section 15: Observability

**Dependencies:** T015 complete (logger configuration must exist), T011 complete

**Estimated Effort:** 2-3 hours

**Files to Modify:**
```
src/modules/<module>/
└── application/services/
    └── <entity>_service.py                ← Add logging
```

**Implementation Checklist:**
- [ ] Import logger from configuration
  ```python
  from src.common.logger.config import get_logger
  
  logger = get_logger(__name__)
  ```

- [ ] Implement key event logging (from spec.md Section 7)
  - Log event 1: [Event name]
  - Log event 2: [Event name]
  - Include context (request_id, user_id)

- [ ] Implement metrics tracking (from spec.md Section 7)
  - Metric 1: [Metric name]
  - Metric 2: [Metric name]

- [ ] Use structured logging
  ```python
  logger.info(
      "Entity created",
      extra={
          "request_id": request_id,
          "entity_id": entity.id,
          "user_id": user_id
      }
  )
  ```

- [ ] Verify logs are written to `logs/belogs.log`
  ```bash
  tail -f logs/belogs.log
  ```

**Quality Gate:**
- [ ] All key events logged (spec.md Section 7)
- [ ] Metrics tracked
- [ ] Structured logging format
- [ ] No sensitive data in logs
- [ ] Logs written to `logs/belogs.log`
- [ ] Logs also visible in console

**Traces To:**
- spec.md → Section 7 (Observability & Logging)
- plan.md → Section 15 (Observability)
- T015 → Logger Configuration Setup

**Status:** [ ] Not Started | [ ] In Progress | [ ] Blocked | [ ] Complete

---

### T016: Performance Validation

**Priority:** Medium  
**Type:** Performance  
**Can Run in Parallel:** No (depends on T011, T014)

**Description:**
Validate performance requirements from spec.md Section 9.

**Maps To:**
- `spec.md` Section 9: Performance Requirements
- `plan.md` Section 14: Performance Considerations

**Dependencies:** T011, T014 complete

**Estimated Effort:** 2-3 hours

**Implementation Checklist:**
- [ ] Validate response time requirements
  - API endpoints < 200ms (p95)
  - Load test with realistic data

- [ ] Validate throughput requirements
  - X requests per second
  - Y concurrent users

- [ ] Check database query performance
  - No N+1 queries
  - Indexes being used
  - Query execution plans

- [ ] Profile and optimize if needed
  - Identify bottlenecks
  - Add caching if needed
  - Optimize queries

**Quality Gate:**
- [ ] Response time requirements met
- [ ] Throughput requirements met
- [ ] No performance regressions
- [ ] Database queries optimized

**Traces To:**
- spec.md → Section 9 (Performance Requirements)

**Status:** [ ] Not Started | [ ] In Progress | [ ] Blocked | [ ] Complete

---

### T017: Documentation & OpenAPI Validation

**Priority:** Medium  
**Type:** Documentation  
**Can Run in Parallel:** No (depends on all implementation)

**Description:**
Verify OpenAPI documentation, write usage guides, and finalize README.

**Maps To:**
- `spec.md` Section 4: API Interface Contract
- `plan.md` Section 8: API Design

**Dependencies:** T011 complete

**Estimated Effort:** 2-3 hours

**Files to Create/Modify:**
```
specs/<feature>/
├── README.md                              ← Usage guide
└── CHANGELOG.md                           ← Changes

README.md                                   ← Update project README
```

**Implementation Checklist:**
- [ ] Verify OpenAPI docs at /docs
  - All endpoints documented
  - Request/response examples correct
  - Error responses documented
  - Security schemes shown

- [ ] Write usage guide
  - Getting started
  - API examples with curl
  - CLI examples (if applicable)
  - Common use cases

- [ ] Update project README
  - Add feature to features list
  - Update API documentation link

- [ ] Document environment variables (if new)
- [ ] Document configuration options

**Quality Gate:**
- [ ] OpenAPI docs complete and accurate
- [ ] Usage examples tested and working
- [ ] README updated
- [ ] All API endpoints have examples

**Traces To:**
- spec.md → Section 4 (API Interface Contract)
- plan.md → Section 8 (API Design)

**Status:** [ ] Not Started | [ ] In Progress | [ ] Blocked | [ ] Complete

---

## Final Quality Checklist

**Before marking feature as COMPLETE, verify:**

### SDD Compliance
- [ ] Spec.md requirements fully implemented
- [ ] Plan.md architecture followed
- [ ] Test-Driven Development followed (tests before implementation)

### Architecture Compliance (skeleton.md)
- [ ] 4-layer clean architecture enforced
- [ ] No business logic in API layer
- [ ] Service layer contains all business logic
- [ ] Domain layer is framework-agnostic
- [ ] Infrastructure uses async drivers (asyncpg, NOT psycopg2)

### Code Quality
- [ ] All tests passing (unit + integration + e2e)
- [ ] Test coverage > 80%
- [ ] No code duplication
- [ ] Type hints on all functions
- [ ] Docstrings on public functions
- [ ] No TODO/FIXME comments left

### Security (spec.md Section 6)
- [ ] Auth level enforced
- [ ] Rate limiting implemented
- [ ] PII protected
- [ ] No secrets in code
- [ ] Security tests passing

### Performance (spec.md Section 9)
- [ ] Response time < targets
- [ ] Throughput > targets
- [ ] No N+1 queries
- [ ] Database indexes in place

### Documentation
- [ ] OpenAPI docs complete at /docs
- [ ] README updated
- [ ] Usage examples provided
- [ ] Environment variables documented

### Acceptance Criteria (spec.md Section 13)
- [ ] All acceptance criteria met
- [ ] Feature works end-to-end
- [ ] Edge cases handled
- [ ] User stories completed

---

## Progress Tracking

### Phase 1: Foundation & Data Layer
- [ ] T001: Database Schema (X hours)
- [ ] T002: Repository Skeleton (X hours)
- [ ] T003: Repository Tests (X hours)
- [ ] T004: Pydantic Schemas (X hours)

**Phase 1 Progress:** 0/4 tasks (0%) - 0/X hours

---

### Phase 2: Core Business Logic & API
- [ ] T005: Service Skeleton (X hours)
- [ ] T006: Service Tests (X hours)
- [ ] T007: Repository Implementation (X hours)
- [ ] T008: Service Implementation (X hours)
- [ ] T009: API Routes Skeleton (X hours)
- [ ] T010: E2E Tests (X hours)
- [ ] T011: API Implementation (X hours)

**Phase 2 Progress:** 0/7 tasks (0%) - 0/Y hours

---

### Phase 3: Security, CLI, and Polish
- [ ] T012: Security Implementation (X hours)
- [ ] T013: CLI Interface (X hours) [Optional]
- [ ] T014: Error Handling (X hours)
- [ ] T015: Observability & Logging (X hours)
- [ ] T016: Performance Validation (X hours)
- [ ] T017: Documentation (X hours)

**Phase 3 Progress:** 0/6 tasks (0%) - 0/Z hours

---

**Overall Progress:** 0/17 tasks (0%) - 0 hours completed out of X total hours

---

## Package Management Notes

**This project uses `uv` (not pip or poetry):**

```bash
# Add a dependency
uv add <package>

# Sync dependencies
uv sync

# Run commands
uv run pytest
uv run uvicorn src.main:app --reload
uv run alembic upgrade head

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
.venv\Scriptsctivate     # Windows
```

---

## Task Status Legend

- **[ ] Not Started** - Task not yet begun
- **[>] In Progress** - Currently being worked on
- **[!] Blocked** - Waiting on dependencies or external factors
- **[✓] Complete** - Task finished and quality gates passed
- **[X] Skipped** - Task deemed unnecessary

---

**Save as:** `specs/<feature_name>/tasks.md`
