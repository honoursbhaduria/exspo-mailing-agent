"""
Design System, Google Fonts, Glassmorphism, and Light Theme Component Styles.
Eliminates all darkness, ensures crisp white cards matching image.png,
bright blue primary buttons (#2563EB), pure white dropdown menus,
clean white data tables, and exact typography.
"""

def get_theme_css() -> str:
    return """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,200..800&family=Dancing+Script:wght@400..700&family=Iosevka+Charon:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700&family=Libre+Caslon+Display&family=Lobster+Two:ital,wght@0,400;0,700;1,400;1,700&display=swap" rel="stylesheet">

<style>
    /* ========================================================================
       1. GLOBAL RESET & TYPOGRAPHY (PURE LIGHT MODE, ZERO DARKNESS)
       ======================================================================== */
    :root {
        --primary-color: #2563EB !important;
        --background-color: #F1F4FA !important;
        --secondary-background-color: #FFFFFF !important;
        --text-color: #1E293B !important;
    }

    html, body, [class*="css"], [class*="st-"] {
        font-family: 'Bricolage Grotesque', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: #1E293B !important;
    }

    /* Monospace / Numerical Font Classes */
    .mono-num, .iosevka-charon-regular, code, pre {
        font-family: 'Iosevka Charon', monospace !important;
        font-style: normal;
    }

    .iosevka-charon-medium {
        font-family: 'Iosevka Charon', monospace !important;
        font-weight: 500;
    }

    .iosevka-charon-bold {
        font-family: 'Iosevka Charon', monospace !important;
        font-weight: 700;
    }

    /* Base Canvas - Crisp Cool-Slate Light Background (EXACT MATCH FOR IMAGE.PNG) */
    .stApp {
        background-color: #F1F4FA !important;
        background-image: 
            radial-gradient(circle at 12% 10%, rgba(219, 234, 254, 0.7) 0%, transparent 35%),
            radial-gradient(circle at 88% 12%, rgba(224, 231, 255, 0.75) 0%, transparent 35%),
            radial-gradient(circle at 85% 85%, rgba(245, 235, 255, 0.6) 0%, transparent 35%),
            radial-gradient(circle at 15% 88%, rgba(219, 234, 254, 0.65) 0%, transparent 35%) !important;
        background-attachment: fixed !important;
    }

    /* Container constraints */
    .block-container {
        padding-top: 1.6rem !important;
        padding-bottom: 3.5rem !important;
        max-width: 1300px !important;
    }

    /* ========================================================================
       2. CRISP WHITE CARDS & PANELS (MATCHING IMAGE.PNG)
       ======================================================================== */
    .glass-card, .glass-panel {
        background: #FFFFFF !important;
        border: 1px solid #ECEFF8 !important;
        border-radius: 22px !important;
        box-shadow: 0 10px 30px -10px rgba(99, 102, 241, 0.07), 0 2px 6px -1px rgba(0, 0, 0, 0.02) !important;
        padding: 22px !important;
        color: #1E293B !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }
    .glass-card:hover, .glass-panel:hover {
        transform: translateY(-2px);
        box-shadow: 0 14px 34px -10px rgba(99, 102, 241, 0.12) !important;
    }

    /* Streamlit Container Card Override (st.container(border=True)) */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF !important;
        border: 1px solid #ECEFF8 !important;
        border-radius: 22px !important;
        box-shadow: 0 10px 30px -10px rgba(99, 102, 241, 0.07) !important;
        padding: 20px 22px !important;
    }

    .glass-card-subtle, .glass-panel-subtle {
        background: #F8FAFC !important;
        border: 1px solid #EEF2F6 !important;
        border-radius: 12px !important;
        padding: 9px 12px !important;
        color: #1E293B !important;
    }

    /* ========================================================================
       3. HERO HEADER (EXACT REPLICA OF IMAGE.PNG GOSCRAPING HEADER)
       ======================================================================== */
    .hero-wrapper, .app-header {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        padding-bottom: 1.8rem;
    }

    .brand-pill, .brand-capsule {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        padding: 5px 16px;
        border-radius: 9999px;
        box-shadow: 0 2px 8px rgba(99, 102, 241, 0.05);
        margin-bottom: 12px;
    }

    .dual-dot, .capsule-dot {
        width: 14px;
        height: 14px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 2px;
    }
    .dual-dot-top, .capsule-dot-top {
        width: 10px;
        height: 5px;
        background: #6366F1;
        border-radius: 4px 4px 0 0;
    }
    .dual-dot-bottom, .capsule-dot-bottom {
        width: 10px;
        height: 5px;
        background: #38BDF8;
        border-radius: 0 0 4px 4px;
    }

    .brand-name, .brand-title {
        font-family: 'Bricolage Grotesque', sans-serif;
        font-size: 0.95rem;
        font-weight: 700;
        color: #1E1B4B !important;
    }

    .hero-title, .main-heading {
        font-family: 'Bricolage Grotesque', sans-serif;
        font-size: 3.1rem;
        font-weight: 800;
        color: #1E1B4B !important;
        letter-spacing: -1.2px;
        margin: 0;
        line-height: 1.15;
    }

    .hero-sub, .main-subheading {
        font-family: 'Bricolage Grotesque', sans-serif;
        font-size: 1.05rem;
        color: #64748B !important;
        font-weight: 500;
        margin-top: 8px;
        max-width: 680px;
        line-height: 1.5;
    }

    /* Metric Numbers and Labels */
    .stat-number {
        font-size: 1.45rem;
        font-weight: 700;
        color: #1E293B !important;
        line-height: 1.2;
    }
    .stat-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: #64748B !important;
        margin-top: 2px;
    }

    /* ========================================================================
       4. CENTER CARD PASTEL STAT TILES (LAVENDER, SKY BLUE, SOFT PINK)
       ======================================================================== */
    .stat-tile-grid, .stat-tile-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        margin-top: 16px;
    }
    .stat-tile, .stat-tile-muted {
        border-radius: 14px;
        padding: 14px 16px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .stat-tile.purple, .stat-tile-muted.lavender {
        background: #EEF2FF !important;
        border: 1px solid #C7D2FE !important;
    }
    .stat-tile.blue, .stat-tile-muted.slate, .stat-tile-muted.blue {
        background: #E0F2FE !important;
        border: 1px solid #BAE6FD !important;
    }
    .stat-tile.pink, .stat-tile-muted.sage, .stat-tile-muted.pink {
        background: #FCE7F3 !important;
        border: 1px solid #FBCFE8 !important;
    }

    .stat-tile-val {
        font-family: 'Iosevka Charon', monospace;
        font-size: 1.45rem;
        font-weight: 700;
        line-height: 1;
    }
    .stat-tile.purple .stat-tile-val, .stat-tile-muted.lavender .stat-number { color: #4338CA !important; }
    .stat-tile.blue .stat-tile-val, .stat-tile-muted.slate .stat-number { color: #0284C7 !important; }
    .stat-tile.pink .stat-tile-val, .stat-tile-muted.sage .stat-number { color: #BE185D !important; }

    .stat-tile-lbl {
        font-family: 'Bricolage Grotesque', sans-serif;
        font-size: 0.75rem;
        font-weight: 600;
        color: #64748B !important;
        margin-top: 4px;
    }

    /* Status Pills */
    .badge-pill-pass {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: #D1FAE5 !important;
        color: #065F46 !important;
        font-size: 0.74rem;
        font-weight: 700;
        padding: 3px 9px;
        border-radius: 9999px;
    }
    .badge-pill-fail {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: #FEE2E2 !important;
        color: #991B1B !important;
        font-size: 0.74rem;
        font-weight: 700;
        padding: 3px 9px;
        border-radius: 9999px;
    }
    .badge-pill-neutral {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: #F1F5F9 !important;
        color: #475569 !important;
        font-size: 0.74rem;
        font-weight: 600;
        padding: 3px 9px;
        border-radius: 9999px;
    }

    /* ========================================================================
       5. FIXING ALL DARKNESS IN DROPDOWNS, BUTTONS, TABLES & TABS
       ======================================================================== */

    /* BASEWEB DROPDOWNS - PURE WHITE POPUP MENU */
    div[data-baseweb="popover"],
    div[data-baseweb="menu"],
    ul[data-baseweb="menu"],
    div[role="listbox"] {
        background-color: #FFFFFF !important;
        color: #1E293B !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 12px !important;
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.08) !important;
    }
    li[data-baseweb="menu-item"],
    div[role="option"] {
        background-color: #FFFFFF !important;
        color: #1E293B !important;
        font-family: 'Bricolage Grotesque', sans-serif !important;
        font-size: 0.9rem !important;
        padding: 9px 14px !important;
    }
    li[data-baseweb="menu-item"]:hover,
    div[role="option"]:hover,
    li[aria-selected="true"],
    div[aria-selected="true"] {
        background-color: #EFF6FF !important;
        color: #2563EB !important;
        font-weight: 600 !important;
    }

    /* SELECTBOX CONTROL CONTAINER - PURE WHITE */
    div[data-baseweb="select"] {
        background-color: transparent !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 10px !important;
        color: #1E293B !important;
        box-shadow: none !important;
        min-height: 42px !important;
    }
    div[data-baseweb="select"] span {
        color: #1E293B !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
    }
    div[data-baseweb="select"] svg {
        fill: #64748B !important;
    }

    /* INPUTS & TEXT BOXES */
    .stTextInput input, .stNumberInput input, .stTextArea textarea {
        background-color: #FFFFFF !important;
        color: #1E293B !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 10px !important;
        box-shadow: none !important;
        font-weight: 500 !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.15) !important;
    }

    /* LABELS */
    label[data-testid="stWidgetLabel"] p {
        color: #475569 !important;
        font-weight: 600 !important;
        font-size: 0.84rem !important;
    }

    /* BUTTONS - BRIGHT CLEAN BLUE PRIMARY (#2563EB), PURE WHITE SECONDARY */
    .stButton > button {
        font-family: 'Bricolage Grotesque', sans-serif !important;
        background: #2563EB !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 22px !important;
        font-weight: 700 !important;
        font-size: 0.88rem !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.28) !important;
        transition: all 0.15s ease !important;
    }
    .stButton > button:hover {
        background: #1D4ED8 !important;
        box-shadow: 0 6px 18px rgba(37, 99, 235, 0.38) !important;
        color: #FFFFFF !important;
    }

    /* SECONDARY BUTTONS (RESET, ETC.) */
    .stButton > button[kind="secondary"] {
        background: #FFFFFF !important;
        color: #475569 !important;
        border: 1px solid #CBD5E1 !important;
        box-shadow: none !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background: #F8FAFC !important;
        border-color: #94A3B8 !important;
        color: #1E293B !important;
    }

    /* DOWNLOAD BUTTONS */
    .stDownloadButton > button {
        font-family: 'Bricolage Grotesque', sans-serif !important;
        background: #FFFFFF !important;
        color: #2563EB !important;
        border: 1px solid #BFDBFE !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        box-shadow: none !important;
    }
    .stDownloadButton > button:hover {
        background: #EFF6FF !important;
        color: #1D4ED8 !important;
    }

    /* TABS - CRISP WHITE BAR, VIBRANT BLUE ACTIVE PILL */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px !important;
        background: #FFFFFF !important;
        padding: 6px !important;
        border-radius: 14px !important;
        border: 1px solid #E2E8F0 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02) !important;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Bricolage Grotesque', sans-serif !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        padding: 8px 18px !important;
        color: #64748B !important;
        background: transparent !important;
        border: none !important;
    }
    .stTabs [aria-selected="true"] {
        background: #2563EB !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25) !important;
    }

    /* TABLES / DATAFRAMES - PURE WHITE LIGHT THEME, CLEAN CRISP CELLS */
    [data-testid="stDataFrame"] {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 16px !important;
        overflow: hidden !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02) !important;
    }
    [data-testid="stDataFrame"] div {
        background-color: #FFFFFF !important;
        color: #1E293B !important;
    }

    /* EXPANDER */
    .stExpander {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 14px !important;
    }

    /* Streamlit Chrome cleanup */
    div[data-testid="stToolbar"] { visibility: hidden; height: 0; }
    header[data-testid="stHeader"] { background: transparent; }
</style>
"""
