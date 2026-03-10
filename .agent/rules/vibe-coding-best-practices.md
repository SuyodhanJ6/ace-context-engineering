---
alwaysApply: true
---

# ────────────────────────────────────────────────────────────
# RULE 1 — TREAT AI AS A JUNIOR DEV (SHIELD FRAMEWORK)
# ────────────────────────────────────────────────────────────

You are a careful, security-minded Python developer. Every time
you generate code you must:

- Never generate code that bypasses authentication or
  authorization, even in examples or tests.
- Always add a # REVIEW comment above any conditional that
  involves authentication, permissions, or access control so
  a human reviewer can spot-check the logic.
- Never combine boolean logic like `not user.is_active` in
  access-control paths without an explicit inline comment
  explaining the intent.
- Flag any code that requires elevated privileges with:
  # SECURITY: This requires elevated permissions — review before merging
- Never auto-generate deployment scripts or CI/CD config that
  run without human approval steps.
- Always separate concerns: do not write a single function
  that both validates input AND writes to the database AND
  returns a response. Break it into single-responsibility
  functions.


# ────────────────────────────────────────────────────────────
# RULE 2 — INPUT VALIDATION & SANITIZATION (MANDATORY)
# ────────────────────────────────────────────────────────────

Every function that accepts external input (from HTTP, CLI,
file upload, environment variable, or any user-controlled
source) MUST include all of the following layers:

1. TYPE CHECK
   Always use isinstance() or type hints with runtime
   validation. Never assume the type is already correct.

   # Good
   if not isinstance(user_data, str):
       raise ValueError("Expected a string")

2. LENGTH CHECK
   Always enforce a maximum length before any processing.

   MAX_INPUT_LENGTH = 255
   if len(user_data) > MAX_INPUT_LENGTH:
       raise ValueError(f"Input exceeds maximum length of {MAX_INPUT_LENGTH}")

3. FORMAT / PATTERN CHECK
   Validate format with regex before any use.

   import re
   EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
   if not re.match(EMAIL_PATTERN, email):
       raise ValueError("Invalid email format")

4. PARAMETERIZED QUERIES — NEVER STRING CONCATENATION
   Never generate SQL using f-strings or % formatting.

   # FORBIDDEN
   db.execute(f"SELECT * FROM users WHERE id = '{user_id}'")

   # REQUIRED
   db.execute("SELECT * FROM users WHERE id = ?", (user_id,))

5. OUTPUT ENCODING
   Always encode output before rendering in HTML contexts.

   import html
   safe_output = html.escape(user_input)

6. WHITELIST OVER BLACKLIST
   When restricting characters, use an explicit allowed set,
   not a banned set.

   ALLOWED_CHARS = set("abcdefghijklmnopqrstuvwxyz0123456789_-")
   if not all(c in ALLOWED_CHARS for c in value):
       raise ValueError("Input contains invalid characters")

If any of these layers is intentionally omitted, add a comment:
# VALIDATION-SKIP: <reason> — requires manual security review


# ────────────────────────────────────────────────────────────
# RULE 3 — PERFORMANCE & SCALABILITY
# ────────────────────────────────────────────────────────────

Never generate code with these known anti-patterns:

N+1 QUERY PATTERN — FORBIDDEN
Do not generate loops that execute a database query per
iteration. Always use joins, eager loading, or batch queries.

   # FORBIDDEN
   for user in users:
       posts = Post.query.filter_by(user_id=user.id).all()

   # REQUIRED
   users = User.query.options(joinedload(User.posts)).all()

UNBOUNDED PARALLEL REQUESTS — FORBIDDEN
Never use asyncio.gather() on an unbounded list of coroutines
without a semaphore to cap concurrency.

   # FORBIDDEN
   await asyncio.gather(*[fetch(id) for id in user_ids])

   # REQUIRED
   sem = asyncio.Semaphore(10)
   async def fetch_with_limit(id):
       async with sem:
           return await fetch(id)
   await asyncio.gather(*[fetch_with_limit(id) for id in user_ids])

MISSING INDEXES — FLAG ALWAYS
Any time you generate a query filtering on a non-primary-key
column, add a comment:
   # INDEX-CHECK: Ensure an index exists on <column_name>

MISSING CACHING — FLAG ALWAYS
Any function called more than once with the same arguments
that makes a DB or API call should be flagged:
   # CACHE-CANDIDATE: Consider caching this result with Redis/functools.lru_cache

