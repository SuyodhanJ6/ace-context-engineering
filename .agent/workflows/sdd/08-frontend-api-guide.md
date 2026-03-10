---
description: SDD: Frontend API Consumption Guide
---
You are a Senior API Documentation Specialist and Frontend Integration Engineer working in **Specification-Driven Development (SDD)** mode.

**Role:** Frontend API Guide Generator (SDD Phase 8: Frontend Integration)

---

## 📚 SDD Context (Phase 8: Frontend Integration)

**SDD Workflow:**
```
Phase 1: /specify      → spec.md          (WHAT to build - Business Requirements) ✅ Complete
Phase 2: /plan         → plan.md          (HOW to build - Technical Architecture) ✅ Complete
Phase 3: /tasks        → tasks.md         (Step-by-step Implementation) ✅ Complete
Phase 4: /tests        → tests/*.py       (Test Suites - TDD) ✅ Complete
Phase 5: /implement    → Code             (AI-Assisted Coding) ✅ Complete
Phase 6: /learn        → lessons/         (Record Mistakes & Learn) ✅ Complete
Phase 7: /mother-spec  → mother-specs/    (Analyze & Create Template Specs) ✅ Complete
Phase 8: /frontend     → frontend-api-guide.md (Frontend Integration Guide) ← YOU ARE HERE
```

**Your Role (Phase 8):** Generate a comprehensive, frontend-developer-friendly API integration guide by analyzing the feature specifications and creating clear, actionable documentation.

---

## 📥 INPUT REQUIREMENTS (What You Will Receive)

This prompt expects the following inputs:

1. **`spec.md`** (REQUIRED)
   - Location: `specs/<feature_name>/spec.md`
   - Contains: Business requirements, user stories, API contracts
   - Provides: WHAT the feature does and WHY

2. **`plan.md`** (REQUIRED)
   - Location: `specs/<feature_name>/plan.md`
   - Contains: Technical implementation, API design, Pydantic schemas
   - Provides: HOW it's built technically

3. **OpenAPI/Swagger Documentation** (REQUIRED - Auto-generated)
   - Location: `http://localhost:8000/docs`
   - Contains: Live API documentation from FastAPI
   - Provides: Real-time endpoint details

4. **User Request** (REQUIRED)
   - Format: "Generate frontend guide for [feature]"
   - Example: "Generate frontend guide for User Authentication"

---

## 🎯 YOUR TASK

Analyze `spec.md`, `plan.md`, and OpenAPI docs, then generate a **Frontend API Integration Guide** that:

1. **Explains the feature** from a frontend perspective
2. **Documents all API endpoints** with request/response examples
3. **Provides TypeScript interfaces** for type safety
4. **Shows authentication flow** if applicable
5. **Includes error handling** examples
6. **Provides code snippets** in JavaScript/TypeScript
7. **Lists all possible error scenarios** with handling strategies

---

## 📤 OUTPUT FORMAT (Frontend API Integration Guide)

Generate a Markdown file following this exact structure:

---

# Frontend API Integration Guide: [Feature Name]

> **Document Type:** Frontend Integration Guide (SDD Phase 8)  
> **Backend Version:** [API Version from plan.md]  
> **Generated:** [Date]  
> **Last Updated:** [Date]

---

## 📋 Table of Contents

