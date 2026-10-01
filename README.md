# HARVESTSAARTHI AI

> **"From Harvest Uncertainty to the Right Next Move."**

![Domain](https://img.shields.io/badge/Domain-AgriTech_%26_Rural_Bharat-emerald?style=for-the-badge)
![Submission](https://img.shields.io/badge/Hackathon-BHARAT_AGENTIC_2026-teal?style=for-the-badge)
![Powered By](https://img.shields.io/badge/Powered_By-aiKart-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Submission_Ready_Prototype-brightgreen?style=for-the-badge)

HarvestSaarthi AI is an evidence-driven AI decision agent built for BHARAT AGENTIC 2026. It turns a small farmer's post-harvest uncertainty into an optimal, data-backed, explainable, and executable **sell, store, transport, and timing plan**.

---

## 1. Problem Statement & Why It Matters

Smallholder farmers in Bharat face complex post-harvest trade-offs:
- *Should I sell at my local mandi today or transport to a distant market offering higher nominal prices?*
- *Is temporary cold storage worth the cost, or will perishability spoilage wipe out my margins?*
- *How much will transport logistics cost, and does weather delay risk threaten my crop?*
- *Which action should I take first, and what information is missing?*

Without a unified decision system, farmers often fall back on guesswork, leading to distress sales or high spoilage losses.

> **Disclaimer & Responsible AI:** HarvestSaarthi AI provides decision-support estimates (projected net realization based on available prototype/live data) and never claims financial guarantees.

---

## 2. Core Agentic Workflow

Unlike generic chatbots or LLM wrappers, HarvestSaarthi AI implements a genuine 12-stage **Decision-and-Action Agent Workflow**:

```
USER INPUT
   │
   ▼
SITUATION UNDERSTANDING (Entity Normalization & Gap Analysis)
   │
   ▼
REQUIREMENT PLANNING ──► TOOL SELECTION ──► DATA COLLECTION
                                                  │
   ┌──────────────────────────────────────────────┘
   ▼
NORMALIZATION (INR Currency, kg, km)
   │
   ▼
OPTION GENERATION (Sell Today, Transport Distant, Store & Sell Later, Split Market)
   │
   ▼
COST / RISK CALCULATION (Gross Rev, Transport, Storage, Spoilage Loss)
   │
   ▼
OPTION COMPARISON & FEASIBILITY FILTERING
   │
   ▼
DETERMINISTIC DECISION RANKING ──► ACTION PLAN ──► EXPLANATION + EVIDENCE
```

---

## 3. System Architecture

```
                    FARMER (Voice / Web UI)
                               │
                               ▼
                    ORCHESTRATOR AGENT
                               │
       ┌───────────────────────┼───────────────────────┐
       ▼                       ▼                       ▼
Situation Understanding    Logistics Tool       Perishability & Decay
     Agent (NLU)          & Transport Tool           Engine
       │                       │                       │
       └───────────────────────┼───────────────────────┘
                               │
                               ▼
                   DETERMINISTIC DECISION ENGINE
             (Revenue - Transport - Storage - Spoilage)
                               │
       ┌───────────────────────┴───────────────────────┐
       ▼                                               ▼
 Action Planner Agent                         Report Generator
(Steps & Negotiation Templates)           (HarvestSaarthi_Decision_Report.pdf)
```

---

## 4. Tool Architecture & Data Strategy

The system features six actual tool interfaces that operate against a deterministic benchmark dataset (`backend/data/dataset.json`) covering South Indian / Karnataka mandis (Hassan, Bangalore APMC, Kolar, Mysuru, Hubballi, Chintamani):

1. `market_price_tool`: Queries current mandi purchase prices and price trends.
2. `route_distance_tool`: Calculates transit distance and truck logistics rates.
3. `weather_risk_tool`: Assesses rainfall and temperature transit delay risks.
4. `perishability_tool`: Models crop-specific decay rates (Ambient vs Cold Storage).
5. `storage_tool`: Checks warehouse availability, daily rates, and capacity.
6. `transport_tool`: Assesses truck availability and logistics capacity.

**Data Provenance:** Every response explicitly displays `DATA MODE: DEMO` and `SOURCE: HarvestSaarthi Prototype Dataset`.

---

## 5. Pure Python Deterministic Decision Math

Critical arithmetic is handled by pure Python code to guarantee 100% accuracy:

$$ \text{Gross Revenue} = \text{Quantity (kg)} \times \text{Price per kg} $$

$$ \text{Spoilage Loss} = \text{Quantity (kg)} \times \left(\frac{\text{Spoilage \%}}{100}\right) \times \text{Price per kg} $$

$$ \text{Expected Net Realization} = \text{Gross Revenue} - \text{Transport Cost} - \text{Storage Cost} - \text{Spoilage Loss} $$

The LLM is strictly reserved for natural language understanding, input normalization, multilingual translation, action plan wording, and synthesis explanations.

---

## 6. Zero-Crash Fallback Architecture

If an external LLM API key is unconfigured or fails:
- The system automatically executes in **`FALLBACK_MODE`**.
- It runs the complete 12-stage deterministic decision workflow without crashing.
- It displays an honest badge: `MODE: FALLBACK_MODE`.

---

## 7. Key Features

- **Hero Recommendation Dashboard:** Highlights recommended action, Expected Net Realization (₹), Confidence Score (%), and Risk Level (LOW/MEDIUM/HIGH).
- **Interactive "What-If?" Simulator:** Dynamic parameter sliders (Quantity, Price %, Cold Storage toggle) that recalculate recommendations in real time.
- **Auditable Agent Execution Trace:** Visual 12-stage progress cards showing tool calls and reasoning metrics.
- **Multilingual Negotiation Assistant:** One-click copyable WhatsApp/SMS message templates in **English**, **Kannada (ಕನ್ನಡ)**, and **Hindi (हिंदी)**.
- **Voice Input Support:** Integrated Web Speech API for voice recognition in rural languages.
- **Downloadable PDF Report:** Generates `HarvestSaarthi_Decision_Report.pdf` via ReportLab.

---

## 8. API Documentation

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Health check and system mode status |
| `GET` | `/api/crops` | Returns list of supported crops |
| `GET` | `/api/markets` | Returns available APMC mandis |
| `POST` | `/api/analyze` | Input normalization and missing field detection |
| `POST` | `/api/decision` | Main decision endpoint executing 12-stage workflow |
| `POST` | `/api/what-if` | Dynamic parameter re-evaluation |
| `GET` | `/api/demo/{demo_id}` | One-click judge demo scenarios (`tomato`, `onion`, `banana`) |
| `POST` | `/api/action-plan` | Priority steps and WhatsApp/SMS templates |
| `GET` | `/api/report/{run_id}` | Downloads PDF decision report |

---

## 9. Local Setup & Demo Instructions

### Backend Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Run FastAPI backend
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000` in your browser.

---

## 10. Automated Test Suite

Run the Pytest suite covering math, tools, API endpoints, and security checks:

```bash
python -m pytest tests/test_decision_engine.py tests/test_tools.py tests/test_api.py tests/test_security.py
```

---

## 11. Docker Build & Execution

### Build Docker Image
```bash
docker build -t harvestsaarthi-ai .
```

### Run Docker Container
```bash
docker run -d -p 8000:8000 --name harvestsaarthi_app harvestsaarthi-ai
```

Verify health: `curl http://localhost:8000/api/health`

---

## 12. aiKart Manifest Status

- **Status:** Manifest configuration isolated in [`aikart-manifest.yaml`](file:///C:/Users/heman/OneDrive/Desktop/HarvestSaarthi_AI/aikart-manifest.yaml).
- **Note:** The manifest configuration is isolated cleanly and ready for official schema validation once published by BHARAT AGENTIC 2026 organizers.
