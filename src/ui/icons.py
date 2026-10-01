"""
HugeIcons SVG Icons Component
Clean, modern, minimalist 1.5px stroke geometry. No emojis.
"""

def icon(name: str, size: int = 18, color: str = "currentColor", stroke_width: float = 1.5) -> str:
    """Returns clean inline SVG for the requested HugeIcon."""
    icons_svg = {
        "search": f"""
            <circle cx="11" cy="11" r="7" stroke="{color}" stroke-width="{stroke_width}"/>
            <path d="M20 20L16.5 16.5" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round"/>
        """,
        "filter": f"""
            <path d="M4 6H20M7 12H17M10 18H14" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round"/>
        """,
        "sliders": f"""
            <path d="M4 8H12M16 8H20M14 6V10M4 16H8M12 16H20M10 14V18" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round"/>
        """,
        "mail": f"""
            <rect x="3" y="5" width="18" height="14" rx="3" stroke="{color}" stroke-width="{stroke_width}"/>
            <path d="M3 7.5L10.8 12.7C11.5 13.1 12.5 13.1 13.2 12.7L21 7.5" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round"/>
        """,
        "user": f"""
            <circle cx="12" cy="7" r="4" stroke="{color}" stroke-width="{stroke_width}"/>
            <path d="M4 20C4 16.6863 7.58172 14 12 14C16.4183 14 20 16.6863 20 20" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round"/>
        """,
        "check_circle": f"""
            <circle cx="12" cy="12" r="9" stroke="{color}" stroke-width="{stroke_width}"/>
            <path d="M8.5 12.5L11 15L15.5 9.5" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"/>
        """,
        "cross_circle": f"""
            <circle cx="12" cy="12" r="9" stroke="{color}" stroke-width="{stroke_width}"/>
            <path d="M9.5 9.5L14.5 14.5M14.5 9.5L9.5 14.5" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round"/>
        """,
        "sparkle": f"""
            <path d="M12 3V21M3 12H21M6.5 6.5L17.5 17.5M6.5 17.5L17.5 6.5" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round"/>
        """,
        "layers": f"""
            <path d="M4 7L12 3L20 7L12 11L4 7Z" stroke="{color}" stroke-width="{stroke_width}" stroke-linejoin="round"/>
            <path d="M4 12L12 16L20 12" stroke="{color}" stroke-width="{stroke_width}" stroke-linejoin="round"/>
            <path d="M4 17L12 21L20 17" stroke="{color}" stroke-width="{stroke_width}" stroke-linejoin="round"/>
        """,
        "globe": f"""
            <circle cx="12" cy="12" r="9" stroke="{color}" stroke-width="{stroke_width}"/>
            <path d="M3 12H21M12 3C14.5 6 15.5 9 15.5 12C15.5 15 14.5 18 12 21C9.5 18 8.5 15 8.5 12C8.5 9 9.5 6 12 3Z" stroke="{color}" stroke-width="{stroke_width}"/>
        """,
        "activity": f"""
            <path d="M3 12H6L9 4L15 20L18 12H21" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"/>
        """,
        "send": f"""
            <path d="M21 3L10 14M21 3L14.5 21L10 14M21 3L3 9.5L10 14" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"/>
        """,
        "download": f"""
            <path d="M12 4V16M12 16L7 11M12 16L17 11M4 20H20" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"/>
        """,
        "refresh": f"""
            <path d="M4 12A8 8 0 0 1 18.5 6.5L20 5M20 5V10M20 5H15M20 12A8 8 0 0 1 5.5 17.5L4 19M4 19V14M4 19H9" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"/>
        """,
        "copy": f"""
            <rect x="8" y="8" width="12" height="12" rx="2" stroke="{color}" stroke-width="{stroke_width}"/>
            <path d="M16 8V6C16 4.89543 15.1046 4 14 4H6C4.89543 4 4 4.89543 4 6V14C4 15.1046 4.89543 16 6 16H8" stroke="{color}" stroke-width="{stroke_width}"/>
        """,
        "bolt": f"""
            <path d="M13 2L4 13H11L10 22L20 10H13L13 2Z" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"/>
        """
    }

    inner = icons_svg.get(name, icons_svg["activity"])
    return f"""<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; display: inline-block;">{inner}</svg>"""
