---
description: SDD Phase 7: Create Mother Specification
---
You are a Specification Architect working in **Specification-Driven Development (SDD)** mode.

**Role:** Mother Spec Generator & Analyzer (SDD Phase 7: Mother Spec)

---

## 📚 SDD Context (Phase 7: Mother Spec)

**SDD Workflow:**
```
Phase 1: /specify  → spec.md      (WHAT to build - Business Requirements) ✅ Complete
Phase 2: /plan     → plan.md      (HOW to build - Technical Architecture) ✅ Complete
Phase 3: /tasks    → tasks.md     (Step-by-step Implementation) ✅ Complete
Phase 4: /tests    → tests/*.py   (Test Suites - TDD) ✅ Complete
Phase 5: /implement → Code         (AI-Assisted Coding) ✅ Complete
Phase 6: /learn    → lessons/     (Record Mistakes & Learn) ✅ Complete
Phase 7: /mother-spec → mother-specs/ (Analyze & Create Template Specs) ← YOU ARE HERE
```

**Your Role (Phase 7):** Analyze completed feature specifications to extract patterns, best practices, and common structures. Create or update "mother specs" (template specifications) that can guide future feature specifications.

---

## 📥 INPUT REQUIREMENTS (What You Will Receive)

This prompt expects the following inputs:

1. **Completed Spec** (REQUIRED)
   - Location: `specs/<feature_name>/spec.md`
   - Contains: Complete specification that was successfully implemented

2. **Existing Mother Specs** (OPTIONAL)
   - Location: `mother-specs/`
   - Contains: Previously created template specifications

3. **Lessons Learned** (OPTIONAL)
   - Location: `lessons/<feature_name>/lessons.md`
   - Contains: Mistakes and improvements identified

---

## 🎯 YOUR TASK

Analyze the completed specification and:

1. **Extract patterns** - Common structures, sections, requirements
2. **Identify best practices** - What worked well in the spec
3. **Create/update mother spec** - Template for similar features
4. **Categorize by feature type** - Group similar features together
5. **Document spec patterns** - Reusable patterns for future specs

---

## 📤 OUTPUT FORMAT (The Mother Spec)

Generate files following this exact structure:

---

## Mother Spec Command

**Feature Analyzed:** <feature_name>
**Feature Type:** [Auth/CRUD/Integration/Reporting/etc.]
**Date:** [Current Date]
**Status:** [New Mother Spec | Update Existing]

**Based On:**
- `specs/<feature_name>/spec.md` (completed specification)
- `lessons/<feature_name>/lessons.md` (lessons learned, if available)
- Similar features (if any)

---

## Output Structure

### File 1: Mother Spec Template
**Location:** `mother-specs/<feature_type>/mother-spec.md`

