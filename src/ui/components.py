"""
Modular UI Components for Influencer Outreach System
Clean glassmorphic components, HugeIcons SVGs, no emojis, no black, no harsh shadows.
"""

from src.ui.icons import icon

def render_hero_header() -> str:
    return f"""
    <div class="app-header">
        <div class="brand-capsule">
            <div class="capsule-dot">
                <div class="capsule-dot-top"></div>
                <div class="capsule-dot-bottom"></div>
            </div>
            <span class="brand-title">Goscraping &nbsp;|&nbsp; EDXSO</span>
        </div>
        <h1 class="main-heading">Dashboard scraping</h1>
        <p class="main-subheading">Dashboard is developed for scraping data from multiple known platforms</p>
    </div>
    """

def render_left_showcase_card(total_count: int = 65, avg_followers: str = "35K", avg_reach: str = "11K") -> str:
    return f"""
    <div class="glass-panel" style="height: 100%;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
            <span style="font-size: 0.86rem; font-weight: 700; color: #2D3142;">Audience Reach</span>
            <span class="badge-pill-neutral">{icon('activity', 12, '#5A5F75')} LIVE</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 16px;">
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
        <!-- Smooth Curve Trajectory Wave (Muted Slate Blue & Dusty Rose) -->
        <div style="margin: 12px 0 16px;">
            <svg viewBox="0 0 240 50" style="width: 100%; height: 46px; overflow: visible;">
                <path d="M 0,38 Q 60,10 120,28 T 240,12" fill="none" stroke="#6C8CA5" stroke-width="2.5" stroke-linecap="round"/>
                <path d="M 0,46 Q 70,42 140,20 T 240,38" fill="none" stroke="#9E7682" stroke-width="2" stroke-linecap="round" opacity="0.8"/>
            </svg>
        </div>
        <!-- Top Micro-influencer Ranking Rows -->
        <div style="font-size: 0.75rem; font-weight: 700; color: #8288A0; margin-bottom: 8px; letter-spacing: 0.3px;">
            TOP QUALIFIED CREATORS
        </div>
        <div class="glass-panel-subtle" style="padding: 7px 10px; margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 0.82rem; font-weight: 600; color: #373C52;">Nazima Mogra</span>
            <span class="mono-num" style="font-size: 0.75rem; font-weight: 600; color: #5B638A;">62.0K</span>
        </div>
        <div class="glass-panel-subtle" style="padding: 7px 10px; margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 0.82rem; font-weight: 600; color: #373C52;">Isabella Quintero</span>
            <span class="mono-num" style="font-size: 0.75rem; font-weight: 600; color: #5B638A;">36.8K</span>
        </div>
        <div class="glass-panel-subtle" style="padding: 7px 10px; margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center; border-color: rgba(91, 99, 138, 0.4);">
            <span style="font-size: 0.82rem; font-weight: 600; color: #5B638A;">Dhanu Gunathissa</span>
            <span class="mono-num" style="font-size: 0.75rem; font-weight: 700; color: #5B638A;">92.0K</span>
        </div>
        <div class="glass-panel-subtle" style="padding: 7px 10px; display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 0.82rem; font-weight: 600; color: #373C52;">Rashonda Wisner</span>
            <span class="mono-num" style="font-size: 0.75rem; font-weight: 600; color: #5B638A;">24.5K</span>
        </div>
    </div>
    """

def render_center_topbar() -> str:
    return f"""
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px; padding-bottom: 10px; border-bottom: 1px solid rgba(222, 227, 238, 0.7);">
        <div style="display: flex; align-items: center; gap: 8px;">
            <div style="width: 10px; height: 10px; border-radius: 3px; background: #5B638A;"></div>
            <span style="font-size: 0.92rem; font-weight: 700; color: #2D3142;">Dashboard Control</span>
        </div>
        <div style="display: flex; gap: 10px; align-items: center;">
            <div style="width: 55px; height: 5px; background: #DFE5EC; border-radius: 9999px; overflow: hidden;">
                <div style="width: 80%; height: 100%; background: #6C8CA5;"></div>
            </div>
            <div style="width: 55px; height: 5px; background: #EAE1E4; border-radius: 9999px; overflow: hidden;">
                <div style="width: 100%; height: 100%; background: #9E7682;"></div>
            </div>
            <div style="width: 55px; height: 5px; background: #DFE2EE; border-radius: 9999px; overflow: hidden;">
                <div style="width: 65%; height: 100%; background: #5B638A;"></div>
            </div>
        </div>
    </div>
    """

