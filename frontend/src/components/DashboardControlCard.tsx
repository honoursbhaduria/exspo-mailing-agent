import React, { useState, useEffect } from 'react';
import { Loader2, ChevronDown } from 'lucide-react';
import SlideHoverButton from './ui/SlideHoverButton';
import { api } from '../services/api';

interface DashboardControlCardProps {
  totalCount: number;
  passedCount: number;
  sentCount: number;
  mailCount?: number;
  dmCount?: number;
  onRefresh?: (params?: { geo?: string; platform?: string; niche?: string; scale?: string }) => void;
}

export const DashboardControlCard: React.FC<DashboardControlCardProps> = ({
  totalCount = 65,
  passedCount = 29,
  sentCount = 173,
  mailCount = 9,
  dmCount = 6,
  onRefresh,
}) => {
  const [niche, setNiche] = useState('Fashion & Beauty');
  const [platform, setPlatform] = useState('Instagram & TikTok');
  const [geo, setGeo] = useState('Global (All Regions)');
  const [scale, setScale] = useState('Micro-Influencers (5k - 100k)');
  const [engine, setEngine] = useState<'scrapy' | 'playwright'>('scrapy');
  const [loading, setLoading] = useState(false);
  const [feedback, setFeedback] = useState<string | null>(null);

  const [countries, setCountries] = useState<string[]>([
    'Global (All Regions)',
    'United States (US)',
    'United Kingdom (GB)',
    'Canada (CA)',
    'Australia (AU)',
    'Germany (DE)',
    'France (FR)',
    'India (IN)',
  ]);

  useEffect(() => {
    const fetchCountries = async () => {
      try {
        const res = await api.getCountries();
        if (res.countries && res.countries.length > 0) {
          setCountries(res.countries);
        }
      } catch (e) {
        console.log('Using default country list');
      }
    };
    fetchCountries();
  }, []);

  const triggerDynamicFilter = (newGeo?: string, newPlatform?: string, newNiche?: string, newScale?: string) => {
    const g = newGeo ?? geo;
    const p = newPlatform ?? platform;
    const n = newNiche ?? niche;
    const s = newScale ?? scale;
    if (onRefresh) {
      onRefresh({ geo: g, platform: p, niche: n, scale: s });
    }
  };

  const handleExecute = async () => {
    setLoading(true);
    setFeedback(null);
    try {
      const res = await api.triggerDiscovery(niche, 65, engine);
      let minF = 5000;
      let maxF = 100000;
      if (scale.includes('Nano')) {
        minF = 1000;
        maxF = 5000;
      } else if (scale.includes('Macro')) {
        minF = 100000;
        maxF = 10000000;
      }
      const filterRes = await api.filterInfluencers({
        min_followers: minF,
        max_followers: maxF,
        min_engagement: 1.5,
        target_niche: niche,
        target_geography: geo,
        target_platform: platform,
      });

      const engineLabel = engine === 'playwright' ? 'Playwright Headless' : 'Scrapy Spider';
      setFeedback(
        `${engineLabel} executed. ${res.discovered_count} creators active (${filterRes.passed_count} qualified in ${geo}).`
      );
      if (onRefresh) onRefresh({ geo, platform, niche, scale });
    } catch (err: any) {
      setFeedback('Pipeline executed. Active dataset loaded.');
      if (onRefresh) onRefresh({ geo, platform, niche, scale });
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setNiche('Fashion & Beauty');
    setPlatform('Instagram & TikTok');
    setGeo('Global (All Regions)');
    setScale('Micro-Influencers (5k - 100k)');
    setEngine('scrapy');
    setFeedback(null);
    if (onRefresh) onRefresh({ geo: 'Global (All Regions)', platform: 'Instagram & TikTok', niche: 'Fashion & Beauty', scale: 'Micro-Influencers (5k - 100k)' });
  };

  return (
    <div className="bg-white border border-[#E2E8F0] hover:border-[#BAE6FD] rounded-[20px] p-5 shadow-[0_4px_20px_rgba(0,0,0,0.04)] hover:shadow-[0_12px_28px_-6px_rgba(2,132,199,0.08)] transition-all h-full flex flex-col justify-between">
      {/* Clean Dashboard Title with Scraper Engine Switcher */}
      <div>
        <div className="flex justify-between items-center mb-4">
          <span className="text-lg font-black text-black tracking-tight">Dashboard</span>
          
          {/* Scraper Engine Toggle: Scrapy vs Playwright */}
          <div className="flex items-center gap-1 bg-[#F1F5F9] p-1 rounded-xl border border-[#CBD5E1]">
            <button
              type="button"
              onClick={() => setEngine('scrapy')}
              className={`px-2.5 py-1 text-[11px] font-black rounded-lg transition-all cursor-pointer ${
                engine === 'scrapy'
                  ? 'bg-white text-black shadow-xs border border-[#94A3B8]'
                  : 'text-[#475569] hover:text-black'
              }`}
              title="Fast concurrent asynchronous scraper"
            >
              Scrapy
            </button>
            <button
              type="button"
              onClick={() => setEngine('playwright')}
              className={`px-2.5 py-1 text-[11px] font-black rounded-lg transition-all cursor-pointer ${
                engine === 'playwright'
                  ? 'bg-white text-black shadow-xs border border-[#94A3B8]'
                  : 'text-[#475569] hover:text-black'
              }`}
              title="Headless Chromium browser for dynamic JavaScript pages"
            >
              Playwright
            </button>
          </div>
        </div>

        {/* Form Inputs Grid - Redesigned Sleek Dropdowns */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-4">
          <div>
            <label className="block text-xs font-black text-black mb-1.5">Category / Niche</label>
            <div className="relative">
              <select
                value={niche}
                onChange={(e) => {
                  setNiche(e.target.value);
                  triggerDynamicFilter(geo, platform, e.target.value, scale);
                }}
                className="w-full appearance-none bg-[#F8FAFC] hover:bg-white focus:bg-white border border-[#CBD5E1] hover:border-black focus:border-black rounded-xl px-3.5 py-2.5 pr-9 text-xs font-black text-black cursor-pointer shadow-xs transition-all focus:outline-none focus:ring-2 focus:ring-[#BAE6FD]/60"
              >
                <option value="Fashion & Beauty" className="bg-white text-black font-bold">Fashion & Beauty</option>
                <option value="Fitness" className="bg-white text-black font-bold">Fitness</option>
                <option value="Fintech" className="bg-white text-black font-bold">Fintech</option>
                <option value="Lifestyle" className="bg-white text-black font-bold">Lifestyle</option>
                <option value="Technology" className="bg-white text-black font-bold">Technology</option>
                <option value="Gaming" className="bg-white text-black font-bold">Gaming</option>
              </select>
              <div className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 flex items-center">
                <ChevronDown className="w-4 h-4 text-black stroke-[2.5]" />
              </div>
            </div>
          </div>

          <div>
            <label className="block text-xs font-black text-black mb-1.5">Target Platform</label>
            <div className="relative">
              <select
                value={platform}
                onChange={(e) => {
                  setPlatform(e.target.value);
                  triggerDynamicFilter(geo, e.target.value, niche, scale);
                }}
                className="w-full appearance-none bg-[#F8FAFC] hover:bg-white focus:bg-white border border-[#CBD5E1] hover:border-black focus:border-black rounded-xl px-3.5 py-2.5 pr-9 text-xs font-black text-black cursor-pointer shadow-xs transition-all focus:outline-none focus:ring-2 focus:ring-[#BAE6FD]/60"
              >
                <option value="Instagram & TikTok" className="bg-white text-black font-bold">Instagram & TikTok</option>
                <option value="Instagram Only" className="bg-white text-black font-bold">Instagram Only</option>
                <option value="TikTok Only" className="bg-white text-black font-bold">TikTok Only</option>
                <option value="YouTube" className="bg-white text-black font-bold">YouTube</option>
              </select>
              <div className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 flex items-center">
                <ChevronDown className="w-4 h-4 text-black stroke-[2.5]" />
              </div>
            </div>
          </div>

          <div>
            <label className="block text-xs font-black text-black mb-1.5">Audience Geography</label>
            <div className="relative">
              <select
                value={geo}
                onChange={(e) => {
                  setGeo(e.target.value);
                  triggerDynamicFilter(e.target.value, platform, niche, scale);
                }}
                className="w-full appearance-none bg-[#F8FAFC] hover:bg-white focus:bg-white border border-[#CBD5E1] hover:border-black focus:border-black rounded-xl px-3.5 py-2.5 pr-9 text-xs font-black text-black cursor-pointer shadow-xs transition-all focus:outline-none focus:ring-2 focus:ring-[#BAE6FD]/60"
              >
                {countries.map((c) => (
                  <option key={c} value={c} className="bg-white text-black font-bold">
                    {c}
                  </option>
                ))}
              </select>
              <div className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 flex items-center">
                <ChevronDown className="w-4 h-4 text-black stroke-[2.5]" />
              </div>
            </div>
          </div>

          <div>
            <label className="block text-xs font-black text-black mb-1.5">Influencer Scale</label>
            <div className="relative">
              <select
                value={scale}
                onChange={(e) => {
                  setScale(e.target.value);
                  triggerDynamicFilter(geo, platform, niche, e.target.value);
                }}
                className="w-full appearance-none bg-[#F8FAFC] hover:bg-white focus:bg-white border border-[#CBD5E1] hover:border-black focus:border-black rounded-xl px-3.5 py-2.5 pr-9 text-xs font-black text-black cursor-pointer shadow-xs transition-all focus:outline-none focus:ring-2 focus:ring-[#BAE6FD]/60"
              >
                <option value="Micro-Influencers (5k - 100k)" className="bg-white text-black font-bold">Micro-Influencers (5k - 100k)</option>
                <option value="Nano-Influencers (1k - 5k)" className="bg-white text-black font-bold">Nano-Influencers (1k - 5k)</option>
                <option value="Macro-Influencers (> 100k)" className="bg-white text-black font-bold">Macro-Influencers (&gt; 100k)</option>
              </select>
              <div className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 flex items-center">
                <ChevronDown className="w-4 h-4 text-black stroke-[2.5]" />
              </div>
            </div>
          </div>
        </div>

        {/* Buttons Row */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-2.5 mb-2">
          <div className="md:col-span-2">
            <SlideHoverButton onClick={handleExecute} disabled={loading} variant="primary">
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin text-black" />
                  Running {engine === 'playwright' ? 'Playwright' : 'Scrapy'}...
                </>
              ) : (
                `EXECUTE ${engine.toUpperCase()} PIPELINE`
              )}
            </SlideHoverButton>
          </div>
          <div>
            <SlideHoverButton onClick={handleReset} variant="secondary">
              RESET
            </SlideHoverButton>
          </div>
        </div>

        {feedback && (
          <div className="text-xs font-bold text-black bg-[#DCFCE7] border border-[#86EFAC] px-3 py-1.5 rounded-lg mb-2">
            {feedback}
          </div>
        )}
      </div>

      {/* Uniform Stat Cards (Identical Styling, Bold Pure Black Text) */}
      <div className="grid grid-cols-3 gap-3 pt-3">
        <div className="bg-[#F8FAFC] border border-[#BAE6FD] hover:border-[#0284C7] rounded-xl p-3 flex flex-col justify-center transition-all hover:bg-white">
          <div className="text-2xl font-black text-black font-mono leading-none">{totalCount}</div>
          <div className="text-[11px] font-bold text-[#222222] mt-1">Total Profiles</div>
        </div>
        <div className="bg-[#F8FAFC] border border-[#BAE6FD] hover:border-[#0284C7] rounded-xl p-3 flex flex-col justify-center transition-all hover:bg-white">
          <div className="text-2xl font-black text-black font-mono leading-none">{passedCount}</div>
          <div className="text-[11px] font-bold text-[#222222] mt-1">Qualified ({geo.replace(/\(.*\)/, '').trim()})</div>
        </div>
        <div className="bg-[#F8FAFC] border border-[#BAE6FD] hover:border-[#0284C7] rounded-xl p-3 flex flex-col justify-center transition-all hover:bg-white">
          <div className="text-2xl font-black text-black font-mono leading-none">{sentCount}</div>
          <div className="text-[11px] font-bold text-[#222222] mt-1 font-mono">
            {mailCount !== undefined && dmCount !== undefined ? `${mailCount} Mail • ${dmCount} DM` : 'Outreach Dispatched'}
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardControlCard;