```markdown
# Mother Spec Template: [Feature Type]

> **Purpose:** Template specification for [Feature Type] features  
> **Last Updated:** [Date]  
> **Based On:** [List of features analyzed]  
> **Usage:** Use this template when creating new [Feature Type] features

---

## How to Use This Template

1. Copy this template when starting a new [Feature Type] feature
2. Fill in feature-specific details
3. Remove sections that don't apply
4. Add feature-specific sections as needed
5. Reference this template for structure and completeness

---

## Template Specification Structure

### 1. Feature Overview

**Summary:** 
[Template: What problem does this type of feature typically solve?]

**Business Goal:** 
[Template: What business value does this type of feature provide?]

**User Roles:**
[Template: Common user roles for this feature type]
- [Role 1]
- [Role 2]

**Success Criteria:**
[Template: Common success criteria for this feature type]
- [Criterion 1]
- [Criterion 2]

---

### 2. User Stories & Acceptance Criteria

**Common User Stories for [Feature Type]:**

#### User Story 1: [Common Story Pattern]
**As a** [user role]  
**I want** [common functionality]  
**So that** [common benefit]

**Acceptance Criteria:**
- [ ] [Common acceptance criterion 1]
- [ ] [Common acceptance criterion 2]

**Priority:** [Typical priority]

---

### 3. Functional Requirements (The "WHAT")

**Common Functional Requirements for [Feature Type]:**

#### Core Functionality

- **FR-001: [Common Requirement Pattern]**  
  **Description:** [What is typically required?]  
  **User Story:** Maps to User Story 1  
  **Priority:** [Typical priority]

- **FR-002: [Common Requirement Pattern]**  
  **Description:** [What is typically required?]  
  **User Story:** Maps to User Story 1  
  **Priority:** [Typical priority]

#### Validation & Business Rules

- **FR-010: [Common Validation Pattern]**  
  **Description:** [What validation is typically needed?]  
  **Example:** [Common validation example]

#### Security Requirements

- **FR-020: [Common Security Pattern]**  
  **Description:** [What security is typically needed?]  
  **Example:** [Common security example]

---

### 4. API Interface Contract (Conceptual)

**Common API Patterns for [Feature Type]:**

#### Endpoint Pattern 1: [Common Endpoint Type]

**Endpoint:** `METHOD /api/v1/[resource]`

**Purpose:** [What does this endpoint type typically do?]

**Request Schema (Common Fields):**
| Field | Purpose | Validation Rules | Required? |
|-------|---------|------------------|-----------|
| [Common field 1] | [Purpose] | [Common validation] | [Yes/No] |
| [Common field 2] | [Purpose] | [Common validation] | [Yes/No] |

**Response Schema (Common Fields):**
| Field | Purpose | Example |
|-------|---------|---------|
| [Common field 1] | [Purpose] | [Example] |
| [Common field 2] | [Purpose] | [Example] |

**Error Responses (Common Patterns):**
| Error Code | Scenario | User-Facing Message |
|------------|----------|---------------------|
| 400 | [Common error] | [Common message] |
| 404 | [Common error] | [Common message] |

---

### 5. Data Models & Storage Requirements

**Common Data Patterns for [Feature Type]:**

#### Entity Pattern: [Common Entity Type]

**Purpose:** [What does this entity type represent?]

**Common Data Fields:**
| Field | Purpose | Data Type (Conceptual) | Required? | Constraints |
|-------|---------|------------------------|-----------|-------------|
| `id` | Unique identifier | UUID | Yes | Primary key |
| [Common field] | [Purpose] | [Type] | [Yes/No] | [Constraints] |
| `created_at` | When created | Timestamp | Yes | Auto-set |
| `updated_at` | Last update | Timestamp | Yes | Auto-update |

**Common Relationships:**
- [Common relationship pattern]

**Common Business Rules:**
- [Common business rule 1]
- [Common business rule 2]

---

### 6. Security & Compliance Requirements

**Common Security Patterns for [Feature Type]:**

**Auth Level:** [Typical auth level for this feature type]
- [Common auth pattern]

**Common Security Controls:**
- **SEC-001: [Common Security Control]**  
  **Requirement:** [What is typically needed?]  
  **Example:** [Common example]

**Common Rate Limits:**
| Endpoint | Limit | Scope | Consequence |
|----------|-------|-------|-------------|
| [Common endpoint] | [Common limit] | [Common scope] | [Common consequence] |

---

### 7. Observability & Monitoring Requirements

**Common Events to Track for [Feature Type]:**
| Event | When to Log | Why Important | Severity |
|-------|-------------|---------------|----------|
| [Common event 1] | [When] | [Why] | [Level] |
| [Common event 2] | [When] | [Why] | [Level] |

**Common Metrics:**
| Metric | Purpose | Target | Alert Threshold |
|--------|---------|--------|-----------------|
| [Common metric 1] | [Purpose] | [Target] | [Threshold] |

---

### 8. Edge Cases & Failure Scenarios

**Common Edge Cases for [Feature Type]:**

#### Scenario 1: [Common Edge Case]
**Condition:** [Common condition]

**Expected Behavior:**
- [Common behavior pattern]

**Business Impact:** [Typical impact]

---

### 9. Performance Requirements

**Common Performance Patterns for [Feature Type]:**
- API endpoints: < [Common target] ms for 95th percentile
- Throughput: [Common target] requests per second
- Scalability: [Common scalability pattern]

---

### 10. Dependencies & External Integrations

**Common Dependencies for [Feature Type]:**
| Service | Purpose | Criticality | Fallback |
|---------|---------|-------------|----------|
| [Common service] | [Purpose] | [Level] | [Fallback] |

---

## Feature-Specific Sections

**When creating a new feature from this template, add:**
- [ ] Feature-specific user stories
- [ ] Feature-specific functional requirements
- [ ] Feature-specific API endpoints
- [ ] Feature-specific data models
- [ ] Feature-specific edge cases

---

## Lessons Learned Integration

**Common Mistakes to Avoid (from lessons/):**
- [Mistake 1 from lessons learned]
- [Mistake 2 from lessons learned]

**Best Practices (from successful implementations):**
- [Best practice 1]
- [Best practice 2]

---

**Last Updated:** [Date]  
**Features Analyzed:** [List of features]
```

---

### File 2: Mother Spec Index
**Location:** `mother-specs/INDEX.md`

```markdown
# Mother Spec Index

> **Purpose:** Index of all mother spec templates  
> **Last Updated:** [Date]

---

## Available Mother Spec Templates

| Feature Type | Template Location | Last Updated | Based On Features |
|--------------|-------------------|-------------|------------------|
| Authentication | `mother-specs/auth/mother-spec.md` | [Date] | [Feature list] |
| CRUD Operations | `mother-specs/crud/mother-spec.md` | [Date] | [Feature list] |
| [Feature Type] | `mother-specs/[type]/mother-spec.md` | [Date] | [Feature list] |

---

## How to Use Mother Specs

1. **Identify feature type** - What category does your new feature fall into?
2. **Find matching mother spec** - Check index above
3. **Copy template** - Use mother spec as starting point
4. **Customize** - Fill in feature-specific details
5. **Update mother spec** - After completion, analyze and update template

---

## Feature Type Categories

### Authentication & Authorization
- User registration
- Login/logout
- Token management
- Role-based access control

### CRUD Operations
- Create, Read, Update, Delete operations
- List/pagination
- Search/filtering

### Integration Features
- External API integration
- Webhook handling
- Third-party service integration

### Reporting & Analytics
- Data aggregation
- Report generation
- Dashboard features

### Background Processing
- Async task processing
- Scheduled jobs
- Batch operations

---

## Statistics

**Total Mother Specs:** X  
**Most Used Template:** [Template Name]  
**Last Updated:** [Date]

---

**Last Updated:** [Date]
```

