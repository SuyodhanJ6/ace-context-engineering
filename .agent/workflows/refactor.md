---
description: Strict TDD-based refactoring workflow
---

# AI Refactoring Workflow

## Phase 1: Analysis (Understand Before Changing)
1. **Analyze Current Structure**:
   - What does the code do?
   - What are the dependencies?
   - What parts of the system use this?
2. **Assess Risks**:
   - What could break?
   - Any critical business rules?
   - Locate existing tests.
3. **Propose Approach**:
   - Recommend exact structural changes.
4. **Identify Required Tests**:
   - What tests need to exist before refactoring?

## Phase 2: TDD Lock & Replace
1. **Step 1: Lock Behavior (Tests First)**:
   - Create unit tests that verify CURRENT behavior.
   - Use current implementation as source of truth.
2. **Step 2: Refactor**:
   - Make ONLY the structural changes.
   - ❌ DO NOT change variable names, signatures, error messages, or logs.
   - ❌ DO NOT optimize logic.
3. **Step 3: Verify**:
   - Re-run tests. If they fail, rollback immediately.

## Phase 3: Verification & Review
1. Ensure all tests pass.
2. Check against `.cursorrules` (Layering, Type hints, Async/Await, Pydantic V2).
3. Confirm if ready to commit.
