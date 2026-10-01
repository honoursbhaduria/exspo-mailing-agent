"""
Design System, Fonts, Glassmorphism, and Component Styles.
Adheres strictly to:
- Google Fonts: Bricolage Grotesque, Iosevka Charon, Libre Caslon Display
- True glassmorphism (frosted backdrop-filter, subtle borders)
- NO black colors, NO popping/neon colors, NO harsh gradients
- NO harsh shadows (clean border-driven depth)
- NO emojis
"""

def get_theme_css() -> str:
    return """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,200..800&family=Dancing+Script:wght@400..700&family=Iosevka+Charon:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700&family=Libre+Caslon+Display&family=Lobster+Two:ital,wght@0,400;0,700;1,400;1,700&display=swap" rel="stylesheet">

<style>
    /* Reset & Typography */
    html, body, [class*="css"], [class*="st-"] {
        font-family: 'Bricolage Grotesque', -apple-system, sans-serif !important;
        color: #2D3142;
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

    /* Base Canvas - Soft Muted Neutral with Gentle Diffusion */
    .stApp {
        background-color: #F4F5F9;
        background-image: 
            radial-gradient(circle at 10% 12%, rgba(220, 224, 240, 0.6) 0%, transparent 30%),
            radial-gradient(circle at 90% 15%, rgba(215, 230, 240, 0.6) 0%, transparent 30%),
            radial-gradient(circle at 85% 85%, rgba(230, 225, 240, 0.5) 0%, transparent 35%),
            radial-gradient(circle at 15% 85%, rgba(225, 235, 240, 0.5) 0%, transparent 35%);
        background-attachment: fixed;
    }

    /* Glassmorphism Surface Container */
    .glass-panel {
        background: rgba(255, 255, 255, 0.78);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(222, 227, 238, 0.85);
        border-radius: 18px;
        box-shadow: 0 1px 3px rgba(45, 49, 66, 0.03);
        padding: 22px;
        transition: border-color 0.2s ease;
    }

    .glass-panel-subtle {
        background: rgba(248, 249, 252, 0.7);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(226, 230, 240, 0.8);
        border-radius: 14px;
        padding: 14px 16px;
    }

    /* Header & Branding */
    .app-header {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        padding-top: 1.2rem;
        padding-bottom: 2rem;
    }

    .brand-capsule {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(215, 220, 235, 0.8);
        padding: 6px 16px;
        border-radius: 9999px;
        margin-bottom: 12px;
        box-shadow: 0 1px 2px rgba(45, 49, 66, 0.03);
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
        background: rgba(255, 255, 255, 0.7);
        border: 1px solid rgba(220, 225, 238, 0.8);
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

    /* Clean Streamlit Overrides */
    div[data-testid="stToolbar"] { visibility: hidden; height: 0; }
    header[data-testid="stHeader"] { background: transparent; }

    /* Buttons: Flat, Clean, Muted Tone */
    .stButton>button {
        font-family: 'Bricolage Grotesque', sans-serif !important;
        background: #4E5370 !important;
        color: #FFFFFF !important;
        border: 1px solid #444962 !important;
        border-radius: 10px !important;
        padding: 8px 18px !important;
        font-weight: 600 !important;
        box-shadow: none !important;
        transition: background 0.15s ease !important;
    }
    .stButton>button:hover {
        background: #3F445D !important;
        border-color: #383C52 !important;
    }

    /* Tabs Override */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: rgba(255, 255, 255, 0.75);
        backdrop-filter: blur(14px);
        padding: 5px;
        border-radius: 14px;
        border: 1px solid rgba(222, 227, 238, 0.85);
        box-shadow: none;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Bricolage Grotesque', sans-serif !important;
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.88rem;
        padding: 7px 16px;
        color: #646A80;
        background: transparent;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        background: #4E5370 !important;
        color: #FFFFFF !important;
    }

    /* Inputs & Selects */
    .stSelectbox>div>div, .stTextInput>div>div {
        background: rgba(255, 255, 255, 0.85) !important;
        border: 1px solid #DCE1EC !important;
        border-radius: 10px !important;
        box-shadow: none !important;
        font-family: 'Bricolage Grotesque', sans-serif !important;
    }
    .stSelectbox>div>div:focus-within, .stTextInput>div>div:focus-within {
        border-color: #5B638A !important;
    }

    /* Dataframe view */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(222, 227, 238, 0.85);
    }
</style>
"""