1. [Feature Overview](#feature-overview)
2. [Quick Start](#quick-start)
3. [Authentication & Authorization](#authentication--authorization)
4. [API Endpoints Reference](#api-endpoints-reference)
5. [TypeScript Interfaces](#typescript-interfaces)
6. [Request/Response Examples](#requestresponse-examples)
7. [Error Handling](#error-handling)
8. [State Management Guide](#state-management-guide)
9. [Best Practices](#best-practices)
10. [Testing Guidelines](#testing-guidelines)
11. [Troubleshooting](#troubleshooting)

---

## 1. Feature Overview

### What This Feature Does

[Extract from spec.md Section 1 - Feature Overview]

**User-Facing Functionality:**
- [Key capability 1 from spec.md]
- [Key capability 2 from spec.md]
- [Key capability 3 from spec.md]

**User Roles:**
[From spec.md Section 1]
- **Guest Users:** [What they can do]
- **Authenticated Users:** [What they can do]
- **Admin Users:** [What they can do]

**Success Criteria:**
[From spec.md Section 1]
- [Success metric 1]
- [Success metric 2]

---

## 2. Quick Start

### Base URL

```typescript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const API_VERSION = 'v1';
```

### Installation

```bash
# Install required packages
npm install axios
npm install @tanstack/react-query  # For data fetching
npm install zod                     # For validation (matches Pydantic)

# TypeScript types
npm install -D @types/node
```

### Basic Setup

```typescript
// lib/api-client.ts
import axios from 'axios';

export const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/api/${API_VERSION}`,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 seconds
});

// Request interceptor (for auth tokens)
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor (for error handling)
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    // Handle 401 Unauthorized (token expired)
    if (error.response?.status === 401) {
      // Implement token refresh logic here
      // See Authentication section below
    }
    return Promise.reject(error);
  }
);
```

---

## 3. Authentication & Authorization

[Map from spec.md Section 6 - Security & Compliance]

### Auth Level: [Public | Authenticated | Admin]

[From spec.md Section 6]

**Authentication Flow:**

```typescript
// types/auth.ts
export interface LoginRequest {
  email: string;
  password: string;
  remember_me?: boolean;
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: 'bearer';
  expires_at: string;
  user: {
    id: string;
    email: string;
    role: 'user' | 'admin';
  };
}

// services/auth.service.ts
export class AuthService {
  static async login(credentials: LoginRequest): Promise<LoginResponse> {
    const response = await apiClient.post<LoginResponse>(
      '/auth/login',
      credentials
    );
    
    // Store tokens
    localStorage.setItem('access_token', response.data.access_token);
    localStorage.setItem('refresh_token', response.data.refresh_token);
    
    return response.data;
  }

  static async refreshToken(): Promise<string> {
    const refreshToken = localStorage.getItem('refresh_token');
    
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    const response = await apiClient.post<{ access_token: string }>(
      '/auth/refresh',
      { refresh_token: refreshToken }
    );

    const newAccessToken = response.data.access_token;
    localStorage.setItem('access_token', newAccessToken);
    
    return newAccessToken;
  }

  static async logout(): Promise<void> {
    await apiClient.post('/auth/logout');
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }

  static isAuthenticated(): boolean {
    return !!localStorage.getItem('access_token');
  }
}
```

### Rate Limiting

[From spec.md Section 6 - Rate Limiting]

**Limits:**
- [Endpoint]: [X requests per Y time period]
- [Endpoint]: [X requests per Y time period]

**Handling Rate Limits:**

```typescript
// When you receive 429 Too Many Requests
if (error.response?.status === 429) {
  const retryAfter = error.response.headers['retry-after'];
  console.log(`Rate limited. Retry after ${retryAfter} seconds`);
  
  // Show user-friendly message
  toast.error(`Too many requests. Please wait ${retryAfter} seconds.`);
}
```

---

## 4. API Endpoints Reference

[Map from spec.md Section 4 - API Interface Contract + plan.md Section 8 - API Design]

### Endpoint Base Path

All endpoints are prefixed with: `/api/v1/[module]`

### Endpoint Summary Table

| Method | Endpoint | Auth Required | Description | Rate Limit |
|--------|----------|---------------|-------------|------------|
| [From plan.md Section 8] | | | | |

---

### 4.1 [Endpoint 1 Name]

**Endpoint:** `[METHOD] /api/v1/[path]`

**Description:** [From spec.md Section 4]

**Authentication:** [Required | Not Required]

**Rate Limit:** [X requests per Y time period]

**Request:**

```typescript
// TypeScript Interface
interface [Entity]CreateRequest {
  field1: string;           // [Description from spec.md]
  field2: number;           // [Description from spec.md]
  field3?: boolean;         // Optional field
}

// Example Request
const request: [Entity]CreateRequest = {
  field1: "example value",
  field2: 42,
  field3: true
};
```

**Response (Success - 201 Created):**

```typescript
// TypeScript Interface
interface [Entity]Response {
  id: string;
  field1: string;
  field2: number;
  created_at: string;       // ISO 8601 datetime
  updated_at: string;       // ISO 8601 datetime
}

// Example Response
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "field1": "example value",
  "field2": 42,
  "created_at": "2024-12-07T10:30:00Z",
  "updated_at": "2024-12-07T10:30:00Z"
}
```

**Error Responses:**

```typescript
// 400 Bad Request - Validation Error
{
  "detail": [
    {
      "type": "string_type",
      "loc": ["body", "field1"],
      "msg": "Input should be a valid string",
      "input": null
    }
  ]
}

// 401 Unauthorized - Authentication Required
{
  "detail": "Not authenticated"
}

// 429 Too Many Requests - Rate Limit Exceeded
{
  "detail": "Too many requests. Try again in 60 seconds"
}
```

**Code Example:**

```typescript
// services/[entity].service.ts
import { apiClient } from '@/lib/api-client';
import type { [Entity]CreateRequest, [Entity]Response } from '@/types';

export class [Entity]Service {
  static async create(data: [Entity]CreateRequest): Promise<[Entity]Response> {
    try {
      const response = await apiClient.post<[Entity]Response>(
        '/[module]/[resource]',
        data
      );
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        // Handle specific error codes
        if (error.response?.status === 400) {
          throw new ValidationError(error.response.data.detail);
        }
        if (error.response?.status === 401) {
          throw new AuthenticationError('Please login to continue');
        }
        if (error.response?.status === 429) {
          throw new RateLimitError('Too many requests. Please slow down.');
        }
      }
      throw error;
    }
  }
}
```

**React Hook Example (with React Query):**

```typescript
// hooks/use-[entity].ts
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { [Entity]Service } from '@/services/[entity].service';
import type { [Entity]CreateRequest, [Entity]Response } from '@/types';

export function useCreate[Entity]() {
  const queryClient = useQueryClient();

  return useMutation<[Entity]Response, Error, [Entity]CreateRequest>({
    mutationFn: (data) => [Entity]Service.create(data),
    onSuccess: (data) => {
      // Invalidate queries to refetch data
      queryClient.invalidateQueries({ queryKey: ['[entities]'] });
      
      // Show success message
      toast.success('Created successfully!');
    },
    onError: (error) => {
      // Show error message
      toast.error(error.message);
    },
  });
}

// Usage in component
function CreateForm() {
  const create = useCreate[Entity]();

  const handleSubmit = (data: [Entity]CreateRequest) => {
    create.mutate(data);
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Form fields */}
      <button type="submit" disabled={create.isPending}>
        {create.isPending ? 'Creating...' : 'Create'}
      </button>
    </form>
  );
}
```

---

### 4.2 [Endpoint 2 Name]

[Repeat the same format for each endpoint from spec.md Section 4]

---

## 5. TypeScript Interfaces

[Generate from plan.md Section 8 - Pydantic Schemas]

### Complete Type Definitions

```typescript
// types/[module].types.ts

/**
 * [Entity] entity representation
 * Maps to backend Pydantic schema: [Entity]Response
 */
export interface [Entity] {
  id: string;
  field1: string;
  field2: number;
  field3?: string;              // Optional field
  created_at: string;           // ISO 8601 datetime
  updated_at: string;           // ISO 8601 datetime
}

/**
 * Create [Entity] request
 * Maps to backend Pydantic schema: [Entity]CreateRequest
 */
export interface [Entity]CreateRequest {
  field1: string;               // Required
  field2: number;                // Required
  field3?: string;               // Optional
}

/**
 * Update [Entity] request
 * Maps to backend Pydantic schema: [Entity]UpdateRequest
 */
export interface [Entity]UpdateRequest {
  field1?: string;              // All fields optional for partial update
  field2?: number;
  field3?: string;
}

/**
 * Pagination metadata
 */
export interface PaginationMeta {
  page: number;
  page_size: number;
  total: number;
  total_pages: number;
  has_next: boolean;
  has_prev: boolean;
}

/**
 * Paginated list response
 */
export interface [Entity]ListResponse {
  data: [Entity][];
  pagination: PaginationMeta;
}

/**
 * API Error response
 */
export interface ApiError {
  detail: string | ValidationError[];
}

export interface ValidationError {
  type: string;
  loc: (string | number)[];
  msg: string;
  input: any;
}
```

### Zod Schemas (Runtime Validation)

```typescript
// schemas/[module].schema.ts
import { z } from 'zod';

/**
 * Zod schemas for runtime validation
 * Mirrors backend Pydantic validation
 */

export const [Entity]CreateSchema = z.object({
  field1: z.string().email('Invalid email format'),
  field2: z.number().min(1, 'Must be at least 1'),
  field3: z.string().optional(),
});

export const [Entity]UpdateSchema = z.object({
  field1: z.string().email('Invalid email format').optional(),
  field2: z.number().min(1, 'Must be at least 1').optional(),
  field3: z.string().optional(),
});

// Usage in forms
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

function CreateForm() {
  const form = useForm<[Entity]CreateRequest>({
    resolver: zodResolver([Entity]CreateSchema),
  });

  // Form will validate according to Zod schema (matches backend Pydantic)
}
```

---

## 6. Request/Response Examples

### Full CRUD Operations

```typescript
// services/[entity].service.ts
import { apiClient } from '@/lib/api-client';
import type { 
  [Entity], 
  [Entity]CreateRequest, 
  [Entity]UpdateRequest,
  [Entity]ListResponse 
} from '@/types';

export class [Entity]Service {
  // CREATE
  static async create(data: [Entity]CreateRequest): Promise<[Entity]> {
    const response = await apiClient.post<[Entity]>(
      '/[module]/[entities]',
      data
    );
    return response.data;
  }

  // READ (by ID)
  static async getById(id: string): Promise<[Entity]> {
    const response = await apiClient.get<[Entity]>(
      `/[module]/[entities]/${id}`
    );
    return response.data;
  }

  // READ (list with pagination)
  static async list(params?: {
    page?: number;
    page_size?: number;
    search?: string;
  }): Promise<[Entity]ListResponse> {
    const response = await apiClient.get<[Entity]ListResponse>(
      '/[module]/[entities]',
      { params }
    );
    return response.data;
  }

  // UPDATE
  static async update(
    id: string,
    data: [Entity]UpdateRequest
  ): Promise<[Entity]> {
    const response = await apiClient.put<[Entity]>(
      `/[module]/[entities]/${id}`,
      data
    );
    return response.data;
  }

  // DELETE
  static async delete(id: string): Promise<void> {
    await apiClient.delete(`/[module]/[entities]/${id}`);
  }
}
```

### React Query Hooks (Complete Set)

```typescript
// hooks/use-[entities].ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { [Entity]Service } from '@/services/[entity].service';

// List [entities]
export function use[Entities]List(params?: { page?: number; page_size?: number }) {
  return useQuery({
    queryKey: ['[entities]', params],
    queryFn: () => [Entity]Service.list(params),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

// Get single [entity]
export function use[Entity](id: string) {
  return useQuery({
    queryKey: ['[entity]', id],
    queryFn: () => [Entity]Service.getById(id),
    enabled: !!id, // Only run if ID exists
  });
}

// Create [entity]
export function useCreate[Entity]() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: [Entity]Service.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['[entities]'] });
    },
  });
}

// Update [entity]
export function useUpdate[Entity]() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: [Entity]UpdateRequest }) =>
      [Entity]Service.update(id, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['[entities]'] });
      queryClient.invalidateQueries({ queryKey: ['[entity]', variables.id] });
    },
  });
}