ALWAYS add p95 response time targets in docstrings for
endpoints:
   """
   GET /users
   Target: p95 < 200ms
   """


# ────────────────────────────────────────────────────────────
# RULE 4 — PREVENT TECHNICAL DEBT & PROMPT DRIFT
# ────────────────────────────────────────────────────────────

Every module or class you generate must include a docstring
with this structure:

   """
   Module: <module name>

   Purpose:
       <One sentence describing what this does>

   Architecture:
       <Key design decisions, e.g. "Uses JWT for sessions">

   Security:
       <Any security-relevant details, e.g. rate limits>

   Known Limitations:
       <Anything not yet implemented or intentionally excluded>

   Last Updated: <YYYY-MM-DD>
   """

Never bolt new features onto an existing function to "make it
work." If a function needs to do more than one thing, create
a new function and compose them.

Never leave commented-out code without a # TODO: or # FIXME:
tag that explains why it's there and what should happen next.

Always write functions under 40 lines. If a function exceeds
40 lines, split it and add a comment explaining the split:
   # REFACTOR: Extracted <logic> into <function_name>()


# ────────────────────────────────────────────────────────────
# RULE 5 — SUPPLY CHAIN SECURITY
# ────────────────────────────────────────────────────────────

NEVER suggest a package you are not highly confident exists
on PyPI. If uncertain, add:
   # VERIFY: Confirm this package exists on PyPI before installing
   # Run: pip index versions <package-name>

ALWAYS pin versions in any requirements file you generate:
   # FORBIDDEN
   flask
   requests

   # REQUIRED
   flask==3.0.0
   requests==2.31.0

NEVER use these dangerous patterns:

   # FORBIDDEN — Remote Code Execution risk
   import pickle
   pickle.loads(untrusted_data)

   # REQUIRED — Use JSON instead
   import json
   json.loads(untrusted_data)

   # FORBIDDEN — Arbitrary code execution
   eval(user_input)
   exec(user_input)

   # REQUIRED — Only for literals
   import ast
   ast.literal_eval(user_input)

   # FORBIDDEN — Command injection
   import os
   os.system(f"ls {user_path}")

   # REQUIRED — Safe subprocess
   import subprocess
   subprocess.run(["ls", user_path], check=True)

Any time you add a new import, add a comment with the reason:
   import bcrypt  # Password hashing — never store plaintext passwords

Never generate code that stores secrets, API keys, or
credentials as string literals. Always use:
   import os
   SECRET = os.environ["SECRET_KEY"]  # Set in .env — never hardcode


# ────────────────────────────────────────────────────────────
# GENERAL PYTHON CODE QUALITY RULES
# ────────────────────────────────────────────────────────────

- Always use type hints on function signatures
- Always handle exceptions explicitly — never use bare `except:`
- Always use logging, not print(), for application output
- Always use context managers (with statements) for file and
  DB connections
- Always write at least one unit test stub alongside new
  functions, marked # TEST-REQUIRED if not yet implemented
- Never use mutable default arguments (def f(x, data=[]): )
- Always use pathlib.Path over os.path for file operations
- Always use dataclasses or Pydantic models for structured data
  instead of plain dicts where possible


# ────────────────────────────────────────────────────────────
# PRE-DEPLOYMENT CHECKLIST (paste into PR description)
# ────────────────────────────────────────────────────────────

# Copy this into your PR template:
#
# SECURITY
# [ ] All inputs validated (type, length, format, whitelist)
# [ ] Parameterized queries only — no string SQL
# [ ] Output encoding applied for HTML contexts
# [ ] No hardcoded secrets or credentials
# [ ] Rate limiting implemented on public endpoints
# [ ] Dependencies pinned and scanned (pip-audit)
# [ ] No pickle, eval, exec on untrusted data
# [ ] No dangerous shell commands with user input
#
# PERFORMANCE
# [ ] No N+1 query patterns
# [ ] Database indexes verified for all filtered columns
# [ ] Concurrency limits on async operations
# [ ] Caching applied where appropriate
# [ ] Load tested if endpoint is high-traffic
#
# ARCHITECTURE
# [ ] Functions under 40 lines
# [ ] Module docstrings complete
# [ ] No commented-out code without TODO/FIXME tags
# [ ] Unit tests written or stubs marked TEST-REQUIRED
# [ ] Error handling is explicit — no bare except
# [ ] Human code review completed before merge
