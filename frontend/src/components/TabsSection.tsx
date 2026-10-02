import React, { useState, useEffect } from 'react';
import { Search, Download, Sparkles, Send, ExternalLink, Loader2, ChevronDown, CheckCircle2, XCircle, Mail, MessageSquare, Globe, Tag, Smartphone, Users, MapPin, X, AlertCircle } from 'lucide-react';
import AnimatedOutlineNavbar, { type TabItem } from './ui/AnimatedOutlineNavbar';
import SlideHoverButton from './ui/SlideHoverButton';
import Pagination from './ui/Pagination';
import type { FilterState } from './DashboardControlCard';
import { api, type Influencer, type PersonalizedPitch, type OutreachRecord, type TrackerStats } from '../services/api';

const TABS: TabItem[] = [
  { id: 'records', label: 'Discovered Records' },
  { id: 'classification', label: 'Classification Engine' },
  { id: 'enrichment', label: 'Profile Context & Themes' },
  { id: 'personalization', label: 'AI Personalization' },
  { id: 'tracker', label: 'Outreach Audit Log' },
];

export interface TabsSectionProps {
  filters: FilterState;
  onFilterChange: (updates: Partial<FilterState>) => void;
  filteredResults: Influencer[];
  passedInfluencers: Influencer[];
  failedInfluencers: Influencer[];
  filterLoading: boolean;
  onRunFilter: (overrideFilters?: Partial<FilterState>) => Promise<void>;
  countries: string[];
  allInfluencers: Influencer[];
  onRefreshTracker?: () => void;
}

