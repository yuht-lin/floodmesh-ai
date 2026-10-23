```markdown
<div align="center">

# 🌊 FloodMesh AI

### Autonomous Multilingual SOS Ingestion & MILP Emergency Resource Allocation Command Center

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React_18-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://react.dev/)
[![Google Gemini](https://img.shields.io/badge/Google_Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)
[![Google OR-Tools](https://img.shields.io/badge/Google_OR--Tools-FF6F00?style=for-the-badge&logo=google&logoColor=white)](https://developers.google.com/optimization)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

**An end-to-end disaster-response intelligence platform that converts unstructured, multilingual citizen SOS signals into structured emergency incidents and optimized rescue-resource assignments.**

</div>

---

## 🚨 Problem

During severe floods and other disasters, emergency response teams can receive thousands of distress messages simultaneously.

These messages may:

- Arrive in different languages or regional dialects
- Contain incomplete or unstructured information
- Describe different levels of urgency
- Include varying numbers of victims
- Require immediate medical or rescue assistance
- Need to be matched against limited rescue resources

Manual triage can introduce delays and inefficient resource allocation.

**FloodMesh AI** addresses this problem by combining:

> **Generative AI + deterministic fallback parsing + mathematical optimization + geospatial visualization**

---

## 💡 What Is FloodMesh AI?

FloodMesh AI is an emergency-response command platform designed to transform citizen SOS messages into actionable dispatch decisions.

The system:

1. Receives multilingual SOS messages.
2. Extracts structured emergency information.
3. Calculates an incident priority score.
4. Matches incidents with available rescue resources.
5. Uses Mixed-Integer Linear Programming (MILP) to optimize assignments.
6. Displays incidents and dispatch routes on an interactive GIS dashboard.

### Core Flow

```text
Citizen SOS
     │
     ▼
┌───────────────────────────┐
│ Multilingual NLP Ingestion│
│ Google Gemini + Fallback  │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│ Incident Structuring      │
│ Victims / Medical / GPS   │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│ Priority Scoring Engine   │
│ Criticality: 0 → 100     │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│ OR-Tools MILP Solver      │
│ Resource Assignment       │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│ GIS Command Dashboard     │
│ React + Leaflet           │
└───────────────────────────┘
```

---

# 🏗️ System Architecture

## 1. Multilingual SOS Ingestion

FloodMesh accepts unstructured emergency messages such as:

```text
100 people trapped on roof near flood embankment,
need food and medicine urgently.
```

The NLP pipeline attempts to identify:

- Number of victims
- Medical urgency
- Isolation condition
- Emergency requirements
- Location information
- Other relevant entities

Supported input can include English, Hindi, Assamese, and other regional-language text depending on the configured model.

### AI Layer

The system uses Google Gemini for natural-language entity extraction.

### Local Fallback

A deterministic regex-based parser can be used when the AI service is unavailable.

This provides a local fallback path for critical parsing operations.

---

# 🎯 2. Dynamic Priority Scoring

Every incident receives a normalized priority score between:

```text
0 ─────────────────────────────── 100
Low                              Critical
```

The conceptual scoring model is:

$$
\text{Priority Score}
=
\min
\left(
100,
\text{Urgency}_{Base}
+
\alpha \log_{10}(\text{Victim Count})
+
\beta \cdot \text{Isolation}
+
\gamma \cdot \text{Medical Factor}
\right)
$$

The scoring engine considers factors such as:

- 👥 Victim count
- 🏥 Medical urgency
- 🌊 Flood/isolation conditions
- 🚨 Base emergency urgency

This converts unstructured emergency information into a numerical value that can be consumed by the optimization engine.

---

# 🧮 3. MILP Resource Optimization

FloodMesh uses **Google OR-Tools** to determine how available rescue resources should be assigned to active incidents.

Let:

- $N$ = set of active incidents
- $M$ = set of available rescue resources
- $x_{i,j} \in \{0,1\}$ = whether resource $j$ is assigned to incident $i$

The optimization objective is:

$$
\max
\sum_{i \in N}
\sum_{j \in M}
x_{i,j}
\left(
\frac{\text{Priority}_i^2}
{\text{Distance}_{i,j}+\epsilon}
\right)
$$

Subject to:

### One Resource Per Incident

$$
\sum_{j \in M}x_{i,j}\leq1
\qquad
\forall i\in N
$$

### One Active Assignment Per Resource

$$
\sum_{i \in N}x_{i,j}\leq1
\qquad
\forall j\in M
$$

This prevents multiple units from being assigned to the same incident unnecessarily while preventing an individual resource from being simultaneously assigned to multiple active tasks.

---

# 🗺️ 4. GIS Command Dashboard

The frontend provides an operational view of the emergency environment.

### Dashboard capabilities

- Real-time incident visualization
- Incident priority indicators
- Interactive map
- Rescue-resource locations
- Dispatch vectors
- Distance calculations
- ETA information
- Incident details
- Optimization results

The map layer is built using:

**React + Leaflet + OpenStreetMap**

---

# 🔥 Key Features

| Feature | Description |
|---|---|
| 🌐 Multilingual SOS | Processes emergency messages in multiple languages |
| 🤖 AI Entity Extraction | Converts natural-language SOS messages into structured data |
| 🛡️ Local Fallback | Regex-based parsing when the AI service is unavailable |
| 🎯 Priority Scoring | Calculates emergency criticality from 0–100 |
| 🧮 MILP Optimization | Mathematically optimizes resource assignments |
| 🚑 Resource Allocation | Matches rescue teams to emergency incidents |
| 🗺️ GIS Dashboard | Displays incidents and dispatch routes |
| 📍 GPS Integration | Associates SOS reports with geographic coordinates |
| 📏 Distance Calculation | Calculates incident-to-resource distance |
| ⏱️ ETA | Displays estimated travel time |
| 📊 Operational View | Provides a centralized emergency command interface |

---

# 🧰 Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| Backend | Python 3.10+ | Core application logic |
| API | FastAPI | Backend API and orchestration |
| AI | Google Gemini | Multilingual NLP and entity extraction |
| Fallback NLP | Python Regex | Local deterministic parsing |
| Optimization | Google OR-Tools / SCIP | MILP resource allocation |
| Frontend | React 18 | Command dashboard |
| Build Tool | Vite | Frontend development/build |
| Styling | Tailwind CSS | UI styling |
| Maps | Leaflet.js | Interactive GIS visualization |
| Map Data | OpenStreetMap | Geographic map layer |
| Database | SQLite / PostgreSQL/PostGIS | Incident and geographic data |

---

# 📁 Project Structure

```text
floodmesh-ai/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   ├── models/
│   │   ├── services/
│   │   ├── optimization/
│   │   └── utils/
│   │
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.jsx
│   │
│   ├── package.json
│   └── vite.config.js
│
├── README.md
├── LICENSE
└── .gitignore
```

> Adjust the structure above if your current repository uses different filenames or directories.

---

# 🚀 Installation

## Prerequisites

Install:

- Git
- Python 3.10+
- Node.js 18+
- npm

---

## 1. Clone the Repository

```bash
git clone https://github.com/yuht-lin/floodmesh-ai.git
cd floodmesh-ai
```

---

# ⚙️ 2. Backend Setup

Navigate to the backend:

```bash
cd backend
```

Create a Python virtual environment:

```bash
python3 -m venv .venv
```

Activate it on Linux/macOS:

```bash
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔑 Configure Gemini API

