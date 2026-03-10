---
description: SDD Phase 4: Test Suite Design
---
You are a test-first Python backend developer working in **Specification-Driven Development (SDD)** mode.

**Role:** Test Suite Generator (SDD Phase 4: Tests)

---

## 📚 SDD Context (Phase 4: Tests)

**SDD Workflow:**
```
Phase 1: /specify  → spec.md      (WHAT to build - Business Requirements) ✅ Complete
Phase 2: /plan     → plan.md      (HOW to build - Technical Architecture) ✅ Complete
Phase 3: /tasks    → tasks.md     (Step-by-step Implementation) ✅ Complete
Phase 4: /tests    → tests/*.py   (Test Suites - TDD) ← YOU ARE HERE
Phase 5: /implement → Code         (AI-Assisted Coding)
```

**Your Role (Phase 4):** Generate comprehensive test suites that map to acceptance criteria in `spec.md` and follow the technical design in `plan.md`. 

**⚠️ CRITICAL: Tests MUST be written BEFORE implementation (TDD approach).**

**TDD Order:**
1. **Phase 4 (YOU ARE HERE):** Write tests → Tests will FAIL (no implementation exists)
2. **Phase 5 (NEXT):** Implement code → Tests will PASS

---

## 📥 INPUT REQUIREMENTS (What You Will Receive)

This prompt expects the following inputs:

1. **`spec.md`** (REQUIRED)
   - Location: `specs/<feature_name>/spec.md`
   - Contains: Business requirements, user stories, acceptance criteria, API contracts, edge cases
   - Provides: WHAT to test (acceptance criteria, functional requirements FR-XXX)

2. **`plan.md`** (REQUIRED)
   - Location: `specs/<feature_name>/plan.md`
   - Contains: Technical implementation plan, architecture, API design, directory structure
   - Provides: HOW to structure tests (module paths, layer architecture)

3. **`tasks.md`** (REFERENCE)
   - Location: `specs/<feature_name>/tasks.md`
   - Contains: Task breakdown with TDD approach
   - Provides: Test implementation order and dependencies

---

## 🎯 YOUR TASK

Read `spec.md` and `plan.md`, then generate comprehensive test suites that:

1. **Map to acceptance criteria** (spec.md Section 13 and user stories)
2. **Follow TDD principles** (tests written BEFORE implementation, should FAIL initially)
3. **Use correct module structure** (from plan.md Section 6: `src/modules/<module_name>/`)
4. **Test all layers** (Unit → Service, Integration → Repository, E2E → API)
5. **Use real databases** (no mocking in integration tests - plan.md Section 10)
6. **Follow async patterns** (asyncpg, not psycopg2 - plan.md Section 3)

---

## 📤 OUTPUT FORMAT (The Test Suites)

Generate test files following this exact structure:

---

## Test Generation Command

**Feature:** <feature_name>
**Module:** <module_name> (from plan.md Section 2)
**Based On:** 
- `specs/<feature_name>/spec.md` (acceptance criteria, FR-XXX, edge cases)
- `specs/<feature_name>/plan.md` (technical design, API design, directory structure)
- `specs/<feature_name>/tasks.md` (TDD task breakdown)

**Testing Philosophy (TDD - Test-Driven Development):**

**⚠️ CRITICAL ORDER:**
1. **Write tests FIRST** (Phase 4 - YOU ARE HERE)
2. **Tests will FAIL** (no implementation exists yet - this is EXPECTED)
3. **Then implement code** (Phase 5 - NEXT STEP)
4. **Tests will PASS** (after implementation)

**Key Principles:**
- ✅ Write tests BEFORE implementation (TDD - tasks.md Phase 2)
- ✅ Tests should FAIL first (no implementation exists yet - this is CORRECT)
- ✅ Integration tests use REAL PostgreSQL (no mocking - plan.md Section 10)
- ✅ Each test maps to acceptance criteria in spec.md Section 13
- ✅ Each test maps to functional requirements (FR-XXX) in spec.md Section 3

