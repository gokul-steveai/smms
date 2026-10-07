# SMMS™ Implementation & Architecture Guidelines

This document outlines the technical architecture, design patterns, and coding standards required to build SMMS™ as an industry-grade, highly scalable, and loosely coupled enterprise application.

---

## 1. Architectural Philosophy: Domain-Driven Design (DDD) & Clean Architecture

To ensure the SMMS™ platform remains scalable and maintainable, we will adopt a **Clean / Hexagonal Architecture** combined with **Domain-Driven Design (DDD)** principles. 

This ensures that the core business logic (e.g., the 100% FTE invariant, Value Exchange rules) is entirely decoupled from external frameworks, databases, or LLM providers.

### The Four Layers
1. **Domain Layer (`src/domain/`):** Contains enterprise business rules, Pydantic models (Entities like `ServiceProfile`, `ValueExchange`), and Domain Exceptions. Has **zero dependencies** on other layers.
2. **Application Layer (`src/application/`):** Contains Use Cases (e.g., `DecomposeJobToServices`, `NegotiateValueExchange`). Orchestrates the domain models and defines interfaces (Ports) for repositories and external services.
3. **Infrastructure Layer (`src/infrastructure/`):** Implements the interfaces defined in the Application layer. Contains the Database ORM (SQLAlchemy/SQLModel), Event Bus (Redis/Kafka), and External LLM clients (Claude/OpenAI integrations).
4. **Presentation/API Layer (`src/presentation/`):** Exposes the application to the outside world (e.g., FastAPI routers, WebSocket endpoints for real-time agent chats).

---

## 2. Recommended Tech Stack

* **API Framework:** `FastAPI` (Async, high-performance, native OpenAPI support)
* **Data Validation:** `Pydantic` v2 (Native typing, high-speed Rust core)
* **ORM:** `SQLModel` or `SQLAlchemy 2.0` (Async)
* **Database Migration:** `Alembic`
* **Dependency Injection:** Native FastAPI `Depends()` or `dependency-injector` library
* **Event Bus / Message Queue:** `Redis` (for pub/sub routing in the Multi-Agent VE engine)
* **Testing:** `pytest`, `pytest-asyncio`, `testcontainers` (for integration testing)
* **Linting & Formatting:** `Ruff`, `mypy` (Strict mode)

---

## 3. Industry-Grade System Design Patterns

To maintain loose coupling, the following patterns MUST be implemented:

### A. Repository Pattern
Never query the database directly in a Use Case or API route. 
* **Why:** Decouples business logic from data access. Allows swapping Postgres for MongoDB or mocking the DB in tests.
* **Implementation:** Define `abstract base classes (ABCs)` in the Application layer; implement them in the Infrastructure layer.

### B. Unit of Work (UoW) Pattern
Used alongside the Repository pattern to handle atomic transactions.
* **Why:** Ensures that when a `ValueExchange` state changes and a `ServiceAllocation` updates, both commit together or roll back entirely.

### C. Strategy Pattern
Used for swapping implementations dynamically.
* **Why:** The PRD specifies an LLM-agnostic agent interface. We will use a Strategy pattern for the `LLMProvider` interface, allowing hot-swapping between Option A (Embedded/Local) and Option B (Federated/Claude API).

### D. Event-Driven Pub/Sub (Event Bus)
The PRD requires Value Exchanges (Option 2) to be an event-driven multi-agent system.
* **Why:** Hard-coding agent-to-agent communication creates rigid monoliths. 
* **Implementation:** When an agent proposes a VE change, it emits a `ValueExchangeProposedEvent` to an Event Bus. The `ManagementAgent` listens to this bus, processes the rules, and emits a `ValueExchangeApproved` or `ValueExchangeEscalated` event.

---

## 4. Application Flow Example: Job-to-Service Pipeline

How a request flows through the loosely coupled architecture:

1. **Request:** HRIS system sends a POST request with job data to `/api/v1/jobs/decompose`.
2. **Presentation Layer:** FastAPI route validates the incoming JSON against a Pydantic schema and injects the `DecomposeJobUseCase`.
3. **Application Layer:** The Use Case receives the data. It calls the injected `LLMProvider` (Interface) to decompose the job.
4. **Infrastructure Layer:** The concrete `ClaudeLLMProvider` executes the prompt and returns raw JSON.
5. **Application Layer:** The Use Case passes the raw output to a Domain `Normalizer` service.
6. **Domain Layer:** The `Normalizer` validates the output against the `ServiceProfile` entity rules (e.g., ensuring FTE = 100%).
7. **Application Layer:** The Use Case calls the injected `ServiceRepository` to save the data.
8. **Infrastructure Layer:** The SQLAlchemy repository persists it to Postgres.
9. **Response:** FastAPI returns the 201 Created response.

---

## 5. Coding Standards & Best Practices

* **Strict Type Hinting:** All functions must have return types and argument types. Run `mypy --strict` in CI.
* **Error Handling:** Define custom Domain Exceptions (e.g., `InvalidFTEAllocationError`). Catch these in the Presentation layer using FastAPI Exception Handlers to return standardized HTTP 400 responses.
* **Configuration:** Use `pydantic-settings` to manage environment variables (`.env`). Never hardcode secrets.
* **Logging:** Use structured JSON logging (e.g., `structlog`) to ensure logs can be ingested by Datadog or ELK. Include `trace_id` for distributed tracing.
* **Documentation:** All public functions and classes must include Google-style docstrings.

---

## 6. Directory Structure Blueprint

```text
smms/
├── pyproject.toml
├── alembic/                    # DB Migrations
├── src/
│   ├── main.py                 # FastAPI Application Entrypoint
│   ├── core/                   # Config, structured logging, error handlers
│   │   ├── config.py
│   │   └── exceptions.py
│   ├── domain/                 # Layer 1: Entities & Business Rules
│   │   ├── models/             # Pydantic domain entities (Talent, Service)
│   │   └── events/             # Domain events (VEProposedEvent)
│   ├── application/            # Layer 2: Use Cases & Interfaces
│   │   ├── use_cases/          # Job decomposition, ROTA calculation
│   │   └── interfaces/         # Repositories, LLM Providers (ABCs)
│   ├── infrastructure/         # Layer 3: External Implementations
│   │   ├── database/           # SQLAlchemy models & concrete repos
│   │   ├── llm/                # Claude, OpenAI API clients
│   │   └── messaging/          # Redis/RabbitMQ event bus concrete class
│   └── presentation/           # Layer 4: API
│       ├── api/                # FastAPI Routers (v1/services, v1/agents)
│       └── dependencies.py     # FastAPI Depends() injection graph
└── tests/
    ├── unit/                   # Tests isolating domain and application layers
    └── integration/            # Tests with testcontainers for DB/Redis
```

By adhering to this document, the SMMS platform will be robust, highly testable, and prepared for enterprise-scale expansion and advanced agentic orchestration.
