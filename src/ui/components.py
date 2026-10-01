"""
Modular UI Components for Influencer Outreach System
Clean glassmorphic cards, Navbar Action Button SVGs, #03045e single color theme,
icon-free Dashboard header, and uniform stat tiles.
"""

from src.ui.icons import icon

def render_hero_header() -> str:
    return """
    <div class="hero-wrapper">
        <div class="brand-pill">
            <div class="icon-conatiner" title="EDXSO Architecture">
                <svg width="19px" height="21px" viewBox="0 0 19 21" version="1.1" xmlns="http://www.w3.org/2000/svg">
                    <g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                        <g transform="translate(-142.000000, -122.000000)">
                            <g transform="translate(142.000000, 122.000000)">
                                <path d="M3.4,4 L11.5,4 L16,8.25 L16,17.6 C16,19.4777681 14.4777681,21 12.6,21 L3.4,21 C1.52223185,21 0,19.4777681 0,17.6 L0,7.4 C0,5.52223185 1.52223185,4 3.4,4 Z" fill="#C4FFE4" />
                                <path d="M6.4,0 L12,0 L19,6.5 L19,14.6 C19,16.4777681 17.4777681,18 15.6,18 L6.4,18 C4.52223185,18 3,16.4777681 3,14.6 L3,3.4 C3,1.52223185 4.52223185,0 6.4,0 Z" fill="#85EBBC" />
                                <path d="M12,0 L12,5.5 C12,6.05228475 12.4477153,6.5 13,6.5 L19,6.5 L12,0 Z" fill="#64B18D" />
                            </g>
                        </g>
                    </g>
                </svg>
                <svg width="19px" height="21px" viewBox="0 0 19 21" version="1.1" xmlns="http://www.w3.org/2000/svg">
                    <g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                        <g transform="translate(-142.000000, -122.000000)">
                            <g transform="translate(142.000000, 122.000000)">
                                <path d="M3.4,4 L11.5,4 L16,8.25 L16,17.6 C16,19.4777681 14.4777681,21 12.6,21 L3.4,21 C1.52223185,21 0,19.4777681 0,17.6 L0,7.4 C0,5.52223185 1.52223185,4 3.4,4 Z" fill="#C4FFE4" />
                                <path d="M6.4,0 L12,0 L19,6.5 L19,14.6 C19,16.4777681 17.4777681,18 15.6,18 L6.4,18 C4.52223185,18 3,16.4777681 3,14.6 L3,3.4 C3,1.52223185 4.52223185,0 6.4,0 Z" fill="#85EBBC" />
                                <path d="M12,0 L12,5.5 C12,6.05228475 12.4477153,6.5 13,6.5 L19,6.5 L12,0 Z" fill="#64B18D" />
                            </g>
                        </g>
                    </g>
                </svg>
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
            <span style="font-size: 0.92rem; font-weight: 700; color: #03045e;">Audience Reach</span>
            <span class="badge-pill-neutral">{icon('activity', 12, '#03045e')} LIVE</span>
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
        <!-- Single Unified Color Wave Trajectory (#03045e) -->
        <div style="margin: 12px 0 18px;">
            <svg viewBox="0 0 240 50" style="width: 100%; height: 48px; overflow: visible;">
                <path d="M 0,38 Q 60,8 120,26 T 240,12" fill="none" stroke="#03045e" stroke-width="2.5" stroke-linecap="round"/>
                <path d="M 0,46 Q 70,40 140,18 T 240,36" fill="none" stroke="#03045e" stroke-width="1.8" stroke-linecap="round" opacity="0.35"/>
            </svg>
        </div>
        <!-- Top Micro-influencer Ranking Rows -->
        <div style="font-size: 0.74rem; font-weight: 700; color: #5A6282; margin-bottom: 8px; letter-spacing: 0.4px;">
            TOP QUALIFIED CREATORS
        </div>
        <div class="glass-card-subtle" style="margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 0.82rem; font-weight: 600; color: #03045e;">Nazima Mogra</span>
            <span class="mono-num" style="font-size: 0.76rem; font-weight: 700; color: #03045e;">62.0K</span>
        </div>
        <div class="glass-card-subtle" style="margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 0.82rem; font-weight: 600; color: #03045e;">Isabella Quintero</span>
            <span class="mono-num" style="font-size: 0.76rem; font-weight: 700; color: #03045e;">36.8K</span>
        </div>
        <div class="glass-card-subtle" style="margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center; border-color: #03045e;">
            <span style="font-size: 0.82rem; font-weight: 700; color: #03045e;">Dhanu Gunathissa</span>
            <span class="mono-num" style="font-size: 0.76rem; font-weight: 700; color: #03045e;">92.0K</span>
        </div>
        <div class="glass-card-subtle" style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 0.82rem; font-weight: 600; color: #03045e;">Rashonda Wisner</span>
            <span class="mono-num" style="font-size: 0.76rem; font-weight: 700; color: #03045e;">24.5K</span>
        </div>
    </div>
    """