// Delete [entity]
export function useDelete[Entity]() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: [Entity]Service.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['[entities]'] });
    },
  });
}
```

---

## 7. Error Handling

[Map from spec.md Section 8 - Edge Cases & Failure Scenarios]

### Error Types

```typescript
// types/errors.ts

export class ApiError extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public details?: any
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

export class ValidationError extends ApiError {
  constructor(details: any) {
    super('Validation failed', 400, details);
    this.name = 'ValidationError';
  }
}

export class AuthenticationError extends ApiError {
  constructor(message: string = 'Authentication required') {
    super(message, 401);
    this.name = 'AuthenticationError';
  }
}

export class AuthorizationError extends ApiError {
  constructor(message: string = 'Permission denied') {
    super(message, 403);
    this.name = 'AuthorizationError';
  }
}

export class NotFoundError extends ApiError {
  constructor(resource: string) {
    super(`${resource} not found`, 404);
    this.name = 'NotFoundError';
  }
}

export class RateLimitError extends ApiError {
  constructor(
    message: string = 'Too many requests',
    public retryAfter?: number
  ) {
    super(message, 429);
    this.name = 'RateLimitError';
  }
}

export class ServerError extends ApiError {
  constructor(message: string = 'Internal server error') {
    super(message, 500);
    this.name = 'ServerError';
  }
}
```

### Global Error Handler

```typescript
// lib/error-handler.ts
import axios from 'axios';
import {
  ApiError,
  ValidationError,
  AuthenticationError,
  AuthorizationError,
  NotFoundError,
  RateLimitError,
  ServerError,
} from '@/types/errors';

