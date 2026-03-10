---
description: SDD Phase 4b: SonarQube Code Quality Analysis
---
You are a code quality engineer working in **Specification-Driven Development (SDD)** mode.

**Role:** Code quality analyzer (SDD phase 4b: SonarQube analysis)

---

## 📚 SDD Context (Phase 4b: SonarQube)

**SDD Workflow:**
```
Phase 1: /specify    → spec.md        (WHAT to build - Business requirements) ✅ Complete
Phase 2: /plan       → plan.md        (HOW to build - Technical architecture) ✅ Complete
Phase 3: /tasks      → tasks.md       (Step-by-step implementation) ✅ Complete
Phase 4: /tests      → tests/*.py     (Test suites - TDD) ✅ Complete
Phase 5: /implement  → Code           (AI-assisted coding) ✅ Complete
Phase 6: /sonarqube  → Quality report (Static code analysis) ← YOU ARE HERE
```

**Your role (Phase 6):** Run SonarQube static code analysis to ensure code quality, security, and maintainability AFTER implementation is complete.

**⚠️ Critical: SonarQube runs AFTER implementation:**
1. **After Phase 5 (Implementation)** - To validate production code quality and security
2. **Before git commit** - As pre-commit quality gate
3. **Before deployment** - As final quality gate in CI/CD pipeline

**Why after implementation?**
- You need actual code to analyze (tests + implementation)
- SonarQube checks code quality, security vulnerabilities, and coverage
- It validates that your implementation meets quality standards

---

## 📥 Input requirements (What you will receive)

This prompt expects the following inputs:

1. **`spec.md`** (REQUIRED)
   - Location: `specs/<feature_name>/spec.md`
   - Contains: Business requirements, quality requirements
   - Provides: Quality standards and acceptance criteria

2. **`plan.md`** (REQUIRED)
   - Location: `specs/<feature_name>/plan.md`
   - Contains: Technical architecture, module structure
   - Provides: Source code locations and dependencies

3. **Source code** (REQUIRED)
   - Location: `src/` directory
   - Contains: Implementation code to be analyzed
   - Provides: Code to scan for quality issues

4. **Test code** (OPTIONAL but recommended)
   - Location: `tests/` directory
   - Contains: Test suites from Phase 4
   - Provides: Test coverage data

---

## 🎯 Your task

Set up SonarQube and generate comprehensive code quality reports that:

1. **Identify code quality issues** (bugs, code smells, duplications)
2. **Detect security vulnerabilities** (OWASP top 10, security hotspots)
3. **Measure test coverage** (integrate with pytest coverage)
4. **Check maintainability** (complexity, technical debt)
5. **Enforce quality gates** (fail build if quality standards not met)

---

## 📤 Output format (SonarQube setup and reports)

Generate SonarQube setup and configuration following this structure:

---

## SonarQube Analysis Command

**Feature:** <feature_name>
**Module:** <module_name> (from plan.md Section 2)
**Based on:** 
- `specs/<feature_name>/spec.md` (quality requirements)
- `specs/<feature_name>/plan.md` (module structure)
- Source code in `src/` directory

---

## Step 1: SonarQube installation

### Option A: Docker (Recommended for local development)

```bash
# Pull SonarQube docker image
docker pull sonarqube:latest

# Start SonarQube container
docker run -d --name sonarqube \
  -p 9000:9000 \
  -e SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true \
  sonarqube:latest

# Wait for SonarQube to start (takes 1-2 minutes)
# Access at: http://localhost:9000
# Default credentials: admin/admin (change on first login)
```

### Option B: SonarQube scanner CLI (For CI/CD)

```bash
# Download SonarQube scanner
wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-linux.zip
unzip sonar-scanner-cli-5.0.1.3006-linux.zip
export PATH=$PATH:$(pwd)/sonar-scanner-5.0.1.3006-linux/bin

# Verify installation
sonar-scanner --version
```

