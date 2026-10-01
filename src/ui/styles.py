"""
Design System, Google Fonts, Button Template, Navbar Icons & Single Color Architecture.
Adheres strictly to the user's #03045e color theme, uiverse button hover effects,
single-color stat tiles (no multiple/two-colored items), and icon-free Dashboard card header.
"""

def get_theme_css() -> str:
    return """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,200..800&family=Dancing+Script:wght@400..700&family=Iosevka+Charon:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700&family=Libre+Caslon+Display&family=Lobster+Two:ital,wght@0,400;0,700;1,400;1,700&display=swap" rel="stylesheet">

<style>
    /* ========================================================================
       1. GLOBAL RESET & TYPOGRAPHY (SINGLE UNIFIED COLOR: #03045E)
       ======================================================================== */
    :root {
        --primary-color: #03045e !important;
        --background-color: #F1F4FA !important;
        --secondary-background-color: #FFFFFF !important;
        --text-color: #03045e !important;
    }

    html, body, [class*="css"], [class*="st-"] {
        font-family: 'Bricolage Grotesque', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: #03045e !important;
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

    /* Base Canvas - Crisp Cool-Slate Light Background */
    .stApp {
        background-color: #F1F4FA !important;
        background-image: 
            radial-gradient(circle at 12% 10%, rgba(224, 231, 255, 0.5) 0%, transparent 35%),
            radial-gradient(circle at 88% 12%, rgba(219, 234, 254, 0.5) 0%, transparent 35%),
            radial-gradient(circle at 85% 85%, rgba(238, 242, 255, 0.45) 0%, transparent 35%),
            radial-gradient(circle at 15% 88%, rgba(224, 231, 255, 0.45) 0%, transparent 35%) !important;
        background-attachment: fixed !important;
    }

    /* Container constraints */
    .block-container {
        padding-top: 1.6rem !important;
        padding-bottom: 3.5rem !important;
        max-width: 1300px !important;
    }

    /* ========================================================================
       2. CRISP WHITE CARDS & PANELS
       ======================================================================== */
    .glass-card, .glass-panel {
        background: #FFFFFF !important;
        border: 1px solid #ECEFF8 !important;
        border-radius: 22px !important;
        box-shadow: 0 10px 30px -10px rgba(3, 4, 94, 0.05), 0 2px 6px -1px rgba(0, 0, 0, 0.02) !important;
        padding: 22px !important;
        color: #03045e !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }
    .glass-card:hover, .glass-panel:hover {
        transform: translateY(-2px);
        box-shadow: 0 14px 34px -10px rgba(3, 4, 94, 0.09) !important;
    }

    /* Streamlit Container Card Override (st.container(border=True)) */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF !important;
        border: 1px solid #ECEFF8 !important;
        border-radius: 22px !important;
        box-shadow: 0 10px 30px -10px rgba(3, 4, 94, 0.05) !important;
        padding: 20px 22px !important;
    }

    .glass-card-subtle, .glass-panel-subtle {
        background: #F8FAFC !important;
        border: 1px solid #EEF2F6 !important;
        border-radius: 12px !important;
        padding: 9px 12px !important;
        color: #03045e !important;
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
        border: 1px solid #E2E8F0 !important;
        padding: 6px 18px;
        border-radius: 9999px;
        box-shadow: 0 2px 8px rgba(3, 4, 94, 0.05);
        margin-bottom: 12px;
    }

    /* Navbar Action Button with Press & Bounce Animation */
    .icon-conatiner {
        width: 32px;
        height: 32px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background: #FFFFFF;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
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
        font-weight: 700;
        color: #03045e !important;
    }

    .hero-title, .main-heading {
        font-family: 'Bricolage Grotesque', sans-serif;
        font-size: 3.1rem;
        font-weight: 800;
        color: #03045e !important;
        letter-spacing: -1.2px;
        margin: 0;
        line-height: 1.15;
    }

    .hero-sub, .main-subheading {
        font-family: 'Bricolage Grotesque', sans-serif;
        font-size: 1.05rem;
        color: #5A6282 !important;
        font-weight: 500;
        margin-top: 8px;
        max-width: 680px;
        line-height: 1.5;
    }

    .stat-number {
        font-size: 1.45rem;
        font-weight: 700;
        color: #03045e !important;
        line-height: 1.2;
    }
    .stat-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: #5A6282 !important;
        margin-top: 2px;
    }

    /* ========================================================================
       4. CENTER CARD STAT TILES - UNIFIED SINGLE COLOR (NO MULTIPLE/TWO COLORED)
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
    
    /* ALL THREE TILES FOLLOW EXACT SAME SINGLE COLOR PALETTE */
    .stat-tile, .stat-tile-muted, .stat-tile.purple, .stat-tile.blue, .stat-tile.pink {
        background: #F8FAFC !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 14px !important;
        padding: 14px 16px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        transition: all 0.2s ease !important;
    }
    .stat-tile:hover, .stat-tile-muted:hover {
        border-color: #03045e !important;
        background: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(3, 4, 94, 0.05) !important;
    }

    .stat-tile-val, .stat-tile .stat-number, .stat-tile-muted .stat-number {
        font-family: 'Iosevka Charon', monospace !important;
        font-size: 1.45rem !important;
        font-weight: 700 !important;
        line-height: 1 !important;
        color: #03045e !important;
    }

    .stat-tile-lbl, .stat-tile .stat-label, .stat-tile-muted .stat-label {
        font-family: 'Bricolage Grotesque', sans-serif !important;
        font-size: 0.76rem !important;
        font-weight: 600 !important;
        color: #5A6282 !important;
        margin-top: 4px !important;
    }

    /* Status Pills */
    .badge-pill-pass {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: #EEF2FF !important;
        color: #03045e !important;
        border: 1px solid #CBD5E1 !important;
        font-size: 0.74rem;
        font-weight: 700;
        padding: 3px 9px;
        border-radius: 9999px;
    }
    .badge-pill-fail {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: #F8FAFC !important;
        color: #5A6282 !important;
        border: 1px solid #E2E8F0 !important;
        font-size: 0.74rem;
        font-weight: 700;
        padding: 3px 9px;
        border-radius: 9999px;
    }
    .badge-pill-neutral {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: #F8FAFC !important;
        color: #03045e !important;
        border: 1px solid #E2E8F0 !important;
        font-size: 0.74rem;
        font-weight: 600;
        padding: 3px 9px;
        border-radius: 9999px;
    }

    /* ========================================================================
       5. UIVERSE BUTTON TEMPLATE IMPLEMENTATION (@Ali-Tahmazi99)
       ======================================================================== */
    .stButton > button,
    .stDownloadButton > button {
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        min-height: 48px !important;
        border-radius: 10px !important;
        border: 1.5px solid #03045e !important;
        background: #FFFFFF !important;
        position: relative !important;
        overflow: hidden !important;
        transition: all 0.5s ease-in !important;
        z-index: 1 !important;
        box-shadow: 0 2px 8px rgba(3, 4, 94, 0.05) !important;
        cursor: pointer !important;
    }

    .stButton > button::before,
    .stButton > button::after,
    .stDownloadButton > button::before,
    .stDownloadButton > button::after {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        width: 0 !important;
        height: 100% !important;
        transform: skew(15deg) !important;
        transition: all 0.5s !important;
        overflow: hidden !important;
        z-index: -1 !important;
    }

    .stButton > button::before,
    .stDownloadButton > button::before {
        left: -10px !important;
        background: #240046 !important;
    }

    .stButton > button::after,
    .stDownloadButton > button::after {
        right: -10px !important;
        background: #5a189a !important;
    }

    .stButton > button:hover::before,
    .stButton > button:hover::after,
    .stDownloadButton > button:hover::before,
    .stDownloadButton > button:hover::after {
        width: 58% !important;
    }

    .stButton > button span,
    .stButton > button p,
    .stButton > button div,
    .stDownloadButton > button span,
    .stDownloadButton > button p {
        color: #03045e !important;
        font-size: 0.88rem !important;
        font-weight: 700 !important;
        transition: all 0.3s ease-in !important;
        position: relative !important;
        z-index: 2 !important;
    }

    .stButton > button:hover span,
    .stButton > button:hover p,
    .stButton > button:hover div,
    .stDownloadButton > button:hover span,
    .stDownloadButton > button:hover p {
        color: #e0aaff !important;
        transition: 0.3s !important;
    }

    /* Secondary Button Variant */
    .stButton > button[kind="secondary"] {
        border-color: #03045e !important;
        background: #FFFFFF !important;
    }

    /* ========================================================================
       6. BAR SECTION / TABS (ANIMATED OUTLINE & UNIFIED PALETTE)
       ======================================================================== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px !important;
        background: #FFFFFF !important;
        padding: 6px !important;
        border-radius: 14px !important;
        border: 1.5px solid #03045e !important;
        box-shadow: 0 4px 16px rgba(3, 4, 94, 0.04) !important;
        position: relative !important;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Bricolage Grotesque', sans-serif !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        padding: 8px 18px !important;
        color: #03045e !important;
        background: transparent !important;
        border: none !important;
        transition: all 0.2s ease !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: #F1F4FA !important;
        color: #240046 !important;
    }
    .stTabs [aria-selected="true"] {
        background: #03045e !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(3, 4, 94, 0.2) !important;
    }
    .stTabs [aria-selected="true"] p {
        color: #FFFFFF !important;
    }

    /* ========================================================================
       7. SELECTBOX, INPUTS, TABLES & CHROME
       ======================================================================== */
    div[data-baseweb="popover"],
    div[data-baseweb="menu"],
    ul[data-baseweb="menu"],
    div[role="listbox"] {
        background-color: #FFFFFF !important;
        color: #03045e !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 12px !important;
        box-shadow: 0 12px 32px rgba(3, 4, 94, 0.08) !important;
    }
    li[data-baseweb="menu-item"],
    div[role="option"] {
        background-color: #FFFFFF !important;
        color: #03045e !important;
        font-family: 'Bricolage Grotesque', sans-serif !important;
        font-size: 0.9rem !important;
        padding: 9px 14px !important;
    }
    li[data-baseweb="menu-item"]:hover,
    div[role="option"]:hover,
    li[aria-selected="true"],
    div[aria-selected="true"] {
        background-color: #EEF2FF !important;
        color: #03045e !important;
        font-weight: 600 !important;
    }

    div[data-baseweb="select"] {
        background-color: transparent !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 10px !important;
        color: #03045e !important;
        box-shadow: none !important;
        min-height: 42px !important;
    }
    div[data-baseweb="select"] span {
        color: #03045e !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
    }
    div[data-baseweb="select"] svg {
        fill: #03045e !important;
    }

    .stTextInput input, .stNumberInput input, .stTextArea textarea {
        background-color: #FFFFFF !important;
        color: #03045e !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 10px !important;
        box-shadow: none !important;
        font-weight: 500 !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus {
        border-color: #03045e !important;
        box-shadow: 0 0 0 2px rgba(3, 4, 94, 0.15) !important;
    }

    label[data-testid="stWidgetLabel"] p {
        color: #03045e !important;
        font-weight: 600 !important;
        font-size: 0.84rem !important;
    }

    [data-testid="stDataFrame"] {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 16px !important;
        overflow: hidden !important;
        box-shadow: 0 2px 8px rgba(3, 4, 94, 0.02) !important;
    }
    [data-testid="stDataFrame"] div {
        background-color: #FFFFFF !important;
        color: #03045e !important;
    }

    .stExpander {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 14px !important;
    }

    div[data-testid="stToolbar"] { visibility: hidden; height: 0; }
    header[data-testid="stHeader"] { background: transparent; }
</style>
"""
