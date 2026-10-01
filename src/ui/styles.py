"""
Design System, Fonts, Glassmorphism, and Component Styles.
Adheres strictly to:
- Google Fonts: Bricolage Grotesque, Iosevka Charon, Libre Caslon Display
- True glassmorphism (frosted backdrop-filter, subtle borders)
- NO black colors, NO popping/neon colors, NO dark bleed-through in dropdowns/tables/buttons
- NO harsh shadows (clean border-driven depth)
- NO emojis
"""

def get_theme_css() -> str:
    return """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,200..800&family=Dancing+Script:wght@400..700&family=Iosevka+Charon:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700&family=Libre+Caslon+Display&family=Lobster+Two:ital,wght@0,400;0,700;1,400;1,700&display=swap" rel="stylesheet">

<style>
    /* Global Typography & Light Theme Enforcement */
    html, body, [class*="css"], [class*="st-"] {
        font-family: 'Bricolage Grotesque', -apple-system, sans-serif !important;
        color: #2D3142 !important;
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

    .libre-caslon-display-regular {
        font-family: 'Libre Caslon Display', serif !important;
        font-weight: 400;
    }

    /* Base Canvas - Soft Muted Neutral with Gentle Diffusion (NO DARKNESS) */
    .stApp {
        background-color: #F5F6FA !important;
        background-image: 
            radial-gradient(circle at 10% 12%, rgba(220, 224, 240, 0.55) 0%, transparent 35%),
            radial-gradient(circle at 90% 15%, rgba(215, 230, 240, 0.55) 0%, transparent 35%),
            radial-gradient(circle at 85% 85%, rgba(230, 225, 240, 0.45) 0%, transparent 35%),
            radial-gradient(circle at 15% 85%, rgba(225, 235, 240, 0.45) 0%, transparent 35%) !important;
        background-attachment: fixed !important;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        max-width: 1280px !important;
    }

    /* Glassmorphism Surface Container - Crisp White Frosted Glass */
    .glass-panel {
        background: rgba(255, 255, 255, 0.82) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(222, 227, 238, 0.95) !important;
        border-radius: 18px !important;
        box-shadow: 0 1px 3px rgba(45, 49, 66, 0.02) !important;
        padding: 22px !important;
        color: #2D3142 !important;
    }

    .glass-panel-subtle {
        background: rgba(248, 249, 252, 0.85) !important;
        backdrop-filter: blur(14px) !important;
        -webkit-backdrop-filter: blur(14px) !important;
        border: 1px solid rgba(226, 230, 240, 0.9) !important;
        border-radius: 12px !important;
        padding: 12px 14px !important;
        color: #2D3142 !important;
    }

    /* Header & Branding */
    .app-header {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        padding-top: 0.5rem;
        padding-bottom: 1.8rem;
    }

    .brand-capsule {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(255, 255, 255, 0.92);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(215, 220, 235, 0.9);
        padding: 6px 16px;
        border-radius: 9999px;
        margin-bottom: 12px;
    }

    .capsule-dot {
        width: 16px;
        height: 16px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 2px;
    }
    .capsule-dot-top {
        width: 10px;
        height: 6px;
        background: #5B638A;
        border-radius: 4px 4px 0 0;
    }
    .capsule-dot-bottom {
        width: 10px;
        height: 6px;
        background: #6C8CA5;
        border-radius: 0 0 4px 4px;
    }

    .brand-title {
        font-family: 'Bricolage Grotesque', sans-serif;
        font-size: 0.95rem;
        font-weight: 700;
        color: #2D3142;
        letter-spacing: -0.2px;
    }

    .main-heading {
        font-family: 'Bricolage Grotesque', sans-serif;
        font-size: 2.8rem;
        font-weight: 800;
        color: #242738;
        letter-spacing: -1px;
        margin: 0;
        line-height: 1.15;
    }

    .main-subheading {
        font-family: 'Bricolage Grotesque', sans-serif;
        font-size: 1.05rem;
        color: #5A5F75;
        font-weight: 400;
        margin-top: 8px;
        max-width: 620px;
        line-height: 1.5;
    }

    /* Clean Status Badges */
    .badge-pill-pass {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: #EBF4EE;
        color: #315844;
        font-size: 0.74rem;
        font-weight: 600;
        padding: 3px 9px;
        border-radius: 9999px;
        border: 1px solid rgba(63, 110, 86, 0.25);
    }

    .badge-pill-fail {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: #F9EBEC;
        color: #7D383D;
        font-size: 0.74rem;
        font-weight: 600;
        padding: 3px 9px;
        border-radius: 9999px;
        border: 1px solid rgba(147, 69, 75, 0.25);
    }

    .badge-pill-neutral {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: #EFF2F7;
        color: #484D63;
        font-size: 0.74rem;
        font-weight: 600;
        padding: 3px 9px;
        border-radius: 9999px;
        border: 1px solid rgba(100, 116, 139, 0.2);
    }

    /* Muted Pastel Stat Cards */
    .stat-tile-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        margin-top: 14px;
    }

    .stat-tile-muted {
        border-radius: 12px;
        padding: 12px 14px;
        background: rgba(255, 255, 255, 0.85);
        border: 1px solid rgba(220, 225, 238, 0.9);
    }
    .stat-tile-muted.lavender {
        background: #EFF1F8;
        border-color: #DFE2EE;
    }
    .stat-tile-muted.slate {
        background: #EDF3F7;
        border-color: #DCE5EC;
    }
    .stat-tile-muted.sage {
        background: #EFF5F1;
        border-color: #DEEAE1;
    }

    .stat-number {
        font-family: 'Iosevka Charon', monospace;
        font-size: 1.35rem;
        font-weight: 700;
        color: #2D3142;
        line-height: 1;
    }
    .stat-label {
        font-family: 'Bricolage Grotesque', sans-serif;
        font-size: 0.72rem;
        font-weight: 500;
        color: #646A80;
        margin-top: 5px;
    }

    /* ========================================================================
       ELIMINATING ALL UI DARKNESS: DROPDOWNS, BUTTONS, TABLES, AND INPUTS
       ======================================================================== */

    /* 1. BaseWeb Dropdowns & Popovers - Pure Crisp Light Frosted Menu */
    div[data-baseweb="popover"],
    div[data-baseweb="menu"],
    ul[data-baseweb="menu"],
    div[role="listbox"] {
        background-color: #FFFFFF !important;
        color: #2D3142 !important;
        border: 1px solid #DEE3EE !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 16px rgba(45, 49, 66, 0.06) !important;
    }
    li[data-baseweb="menu-item"],
    div[role="option"] {
        background-color: #FFFFFF !important;
        color: #2D3142 !important;
        font-family: 'Bricolage Grotesque', sans-serif !important;
        font-size: 0.9rem !important;
    }
    li[data-baseweb="menu-item"]:hover,
    div[role="option"]:hover,
    li[aria-selected="true"],
    div[aria-selected="true"] {
        background-color: #F1F4F9 !important;
        color: #1E2235 !important;
    }

    /* Selectbox Input Box */
    div[data-baseweb="select"] {
        background-color: transparent !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 1px solid #DCE1EC !important;
        border-radius: 10px !important;
        color: #2D3142 !important;
        box-shadow: none !important;
    }
    div[data-baseweb="select"] span {
        color: #2D3142 !important;
        font-weight: 500 !important;
    }
    div[data-baseweb="select"] svg {
        fill: #5A5F75 !important;
    }

    /* 2. Text Inputs & Number Inputs */
    .stTextInput input, .stNumberInput input {
        background-color: #FFFFFF !important;
        color: #2D3142 !important;
        border: 1px solid #DCE1EC !important;
        border-radius: 10px !important;
        box-shadow: none !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #5B638A !important;
        box-shadow: none !important;
    }

    /* Labels */
    label[data-testid="stWidgetLabel"] p {
        color: #484D63 !important;
        font-weight: 600 !important;
        font-size: 0.84rem !important;
    }

    /* 3. Buttons - Refined Slate & Frosted White, NO PURE BLACK */
    .stButton > button {
        font-family: 'Bricolage Grotesque', sans-serif !important;
        background: #5B638A !important;
        color: #FFFFFF !important;
        border: 1px solid #4F5679 !important;
        border-radius: 10px !important;
        padding: 9px 18px !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        box-shadow: none !important;
        transition: background 0.15s ease !important;
    }
    .stButton > button:hover {
        background: #4E5370 !important;
        border-color: #444962 !important;
        color: #FFFFFF !important;
    }

    /* Secondary Download Buttons */
    .stDownloadButton > button {
        font-family: 'Bricolage Grotesque', sans-serif !important;
        background: #FFFFFF !important;
        color: #2D3142 !important;
        border: 1px solid #DCE1EC !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        box-shadow: none !important;
    }
    .stDownloadButton > button:hover {
        background: #F1F4F9 !important;
        border-color: #CBD5E1 !important;
        color: #1E2235 !important;
    }

    /* 4. Dataframe & Tables - Light Theme, Clear Rows, No Dark Cells */
    [data-testid="stDataFrame"] {
        background: #FFFFFF !important;
        border: 1px solid #DEE3EE !important;
        border-radius: 14px !important;
        overflow: hidden !important;
    }
    [data-testid="stDataFrame"] div {
        background-color: transparent !important;
    }

    /* 5. Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px !important;
        background: rgba(255, 255, 255, 0.85) !important;
        backdrop-filter: blur(14px) !important;
        padding: 5px !important;
        border-radius: 14px !important;
        border: 1px solid rgba(222, 227, 238, 0.95) !important;
        box-shadow: none !important;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Bricolage Grotesque', sans-serif !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        padding: 7px 16px !important;
        color: #5A5F75 !important;
        background: transparent !important;
        border: none !important;
    }
    .stTabs [aria-selected="true"] {
        background: #5B638A !important;
        color: #FFFFFF !important;
    }

    /* 6. Slider */
    div[data-testid="stSlider"] div[role="slider"] {
        background-color: #5B638A !important;
    }

    /* Streamlit Chrome cleanup */
    div[data-testid="stToolbar"] { visibility: hidden; height: 0; }
    header[data-testid="stHeader"] { background: transparent; }
</style>
"""