def render_center_topbar() -> str:
    # Notice: ZERO icons in front of "Dashboard", strictly single-color #03045e bars
    return """
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid #ECEFF8;">
        <div>
            <span style="font-size: 1.05rem; font-weight: 700; color: #03045e; letter-spacing: -0.2px;">Dashboard</span>
        </div>
        <div style="display: flex; gap: 8px; align-items: center;">
            <div style="width: 50px; height: 5px; background: #EEF2F6; border-radius: 9999px; overflow: hidden;">
                <div style="width: 80%; height: 100%; background: #03045e; border-radius: 9999px;"></div>
            </div>
            <div style="width: 50px; height: 5px; background: #EEF2F6; border-radius: 9999px; overflow: hidden;">
                <div style="width: 60%; height: 100%; background: #03045e; opacity: 0.65; border-radius: 9999px;"></div>
            </div>
            <div style="width: 50px; height: 5px; background: #EEF2F6; border-radius: 9999px; overflow: hidden;">
                <div style="width: 40%; height: 100%; background: #03045e; opacity: 0.4; border-radius: 9999px;"></div>
            </div>
        </div>
    </div>
    """

def render_center_stat_tiles(total_count: int, passed_count: int, sent_count: int) -> str:
    # EXACT same single color design for all three cards: no multiple or two-colored styling
    return f"""
    <div class="stat-tile-grid">
        <div class="stat-tile">
            <div class="stat-tile-val">{total_count}</div>
            <div class="stat-tile-lbl">Total Profiles</div>
        </div>
        <div class="stat-tile">
            <div class="stat-tile-val">{passed_count}</div>
            <div class="stat-tile-lbl">Qualified (5k-100k)</div>
        </div>
        <div class="stat-tile">
            <div class="stat-tile-val">{sent_count}</div>
            <div class="stat-tile-lbl">Outreach Dispatched</div>
        </div>
    </div>
    """

def render_right_feed_card() -> str:
    return f"""
    <div class="glass-card" style="height: 100%;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
            <span style="font-size: 0.92rem; font-weight: 700; color: #03045e;">Feed & Activity</span>
            <span class="badge-pill-neutral">{icon('globe', 12, '#03045e')} Global</span>
        </div>
        <div style="display: flex; flex-direction: column; gap: 8px;">
            <div style="display: flex; align-items: center; justify-content: space-between; padding-bottom: 8px; border-bottom: 1px solid #ECEFF8;">
                <div>
                    <div style="font-size: 0.84rem; font-weight: 600; color: #03045e;">Alina Paziuk</div>
                    <div class="mono-num" style="font-size: 0.74rem; color: #5A6282;">London, UK</div>
                </div>
                <span class="badge-pill-pass">{icon('check_circle', 11, '#03045e')} PASS</span>
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between; padding-bottom: 8px; border-bottom: 1px solid #ECEFF8;">
                <div>
                    <div style="font-size: 0.84rem; font-weight: 600; color: #03045e;">Cameron Stokes</div>
                    <div class="mono-num" style="font-size: 0.74rem; color: #5A6282;">Athens, US</div>
                </div>
                <span class="badge-pill-pass">{icon('check_circle', 11, '#03045e')} PASS</span>
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between; padding-bottom: 8px; border-bottom: 1px solid #ECEFF8;">
                <div>
                    <div style="font-size: 0.84rem; font-weight: 600; color: #03045e;">Katarina Durcakova</div>
                    <div class="mono-num" style="font-size: 0.74rem; color: #5A6282;">Slovakia</div>
                </div>
                <span class="badge-pill-fail">{icon('cross_circle', 11, '#5A6282')} &lt; 5k</span>
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between; padding-bottom: 8px; border-bottom: 1px solid #ECEFF8;">
                <div>
                    <div style="font-size: 0.84rem; font-weight: 600; color: #03045e;">Allee-Sutton H.</div>
                    <div class="mono-num" style="font-size: 0.74rem; color: #5A6282;">Nashville, US</div>
                </div>
                <span class="badge-pill-pass">{icon('check_circle', 11, '#03045e')} PASS</span>
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <div style="font-size: 0.84rem; font-weight: 600; color: #03045e;">Jordy Boulet-Viau</div>
                    <div class="mono-num" style="font-size: 0.74rem; color: #5A6282;">Montreal, CA</div>
                </div>
                <span class="badge-pill-fail">{icon('cross_circle', 11, '#5A6282')} &gt; 100k</span>
            </div>
        </div>
    </div>
    """
