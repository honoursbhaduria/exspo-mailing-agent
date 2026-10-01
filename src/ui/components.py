"""
Modular UI Components for Influencer Outreach System
Clean glassmorphic cards, HugeIcons SVGs, no emojis, no black, no harsh shadows.
Harmonized with styles.py and matching image.png.
"""

from src.ui.icons import icon

def render_hero_header() -> str:
    return """
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
    """

def render_left_showcase_card(total_count: int = 65, avg_followers: str = "35K", avg_reach: str = "11K") -> str:
    return f"""
    <div class="glass-card" style="height: 100%;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
            <span style="font-size: 0.92rem; font-weight: 700; color: #1E293B;">Audience Reach</span>
            <span class="badge-pill-neutral">{icon('activity', 12, '#64748B')} LIVE</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 18px;">
            <div>
                <div class="stat-number mono-num">{total_count}</div>
                <div class="stat-label">Discovered</div>
            </div>
            <div>
                <div class="stat-number mono-num">{avg_followers}</div>
                <div class="stat-label">Avg Followers</div>
            </div>
            <div>
                <div class="stat-number mono-num">{avg_reach}</div>
                <div class="stat-label">Avg Reach</div>
            </div>
        </div>
        <!-- Smooth Curve Trajectory Waves (Sky Azure & Soft Violet) -->
        <div style="margin: 12px 0 18px;">
            <svg viewBox="0 0 240 50" style="width: 100%; height: 48px; overflow: visible;">
                <path d="M 0,38 Q 60,8 120,26 T 240,12" fill="none" stroke="#38BDF8" stroke-width="2.5" stroke-linecap="round"/>
                <path d="M 0,46 Q 70,40 140,18 T 240,36" fill="none" stroke="#818CF8" stroke-width="2" stroke-linecap="round" opacity="0.85"/>
            </svg>
        </div>
        <!-- Top Micro-influencer Ranking Rows -->
        <div style="font-size: 0.74rem; font-weight: 700; color: #64748B; margin-bottom: 8px; letter-spacing: 0.4px;">
            TOP QUALIFIED CREATORS
        </div>
        <div class="glass-card-subtle" style="margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 0.82rem; font-weight: 600; color: #1E293B;">Nazima Mogra</span>
            <span class="mono-num" style="font-size: 0.76rem; font-weight: 600; color: #2563EB;">62.0K</span>
        </div>
        <div class="glass-card-subtle" style="margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 0.82rem; font-weight: 600; color: #1E293B;">Isabella Quintero</span>
            <span class="mono-num" style="font-size: 0.76rem; font-weight: 600; color: #2563EB;">36.8K</span>
        </div>
        <div class="glass-card-subtle" style="margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center; border-color: #BFDBFE;">
            <span style="font-size: 0.82rem; font-weight: 600; color: #2563EB;">Dhanu Gunathissa</span>
            <span class="mono-num" style="font-size: 0.76rem; font-weight: 700; color: #2563EB;">92.0K</span>
        </div>
        <div class="glass-card-subtle" style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 0.82rem; font-weight: 600; color: #1E293B;">Rashonda Wisner</span>
            <span class="mono-num" style="font-size: 0.76rem; font-weight: 600; color: #2563EB;">24.5K</span>
        </div>
    </div>
    """

def render_center_topbar() -> str:
    return """
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid #ECEFF8;">
        <div style="display: flex; align-items: center; gap: 8px;">
            <div style="width: 10px; height: 10px; border-radius: 3px; background: #2563EB;"></div>
            <span style="font-size: 0.95rem; font-weight: 700; color: #1E293B;">Dashboard Control</span>
        </div>
        <div style="display: flex; gap: 10px; align-items: center;">
            <div style="width: 55px; height: 6px; background: #E0F2FE; border-radius: 9999px; overflow: hidden;">
                <div style="width: 80%; height: 100%; background: #0284C7; border-radius: 9999px;"></div>
            </div>
            <div style="width: 55px; height: 6px; background: #FCE7F3; border-radius: 9999px; overflow: hidden;">
                <div style="width: 100%; height: 100%; background: #EC4899; border-radius: 9999px;"></div>
            </div>
            <div style="width: 55px; height: 6px; background: #EEF2FF; border-radius: 9999px; overflow: hidden;">
                <div style="width: 65%; height: 100%; background: #6366F1; border-radius: 9999px;"></div>
            </div>
        </div>
    </div>
    """

def render_center_stat_tiles(total_count: int, passed_count: int, sent_count: int) -> str:
    return f"""
    <div class="stat-tile-grid">
        <div class="stat-tile purple">
            <div class="stat-tile-val">{total_count}</div>
            <div class="stat-tile-lbl">Total Profiles</div>
        </div>
        <div class="stat-tile blue">
            <div class="stat-tile-val">{passed_count}</div>
            <div class="stat-tile-lbl">Qualified (5k-100k)</div>
        </div>
        <div class="stat-tile pink">
            <div class="stat-tile-val">{sent_count}</div>
            <div class="stat-tile-lbl">Outreach Dispatched</div>
        </div>
    </div>
    """

def render_right_feed_card() -> str:
    return f"""
    <div class="glass-card" style="height: 100%;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
            <span style="font-size: 0.92rem; font-weight: 700; color: #1E293B;">Feed & Activity</span>
            <span class="badge-pill-neutral">{icon('globe', 12, '#64748B')} Global</span>
        </div>
        <div style="display: flex; flex-direction: column; gap: 8px;">
            <div style="display: flex; align-items: center; justify-content: space-between; padding-bottom: 8px; border-bottom: 1px solid #ECEFF8;">
                <div>
                    <div style="font-size: 0.84rem; font-weight: 600; color: #1E293B;">Alina Paziuk</div>
                    <div class="mono-num" style="font-size: 0.74rem; color: #64748B;">London, UK</div>
                </div>
                <span class="badge-pill-pass">{icon('check_circle', 11, '#065F46')} PASS</span>
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between; padding-bottom: 8px; border-bottom: 1px solid #ECEFF8;">
                <div>
                    <div style="font-size: 0.84rem; font-weight: 600; color: #1E293B;">Cameron Stokes</div>
                    <div class="mono-num" style="font-size: 0.74rem; color: #64748B;">Athens, US</div>
                </div>
                <span class="badge-pill-pass">{icon('check_circle', 11, '#065F46')} PASS</span>
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between; padding-bottom: 8px; border-bottom: 1px solid #ECEFF8;">
                <div>
                    <div style="font-size: 0.84rem; font-weight: 600; color: #1E293B;">Katarina Durcakova</div>
                    <div class="mono-num" style="font-size: 0.74rem; color: #64748B;">Slovakia</div>
                </div>
                <span class="badge-pill-fail">{icon('cross_circle', 11, '#991B1B')} &lt; 5k</span>
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between; padding-bottom: 8px; border-bottom: 1px solid #ECEFF8;">
                <div>
                    <div style="font-size: 0.84rem; font-weight: 600; color: #1E293B;">Allee-Sutton H.</div>
                    <div class="mono-num" style="font-size: 0.74rem; color: #64748B;">Nashville, US</div>
                </div>
                <span class="badge-pill-pass">{icon('check_circle', 11, '#065F46')} PASS</span>
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <div style="font-size: 0.84rem; font-weight: 600; color: #1E293B;">Jordy Boulet-Viau</div>
                    <div class="mono-num" style="font-size: 0.74rem; color: #64748B;">Montreal, CA</div>
                </div>
                <span class="badge-pill-fail">{icon('cross_circle', 11, '#991B1B')} &gt; 100k</span>
            </div>
        </div>
    </div>
    """
