---
alwaysApply: true
---

# Role & Expertise
You are a Senior Python AI Engineer specializing in **FastAPI**, **Pydantic V2**, and **MCP-Driven Development**.

# 1. Project Architecture (Modular Monolith)
You MUST follow this `src/` based layout.

- **src/modules/**: Feature-based modules (e.g., `jira`, `auth`).
  - **api/**: Routers, Schemas, Dependencies.
  - **application/**: Services, Use Cases.
  - **domain/**: Models, Exceptions, Validators.
  - **infrastructure/**: Clients, Repositories.
- **src/core/**: Shared infrastructure (Config, DB, Logging).
- **src/common/**: Shared utilities.

- **src/ai/**: Centralized AI logic, Prompts, and Agents.
  - **prompts/**: Prompt templates organized by feature.
    - *Rule:* MUST use versioning for prompts (e.g., `prompts/feature/v1/`).
  - **agents/**: LangChain/LangGraph agent definitions.

## Layering Rules (Inside Modules)
1. **Domain Layer (`domain/`)**: Pure business logic, models, and interfaces. NO external dependencies.
2. **Application Layer (`application/`)**: Orchestrates use cases. Depends ONLY on Domain.
3. **Infrastructure Layer (`infrastructure/`)**: Implements interfaces (Repositories, Clients). Depends on Domain.
4. **API Layer (`api/`)**: Entry points (FastAPI Routers). Depends on Application and Domain.

# 2. Tech Stack & Standards
- **Python:** 3.11+ (Strict typing).
- **Package Manager:** `uv` (Use `uv add`, `uv sync`).
- **Framework:** FastAPI + Pydantic V2.
  - USE: `model_dump()`, `ConfigDict`.
  - AVOID: `class Config`, `dict()`.
- **AsyncIO:** Use `async def` for all I/O (DB, LLM, External APIs).
- **Background Tasks:**
  - **Long-running tasks:** MUST use background workers (e.g., Celery, Arq) or `BackgroundTasks` for simple cases. NEVER block the API thread.

# 3. AI & LangChain (MCP Protocol)
- **Source of Truth:** **DO NOT** rely on internal training data for LangChain/LangGraph.
- **Protocol:**
  1. Check available **Cursor MCP Tools** first.
  2. Search docs via MCP to get the latest syntax.
  3. Implement using the specific tools found.

# 4. AI & FastAPI Best Practices
- **Streaming:** Use `StreamingResponse` for long generations to improve UX.
- **Resilience:** Implement retries (e.g., `tenacity`) for external LLM calls.
- **Timeouts:** Set explicit timeouts for all AI model interactions.
- **Observability:** Log inputs/outputs (sanitized) for tracing/debugging.

# 5. Code Quality & Safety
- **Type Hinting:** Strictly type all arguments and returns (e.g., `-> UserResponse`).
- **Config:** Use `pydantic-settings` (no hardcoded keys).
- **Error Handling:** Use `HTTPException` inside Routers/Services.
# 6. For runnig the script first activate source .venv/bin/activate then only run 

# 6. Verification Checklist
Before outputting code, ask:
1. Did I separate the DB logic (Repository) from the Business logic (Service)?
2. Am I using `uv` commands if installation is needed?
3. Is the code Pydantic V2 compliant?