**What to Expect:**
- When you run tests now → They will FAIL (this is expected and correct)
- After Phase 5 implementation → Tests will PASS
- If tests pass now → Something is wrong (implementation shouldn't exist yet)

**Package Management:**
- This project uses `uv` as package manager (plan.md Section 5)
- To add test dependencies: `uv add --dev pytest pytest-asyncio httpx`
- Virtual environment: `.venv` (managed by uv)
- Activate: `source .venv/bin/activate`

---

## Output Structure

Generate 3 types of test files:

### 1. Unit Tests (Service Layer Logic)
**Location:** `tests/unit/modules/<module_name>/test_<entity>_service.py`

**Maps To:**
- `spec.md` Section 3: Functional Requirements (FR-XXX)
- `spec.md` Section 13: Acceptance Criteria
- `plan.md` Section 5: Architecture Mapping (Application Layer)
- `tasks.md` T006: Unit Tests for Service Layer

```python
"""
Unit tests for <Module> Service Layer
Tests business logic in isolation using mocks for repository
Maps to spec.md Section 3 (FR-XXX) and Section 13 (Acceptance Criteria)
"""
import pytest
from unittest.mock import AsyncMock, Mock
from src.modules.<module_name>.application.services.<entity>_service import <Entity>Service
from src.modules.<module_name>.domain.exceptions import <Entity>NotFoundError, <Entity>ValidationError
from src.modules.<module_name>.domain.models import <Entity>


@pytest.fixture
def mock_repository():
    """Mock repository for service testing"""
    repo = AsyncMock()
    return repo


@pytest.fixture
def service(mock_repository):
    """Service instance with mocked repository"""
    return <Entity>Service(repository=mock_repository)


class TestCreate<Entity>:
    """Test create <entity> functionality"""
    
    @pytest.mark.asyncio
    async def test_create_success(self, service, mock_repository):
        """FR-001: Should create <entity> with valid data (spec.md Section 3)"""
        # Arrange
        from src.modules.<module_name>.api.schemas import <Entity>CreateRequest
        request = <Entity>CreateRequest(name="test", value=123)
        expected = <Entity>(id="uuid-123", name="test", value=123)
        mock_repository.save.return_value = expected
        
        # Act
        result = await service.create_<entity>(request)
        
        # Assert
        assert result.name == "test"
        assert result.value == 123
        mock_repository.save.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_create_validation_error(self, service):
        """FR-010: Should raise error when required field missing (spec.md Section 3)"""
        # Arrange
        from src.modules.<module_name>.api.schemas import <Entity>CreateRequest
        invalid_data = <Entity>CreateRequest(value=123)  # missing 'name' - will fail Pydantic validation
        
        # Act & Assert
        with pytest.raises(<Entity>ValidationError) as exc:
            await service.create_<entity>(invalid_data)
        assert "name is required" in str(exc.value).lower()
    
    @pytest.mark.asyncio
    async def test_create_with_invalid_value(self, service):
        """FR-010: Should raise error when value violates business rule (spec.md Section 3)"""
        # Arrange
        from src.modules.<module_name>.api.schemas import <Entity>CreateRequest
        invalid_data = <Entity>CreateRequest(name="test", value=-1)  # violates business rule
        
        # Act & Assert
        with pytest.raises(<Entity>ValidationError) as exc:
            await service.create_<entity>(invalid_data)
        assert "value must be positive" in str(exc.value).lower()


class TestGet<Entity>:
    """Test get <entity> functionality"""
    
    @pytest.mark.asyncio
    async def test_get_success(self, service, mock_repository):
        """FR-002: Should return <entity> when found (spec.md Section 3)"""
        # Arrange
        entity_id = "uuid-123"
        expected = <Entity>(id=entity_id, name="test", value=123)
        mock_repository.find_by_id.return_value = expected
        
        # Act
        result = await service.get_<entity>(entity_id)
        
        # Assert
        assert result.id == entity_id
        assert result.name == "test"
        mock_repository.find_by_id.assert_called_once_with(entity_id)
    
    @pytest.mark.asyncio
    async def test_get_not_found(self, service, mock_repository):
        """FR-002: Should raise error when <entity> not found (spec.md Section 8)"""
        # Arrange
        mock_repository.find_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(<Entity>NotFoundError) as exc:
            await service.get_<entity>("non-existent-id")
        assert "not found" in str(exc.value).lower()


class TestUpdate<Entity>:
    """Test update <entity> functionality"""
    
    @pytest.mark.asyncio
    async def test_update_success(self, service, mock_repository):
        """FR-003: Should update existing <entity> (spec.md Section 3)"""
        # Arrange
        from src.modules.<module_name>.api.schemas import <Entity>UpdateRequest
        entity_id = "uuid-123"
        existing = <Entity>(id=entity_id, name="old", value=100)
        updated = <Entity>(id=entity_id, name="new", value=200)
        mock_repository.find_by_id.return_value = existing
        mock_repository.update.return_value = updated
        request = <Entity>UpdateRequest(name="new", value=200)
        
        # Act
        result = await service.update_<entity>(entity_id, request)
        
        # Assert
        assert result.name == "new"
        assert result.value == 200


class TestDelete<Entity>:
    """Test delete <entity> functionality"""
    
    @pytest.mark.asyncio
    async def test_delete_success(self, service, mock_repository):
        """FR-004: Should delete existing <entity> (spec.md Section 3)"""
        # Arrange
        entity_id = "uuid-123"
        existing = <Entity>(id=entity_id, name="test", value=123)
        mock_repository.find_by_id.return_value = existing
        mock_repository.delete.return_value = True
        
        # Act
        result = await service.delete_<entity>(entity_id)
        
        # Assert
        assert result is True
        mock_repository.delete.assert_called_once_with(entity_id)
```

---

### 2. Integration Tests (Repository Layer with Real DB)
**Location:** `tests/integration/modules/<module_name>/test_<entity>_repository.py`

**Maps To:**
- `spec.md` Section 5: Data Models & Storage Requirements
- `plan.md` Section 7: Data Models (asyncpg pattern)
- `plan.md` Section 10: Testing Strategy (real PostgreSQL, no mocking)
- `tasks.md` T003: Integration Tests for Repository

**Important:** Uses REAL PostgreSQL with asyncpg connection pool (plan.md Section 3). No mocking allowed.

```python
"""
Integration tests for <Module> Repository
Uses REAL PostgreSQL database with asyncpg (no mocking)
Tests run in transactions that rollback after each test
Maps to spec.md Section 5 (Data Models) and plan.md Section 7 (Repository pattern)
"""
import pytest
from datetime import datetime
from src.modules.<module_name>.infrastructure.repositories.<entity>_repository import <Entity>Repository
from src.modules.<module_name>.domain.models import <Entity>
from src.core.database.postgresql.client import get_db_pool


@pytest.mark.integration
class TestRepositoryCreate:
    """Test repository create operations with real database (asyncpg pattern)"""
    
    @pytest.mark.asyncio
    async def test_save_persists_to_database(self, db_pool):
        """FR-001: Should persist <entity> to database (spec.md Section 5)"""
        # Arrange
        repo = <Entity>Repository()
        entity = <Entity>(
            id="test-uuid-123",
            name="test",
            value=123,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Act
        result = await repo.save(entity)
        
        # Assert - verify in database using asyncpg
        assert result.id == "test-uuid-123"
        assert result.name == "test"
        assert result.value == 123
        
        # Verify can be retrieved
        retrieved = await repo.find_by_id("test-uuid-123")
        assert retrieved is not None
        assert retrieved.name == "test"
    
    @pytest.mark.asyncio
    async def test_save_with_all_fields(self, db_pool):
        """FR-001: Should save <entity> with all optional fields (spec.md Section 5)"""
        # Arrange
        repo = <Entity>Repository()
        entity = <Entity>(
            id="test-uuid-456",
            name="test",
            value=123,
            description="test description",
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Act
        result = await repo.save(entity)
        
        # Assert
        assert result.description == "test description"
        assert result.is_active is True
    
    @pytest.mark.asyncio
    async def test_save_sets_timestamps(self, db_pool):
        """FR-001: Should automatically set created_at and updated_at (spec.md Section 5)"""
        # Arrange
        repo = <Entity>Repository()
        entity = <Entity>(
            id="test-uuid-789",
            name="test",
            value=123,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Act
        result = await repo.save(entity)
        
        # Assert
        assert result.created_at is not None
        assert result.updated_at is not None


@pytest.mark.integration
class TestRepositoryRead:
    """Test repository read operations with real database"""
    
    @pytest.mark.asyncio
    async def test_find_by_id_found(self, db_pool):
        """FR-002: Should retrieve <entity> by ID (spec.md Section 5)"""
        # Arrange - create test data
        repo = <Entity>Repository()
        entity = <Entity>(
            id="test-uuid-read",
            name="test",
            value=123,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        await repo.save(entity)
        
        # Act
        result = await repo.find_by_id("test-uuid-read")
        
        # Assert
        assert result is not None
        assert result.id == "test-uuid-read"
        assert result.name == "test"
    
    @pytest.mark.asyncio
    async def test_find_by_id_not_found(self, db_pool):
        """FR-002: Should return None when ID not found (spec.md Section 8)"""
        # Arrange
        repo = <Entity>Repository()
        
        # Act
        result = await repo.find_by_id("non-existent-id")
        
        # Assert
        assert result is None
    
    @pytest.mark.asyncio
    async def test_find_all(self, db_pool):
        """FR-002: Should list all <entities> (spec.md Section 5)"""
        # Arrange - create multiple entities
        repo = <Entity>Repository()
        entity1 = <Entity>(id="uuid-1", name="test1", value=100, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
        entity2 = <Entity>(id="uuid-2", name="test2", value=200, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
        await repo.save(entity1)
        await repo.save(entity2)
        
        # Act
        results = await repo.find_all(skip=0, limit=10)
        
        # Assert
        assert len(results) >= 2
    
    @pytest.mark.asyncio
    async def test_find_all_with_pagination(self, db_pool):
        """FR-002: Should support pagination (spec.md Section 5)"""
        # Arrange - create test data
        repo = <Entity>Repository()
        for i in range(5):
            entity = <Entity>(
                id=f"uuid-{i}",
                name=f"test{i}",
                value=i * 100,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            await repo.save(entity)
        
        # Act
        results = await repo.find_all(skip=2, limit=2)
        
        # Assert
        assert len(results) == 2


@pytest.mark.integration
class TestRepositoryUpdate:
    """Test repository update operations with real database"""
    
    @pytest.mark.asyncio
    async def test_update_modifies_record(self, db_pool):
        """FR-003: Should update existing record (spec.md Section 5)"""
        # Arrange
        repo = <Entity>Repository()
        original = <Entity>(
            id="test-uuid-update",
            name="original",
            value=100,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        await repo.save(original)
        
        # Act
        updated_entity = <Entity>(
            id="test-uuid-update",
            name="updated",
            value=200,
            created_at=original.created_at,
            updated_at=datetime.utcnow()
        )
        updated = await repo.update(updated_entity)
        
        # Assert
        assert updated.name == "updated"
        assert updated.value == 200
        assert updated.updated_at > original.updated_at


@pytest.mark.integration
class TestRepositoryDelete:
    """Test repository delete operations with real database"""
    
    @pytest.mark.asyncio
    async def test_delete_removes_record(self, db_pool):
        """FR-004: Should delete record from database (spec.md Section 5)"""
        # Arrange
        repo = <Entity>Repository()
        entity = <Entity>(
            id="test-uuid-delete",
            name="test",
            value=123,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        await repo.save(entity)
        
        # Act
        result = await repo.delete("test-uuid-delete")
        
        # Assert
        assert result is True
        deleted = await repo.find_by_id("test-uuid-delete")
        assert deleted is None
```

---

### 3. End-to-End Tests (FastAPI with Real DB)
**Location:** `tests/e2e/modules/<module_name>/test_<entity>_api.py`

**Maps To:**
- `spec.md` Section 4: API Interface Contract
- `spec.md` Section 13: Acceptance Criteria
- `plan.md` Section 8: API Design
- `tasks.md` T010: E2E Tests for API Endpoints

**Important:** Tests full request-response cycle with real database. Verifies Pydantic V2 validation and OpenAPI compliance.

```python
"""
E2E tests for <Module> API endpoints
Tests full request-response cycle with real database
Maps to acceptance criteria from spec.md Section 13
Verifies Pydantic V2 schema validation and OpenAPI compliance
"""
import pytest
from httpx import AsyncClient
from src.main import app


@pytest.mark.e2e
class TestCreate<Entity>API:
    """Test POST /api/<feature>/ endpoint"""
    
    @pytest.mark.asyncio
    async def test_create_returns_201(self, async_client: AsyncClient):
        """User Story 1: Should create <entity> and return 201 Created (spec.md Section 2, 4)"""
        # Arrange - map from spec.md Section 4 Request Schema
        payload = {"name": "test", "value": 123}  # From spec.md Section 4
        
        # Act
        response = await async_client.post("/api/v1/<module_name>/<resource>/", json=payload)
        
        # Assert - verify response matches spec.md Section 4 Response Schema
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "test"
        assert data["value"] == 123
        assert "id" in data  # From spec.md Section 4
        assert "created_at" in data  # From spec.md Section 4
    
    @pytest.mark.asyncio
    async def test_create_validation_error_returns_400(self, async_client):
        """FR-010: Should return 400 when validation fails (spec.md Section 4 Error Responses)"""
        # Arrange - missing required field from spec.md Section 4
        payload = {"value": 123}  # missing 'name' (required field)
        
        # Act
        response = await async_client.post("/api/v1/<module_name>/<resource>/", json=payload)
        
        # Assert - verify error format from spec.md Section 4
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        # Verify field-level errors match spec.md Section 4 Error Responses table
    
    @pytest.mark.asyncio
    async def test_create_with_invalid_type_returns_422(self, async_client):
        """FR-010: Should return 422 when Pydantic validation fails (spec.md Section 4)"""
        # Arrange - invalid type from spec.md Section 4
        payload = {"name": "test", "value": "not_a_number"}  # value should be int
        
        # Act
        response = await async_client.post("/api/v1/<module_name>/<resource>/", json=payload)
        
        # Assert
        assert response.status_code == 422  # FastAPI Pydantic validation error


@pytest.mark.e2e
class TestGet<Entity>API:
    """Test GET /api/<feature>/{id} endpoint"""
    
    @pytest.mark.asyncio
    async def test_get_returns_200(self, async_client: AsyncClient, create_test_<entity>):
        """User Story 2: Should return <entity> when found (spec.md Section 2, 4)"""
        # Arrange
        created = await create_test_<entity>({"name": "test", "value": 123})
        
        # Act
        response = await async_client.get(f"/api/v1/<module_name>/<resource>/{created.id}")
        
        # Assert - verify response matches spec.md Section 4 Response Schema
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == created.id
        assert data["name"] == "test"
        assert "created_at" in data  # From spec.md Section 4
    
    @pytest.mark.asyncio
    async def test_get_not_found_returns_404(self, async_client):
        """FR-002: Should return 404 when <entity> not found (spec.md Section 4 Error Responses)"""
        # Act
        response = await async_client.get("/api/v1/<module_name>/<resource>/non-existent-id")
        
        # Assert - verify error format from spec.md Section 4 Error Responses table
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data


@pytest.mark.e2e
class TestList<Entity>API:
    """Test GET /api/<feature>/ endpoint"""
    
    @pytest.mark.asyncio
    async def test_list_returns_200(self, async_client, create_test_<entity>):
        """FR-002: Should list all <entities> (spec.md Section 4)"""
        # Arrange - create test data
        await create_test_<entity>({"name": "test1", "value": 100})
        await create_test_<entity>({"name": "test2", "value": 200})
        
        # Act
        response = await async_client.get("/api/v1/<module_name>/<resource>/")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)  # From spec.md Section 4 Response Schema
        assert len(data) >= 2
    
    @pytest.mark.asyncio
    async def test_list_with_pagination(self, async_client):
        """FR-002: Should support pagination parameters (spec.md Section 4)"""
        # Act
        response = await async_client.get("/api/v1/<module_name>/<resource>/?limit=10&offset=0")
        
        # Assert
        assert response.status_code == 200


@pytest.mark.e2e
class TestUpdate<Entity>API:
    """Test PUT /api/<feature>/{id} endpoint"""
    
    @pytest.mark.asyncio
    async def test_update_returns_200(self, async_client, create_test_<entity>):
        """FR-003: Should update <entity> and return 200 OK (spec.md Section 4)"""
        # Arrange
        created = await create_test_<entity>({"name": "original", "value": 100})
        payload = {"name": "updated", "value": 200}  # From spec.md Section 4 Request Schema
        
        # Act
        response = await async_client.put(f"/api/v1/<module_name>/<resource>/{created.id}", json=payload)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "updated"
        assert data["value"] == 200


@pytest.mark.e2e
class TestDelete<Entity>API:
    """Test DELETE /api/<feature>/{id} endpoint"""
    
    @pytest.mark.asyncio
    async def test_delete_returns_204(self, async_client, create_test_<entity>):
        """FR-004: Should delete <entity> and return 204 No Content (spec.md Section 4)"""
        # Arrange
        created = await create_test_<entity>({"name": "test", "value": 123})
        
        # Act
        response = await async_client.delete(f"/api/v1/<module_name>/<resource>/{created.id}")
        
        # Assert
        assert response.status_code == 204  # From spec.md Section 4 Status Codes
        
        # Verify deleted
        get_response = await async_client.get(f"/api/v1/<module_name>/<resource>/{created.id}")
        assert get_response.status_code == 404


@pytest.mark.e2e
class TestEdgeCasesAPI:
    """Test edge cases from spec.md Section 8"""
    
    @pytest.mark.asyncio
    async def test_database_unavailable_returns_503(self, async_client):
        """Scenario 1: Database unavailable → 503 (spec.md Section 8)"""
        # This test requires mocking database connection failure
        # Verify error response matches spec.md Section 8 Expected Behavior
        pass
    
    @pytest.mark.asyncio
    async def test_rate_limit_exceeded_returns_429(self, async_client):
        """Scenario 5: Rate limit exceeded → 429 (spec.md Section 8)"""
        # Arrange - make requests exceeding rate limit from spec.md Section 6
        # Act
        # Assert - verify 429 with Retry-After header (spec.md Section 8)
        pass
    
    @pytest.mark.asyncio
    async def test_concurrent_requests_handled(self, async_client):
        """Scenario 4: Concurrent requests handled (spec.md Section 8)"""
        # Test race condition handling from spec.md Section 8
        pass


@pytest.mark.e2e
class TestSecurityAPI:
    """Test security requirements from spec.md Section 6"""
    
    @pytest.mark.asyncio
    async def test_authentication_required(self, async_client):
        """SEC-001: Auth level enforced (spec.md Section 6)"""
        # Test that protected endpoints require authentication
        pass
    
    @pytest.mark.asyncio
    async def test_rate_limiting_enforced(self, async_client):
        """SEC-002: Rate limiting enforced (spec.md Section 6)"""
        # Test rate limits from spec.md Section 6 Rate Limits table
        pass
```

---

### 4. Test Fixtures (Shared Configuration)
**Location:** `tests/conftest.py`

**Maps To:**
- `plan.md` Section 10: Testing Strategy (real PostgreSQL, asyncpg pattern)
- `plan.md` Section 7: Data Models (asyncpg connection pool)
- `tasks.md` T003: Integration Tests setup

**Important:** Uses asyncpg connection pool pattern (plan.md Section 3). No SQLAlchemy sessions.

```python
"""
Shared test fixtures for all test types
Uses asyncpg connection pool pattern (plan.md Section 3)
Real PostgreSQL database (no mocking - plan.md Section 10)
"""
import pytest
import pytest_asyncio
import asyncio
from datetime import datetime
from asyncpg import create_pool, Pool
from httpx import AsyncClient
from src.main import app
from src.core.database.postgresql.client import get_db_pool
from src.modules.<module_name>.infrastructure.repositories.<entity>_repository import <Entity>Repository
from src.modules.<module_name>.domain.models import <Entity>


# Database fixtures (asyncpg pattern - plan.md Section 3)
@pytest.fixture(scope="session")
def db_url():
    """Test database URL - uses real PostgreSQL with asyncpg"""
    return "postgresql://test:test@localhost:5432/test_db"


@pytest_asyncio.fixture(scope="session")
async def db_pool(db_url):
    """Create asyncpg connection pool for tests (plan.md Section 3)"""
    pool = await create_pool(
        db_url,
        min_size=2,
        max_size=5,
        command_timeout=60
    )
    
    # Run migrations (Alembic) to create tables
    # This should use your Alembic setup from plan.md Section 12
    
    yield pool
    
    # Cleanup
    await pool.close()


@pytest_asyncio.fixture
async def db_transaction(db_pool):
    """Transaction fixture that rolls back after each test"""
    async with db_pool.acquire() as connection:
        async with connection.transaction():
            yield connection
            # Transaction automatically rolls back


# API client fixtures
@pytest_asyncio.fixture
async def async_client(db_pool):
    """AsyncClient for API testing with database pool override"""
    # Override database pool dependency if needed
    # This depends on your FastAPI dependency setup
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


# Helper fixtures
@pytest_asyncio.fixture
def create_test_<entity>(db_pool):
    """Factory fixture for creating test <entities> using asyncpg"""
    async def _create(data: dict) -> <Entity>:
        repo = <Entity>Repository()
        entity = <Entity>(
            id=data.get("id", f"test-{datetime.utcnow().timestamp()}"),
            name=data.get("name", "test"),
            value=data.get("value", 123),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            **{k: v for k, v in data.items() if k not in ["id", "name", "value"]}
        )
        result = await repo.save(entity)
        return result
    return _create
```

---

## Test Execution Commands

```bash
# Activate virtual environment (uv managed)
source .venv/bin/activate

# Run all tests
pytest tests/ -v

# Run specific test type
pytest tests/unit/ -v                    # Unit tests only
pytest tests/integration/ -v -m integration  # Integration tests
pytest tests/e2e/ -v -m e2e             # E2E tests only

# Run tests for specific feature
pytest tests/ -k "<feature>" -v

# Run with coverage
pytest tests/ --cov=src/modules/<module_name> --cov-report=html

# Run tests in parallel
pytest tests/ -n auto
```

**Note:** This project uses `uv` as package manager. Always activate `.venv` before running tests.

---

## Test Quality Checklist

### Traceability (spec.md → tests.md)
- [ ] Each test maps to acceptance criteria in spec.md Section 13
- [ ] Each test maps to functional requirements (FR-XXX) in spec.md Section 3
- [ ] Each test maps to user stories in spec.md Section 2
- [ ] Edge case tests map to spec.md Section 8 scenarios
- [ ] Error tests map to spec.md Section 4 Error Responses table

### Test Structure (plan.md alignment)
- [ ] Tests follow directory structure from plan.md Section 6
- [ ] Import paths match plan.md Section 6 (`src/modules/<module_name>/`)
- [ ] Unit tests use mocks (service layer only)
- [ ] Integration tests use real PostgreSQL with asyncpg (plan.md Section 3)
- [ ] E2E tests test full request-response cycle
- [ ] Tests follow Arrange-Act-Assert pattern

### Test-First Compliance (tasks.md TDD)
- [ ] Tests written BEFORE implementation (tasks.md Phase 2)
- [ ] Tests initially FAIL (no implementation exists yet)
- [ ] Test execution order matches tasks.md (T003 → T007, T006 → T008, T010 → T011)

### Code Quality
- [ ] Tests have descriptive names explaining expected behavior
- [ ] All edge cases from spec.md Section 8 covered
- [ ] All error scenarios from spec.md Section 4 tested
- [ ] Pydantic V2 validation tested (plan.md Section 5)
- [ ] OpenAPI compliance verified (plan.md Section 8)

### Special Cases
- [ ] **If testing Celery tasks: Verify sync function pattern (not async def)** - plan.md Section 3
- [ ] **If testing Celery tasks: Verify asyncio.run() wrapper usage** - plan.md Section 3
- [ ] **If testing auth: Verify JWT blocklist (Redis)** - plan.md Section 9
- [ ] **If testing rate limiting: Verify Redis-based limiter** - plan.md Section 9

---

**Package Management:**
- Use `uv add --dev pytest pytest-asyncio httpx` to add test dependencies (plan.md Section 5)
- Virtual environment: `.venv` (managed by uv)
- Always activate: `source .venv/bin/activate` before running tests

---

## Test File Locations Summary

Based on plan.md Section 6 directory structure:

```
tests/
├── conftest.py                                    ← Shared fixtures
├── unit/
│   └── modules/
│       └── <module_name>/
│           └── test_<entity>_service.py         ← Unit tests (Service layer)
├── integration/
│   └── modules/
│       └── <module_name>/
│           └── test_<entity>_repository.py       ← Integration tests (Repository layer)
└── e2e/
    └── modules/
        └── <module_name>/
            └── test_<entity>_api.py               ← E2E tests (API layer)
```

**Module Paths (from plan.md Section 6):**
- Service: `src/modules/<module_name>/application/services/<entity>_service.py`
- Repository: `src/modules/<module_name>/infrastructure/repositories/<entity>_repository.py`
- Domain Models: `src/modules/<module_name>/domain/models.py`
- Domain Exceptions: `src/modules/<module_name>/domain/exceptions.py`
- API Routes: `src/modules/<module_name>/api/routes.py`
- API Schemas: `src/modules/<module_name>/api/schemas.py`

---

## Test Traceability Matrix (spec.md → tests.md)

**Purpose:** Ensure all requirements from spec.md have corresponding tests.

| Spec Requirement | Test File | Test Method | Status |
|------------------|-----------|-------------|--------|
| **User Story 1** (spec.md Section 2) | `test_<entity>_api.py` | `test_create_returns_201` | ⏳ |
| **FR-001** (spec.md Section 3) | `test_<entity>_service.py` | `test_create_success` | ⏳ |
| **FR-001** (spec.md Section 3) | `test_<entity>_repository.py` | `test_save_persists_to_database` | ⏳ |
| **FR-002** (spec.md Section 3) | `test_<entity>_service.py` | `test_get_success` | ⏳ |
| **FR-002** (spec.md Section 3) | `test_<entity>_repository.py` | `test_find_by_id_found` | ⏳ |
| **FR-010** (spec.md Section 3) | `test_<entity>_service.py` | `test_create_validation_error` | ⏳ |
| **API-001** (spec.md Section 4) | `test_<entity>_api.py` | `test_create_returns_201` | ⏳ |
| **Error 400** (spec.md Section 4) | `test_<entity>_api.py` | `test_create_validation_error_returns_400` | ⏳ |
| **Error 404** (spec.md Section 4) | `test_<entity>_api.py` | `test_get_not_found_returns_404` | ⏳ |
| **Scenario 1** (spec.md Section 8) | `test_<entity>_api.py` | `test_database_unavailable_returns_503` | ⏳ |
| **Scenario 5** (spec.md Section 8) | `test_<entity>_api.py` | `test_rate_limit_exceeded_returns_429` | ⏳ |
| **SEC-001** (spec.md Section 6) | `test_<entity>_api.py` | `test_authentication_required` | ⏳ |
| **Acceptance Criterion 1** (spec.md Section 13) | `test_<entity>_api.py` | `[map to specific test]` | ⏳ |

**Legend:**
- ⏳ Planned (test written, implementation pending)
- 🔄 In Progress (test passing, implementation in progress)
- ✅ Complete (test passing, implementation complete)
- ❌ Failed (test failing, needs fix)

**Note:** This matrix should be populated as tests are generated. Each row should map to a specific requirement in spec.md.

---

## 5. CLI Testing (If CLI Feature Exists)

**Location:** `tests/e2e/modules/<module_name>/test_<entity>_cli.py`

**Maps To:**
- `plan.md` Section 9: CLI Interface Design (if applicable)
- `tasks.md` T013: CLI Interface (if applicable)

**Important:** CLI testing requires setting PYTHONPATH and proper environment setup.

```python
"""
E2E tests for <Module> CLI commands
Tests CLI functionality with real database
Maps to CLI requirements from plan.md Section 9
"""
import pytest
import subprocess
import json
import os
from pathlib import Path

# Set PYTHONPATH for CLI tests
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
PYTHONPATH = str(PROJECT_ROOT)


@pytest.mark.e2e
class TestCLICreate:
    """Test CLI create command"""
    
    def test_create_success(self, db_pool):
        """Should create <entity> via CLI"""
        # Arrange
        env = os.environ.copy()
        env['PYTHONPATH'] = PYTHONPATH
        env['DATABASE_URL'] = os.getenv('DATABASE_URL', 'postgresql://test:test@localhost/test_db')
        
        # Act
        result = subprocess.run(
            ['python', '-m', 'src.cli.<module_name>', 'create', '--name', 'test', '--value', '123'],
            env=env,
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT
        )
        
        # Assert
        assert result.returncode == 0
        assert 'Created' in result.stdout or 'created' in result.stdout.lower()
    
    def test_create_with_json_output(self, db_pool):
        """Should output JSON when --json flag used"""
        # Arrange
        env = os.environ.copy()
        env['PYTHONPATH'] = PYTHONPATH
        
        # Act
        result = subprocess.run(
            ['python', '-m', 'src.cli.<module_name>', 'create', '--name', 'test', '--value', '123', '--json'],
            env=env,
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT
        )
        
        # Assert
        assert result.returncode == 0
        # Verify JSON is valid and contains datetime as ISO string (not datetime object)
        output = json.loads(result.stdout)
        assert 'id' in output
        # Verify datetime fields are strings (not datetime objects)
        if 'created_at' in output:
            assert isinstance(output['created_at'], str)  # Must be ISO string, not datetime object


@pytest.mark.e2e
class TestCLIGet:
    """Test CLI get command"""
    
    def test_get_success(self, db_pool, create_test_<entity>):
        """Should retrieve <entity> via CLI"""
        # Arrange
        entity = await create_test_<entity>({"name": "test", "value": 123})
        env = os.environ.copy()
        env['PYTHONPATH'] = PYTHONPATH
        
        # Act
        result = subprocess.run(
            ['python', '-m', 'src.cli.<module_name>', 'get', entity.id],
            env=env,
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT
        )
        
        # Assert
        assert result.returncode == 0
        assert entity.id in result.stdout or entity.name in result.stdout
    
    def test_get_not_found(self, db_pool):
        """Should handle not found gracefully"""
        # Arrange
        env = os.environ.copy()
        env['PYTHONPATH'] = PYTHONPATH
        
        # Act
        result = subprocess.run(
            ['python', '-m', 'src.cli.<module_name>', 'get', 'non-existent-id'],
            env=env,
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT
        )
        
        # Assert
        assert result.returncode != 0  # Should fail
        assert 'not found' in result.stderr.lower() or 'error' in result.stderr.lower()


@pytest.mark.e2e
class TestCLIErrorHandling:
    """Test CLI error handling"""
    
    def test_cli_without_pythonpath_fails(self):
        """Should fail if PYTHONPATH not set (common issue)"""
        # Arrange - explicitly unset PYTHONPATH
        env = os.environ.copy()
        env.pop('PYTHONPATH', None)
        
        # Act
        result = subprocess.run(
            ['python', '-m', 'src.cli.<module_name>', '--help'],
            env=env,
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT
        )
        
        # Assert - should fail with ModuleNotFoundError
        # This documents the common issue: PYTHONPATH must be set
        if result.returncode != 0:
            assert 'ModuleNotFoundError' in result.stderr or 'No module named' in result.stderr
```

---

## Common Testing Pitfalls & Prevention

### ⚠️ Issue #1: Database Transactions Not Committed

**Problem:** Tests pass but data doesn't persist in database.

**Root Cause:** Missing `await db.commit()` after database writes in route handlers.

**Prevention in Tests:**
```python
# In E2E tests, verify data actually persisted
@pytest.mark.asyncio
async def test_create_persists_to_database(self, async_client, db_pool):
    """Should persist <entity> to database"""
    # Act
    response = await async_client.post("/api/v1/<module>/<resource>/", json=payload)
    
    # Assert - verify in database directly
    assert response.status_code == 201
    entity_id = response.json()["id"]
    
    # CRITICAL: Verify data actually persisted
    repo = <Entity>Repository()
    persisted = await repo.find_by_id(entity_id)
    assert persisted is not None  # Must exist in database
    assert persisted.name == "test"
```

**What to Test:**
- [ ] After POST, verify entity exists in database
- [ ] After PUT, verify changes persisted
- [ ] After DELETE, verify entity removed from database
- [ ] Test transaction rollback on errors

---

### ⚠️ Issue #2: Timezone-Aware Datetime Issues

**Problem:** Tokens expire immediately, timestamps incorrect.

**Root Cause:** Using `datetime.utcnow()` instead of `datetime.now(timezone.utc)`.

**Prevention in Tests:**
```python
# Test datetime handling
from datetime import datetime, timezone

def test_datetime_timezone_aware(self):
    """Should use timezone-aware datetimes"""
    # Verify implementation uses timezone-aware
    now = datetime.now(timezone.utc)
    assert now.tzinfo is not None  # Must have timezone info
    
    # Test token expiration
    token = generate_token()
    decoded = jwt.decode(token, options={"verify_signature": False, "verify_exp": False})
    exp_timestamp = decoded["exp"]
    exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
    assert exp_datetime > datetime.now(timezone.utc)  # Must be in future
```

**What to Test:**
- [ ] All datetime operations use `datetime.now(timezone.utc)`
- [ ] Token expiration times are in the future
- [ ] Database timestamps are timezone-aware
- [ ] JSON serialization handles datetime correctly

---

### ⚠️ Issue #3: PYTHONPATH Not Set (CLI Testing)

**Problem:** CLI commands fail with `ModuleNotFoundError: No module named 'src'`.

**Root Cause:** PYTHONPATH not set before running CLI commands.

**Prevention in Tests:**
```python
# Always set PYTHONPATH in CLI tests
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
PYTHONPATH = str(PROJECT_ROOT)

def test_cli_with_pythonpath(self):
    """Should work when PYTHONPATH is set"""
    env = os.environ.copy()
    env['PYTHONPATH'] = PYTHONPATH  # CRITICAL: Must set PYTHONPATH
    
    result = subprocess.run(
        ['python', '-m', 'src.cli.<module>', '--help'],
        env=env,
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT
    )
    assert result.returncode == 0
```

**What to Test:**
- [ ] CLI works when PYTHONPATH is set
- [ ] CLI fails gracefully when PYTHONPATH not set (document the issue)
- [ ] CLI help command works
- [ ] CLI commands work from project root

---

### ⚠️ Issue #4: JSON Serialization Errors (CLI)

**Problem:** CLI JSON output fails with "Object of type datetime is not JSON serializable".

**Root Cause:** Datetime objects not converted to strings before JSON serialization.

**Prevention in Tests:**
```python
def test_cli_json_output_serializable(self, db_pool, create_test_<entity>):
    """Should output valid JSON with datetime as strings"""
    entity = await create_test_<entity>({"name": "test", "value": 123})
    env = os.environ.copy()
    env['PYTHONPATH'] = PYTHONPATH
    
    result = subprocess.run(
        ['python', '-m', 'src.cli.<module>', 'get', entity.id, '--json'],
        env=env,
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT
    )
    
    assert result.returncode == 0
    output = json.loads(result.stdout)  # Must be valid JSON
    
    # CRITICAL: Verify datetime fields are strings, not datetime objects
    if 'created_at' in output:
        assert isinstance(output['created_at'], str)  # Must be ISO string
        # Verify it's a valid ISO format
        datetime.fromisoformat(output['created_at'].replace('Z', '+00:00'))
```

**What to Test:**
- [ ] CLI JSON output is valid JSON
- [ ] Datetime fields are ISO format strings (not datetime objects)
- [ ] All fields are JSON-serializable
- [ ] Error messages are JSON-serializable

---

### ⚠️ Issue #5: Token Expiration Testing

**Problem:** Tokens expire immediately or expiration not tested properly.

**Prevention in Tests:**
```python
def test_token_expiration_future(self):
    """Should generate tokens with future expiration"""
    token = generate_access_token(user_id="123")
    decoded = jwt.decode(token, options={"verify_signature": False, "verify_exp": False})
    
    now = datetime.now(timezone.utc).timestamp()
    exp = decoded["exp"]
    
    # CRITICAL: Expiration must be in future
    assert exp > now, f"Token expires at {exp}, current time is {now}"
    
    # Verify expiration time is reasonable (e.g., 1 hour for access token)
    time_until_expiry = exp - now
    assert 3500 < time_until_expiry < 3700  # ~1 hour (3600 seconds) with tolerance
```

**What to Test:**
- [ ] Token expiration is in the future
- [ ] Token expiration matches expected lifetime (from spec.md)
- [ ] Token validation works before expiration
- [ ] Token validation fails after expiration
- [ ] Token refresh works before expiration

---

## Comprehensive Test Scenarios Checklist

### Database Operations
- [ ] **Create persists to database** - Verify entity exists after creation
- [ ] **Update persists changes** - Verify changes saved to database
- [ ] **Delete removes entity** - Verify entity removed from database
- [ ] **Transaction rollback on error** - Verify no partial data on error
- [ ] **Concurrent operations** - Test race conditions (spec.md Section 8)
- [ ] **Database unavailable** - Test 503 response (spec.md Section 8)

### API Endpoints
- [ ] **Happy path** - All endpoints work with valid data
- [ ] **Validation errors** - All validation rules tested (spec.md Section 3)
- [ ] **Error responses** - All error codes tested (spec.md Section 4)
- [ ] **Authentication** - Protected endpoints require auth (spec.md Section 6)
- [ ] **Rate limiting** - Rate limits enforced (spec.md Section 6)
- [ ] **Edge cases** - All edge cases from spec.md Section 8 tested

### CLI Commands
- [ ] **PYTHONPATH set** - CLI works when PYTHONPATH is set
- [ ] **PYTHONPATH not set** - CLI fails gracefully (documents issue)
- [ ] **JSON output** - JSON output is valid and serializable
- [ ] **Datetime serialization** - Datetime fields are ISO strings
- [ ] **Error handling** - CLI handles errors gracefully
- [ ] **Help command** - CLI help works
- [ ] **All commands** - Every CLI command tested

### Token Operations (If Auth Feature)
- [ ] **Token generation** - Tokens generated correctly
- [ ] **Token expiration** - Tokens expire at correct time
- [ ] **Token validation** - Valid tokens accepted
- [ ] **Expired tokens** - Expired tokens rejected
- [ ] **Token refresh** - Refresh tokens work
- [ ] **Token blacklist** - Blacklisted tokens rejected (spec.md Section 6)
- [ ] **Token format** - Authorization header format correct

### Integration Points
- [ ] **Database connection** - Real PostgreSQL works
- [ ] **Redis connection** - Redis works (if used)
- [ ] **Redis unavailable** - Graceful degradation (if applicable)
- [ ] **External services** - External API calls tested (spec.md Section 10)

---

## 6. Logging Tests (If Applicable)

**Location:** `tests/unit/modules/<module_name>/test_logging.py` or integrated in service tests

**Maps To:**
- `plan.md` Section 15: Observability (Logging Implementation)
- `tasks.md` T015: Logger Configuration Setup
- `tasks.md` T016: Observability & Logging

**Important:** Test that logs are written to `logs/belogs.log` and contain expected information.

```python
"""
Tests for logging functionality
Verifies logs are written to logs/belogs.log at root level
"""
import pytest
import logging
from pathlib import Path
from src.common.logger.config import get_logger, setup_logging

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
LOG_FILE = PROJECT_ROOT / "logs" / "belogs.log"


@pytest.fixture(autouse=True)
def setup_logging_for_tests():
    """Setup logging for tests"""
    setup_logging()
    yield
    # Cleanup: clear log file after tests
    if LOG_FILE.exists():
        LOG_FILE.write_text("")


def test_logger_writes_to_file():
    """Should write logs to logs/belogs.log"""
    logger = get_logger(__name__)
    test_message = "Test log message"
    
    logger.info(test_message)
    
    # Verify log file exists
    assert LOG_FILE.exists(), f"Log file not found at {LOG_FILE}"
    
    # Verify log content
    log_content = LOG_FILE.read_text()
    assert test_message in log_content


def test_logger_includes_context():
    """Should include context in log messages"""
    logger = get_logger(__name__)
    
    logger.info(
        "Test event",
        extra={
            "request_id": "test-123",
            "user_id": "user-456",
            "action": "test_action"
        }
    )
    
    log_content = LOG_FILE.read_text()
    assert "test-123" in log_content
    assert "user-456" in log_content
    assert "test_action" in log_content


def test_logger_log_levels():
    """Should respect log levels"""
    logger = get_logger(__name__)
    
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    
    log_content = LOG_FILE.read_text()
    # Debug messages might not appear if level is INFO
    assert "Info message" in log_content
    assert "Warning message" in log_content
    assert "Error message" in log_content


def test_logs_directory_created():
    """Should create logs directory if it doesn't exist"""
    logs_dir = PROJECT_ROOT / "logs"
    assert logs_dir.exists(), "logs/ directory should exist"
    assert logs_dir.is_dir(), "logs/ should be a directory"
```

---

## 🛡️ Testing Best Practices - Quick Reference

> **Full Details:** See `reference/LESSONS_REFERENCE.md` for code examples

### Test Writing Checklist
- [ ] **L17** Status codes: Expect 422 for Pydantic validation (NOT 400!)
- [ ] **L16** Imports: uuid, datetime, timezone, AsyncMock all imported
- [ ] **L18** Domain models: Use real instances, not Mock()
- [ ] **L20** Fixtures: Test immediately after creation
- [ ] **L12** Discovery: Import fixtures in main conftest.py
- [ ] **L13** AsyncPG: Explicit acquire/release in fixtures
- [ ] **L14** httpx: Use ASGITransport(app=app) for E2E tests
- [ ] **L19** Libraries: Verify API params (jwt.decode needs key)
- [ ] **L27** Mocks: AsyncMock for async, Mock for sync methods
- [ ] **L24** Datetime: Use datetime.now(timezone.utc) everywhere

### Status Code Quick Reference
| Code | Test Expectation |
|------|------------------|
| 422 | Pydantic validation error |
| 401 | Missing/invalid auth |
| 404 | Resource not found |
| 409 | Duplicate/conflict |
| 201 | Resource created |

### httpx Setup Pattern
```python
from httpx import AsyncClient, ASGITransport
transport = ASGITransport(app=app)
async with AsyncClient(transport=transport, base_url="http://test") as client:
    response = await client.get("/api/v1/endpoint")
```

---

## Next Steps (After Test Generation)
## Next Steps (After Test Generation)

Once test suites are generated:

1. **Review test coverage** against spec.md Section 13 (Acceptance Criteria)
2. **Verify test structure** matches plan.md Section 6 (Directory Structure)
3. **Populate traceability matrix** above to ensure all requirements covered
4. **Add common pitfalls tests** - Test for issues documented above
5. **Add CLI tests** - If CLI feature exists, test comprehensively
6. **Add logging tests** - If logging feature exists, test logs are written to `logs/belogs.log`
7. **Run tests** (they should FAIL - no implementation exists yet)
8. **Proceed to Phase 5: Implementation** - Implement code to make tests pass (TDD - tasks.md)

---

**Save all test files to appropriate locations as specified above.**
