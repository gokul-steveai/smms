# SMMS™ (Service Model Management System™)
## Project Development Plan & Technical Blueprint

This document outlines the detailed development plan for the SMMS™ platform based on the Product Requirements Document (PRD) and Technical Proposal.

---

## 1. Project Overview & Objectives

**Vision:** Transition organizations from job/headcount-based operations to a service-centric model where work is delivered by **Talent+AI™** units and managed via the SMMS™ platform.
**Primary Business Goal:** Achieve margin acceleration within 18-24 months by reallocating freed capacity to higher-value services.
**Key Deliverables:**
1. A Jobs-to-Services pipeline that decomposes HRIS roles into normalized Service Profiles.
2. An application to manage Service Profiles (Current, 1-Month, 3-Month) enforcing a 100% FTE rule.
3. An Agent Network to manage supplier-customer "Value Exchange" (VE) agreements.
4. ROTA™ (Return on Talent+AI) analytics and dashboarding.

---

## 2. Technical Architecture & Tech Stack

**Language/Framework:** Python 3.13+
**Architecture Style:** Event-driven microservices / Multi-Agent System
**Core Layers:**
- **Data Layer:** Pydantic models for strict schema validation.
- **Service Engine:** LLM-powered decomposition pipeline.
- **Agent Network Layer:** 3-Tier topology (Individual, Organizational, Ecosystem) connected via **App Connectors** to enterprise systems (CRM, HRIS, Finance).
  - Starts with Option A (Embedded lightweight LLM) to minimize cost.
  - Designed with an SMMS protocol to support Option B (Federated multi-LLMs) later.
- **Value Exchange Engine:** Event-driven multi-agent system managing service agreements (Option 2 production architecture), starting with a simple sequential state machine for MVP testing (Option 1).

---

## 3. Phased Development Roadmap

The software engineering lifecycle is structured into five core phases to build the platform progressively before it is deployed for the client's operational rollout.

### Phase 1: Core Domain Models & Data Foundation
**Goal:** Establish the strict data schemas and constraints defined in the PRD.

* **Tasks:**
  * Define `Talent` (User/Team profiles).
  * Define `Service` and `Customer` schemas (Internal/External).
  * Implement `ServiceAllocation` with the critical validation logic: **FTE% for any given version (Current, 1M, 3M) must sum to exactly 100%**.
  * Define `Project` (Individual & Team improvement initiatives).
  * Create mock data generation for POC testing.
* **Deliverables:** Validated Pydantic models in `smms.models`.

### Phase 2: Jobs-to-Services AI Pipeline & Workforce Agent
**Goal:** Build the engine that converts legacy HRIS job data and existing catalogs into normalized SMMS services.

* **Tasks:**
  * Build Data Ingestion: Import role data from HRIS and any existing service catalogs.
  * Integrate LLM client (model-agnostic, starting with lightweight/embedded API).
  * Create the **Workforce Agent**: Analyzes job descriptions, manages service decomposition, and monitors resource supply and demand.
  * Implement the Normalizer to standardize LLM outputs against the `Service` schema (Name, Target Customer, %FTE, Attributes like Quality & SVM).
  * Build the Human-in-the-Loop review mechanism (approval/edit gates).
* **Deliverables:** Working pipeline script where the Workforce Agent takes a job description and outputs a validated `ServiceProfile`.

### Phase 3: The Value Exchange (VE) Engine & Agent Network
**Goal:** Develop the agentic system that manages live service agreements between Talent and Customers.

* **Tasks:**
  * Implement the VE architecture: Option 1 (Sequential State Machine) for testing MVP, scaling to Option 2 (Event-Driven Multi-Agent with message bus) for production.
  * Build the **Management Agent** (Organizational Tier Supervisory Engine):
    * Define thresholds for automated agent negotiation.
    * Implement escalation logic (when to involve human Talent).
  * Develop the **Talent+AI Login Agent**: A conversational interface for users to check VE status, draft communications, and view their portfolio.
* **Deliverables:** Agent interaction tests simulating a successful and an escalated Value Exchange negotiation.

### Phase 4: Analytics, ROTA™, and Continuous Loop
**Goal:** Implement the metrics that prove the margin acceleration and drive continuous improvement.

* **Tasks:**
  * Build the **Self-Assessment Module**: Questionnaire that feeds individual and team improvement opportunities.
  * Implement the `Project` tracking module: Draft, approve, and track improvement projects (1-4 weeks individual, 1-3 months team).
  * Build the ROTA™ calculation engine (Net Value Created / Total Investment).
  * Implement the `Human Equivalence™` conversion logic.
  * Create aggregation views for Team Leads and Executive Sponsors.
  * Implement triggers for Monthly and Quarterly review cycles to foster a Highly Adaptable Organization (HAO).
* **Deliverables:** Analytics module outputting enterprise ROTA scores, capacity reallocation metrics, and active project tracking.

### Phase 5: Security, Governance & Compliance (Ongoing)
**Goal:** Ensure the system meets enterprise IT and Responsible AI standards.

* **Tasks:**
  * **Human-in-the-Loop (HITL) Enforcement:** Ensure no AI agent can alter service agreements or publish service profiles without human approval.
  * **Role-Based Access Control (RBAC):** Ensure Talent only sees their own and team data, while executives see aggregated ROTA metrics.
  * **Change Management Integration:** Design user onboarding to alleviate job loss fears by emphasizing Human Equivalence™ and the Talent+AI augmentation philosophy.
  * **Audit Logging:** Maintain a strict ledger of all Value Exchange negotiations and FTE shifts for accountability.
  * **Model Evaluation:** Establish evaluation sets for LLM service decomposition accuracy to prevent hallucinated services.
* **Deliverables:** A hardened, secure platform ready for enterprise deployment.

---

## 4. Key Milestones & Testing Gates

| Milestone | Description | Success Criteria |
| :--- | :--- | :--- |
| **M1: Schema Validation** | Core data models are locked. | Creating a ServiceProfile with 95% FTE throws an error. |
| **M2: Pipeline Demo** | Jobs-to-Services pipeline works. | LLM successfully outputs valid JSON matching the Service schema from raw text. |
| **M3: VE Simulation** | Agents can negotiate an agreement. | Two agents successfully transition a VE from `Change Request` to `Acceptance` using the event bus. |
| **M4: MVP Ready** | End-to-end system works for the POC. | Full flow: Ingest Job -> Create Profile -> Modify VE -> Calculate ROTA. |

---

## 5. Outstanding Decisions / Risk Mitigation

* **Agent Autonomy Thresholds:** We need to define the exact percentage/scope an agent can negotiate without human approval. *Mitigation: Start with zero autonomy (all changes require human click) and loosen via config.*
* **LLM Vendor Lock-in:** The PRD specifies model-agnosticism. *Mitigation: Abstract all LLM calls behind a generic Provider interface (starting with a lightweight local model or standard API).*
* **FTE Calculation Accuracy:** Employees might struggle to estimate exact %. *Mitigation: The Human-in-the-Loop interface must visually guide the balancing of percentages.*