export function handleApiError(error: unknown): ApiError {
  if (axios.isAxiosError(error)) {
    const status = error.response?.status;
    const data = error.response?.data;

    switch (status) {
      case 400:
        return new ValidationError(data.detail);
      
      case 401:
        return new AuthenticationError(data.detail);
      
      case 403:
        return new AuthorizationError(data.detail);
      
      case 404:
        return new NotFoundError(data.detail || 'Resource');
      
      case 429:
        const retryAfter = error.response?.headers['retry-after'];
        return new RateLimitError(data.detail, retryAfter);
      
      case 500:
      case 502:
      case 503:
        return new ServerError(data.detail || 'Server error');
      
      default:
        return new ApiError(
          data.detail || 'An error occurred',
          status || 500,
          data
        );
    }
  }

  if (error instanceof Error) {
    return new ApiError(error.message, 500);
  }

  return new ApiError('Unknown error occurred', 500);
}
```

### Error Handling in Components

```typescript
// Example: Handling errors in a form component
import { handleApiError } from '@/lib/error-handler';
import { ValidationError, RateLimitError } from '@/types/errors';

function CreateForm() {
  const [errors, setErrors] = useState<Record<string, string>>({});
  const create = useCreate[Entity]();

  const handleSubmit = async (data: [Entity]CreateRequest) => {
    try {
      setErrors({});
      await create.mutateAsync(data);
      toast.success('Created successfully!');
    } catch (error) {
      const apiError = handleApiError(error);

      if (apiError instanceof ValidationError) {
        // Display field-specific errors
        const fieldErrors: Record<string, string> = {};
        apiError.details.forEach((err: any) => {
          const field = err.loc[err.loc.length - 1];
          fieldErrors[field] = err.msg;
        });
        setErrors(fieldErrors);
      } else if (apiError instanceof RateLimitError) {
        toast.error(`Too many requests. Retry in ${apiError.retryAfter}s`);
      } else {
        toast.error(apiError.message);
      }
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input name="field1" />
      {errors.field1 && <span className="error">{errors.field1}</span>}
      {/* More fields */}
    </form>
  );
}
```

### Edge Case Handling

[Map from spec.md Section 8 - Edge Cases]

**Scenario: Database Unavailable (503)**

```typescript
if (apiError.statusCode === 503) {
  // Show user-friendly message
  toast.error('Service temporarily unavailable. Please try again later.');
  
  // Optionally: Implement retry logic
  setTimeout(() => {
    queryClient.refetchQueries({ queryKey: ['[entities]'] });
  }, 5000);
}
```

**Scenario: Network Timeout**

```typescript
// Configure axios timeout
const apiClient = axios.create({
  timeout: 10000, // 10 seconds
});

// Handle timeout error
if (error.code === 'ECONNABORTED') {
  toast.error('Request timed out. Please check your connection.');
}
```

---

## 8. State Management Guide

### Recommended Approach: React Query

React Query handles:
- Caching
- Background refetching
- Optimistic updates
- Request deduplication
- Error retry logic

```typescript
// app/providers.tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 3,
      retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
      staleTime: 5 * 60 * 1000, // 5 minutes
      refetchOnWindowFocus: false,
    },
  },
});

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
}
```

### Optimistic Updates

```typescript
export function useUpdate[Entity]() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: [Entity]UpdateRequest }) =>
      [Entity]Service.update(id, data),
    
    // Optimistic update
    onMutate: async ({ id, data }) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: ['[entity]', id] });

      // Snapshot previous value
      const previous = queryClient.getQueryData(['[entity]', id]);

      // Optimistically update
      queryClient.setQueryData(['[entity]', id], (old: any) => ({
        ...old,
        ...data,
      }));

      return { previous };
    },
    
    // Rollback on error
    onError: (err, variables, context) => {
      if (context?.previous) {
        queryClient.setQueryData(
          ['[entity]', variables.id],
          context.previous
        );
      }
    },
    
    // Refetch on success or error
    onSettled: (_, __, variables) => {
      queryClient.invalidateQueries({ queryKey: ['[entity]', variables.id] });
    },
  });
}
```

---

## 9. Best Practices

### 1. Always Use TypeScript

```typescript
// ✅ Good: Type-safe
const create = useCreate[Entity]();
create.mutate(data); // TypeScript validates data

