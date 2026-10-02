# Automated Micro-Influencer Outreach System
### Autonomous Creator Discovery, Context Enrichment & Multi-Channel AI Personalization Engine

An automated, end-to-end intelligent pipeline that discovers authentic micro-influencers across platforms, evaluates them according to multi-factor quantitative and qualitative criteria, enriches their profiles with contextual intelligence, and generates hyper-personalized collaboration outreach messages via Google Gemini LLM with an integrated delivery and tracking layer.

---

## 📑 Table of Contents
1. [System Architecture](#-system-architecture)
2. [Technology Stack](#-technology-stack)
3. [Core Pipeline Phases](#-core-pipeline-phases)
   - [Phase 1: Discovery Engine](#phase-1-influencer-discovery)
   - [Phase 2: Filtering & Classification](#phase-2-filtering--classification)
   - [Phase 3: Profile Enrichment](#phase-3-profile-enrichment)
   - [Phase 4: AI Personalization Engine](#phase-4-ai-personalization-engine)
   - [Phase 5: Sending Layer & Outreach Tracker](#phase-5-sending-layer--outreach-tracker)
4. [Data Architecture & Schemas](#-data-architecture--schemas)
5. [Setup & Execution Instructions](#-setup--execution-instructions)
6. [Design Decisions & Compliance](#-design-decisions--compliance)

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    A["1. Discovery Engine<br/>(Scrapy & Playwright Crawlers)"] -->|"270+ Creator Profiles"| B["2. Profile Enrichment<br/>(Themes, Demographics, Emails)"]
    B --> C["3. Filtering & Classification<br/>(Follower Range, Engagement, Brand Fit)"]
    C -->|"Passed Criteria"| D["4. AI Personalization Studio<br/>(Google Gemini LLM)"]
    C -->|"Disqualified"| J["Disqualification Audit<br/>(Explicit Metric Reasons)"]
    D -->|"Email: 60-90w & DM: 15-30w"| E["5. Sending Layer<br/>(Resend API / DM Workflow)"]
    E --> F["6. Outreach Audit Tracker<br/>(Neon PostgreSQL / Deduplication)"]
    F --> G["7. Presentation Layer<br/>(React + Vite Dashboard & FastAPI)"]
```

---

## 🛠️ Technology Stack

| Component | Technology | Rationale |
| :--- | :--- | :--- |
| **Frontend Dashboard** | **React 18** + **Vite** + **Tailwind CSS** | High-performance, responsive UI with real-time creator search, interactive filtering, and pitch dispatch. |
| **Backend API** | **FastAPI** + **Uvicorn** | Asynchronous REST backend handling pipeline orchestration, AI generation, and database synchronization. |
| **Database** | **Neon PostgreSQL** (Cloud Serverless) | Scalable PostgreSQL database with pooled connections and atomic batch upserts for creator metrics. |
| **Scraping Framework** | **Scrapy 2.19** + **Playwright** | Asynchronous crawling engine extracting public creator handles, metrics, bios, and engagement stats. |
| **AI Personalization** | **Google Gemini LLM** (`gemini-2.5-flash`) | Rapid LLM generation with strict JSON schema validation for length, tone, and contextual alignment. |
| **Email Delivery** | **Resend** (`resend` Python SDK) | Modern transactional email API with sandbox simulation, delivery status tracking, and verification. |
| **Data Processing** | **Pandas** & **Pydantic** | Strict schema validation, data deduplication, and structured CSV/JSON persistence. |

---

## 🚀 Core Pipeline Phases

### Phase 1: Influencer Discovery
- **Engine**: Asynchronous web crawler built with Scrapy and Playwright to extract creator public profiles.
- **Target Niches**: Fashion & Beauty, Gaming, Tech, Fitness, and Lifestyle.
- **Yield**: Discovers **270+ creator profiles** with handles, platform links, geographic locations, ratings, and follower metrics.

### Phase 2: Filtering & Classification
Every creator is evaluated using multi-dimensional criteria:
1. **Follower Count Bounds**: Configurable micro-influencer window (e.g. $5,000 \le \text{followers} \le 100,000$).
2. **Minimum Engagement Rate**: Dynamic engagement threshold (e.g. $\ge 2.0\%$).
3. **Audience Geography & Platform Alignment**: Regional matching (e.g. India, US, UK, Global) and platform availability (Instagram & TikTok).
4. **Category Relevance**: Contextual token analysis against target niche content.

**Output Guarantee**: Every creator profile is classified with `PASSED` or `FAILED` accompanied by an explicit evaluation reason.

### Phase 3: Profile Context Enrichment
Each profile is enriched with structured metadata:
- **Verified Metrics**: Platform handle, profile URL, follower count, engagement rate, primary category.
- **Content Themes & Context**: Extracted bio keywords and core styling/content focus areas.
- **Audience Demographics**: Core age cohort, gender distribution, and top geographic locations.
- **Contact Extraction**: Verified contact email (marked strictly as `"Not Found"` if unavailable—never guessed or hallucinated).

### Phase 4: AI Personalization Engine
Generates two tailored outreach messages per shortlisted creator via Google Gemini:
1. **Email Collaboration Pitch**:
   - **Target**: 60–90 words.
   - **Elements**: Contextual compliment referencing creator themes, proposed collaboration angle (UGC, paid showcase, brand ambassador), clear compensation offer, and low-friction call-to-action.
2. **Instagram Direct Message (DM)**:
   - **Target**: 15–30 words.
   - **Tone**: Authentic, friendly conversation starter tailored to recent content.

### Phase 5: Sending Layer & Outreach Tracker
- **Email Channel**: Dispatches emails via **Resend API** in Live Mode, or simulates delivery in Safe Simulation Mode (`sim_<hash>`).
- **Instagram DM Channel**: Integrated direct message workflow with deep-links (`https://ig.me/m/<handle>`), respecting Meta Graph API boundaries.
- **Deduplication Engine**: Prevents duplicate outreach attempts by verifying prior handles and email hashes.
- **Audit Log**: Persistent records stored in **Neon PostgreSQL** and mirrored in `data/outreach_log.csv`.

---

## 📊 Data Architecture & Schemas

The pipeline maintains persistent, structured records across:

1. **`data/influencers_raw.csv`**: Raw creator records extracted by discovery crawlers.
2. **`data/influencers_processed.csv`**: Enriched dataset with `qualification_status` and `qualification_reason`.
3. **`data/outreach_log.csv`**: Outreach tracking history with message payloads, delivery IDs, timestamps, and delivery statuses.
4. **Neon PostgreSQL Cloud Tables**: Synchronized cloud storage with indexed handles and execution timestamps.

---

## 💻 Setup & Execution Instructions

### 1. Clone & Set Up Environment
```bash
# Clone the repository
git clone https://github.com/honoursbhaduria/exspo-mailing-agent.git
cd exspo-mailing-agent

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Configure your keys:
```env
GEMINI_API_KEY=your_gemini_api_key_here
RESEND_API_KEY=your_resend_api_key_here
DATABASE_URL=postgresql://user:pass@host/neondb?sslmode=require
DATABASE_URL_POOLED=postgresql://user:pass@host-pooler/neondb?sslmode=require
SIMULATION_MODE=True
```
> **Note:** The system includes complete fallback generators and a sandbox simulator, allowing it to run out-of-the-box even without active external API keys.

### 3. Launch Dashboards & API

```bash
# Terminal 1: Start FastAPI Backend
./venv/bin/python3 -m uvicorn server:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Start Vite React Frontend
cd frontend
npm install
npm run dev
```
Open **`http://localhost:3000`** in your browser to access the interactive React dashboard.

### 4. Run Automated Test Suite
To run the automated verification suite:
```bash
./venv/bin/python -m unittest discover -s tests -v
```

### 5. Run Headless CLI Pipeline
To run the end-to-end automated pipeline in the terminal:
```bash
./venv/bin/python run_pipeline.py
```

---

## ⚖️ Design Decisions & Compliance

1. **Meta Graph API Compliance**: To respect Meta platform policies regarding automated cold messaging, the system generates targeted DM copy and provides a 1-click dispatch workflow + simulated audit logging.
2. **Anti-Hallucination Email Policy**: Missing contact emails are strictly marked as `"Not Found"`. Creators without public emails are automatically routed to the Instagram DM outreach workflow.
3. **Safe Simulation Mode**: A global simulation toggle guarantees that users can run the entire pipeline end-to-end without sending unsolicited live emails or requiring paid credentials.
4. **Idempotency & Deduplication**: Prevents sending duplicate pitches to the same handle or email, maintaining a verifiable audit trail.