export const TabsSection: React.FC<TabsSectionProps> = ({
  filters,
  onFilterChange,
  filteredResults,
  passedInfluencers,
  failedInfluencers,
  filterLoading,
  onRunFilter,
  countries,
  allInfluencers,
  onRefreshTracker,
}) => {
  const [activeTab, setActiveTab] = useState('records');

  // Tab 1 Local State
  const [searchQuery, setSearchQuery] = useState('');
  const [recordsPage, setRecordsPage] = useState(1);
  const [recordsPerPage, setRecordsPerPage] = useState(10);
  const [dashboardFilterEnabled, setDashboardFilterEnabled] = useState(true);

  // Tab 3 & 4 State
  const [selectedHandle, setSelectedHandle] = useState<string>('');
  const [targetCreator, setTargetCreator] = useState<string>('');
  const [brandName, setBrandName] = useState('LumiGlow');
  const [collabType, setCollabType] = useState('UGC & Paid Showcase');
  const [generating, setGenerating] = useState(false);
  const [activePitch, setActivePitch] = useState<PersonalizedPitch | null>(null);

  // Tab 5 Outreach Tracker State
  const [trackerStats, setTrackerStats] = useState<TrackerStats>({ total_logged: 173, successfully_sent: 128, skipped: 45 });
  const [outreachLogs, setOutreachLogs] = useState<OutreachRecord[]>([]);
  const [auditPage, setAuditPage] = useState(1);
  const [auditPerPage, setAuditPerPage] = useState(10);

  // Tab 1 Direct Outreach Messaging State
  const [directOutreachCreator, setDirectOutreachCreator] = useState<Influencer | null>(null);
  const [directSubject, setDirectSubject] = useState('');
  const [directBody, setDirectBody] = useState('');
  const [directChannel, setDirectChannel] = useState<'Email' | 'Instagram Direct'>('Email');
  const [directSending, setDirectSending] = useState(false);
  const [directGenerating, setDirectGenerating] = useState(false);
  const [directStatusNotice, setDirectStatusNotice] = useState<{ type: 'success' | 'error' | 'info'; message: string } | null>(null);
  const [contactedHandles, setContactedHandles] = useState<Set<string>>(new Set());

  // Fetch Outreach tracker data on mount
  useEffect(() => {
    fetchTracker();
  }, []);

  const fetchTracker = async () => {
    try {
      const res = await api.getTrackerStats();
      setTrackerStats(res.stats);
      setOutreachLogs(res.logs);
      if (res.logs && res.logs.length > 0) {
        const handles = new Set<string>();
        res.logs.forEach((l) => {
          if (l.handle) handles.add(l.handle.replace('@', '').toLowerCase());
        });
        setContactedHandles(handles);
      }
      if (onRefreshTracker) onRefreshTracker();
    } catch (err) {
      console.error(err);
    }
  };

  const handleOpenDirectOutreach = (creator: Influencer) => {
    setDirectOutreachCreator(creator);
    setDirectStatusNotice(null);
    const hasEmail = Boolean(creator.contact_email && creator.contact_email !== 'Not Found');
    const channel = hasEmail ? 'Email' : 'Instagram Direct';
    setDirectChannel(channel);

    const firstName = creator.name.split(' ')[0] || creator.name;
    const nicheTag = creator.niche || 'Fashion & Beauty';

    if (channel === 'Email') {
      setDirectSubject(`Collaboration Opportunity: LumiGlow x ${creator.name}`);
      setDirectBody(
        `Hi ${firstName},\n\nWe love your creative content in ${nicheTag} and your authentic audience engagement! At LumiGlow, we develop clean, high-performance skincare essentials, and we'd love to partner with you for an authentic showcase. We offer gifted PR packages along with competitive compensation per deliverable. Let us know if you're open to collaborating, and we'll send our campaign brief right over!`
      );
    } else {
      setDirectSubject(`Instagram Direct Outreach to @${creator.handle}`);
      setDirectBody(
        `Hey ${firstName}! Love your ${nicheTag} posts. We'd love to collaborate with you on our upcoming LumiGlow campaign. Mind if we send over the brief?`
      );
    }
  };

  const handleGenerateAIDirectPitch = async () => {
    if (!directOutreachCreator) return;
    try {
      setDirectGenerating(true);
      const res = await api.generatePersonalization({
        influencer: directOutreachCreator,
        brand_name: 'LumiGlow',
        collaboration_type: 'UGC & Paid Showcase',
      });
      if (res.messages) {
        if (directChannel === 'Email') {
          setDirectSubject(res.messages.subject);
          setDirectBody(res.messages.email_pitch);
        } else {
          setDirectBody(res.messages.instagram_dm);
        }
        setDirectStatusNotice({ type: 'info', message: 'Pitch hyper-personalized with Google Gemini!' });
      }
    } catch (e: any) {
      setDirectStatusNotice({ type: 'error', message: 'Failed to generate pitch. Using default template.' });
    } finally {
      setDirectGenerating(false);
    }
  };

  const handleDispatchDirectOutreach = async () => {
    if (!directOutreachCreator) return;
    try {
      setDirectSending(true);
      setDirectStatusNotice(null);

      const hasEmail = Boolean(
        directOutreachCreator.contact_email && directOutreachCreator.contact_email !== 'Not Found'
      );
      const emailToSend = directChannel === 'Email' && hasEmail ? directOutreachCreator.contact_email! : 'Not Found';

      const res = await api.sendOutreach({
        to_email: emailToSend,
        subject: directSubject || `Partnership Opportunity with LumiGlow`,
        message_body: directBody,
        recipient_name: directOutreachCreator.name,
        handle: directOutreachCreator.handle,
        platform: directOutreachCreator.platform,
        instagram_dm: directBody,
        notes: `Dispatched directly via Discovered Records table (${directChannel})`,
      });

      if (res.status === 'SKIPPED') {
        setDirectStatusNotice({ type: 'info', message: res.message || 'Already contacted. Duplicate prevented.' });
      } else {
        setDirectStatusNotice({
          type: 'success',
          message: `Outreach dispatched successfully via ${res.channel}! Delivery ID: ${
            res.delivery_id || 'sim_' + Date.now()
          }`,
        });

        // Mark creator as contacted
        setContactedHandles((prev) => new Set(prev).add(directOutreachCreator.handle.replace('@', '').toLowerCase()));

        // Refresh tracker in background
        await fetchTracker();
        if (onRefreshTracker) onRefreshTracker();

        // Close after a brief moment
        setTimeout(() => {
          setDirectOutreachCreator(null);
          setDirectStatusNotice(null);
        }, 1800);
      }
    } catch (e: any) {
      setDirectStatusNotice({ type: 'error', message: e.message || 'Failed to dispatch outreach' });
    } finally {
      setDirectSending(false);
    }
  };

  // Set default selected creator when dataset updates
  useEffect(() => {
    const list = passedInfluencers.length > 0 ? passedInfluencers : filteredResults;
    if (list.length > 0) {
      if (!selectedHandle || !list.some((c) => c.handle === selectedHandle)) {
        setSelectedHandle(list[0].handle);
      }
      if (!targetCreator || !list.some((c) => c.handle === targetCreator)) {
        setTargetCreator(list[0].handle);
      }
    }
  }, [passedInfluencers, filteredResults]);

  // Tab 1 Filter Mode: 'qualified' (strict criteria) | 'region' (all in target country) | 'all' (all database)
  const [recordsFilterMode, setRecordsFilterMode] = useState<'qualified' | 'region' | 'all'>('qualified');

  const isGlobal = !filters.geo || filters.geo.toLowerCase().includes('global') || filters.geo.toLowerCase().includes('all');
  const geoMatchedList = isGlobal
    ? filteredResults
    : filteredResults.filter(
        (r) => !r.qualification_reason || !r.qualification_reason.includes('does not match target')
      );

  let activeSourceList = allInfluencers;
  if (recordsFilterMode === 'qualified') {
    activeSourceList = passedInfluencers.length > 0 ? passedInfluencers : (geoMatchedList.length > 0 ? geoMatchedList : filteredResults);
  } else if (recordsFilterMode === 'region') {
    activeSourceList = geoMatchedList.length > 0 ? geoMatchedList : filteredResults;
  } else {
    activeSourceList = allInfluencers.length > 0 ? allInfluencers : filteredResults;
  }

  const displayRecords = activeSourceList.filter((item) => {
    if (!searchQuery) return true;
    const q = searchQuery.toLowerCase().trim();
    return (
      (item.name || '').toLowerCase().includes(q) ||
      (item.handle || '').toLowerCase().includes(q) ||
      (item.location || '').toLowerCase().includes(q) ||
      (item.niche || '').toLowerCase().includes(q)
    );
  });

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

  // Current creator for Tab 3 & 4
  const eligibleCreators = passedInfluencers.length > 0 ? passedInfluencers : filteredResults.length > 0 ? filteredResults : allInfluencers;
  const currentCreator = eligibleCreators.find((i) => i.handle === selectedHandle) || eligibleCreators[0];

  // Generate AI Outreach
  const handleGeneratePitch = async () => {
    const creator = eligibleCreators.find((i) => i.handle === targetCreator);
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

  return (
    <div className="space-y-6">
      {/* 1. Header Navigation Bar (Underline Animated Tabs) */}
      <div className="w-full overflow-x-auto no-scrollbar pb-1">
        <AnimatedOutlineNavbar items={TABS} activeId={activeTab} onSelect={setActiveTab} />
      </div>

      {/* =========================================================================
          TAB 1: DISCOVERED RECORDS
          ========================================================================= */}
      {activeTab === 'records' && (
        <div className="bg-white border border-[#E2E8F0] rounded-[20px] p-6 shadow-[0_4px_24px_rgba(0,0,0,0.05)]">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-5">
            <div>
              <h2 className="text-xl font-black text-black">Discovered Micro-Influencer Records</h2>
              <p className="text-xs font-semibold text-[#333333] mt-0.5">
                Targeted creator dataset scraped and synchronized with indexed database
              </p>
            </div>

            <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-2 sm:gap-3 w-full sm:w-auto">
              <div className="relative w-full sm:w-auto">
                <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-black stroke-[2.5]" />
                <input
                  type="text"
                  placeholder="Search name, handle, location..."
                  value={searchQuery}
                  onChange={(e) => {
                    setSearchQuery(e.target.value);
                    setRecordsPage(1);
                  }}
                  className="bg-[#F8FAFC] border border-[#CBD5E1] rounded-xl pl-9 pr-3.5 py-2 text-xs font-bold text-black focus:outline-none focus:border-black focus:bg-white w-full sm:w-64 shadow-xs"
                />
              </div>
              <button
                onClick={() => downloadCSV(displayRecords, 'discovered_influencers.csv')}
                className="inline-flex items-center justify-center gap-2 bg-white border border-[#CBD5E1] hover:border-black hover:bg-[#F8FAFC] text-black font-extrabold text-xs px-3.5 py-2 rounded-xl transition-all cursor-pointer shadow-xs shrink-0"
              >
                <Download className="w-3.5 h-3.5 text-black stroke-[2.5]" /> Export
              </button>
            </div>
          </div>

          {filterLoading ? (
            <div className="flex items-center justify-center py-16">
              <Loader2 className="w-6 h-6 animate-spin text-black" />
            </div>
          ) : (
            <>
              {/* Active Dashboard Filter Banner */}
              <div className="flex flex-wrap items-center justify-between gap-3 mb-4 bg-[#F8FAFC] border border-[#CBD5E1] p-3 rounded-xl">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="text-xs font-black text-black">Active Filter:</span>
                  <span className="inline-flex items-center gap-1.5 bg-white border border-[#94A3B8] text-xs font-black px-2.5 py-1 rounded-md text-black shadow-xs">
                    <Globe className="w-3.5 h-3.5 text-black" />
                    <span>{filters.geo}</span>
                  </span>
                  <span className="inline-flex items-center gap-1.5 bg-white border border-[#94A3B8] text-xs font-black px-2.5 py-1 rounded-md text-black shadow-xs">
                    <Tag className="w-3.5 h-3.5 text-black" />
                    <span>{filters.niche}</span>
                  </span>
                  {filters.platform !== 'All Platforms' && filters.platform !== 'Instagram & TikTok' && (
                    <span className="inline-flex items-center gap-1.5 bg-white border border-[#94A3B8] text-xs font-black px-2.5 py-1 rounded-md text-black shadow-xs">
                      <Smartphone className="w-3.5 h-3.5 text-black" />
                      <span>{filters.platform}</span>
                    </span>
                  )}
                  <span className="inline-flex items-center gap-1.5 bg-white border border-[#94A3B8] text-xs font-black px-2.5 py-1 rounded-md text-black shadow-xs">
                    <Users className="w-3.5 h-3.5 text-black" />
                    <span>{filters.scale.replace(/\(.*\)/, '').trim()}</span>
                  </span>
                </div>

                <div className="flex flex-wrap items-center gap-2">
                  <span className="text-xs font-black text-black">
                    Showing <span className="text-[#0284C7] font-mono text-sm">{displayRecords.length}</span> creators:
                  </span>
                  
                  <div className="inline-flex items-center gap-1 bg-[#F1F5F9] p-1 rounded-xl border border-[#CBD5E1]">
                    <button
                      type="button"
                      onClick={() => {
                        setRecordsFilterMode('qualified');
                        setRecordsPage(1);
                      }}
                      className={`px-2.5 py-1 text-[11px] font-black rounded-lg transition-all cursor-pointer ${
                        recordsFilterMode === 'qualified'
                          ? 'bg-white text-black shadow-xs border border-[#94A3B8]'
                          : 'text-[#475569] hover:text-black'
                      }`}
                    >
                      Qualified ({passedInfluencers.length})
                    </button>
                    {!isGlobal && (
                      <button
                        type="button"
                        onClick={() => {
                          setRecordsFilterMode('region');
                          setRecordsPage(1);
                        }}
                        className={`px-2.5 py-1 text-[11px] font-black rounded-lg transition-all cursor-pointer ${
                          recordsFilterMode === 'region'
                            ? 'bg-white text-black shadow-xs border border-[#94A3B8]'
                            : 'text-[#475569] hover:text-black'
                        }`}
                      >
                        All in {filters.geo.replace(/\(.*\)/, '').trim()} ({geoMatchedList.length})
                      </button>
                    )}
                    <button
                      type="button"
                      onClick={() => {
                        setRecordsFilterMode('all');
                        setRecordsPage(1);
                      }}
                      className={`px-2.5 py-1 text-[11px] font-black rounded-lg transition-all cursor-pointer ${
                        recordsFilterMode === 'all'
                          ? 'bg-white text-black shadow-xs border border-[#94A3B8]'
                          : 'text-[#475569] hover:text-black'
                      }`}
                    >
                      All Database ({allInfluencers.length || filteredResults.length})
                    </button>
                  </div>
                </div>
              </div>

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
                      <th className="py-3 px-4 text-center">Profile</th>
                      <th className="py-3 px-4 text-right">Outreach</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-[#E2E8F0] bg-white font-medium text-black">
                    {paginatedRecords.length > 0 ? (
                      paginatedRecords.map((item, idx) => {
                        const isContacted = contactedHandles.has((item.handle || '').replace('@', '').toLowerCase());
                        return (
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
                            <td className="py-3 px-4 text-center">
                              <a
                                href={item.profile_url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="inline-flex items-center gap-1 font-bold text-xs text-black hover:underline"
                              >
                                View <ExternalLink className="w-3 h-3 text-black" />
                              </a>
                            </td>
                            <td className="py-3 px-4 text-right whitespace-nowrap">
                              <button
                                type="button"
                                onClick={() => handleOpenDirectOutreach(item)}
                                className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-black transition-all cursor-pointer border shadow-xs ${
                                  isContacted
                                    ? 'bg-[#DCFCE7] text-black border-[#86EFAC] hover:bg-[#BBF7D0]'
                                    : 'bg-black text-white border-black hover:bg-[#1E293B]'
                                }`}
                                title={`Send personalized pitch to ${item.name}`}
                              >
                                {isContacted ? (
                                  <>
                                    <CheckCircle2 className="w-3.5 h-3.5 text-black" />
                                    <span>Contacted</span>
                                  </>
                                ) : (
                                  <>
                                    <Send className="w-3.5 h-3.5 text-white" />
                                    <span>Send Message</span>
                                  </>
                                )}
                              </button>
                            </td>
                          </tr>
                        );
                      })
                    ) : (
                      <tr>
                        <td colSpan={9} className="py-10 text-center text-sm font-bold text-black">
                          <div>
                            No creator records found matching {dashboardFilterEnabled ? `active filter "${filters.geo}"` : ''}{searchQuery ? ` and search "${searchQuery}"` : ''}.
                          </div>
                          {dashboardFilterEnabled && (
                            <div className="mt-3">
                              <button
                                onClick={() => setDashboardFilterEnabled(false)}
                                className="text-xs font-black text-black underline bg-[#F1F5F9] px-3 py-1.5 rounded-lg border border-[#CBD5E1]"
                              >
                                View full unfiltered dataset ({allInfluencers.length} creators)
                              </button>
                            </div>
                          )}
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

              {/* Direct Outreach Dispatch Modal */}
              {directOutreachCreator && (
                <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-xs flex items-center justify-center p-4">
                  <div className="bg-white border border-[#CBD5E1] rounded-2xl max-w-lg w-full p-5 sm:p-6 shadow-2xl relative max-h-[92vh] overflow-y-auto">
                    {/* Header */}
                    <div className="flex items-start justify-between gap-3 border-b border-[#E2E8F0] pb-3 mb-4">
                      <div>
                        <div className="flex items-center gap-2 mb-1">
                          <span className="text-[10px] font-black uppercase tracking-wider text-black bg-[#E0F2FE] border border-[#BAE6FD] px-2 py-0.5 rounded-full">
                            Direct Outreach Dispatch
                          </span>
                        </div>
                        <h3 className="text-lg font-black text-black">
                          Send Message to {directOutreachCreator.name}
                        </h3>
                        <div className="font-mono text-xs font-bold text-[#64748B] flex items-center gap-2 mt-0.5">
                          <span>@{directOutreachCreator.handle}</span>
                          <span>•</span>
                          <span>{directOutreachCreator.platform}</span>
                          <span>•</span>
                          <span>{Number(directOutreachCreator.follower_count).toLocaleString()} followers</span>
                        </div>
                      </div>
                      <button
                        type="button"
                        onClick={() => setDirectOutreachCreator(null)}
                        className="text-[#64748B] hover:text-black p-1.5 rounded-lg hover:bg-[#F1F5F9] transition-all cursor-pointer"
                      >
                        <X className="w-5 h-5" />
                      </button>
                    </div>

                    {/* Delivery Channel Switcher */}
                    <div className="mb-4">
                      <label className="block text-xs font-black text-black mb-1.5">Delivery Channel</label>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                        <button
                          type="button"
                          onClick={() => setDirectChannel('Email')}
                          className={`flex items-center justify-center gap-1.5 py-2 px-3 rounded-xl border text-xs font-black transition-all cursor-pointer ${
                            directChannel === 'Email'
                              ? 'bg-white text-black border-black shadow-xs ring-2 ring-[#BAE6FD]/60'
                              : 'bg-[#F8FAFC] text-[#64748B] border-[#CBD5E1] hover:text-black'
                          }`}
                        >
                          <Mail className="w-3.5 h-3.5" />
                          <span className="truncate">
                            Email ({directOutreachCreator.contact_email && directOutreachCreator.contact_email !== 'Not Found' ? directOutreachCreator.contact_email : 'Not Found'})
                          </span>
                        </button>
                        <button
                          type="button"
                          onClick={() => setDirectChannel('Instagram Direct')}
                          className={`flex items-center justify-center gap-1.5 py-2 px-3 rounded-xl border text-xs font-black transition-all cursor-pointer ${
                            directChannel === 'Instagram Direct'
                              ? 'bg-white text-black border-black shadow-xs ring-2 ring-[#BAE6FD]/60'
                              : 'bg-[#F8FAFC] text-[#64748B] border-[#CBD5E1] hover:text-black'
                          }`}
                        >
                          <MessageSquare className="w-3.5 h-3.5" />
                          <span className="truncate">Instagram DM (@{directOutreachCreator.handle})</span>
                        </button>
                      </div>
                    </div>

                    {/* Subject Line (for Email) */}
                    {directChannel === 'Email' && (
                      <div className="mb-3">
                        <label className="block text-xs font-black text-black mb-1">Subject Line</label>
                        <input
                          type="text"
                          value={directSubject}
                          onChange={(e) => setDirectSubject(e.target.value)}
                          className="w-full bg-[#F8FAFC] focus:bg-white border border-[#CBD5E1] focus:border-black rounded-xl px-3.5 py-2 text-xs font-bold text-black focus:outline-none transition-all"
                          placeholder="Subject line..."
                        />
                      </div>
                    )}

                    {/* Message Body */}
                    <div className="mb-4">
                      <div className="flex justify-between items-center mb-1">
                        <label className="text-xs font-black text-black">
                          {directChannel === 'Email' ? 'Collaboration Email Pitch' : 'Instagram DM Message'}
                        </label>
                        <span className="text-[11px] font-mono font-bold text-[#64748B]">
                          {directBody.trim() ? directBody.trim().split(/\s+/).length : 0} words
                        </span>
                      </div>
                      <textarea
                        rows={5}
                        value={directBody}
                        onChange={(e) => setDirectBody(e.target.value)}
                        className="w-full bg-[#F8FAFC] focus:bg-white border border-[#CBD5E1] focus:border-black rounded-xl p-3 text-xs font-medium text-black focus:outline-none leading-relaxed transition-all"
                        placeholder="Compose your personalized pitch..."
                      />
                    </div>

                    {/* Status Notice */}
                    {directStatusNotice && (
                      <div
                        className={`mb-4 p-3 rounded-xl text-xs font-bold border flex items-start gap-2 ${
                          directStatusNotice.type === 'success'
                            ? 'bg-[#DCFCE7] text-black border-[#86EFAC]'
                            : directStatusNotice.type === 'error'
                            ? 'bg-[#FEE2E2] text-black border-[#FCA5A5]'
                            : 'bg-[#E0F2FE] text-black border-[#BAE6FD]'
                        }`}
                      >
                        {directStatusNotice.type === 'success' ? (
                          <CheckCircle2 className="w-4 h-4 shrink-0 text-black" />
                        ) : (
                          <AlertCircle className="w-4 h-4 shrink-0 text-black" />
                        )}
                        <span>{directStatusNotice.message}</span>
                      </div>
                    )}

                    {/* Actions */}
                    <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-2.5 pt-3 border-t border-[#E2E8F0]">
                      <button
                        type="button"
                        onClick={handleGenerateAIDirectPitch}
                        disabled={directGenerating}
                        className="inline-flex items-center justify-center gap-1.5 px-3 py-2 bg-[#F8FAFC] hover:bg-white border border-[#CBD5E1] hover:border-black text-xs font-black text-black rounded-xl transition-all cursor-pointer"
                      >
                        {directGenerating ? (
                          <>
                            <Loader2 className="w-3.5 h-3.5 animate-spin text-black" />
                            <span>Personalizing...</span>
                          </>
                        ) : (
                          <>
                            <Sparkles className="w-3.5 h-3.5 text-black" />
                            <span>Regenerate with Gemini AI</span>
                          </>
                        )}
                      </button>

                      <div className="flex items-center justify-end gap-2">
                        <button
                          type="button"
                          onClick={() => setDirectOutreachCreator(null)}
                          className="px-3.5 py-2 text-xs font-black text-[#64748B] hover:text-black rounded-xl hover:bg-[#F1F5F9] transition-all cursor-pointer"
                        >
                          Cancel
                        </button>
                        <button
                          type="button"
                          onClick={handleDispatchDirectOutreach}
                          disabled={directSending}
                          className="inline-flex items-center justify-center gap-1.5 px-4 py-2 bg-black hover:bg-[#1E293B] text-white text-xs font-black rounded-xl transition-all cursor-pointer shadow-xs disabled:opacity-50"
                        >
                          {directSending ? (
                            <>
                              <Loader2 className="w-3.5 h-3.5 animate-spin text-white" />
                              <span>Dispatching...</span>
                            </>
                          ) : (
                            <>
                              <Send className="w-3.5 h-3.5 text-white" />
                              <span>{directChannel === 'Email' ? 'Send Email via Resend' : 'Dispatch Instagram DM'}</span>
                            </>
                          )}
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              )}
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
              onClick={() => onRunFilter()}
              disabled={filterLoading}
              className="inline-flex items-center gap-2 bg-[#BAE6FD] hover:bg-[#93C5FD] border border-[#7DD3FC] text-black font-black text-xs px-4 py-2.5 rounded-xl cursor-pointer transition-all"
            >
              {filterLoading ? <Loader2 className="w-3.5 h-3.5 animate-spin text-black" /> : 'APPLY FILTERS'}
            </button>
          </div>

          {/* Unified 2-Row Filter Grid (Controlled via Single Source of Truth) */}
          <div className="mb-6 bg-[#F8FAFC] border border-[#E2E8F0] p-4 rounded-xl space-y-3">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              <div>
                <label className="block text-xs font-black text-black mb-1">Audience Geography</label>
                <div className="relative">
                  <select
                    value={filters.geo}
                    onChange={(e) => onFilterChange({ geo: e.target.value })}
                    className="w-full appearance-none bg-white border border-[#CBD5E1] rounded-lg px-3 py-2 text-xs font-bold text-black cursor-pointer shadow-xs focus:outline-none focus:ring-2 focus:ring-[#BAE6FD]"
                  >
                    {countries.map((c) => (
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
                    value={filters.platform}
                    onChange={(e) => onFilterChange({ platform: e.target.value })}
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
                    value={filters.niche}
                    onChange={(e) => onFilterChange({ niche: e.target.value })}
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
                  value={filters.minFollowers}
                  onChange={(e) => onFilterChange({ minFollowers: Number(e.target.value) })}
                  onKeyDown={(e) => { if (e.key === 'Enter') onRunFilter(); }}
                  className="w-full bg-white border border-[#CBD5E1] rounded-lg px-3 py-1.5 text-xs font-extrabold text-black font-mono"
                />
              </div>
              <div>
                <label className="block text-xs font-black text-black mb-1">Follower Max Bound</label>
                <input
                  type="number"
                  value={filters.maxFollowers}
                  onChange={(e) => onFilterChange({ maxFollowers: Number(e.target.value) })}
                  onKeyDown={(e) => { if (e.key === 'Enter') onRunFilter(); }}
                  className="w-full bg-white border border-[#CBD5E1] rounded-lg px-3 py-1.5 text-xs font-extrabold text-black font-mono"
                />
              </div>
              <div>
                <label className="block text-xs font-black text-black mb-1">
                  Minimum Engagement ({filters.minEngagement}%)
                </label>
                <input
                  type="range"
                  min="0.5"
                  max="8.0"
                  step="0.1"
                  value={filters.minEngagement}
                  onChange={(e) => onFilterChange({ minEngagement: Number(e.target.value) })}
                  className="w-full mt-2 cursor-pointer accent-black"
                />
              </div>
            </div>
          </div>

          {/* Qualified vs Disqualified Strict Split Tables */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* 1. Qualified Profiles (Passed) */}
            <div data-testid="qualified-profiles-card" className="border border-[#86EFAC] rounded-2xl overflow-hidden shadow-xs flex flex-col bg-white">
              <div className="bg-[#DCFCE7] px-4 py-3.5 border-b border-[#86EFAC] flex justify-between items-center">
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-[#166534]" />
                  <span className="font-black text-sm text-black">Qualified Profiles (Passed)</span>
                </div>
                <span className="bg-white border border-[#86EFAC] text-xs font-black px-2.5 py-0.5 rounded-full text-[#14532D] shadow-xs">
                  {passedInfluencers.length} Passed
                </span>
              </div>
              <div className="max-h-[520px] overflow-y-auto p-4 space-y-3 bg-[#F8FAFC]/50 flex-1">
                {passedInfluencers.length > 0 ? (
                  passedInfluencers.map((item, idx) => (
                    <div key={idx} className="p-4 bg-white hover:bg-[#F0FDF4]/50 border border-[#E2E8F0] hover:border-[#86EFAC] rounded-xl transition-all shadow-xs space-y-3">
                      {/* Top Row: Creator Details & Stat Chips */}
                      <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-3">
                        <div className="min-w-0 flex-1">
                          <div className="flex flex-wrap items-center gap-1.5">
                            <span className="font-black text-sm text-black">{item.name}</span>
                            <span className="text-xs font-mono font-bold text-[#64748B]">@{item.handle}</span>
                            {item.contact_email && item.contact_email !== 'Not Found' && (
                              <span className="text-[10px] font-black bg-[#DCFCE7] text-[#166534] border border-[#86EFAC] px-2 py-0.5 rounded-md">
                                Verified Email
                              </span>
                            )}
                          </div>
                          <div className="text-xs font-semibold text-[#475569] mt-1 flex flex-wrap items-center gap-1.5">
                            <span className="inline-flex items-center gap-1">
                              <MapPin className="w-3 h-3 text-[#64748B]" />
                              <span>{item.location || 'Global'}</span>
                            </span>
                            <span className="text-[#94A3B8]">•</span>
                            <span>{item.platform}</span>
                            <span className="text-[#94A3B8]">•</span>
                            <span className="font-bold text-black">{item.niche}</span>
                          </div>
                        </div>

                        {/* Metric Chips & Status Pill */}
                        <div className="flex items-center gap-2 shrink-0">
                          <div className="bg-[#F8FAFC] border border-[#CBD5E1] px-2.5 py-1 rounded-lg text-right shadow-xs">
                            <span className="text-[9px] font-bold text-[#64748B] block leading-none uppercase">Followers</span>
                            <span className="text-xs font-black text-black font-mono leading-tight">
                              {Number(item.follower_count).toLocaleString()}
                            </span>
                          </div>
                          <div className="bg-[#F8FAFC] border border-[#CBD5E1] px-2.5 py-1 rounded-lg text-right shadow-xs">
                            <span className="text-[9px] font-bold text-[#64748B] block leading-none uppercase">Engagement</span>
                            <span className="text-xs font-black text-black font-mono leading-tight">
                              {Number(item.engagement_rate).toFixed(1)}%
                            </span>
                          </div>
                          <div className="bg-[#DCFCE7] border border-[#86EFAC] text-[#14532D] text-xs font-black px-2.5 py-2 rounded-lg flex items-center gap-1 shadow-xs">
                            <CheckCircle2 className="w-3.5 h-3.5 text-[#166534]" />
                            <span>PASSED</span>
                          </div>
                        </div>
                      </div>

                      {/* Bottom Row: Full-width Evaluation Reasoning Strip */}
                      <div className="bg-[#F0FDF4] border border-[#86EFAC] rounded-lg px-3.5 py-2 flex items-start gap-2">
                        <CheckCircle2 className="w-3.5 h-3.5 text-[#166534] shrink-0 mt-0.5" />
                        <span className="text-xs font-semibold text-[#14532D] leading-relaxed">
                          {item.qualification_reason || 'Qualified: Meets follower bounds, engagement threshold, and target demographic criteria.'}
                        </span>
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="p-10 text-center text-xs font-bold text-[#64748B] bg-white rounded-xl border border-dashed border-[#CBD5E1]">
                    No creator profiles passed all active criteria for {filters.geo}. Try broadening follower bounds or selecting another category.
                  </div>
                )}
              </div>
            </div>

            {/* 2. Disqualified Profiles (Failed) */}
            <div data-testid="disqualified-profiles-card" className="border border-[#FCA5A5] rounded-2xl overflow-hidden shadow-xs flex flex-col bg-white">
              <div className="bg-[#FEE2E2] px-4 py-3.5 border-b border-[#FCA5A5] flex justify-between items-center">
                <div className="flex items-center gap-2">
                  <XCircle className="w-4 h-4 text-[#991B1B]" />
                  <span className="font-black text-sm text-black">Disqualified Profiles (Failed)</span>
                </div>
                <span className="bg-white border border-[#FCA5A5] text-xs font-black px-2.5 py-0.5 rounded-full text-[#991B1B] shadow-xs">
                  {failedInfluencers.length} Failed
                </span>
              </div>
              <div className="max-h-[520px] overflow-y-auto p-4 space-y-3 bg-[#F8FAFC]/50 flex-1">
                {failedInfluencers.length > 0 ? (
                  failedInfluencers.map((item, idx) => (
                    <div key={idx} className="p-4 bg-white hover:bg-[#FEF2F2]/50 border border-[#E2E8F0] hover:border-[#FCA5A5] rounded-xl transition-all shadow-xs space-y-3">
                      {/* Top Row: Creator Details & Stat Chips */}
                      <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-3">
                        <div className="min-w-0 flex-1">
                          <div className="flex flex-wrap items-center gap-1.5">
                            <span className="font-black text-sm text-black">{item.name}</span>
                            <span className="text-xs font-mono font-bold text-[#64748B]">@{item.handle}</span>
                          </div>
                          <div className="text-xs font-semibold text-[#475569] mt-1 flex flex-wrap items-center gap-1.5">
                            <span className="inline-flex items-center gap-1">
                              <MapPin className="w-3 h-3 text-[#64748B]" />
                              <span>{item.location || 'Not Specified'}</span>
                            </span>
                            <span className="text-[#94A3B8]">•</span>
                            <span>{item.platform}</span>
                            <span className="text-[#94A3B8]">•</span>
                            <span className="font-bold text-black">{item.niche}</span>
                          </div>
                        </div>

                        {/* Metric Chips & Status Pill */}
                        <div className="flex items-center gap-2 shrink-0">
                          <div className="bg-[#F8FAFC] border border-[#CBD5E1] px-2.5 py-1 rounded-lg text-right shadow-xs">
                            <span className="text-[9px] font-bold text-[#64748B] block leading-none uppercase">Followers</span>
                            <span className="text-xs font-black text-black font-mono leading-tight">
                              {Number(item.follower_count).toLocaleString()}
                            </span>
                          </div>
                          <div className="bg-[#F8FAFC] border border-[#CBD5E1] px-2.5 py-1 rounded-lg text-right shadow-xs">
                            <span className="text-[9px] font-bold text-[#64748B] block leading-none uppercase">Engagement</span>
                            <span className="text-xs font-black text-black font-mono leading-tight">
                              {Number(item.engagement_rate).toFixed(1)}%
                            </span>
                          </div>
                          <div className="bg-[#FEE2E2] border border-[#FCA5A5] text-[#991B1B] text-xs font-black px-2.5 py-2 rounded-lg flex items-center gap-1 shadow-xs">
                            <XCircle className="w-3.5 h-3.5 text-[#991B1B]" />
                            <span>FAILED</span>
                          </div>
                        </div>
                      </div>

                      {/* Bottom Row: Full-width Disqualification Reasons Breakdown */}
                      <div className="bg-[#FEF2F2] border border-[#FCA5A5] rounded-lg px-3.5 py-2 flex items-start gap-2">
                        <XCircle className="w-3.5 h-3.5 text-[#991B1B] shrink-0 mt-0.5" />
                        <div className="text-xs font-semibold text-[#7F1D1D] leading-relaxed space-y-1">
                          {item.qualification_reason ? (
                            item.qualification_reason.split(' | ').map((reason, rIdx) => (
                              <div key={rIdx} className="flex items-center gap-1.5">
                                <span className="w-1.5 h-1.5 rounded-full bg-[#EF4444] shrink-0 inline-block" />
                                <span>{reason}</span>
                              </div>
                            ))
                          ) : (
                            <span>Disqualified: Did not satisfy active criteria bounds.</span>
                          )}
                        </div>
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="p-10 text-center text-xs font-bold text-[#64748B] bg-white rounded-xl border border-dashed border-[#CBD5E1]">
                    All evaluated profiles passed criteria.
                  </div>
                )}
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
                {eligibleCreators.map((i) => (
                  <option key={i.handle} value={i.handle} className="bg-white text-black font-bold">
                    {i.name} (@{i.handle}) - {i.location || 'Global'}
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
                      'Verified content creator sharing authentic perspectives, daily tutorials, and engaging brand partnerships.'}
                  </p>

                  <div className="text-xs font-extrabold text-black uppercase tracking-wider">Identified Themes:</div>
                  <div className="font-mono text-sm font-extrabold text-black mt-1 bg-white border border-[#BAE6FD] px-3 py-1.5 rounded-xl inline-block">
                    {currentCreator.content_themes || `${filters.niche} Content, UGC, Brand Collaborations`}
                  </div>
                </div>

                <div className="mt-5 pt-4 border-t border-[#E2E8F0]">
                  <div className="text-xs font-extrabold text-black uppercase tracking-wider mb-2.5">
                    Audience Demographics &amp; Geography
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                    <div className="bg-white border border-[#E2E8F0] p-3 rounded-xl flex flex-col justify-between">
                      <div className="text-[11px] font-bold text-[#64748B] flex items-center gap-1">
                        <Users className="w-3 h-3 text-[#64748B]" /> Age Group
                      </div>
                      <div className="font-mono text-sm font-black text-black mt-1">
                        {currentCreator.audience_age || '18-34 (72%)'}
                      </div>
                      <div className="text-[10px] font-bold text-[#64748B] mt-1">
                        Core Cohort
                      </div>
                    </div>

                    <div className="bg-white border border-[#E2E8F0] p-3 rounded-xl flex flex-col justify-between">
                      <div className="text-[11px] font-bold text-[#64748B] flex items-center gap-1">
                        <Users className="w-3 h-3 text-[#64748B]" /> Gender Distribution
                      </div>
                      <div className="font-mono text-sm font-black text-black mt-1">
                        {currentCreator.audience_gender || 'Female (78%)'}
                      </div>
                      <div className="text-[10px] font-bold text-[#64748B] mt-1">
                        Audience Split
                      </div>
                    </div>

                    {(() => {
                      const rawGeo = currentCreator.audience_geography || currentCreator.location || filters.geo;
                      let countryTag = 'India (IN)';
                      const g = rawGeo.toLowerCase();
                      if (g.includes(', in') || g.includes('india') || g.includes('mumbai') || g.includes('delhi') || g.includes('bangalore') || g.includes('hyderabad')) {
                        countryTag = 'India (IN)';
                      } else if (g.includes(', us') || g.includes('united states') || g.includes('usa')) {
                        countryTag = 'United States (US)';
                      } else if (g.includes(', gb') || g.includes('uk') || g.includes('london')) {
                        countryTag = 'United Kingdom (GB)';
                      } else if (g.includes(', ca') || g.includes('canada') || g.includes('toronto')) {
                        countryTag = 'Canada (CA)';
                      } else if (g.includes(', au') || g.includes('australia')) {
                        countryTag = 'Australia (AU)';
                      }

                      return (
                        <div className="bg-white border border-[#E2E8F0] p-3 rounded-xl flex flex-col justify-between">
                          <div className="text-[11px] font-bold text-[#64748B] flex items-center gap-1">
                            <Globe className="w-3 h-3 text-[#64748B]" /> Top Geography
                          </div>
                          <div className="font-mono text-sm font-black text-black mt-1">
                            {rawGeo}
                          </div>
                          <div className="text-[10px] font-black text-[#0284C7] bg-[#E0F2FE] border border-[#BAE6FD] px-2 py-0.5 rounded-md inline-block mt-1 w-fit">
                            {countryTag}
                          </div>
                        </div>
                      );
                    })()}
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
                  {eligibleCreators.map((i) => (
                    <option key={i.handle} value={i.handle} className="bg-white text-black font-bold">
                      {i.name} (@{i.handle}) - {i.location || 'Global'}
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
                      const creator = eligibleCreators.find((i) => i.handle === targetCreator);
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
                      const creator = eligibleCreators.find((i) => i.handle === targetCreator);
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