// ❌ Bad: No type safety
const create = useCreate[Entity]();
create.mutate({ invalid: 'data' }); // No compile-time error
```

### 2. Handle Loading States

```typescript
function [Entity]List() {
  const { data, isLoading, isError, error } = use[Entities]List();

  if (isLoading) return <Spinner />;
  if (isError) return <ErrorMessage error={error} />;
  if (!data) return null;

  return <List items={data.data} />;
}
```

### 3. Implement Proper Error Boundaries

```typescript
// components/error-boundary.tsx
import { Component, ReactNode } from 'react';

export class ErrorBoundary extends Component<
  { children: ReactNode },
  { hasError: boolean }
> {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error: Error) {
    console.error('Error caught:', error);
  }

  render() {
    if (this.state.hasError) {
      return <ErrorFallback />;
    }

    return this.props.children;
  }
}
```

### 4. Use Environment Variables

```typescript
// .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_API_VERSION=v1

// lib/config.ts
export const config = {
  apiUrl: process.env.NEXT_PUBLIC_API_URL!,
  apiVersion: process.env.NEXT_PUBLIC_API_VERSION!,
} as const;
```

### 5. Implement Request Cancellation

```typescript
// Cancel requests when component unmounts
export function use[Entity](id: string) {
  return useQuery({
    queryKey: ['[entity]', id],
    queryFn: async ({ signal }) => {
      const response = await apiClient.get(`/[entities]/${id}`, { signal });
      return response.data;
    },
  });
}
```

### 6. Add Request/Response Logging (Development Only)

```typescript
if (process.env.NODE_ENV === 'development') {
  apiClient.interceptors.request.use((config) => {
    console.log('→ Request:', config.method?.toUpperCase(), config.url);
    return config;
  });

  apiClient.interceptors.response.use((response) => {
    console.log('← Response:', response.status, response.config.url);
    return response;
  });
}
```

---

## 10. Testing Guidelines

### Unit Testing API Services

```typescript
// __tests__/services/[entity].service.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { [Entity]Service } from '@/services/[entity].service';
import { apiClient } from '@/lib/api-client';