def render_center_stat_tiles(total_count: int, passed_count: int, sent_count: int) -> str:
    return f"""
    <div class="stat-tile-container">
        <div class="stat-tile-muted lavender">
            <div class="stat-number mono-num">{total_count}</div>
            <div class="stat-label">Total Profiles</div>
        </div>
        <div class="stat-tile-muted slate">
            <div class="stat-number mono-num">{passed_count}</div>
            <div class="stat-label">Qualified (5k-100k)</div>
        </div>
        <div class="stat-tile-muted sage">
            <div class="stat-number mono-num">{sent_count}</div>
            <div class="stat-label">Outreach Dispatched</div>
        </div>
    </div>
    """

def render_right_feed_card() -> str:
    return f"""
    <div class="glass-panel" style="height: 100%;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
            <span style="font-size: 0.92rem; font-weight: 700; color: #2D3142;">Feed & Activity</span>
            <span class="badge-pill-neutral">{icon('globe', 12, '#5A5F75')} Global</span>
        </div>
        <div style="display: flex; flex-direction: column; gap: 8px;">
            <div style="display: flex; align-items: center; justify-content: space-between; padding-bottom: 7px; border-bottom: 1px solid rgba(222, 227, 238, 0.6);">
                <div>
                    <div style="font-size: 0.82rem; font-weight: 600; color: #2D3142;">Alina Paziuk</div>
                    <div class="mono-num" style="font-size: 0.72rem; color: #8288A0;">London, UK</div>
                </div>
                <span class="badge-pill-pass">{icon('check_circle', 11, '#315844')} PASS</span>
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between; padding-bottom: 7px; border-bottom: 1px solid rgba(222, 227, 238, 0.6);">
                <div>
                    <div style="font-size: 0.82rem; font-weight: 600; color: #2D3142;">Cameron Stokes</div>
                    <div class="mono-num" style="font-size: 0.72rem; color: #8288A0;">Athens, US</div>
                </div>
                <span class="badge-pill-pass">{icon('check_circle', 11, '#315844')} PASS</span>
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between; padding-bottom: 7px; border-bottom: 1px solid rgba(222, 227, 238, 0.6);">
                <div>
                    <div style="font-size: 0.82rem; font-weight: 600; color: #2D3142;">Katarina Durcakova</div>
                    <div class="mono-num" style="font-size: 0.72rem; color: #8288A0;">Slovakia</div>
                </div>
                <span class="badge-pill-fail">{icon('cross_circle', 11, '#7D383D')} &lt; 5k</span>
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between; padding-bottom: 7px; border-bottom: 1px solid rgba(222, 227, 238, 0.6);">
                <div>
                    <div style="font-size: 0.82rem; font-weight: 600; color: #2D3142;">Allee-Sutton H.</div>
                    <div class="mono-num" style="font-size: 0.72rem; color: #8288A0;">Nashville, US</div>
                </div>
                <span class="badge-pill-pass">{icon('check_circle', 11, '#315844')} PASS</span>
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <div style="font-size: 0.82rem; font-weight: 600; color: #2D3142;">Jordy Boulet-Viau</div>
                    <div class="mono-num" style="font-size: 0.72rem; color: #8288A0;">Montreal, CA</div>
                </div>
                <span class="badge-pill-fail">{icon('cross_circle', 11, '#7D383D')} &gt; 100k</span>
            </div>
        </div>
    </div>
    """
