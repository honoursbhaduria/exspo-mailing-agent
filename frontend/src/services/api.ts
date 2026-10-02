export interface Influencer {
  name: string;
  handle: string;
  platform: string;
  profile_url: string;
  follower_str?: string;
  follower_count: number;
  engagement_rate: number;
  niche: string;
  location: string;
  price?: string;
  rating?: number;
  bio?: string;
  contact_email?: string;
  content_themes?: string;
  audience_age?: string;
  audience_gender?: string;
  audience_geography?: string;
  qualification_status?: 'PASSED' | 'FAILED';
  qualification_reason?: string;
  instagram_url?: string;
  tiktok_url?: string;
  youtube_url?: string;
}

export interface PersonalizedPitch {
  influencer: string;
  handle: string;
  collaboration_type: string;
  subject: string;
  email_pitch: string;
  email_word_count: number;
  instagram_dm: string;
  dm_word_count: number;
  generated_at?: string;
}

export interface OutreachRecord {
  influencer: string;
  handle: string;
  email: string;
  platform: string;
  channel: string;
  sent: boolean;
  status: string;
  delivery_id: string;
  date: string;
  notes?: string;
}

export interface TrackerStats {
  total_logged: number;
  successfully_sent: number;
  mail_sent?: number;
  dm_sent?: number;
  skipped: number;
}

export interface DatabaseStatus {
  engine: string;
  is_postgres: boolean;
  connected: boolean;
  total_records: number;
  database_url_configured: boolean;
  storage_target: string;
}

export interface FilterResponse {
  total: number;
  total_evaluated: number;
  passed_count: number;
  failed_count: number;
  target_geography?: string;
  target_platform?: string;
  target_niche?: string;
  results: Influencer[];
  passed_influencers: Influencer[];
  failed_influencers: Influencer[];
}

const rawBase: string = (import.meta as any).env?.VITE_API_URL || '';
const cleanBase = rawBase ? rawBase.replace(/\/+$/, '') : '';
const API_BASE = cleanBase
  ? (cleanBase.endsWith('/api') ? cleanBase : `${cleanBase}/api`)
  : '/api';

export const api = {
  async getDatabaseStatus(): Promise<DatabaseStatus> {
    const res = await fetch(`${API_BASE}/database/status`);
    if (!res.ok) throw new Error('Failed to fetch database status');
    return res.json();
  },

  async getCountries(): Promise<{ total: number; countries: string[] }> {
    const res = await fetch(`${API_BASE}/geo/countries`);
    if (!res.ok) throw new Error('Failed to fetch countries list');
    return res.json();
  },

  async getRawInfluencers(limit?: number, offset = 0, search?: string): Promise<{ total: number; count: number; limit?: number; offset: number; influencers: Influencer[] }> {
    let url = `${API_BASE}/influencers/raw?offset=${offset}`;
    if (limit !== undefined && limit !== null) {
      url += `&limit=${limit}`;
    }
    if (search) {
      url += `&search=${encodeURIComponent(search)}`;
    }
    const res = await fetch(url);
    if (!res.ok) throw new Error('Failed to fetch discovered influencers');
    return res.json();
  },

  async triggerDiscovery(niche = 'Fashion & Beauty', limit = 65, engine = 'scrapy', geo = 'Global (All Regions)'): Promise<{ status: string; discovered_count: number; engine?: string; geo?: string }> {
    const res = await fetch(`${API_BASE}/influencers/discover?niche=${encodeURIComponent(niche)}&limit=${limit}&engine=${encodeURIComponent(engine)}&geo=${encodeURIComponent(geo)}`, {
      method: 'POST',
    });
    if (!res.ok) throw new Error('Discovery pipeline failed');
    return res.json();
  },

  async filterInfluencers(params: {
    min_followers: number;
    max_followers: number;
    min_engagement: number;
    target_niche: string;
    target_geography?: string;
    target_platform?: string;
  }): Promise<FilterResponse> {
    const res = await fetch(`${API_BASE}/influencers/filter`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(params),
    });
    if (!res.ok) throw new Error('Filtering classification failed');
    return res.json();
  },

  async generatePersonalization(params: {
    influencer: Record<string, any>;
    brand_name: string;
    collaboration_type: string;
  }): Promise<{ status: string; messages: PersonalizedPitch }> {
    const res = await fetch(`${API_BASE}/personalize`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(params),
    });
    if (!res.ok) throw new Error('Failed to generate personalized outreach');
    return res.json();
  },

  async sendOutreach(params: {
    to_email: string;
    subject: string;
    message_body: string;
    recipient_name: string;
    handle: string;
    platform: string;
    instagram_dm?: string;
    notes?: string;
  }): Promise<any> {
    const res = await fetch(`${API_BASE}/outreach/send`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(params),
    });
    if (!res.ok) throw new Error('Outreach dispatch failed');
    return res.json();
  },

  async getTrackerStats(): Promise<{ stats: TrackerStats; logs: OutreachRecord[] }> {
    const res = await fetch(`${API_BASE}/outreach/tracker`);
    if (!res.ok) throw new Error('Failed to fetch outreach audit log');
    return res.json();
  },
};