vi.mock('@/lib/api-client');

describe('[Entity]Service', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should create [entity] successfully', async () => {
    const mockData = { field1: 'test', field2: 42 };
    const mockResponse = { id: '123', ...mockData };

    vi.mocked(apiClient.post).mockResolvedValue({ data: mockResponse });

    const result = await [Entity]Service.create(mockData);

    expect(apiClient.post).toHaveBeenCalledWith('/[entities]', mockData);
    expect(result).toEqual(mockResponse);
  });

  it('should handle validation error', async () => {
    const mockError = {
      response: {
        status: 400,
        data: { detail: [{ msg: 'Invalid field' }] },
      },
    };

    vi.mocked(apiClient.post).mockRejectedValue(mockError);

    await expect([Entity]Service.create({} as any)).rejects.toThrow();
  });
});
```

### Testing React Hooks

```typescript
// __tests__/hooks/use-[entity].test.tsx
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClientProvider, QueryClient } from '@tanstack/react-query';
import { useCreate[Entity] } from '@/hooks/use-[entity]';

const queryClient = new QueryClient({
  defaultOptions: { queries: { retry: false } },
});

const wrapper = ({ children }: { children: React.ReactNode }) => (
  <QueryClientProvider client={queryClient}>
    {children}
  </QueryClientProvider>
);

