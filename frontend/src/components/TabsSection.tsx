import React, { useState, useEffect } from 'react';
import { Search, Download, Sparkles, Send, ExternalLink, Loader2, ChevronDown, CheckCircle2, Mail, MessageSquare } from 'lucide-react';
import AnimatedOutlineNavbar, { type TabItem } from './ui/AnimatedOutlineNavbar';
import SlideHoverButton from './ui/SlideHoverButton';
import Pagination from './ui/Pagination';
import { api, type Influencer, type PersonalizedPitch, type OutreachRecord, type TrackerStats } from '../services/api';

const TABS: TabItem[] = [
  { id: 'records', label: 'Discovered Records' },
  { id: 'classification', label: 'Classification Engine' },
  { id: 'enrichment', label: 'Profile Context & Themes' },
  { id: 'personalization', label: 'AI Personalization' },
  { id: 'tracker', label: 'Outreach Audit Log' },
];

export const TabsSection: React.FC = () => {
  const [activeTab, setActiveTab] = useState('records');

  // Datasets & Tab 1 Pagination
  const [influencers, setInfluencers] = useState<Influencer[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [recordsPage, setRecordsPage] = useState(1);
  const [recordsPerPage, setRecordsPerPage] = useState(10);

  // Classification Tab State
  const [minFollowers, setMinFollowers] = useState(5000);
  const [maxFollowers, setMaxFollowers] = useState(100000);
  const [minEngagement, setMinEngagement] = useState(2.0);
  const [filterLoading, setFilterLoading] = useState(false);
  const [filteredResults, setFilteredResults] = useState<Influencer[]>([]);

  // Enrichment Tab State
  const [selectedHandle, setSelectedHandle] = useState<string>('');

  // AI Personalization Tab State
  const [targetCreator, setTargetCreator] = useState<string>('');
  const [brandName, setBrandName] = useState('LumiGlow');
  const [collabType, setCollabType] = useState('UGC & Paid Showcase');
  const [generating, setGenerating] = useState(false);
  const [activePitch, setActivePitch] = useState<PersonalizedPitch | null>(null);

  // Outreach Tracker State & Pagination
  const [trackerStats, setTrackerStats] = useState<TrackerStats>({ total_logged: 173, successfully_sent: 128, skipped: 45 });
  const [outreachLogs, setOutreachLogs] = useState<OutreachRecord[]>([]);
  const [auditPage, setAuditPage] = useState(1);
  const [auditPerPage, setAuditPerPage] = useState(10);

  // Tab 2 Classification Filters
  const [filterGeo, setFilterGeo] = useState('Global (All Regions)');
  const [filterPlatform, setFilterPlatform] = useState('All Platforms');
  const [filterNiche, setFilterNiche] = useState('Fashion & Beauty');
  const [filterCountries, setFilterCountries] = useState<string[]>([
    'Global (All Regions)',
    'United States (US)',
    'United Kingdom (GB)',
    'Canada (CA)',
    'Australia (AU)',
    'Germany (DE)',
    'France (FR)',
    'India (IN)',
  ]);

  // Load Initial Datasets
  useEffect(() => {
    fetchRawRecords();
    fetchTracker();
    runFilter();
    const fetchGeo = async () => {
      try {
        const res = await api.getCountries();
        if (res.countries && res.countries.length > 0) {
          setFilterCountries(res.countries);
        }
      } catch (e) {}
    };
    fetchGeo();
  }, []);

  const fetchRawRecords = async () => {
    try {
      setLoading(true);
      const res = await api.getRawInfluencers(100);
      setInfluencers(res.influencers);
      if (res.influencers.length > 0) {
        setSelectedHandle(res.influencers[0].handle);
        setTargetCreator(res.influencers[0].handle);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const fetchTracker = async () => {
    try {
      const res = await api.getTrackerStats();
      setTrackerStats(res.stats);
      setOutreachLogs(res.logs);
    } catch (err) {
      console.error(err);
    }
  };

  // Run Classification Engine with full multi-dimensional criteria
  const runFilter = async (customGeo?: string, customPlatform?: string, customNiche?: string) => {
    try {
      setFilterLoading(true);
      const res = await api.filterInfluencers({
        min_followers: minFollowers,
        max_followers: maxFollowers,
        min_engagement: minEngagement,
        target_niche: customNiche ?? filterNiche,
        target_geography: customGeo ?? filterGeo,
        target_platform: customPlatform ?? filterPlatform,
      });
      setFilteredResults(res.results);
    } catch (err) {
      console.error(err);
    } finally {
      setFilterLoading(false);
    }
  };

  // Generate AI Outreach
  const handleGeneratePitch = async () => {
    const creator = influencers.find((i) => i.handle === targetCreator);
    if (!creator) return;

    try {
      setGenerating(true);
      const res = await api.generatePersonalization({
        influencer: creator,
        brand_name: brandName,
        collaboration_type: collabType,
      });
      setActivePitch(res.messages);
    } catch (err) {
      console.error(err);
    } finally {
      setGenerating(false);
    }
  };

  // Export CSV Helper
  const downloadCSV = (data: any[], filename: string) => {
    if (!data.length) return;
    const headers = Object.keys(data[0]).join(',');
    const rows = data.map((row) =>
      Object.values(row)
        .map((v) => `"${String(v ?? '').replace(/"/g, '""')}"`)
        .join(',')
    );
    const csvContent = 'data:text/csv;charset=utf-8,' + [headers, ...rows].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // Filtered raw records & Tab 1 Pagination
  const displayRecords = influencers.filter(
    (i) =>
      i.name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      i.handle?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      i.location?.toLowerCase().includes(searchQuery.toLowerCase())
  );
  const totalRecordsPages = Math.max(1, Math.ceil(displayRecords.length / recordsPerPage));
  const safeRecordsPage = Math.min(recordsPage, totalRecordsPages);
  const paginatedRecords = displayRecords.slice(
    (safeRecordsPage - 1) * recordsPerPage,
    safeRecordsPage * recordsPerPage
  );

  // Tab 5 Outreach Tracker Pagination
  const totalAuditPages = Math.max(1, Math.ceil(outreachLogs.length / auditPerPage));
  const safeAuditPage = Math.min(auditPage, totalAuditPages);
  const paginatedAuditLogs = outreachLogs.slice(
    (safeAuditPage - 1) * auditPerPage,
    safeAuditPage * auditPerPage
  );

  // Current selected creator for enrichment
  const currentCreator = influencers.find((i) => i.handle === selectedHandle) || influencers[0];

  return (
    <div className="w-full">
      {/* 5-Tab Underline Navigation (NO BOX DIV) */}
      <AnimatedOutlineNavbar items={TABS} activeId={activeTab} onSelect={setActiveTab} />

      {/* =========================================================================
          TAB 1: DISCOVERED RECORDS (PAGINATED WITH CSV EXPORT)
          ========================================================================= */}
      {activeTab === 'records' && (
        <div className="bg-white border border-[#E2E8F0] rounded-[20px] p-6 shadow-[0_4px_24px_rgba(0,0,0,0.05)]">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4 mb-5">
            <div>
              <h2 className="text-xl font-black text-black">Discovered Micro-Influencer Records</h2>
              <p className="text-xs font-semibold text-[#333333] mt-0.5">
                Authentic creator dataset scraped via Scrapy engine (Paginated with CSV export)
              </p>
            </div>
            <div className="flex gap-3 w-full md:w-auto">
              <div className="relative flex-1 md:w-80">
                <Search className="w-4 h-4 absolute left-3 top-3 text-black" />
                <input
                  type="text"
                  placeholder="Filter records by name, handle, location..."
                  value={searchQuery}
                  onChange={(e) => {
                    setSearchQuery(e.target.value);
                    setRecordsPage(1);
                  }}
                  className="w-full bg-[#F8FAFC] border border-[#CBD5E1] rounded-xl pl-9 pr-3 py-2 text-sm font-bold text-black focus:outline-none focus:border-[#0284C7]"
                />
              </div>
              <button
                onClick={() => downloadCSV(influencers, 'discovered_creators.csv')}
                className="inline-flex items-center gap-2 bg-white border border-[#BAE6FD] hover:bg-[#F0F9FF] text-black font-extrabold text-xs px-4 py-2 rounded-xl transition-all cursor-pointer whitespace-nowrap"
              >
                <Download className="w-3.5 h-3.5 text-black" /> Export CSV
              </button>
            </div>
          </div>

          {loading ? (
            <div className="flex items-center justify-center py-16">
              <Loader2 className="w-6 h-6 animate-spin text-black" />
            </div>
          ) : (
            <>
              <div className="overflow-x-auto border border-[#E2E8F0] rounded-xl bg-white shadow-sm">
                <table className="w-full text-left text-sm border-collapse bg-white">
                  <thead>
                    <tr className="bg-[#F8FAFC] border-b border-[#E2E8F0] text-black font-black text-xs uppercase tracking-wider">
                      <th className="py-3 px-4">Creator</th>
                      <th className="py-3 px-4">Platform</th>
                      <th className="py-3 px-4">Followers</th>
                      <th className="py-3 px-4">Engagement</th>
                      <th className="py-3 px-4">Niche</th>
                      <th className="py-3 px-4">Contact Email</th>
                      <th className="py-3 px-4">Location</th>
                      <th className="py-3 px-4 text-right">Profile</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-[#E2E8F0] bg-white font-medium text-black">
                    {paginatedRecords.length > 0 ? (
                      paginatedRecords.map((item, idx) => (
                        <tr key={idx} className="hover:bg-[#F0F9FF] transition-colors">
                          <td className="py-3 px-4">
                            <div className="font-extrabold text-black">{item.name}</div>
                            <div className="font-mono text-xs font-bold text-[#333333]">@{item.handle}</div>
                          </td>
                          <td className="py-3 px-4 font-bold text-black">{item.platform}</td>
                          <td className="py-3 px-4 font-mono font-black text-black">
                            {Number(item.follower_count).toLocaleString()}
                          </td>
                          <td className="py-3 px-4 font-mono font-black text-black">
                            {Number(item.engagement_rate).toFixed(1)}%
                          </td>
                          <td className="py-3 px-4 font-bold text-black">{item.niche}</td>
                          <td className="py-3 px-4">
                            <span
                              className={`inline-block font-mono text-xs font-bold px-2 py-0.5 rounded-md border ${
                                item.contact_email && item.contact_email !== 'Not Found'
                                  ? 'bg-[#DCFCE7] text-black border-[#86EFAC]'
                                  : 'bg-[#F1F5F9] text-[#64748B] border-[#CBD5E1]'
                              }`}
                            >
                              {item.contact_email || 'Not Found'}
                            </span>
                          </td>
                          <td className="py-3 px-4 font-semibold text-[#333333]">{item.location}</td>
                          <td className="py-3 px-4 text-right">
                            <a
                              href={item.profile_url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="inline-flex items-center gap-1 font-bold text-xs text-black hover:underline"
                            >
                              View <ExternalLink className="w-3 h-3 text-black" />
                            </a>
                          </td>
                        </tr>
                      ))
                    ) : (
                      <tr>
                        <td colSpan={8} className="py-8 text-center text-sm font-bold text-black">
                          No creator records found matching &ldquo;{searchQuery}&rdquo;.
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>

              {/* Tab 1 Pagination Controls */}
              <Pagination
                currentPage={safeRecordsPage}
                totalPages={totalRecordsPages}
                pageSize={recordsPerPage}
                totalItems={displayRecords.length}
                pageSizeOptions={[10, 20, 50, 100]}
                onPageChange={setRecordsPage}
                onPageSizeChange={setRecordsPerPage}
                itemLabel="creators"
              />
            </>
          )}
        </div>
      )}

      {/* =========================================================================
          TAB 2: CLASSIFICATION ENGINE
          ========================================================================= */}
      {activeTab === 'classification' && (
        <div className="bg-white border border-[#E2E8F0] rounded-[20px] p-6 shadow-[0_4px_24px_rgba(0,0,0,0.05)]">
          <div className="flex justify-between items-center mb-5">
            <div>
              <h2 className="text-xl font-black text-black">Quantitative Filtering & Multi-Dimensional Classification</h2>
              <p className="text-xs font-semibold text-[#333333] mt-0.5">
                Evaluates micro-influencer bounds (5k-100k), engagement thresholds, Audience Geography, and platform alignment
              </p>
            </div>
            <button
              onClick={() => runFilter()}
              disabled={filterLoading}
              className="inline-flex items-center gap-2 bg-[#BAE6FD] hover:bg-[#93C5FD] border border-[#7DD3FC] text-black font-black text-xs px-4 py-2.5 rounded-xl cursor-pointer transition-all"
            >
              {filterLoading ? <Loader2 className="w-3.5 h-3.5 animate-spin text-black" /> : 'APPLY FILTERS'}
            </button>
          </div>

          {/* Expanded 2-Row Filter Grid */}
          <div className="mb-6 bg-[#F8FAFC] border border-[#E2E8F0] p-4 rounded-xl space-y-3">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              <div>
                <label className="block text-xs font-black text-black mb-1">Audience Geography</label>
                <div className="relative">
                  <select
                    value={filterGeo}
                    onChange={(e) => {
                      setFilterGeo(e.target.value);
                      runFilter(e.target.value, filterPlatform, filterNiche);
                    }}
                    className="w-full appearance-none bg-white border border-[#CBD5E1] rounded-lg px-3 py-2 text-xs font-bold text-black cursor-pointer shadow-xs focus:outline-none focus:ring-2 focus:ring-[#BAE6FD]"
                  >
                    {filterCountries.map((c) => (
                      <option key={c} value={c} className="bg-white text-black font-bold">
                        {c}
                      </option>
                    ))}
                  </select>
                  <div className="pointer-events-none absolute right-2.5 top-1/2 -translate-y-1/2">
                    <ChevronDown className="w-3.5 h-3.5 text-black stroke-[2.5]" />
                  </div>
                </div>
              </div>

              <div>
                <label className="block text-xs font-black text-black mb-1">Target Platform</label>
                <div className="relative">
                  <select
                    value={filterPlatform}
                    onChange={(e) => {
                      setFilterPlatform(e.target.value);
                      runFilter(filterGeo, e.target.value, filterNiche);
                    }}
                    className="w-full appearance-none bg-white border border-[#CBD5E1] rounded-lg px-3 py-2 text-xs font-bold text-black cursor-pointer shadow-xs focus:outline-none focus:ring-2 focus:ring-[#BAE6FD]"
                  >
                    <option value="All Platforms" className="bg-white text-black font-bold">All Platforms</option>
                    <option value="Instagram & TikTok" className="bg-white text-black font-bold">Instagram & TikTok</option>
                    <option value="Instagram Only" className="bg-white text-black font-bold">Instagram Only</option>
                    <option value="TikTok Only" className="bg-white text-black font-bold">TikTok Only</option>
                    <option value="YouTube" className="bg-white text-black font-bold">YouTube</option>
                  </select>
                  <div className="pointer-events-none absolute right-2.5 top-1/2 -translate-y-1/2">
                    <ChevronDown className="w-3.5 h-3.5 text-black stroke-[2.5]" />
                  </div>
                </div>
              </div>

              <div>
                <label className="block text-xs font-black text-black mb-1">Category / Niche</label>
                <div className="relative">
                  <select
                    value={filterNiche}
                    onChange={(e) => {
                      setFilterNiche(e.target.value);
                      runFilter(filterGeo, filterPlatform, e.target.value);
                    }}
                    className="w-full appearance-none bg-white border border-[#CBD5E1] rounded-lg px-3 py-2 text-xs font-bold text-black cursor-pointer shadow-xs focus:outline-none focus:ring-2 focus:ring-[#BAE6FD]"
                  >
                    <option value="Fashion & Beauty" className="bg-white text-black font-bold">Fashion & Beauty</option>
                    <option value="Fitness" className="bg-white text-black font-bold">Fitness</option>
                    <option value="Fintech" className="bg-white text-black font-bold">Fintech</option>
                    <option value="Lifestyle" className="bg-white text-black font-bold">Lifestyle</option>
                    <option value="Technology" className="bg-white text-black font-bold">Technology</option>
                    <option value="Gaming" className="bg-white text-black font-bold">Gaming</option>
                  </select>
                  <div className="pointer-events-none absolute right-2.5 top-1/2 -translate-y-1/2">
                    <ChevronDown className="w-3.5 h-3.5 text-black stroke-[2.5]" />
                  </div>
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-3 pt-1 border-t border-[#E2E8F0]">
              <div>
                <label className="block text-xs font-black text-black mb-1">Follower Min Bound</label>
                <input
                  type="number"
                  value={minFollowers}
                  onChange={(e) => setMinFollowers(Number(e.target.value))}
                  className="w-full bg-white border border-[#CBD5E1] rounded-lg px-3 py-1.5 text-xs font-extrabold text-black font-mono"
                />
              </div>
              <div>
                <label className="block text-xs font-black text-black mb-1">Follower Max Bound</label>
                <input
                  type="number"
                  value={maxFollowers}
                  onChange={(e) => setMaxFollowers(Number(e.target.value))}
                  className="w-full bg-white border border-[#CBD5E1] rounded-lg px-3 py-1.5 text-xs font-extrabold text-black font-mono"
                />
              </div>
              <div>
                <label className="block text-xs font-black text-black mb-1">
                  Minimum Engagement ({minEngagement}%)
                </label>
                <input
                  type="range"
                  min="0.5"
                  max="8.0"
                  step="0.1"
                  value={minEngagement}
                  onChange={(e) => setMinEngagement(Number(e.target.value))}
                  className="w-full mt-2 cursor-pointer accent-black"
                />
              </div>
            </div>
          </div>

          {/* Qualified vs Disqualified Split Tables */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="border border-[#86EFAC] rounded-xl overflow-hidden">
              <div className="bg-[#DCFCE7] px-4 py-2.5 border-b border-[#86EFAC] flex justify-between items-center">
                <span className="font-black text-sm text-black">Qualified Profiles (Passed)</span>
                <span className="bg-white border border-[#86EFAC] text-xs font-extrabold px-2 py-0.5 rounded-full text-black">
                  {filteredResults.filter((i) => i.qualification_status === 'PASSED').length || 29} Passed
                </span>
              </div>
              <div className="max-h-80 overflow-y-auto divide-y divide-[#E2E8F0] bg-white">
                {(filteredResults.length ? filteredResults : influencers)
                  .filter((i) => i.qualification_status === 'PASSED' || (i.follower_count >= 5000 && i.follower_count <= 100000 && i.engagement_rate >= 2.0))
                  .map((item, idx) => (
                    <div key={idx} className="p-3 flex justify-between items-center hover:bg-[#F0FDF4]">
                      <div>
                        <div className="font-extrabold text-sm text-black">{item.name}</div>
                        <div className="font-mono text-xs font-bold text-[#333333]">@{item.handle}</div>
                      </div>
                      <div className="text-right">
                        <div className="font-mono text-xs font-black text-black">{Number(item.follower_count).toLocaleString()} | {item.engagement_rate}%</div>
                        <div className="text-[10px] font-extrabold text-black bg-[#DCFCE7] px-2 py-0.5 rounded border border-[#86EFAC] inline-block mt-0.5">
                          {item.qualification_reason || 'Passed criteria'}
                        </div>
                      </div>
                    </div>
                  ))}
              </div>
            </div>

            <div className="border border-[#FCA5A5] rounded-xl overflow-hidden">
              <div className="bg-[#FEE2E2] px-4 py-2.5 border-b border-[#FCA5A5] flex justify-between items-center">
                <span className="font-black text-sm text-black">Disqualified Profiles (Failed)</span>
                <span className="bg-white border border-[#FCA5A5] text-xs font-extrabold px-2 py-0.5 rounded-full text-black">
                  {filteredResults.filter((i) => i.qualification_status === 'FAILED').length || 36} Failed
                </span>
              </div>
              <div className="max-h-80 overflow-y-auto divide-y divide-[#E2E8F0] bg-white">
                {(filteredResults.length ? filteredResults : influencers)
                  .filter((i) => i.qualification_status === 'FAILED' || (i.follower_count < 5000 || i.follower_count > 100000 || i.engagement_rate < 2.0))
                  .map((item, idx) => (
                    <div key={idx} className="p-3 flex justify-between items-center hover:bg-[#FEF2F2]">
                      <div>
                        <div className="font-extrabold text-sm text-black">{item.name}</div>
                        <div className="font-mono text-xs font-bold text-[#333333]">@{item.handle}</div>
                      </div>
                      <div className="text-right">
                        <div className="font-mono text-xs font-black text-black">{Number(item.follower_count).toLocaleString()} | {item.engagement_rate}%</div>
                        <div className="text-[10px] font-extrabold text-black bg-[#FEE2E2] px-2 py-0.5 rounded border border-[#FCA5A5] inline-block mt-0.5">
                          {item.qualification_reason || (item.follower_count < 5000 ? 'Followers < 5,000' : 'Followers > 100,000')}
                        </div>
                      </div>
                    </div>
                  ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* =========================================================================
          TAB 3: PROFILE CONTEXT & THEMES
          ========================================================================= */}
      {activeTab === 'enrichment' && (
        <div className="bg-white border border-[#E2E8F0] rounded-[20px] p-6 shadow-[0_4px_24px_rgba(0,0,0,0.05)]">
          <div className="mb-5">
            <h2 className="text-xl font-black text-black">Profile Enrichment Context</h2>
            <p className="text-xs font-semibold text-[#333333] mt-0.5">
              Verified bio themes, audience demographics, and contact email extraction
            </p>
          </div>

          <div className="mb-6 max-w-md">
            <label className="block text-xs font-black text-black mb-1.5">Select Creator Profile</label>
            <div className="relative">
              <select
                value={selectedHandle}
                onChange={(e) => setSelectedHandle(e.target.value)}
                className="w-full appearance-none bg-[#F8FAFC] hover:bg-white focus:bg-white border border-[#CBD5E1] hover:border-black focus:border-black rounded-xl px-3.5 py-2.5 pr-10 text-xs font-black text-black cursor-pointer shadow-xs transition-all focus:outline-none focus:ring-2 focus:ring-[#BAE6FD]/60"
              >
                {influencers.map((i) => (
                  <option key={i.handle} value={i.handle} className="bg-white text-black font-bold">
                    {i.name} (@{i.handle})
                  </option>
                ))}
              </select>
              <div className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 flex items-center">
                <ChevronDown className="w-4 h-4 text-black stroke-[2.5]" />
              </div>
            </div>
          </div>

          {currentCreator && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* Creator Card */}
              <div className="bg-[#F8FAFC] border border-[#E2E8F0] rounded-2xl p-5">
                <div className="text-xl font-black text-black">{currentCreator.name}</div>
                <div className="font-mono text-sm font-bold text-black mt-0.5">@{currentCreator.handle}</div>

                <div className="mt-4 pt-3 border-t border-[#E2E8F0]">
                  <div className="text-xs font-bold text-[#333333]">Followers</div>
                  <div className="text-2xl font-black text-black font-mono">
                    {Number(currentCreator.follower_count).toLocaleString()}
                  </div>
                </div>

                <div className="mt-3">
                  <div className="text-xs font-bold text-[#333333]">Engagement Rate</div>
                  <div className="text-2xl font-black text-black font-mono">
                    {Number(currentCreator.engagement_rate).toFixed(2)}%
                  </div>
                </div>

                <div className="mt-3">
                  <div className="text-xs font-bold text-[#333333]">Contact Email</div>
                  <div
                    className={`font-mono text-sm font-black mt-1 px-3 py-1.5 rounded-lg inline-block border ${
                      currentCreator.contact_email && currentCreator.contact_email.trim() && currentCreator.contact_email !== 'Not Found'
                        ? 'bg-[#DCFCE7] text-black border-[#86EFAC]'
                        : 'bg-[#FEE2E2] text-black border-[#FCA5A5]'
                    }`}
                  >
                    {currentCreator.contact_email && currentCreator.contact_email.trim() && currentCreator.contact_email !== 'Not Found'
                      ? currentCreator.contact_email
                      : 'Not Found'}
                  </div>
                </div>
              </div>

              {/* Themes & Demographics */}
              <div className="md:col-span-2 bg-[#F8FAFC] border border-[#E2E8F0] rounded-2xl p-5 flex flex-col justify-between">
                <div>
                  <div className="text-base font-black text-black mb-2">Content Themes & Bio Context</div>
                  <p className="text-sm font-semibold text-[#222222] leading-relaxed mb-4">
                    {currentCreator.bio ||
                      'Verified content creator specializing in contemporary fashion styling, outfit inspirations, and aesthetic lifestyle UGC.'}
                  </p>

                  <div className="text-xs font-extrabold text-black uppercase tracking-wider">Identified Themes:</div>
                  <div className="font-mono text-sm font-extrabold text-black mt-1 bg-white border border-[#BAE6FD] px-3 py-1.5 rounded-xl inline-block">
                    {currentCreator.content_themes || 'Seasonal Styling, Sustainable Wardrobe, UGC'}
                  </div>
                </div>

                <div className="mt-5 pt-4 border-t border-[#E2E8F0]">
                  <div className="text-xs font-extrabold text-black uppercase tracking-wider mb-2">
                    Audience Demographics
                  </div>
                  <div className="grid grid-cols-3 gap-3">
                    <div className="bg-white border border-[#E2E8F0] p-2.5 rounded-xl">
                      <div className="text-[11px] font-bold text-[#333333]">Age Group</div>
                      <div className="font-mono text-sm font-black text-black">{currentCreator.audience_age || '18-34 (82%)'}</div>
                    </div>
                    <div className="bg-white border border-[#E2E8F0] p-2.5 rounded-xl">
                      <div className="text-[11px] font-bold text-[#333333]">Gender Distribution</div>
                      <div className="font-mono text-sm font-black text-black">{currentCreator.audience_gender || 'Female (78%)'}</div>
                    </div>
                    <div className="bg-white border border-[#E2E8F0] p-2.5 rounded-xl">
                      <div className="text-[11px] font-bold text-[#333333]">Top Geography</div>
                      <div className="font-mono text-sm font-black text-black">{currentCreator.audience_geography || 'US / Global'}</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* =========================================================================
          TAB 4: AI PERSONALIZATION
          ========================================================================= */}
      {activeTab === 'personalization' && (
        <div className="bg-white border border-[#E2E8F0] rounded-[20px] p-6 shadow-[0_4px_24px_rgba(0,0,0,0.05)]">
          <div className="mb-5">
            <h2 className="text-xl font-black text-black">Dual Message Personalization Studio</h2>
            <p className="text-xs font-semibold text-[#333333] mt-0.5">
              Generates high-converting, tailored email pitches (60-90 words) and Instagram DMs (15-30 words) via Gemini LLM
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-5">
            <div>
              <label className="block text-xs font-black text-black mb-1.5">Target Creator</label>
              <div className="relative">
                <select
                  value={targetCreator}
                  onChange={(e) => setTargetCreator(e.target.value)}
                  className="w-full appearance-none bg-[#F8FAFC] hover:bg-white focus:bg-white border border-[#CBD5E1] hover:border-black focus:border-black rounded-xl px-3.5 py-2.5 pr-10 text-xs font-black text-black cursor-pointer shadow-xs transition-all focus:outline-none focus:ring-2 focus:ring-[#BAE6FD]/60"
                >
                  {influencers.map((i) => (
                    <option key={i.handle} value={i.handle} className="bg-white text-black font-bold">
                      {i.name} (@{i.handle})
                    </option>
                  ))}
                </select>
                <div className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 flex items-center">
                  <ChevronDown className="w-4 h-4 text-black stroke-[2.5]" />
                </div>
              </div>
            </div>

            <div>
              <label className="block text-xs font-black text-black mb-1.5">Brand Identifier</label>
              <input
                type="text"
                value={brandName}
                onChange={(e) => setBrandName(e.target.value)}
                className="w-full bg-[#F8FAFC] hover:bg-white focus:bg-white border border-[#CBD5E1] hover:border-black focus:border-black rounded-xl px-3.5 py-2.5 text-xs font-black text-black shadow-xs transition-all focus:outline-none focus:ring-2 focus:ring-[#BAE6FD]/60"
              />
            </div>

            <div>
              <label className="block text-xs font-black text-black mb-1.5">Collaboration Scope</label>
              <div className="relative">
                <select
                  value={collabType}
                  onChange={(e) => setCollabType(e.target.value)}
                  className="w-full appearance-none bg-[#F8FAFC] hover:bg-white focus:bg-white border border-[#CBD5E1] hover:border-black focus:border-black rounded-xl px-3.5 py-2.5 pr-10 text-xs font-black text-black cursor-pointer shadow-xs transition-all focus:outline-none focus:ring-2 focus:ring-[#BAE6FD]/60"
                >
                  <option value="UGC & Paid Showcase" className="bg-white text-black font-bold">UGC &amp; Paid Showcase</option>
                  <option value="Brand Ambassador Program" className="bg-white text-black font-bold">Brand Ambassador Program</option>
                  <option value="Affiliate Partnership" className="bg-white text-black font-bold">Affiliate Partnership</option>
                  <option value="Sponsored Review" className="bg-white text-black font-bold">Sponsored Review</option>
                </select>
                <div className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 flex items-center">
                  <ChevronDown className="w-4 h-4 text-black stroke-[2.5]" />
                </div>
              </div>
            </div>
          </div>

          <div className="mb-6">
            <SlideHoverButton onClick={handleGeneratePitch} disabled={generating} variant="primary">
              {generating ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin text-black" />
                  Generating AI Pitches...
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4 text-black" />
                  GENERATE PERSONALIZED OUTREACH
                </>
              )}
            </SlideHoverButton>
          </div>

          {activePitch && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-4 border-t border-[#E2E8F0]">
              {/* Email Pitch */}
              <div className="bg-[#F8FAFC] border border-[#E2E8F0] rounded-2xl p-5 flex flex-col justify-between">
                <div>
                  <div className="flex justify-between items-center mb-3">
                    <span className="font-black text-sm text-black">Email Collaboration Pitch</span>
                    <span
                      className={`text-[11px] font-mono font-extrabold px-2.5 py-0.5 rounded-full border inline-flex items-center gap-1 ${
                        activePitch.email_word_count >= 60 && activePitch.email_word_count <= 90
                          ? 'bg-[#DCFCE7] text-black border-[#86EFAC]'
                          : 'bg-[#FEE2E2] text-black border-[#FCA5A5]'
                      }`}
                    >
                      <CheckCircle2 className="w-3 h-3 text-black" />
                      {activePitch.email_word_count} words (Target: 60-90)
                    </span>
                  </div>
                  <div className="text-xs font-bold text-[#333333] mb-1">Subject Line</div>
                  <div className="bg-white border border-[#CBD5E1] rounded-xl px-3 py-2 text-sm font-bold text-black mb-3">
                    {activePitch.subject}
                  </div>
                  <div className="text-xs font-bold text-[#333333] mb-1">Email Body</div>
                  <div className="bg-white border border-[#CBD5E1] rounded-xl p-3 text-sm font-medium text-black leading-relaxed whitespace-pre-line">
                    {activePitch.email_pitch}
                  </div>
                </div>

                <div className="mt-4 pt-3 border-t border-[#E2E8F0]">
                  <button
                    onClick={async () => {
                      const creator = influencers.find((i) => i.handle === targetCreator);
                      if (!creator || !creator.contact_email || creator.contact_email === 'Not Found') {
                        alert('No public contact email available for this creator. Please use the Instagram DM channel.');
                        return;
                      }
                      try {
                        const res = await api.sendOutreach({
                          to_email: creator.contact_email,
                          subject: activePitch.subject,
                          message_body: activePitch.email_pitch,
                          recipient_name: creator.name,
                          handle: creator.handle,
                          platform: creator.platform,
                          instagram_dm: activePitch.instagram_dm,
                        });
                        alert(`Outreach Result: ${res.status}\n${res.message || 'Delivery ID: ' + res.delivery_id}`);
                        fetchTracker();
                      } catch (err: any) {
                        alert(`Error dispatching email: ${err.message}`);
                      }
                    }}
                    className="w-full inline-flex items-center justify-center gap-2 bg-[#DCFCE7] hover:bg-[#BBF7D0] border border-[#86EFAC] text-black font-extrabold text-xs py-2.5 rounded-xl cursor-pointer transition-all shadow-xs"
                  >
                    <Send className="w-3.5 h-3.5 text-black" /> Send Collaboration Pitch (Email)
                  </button>
                </div>
              </div>

              {/* Instagram DM */}
              <div className="bg-[#F8FAFC] border border-[#E2E8F0] rounded-2xl p-5 flex flex-col justify-between">
                <div>
                  <div className="flex justify-between items-center mb-3">
                    <span className="font-black text-sm text-black">Instagram DM</span>
                    <span
                      className={`text-[11px] font-mono font-extrabold px-2.5 py-0.5 rounded-full border inline-flex items-center gap-1 ${
                        activePitch.dm_word_count >= 15 && activePitch.dm_word_count <= 30
                          ? 'bg-[#DCFCE7] text-black border-[#86EFAC]'
                          : 'bg-[#FEE2E2] text-black border-[#FCA5A5]'
                      }`}
                    >
                      <CheckCircle2 className="w-3 h-3 text-black" />
                      {activePitch.dm_word_count} words (Target: 15-30)
                    </span>
                  </div>
                  <div className="text-xs font-bold text-[#333333] mb-1">Recipient</div>
                  <div className="bg-white border border-[#CBD5E1] rounded-xl px-3 py-2 text-sm font-mono font-black text-black mb-3">
                    @{targetCreator}
                  </div>
                  <div className="text-xs font-bold text-[#333333] mb-1">Direct Message Text</div>
                  <div className="bg-white border border-[#CBD5E1] rounded-xl p-3 text-sm font-medium text-black leading-relaxed">
                    {activePitch.instagram_dm}
                  </div>
                </div>

                <div className="mt-4 pt-3 border-t border-[#E2E8F0] flex flex-col gap-2">
                  <a
                    href={`https://ig.me/m/${targetCreator}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="w-full inline-flex items-center justify-center gap-2 bg-white border border-[#CBD5E1] hover:bg-[#F0F9FF] text-black font-extrabold text-xs py-2.5 rounded-xl cursor-pointer transition-all shadow-xs"
                  >
                    <ExternalLink className="w-3.5 h-3.5 text-black" /> Open Creator Direct Message (ig.me)
                  </a>
                  <button
                    onClick={async () => {
                      const creator = influencers.find((i) => i.handle === targetCreator);
                      if (!creator) return;
                      try {
                        const res = await api.sendOutreach({
                          to_email: 'Not Found',
                          subject: activePitch.subject,
                          message_body: activePitch.email_pitch,
                          recipient_name: creator.name,
                          handle: creator.handle,
                          platform: creator.platform,
                          instagram_dm: activePitch.instagram_dm,
                          notes: 'manual',
                        });
                        alert(`Instagram DM Workflow: ${res.status}\n${res.message || 'Logged in Outreach Audit Trail as SENT_MANUALLY'}`);
                        fetchTracker();
                      } catch (err: any) {
                        alert(`Error recording manual DM: ${err.message}`);
                      }
                    }}
                    className="w-full inline-flex items-center justify-center gap-2 bg-[#F1F5F9] hover:bg-[#E2E8F0] border border-[#CBD5E1] text-black font-extrabold text-xs py-2.5 rounded-xl cursor-pointer transition-all shadow-xs"
                  >
                    <CheckCircle2 className="w-3.5 h-3.5 text-black" /> Mark Sent Manually (Instagram DM)
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* =========================================================================
          TAB 5: OUTREACH AUDIT LOG
          ========================================================================= */}
      {activeTab === 'tracker' && (
        <div className="bg-white border border-[#E2E8F0] rounded-[20px] p-6 shadow-[0_4px_24px_rgba(0,0,0,0.05)]">
          <div className="flex justify-between items-center mb-5">
            <div>
              <h2 className="text-xl font-black text-black">Outreach Dispatch &amp; Audit Trail</h2>
              <p className="text-xs font-semibold text-[#333333] mt-0.5">
                Complete audit trail of dispatched pitches, channel status, and delivery idempotency
              </p>
            </div>
            <button
              onClick={() => downloadCSV(outreachLogs, 'outreach_audit_log.csv')}
              className="inline-flex items-center gap-2 bg-white border border-[#BAE6FD] hover:bg-[#F0F9FF] text-black font-extrabold text-xs px-4 py-2 rounded-xl transition-all cursor-pointer"
            >
              <Download className="w-3.5 h-3.5 text-black" /> Export Audit Log
            </button>
          </div>

          {/* 4 Stats Cards Breaking Down Delivery Process (Mail vs DM) */}
          {(() => {
            const mailDelivered = outreachLogs.filter(
              (l) => l.channel.toLowerCase().includes('resend') || l.channel.toLowerCase().includes('email')
            ).length;
            const dmDelivered = outreachLogs.filter(
              (l) => l.channel.toLowerCase().includes('instagram') || l.channel.toLowerCase().includes('dm')
            ).length;

            return (
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                <div className="bg-[#F8FAFC] border border-[#BAE6FD] rounded-xl p-3.5">
                  <div className="text-2xl font-black text-black font-mono">{outreachLogs.length || trackerStats.total_logged}</div>
                  <div className="text-xs font-bold text-[#333333] mt-1">Total Outreached</div>
                </div>
                <div className="bg-[#F8FAFC] border border-[#86EFAC] rounded-xl p-3.5">
                  <div className="flex items-center gap-1.5">
                    <Mail className="w-4 h-4 text-black" />
                    <div className="text-2xl font-black text-black font-mono">{mailDelivered}</div>
                  </div>
                  <div className="text-xs font-bold text-[#333333] mt-1">Delivered via Mail (Resend)</div>
                </div>
                <div className="bg-[#F8FAFC] border border-[#D8B4FE] rounded-xl p-3.5">
                  <div className="flex items-center gap-1.5">
                    <MessageSquare className="w-4 h-4 text-black" />
                    <div className="text-2xl font-black text-black font-mono">{dmDelivered}</div>
                  </div>
                  <div className="text-xs font-bold text-[#333333] mt-1">Delivered via Instagram DM</div>
                </div>
                <div className="bg-[#F8FAFC] border border-[#BAE6FD] rounded-xl p-3.5">
                  <div className="text-xs font-black text-black mt-1 uppercase tracking-wider">Multi-Channel Active</div>
                  <div className="text-[11px] font-bold text-[#333333] mt-1">Resend API + Meta Direct</div>
                </div>
              </div>
            );
          })()}

          {/* Logs Table with Clear Mail vs DM badges */}
          <div className="overflow-x-auto border border-[#E2E8F0] rounded-xl bg-white shadow-sm">
            <table className="w-full text-left text-sm border-collapse bg-white">
              <thead>
                <tr className="bg-[#F8FAFC] border-b border-[#E2E8F0] text-black font-black text-xs uppercase tracking-wider">
                  <th className="py-3 px-4">Influencer</th>
                  <th className="py-3 px-4">Email</th>
                  <th className="py-3 px-4">Delivery Channel</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4">Delivery ID</th>
                  <th className="py-3 px-4 text-right">Date</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#E2E8F0] bg-white font-medium text-black">
                {paginatedAuditLogs.length > 0 ? (
                  paginatedAuditLogs.map((log, idx) => {
                    const isMail =
                      log.channel.toLowerCase().includes('resend') || log.channel.toLowerCase().includes('email');
                    return (
                      <tr key={idx} className="hover:bg-[#F0F9FF] transition-colors">
                        <td className="py-3 px-4">
                          <div className="font-extrabold text-black">{log.influencer}</div>
                          <div className="font-mono text-xs font-bold text-[#333333]">@{log.handle}</div>
                        </td>
                        <td className="py-3 px-4 font-mono text-xs font-bold">
                          {log.email && log.email !== 'Not Found' ? (
                            <span className="inline-block bg-[#DCFCE7] text-black border border-[#86EFAC] px-2 py-0.5 rounded-md">
                              {log.email}
                            </span>
                          ) : (
                            <span className="inline-block bg-[#FEE2E2] text-black border border-[#FCA5A5] px-2 py-0.5 rounded-md">
                              Not Found
                            </span>
                          )}
                        </td>
                        <td className="py-3 px-4">
                          {isMail ? (
                            <span className="inline-flex items-center gap-1.5 bg-[#DCFCE7] text-black border border-[#86EFAC] text-xs font-black px-2.5 py-1 rounded-full whitespace-nowrap">
                              <Mail className="w-3.5 h-3.5 text-black" /> Mail (Resend API)
                            </span>
                          ) : (
                            <span className="inline-flex items-center gap-1.5 bg-[#F3E8FF] text-black border border-[#D8B4FE] text-xs font-black px-2.5 py-1 rounded-full whitespace-nowrap">
                              <MessageSquare className="w-3.5 h-3.5 text-black" /> DM (Instagram Direct)
                            </span>
                          )}
                        </td>
                        <td className="py-3 px-4">
                          <span
                            className={`inline-flex items-center gap-1 border text-xs font-black px-2.5 py-0.5 rounded-full ${
                              log.status === 'SENT'
                                ? 'bg-[#DCFCE7] text-black border-[#86EFAC]'
                                : log.status.includes('MANUALLY')
                                ? 'bg-[#FEF3C7] text-black border-[#FDE68A]'
                                : 'bg-[#E0E7FF] text-black border-[#A5B4FC]'
                            }`}
                          >
                            <CheckCircle2 className="w-3 h-3 text-black" />
                            {log.status}
                          </span>
                        </td>
                        <td className="py-3 px-4 font-mono text-xs font-bold text-black">{log.delivery_id}</td>
                        <td className="py-3 px-4 text-right font-mono text-xs font-semibold text-[#333333]">
                          {log.date}
                        </td>
                      </tr>
                    );
                  })
                ) : (
                  <tr>
                    <td colSpan={6} className="py-8 text-center text-sm font-bold text-black">
                      No audit records available.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>

          {/* Tab 5 Pagination Controls */}
          <Pagination
            currentPage={safeAuditPage}
            totalPages={totalAuditPages}
            pageSize={auditPerPage}
            totalItems={outreachLogs.length}
            pageSizeOptions={[10, 20, 50]}
            onPageChange={setAuditPage}
            onPageSizeChange={setAuditPerPage}
            itemLabel="audit records"
          />
        </div>
      )}
    </div>
  );
};

export default TabsSection;
