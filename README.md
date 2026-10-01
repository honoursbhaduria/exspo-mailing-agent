# Automated Micro-Influencer Outreach System
### EDXSO AI Engineer Intern – Assignment 1

An automated, end-to-end intelligent pipeline that discovers authentic micro-influencers, filters and classifies them according to multi-factor criteria, enriches their profiles with contextual intelligence, and generates hyper-personalized collaboration outreach messages via LLMs with a multi-channel delivery & tracking layer.

![EDXSO Logo](images/logo.png)

---

## 📑 Table of Contents
1. [System Architecture](#-system-architecture)
2. [Technology Stack](#-technology-stack)
3. [Core Pipeline Phases](#-core-pipeline-phases)
   - [Phase 1: Discovery Engine](#phase-1-influencer-discovery-scrapy)
   - [Phase 2: Filtering & Classification](#phase-2-filtering--classification)
   - [Phase 3: Profile Enrichment](#phase-3-profile-enrichment)
   - [Phase 4: AI Personalization Engine](#phase-4-ai-personalization-engine)
   - [Phase 5: Sending Layer & Tracker](#phase-5-sending-layer--outreach-tracker)
4. [Deliverables & Data Schemas](#-deliverables--data-schemas)
5. [Setup & Execution Instructions](#-setup--execution-instructions)
6. [Design Decisions & Limitations](#-design-decisions--limitations)

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    A["1. Discovery Engine<br/>(Scrapy Async Spider)"] -->|65+ Authentic Profiles| B["2. Profile Enrichment<br/>(Themes, Demographics, Emails)"]
    B --> C["3. Filtering & Classification<br/>(Follower Range, Eng Rate, Brand Fit)"]
    C -->|Passed (29 Qualified)| D["4. AI Personalization Studio<br/>(Google Gemini / Dynamic LLM)"]
    C -->|Failed (36 Disqualified)| J["Disqualification Audit<br/>(Explicit Failure Reasons)"]
    D -->|Email: 60-90w & DM: 15-30w| E["5. Sending Layer<br/>(Resend API / Safe Simulator)"]
    E --> F["6. Outreach Audit Tracker<br/>(Deduplication + Status Logs)"]
    F --> G["7. Presentation Layer<br/>(Streamlit Web Dashboard + CLI)"]
```

---

## 🛠️ Technology Stack

| Component | Technology | Rationale |
| :--- | :--- | :--- |
| **Scraping Framework** | **Scrapy 2.19** + **Requests Middleware** | Production-grade, asynchronous crawler architecture bypassing TLS fingerprinting via standard HTTP adapters. |
| **Email Delivery** | **Resend** (`resend` Python SDK) | Modern transactional email API with 3,000 free emails/month, delivery status tracking, and safe simulation sandbox. |
| **AI Personalization** | **Google Gemini** (`google-genai` SDK) | Ultra-fast LLM generation with strict JSON formatting for word counts and contextual hook alignment. |
| **Data Processing** | **Pandas** & **Pydantic** | Strict schema validation, data deduplication, and structured CSV/JSON persistence. |
| **Web Dashboard** | **Streamlit** | Interactive UI with landing page overview, real-time filtering sliders, AI preview cards, and CSV export. |
| **CLI Presentation** | **Rich** | Formatted terminal tables, colors, and progress indicators for headless runs. |

---

## 🚀 Core Pipeline Phases

### Phase 1: Influencer Discovery (Scrapy)
- **Engine**: Custom `MicroInfluencerSpider` built in Scrapy with an asynchronous crawling process.
- **Target Category**: Fashion & Beauty (with support for Tech, Fitness, Lifestyle).
- **Yield**: Discovers **65+ real creator profiles** with handles, platform links, locations, ratings, and follower metrics.

### Phase 2: Filtering & Classification
Every influencer is evaluated using deterministic criteria:
1. **Follower Count Bounds**: $5,000 \le \text{followers} \le 100,000$ (Micro-influencer criteria).
2. **Engagement Rate**: $\ge 2.0\%$ threshold.
3. **Category Relevance**: Contextual matching against target niche tokens.

**Output Guarantee**: Every record is tagged with `PASSED` or `FAILED` accompanied by the exact reason (e.g. *"Follower count 4,200 is below minimum threshold (5,000)"* or *"Engagement rate 1.50% is below required threshold (2.00%)"*).

### Phase 3: Profile Enrichment
Each profile is enriched with:
- **Mandatory Fields**: Name, Platform, Profile URL, Follower Count, Engagement Rate, Category, Content Themes, Contact Email (marked strictly as `"Not Found"` if unavailable—never guessed or hallucinated).
- **Optional Context**: Instagram / TikTok handles, Audience Geography, Audience Age distribution, and Audience Gender ratio.

### Phase 4: AI Personalization Engine
Dynamically generates two tailored outreach messages per shortlisted creator:
1. **Email Collaboration Pitch**:
   - **Target**: 60–90 words.
   - **Elements**: Specific compliment on recent content theme, proposed collaboration angle (UGC, sponsorship, affiliate), compensation value proposition, and low-friction call to action.
2. **Instagram DM**:
   - **Target**: 15–30 words.
   - **Tone**: Casual, human, authentic conversation starter.

### Phase 5: Sending Layer & Outreach Tracker
- **Email Channel**: Dispatches emails via **Resend API** in Live Mode, or simulates delivery in Safe Simulation Mode (`sim_<hash>`).
- **Instagram DM Channel**: Compliant simulated workflow with deep-links to creator DMs (`https://ig.me/m/<handle>`), respecting Meta Graph API restrictions.
- **Deduplication Engine**: Prevents duplicate contact attempts by checking prior handles and email hashes.
- **Audit Log**: Persistent records stored in `data/outreach_log.csv`.

---

## 📊 Deliverables & Data Schemas

The repository includes all primary artifacts required by the assignment:

1. **`data/influencers_raw.csv`**: 65 authentic influencer records collected by Scrapy.
2. **`data/influencers_processed.csv`**: Enriched dataset with `qualification_status` and `qualification_reason`.
3. **`data/outreach_log.csv`**: Outreach tracking history with message payloads, delivery IDs, timestamps, and delivery statuses.

---

## 💻 Setup & Execution Instructions

### 1. Clone & Set Up Environment
```bash
# Clone the repository
git clone https://github.com/your-username/edxso-A1.git
cd edxso-A1

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables (Optional)
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Configure your keys if you want live API calls:
```env
GEMINI_API_KEY=your_gemini_api_key_here
RESEND_API_KEY=your_resend_api_key_here
SIMULATION_MODE=True
```
> **Note:** The system includes complete fallback generators and a sandbox simulator, so it runs out-of-the-box even without active API keys!

### 3. Launch Interactive Dashboards & API

#### Option A: Production React + TypeScript + Tailwind CSS v4 Frontend (Recommended)
```bash
# 1. Start FastAPI Backend (Terminal 1)
./venv/bin/python3 -m uvicorn server:app --host 0.0.0.0 --port 8000

# 2. Start Vite React Frontend (Terminal 2)
cd frontend
npm install
npm run dev
```
Open **`http://localhost:3000`** to view the fullstack React dashboard with live proxy to FastAPI on port 8000.

#### Option B: Streamlit Python Dashboard
```bash
./venv/bin/streamlit run app.py --server.port 8501
```
Open **`http://localhost:8501`** in your browser.

### 4. Run Automated Unit Test Suite
To run the automated verification suite validating all 5 assignment requirements:
```bash
./venv/bin/python -m unittest discover -s tests -v
```

### 5. Run Headless CLI Pipeline
To run the full end-to-end automated pipeline in the terminal:
```bash
./venv/bin/python run_pipeline.py
```

---

## ⚖️ Design Decisions & Limitations

1. **Meta Graph API Compliance**: Meta prohibits automated cold DMs from unofficial bots to creator personal inboxes. To ensure platform compliance, our system generates the DM and provides a 1-click manual dispatch workflow + simulated audit log.
2. **Anti-Hallucination Email Policy**: As required by Section 3, missing contact emails are strictly marked as `"Not Found"`. Creators without public emails are automatically routed to the Instagram DM outreach workflow.
3. **Safe Simulation Mode**: A global simulation toggle guarantees that evaluators can run the entire pipeline end-to-end without sending unsolicited emails to real creators or requiring paid credentials.
4. **Idempotency & Deduplication**: Prevents sending duplicate pitches to the same handle or email, maintaining a verifiable audit trail in `data/outreach_log.csv`.