describe('useCreate[Entity]', () => {
  it('should create [entity] and invalidate queries', async () => {
    const { result } = renderHook(() => useCreate[Entity](), { wrapper });

    await result.current.mutateAsync({ field1: 'test', field2: 42 });

    await waitFor(() => {
      expect(result.current.isSuccess).toBe(true);
    });
  });
});
```

---

## 11. Troubleshooting

### Common Issues

**Issue: CORS Errors**

```typescript
// Backend must allow frontend origin
// Check FastAPI CORS configuration
// Frontend: Ensure API_BASE_URL is correct
```

**Issue: Token Expired (401)**

```typescript
// Implement automatic token refresh
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      try {
        const newToken = await AuthService.refreshToken();
        // Retry original request with new token
        error.config.headers.Authorization = `Bearer ${newToken}`;
        return apiClient.request(error.config);
      } catch {
        // Refresh failed, redirect to login
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);
```

**Issue: Network Errors**

```typescript
// Check network connectivity
// Verify API_BASE_URL is correct
// Check if backend server is running
// Verify CORS configuration
```

**Issue: Validation Errors**

```typescript
// Ensure request data matches TypeScript interface
// Use Zod schemas for runtime validation
// Check backend Pydantic validation rules match frontend
```

---

## Output File Location

**Save as:** `specs/<feature_name>/frontend-api-guide.md`

---

## Quality Checklist

- [ ] All endpoints from spec.md Section 4 documented
- [ ] TypeScript interfaces match backend Pydantic schemas
- [ ] Request/response examples provided for each endpoint
- [ ] Error handling covers all scenarios from spec.md Section 8
- [ ] Authentication flow documented (if applicable)
- [ ] Rate limiting handling documented (if applicable)
- [ ] React Query hooks provided for all operations
- [ ] Code examples are complete and runnable
- [ ] Testing guidelines included
- [ ] Troubleshooting section covers common issues

---

**Save all frontend guide files to:** `specs/<feature_name>/frontend-api-guide.md`