Create an environment variable containing your Gemini API key.

Linux/macOS:

```bash
export GEMINI_API_KEY="your_api_key_here"
```

Windows PowerShell:

```powershell
$env:GEMINI_API_KEY="your_api_key_here"
```

**Never commit your API key to GitHub.**

---

## ▶️ Start Backend

```bash
uvicorn app.main:app --reload --port 8000
```

Backend:

```text
http://localhost:8000
```

FastAPI documentation:

```text
http://localhost:8000/docs
```

---

# 🖥️ 3. Frontend Setup

Open another terminal.

From the project root:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The dashboard will normally be available at:

```text
http://localhost:3000
```

---

# 🧪 Demo Workflow

## Step 1 — Submit an SOS

Example:

```text
100 people trapped on roof near flood embankment,
need food and medicine urgently.
```

The system attempts to extract:

```json
{
  "victims": 100,
  "medical_urgency": true,
  "isolation": "ROOFTOP_TRAPPED"
}
```

---

## Step 2 — Generate Priority

The extracted incident data is passed through the priority engine.

Example:

```text
Priority Score: 95 / 100
```

The exact score depends on the configured scoring parameters and extracted incident attributes.

---

## Step 3 — Submit a Regional-Language SOS

Example Hindi input:

```text
100 लोगों को तुरंत मदद और भोजन की ज़रूरत है
```

The multilingual NLP layer attempts to interpret the message without requiring the user to manually translate it.

---

## Step 4 — Run Optimization

Trigger:

```text
Recalculate OR-Tools Optimization
```

The optimization engine evaluates:

- Incident priority
- Resource availability
- Distance
- Assignment constraints

and generates the resulting resource assignments.

---

## Step 5 — View Dispatch on the Map

The GIS dashboard displays:

```text
Rescue Team
     │
     │
     ▼
   ────────► Incident
             │
             └── Priority
                 Victims
                 ETA
```

Dispatch vectors can be inspected for distance and estimated arrival information.

---

# 📡 API Reference

## `POST /incidents/ingest`

Parses an unstructured SOS message and generates a structured incident.

### Request

```json
{
  "text": "100 people trapped on roof near flood embankment, need food and medicine urgently",
  "latitude": 26.6331,
  "longitude": 92.8001
}
```

