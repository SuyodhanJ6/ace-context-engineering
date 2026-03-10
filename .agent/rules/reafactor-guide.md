---
alwaysApply: true
---
# AI Refactoring Guide

## 📍 P1 — Analysis Prompt (Understand Before Changing)

```
Analyze the code in @[specific_file_or_folder] that I want to frefactor.

**Before making ANY changes, tell me:**

1. **Current Structure**
   - What does this code do?
   - What are the dependencies?
   - What other parts of the system use this?

2. **Refactoring Risks**
   - What could break if we change this?
   - Are there any critical business rules here?
   - Where are the existing tests?

3. **Proposed Approach**
   - What exact structural changes do you recommend?
   - What will stay the same?
   - What will change?

4. **Required Tests**
   - What tests need to exist before we refactor?
   - What current behavior must be locked?

Wait for my approval before proceeding.
```

---

## 📍 P2 — TDD Lock & Replace (Safe Refactoring)

```
Refactor @[specific_file.py] following strict TDD workflow from .cursorrules.

**Target:** [Describe EXACTLY what to refactor - e.g., "Extract lines 45-78 into a new method"]

**Step 1: Lock Behavior (Tests First)**
Create unit tests that verify the CURRENT behavior of:
- [specific function/class/method]

Requirements:
- Test all input cases
- Test error conditions  
- Use current implementation as source of truth
- DO NOT modify the code yet

After providing tests, STOP and wait for my confirmation they pass.

**Step 2: Refactor (Only After My Approval)**
Make ONLY this change:
- [Exact structural change, e.g., "Extract method X, move to file Y, update imports"]

**Constraints:**
❌ Do NOT change variable names
❌ Do NOT change function signatures
❌ Do NOT change error messages
❌ Do NOT change log statements
❌ Do NOT optimize or improve logic
✅ ONLY change internal structure

**Step 3: Verify**
Re-run the same tests. If they fail, rollback immediately and explain what went wrong.
```

---

## 📍 P3 — Failure Analysis (When Tests Break)

```
⚠️ **Tests failed after refactoring. Rollback completed.**

Analyze what went wrong:

1. **What Changed That Shouldn't Have?**
   - Show me the exact code differences
   - Which constraint from .cursorrules did you violate?

2. **Why Did You Make That Change?**
   - What was your reasoning?
   - What did you assume was okay to change?

3. **Root Cause**
   - Was it a logic change?
   - Was it a signature change?
   - Was it an unexpected side effect?

4. **How to Fix It**
   - What should you do differently?
   - What additional constraint should we add?

Format as:
```markdown
## What Broke
[Exact change that failed]

## Why I Made That Change
[My reasoning]

## What I Should Have Done
[Correct approach]

## New Constraint to Remember
[Specific rule to prevent this]
```
```

---

## 📍 P4 — Success Confirmation (Move Forward)

```
✅ Tests passed! Refactoring successful.

Confirm:
1. All tests still passing?
2. No behavior changes detected?
3. Code is cleaner/more maintainable?

Show me:
- What changed (structure only)
- What stayed the same (behavior)
- Test coverage report

Ready to commit: [yes/no]
```

---

## 📍 P5 — Code Review Before Commit

```
Before I commit this refactoring, review it against .cursorrules:

**Checklist:**
- [ ] Layering rules followed? (Domain → Application → Infrastructure → API)
- [ ] Type hints present on all functions?
- [ ] Async/await used for I/O operations?
- [ ] Pydantic V2 syntax used? (model_dump, ConfigDict)
- [ ] Repository pattern used for DB access?
- [ ] No hardcoded config values?
- [ ] Proper error handling with HTTPException?
- [ ] Tests cover the refactored code?

Show me what passes and what needs fixing.
```

---

## 🎯 Quick Reference

| Prompt | Use When | Output |
|--------|----------|--------|
| **P1** | Before starting any refactoring | Analysis + approach + risks |
| **P2** | Executing the actual refactor | Tests + refactored code |
| **P3** | Tests fail after refactor | Failure analysis + fix approach |
| **P4** | Tests pass after refactor | Confirmation to commit |
| **P5** | Before final commit | Quality checklist review |

---

## 📋 Typical Workflow

```
You: "I want to refactor UserService.py"
↓
→ P1: Analyze UserService.py
← AI: Here's what it does, risks, and approach
↓
You: "Approved, proceed"
↓
→ P2: Create tests and refactor following TDD
← AI: Here are tests [you run them]
↓
You: "Tests pass, continue"
↓
← AI: Here's refactored code [you run tests again]
↓
✅ Tests pass → Use P4 to confirm
❌ Tests fail → Use P3 to analyze
↓
→ P5: Final review before commit
← AI: Checklist complete
↓
✅ Commit!
```

---

## 🔧 Pro Tips

1. **Be extremely specific in P2**
   ```
   ❌ "Refactor the user validation"
   ✅ "Extract the email validation logic from UserService.validate() 
       lines 23-45 into common/validators.py as validate_email_format()"
   ```

2. **Always use @filename references**
   ```
   "Analyze @src/modules/auth/service.py"
   "Refactor @src/core/database.py"
   ```

3. **One refactor at a time**
   - Don't combine multiple changes
   - Complete P2→P4 cycle for each change

4. **Keep .cursorrules visible**
   - Reference it: "Follow TDD workflow from @.cursorrules"
   - AI will read and follow the rules

5. **Test immediately**
   - After P2 Step 1: Run tests
   - After P2 Step 2: Run tests again
   - Don't skip this!

---

## 🚨 Emergency Commands

```
"Stop. Rollback all changes."
"Show me exactly what changed from original."
"Re-read the constraints in @.cursorrules"
"Start over following strict TDD from @.cursorrules"
```

---