### Option C: Using Python package

```bash
# Install sonar-scanner as Python package
uv add --dev sonar-scanner
```

---

## Step 2: SonarQube server setup

### 2.1 Initial login

1. Open browser: `http://localhost:9000`
2. Login with: `admin/admin`
3. Change password when prompted
4. Complete setup wizard

### 2.2 Create project

1. Click **"Create Project"** → **"Manually"**
2. **Project key:** `your-project-key` (e.g., `innoshop-backend`)
3. **Display name:** `Your project name` (e.g., `Innoshop backend`)
4. Click **"Set up"**

### 2.3 Generate authentication token

1. Click **"Generate token"**
2. **Token name:** `local-dev` or `ci-cd`
3. **Type:** `Project analysis token`
4. **Expires in:** `90 days` (or `No expiration` for CI/CD)
5. Click **"Generate"**
6. **Copy token** (you won't see it again!)

Example token: `sqp_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0`

### 2.4 Configure quality gate (Optional)

1. Go to **"Quality gates"** → **"Create"**
2. Set custom thresholds:
   - **Coverage:** Minimum 80%
   - **Duplicated lines:** Maximum 3%
   - **Maintainability rating:** A
   - **Reliability rating:** A
   - **Security rating:** A
   - **Security hotspots reviewed:** 100%

---

## Step 3: Project configuration

### Option A: Using sonar-project.properties (Recommended)

Create `sonar-project.properties` in your project root:

```properties
# Project identification
sonar.projectKey=your-project-key
sonar.projectName=Your project name
sonar.projectVersion=1.0.0

# Source code
sonar.sources=src
sonar.tests=tests

# Python specific settings
sonar.python.version=3.11
sonar.language=py

# Coverage report (from pytest)
sonar.python.coverage.reportPaths=coverage.xml

# Exclusions
sonar.exclusions=\
  **/*_test.py,\
  **/test_*.py,\
  **/tests/**,\
  **/__pycache__/**,\
  **/.pytest_cache/**,\
  **/.venv/**,\
  **/migrations/**,\
  **/alembic/versions/**

# Test exclusions
sonar.test.exclusions=\
  **/tests/**,\
  **/*_test.py,\
  **/test_*.py

# Encoding
sonar.sourceEncoding=UTF-8

# Additional settings
sonar.python.pylint.reportPaths=pylint-report.txt
sonar.python.bandit.reportPaths=bandit-report.json
```

### Option B: Using command line parameters

If you prefer not to use `sonar-project.properties`:

```bash
sonar-scanner \
  -Dsonar.projectKey=your-project-key \
  -Dsonar.projectName="Your project name" \
  -Dsonar.projectVersion=1.0.0 \
  -Dsonar.sources=src \
  -Dsonar.tests=tests \
  -Dsonar.python.version=3.11 \
  -Dsonar.python.coverage.reportPaths=coverage.xml \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=your-token-here
```

---

## Step 4: Generate test coverage report

SonarQube requires coverage data in XML format. Generate it using pytest:

```bash
# Install coverage tools (if not already installed)
uv add --dev pytest pytest-cov pytest-asyncio

# Generate coverage report for SonarQube
pytest tests/ \
  --cov=src \
  --cov-report=xml:coverage.xml \
  --cov-report=html:htmlcov \
  --cov-report=term \
  -v

# Verify coverage.xml was created
ls -lh coverage.xml
```

**Coverage report locations:**
- **XML (for SonarQube):** `coverage.xml`
- **HTML (for humans):** `htmlcov/index.html`
- **Terminal:** Displayed during test run

---

## Step 5: Run SonarQube analysis

### Basic scan

```bash
# Run SonarQube scanner
sonar-scanner \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=your-token-here

# Wait for analysis to complete
# Check results at: http://localhost:9000/dashboard?id=your-project-key
```

### Advanced scan with additional checks

```bash
# Run pylint (optional, for additional Python checks)
uv add --dev pylint
pylint src/ --output-format=parseable > pylint-report.txt || true

# Run bandit (security checks)
uv add --dev bandit
bandit -r src/ -f json -o bandit-report.json || true

# Generate coverage
pytest tests/ --cov=src --cov-report=xml:coverage.xml -v

# Run SonarQube scan with all reports
sonar-scanner \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=your-token-here \
  -Dsonar.python.coverage.reportPaths=coverage.xml \
  -Dsonar.python.pylint.reportPaths=pylint-report.txt \
  -Dsonar.python.bandit.reportPaths=bandit-report.json
```

---

## Step 6: Analyze results

### 6.1 Access SonarQube dashboard

Open: `http://localhost:9000/dashboard?id=your-project-key`

### 6.2 Review key metrics

**Overview tab:**
- **Bugs:** Critical issues that could cause failures
- **Vulnerabilities:** Security issues (OWASP top 10)
- **Security hotspots:** Code that needs security review
- **Code smells:** Maintainability issues
- **Coverage:** Test coverage percentage
- **Duplications:** Duplicate code blocks

**Quality gate status:**
- ✅ **PASSED:** All quality criteria met
- ❌ **FAILED:** One or more criteria not met

### 6.3 Review issues by severity

**Severity levels:**
1. **Blocker:** Must fix immediately (blocks deployment)
2. **Critical:** Should fix before deployment
3. **Major:** Should fix soon
4. **Minor:** Nice to fix
5. **Info:** Informational only

### 6.4 Review security issues

**Security categories:**
- **SQL injection:** Unsafe database queries
- **XSS vulnerabilities:** Unsafe HTML rendering
- **Authentication issues:** Weak authentication
- **Authorization issues:** Missing access controls
- **Cryptography issues:** Weak encryption
- **Sensitive data exposure:** Logging secrets

---

## Step 7: Fix issues

### Priority order for fixing:

1. **Blockers and critical vulnerabilities** (Fix immediately)
2. **Critical bugs** (Fix before deployment)
3. **Major code smells** (Fix during implementation)
4. **Coverage gaps** (Add missing tests)
5. **Minor issues** (Fix when time permits)

### Example fixes:

**Issue:** SQL injection vulnerability
```python
# ❌ Wrong - vulnerable to SQL injection
query = f"SELECT * FROM users WHERE email = '{email}'"

# ✅ Correct - using parameterized query
query = "SELECT * FROM users WHERE email = $1"
result = await conn.fetch(query, email)
```

**Issue:** Hard-coded secret
```python
# ❌ Wrong - hard-coded API key
api_key = "sk_live_1234567890abcdef"

# ✅ Correct - using environment variable
api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API_KEY environment variable not set")
```

**Issue:** Cognitive complexity too high
```python
# ❌ Wrong - function too complex (complexity > 15)
def process_order(order):
    if order.status == "pending":
        if order.payment_method == "credit_card":
            if order.amount > 1000:
                # ... 50 lines of nested logic
                pass
    return result

# ✅ Correct - break into smaller functions
def process_order(order):
    validate_order(order)
    payment_result = process_payment(order)
    return create_order_record(order, payment_result)
```

---

## Step 8: Re-run analysis

After fixing issues, re-run the analysis:

```bash
# Generate fresh coverage
pytest tests/ --cov=src --cov-report=xml:coverage.xml -v

# Run SonarQube scan again
sonar-scanner \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=your-token-here

# Check if quality gate passed
# http://localhost:9000/dashboard?id=your-project-key
```

---

## Step 9: CI/CD integration

### GitHub actions example:

Create `.github/workflows/sonarqube.yml`:

```yaml
name: SonarQube analysis

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  sonarqube:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
        with:
          fetch-depth: 0  # Full git history for better analysis
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install uv
          uv sync
      
      - name: Run tests with coverage
        run: |
          uv run pytest tests/ \
            --cov=src \
            --cov-report=xml:coverage.xml \
            -v
      
      - name: SonarQube scan
        uses: sonarsource/sonarqube-scan-action@master
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
      
      - name: SonarQube quality gate check
        uses: sonarsource/sonarqube-quality-gate-action@master
        timeout-minutes: 5
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

### GitLab CI example:

Add to `.gitlab-ci.yml`:

```yaml
sonarqube-check:
  stage: test
  image: 
    name: sonarsource/sonar-scanner-cli:latest
    entrypoint: [""]
  variables:
    SONAR_USER_HOME: "${CI_PROJECT_DIR}/.sonar"
    GIT_DEPTH: "0"
  cache:
    key: "${CI_JOB_NAME}"
    paths:
      - .sonar/cache
  script:
    - pip install uv
    - uv sync
    - uv run pytest tests/ --cov=src --cov-report=xml:coverage.xml -v
    - sonar-scanner
      -Dsonar.host.url=$SONAR_HOST_URL
      -Dsonar.login=$SONAR_TOKEN
  only:
    - merge_requests
    - main
    - develop
```

---

## Quality checklist

### Before running SonarQube:

- [ ] All tests passing (`pytest tests/ -v`)
- [ ] Coverage report generated (`coverage.xml` exists)
- [ ] SonarQube server running (`http://localhost:9000`)
- [ ] Authentication token configured
- [ ] `sonar-project.properties` created and validated

### SonarQube quality gates:

- [ ] **No blocker issues** (0 blockers)
- [ ] **No critical vulnerabilities** (0 critical security issues)
- [ ] **Test coverage ≥ 80%** (from spec.md requirements)
- [ ] **Maintainability rating: A or B** (technical debt ratio < 10%)
- [ ] **Reliability rating: A or B** (bug density < 1%)
- [ ] **Security rating: A** (no vulnerabilities)
- [ ] **Security hotspots: 100% reviewed** (all security-sensitive code reviewed)
- [ ] **Duplicated lines < 3%** (minimal code duplication)
- [ ] **Cognitive complexity < 15** (per function)

### After SonarQube analysis:

- [ ] Quality gate status: **PASSED** ✅
- [ ] All blocker and critical issues resolved
- [ ] Security vulnerabilities addressed
- [ ] Code smells reduced (< 10 major smells)
- [ ] Technical debt < 5% (less than 5% of development time for fixes)
- [ ] Coverage meets requirements (from spec.md)

---

## Common issues and solutions

### Issue 1: SonarQube server not starting

**Problem:**
```bash
docker: Error response from daemon: Conflict. The container name "/sonarqube" is already in use
```

**Solution:**
```bash
# Remove existing container
docker rm -f sonarqube

# Start fresh
docker run -d --name sonarqube -p 9000:9000 sonarqube:latest
```

### Issue 2: Coverage report not found

**Problem:**
```
WARN: Coverage report 'coverage.xml' not found
```

**Solution:**
```bash
# Generate coverage before running SonarQube
pytest tests/ --cov=src --cov-report=xml:coverage.xml -v

# Verify file exists
ls -lh coverage.xml

# Then run SonarQube
sonar-scanner
```

### Issue 3: Authentication failed

**Problem:**
```
ERROR: Error during SonarQube Scanner execution
ERROR: Not authorized. Please check the user token
```

**Solution:**
```bash
# Generate new token from SonarQube UI
# Administration → Security → Users → Tokens

# Use token in command
sonar-scanner -Dsonar.login=your-new-token-here
```

### Issue 4: Quality gate failed

**Problem:**
```
Quality Gate Status: FAILED
- Coverage is 65.2% (required ≥ 80%)
- 3 critical bugs found
```

**Solution:**
```bash
# Fix critical bugs first (check SonarQube dashboard)
# Add missing tests to increase coverage

# Run tests
pytest tests/ --cov=src --cov-report=xml:coverage.xml --cov-report=term -v

# Check coverage in terminal (should show ≥ 80%)
# Re-run SonarQube
sonar-scanner
```

### Issue 5: Too many false positives

**Problem:**
SonarQube reports issues in generated code, migrations, or third-party files.

**Solution:**
Add to `sonar-project.properties`:

```properties
# Exclude generated code
sonar.exclusions=\
  **/migrations/**,\
  **/alembic/versions/**,\
  **/pb2.py,\
  **/pb2_grpc.py,\
  **/__pycache__/**,\
  **/.venv/**

# Or mark as false positive in SonarQube UI
# Issues → Select issue → Mark as false positive
```

---

## Integration with SDD workflow

### When to run SonarQube:

**Primary use case (RECOMMENDED):**

**After Phase 5 (Implementation) ← MAIN USE CASE:**
- ✅ Validate production code quality
- ✅ Check security vulnerabilities  
- ✅ Measure final test coverage
- ✅ Verify all quality gates passed
- ✅ This is when you have complete code to analyze

**Secondary use cases:**

**Before git commit:**
- Run as pre-commit hook
- Fail commit if quality gate fails
- Ensure only quality code is committed

**In CI/CD pipeline:**
- Automated quality checks on every PR
- Block merge if quality gate fails
- Track quality metrics over time

### Correct workflow (TDD + SonarQube):

```bash
# Phase 4: Write tests FIRST (TDD)
pytest tests/ -v
# Tests will FAIL (no implementation yet) - this is correct!

# Phase 5: Implement code
# ... write implementation code ...

# Verify tests now PASS
pytest tests/ -v
# Tests should PASS now (implementation exists)

# Phase 6: Run SonarQube AFTER implementation ← YOU ARE HERE
pytest tests/ --cov=src --cov-report=xml:coverage.xml -v
sonar-scanner

# Check quality gate status
# http://localhost:9000/dashboard?id=your-project-key
# Quality gate should be: PASSED ✅

# If quality gate PASSED → Ready to commit
# If quality gate FAILED → Fix issues and re-run
```

### Summary: Correct order

```
1. Phase 4: Write tests (TDD) → Tests FAIL ❌
2. Phase 5: Implement code → Tests PASS ✅
3. Phase 6: Run SonarQube → Quality gate PASSED ✅ ← YOU RUN THIS AFTER IMPLEMENTATION
4. Commit code → Ready for deployment 🚀
```

---

## SonarQube quality report template

After running SonarQube, document results:

```markdown
## SonarQube quality report

**Feature:** <feature_name>
**Analysis date:** <date>
**Analyst:** <your_name>

### Quality gate status
- [ ] ✅ PASSED / ❌ FAILED

### Metrics summary
- **Bugs:** 0 (Threshold: 0)
- **Vulnerabilities:** 0 (Threshold: 0)
- **Security hotspots:** 0 open (Threshold: 100% reviewed)
- **Code smells:** 5 (Threshold: < 10 major)
- **Coverage:** 85.2% (Threshold: ≥ 80%)
- **Duplications:** 1.2% (Threshold: < 3%)
- **Maintainability rating:** A (Threshold: A or B)
- **Reliability rating:** A (Threshold: A or B)
- **Security rating:** A (Threshold: A)

### Issues found
| Severity | Type | Count | Status |
|----------|------|-------|--------|
| Blocker | Bug | 0 | ✅ Fixed |
| Critical | Vulnerability | 0 | ✅ Fixed |
| Major | Code smell | 3 | 🔄 In progress |
| Minor | Code smell | 2 | ⏳ Planned |

### Actions taken
1. Fixed SQL injection in `user_repository.py`
2. Removed hard-coded API key in `config.py`
3. Reduced cognitive complexity in `order_service.py`
4. Added tests for uncovered edge cases

### Recommendations
- Consider refactoring `large_function()` (complexity: 18)
- Add integration tests for error handling paths
- Review security hotspot in authentication flow

### Links
- **Dashboard:** http://localhost:9000/dashboard?id=your-project-key
- **Coverage report:** htmlcov/index.html
- **Issues:** http://localhost:9000/project/issues?id=your-project-key
```

---

## Best practices

### Code quality:

1. **Run SonarQube early and often** (not just at the end)
2. **Fix blockers immediately** (don't accumulate technical debt)
3. **Review security hotspots** (even if marked as safe)
4. **Aim for A ratings** (maintainability, reliability, security)
5. **Monitor trends** (quality should improve over time)

### Test coverage:

1. **Aim for 80%+ coverage** (from spec.md requirements)
2. **Cover edge cases** (not just happy paths)
3. **Test error handling** (exceptions, validation errors)
4. **Test integration points** (database, external APIs)
5. **Avoid testing implementation details** (test behavior, not internals)

### Security:

1. **Review all vulnerabilities** (even if low severity)
2. **Don't ignore security hotspots** (review and mark as safe if appropriate)
3. **Follow OWASP top 10** (built into SonarQube rules)
4. **Scan dependencies** (use separate tools like `safety` or `bandit`)
5. **Update SonarQube rules** (add custom rules for your tech stack)

### Maintainability:

1. **Keep functions small** (< 50 lines, cognitive complexity < 15)
2. **Reduce duplication** (DRY principle)
3. **Use meaningful names** (avoid generic names like `data`, `result`)
4. **Follow coding standards** (PEP 8 for Python)
5. **Document complex logic** (docstrings, comments)

---

## Advanced configuration

### Custom quality profile:

1. Go to **Quality profiles** → **Create**
2. Select **Python** → **Extend** Sonar way
3. Add/remove rules based on your needs:
   - Enable stricter rules for critical modules
   - Disable rules for legacy code
   - Add custom regex rules

### Branch analysis:

```bash
# Analyze specific branch
sonar-scanner \
  -Dsonar.branch.name=feature/new-feature \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=your-token

# Compare branches
# View in SonarQube UI: Activity → Compare versions
```

### Pull request decoration:

Configure SonarQube to comment on pull requests:

1. **Settings** → **Configuration** → **Pull requests**
2. Configure GitHub/GitLab integration
3. Add webhook for PR events
4. SonarQube will comment on PRs with quality issues

---

## Resources

### Official documentation:
- **SonarQube docs:** https://docs.sonarqube.org/latest/
- **Python analyzer:** https://docs.sonarqube.org/latest/analyzing-source-code/languages/python/
- **Quality gates:** https://docs.sonarqube.org/latest/user-guide/quality-gates/

### Additional tools:
- **Bandit:** Security linter for Python
- **Pylint:** Python code analyzer
- **Safety:** Dependency vulnerability scanner
- **Black:** Code formatter (prevents style issues)

### SonarQube rules:
- **Python rules:** https://rules.sonarsource.com/python
- **Security rules:** Based on OWASP top 10, CWE, SANS top 25

---

## Appendix: Quick reference commands

### Setup:
```bash
# Start SonarQube
docker run -d --name sonarqube -p 9000:9000 sonarqube:latest

# Install scanner
uv add --dev sonar-scanner
```

### Analysis:
```bash
# Generate coverage
pytest tests/ --cov=src --cov-report=xml:coverage.xml -v

# Run scan
sonar-scanner -Dsonar.host.url=http://localhost:9000 -Dsonar.login=your-token
```

### Check results:
```bash
# Open dashboard
xdg-open http://localhost:9000/dashboard?id=your-project-key

# View in terminal (requires jq)
curl -u your-token: \
  "http://localhost:9000/api/qualitygates/project_status?projectKey=your-project-key" \
  | jq '.projectStatus.status'
```

---

**End of SonarQube analysis guide**