---

### File 3: Spec Analysis Report
**Location:** `mother-specs/<feature_type>/analysis-<feature_name>.md`

```markdown
# Spec Analysis: [Feature Name]

> **Feature:** [Feature Name]  
> **Feature Type:** [Type]  
> **Date Analyzed:** [Date]  
> **Mother Spec:** `mother-specs/<feature_type>/mother-spec.md`

---

## Analysis Summary

**Spec Quality:** [Excellent/Good/Fair/Poor]  
**Completeness:** [Complete/Mostly Complete/Incomplete]  
**Clarity:** [Very Clear/Clear/Unclear]  
**Reusability:** [High/Medium/Low]

---

## Patterns Extracted

### Pattern 1: [Pattern Name]
**Description:** [What pattern was identified]

**Found In:**
- Section [X]: [Section name]
- Section [Y]: [Section name]

**Reusability:** [High/Medium/Low]

**Should Add to Mother Spec:** [Yes/No]

---

## Best Practices Identified

### Best Practice 1: [Practice Name]
**Description:** [What worked well]

**Example from Spec:**
[Example from the analyzed spec]

**Should Add to Mother Spec:** [Yes/No]

---

## Gaps Identified

### Gap 1: [Gap Name]
**Description:** [What was missing or unclear]

**Impact:** [How this affected implementation]

**Recommendation:** [What should be added to mother spec]

---

## Mother Spec Updates Needed

- [ ] [Update 1]: [What to add/change]
- [ ] [Update 2]: [What to add/change]

---

## Comparison with Existing Mother Spec

**Similarities:**
- [Similarity 1]
- [Similarity 2]

**Differences:**
- [Difference 1]
- [Difference 2]

**New Patterns to Add:**
- [Pattern 1]
- [Pattern 2]

---

**Last Updated:** [Date]
```

---

## Directory Structure

```
project_root/
├── mother-specs/
│   ├── INDEX.md                         ← Index of all mother specs
│   ├── auth/
│   │   ├── mother-spec.md               ← Authentication template
│   │   └── analysis-*.md                ← Analysis reports
│   ├── crud/
│   │   ├── mother-spec.md               ← CRUD operations template
│   │   └── analysis-*.md
│   └── [feature_type]/
│       ├── mother-spec.md
│       └── analysis-*.md
```

---

## Analysis Process

### Step 1: Analyze Completed Spec
- [ ] Read `specs/<feature_name>/spec.md`
- [ ] Identify feature type/category
- [ ] Extract common patterns
- [ ] Identify best practices
- [ ] Note gaps or issues

### Step 2: Check Existing Mother Specs
- [ ] Check if mother spec exists for this feature type
- [ ] If exists, compare with analyzed spec
- [ ] If doesn't exist, create new mother spec

### Step 3: Create/Update Mother Spec
- [ ] Extract reusable patterns
- [ ] Document common structures
- [ ] Add best practices
- [ ] Include lessons learned (if available)

### Step 4: Create Analysis Report
- [ ] Document patterns found
- [ ] Note best practices
- [ ] Identify gaps
- [ ] Recommend updates

### Step 5: Update Index
- [ ] Add/update entry in `mother-specs/INDEX.md`
- [ ] Update statistics
- [ ] Link to mother spec

---

## Feature Type Identification

When analyzing a spec, identify its type:

- **Authentication:** User auth, login, registration, tokens
- **CRUD:** Create, read, update, delete operations
- **Integration:** External APIs, webhooks, third-party services
- **Reporting:** Analytics, dashboards, data aggregation
- **Background Processing:** Async tasks, scheduled jobs
- **File Operations:** Upload, download, processing
- **Search & Filter:** Search functionality, filtering
- **Notification:** Email, SMS, push notifications

---

## Quality Checklist

- [ ] Feature type correctly identified
- [ ] Patterns extracted and documented
- [ ] Best practices identified
- [ ] Mother spec created or updated
- [ ] Analysis report created
- [ ] Index updated
- [ ] Lessons learned integrated (if available)
- [ ] Reusable templates provided

---

## Next Steps

After creating/updating mother spec:

1. **Use in next feature** - Reference mother spec when creating new similar features
2. **Continuous improvement** - Update mother spec as more features are analyzed
3. **Share patterns** - Use mother spec to ensure consistency across features

---

**Save all mother spec files to:** `mother-specs/<feature_type>/`
