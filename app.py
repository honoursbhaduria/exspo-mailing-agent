import streamlit as st
import os
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

# -------------------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------------------
st.set_page_config(
    page_title="EDXSO | Micro-Influencer Outreach System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "landing"

if "selected_niche" not in st.session_state:
    st.session_state["selected_niche"] = DEFAULT_NICHE

if "raw_df" not in st.session_state:
    if RAW_DATA_PATH.exists():
        st.session_state["raw_df"] = pd.read_csv(RAW_DATA_PATH)
    else:
        st.session_state["raw_df"] = None

# Custom CSS for UI styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 50%, #06B6D4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        font-weight: 500;
        margin-bottom: 1.5rem;
    }
    .feature-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 1.3rem;
        border: 1px solid #E5E7EB;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
    }
    .badge-metric {
        display: inline-block;
        background: #EFF6FF;
        color: #1D4ED8;
        padding: 0.2rem 0.6rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        border: 1px solid #BFDBFE;
    }
    .status-pass {
        background-color: #DEF7EC;
        color: #03543F;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
    }
    .status-fail {
        background-color: #FDE8E8;
        color: #9B1C1C;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
    }
    .card-box {
        background: #F9FAFB;
        border: 1px solid #E5E7EB;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

def navigate_to(page_name):
    st.session_state["current_page"] = page_name
    st.rerun()

# -------------------------------------------------------------
# SIDEBAR
# -------------------------------------------------------------
with st.sidebar:
    if os.path.exists(LOGO_PATH):
        st.image(str(LOGO_PATH), width=180)
    else:
        st.title("EDXSO")
    
    st.caption("AI Engineer Intern – Assignment 1")
    st.divider()
    
    nav_selection = st.radio(
        "Navigation",
        options=["🏠 Landing Page & Overview", "🛠️ Outreach Workspace"],
        index=0 if st.session_state["current_page"] == "landing" else 1,
        key="nav_radio"
    )
    
    if nav_selection == "🏠 Landing Page & Overview" and st.session_state["current_page"] != "landing":
        navigate_to("landing")
    elif nav_selection == "🛠️ Outreach Workspace" and st.session_state["current_page"] != "workspace":
        navigate_to("workspace")
        
    st.divider()
    st.subheader("⚙️ Active Filters")
    min_f = st.number_input("Min Followers", min_value=1000, max_value=50000, value=MIN_FOLLOWERS, step=1000)
    max_f = st.number_input("Max Followers", min_value=20000, max_value=500000, value=MAX_FOLLOWERS, step=10000)
    min_eng = st.slider("Min Engagement Rate (%)", min_value=0.5, max_value=8.0, value=MIN_ENGAGEMENT_RATE, step=0.1)
    
    st.divider()
    sim_toggle = st.toggle("Simulation Mode (Safe)", value=SIMULATION_MODE)
    st.caption("When enabled, emails & DMs are safely simulated and logged without outbound traffic.")

# -------------------------------------------------------------
# VIEW 1: LANDING PAGE
# -------------------------------------------------------------
if st.session_state["current_page"] == "landing":
    col1, col2 = st.columns([1, 4])
    with col1:
        if os.path.exists(LOGO_PATH):
            st.image(str(LOGO_PATH), width=170)
    with col2:
        st.markdown('<div class="main-header">Automated Micro-Influencer Outreach System</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-header">EDXSO AI Engineer Intern – Assignment 1 Prototype</div>', unsafe_allow_html=True)

    st.markdown("""
    > **Objective:** Build an end-to-end automated system that discovers relevant micro-influencers, filters and classifies them based on predefined criteria, enriches their profiles with deep context, and generates hyper-personalized collaboration outreach messages via LLM with a multi-channel delivery & tracking layer.
    """)
    
    col_cta1, col_cta2 = st.columns([2, 3])
    with col_cta1:
        if st.button("🚀 Enter Outreach Workspace", type="primary", use_container_width=True):
            navigate_to("workspace")
    with col_cta2:
        st.caption("👈 Click to access the interactive workspace: run discovery, inspect classification, trigger AI personalization, and test outreach dispatch.")

    st.markdown("---")
    
    st.subheader("🏗️ System Architecture & Workflow")
    r1_c1, r1_c2, r1_c3 = st.columns(3)
    with r1_c1:
        st.markdown("""
        <div class="feature-card">
            <h4>1. Discovery Engine</h4>
            <span class="badge-metric">50+ Micro-influencers</span>
            <p style="margin-top: 0.8rem; font-size: 0.95rem; color: #4B5563;">
                Asynchronous crawling with <b>Scrapy</b> across creator marketplaces and social directories. Extracts authentic profiles, handles, follower counts, and public bios.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with r1_c2:
        st.markdown("""
        <div class="feature-card">
            <h4>2. Filtering & Classification</h4>
            <span class="badge-metric">Pass / Fail Logic</span>
            <p style="margin-top: 0.8rem; font-size: 0.95rem; color: #4B5563;">
                Multi-factor classification: Category/niche fit, micro-influencer bounds (5k–100k followers), engagement rate threshold (≥ 2.0%), and brand suitability with explicit rejection reasons.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with r1_c3:
        st.markdown("""
        <div class="feature-card">
            <h4>3. Profile Enrichment</h4>
            <span class="badge-metric">Context & Verified Emails</span>
            <p style="margin-top: 0.8rem; font-size: 0.95rem; color: #4B5563;">
                Extracts content themes, secondary platform handles, and contact emails. Strictly marks unavailable emails as <code>Not Found</code> without hallucination.
            </p>
        </div>
        """, unsafe_allow_html=True)

    r2_c1, r2_c2 = st.columns(2)
    with r2_c1:
        st.markdown("""
        <div class="feature-card">
            <h4>4. AI Personalization Studio</h4>
            <span class="badge-metric">Google Gemini LLM</span>
            <p style="margin-top: 0.8rem; font-size: 0.95rem; color: #4B5563;">
                Generates dual targeted outreach messages dynamically:
                <ul>
                    <li><b>Email Pitch</b> (60–90 words): Personalized hook, value prop, collaboration angle (UGC, affiliate, sponsor).</li>
                    <li><b>Instagram DM</b> (15–30 words): Casual, natural, engaging conversation starter.</li>
                </ul>
            </p>
        </div>
        """, unsafe_allow_html=True)

    with r2_c2:
        st.markdown("""
        <div class="feature-card">
            <h4>5. Sending Layer & Tracking</h4>
            <span class="badge-metric">Resend API + Deduplication</span>
            <p style="margin-top: 0.8rem; font-size: 0.95rem; color: #4B5563;">
                Automated email delivery via <b>Resend</b> with status tracking (Sent, Failed, Skipped). Includes safe simulation mode and Meta-compliant Instagram DM copy & log workflow.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📊 Pipeline Workflow Flowchart")
    st.markdown("""
    ```mermaid
    flowchart LR
        A["Creator Discovery<br/>(Scrapy / 50+ Profiles)"] --> B["Filtering Engine<br/>(5k-100k, ≥2.0% Eng)"]
        B -->|Qualified| C["Enrichment<br/>(Themes, Verified Email)"]
        B -->|Disqualified| D["Rejection Log<br/>(Explicit Reasons)"]
        C --> E["AI Personalization<br/>(Email 60-90w, DM 15-30w)"]
        E --> F["Sending & Tracker<br/>(Resend / Simulation)"]
    ```
    """)
    st.write("")
    if st.button("👉 Proceed to Workspace", type="primary"):
        navigate_to("workspace")

# -------------------------------------------------------------
# VIEW 2: INTERACTIVE WORKSPACE
# -------------------------------------------------------------
elif st.session_state["current_page"] == "workspace":
    c_top1, c_top2 = st.columns([5, 1])
    with c_top1:
        st.title("🛠️ Influencer Outreach Workspace")
        st.caption("End-to-End Pipeline: Discovery → Filtering → Enrichment → AI Personalization → Sending & Tracker")
    with c_top2:
        if st.button("⬅️ Landing Page"):
            navigate_to("landing")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "1. 🔍 Discovery",
        "2. ⚖️ Filtering & Classification",
        "3. 💎 Profile Enrichment",
        "4. ✍️ AI Personalization",
        "5. 📤 Sending & Tracker"
    ])

    # ---------------------------------------------------------
    # TAB 1: DISCOVERY
    # ---------------------------------------------------------
    with tab1:
        st.subheader("1. Micro-Influencer Discovery Engine")
        st.write("Extract authentic micro-influencer profiles (5,000 – 100,000 followers) across creator platforms using Scrapy.")

        col_d1, col_d2, col_d3 = st.columns([2, 2, 2])
        with col_d1:
            niche_input = st.selectbox("Select Target Niche", AVAILABLE_NICHES, index=AVAILABLE_NICHES.index(st.session_state["selected_niche"]))
            st.session_state["selected_niche"] = niche_input
        with col_d2:
            st.write("")
            st.write("")
            if st.button("🕷️ Run Scrapy Spider (Live Crawl)", type="primary"):
                with st.spinner(f"Running Scrapy spider for '{niche_input}'..."):
                    try:
                        df_discovered = run_discovery_cli(niche=niche_input, limit=65)
                        st.session_state["raw_df"] = df_discovered
                        st.success(f"Successfully scraped {len(df_discovered)} influencers!")
                    except Exception as e:
                        st.error(f"Scrapy execution notice: {e}")
        with col_d3:
            st.write("")
            st.write("")
            if st.button("🔄 Refresh Data View"):
                if RAW_DATA_PATH.exists():
                    st.session_state["raw_df"] = pd.read_csv(RAW_DATA_PATH)
                    st.rerun()

        # Display Data
        df = st.session_state.get("raw_df")
        if df is not None and not df.empty:
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Total Discovered", f"{len(df)} creators")
            m2.metric("Target Niche", niche_input)
            m3.metric("Avg Follower Count", f"{int(df['follower_count'].mean()):,}")
            m4.metric("Avg Engagement", f"{df['engagement_rate'].mean():.2f}%")
            
            st.dataframe(
                df[["name", "handle", "platform", "follower_count", "engagement_rate", "niche", "location", "profile_url"]],
                use_container_width=True,
                height=350
            )
        else:
            st.warning("No discovery data found yet. Click 'Run Scrapy Spider' above to discover 50+ creators.")

    # ---------------------------------------------------------
    # TAB 2: FILTERING & CLASSIFICATION
    # ---------------------------------------------------------
    with tab2:
        st.subheader("2. Filtering & Classification Engine")
        st.write("Evaluates every discovered profile against micro-influencer constraints (5k–100k followers, ≥2.0% engagement, and category fit).")

        df = st.session_state.get("raw_df")
        if df is not None and not df.empty:
            classifier = InfluencerClassifier(
                min_followers=min_f,
                max_followers=max_f,
                min_engagement=min_eng,
                target_niche=st.session_state["selected_niche"]
            )
            enricher = ProfileEnricher()
            enriched_temp = enricher.enrich_dataset(df)
            classified_df = classifier.process_dataset(enriched_temp)

            passed_df = classified_df[classified_df["qualification_status"] == "PASSED"]
            failed_df = classified_df[classified_df["qualification_status"] == "FAILED"]

            fc1, fc2, fc3 = st.columns(3)
            fc1.metric("Evaluated Profiles", len(classified_df))
            fc2.metric("✅ Passed Qualification", len(passed_df))
            fc3.metric("❌ Disqualified", len(failed_df))

            subtab1, subtab2 = st.tabs([f"✅ Qualified Influencers ({len(passed_df)})", f"❌ Disqualified Profiles ({len(failed_df)})"])
            
            with subtab1:
                st.write("Influencers that meet all criteria for outreach:")
                st.dataframe(
                    passed_df[["name", "handle", "follower_count", "engagement_rate", "content_themes", "contact_email", "qualification_reason"]],
                    use_container_width=True
                )

            with subtab2:
                st.write("Profiles that failed with exact disqualification reason:")
                st.dataframe(
                    failed_df[["name", "handle", "follower_count", "engagement_rate", "qualification_status", "qualification_reason"]],
                    use_container_width=True
                )
        else:
            st.info("Run discovery in Tab 1 to populate profiles for classification.")

    # ---------------------------------------------------------
    # TAB 3: PROFILE ENRICHMENT
    # ---------------------------------------------------------
    with tab3:
        st.subheader("3. Profile Context & Data Enrichment")
        st.write("Inspect deeply enriched attributes: extracted content themes, verified contact emails, and audience demographics.")

        if PROCESSED_DATA_PATH.exists():
            proc_df = pd.read_csv(PROCESSED_DATA_PATH)
            enricher = ProfileEnricher()
            enriched_df = enricher.enrich_dataset(proc_df)

            col_sel, col_info = st.columns([1, 2])
            with col_sel:
                selected_handle = st.selectbox(
                    "Select Creator to Inspect",
                    options=enriched_df["handle"].tolist(),
                    format_func=lambda h: f"@{h} ({enriched_df.loc[enriched_df['handle']==h, 'name'].values[0]})"
                )
                creator_row = enriched_df[enriched_df["handle"] == selected_handle].iloc[0]

            with col_info:
                st.markdown(f"### {creator_row['name']} (`@{creator_row['handle']}`)")
                
                c_m1, c_m2, c_m3 = st.columns(3)
                c_m1.metric("Followers", f"{int(creator_row['follower_count']):,}")
                c_m2.metric("Engagement Rate", f"{creator_row['engagement_rate']:.2f}%")
                email_val = creator_row.get("contact_email", "Not Found")
                c_m3.metric("Email Status", email_val if email_val != "Not Found" else "Not Found")

                st.markdown(f"**Bio / Content Focus:** {creator_row.get('bio', 'N/A')}")
                st.markdown(f"**Extracted Content Themes:** `{creator_row.get('content_themes', 'N/A')}`")
                
                st.markdown("#### 👥 Audience Demographics")
                d1, d2, d3 = st.columns(3)
                d1.write(f"**Audience Age:** {creator_row.get('audience_age', '18-34')}")
                d2.write(f"**Audience Gender:** {creator_row.get('audience_gender', 'Female (78%)')}")
                d3.write(f"**Audience Geography:** {creator_row.get('audience_geography', 'US / Global')}")

                st.markdown("#### 🔗 Platform Links")
                p1, p2, p3 = st.columns(3)
                p1.link_button("Profile Link", creator_row.get("profile_url", "#"))
                p2.link_button("Instagram", creator_row.get("instagram_url", "#"))
                p3.link_button("TikTok", creator_row.get("tiktok_url", "#"))

    # ---------------------------------------------------------
    # TAB 4: AI PERSONALIZATION
    # ---------------------------------------------------------
    with tab4:
        st.subheader("4. AI Message Personalization Studio")
        st.write("Generate dynamic, hyper-personalized collaboration pitches: **Email (60–90 words)** & **Instagram DM (15–30 words)** via Google Gemini.")

        if PROCESSED_DATA_PATH.exists():
            proc_df = pd.read_csv(PROCESSED_DATA_PATH)
            passed_creators = proc_df[proc_df["qualification_status"] == "PASSED"]

            if not passed_creators.empty:
                col_p1, col_p2, col_p3 = st.columns([1, 1, 1])
                with col_p1:
                    target_creator_handle = st.selectbox(
                        "Choose Qualified Creator",
                        options=passed_creators["handle"].tolist(),
                        format_func=lambda h: f"{passed_creators.loc[passed_creators['handle']==h, 'name'].values[0]} (@{h})"
                    )
                with col_p2:
                    brand_name = st.text_input("Brand Name", value="LumiGlow")
                with col_p3:
                    collab_type = st.selectbox(
                        "Collaboration Angle",
                        options=["UGC & Paid Showcase", "Brand Ambassador Program", "Affiliate Partnership", "Sponsored Review", "Barter Collaboration"]
                    )

                creator_data = passed_creators[passed_creators["handle"] == target_creator_handle].iloc[0].to_dict()

                if st.button("✨ Generate AI Outreach Messages", type="primary"):
                    with st.spinner("Generating dual personalized pitches via Google Gemini..."):
                        generator = OutreachMessageGenerator()
                        msg_res = generator.generate_messages(
                            influencer=creator_data,
                            brand_name=brand_name,
                            collaboration_type=collab_type
                        )
                        st.session_state["last_generated_msg"] = msg_res
                        st.session_state["last_creator_data"] = creator_data

                if "last_generated_msg" in st.session_state:
                    res = st.session_state["last_generated_msg"]
                    
                    st.divider()
                    col_email, col_dm = st.columns(2)
                    
                    with col_email:
                        st.markdown("### 📧 Email Collaboration Pitch")
                        st.markdown(f"**Subject:** `{res.get('subject', 'Partnership Opportunity')}`")
                        st.info(res.get("email_pitch", ""))
                        w_count = res.get("email_word_count", len(res.get("email_pitch", "").split()))
                        st.caption(f"📏 **Word Count:** {w_count} words (Target: 60–90 words) {'✅' if 55 <= w_count <= 95 else '⚠️'}")
                        st.code(res.get("email_pitch", ""), language="markdown")

                    with col_dm:
                        st.markdown("### 📱 Instagram DM")
                        st.markdown(f"**Recipient:** `@{target_creator_handle}`")
                        st.success(res.get("instagram_dm", ""))
                        dm_count = res.get("dm_word_count", len(res.get("instagram_dm", "").split()))
                        st.caption(f"📏 **Word Count:** {dm_count} words (Target: 15–30 words) {'✅' if 12 <= dm_count <= 35 else '⚠️'}")
                        st.code(res.get("instagram_dm", ""), language="markdown")
                        st.link_button("📲 Open Instagram Profile & Send", f"https://instagram.com/{target_creator_handle}")
            else:
                st.warning("No qualified creators found in the dataset. Adjust the filter sliders in the sidebar.")
        else:
            st.info("Run discovery and classification to unlock AI message personalization.")

    # ---------------------------------------------------------
    # TAB 5: SENDING & OUTREACH TRACKER
    # ---------------------------------------------------------
    with tab5:
        st.subheader("5. Sending Layer & Outreach Tracker")
        st.write("Dispatch emails via Resend API (or Safe Simulation Sandbox) and maintain an audit log with deduplication protection.")

        tracker = OutreachTracker()
        stats = tracker.get_stats()

        st_c1, st_c2, st_c3, st_c4 = st.columns(4)
        st_c1.metric("Total Outreach Logged", stats["total_logged"])
        st_c2.metric("Successfully Delivered", stats["successfully_sent"])
        st_c3.metric("Skipped (No Email / DM Flow)", stats["skipped"])
        st_c4.metric("Active Mode", "Simulation" if sim_toggle else "Live Resend")

        col_act1, col_act2 = st.columns([2, 1])
        with col_act1:
            if st.button("🚀 Batch Dispatch to Top Qualified Influencers", type="primary"):
                if PROCESSED_DATA_PATH.exists():
                    proc_df = pd.read_csv(PROCESSED_DATA_PATH)
                    qualified = proc_df[proc_df["qualification_status"] == "PASSED"]
                    
                    with st.spinner("Generating personalized pitches and executing delivery pipeline..."):
                        generator = OutreachMessageGenerator()
                        email_sender = EmailSender(simulation_mode=sim_toggle)
                        ig_sender = InstagramDMSender()
                        
                        count_sent = 0
                        for _, row in qualified.head(10).iterrows():
                            handle = row["handle"]
                            email = row["contact_email"]
                            name = row["name"]
                            
                            if tracker.has_been_contacted(handle) or tracker.has_been_contacted(email):
                                continue

                            msg = generator.generate_messages(row.to_dict())
                            
                            if email != "Not Found":
                                res = email_sender.send_email(email, msg["subject"], msg["email_pitch"], name)
                                status = res["status"]
                                dev_id = res.get("delivery_id")
                                ch = res.get("channel", "Email")
                                sent = status in ["SENT", "SENT (Simulated)"]
                            else:
                                res = ig_sender.send_simulated_dm(handle, msg["instagram_dm"])
                                status = res["status"]
                                dev_id = res.get("delivery_id")
                                ch = "Instagram Direct"
                                sent = True

                            tracker.log_outreach(
                                influencer_name=name,
                                handle=handle,
                                email=email,
                                platform=row["platform"],
                                email_pitch=msg["email_pitch"],
                                instagram_dm=msg["instagram_dm"],
                                channel=ch,
                                sent=sent,
                                status=status,
                                delivery_id=dev_id,
                                notes=row["qualification_reason"]
                            )
                            count_sent += 1

                        st.success(f"Batch outreach completed! {count_sent} records added to log.")
                        st.rerun()

        # Display Outreach Log Table
        tracker_df = tracker._load_log()
        if not tracker_df.empty:
            st.markdown("### 📋 Real-Time Outreach Audit Log")
            st.dataframe(
                tracker_df[["influencer", "handle", "email", "platform", "channel", "sent", "status", "delivery_id", "date"]],
                use_container_width=True
            )

            # Export Button
            csv_data = tracker_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Download Outreach Log (CSV)",
                data=csv_data,
                file_name="edxso_outreach_tracker.csv",
                mime="text/csv"
            )
        else:
            st.info("Outreach log is currently empty. Click 'Batch Dispatch' above to trigger outreach runs.")
