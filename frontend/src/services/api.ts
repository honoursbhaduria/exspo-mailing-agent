export interface Influencer {
  name: string;
  handle: string;
  platform: string;
  profile_url: string;
  follower_count: number;
  engagement_rate: number;
  niche: string;
  location: string;
  bio?: string;
  contact_email?: string;
  content_themes?: string;
  audience_age?: string;
  audience_gender?: string;
  audience_geography?: string;
  qualification_status?: 'PASSED' | 'FAILED';
  qualification_reason?: string;
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
  skipped: number;
}

const API_BASE = '/api';

export const api = {
  async getRawInfluencers(limit = 100): Promise<{ total: number; influencers: Influencer[] }> {
    const res = await fetch(`${API_BASE}/influencers/raw?limit=${limit}`);
    if (!res.ok) throw new Error('Failed to fetch discovered influencers');
    return res.json();
  },

  async triggerDiscovery(niche = 'Fashion', limit = 65): Promise<{ status: string; discovered_count: number }> {
    const res = await fetch(`${API_BASE}/influencers/discover?niche=${encodeURIComponent(niche)}&limit=${limit}`, {
      method: 'POST',
    });
    if (!res.ok) throw new Error('Scrapy discovery pipeline failed');
    return res.json();
  },

  async filterInfluencers(params: {
    min_followers: number;
    max_followers: number;
    min_engagement: number;
    target_niche: string;
  }): Promise<{ total: number; passed_count: number; failed_count: number; results: Influencer[] }> {
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
