---
name: "API Review"
description: "Review API endpoints for REST conventions, validation, error handling, security, documentation, and testability"
argument-hint: "Endpoint file (e.g. #file:app/routers/products.py) or router name"
agent: "ask"
---

Perform a structured code review of the API endpoint(s) provided in $ARGUMENTS (or the currently selected code / active file).

Reference the project guidelines in [.github/copilot-instructions.md](.github/copilot-instructions.md) where applicable (docstrings with runnable doctest examples, Python 3.13 typing, FastAPI conventions, and pytest testing).

Evaluate against the following criteria:

### 1. REST Conventions
- **HTTP Verbs & Semantics**: Are `GET`, `POST`, `PUT`, `PATCH`, `DELETE` used according to HTTP/1.1 specifications?
- **Resource Naming**: Are URL paths resource-oriented, pluralized, and consistent (e.g., `/products/{product_id}`)?
- **Status Codes**: Are status codes semantically accurate (e.g., 200 OK, 201 Created, 204 No Content, 400 Bad Request, 404 Not Found, 409 Conflict, 422 Unprocessable Entity)?

### 2. Input/Output Validation
- **Pydantic Schemas**: Are request bodies, path parameters, and query parameters strictly typed and validated?
- **Response Models**: Is `response_model` defined on endpoint decorators to prevent data leakage and enforce API contracts?
- **Type Annotations**: Are all parameters and return types explicitly annotated?

### 3. Error Handling & Edge Cases
- **Structured Exceptions**: Are errors raised using explicit `HTTPException` with appropriate status codes and detail messages, rather than unhandled exceptions (500s)?
- **Boundary & Missing Values**: Are not-found scenarios, empty bodies, duplicate identifiers, and type mismatches handled gracefully?

### 4. Security & Data Protection
- **Data Exposure**: Are internal fields (passwords, tokens, internal primary keys, system error traces) excluded from schemas and responses?
- **Input Sanitization & Injection**: Are inputs bounded (lengths, min/max values) to mitigate DoS or injection risks?
- **Authentication/Authorization**: Are necessary security dependencies or scopes checked?

### 5. Documentation
- **OpenAPI Metadata**: Are `summary`, `description`, `tags`, and specific status `responses` specified on route decorators?
- **Docstrings**: Does every function include a docstring with at least one runnable example (doctest `>>>` format or `Example:` block)?

### 6. Test Coverage Needs
- Identify uncovered paths: happy paths, error paths (404/422), and boundary/edge conditions.
- Specify tests that should be implemented with `pytest` and `fastapi.testclient.TestClient`.

---

### Output Format

Organize your review using this layout:

1. **Overview**: Brief summary (1-2 sentences) of the reviewed endpoint.
2. **Critical Issues**: 🔴 Bugs, security flaws, improper status codes, or unhandled 500 runtime exceptions.
3. **Improvements & Code Quality**: 🟡 Schema refinements, OpenAPI documentation gaps, missing docstring examples, or style improvements.
4. **Recommended Code Adjustments**: Concrete code blocks showing the refactored endpoint with fixes applied.
5. **Suggested Test Cases**: Specific unit test scenarios to add in `tests/test_*.py`.
