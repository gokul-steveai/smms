# SMMS™ (Service Model Management System™)

![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.142+-green.svg)
![LangGraph](https://img.shields.io/badge/LangGraph-Agentic_AI-orange.svg)
![License](https://img.shields.io/badge/License-Proprietary-red.svg)

**SMMS™** is an Enterprise Agentic AI Platform designed by HumanCentric Labs. It facilitates the transition of enterprise organizations from legacy job-based structures to highly adaptable, service-oriented architectures utilizing **Talent+AI™** hybrid work units.

## 🚀 Core Features

- **Jobs-to-Services AI Pipeline:** LLM-powered engine that decomposes raw HRIS job descriptions into normalized, measurable Service Profiles.
- **100% FTE Validation:** Strict business rule enforcement ensuring that individual and team capacities are perfectly allocated across current and future services.
- **Value Exchange (VE) Engine:** An event-driven, multi-agent system where `Talent+AI` supplier and customer agents negotiate service agreements across a 6-state lifecycle.
- **Management Agent Supervision:** Automated escalation and boundary enforcement for AI-driven service negotiations.
- **ROTA™ Analytics:** Real-time calculation of Return on Talent+AI Investment, proving margin acceleration.

## 🏗️ Architecture

The application is built using **Domain-Driven Design (DDD)** and **Clean Architecture**:
- **Presentation:** `FastAPI` exposing async, high-performance REST APIs.
- **Infrastructure:** `SQLAlchemy` (Async) with `asyncpg` (PostgreSQL) and `aiosqlite` (SQLite fallback).
- **Agent Orchestration:** `LangChain` and `LangGraph` managing the Value Exchange state machines, heavily utilizing `Groq` LLMs.
- **Validation:** Strict, high-speed typing via `Pydantic v2`.

## 🛠️ Local Development Setup

This project uses [`uv`](https://docs.astral.sh/uv/) for ultra-fast Python package and environment management.

### 1. Prerequisites
- Python >= 3.13
- `uv` installed on your system

### 2. Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/gokul-steveai/smms.git
cd smms
uv sync
```

### 3. Environment Configuration
Create a `.env` file in the root directory:
```env
# Server Configuration
PROJECT_NAME="SMMS™ - Service Model Management System"

# Database (Omit POSTGRES_URL to automatically fallback to local SQLite)
# POSTGRES_URL="postgresql://user:pass@localhost:5432/smms"

# LLM Provider Configuration
LLM_PROVIDER="groq"
GROQ_API_KEY="your-groq-api-key-here"
```

### 4. Database Migrations
Initialize the local SQLite database schema using Alembic:
```bash
uv run alembic upgrade head
```

### 5. Running the Application
Start the local FastAPI development server:
```bash
uv run uvicorn src.main:app --reload
```
The API documentation will be available at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## 🧪 Testing & Linting
Run the type-checker and linters:
```bash
uv run ruff check src/
uv run mypy src/
```

## © Authors
- **Gokul Panwar** (gokul.stevesai@gmail.com)