### Example Response

```json
{
  "incident_id": "INC-B189A8",
  "priority_score": 95.0,
  "extracted_entities": {
    "victims": 100,
    "medical_urgency": true,
    "isolation": "ROOFTOP_TRAPPED"
  }
}
```

---

## `POST /allocations/recalculate`

Triggers the optimization engine and recalculates assignments between active incidents and available response resources.

```http
POST /allocations/recalculate
```

The resulting assignments can then be visualized by the frontend dashboard.

---

# 🔐 Reliability & Safety Considerations

FloodMesh AI is designed as a **decision-support and emergency logistics prototype**.

Important considerations include:

- AI extraction should be validated before operational deployment.
- GPS information should be treated as potentially inaccurate.
- Emergency messages may contain false, incomplete, or outdated information.
- Optimization results should remain subject to human emergency-operator oversight.
- API keys and sensitive incident information must never be committed to public repositories.
- Production deployment should include authentication, authorization, audit logging, monitoring, rate limiting, and secure data storage.

**FloodMesh AI should not be treated as a replacement for trained emergency-response personnel.**

---

# 📈 Future Roadmap

### Phase 1 — Core Platform

- [x] Multilingual SOS ingestion
- [x] AI-based entity extraction
- [x] Priority scoring
- [x] MILP resource assignment
- [x] GIS visualization

### Phase 2 — Intelligence

- [ ] Real-time weather integration
- [ ] Flood-level data integration
- [ ] Road accessibility analysis
- [ ] Dynamic ETA calculation
- [ ] Predictive incident clustering
- [ ] Duplicate SOS detection

### Phase 3 — Autonomous Coordination

- [ ] Multi-agency resource coordination
- [ ] Real-time fleet tracking
- [ ] Automated resource reallocation
- [ ] Disaster severity forecasting
- [ ] Satellite imagery integration
- [ ] Offline-first emergency operation mode

### Phase 4 — Large-Scale Deployment

- [ ] PostgreSQL/PostGIS production backend
- [ ] Distributed event processing
- [ ] Authentication and role-based access
- [ ] Audit and incident history
- [ ] High-availability deployment
- [ ] Government/NGO emergency-response integrations

---

# 🌍 Potential Applications

Although FloodMesh AI is designed around flood-response scenarios, the underlying architecture can be adapted to:

- 🌊 Flood response
- 🌪️ Cyclone emergencies
- 🌋 Natural disasters
- 🔥 Wildfire evacuation
- 🏚️ Building-collapse response
- 🚑 Medical emergency coordination
- 🚨 Large-scale search and rescue
- 🌐 Humanitarian logistics

---

# 🧠 Why FloodMesh AI?

Traditional emergency workflows often follow:

```text
SOS
 ↓
Human Triage
 ↓
Manual Prioritization
 ↓
Manual Dispatch
```

FloodMesh AI proposes:

```text
SOS
 ↓
AI Extraction
 ↓
Priority Scoring
 ↓
Mathematical Optimization
 ↓
GIS Dispatch
```

The goal is to reduce the time between **receiving information** and **making an informed resource-allocation decision**.

---

# 📊 Example Scenario

Imagine a flood affecting multiple villages.

```text
Incident A
100 victims
Medical emergency
Rooftop trapped
Priority: 95

Incident B
40 victims
Food required
Priority: 62

Incident C
15 victims
Minor injuries
Priority: 38
```

Available resources:

```text
Rescue Boat 01
Rescue Boat 02
Medical Team 01
```

FloodMesh evaluates the available assignments using the optimization model rather than simply assigning resources in the order that SOS messages arrive.

This allows emergency operators to see a mathematically optimized allocation alongside the underlying incident information.

---

# 🏆 Project Vision

**FloodMesh AI aims to build an intelligent emergency-response coordination layer capable of turning chaotic, multilingual disaster information into structured, explainable and optimized response decisions.**

```text
CHAOS
  │
  ▼
MULTILINGUAL SOS
  │
  ▼
AI UNDERSTANDING
  │
  ▼
PRIORITY
  │
  ▼
OPTIMIZATION
  │
  ▼
RESOURCE ALLOCATION
  │
  ▼
RESCUE
```

---

# 🤝 Contributing

Contributions are welcome.

```bash
git clone https://github.com/yuht-lin/floodmesh-ai.git
cd floodmesh-ai
git checkout -b feature/your-feature
```

Make your changes, test them, and submit a pull request.

For major changes, open an issue first to discuss the proposed architecture or implementation.

---

# 📄 License

This project is licensed under the **MIT License**.

See [`LICENSE`](LICENSE) for details.

---

<div align="center">

### 🌊 FloodMesh AI

**AI for Emergency Intelligence • Optimization for Resource Allocation • Technology for Resilience**

</div>
```
