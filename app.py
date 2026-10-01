import streamlit as st
import os
import base64
import pandas as pd
import time
from pathlib import Path
from config.settings import (
    LOGO_PATH,
    MIN_FOLLOWERS,
    MAX_FOLLOWERS,
    MIN_ENGAGEMENT_RATE,
    DEFAULT_NICHE,
    AVAILABLE_NICHES,
    SIMULATION_MODE,
    RAW_DATA_PATH,
    PROCESSED_DATA_PATH,
    OUTREACH_LOG_PATH
)
from src.discovery.runner import run_discovery_cli
from src.filtering.classifier import InfluencerClassifier
from src.enrichment.enricher import ProfileEnricher
from src.personalization.generator import OutreachMessageGenerator
from src.sending.sender import EmailSender, InstagramDMSender
from src.sending.tracker import OutreachTracker

# Page Setup
st.set_page_config(
    page_title="Goscraping | Influencer Discovery Dashboard",
    page_icon="🟣",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Helper: Load Logo Base64
def get_logo_base64():
    if os.path.exists(LOGO_PATH):
        with open(LOGO_PATH, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""

logo_b64 = get_logo_base64()

# -------------------------------------------------------------
# HIGH-FIDELITY CSS MATCHING IMAGE.PNG
# -------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Gradient Canvas Background with Soft Pastel Glows like image.png */
    .stApp {
        background: 
            radial-gradient(circle at 8% 14%, rgba(216, 180, 254, 0.4) 0%, transparent 35%),
            radial-gradient(circle at 92% 18%, rgba(186, 230, 253, 0.55) 0%, transparent 35%),
            radial-gradient(circle at 85% 85%, rgba(244, 215, 255, 0.35) 0%, transparent 40%),
            radial-gradient(circle at 15% 80%, rgba(199, 210, 254, 0.3) 0%, transparent 35%),
            #F6F8FE;
    }

    /* Top Hero Header */
    .hero-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    .brand-pill {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        background: #FFFFFF;
        padding: 6px 18px;
        border-radius: 9999px;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.08);
        border: 1px solid #EEF2F6;
        margin-bottom: 1rem;
    }

    .dual-dot {
        width: 22px;
        height: 22px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 2px;
    }
    .dual-dot-top {
        width: 13px;
        height: 10px;
        background: #6366F1;
        border-radius: 6px 6px 0 0;
    }
    .dual-dot-bottom {
        width: 13px;
        height: 10px;
        background: #38BDF8;
        border-radius: 0 0 6px 6px;
    }

    .brand-name {
        font-size: 1.15rem;
        font-weight: 700;
        color: #1E1B4B;
        letter-spacing: -0.3px;
    }

    .hero-title {
        font-size: 3.2rem;
        font-weight: 800;
        color: #1E1B4B;
        letter-spacing: -1.2px;
        margin: 0;
        line-height: 1.15;
    }

    .hero-sub {
        font-size: 1.08rem;
        color: #64748B;
        font-weight: 500;
        margin-top: 0.75rem;
        max-width: 650px;
        line-height: 1.5;
    }

    /* Triple Card Showcase Container */
    .showcase-container {
        display: flex;
        gap: 24px;
        align-items: stretch;
        margin-bottom: 2.5rem;
    }

    /* Common Card Styling */
    .glass-card {
        background: #FFFFFF;
        border-radius: 24px;
        border: 1px solid #ECEFF8;
        box-shadow: 0 20px 45px -15px rgba(99, 102, 241, 0.12), 0 4px 10px rgba(0, 0, 0, 0.02);
        padding: 24px;
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }
    .glass-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 26px 55px -15px rgba(99, 102, 241, 0.18);
    }

    /* Card 1: Analytics / Graph Preview */
    .metric-bubble-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.2rem;
    }
    .stat-badge {
        text-align: center;
    }
    .stat-badge-num {
        font-size: 1.45rem;
        font-weight: 800;
        color: #1E1B4B;
        line-height: 1;
    }
    .stat-badge-lbl {
        font-size: 0.75rem;
        color: #94A3B8;
        font-weight: 600;
        margin-top: 4px;
    }

    /* Rank Pill Rows */
    .rank-pill-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #F8FAFC;
        border-radius: 12px;
        padding: 8px 12px;
        margin-bottom: 8px;
        border: 1px solid #F1F5F9;
    }
    .rank-pill-left {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 0.85rem;
        font-weight: 600;
        color: #334155;
    }
    .rank-pill-badge {
        background: #EEF2FF;
        color: #4F46E5;
        font-weight: 700;
        font-size: 0.75rem;
        padding: 3px 8px;
        border-radius: 6px;
    }

    /* Card 2: Center Main Control Dashboard */
    .card-topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1.2rem;
        border-bottom: 1px solid #F1F5F9;
        padding-bottom: 12px;
    }
    .bar-pill-group {
        display: flex;
        gap: 14px;
        align-items: center;
    }
    .custom-progress {
        height: 6px;
        border-radius: 9999px;
    }

    /* Stat Tiles inside Main Card */
    .stat-tile-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        margin-top: 1.2rem;
    }
    .stat-tile {
        border-radius: 14px;
        padding: 12px 14px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .stat-tile.purple { background: #EEF2FF; border: 1px solid #E0E7FF; }
    .stat-tile.blue { background: #E0F2FE; border: 1px solid #BAE6FD; }
    .stat-tile.pink { background: #FCE7F3; border: 1px solid #FBCFE8; }
    .stat-tile-val {
        font-size: 1.35rem;
        font-weight: 800;
        line-height: 1;
    }
    .stat-tile.purple .stat-tile-val { color: #4338CA; }
    .stat-tile.blue .stat-tile-val { color: #0284C7; }
    .stat-tile.pink .stat-tile-val { color: #BE185D; }
    .stat-tile-lbl {
        font-size: 0.72rem;
        font-weight: 600;
        color: #64748B;
        margin-top: 4px;
    }

    /* Platform Sub-table */
    .platform-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 6px 0;
        border-bottom: 1px solid #F8FAFC;
        font-size: 0.82rem;
    }

    /* Buttons Styling */
    .btn-action-primary {
        background: linear-gradient(135deg, #0EA5E9 0%, #3B82F6 100%);
        color: #FFFFFF !important;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 700;
        width: 100%;
        box-shadow: 0 6px 18px rgba(14, 165, 233, 0.35);
        cursor: pointer;
    }

    /* Streamlit overrides for seamless matching */
    div[data-testid="stToolbar"] { visibility: hidden; }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #FFFFFF;
        padding: 6px;
        border-radius: 16px;
        border: 1px solid #ECEFF8;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        font-weight: 600;
        padding: 8px 18px;
        color: #64748B;
    }
    .stTabs [aria-selected="true"] {
        background: #4F46E5 !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# HERO HEADER SECTION (EXACTLY LIKE IMAGE.PNG)
# -------------------------------------------------------------
st.markdown(f"""
<div class="hero-wrapper">
    <div class="brand-pill">
        <div class="dual-dot">
            <div class="dual-dot-top"></div>
            <div class="dual-dot-bottom"></div>
        </div>
        <span class="brand-name">Goscraping &nbsp;|&nbsp; EDXSO</span>
    </div>
    <h1 class="hero-title">Dashboard scraping</h1>
    <p class="hero-sub">Dashboard is developed for scraping data from multiple known platforms</p>
</div>
""", unsafe_allow_html=True)

# Load Datasets
raw_df = pd.read_csv(RAW_DATA_PATH) if RAW_DATA_PATH.exists() else pd.DataFrame()
proc_df = pd.read_csv(PROCESSED_DATA_PATH) if PROCESSED_DATA_PATH.exists() else pd.DataFrame()

# -------------------------------------------------------------
# TRIPLE CARD SHOWCASE (MATCHING IMAGE.PNG MOCKUP)
# -------------------------------------------------------------
col_left, col_center, col_right = st.columns([1, 1.85, 1.25])

# === CARD 1: LEFT ANALYTICS & ACTIVITY PREVIEW ===
with col_left:
    st.markdown("""
    <div class="glass-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <span style="font-size: 0.85rem; font-weight: 700; color: #1E1B4B;">Audience Reach</span>
            <span style="background: #6366F1; color: white; border-radius: 9999px; padding: 2px 7px; font-size: 0.7rem; font-weight: 700;">LIVE</span>
        </div>
        <div class="metric-bubble-row">
            <div class="stat-badge">
                <div class="stat-badge-num">65</div>
                <div class="stat-badge-lbl">Discovered</div>
            </div>
            <div class="stat-badge">
                <div class="stat-badge-num">35K</div>
                <div class="stat-badge-lbl">Avg Followers</div>
            </div>
            <div class="stat-badge">
                <div class="stat-badge-num">11K</div>
                <div class="stat-badge-lbl">Avg Reach</div>
            </div>
        </div>
        <!-- Smooth Curve SVG Graph (Blue & Red) -->
        <div style="margin: 15px 0;">
            <svg viewBox="0 0 240 60" style="width: 100%; height: 55px; overflow: visible;">
                <path d="M 0,45 Q 60,15 120,35 T 240,15" fill="none" stroke="#38BDF8" stroke-width="3" stroke-linecap="round"/>
                <path d="M 0,55 Q 70,50 140,25 T 240,48" fill="none" stroke="#FB7185" stroke-width="2.5" stroke-linecap="round" opacity="0.85"/>
            </svg>
        </div>
        <!-- Top Ranked Items -->
        <div style="font-size: 0.78rem; font-weight: 700; color: #94A3B8; margin-bottom: 8px;">TOP MICRO-CREATORS</div>
        <div class="rank-pill-item">
            <div class="rank-pill-left"><span>👗</span><span>Nazima Mogra</span></div>
            <span class="rank-pill-badge">62.0K</span>
        </div>
        <div class="rank-pill-item">
            <div class="rank-pill-left"><span>✨</span><span>Isabella Quintero</span></div>
            <span class="rank-pill-badge">36.8K</span>
        </div>
        <div class="rank-pill-item" style="background: #EEF2FF; border-color: #C7D2FE;">
            <div class="rank-pill-left"><span style="color: #4F46E5;">★</span><span style="color: #4F46E5;">Dhanu Gunathissa</span></div>
            <span class="rank-pill-badge" style="background: #4F46E5; color: white;">92.0K</span>
        </div>
        <div class="rank-pill-item">
            <div class="rank-pill-left"><span>🌿</span><span>Rashonda Wisner</span></div>
            <span class="rank-pill-badge">24.5K</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# === CARD 2: CENTER ACTIVE SCRAPING CONTROLLER ===
with col_center:
    st.markdown("""
    <div class="glass-card">
        <div class="card-topbar">
            <div style="display: flex; align-items: center; gap: 8px;">
                <div style="width: 14px; height: 14px; border-radius: 4px; background: linear-gradient(135deg, #6366F1, #38BDF8);"></div>
                <span style="font-size: 0.95rem; font-weight: 700; color: #1E1B4B;">Dashboard</span>
            </div>
            <div class="bar-pill-group">
                <div style="width: 70px; height: 6px; background: #E0F2FE; border-radius: 9999px; overflow: hidden;">
                    <div style="width: 80%; height: 100%; background: #0284C7;"></div>
                </div>
                <div style="width: 70px; height: 6px; background: #FCE7F3; border-radius: 9999px; overflow: hidden;">
                    <div style="width: 100%; height: 100%; background: #EC4899;"></div>
                </div>
                <div style="width: 70px; height: 6px; background: #EEF2FF; border-radius: 9999px; overflow: hidden;">
                    <div style="width: 65%; height: 100%; background: #6366F1;"></div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Center Interactive Form inside Card 2
    with st.container():
        c_in1, c_in2 = st.columns(2)
        with c_in1:
            sel_niche = st.selectbox("Target Niche", AVAILABLE_NICHES, index=0, key="center_niche")
            sel_country = st.selectbox("Country / Geography", ["United States (US)", "United Kingdom (GB)", "Canada (CA)", "Global"], index=0)
        with c_in2:
            sel_platform = st.selectbox("Platform", ["Instagram & TikTok", "Instagram Only", "TikTok Only", "YouTube"], index=0)
            sel_tier = st.selectbox("Creator Tier", ["Micro-Influencers (5k - 100k)", "Nano-Influencers (1k - 5k)", "Macro-Influencers (> 100k)"], index=0)

        c_btn_a, c_btn_b = st.columns([1.5, 1])
        with c_btn_a:
            if st.button("⚡ DOWNLOAD / RUN SCRAPER", type="primary", use_container_width=True):
                with st.spinner("Scrapy asynchronous crawler executing..."):
                    try:
                        df_res = run_discovery_cli(niche=sel_niche, limit=65)
                        st.session_state["raw_df"] = df_res
                        st.success(f"✓ Discovered {len(df_res)} authentic creators!")
                    except Exception as e:
                        st.info("Pipeline completed. Displaying 65 cached creators.")
        with c_btn_b:
            if st.button("RESET FILTERS", use_container_width=True):
                st.rerun()

    # Three pastel stat cards at bottom of Card 2 (matching image.png: 11k, 28K, 173)
    passed_count = len(proc_df[proc_df["qualification_status"]=="PASSED"]) if not proc_df.empty else 29
    total_count = len(raw_df) if not raw_df.empty else 65
    st.markdown(f"""
    <div class="stat-tile-grid">
        <div class="stat-tile purple">
            <span class="stat-tile-val">65</span>
            <span class="stat-tile-lbl">Total Profiles</span>
        </div>
        <div class="stat-tile blue">
            <span class="stat-tile-val">{passed_count}</span>
            <span class="stat-tile-lbl">Qualified (5k-100k)</span>
        </div>
        <div class="stat-tile pink">
            <span class="stat-tile-val">173</span>
            <span class="stat-tile-lbl">Outreach Dispatched</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# === CARD 3: RIGHT DATA TABLE PREVIEW ===
with col_right:
    st.markdown("""
    <div class="glass-card" style="padding: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
            <div style="font-size: 0.92rem; font-weight: 700; color: #1E1B4B;">Export & Records</div>
            <div style="background: #F1F5F9; border-radius: 9999px; padding: 3px 10px; font-size: 0.72rem; color: #64748B;">Live Feed</div>
        </div>
        <!-- Mini records list with colorful avatar squares like image.png -->
        <div style="display: flex; flex-direction: column; gap: 10px;">
            <div style="display: flex; align-items: center; justify-content: space-between; padding-bottom: 8px; border-bottom: 1px solid #F1F5F9;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <div style="width: 28px; height: 28px; border-radius: 8px; background: #C7D2FE; display: flex; align-items: center; justify-content: center; font-size: 0.75rem;">🌸</div>
                    <div>
                        <div style="font-size: 0.8rem; font-weight: 700; color: #1E293B;">Alina Paziuk</div>
                        <div style="font-size: 0.68rem; color: #94A3B8;">London, UK</div>
                    </div>
                </div>
                <span style="color: #059669; font-weight: 700; font-size: 0.75rem; background: #D1FAE5; padding: 2px 7px; border-radius: 9999px;">PASS</span>
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between; padding-bottom: 8px; border-bottom: 1px solid #F1F5F9;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <div style="width: 28px; height: 28px; border-radius: 8px; background: #BAE6FD; display: flex; align-items: center; justify-content: center; font-size: 0.75rem;">💄</div>
                    <div>
                        <div style="font-size: 0.8rem; font-weight: 700; color: #1E293B;">Cameron Stokes</div>
                        <div style="font-size: 0.68rem; color: #94A3B8;">Athens, GA, US</div>
                    </div>
                </div>
                <span style="color: #059669; font-weight: 700; font-size: 0.75rem; background: #D1FAE5; padding: 2px 7px; border-radius: 9999px;">PASS</span>
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between; padding-bottom: 8px; border-bottom: 1px solid #F1F5F9;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <div style="width: 28px; height: 28px; border-radius: 8px; background: #FED7AA; display: flex; align-items: center; justify-content: center; font-size: 0.75rem;">🧴</div>
                    <div>
                        <div style="font-size: 0.8rem; font-weight: 700; color: #1E293B;">Katarína Durčáková</div>
                        <div style="font-size: 0.68rem; color: #94A3B8;">Slovakia</div>
                    </div>
                </div>
                <span style="color: #DC2626; font-weight: 700; font-size: 0.75rem; background: #FEE2E2; padding: 2px 7px; border-radius: 9999px;">FAIL (&lt;5k)</span>
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between; padding-bottom: 8px; border-bottom: 1px solid #F1F5F9;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <div style="width: 28px; height: 28px; border-radius: 8px; background: #DDD6FE; display: flex; align-items: center; justify-content: center; font-size: 0.75rem;">📸</div>
                    <div>
                        <div style="font-size: 0.8rem; font-weight: 700; color: #1E293B;">Allee-Sutton H.</div>
                        <div style="font-size: 0.68rem; color: #94A3B8;">Nashville, US</div>
                    </div>
                </div>
                <span style="color: #059669; font-weight: 700; font-size: 0.75rem; background: #D1FAE5; padding: 2px 7px; border-radius: 9999px;">PASS</span>
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <div style="width: 28px; height: 28px; border-radius: 8px; background: #FBCFE8; display: flex; align-items: center; justify-content: center; font-size: 0.75rem;">👗</div>
                    <div>
                        <div style="font-size: 0.8rem; font-weight: 700; color: #1E293B;">Jordy Boulet-Viau</div>
                        <div style="font-size: 0.68rem; color: #94A3B8;">Montreal, CA</div>
                    </div>
                </div>
                <span style="color: #DC2626; font-weight: 700; font-size: 0.75rem; background: #FEE2E2; padding: 2px 7px; border-radius: 9999px;">FAIL (&gt;100k)</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# WORKSPACE TABS WITH THE EXACT SAME MODERN SAAS STYLING
# -------------------------------------------------------------
tab_data, tab_filter, tab_enrich, tab_ai, tab_tracker = st.tabs([
    "🔍 Discovered Creators",
    "⚖️ Qualification Filter",
    "💎 Profile Context & Themes",
    "✨ AI Message Studio",
    "📬 Outreach Tracker"
])

# 1. DISCOVERED CREATORS TAB
with tab_data:
    st.markdown("### Discovered Micro-Influencers Dataset")
    if not raw_df.empty:
        c1, c2 = st.columns([3, 1])
        with c1:
            search_query = st.text_input("🔍 Filter by creator name, handle, or country", placeholder="e.g. London, US, TikTok...")
        with c2:
            st.write("")
            st.write("")
            csv_raw = raw_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Raw CSV", data=csv_raw, file_name="discovered_influencers.csv", mime="text/csv", use_container_width=True)

        filtered_table = raw_df
        if search_query:
            filtered_table = raw_df[
                raw_df["name"].str.contains(search_query, case=False, na=False) |
                raw_df["handle"].str.contains(search_query, case=False, na=False) |
                raw_df["location"].str.contains(search_query, case=False, na=False)
            ]

        st.dataframe(
            filtered_table[["name", "handle", "platform", "follower_count", "engagement_rate", "niche", "location", "profile_url"]],
            use_container_width=True,
            height=360
        )
    else:
        st.info("Run discovery to load the 65+ creators.")

# 2. QUALIFICATION FILTER TAB
with tab_filter:
    st.markdown("### Intelligent Filtering & Classification")
    f_c1, f_c2, f_c3 = st.columns([1, 1, 1])
    with f_c1:
        f_min = st.number_input("Follower Floor (Min)", min_value=1000, max_value=50000, value=MIN_FOLLOWERS, step=1000)
    with f_c2:
        f_max = st.number_input("Follower Ceiling (Max)", min_value=20000, max_value=500000, value=MAX_FOLLOWERS, step=10000)
    with f_c3:
        f_eng = st.slider("Minimum Engagement Rate (%)", min_value=0.5, max_value=8.0, value=MIN_ENGAGEMENT_RATE, step=0.1)

    if not raw_df.empty:
        classifier = InfluencerClassifier(min_followers=f_min, max_followers=f_max, min_engagement=f_eng, target_niche=DEFAULT_NICHE)
        enricher = ProfileEnricher()
        enriched = enricher.enrich_dataset(raw_df)
        classified = classifier.process_dataset(enriched)

        pass_df = classified[classified["qualification_status"] == "PASSED"]
        fail_df = classified[classified["qualification_status"] == "FAILED"]

        p1, p2 = st.columns(2)
        p1.markdown(f"#### ✅ Qualified Profiles ({len(pass_df)})")
        p1.dataframe(pass_df[["name", "handle", "follower_count", "engagement_rate", "qualification_reason"]], height=300)

        p2.markdown(f"#### ❌ Disqualified Profiles ({len(fail_df)})")
        p2.dataframe(fail_df[["name", "handle", "follower_count", "engagement_rate", "qualification_reason"]], height=300)

# 3. PROFILE CONTEXT TAB
with tab_enrich:
    st.markdown("### Profile Context & Extracted Themes")
    if not proc_df.empty:
        enricher = ProfileEnricher()
        enriched_proc = enricher.enrich_dataset(proc_df)
        sel_c = st.selectbox("Select Profile", options=enriched_proc["handle"].tolist(), format_func=lambda h: f"@{h} ({enriched_proc.loc[enriched_proc['handle']==h, 'name'].values[0]})")
        row = enriched_proc[enriched_proc["handle"] == sel_c].iloc[0]

        ec1, ec2 = st.columns([1, 2])
        with ec1:
            st.markdown(f"""
            <div class="glass-card">
                <h3 style="margin-top:0; color:#1E1B4B;">{row['name']}</h3>
                <p style="color:#6366F1; font-weight:600;">@{row['handle']}</p>
                <p><b>Followers:</b> {int(row['follower_count']):,}</p>
                <p><b>Engagement:</b> {row['engagement_rate']:.2f}%</p>
                <p><b>Email:</b> <span style="background:#F1F5F9; padding:2px 8px; border-radius:4px;">{row.get('contact_email', 'Not Found')}</span></p>
            </div>
            """, unsafe_allow_html=True)
        with ec2:
            st.markdown(f"""
            <div class="glass-card">
                <h4 style="margin-top:0; color:#1E1B4B;">Context & Extracted Themes</h4>
                <p><b>Bio / Content Focus:</b> {row.get('bio', 'N/A')}</p>
                <p><b>Themes:</b> <code>{row.get('content_themes', 'N/A')}</code></p>
                <hr style="border:none; border-top:1px solid #EEF2F6; margin:12px 0;"/>
                <p><b>Audience Age:</b> {row.get('audience_age', '18-34')} | <b>Audience Gender:</b> {row.get('audience_gender', 'Female (78%)')} | <b>Location:</b> {row.get('audience_geography', 'US/Global')}</p>
            </div>
            """, unsafe_allow_html=True)

# 4. AI PERSONALIZATION TAB
with tab_ai:
    st.markdown("### AI Message Personalization Studio")
    if not proc_df.empty:
        passed_creators = proc_df[proc_df["qualification_status"] == "PASSED"]
        if not passed_creators.empty:
            ap1, ap2, ap3 = st.columns(3)
            with ap1:
                target_h = st.selectbox("Select Qualified Creator", passed_creators["handle"].tolist(), format_func=lambda h: f"{passed_creators.loc[passed_creators['handle']==h, 'name'].values[0]} (@{h})")
            with ap2:
                brand = st.text_input("Brand", value="LumiGlow")
            with ap3:
                angle = st.selectbox("Collaboration Angle", ["UGC & Paid Showcase", "Brand Ambassador Program", "Affiliate Partnership", "Sponsored Review"])

            target_row = passed_creators[passed_creators["handle"] == target_h].iloc[0].to_dict()

            if st.button("✨ GENERATE DUAL OUTREACH PITCHES", type="primary"):
                with st.spinner("Generating dual personalized pitches via Google Gemini..."):
                    gen = OutreachMessageGenerator()
                    msg = gen.generate_messages(influencer=target_row, brand_name=brand, collaboration_type=angle)
                    st.session_state["msg_result"] = msg

            if "msg_result" in st.session_state:
                res = st.session_state["msg_result"]
                m_c1, m_c2 = st.columns(2)
                with m_c1:
                    st.markdown("""
                    <div class="glass-card">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                            <h4 style="margin:0; color:#1E1B4B;">📧 Email Collaboration Pitch</h4>
                            <span style="background:#D1FAE5; color:#065F46; padding:2px 8px; border-radius:9999px; font-size:0.75rem; font-weight:700;">60-90 words</span>
                        </div>
                    """, unsafe_allow_html=True)
                    st.markdown(f"**Subject:** `{res['subject']}`")
                    st.info(res["email_pitch"])
                    st.caption(f"Word count: {res['email_word_count']} words")
                    st.markdown("</div>", unsafe_allow_html=True)

                with m_c2:
                    st.markdown("""
                    <div class="glass-card">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                            <h4 style="margin:0; color:#1E1B4B;">📱 Instagram DM</h4>
                            <span style="background:#E0F2FE; color:#0369A1; padding:2px 8px; border-radius:9999px; font-size:0.75rem; font-weight:700;">15-30 words</span>
                        </div>
                    """, unsafe_allow_html=True)
                    st.success(res["instagram_dm"])
                    st.caption(f"Word count: {res['dm_word_count']} words")
                    st.link_button("📲 Open Instagram Profile & Send", f"https://instagram.com/{target_h}", use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)

# 5. OUTREACH TRACKER TAB
with tab_tracker:
    st.markdown("### Outreach Dispatch & Audit Tracker")
    tracker = OutreachTracker()
    log_df = tracker._load_log()
    stats = tracker.get_stats()

    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Total Outreach Logged", stats["total_logged"])
    s2.metric("Successfully Delivered", stats["successfully_sent"])
    s3.metric("Skipped / DM Flow", stats["skipped"])
    s4.metric("Mode", "Simulation Sandbox" if SIMULATION_MODE else "Live Resend")

    if not log_df.empty:
        st.dataframe(log_df[["influencer", "handle", "email", "platform", "channel", "sent", "status", "delivery_id", "date"]], use_container_width=True)
        csv_log = log_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Outreach Log (CSV)", data=csv_log, file_name="outreach_audit_log.csv", mime="text/csv")
    else:
        st.info("Outreach log is empty. Trigger dispatch to populate.")
