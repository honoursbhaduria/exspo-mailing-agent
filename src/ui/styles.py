"""
Design System: Pure Black Text Architecture (#000000) & Light Fresh Pastel Palette.
Strictly adheres to:
1. ALL TEXT IS PURE BLACK (#000000) - ultra crisp, high contrast.
2. ZERO DARK COLORS - light fresh sky-blue (#BAE6FD), ice-cyan (#E8F4FD), pure white (#FFFFFF).
3. Bar Section / Tabs match the exact .nav .container spec (#bef6, rounded, white hover/active pill).
4. Uniform light stat cards and buttons with bold black text.
"""

def get_theme_css() -> str:
    return """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,200..800&family=Dancing+Script:wght@400..700&family=Iosevka+Charon:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700&family=Libre+Caslon+Display&family=Lobster+Two:ital,wght@0,400;0,700;1,400;1,700&display=swap" rel="stylesheet">

<style>
    /* ========================================================================
       1. GLOBAL RESET & TYPOGRAPHY - ALL TEXT IS 100% PURE BLACK (#000000)
       ======================================================================== */
    :root {
        --primary-color: #0284C7 !important;
        --background-color: #F4F7FC !important;
        --secondary-background-color: #FFFFFF !important;
        --text-color: #000000 !important;
    }

    html, body, [class*="css"], [class*="st-"] {
        font-family: 'Bricolage Grotesque', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: #000000 !important;
    }

    /* Monospace / Numerical Font Classes - PURE BLACK */
    .mono-num, .iosevka-charon-regular, code, pre {
        font-family: 'Iosevka Charon', monospace !important;
        font-style: normal;
        color: #000000 !important;
    }

    .iosevka-charon-medium {
        font-family: 'Iosevka Charon', monospace !important;
        font-weight: 500;
        color: #000000 !important;
    }

    .iosevka-charon-bold {
        font-family: 'Iosevka Charon', monospace !important;
        font-weight: 700;
        color: #000000 !important;
    }

    /* Base Canvas - Bright, Fresh, Clean Sky Ambient (NO DARK COLORS) */
    .stApp {
        background-color: #F4F7FC !important;
        background-image: 
            radial-gradient(circle at 12% 10%, rgba(186, 230, 253, 0.45) 0%, transparent 35%),
            radial-gradient(circle at 88% 12%, rgba(224, 231, 255, 0.5) 0%, transparent 35%),
            radial-gradient(circle at 85% 85%, rgba(224, 242, 254, 0.4) 0%, transparent 35%),
            radial-gradient(circle at 15% 88%, rgba(186, 230, 253, 0.45) 0%, transparent 35%) !important;
        background-attachment: fixed !important;
    }

    .block-container {
        padding-top: 1.6rem !important;
        padding-bottom: 3.5rem !important;
        max-width: 1300px !important;
    }

    /* ========================================================================
       2. CRISP PURE WHITE CARDS & PANELS (LIGHT BORDERS, ZERO DARKNESS)
       ======================================================================== */
    .glass-card, .glass-panel {
        background: #FFFFFF !important;
        border: 1.5px solid #E2E8F0 !important;
        border-radius: 20px !important;
        box-shadow: 0 8px 24px -6px rgba(0, 0, 0, 0.04) !important;
        padding: 22px !important;
        color: #000000 !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }
    .glass-card:hover, .glass-panel:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 28px -6px rgba(2, 132, 199, 0.08) !important;
        border-color: #BAE6FD !important;
    }

    /* Streamlit Container Card Override (st.container(border=True)) */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF !important;
        border: 1.5px solid #E2E8F0 !important;
        border-radius: 20px !important;
        box-shadow: 0 8px 24px -6px rgba(0, 0, 0, 0.04) !important;
        padding: 20px 22px !important;
    }

    .glass-card-subtle, .glass-panel-subtle {
        background: #F8FAFC !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        padding: 9px 12px !important;
        color: #000000 !important;
    }

    /* ========================================================================
       3. HERO HEADER & NAVBAR ACTION BUTTON
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
        gap: 10px;
        background: #FFFFFF !important;
        border: 1.5px solid #BAE6FD !important;
        padding: 6px 18px;
        border-radius: 9999px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
        margin-bottom: 12px;
    }

    .icon-conatiner {
        width: 32px;
        height: 32px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background: #FFFFFF;
        border-radius: 8px;
        border: 1px solid #BAE6FD;
        cursor: pointer;
        position: relative;
        transition: transform 0.15s ease;
    }
    .icon-conatiner svg {
        width: 16px;
        height: auto;
    }
    .icon-conatiner svg:last-child {
        position: absolute;
    }
    .icon-conatiner:active {
        animation: press 0.2s 1 linear;
    }
    .icon-conatiner:active svg:last-child {
        animation: bounce 0.2s 1 linear;
    }

    @keyframes press {
        0% { transform: scale(1); }
        50% { transform: scale(0.92); }
        to { transform: scale(1); }
    }
    @keyframes bounce {
        50% { transform: rotate(5deg) translate(4px, -8px); }
        to { transform: scale(0.9) rotate(10deg) translate(8px, -15px); opacity: 0; }
    }

    .brand-name, .brand-title {
        font-family: 'Bricolage Grotesque', sans-serif;
        font-size: 0.95rem;
        font-weight: 800;
        color: #000000 !important;
    }

    .hero-title, .main-heading {
        font-family: 'Bricolage Grotesque', sans-serif;
        font-size: 3.1rem;
        font-weight: 900;
        color: #000000 !important;
        letter-spacing: -1.2px;
        margin: 0;
        line-height: 1.15;
    }

    .hero-sub, .main-subheading {
        font-family: 'Bricolage Grotesque', sans-serif;
        font-size: 1.05rem;
        color: #222222 !important;
        font-weight: 600;
        margin-top: 8px;
        max-width: 680px;
        line-height: 1.5;
    }

    .stat-number {
        font-size: 1.5rem;
        font-weight: 800;
        color: #000000 !important;
        line-height: 1.2;
    }
    .stat-label {
        font-size: 0.78rem;
        font-weight: 700;
        color: #333333 !important;
        margin-top: 2px;
    }

    /* ========================================================================
       4. CENTER CARD STAT TILES - UNIFIED LIGHT PASTEL (PURE BLACK TEXT)
       Fixing:
       65 Total Profiles
       29 Qualified (5k-100k)
       173 Outreach Dispatched
       ======================================================================== */
    .stat-tile-grid, .stat-tile-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        margin-top: 16px;
    }
    
    .stat-tile, .stat-tile-muted, .stat-tile.purple, .stat-tile.blue, .stat-tile.pink {
        background: #F8FAFC !important;
        border: 1.5px solid #BAE6FD !important;
        border-radius: 14px !important;
        padding: 14px 16px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        transition: all 0.2s ease !important;
    }
    .stat-tile:hover, .stat-tile-muted:hover {
        border-color: #0284C7 !important;
        background: #FFFFFF !important;
        box-shadow: 0 4px 14px rgba(2, 132, 199, 0.08) !important;
    }

    .stat-tile-val, .stat-tile .stat-number, .stat-tile-muted .stat-number {
        font-family: 'Iosevka Charon', monospace !important;
        font-size: 1.5rem !important;
        font-weight: 800 !important;
        line-height: 1 !important;
        color: #000000 !important;
    }

    .stat-tile-lbl, .stat-tile .stat-label, .stat-tile-muted .stat-label {
        font-family: 'Bricolage Grotesque', sans-serif !important;
        font-size: 0.78rem !important;
        font-weight: 700 !important;
        color: #222222 !important;
        margin-top: 4px !important;
    }

    /* Status Pills */
    .badge-pill-pass {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: #DCFCE7 !important;
        color: #000000 !important;
        border: 1px solid #86EFAC !important;
        font-size: 0.75rem;
        font-weight: 800;
        padding: 3px 9px;
        border-radius: 9999px;
    }
    .badge-pill-fail {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: #FEE2E2 !important;
        color: #000000 !important;
        border: 1px solid #FCA5A5 !important;
        font-size: 0.75rem;
        font-weight: 800;
        padding: 3px 9px;
        border-radius: 9999px;
    }
    .badge-pill-neutral {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: #F1F5F9 !important;
        color: #000000 !important;
        border: 1px solid #CBD5E1 !important;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 3px 9px;
        border-radius: 9999px;
    }

    /* ========================================================================
       5. BUTTONS - CLEAN FRESH SKY BLUE (#BAE6FD) WITH SOLID BLACK TEXT
       ======================================================================== */
    .stButton > button {
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        min-height: 48px !important;
        border-radius: 12px !important;
        border: 1.5px solid #7DD3FC !important;
        background: #BAE6FD !important;
        color: #000000 !important;
        font-size: 0.92rem !important;
        font-weight: 800 !important;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.12) !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
    }

    .stButton > button:hover {
        background: #93C5FD !important;
        border-color: #38BDF8 !important;
        color: #000000 !important;
        box-shadow: 0 6px 18px rgba(2, 132, 199, 0.2) !important;
        transform: translateY(-1px);
    }

    .stButton > button span,
    .stButton > button p,
    .stButton > button div {
        color: #000000 !important;
        font-size: 0.92rem !important;
        font-weight: 800 !important;
    }

    /* Secondary Button (RESET PARAMETERS) */
    .stButton > button[kind="secondary"] {
        background: #FFFFFF !important;
        border: 1.5px solid #CBD5E1 !important;
        color: #000000 !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03) !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background: #F8FAFC !important;
        border-color: #94A3B8 !important;
        color: #000000 !important;
    }

    /* Download Buttons */
    .stDownloadButton > button {
        background: #FFFFFF !important;
        border: 1.5px solid #BAE6FD !important;
        color: #000000 !important;
        border-radius: 10px !important;
        font-weight: 800 !important;
        transition: all 0.2s ease !important;
    }
    .stDownloadButton > button:hover {
        background: #F0F9FF !important;
        border-color: #7DD3FC !important;
        color: #000000 !important;
    }
    .stDownloadButton > button span,
    .stDownloadButton > button p {
        color: #000000 !important;
        font-weight: 800 !important;
    }

    /* ========================================================================
       6. WORKSPACE TABS - CLEAN MINIMALIST UNDERLINE (NO BOX DIV / NO CONTAINER)
       Just a clean bottom line below the selected section
       ======================================================================== */
    .stTabs [data-baseweb="tab-list"] {
        background: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        padding: 0 !important;
        gap: 28px !important;
        border-bottom: 2px solid #E2E8F0 !important;
        box-shadow: none !important;
        margin-bottom: 20px !important;
        display: flex !important;
        justify-content: flex-start !important;
        width: 100% !important;
    }

    .stTabs [data-baseweb="tab"] {
        font-family: 'Bricolage Grotesque', sans-serif !important;
        background: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        padding: 10px 4px 12px 4px !important;
        margin: 0 !important;
        cursor: pointer !important;
        box-shadow: none !important;
        border-bottom: 3px solid transparent !important;
        margin-bottom: -2px !important;
        transition: all 0.2s ease !important;
    }

    .stTabs [data-baseweb="tab"] p,
    .stTabs [data-baseweb="tab"] span,
    .stTabs [data-baseweb="tab"] div {
        color: #555555 !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        transition: color 0.2s ease !important;
        user-select: none !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: transparent !important;
        border-bottom: 3px solid #CBD5E1 !important;
    }

    .stTabs [data-baseweb="tab"]:hover p,
    .stTabs [data-baseweb="tab"]:hover span {
        color: #000000 !important;
    }

    /* Active Tab: Pure Black Text with solid underline directly below */
    .stTabs [aria-selected="true"] {
        background: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        border-bottom: 3px solid #000000 !important;
        box-shadow: none !important;
        margin-bottom: -2px !important;
    }

    .stTabs [aria-selected="true"] p,
    .stTabs [aria-selected="true"] span,
    .stTabs [aria-selected="true"] div {
        color: #000000 !important;
        font-weight: 900 !important;
        font-size: 0.96rem !important;
    }

    .stTabs [data-baseweb="tab-highlight"],
    .stTabs [data-baseweb="tab-border"] {
        display: none !important;
    }

    /* ========================================================================
       7. SELECTBOX, INPUTS, TABLES & CHROME - ALL TEXT BLACK ONLY
       ======================================================================== */
    div[data-baseweb="popover"],
    div[data-baseweb="menu"],
    ul[data-baseweb="menu"],
    div[role="listbox"] {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 12px !important;
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.08) !important;
    }
    li[data-baseweb="menu-item"],
    div[role="option"] {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        font-family: 'Bricolage Grotesque', sans-serif !important;
        font-size: 0.9rem !important;
        font-weight: 700 !important;
        padding: 9px 14px !important;
    }
    li[data-baseweb="menu-item"]:hover,
    div[role="option"]:hover,
    li[aria-selected="true"],
    div[aria-selected="true"] {
        background-color: #F0F9FF !important;
        color: #000000 !important;
        font-weight: 800 !important;
    }

    div[data-baseweb="select"] {
        background-color: transparent !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 10px !important;
        color: #000000 !important;
        box-shadow: none !important;
        min-height: 42px !important;
    }
    div[data-baseweb="select"] span {
        color: #000000 !important;
        font-weight: 700 !important;
        font-size: 0.88rem !important;
    }
    div[data-baseweb="select"] svg {
        fill: #000000 !important;
    }

    .stTextInput input, .stNumberInput input, .stTextArea textarea {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 10px !important;
        box-shadow: none !important;
        font-weight: 700 !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus {
        border-color: #0284C7 !important;
        box-shadow: 0 0 0 2px rgba(2, 132, 199, 0.2) !important;
    }

    label[data-testid="stWidgetLabel"] p {
        color: #000000 !important;
        font-weight: 800 !important;
        font-size: 0.86rem !important;
    }

    /* Clean Dataframe / Table */
    [data-testid="stDataFrame"] {
        background: #FFFFFF !important;
        border: 1.5px solid #E2E8F0 !important;
        border-radius: 16px !important;
        overflow: hidden !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02) !important;
    }
    [data-testid="stDataFrame"] div {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }

    .stExpander {
        background: #FFFFFF !important;
        border: 1.5px solid #E2E8F0 !important;
        border-radius: 14px !important;
    }
    .stExpander summary span p {
        color: #000000 !important;
        font-weight: 800 !important;
    }

    div[data-testid="stToolbar"] { visibility: hidden; height: 0; }
    header[data-testid="stHeader"] { background: transparent; }
</style>
"""
