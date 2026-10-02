import React, { useState, useEffect } from 'react';
import HeroHeader from './components/HeroHeader';
import AudienceReachCard, { type CreatorHighlight } from './components/AudienceReachCard';
import DashboardControlCard, { type FilterState } from './components/DashboardControlCard';
import FeedActivityCard, { type FeedItem } from './components/FeedActivityCard';
import TabsSection from './components/TabsSection';
import BackgroundPattern from './components/ui/BackgroundPattern';
import { api, type Influencer, type DatabaseStatus } from './services/api';

export const App: React.FC = () => {
  // Stats
  const [totalCount, setTotalCount] = useState(273);
  const [passedCount, setPassedCount] = useState(29);
  const [sentCount, setSentCount] = useState(173);
  const [mailCount, setMailCount] = useState(9);
  const [dmCount, setDmCount] = useState(6);
  const [avgFollowers, setAvgFollowers] = useState('35K');
  const [avgReach, setAvgReach] = useState('11K');
  const [topCreators, setTopCreators] = useState<CreatorHighlight[]>([]);
  const [feedItems, setFeedItems] = useState<FeedItem[]>([]);

  // Database & Countries State
  const [dbStatus, setDbStatus] = useState<DatabaseStatus | null>(null);
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

  // Unified Filter State (Single Source of Truth)
  const [filters, setFilters] = useState<FilterState>({
    niche: 'Fashion & Beauty',
    platform: 'Instagram & TikTok',
    geo: 'Global (All Regions)',
    scale: 'Micro-Influencers (5k - 100k)',
    minFollowers: 5000,
    maxFollowers: 100000,
    minEngagement: 2.0,
  });

  // Filtered Datasets from Database Engine
  const [allInfluencers, setAllInfluencers] = useState<Influencer[]>([]);
  const [filteredResults, setFilteredResults] = useState<Influencer[]>([]);
  const [passedInfluencers, setPassedInfluencers] = useState<Influencer[]>([]);
  const [failedInfluencers, setFailedInfluencers] = useState<Influencer[]>([]);
  const [filterLoading, setFilterLoading] = useState(false);

  // Initial Data Fetch
  useEffect(() => {
    const init = async () => {
      try {
        const filterPromise = runPipelineFilter(filters);
        const [dbRes, geoRes, trackerRes] = await Promise.all([
          api.getDatabaseStatus().catch(() => null),
          api.getCountries().catch(() => null),
          api.getTrackerStats().catch(() => null),
          filterPromise,
        ]);

        if (dbRes) setDbStatus(dbRes);
        if (geoRes?.countries?.length) setCountries(geoRes.countries);
        if (trackerRes?.stats) {
          setSentCount(trackerRes.stats.total_logged);
          if (trackerRes.stats.mail_sent !== undefined) setMailCount(trackerRes.stats.mail_sent);
          if (trackerRes.stats.dm_sent !== undefined) setDmCount(trackerRes.stats.dm_sent);
        }
      } catch (err) {
        console.error('App init error:', err);
      }
    };
    init();
  }, []);

  // Filter Pipeline Execution
  const runPipelineFilter = async (activeFilters?: Partial<FilterState>) => {
    const active = { ...filters, ...(activeFilters || {}) };
    setFilterLoading(true);
    try {
      const filterRes = await api.filterInfluencers({
        min_followers: active.minFollowers,
        max_followers: active.maxFollowers,
        min_engagement: active.minEngagement,
        target_niche: active.niche,
        target_geography: active.geo,
        target_platform: active.platform,
      });

      setFilteredResults(filterRes.results);
      setPassedInfluencers(filterRes.passed_influencers);
      setFailedInfluencers(filterRes.failed_influencers);
      setAllInfluencers(filterRes.results);
      setPassedCount(filterRes.passed_count);

      // Refresh DB Status
      const statusRes = await api.getDatabaseStatus().catch(() => null);
      if (statusRes) setDbStatus(statusRes);

      // Geography matching for card metrics
      const isGlobal = !active.geo || active.geo.toLowerCase().includes('global') || active.geo.toLowerCase().includes('all');
      const geoMatches = isGlobal
        ? filterRes.results
        : filterRes.results.filter(
            (r) => !r.qualification_reason || !r.qualification_reason.includes('does not match target')
          );

      const activeCreators = geoMatches.length > 0 ? geoMatches : filterRes.results;
      setTotalCount(isGlobal ? (statusRes?.total_records || filterRes.total) : geoMatches.length);

      // Dynamic creator averages based on the active region
      if (activeCreators.length > 0) {
        const totalFollowers = activeCreators.reduce((acc, cur) => acc + (cur.follower_count || 0), 0);
        const avgF = Math.round(totalFollowers / activeCreators.length);
        setAvgFollowers(`${Math.round(avgF / 1000)}K`);

        const totalReach = activeCreators.reduce(
          (acc, cur) => acc + (cur.follower_count || 0) * ((cur.engagement_rate || 2.5) / 100),
          0
        );
        const avgR = Math.round(totalReach / activeCreators.length);
        setAvgReach(`${Math.max(1, Math.round(avgR / 1000))}K`);
      }

      // Top 4 qualified creators sorted by followers
      const passedOnly = filterRes.passed_influencers
        .slice()
        .sort((a, b) => b.follower_count - a.follower_count);

      const highlights: CreatorHighlight[] = (passedOnly.length > 0 ? passedOnly : activeCreators)
        .slice(0, 4)
        .map((c) => ({
          name: c.name,
          follower_str: `${(c.follower_count / 1000).toFixed(1)}K`,
        }));
      setTopCreators(highlights);

      // Feed Activity items: Mix of passed and edge failure cases for dynamic feedback
      const relevantForFeed = geoMatches.length > 0 ? geoMatches : filterRes.results;
      const passedFeed = relevantForFeed.filter((r) => r.qualification_status === 'PASSED');
      const failedFeed = relevantForFeed.filter((r) => r.qualification_status === 'FAILED');

      const feedCandidates: typeof relevantForFeed = [];
      feedCandidates.push(...passedFeed.slice(0, 2));
      feedCandidates.push(...failedFeed.slice(0, 3));
      if (feedCandidates.length < 5) {
        const remainingPassed = passedFeed.slice(2, 2 + (5 - feedCandidates.length));
        feedCandidates.push(...remainingPassed);
      }

      const feed: FeedItem[] = (feedCandidates.length > 0 ? feedCandidates : relevantForFeed.slice(0, 5)).map((item) => {
        let tag = 'PASS';
        if (item.qualification_status !== 'PASSED') {
          const reason = item.qualification_reason || '';
          if (reason.includes('Audience geography')) tag = 'Geo Mismatch';
          else if (reason.includes('Platform')) tag = 'Platform';
          else if (item.follower_count < active.minFollowers) tag = `< ${Math.round(active.minFollowers / 1000)}k`;
          else if (item.follower_count > active.maxFollowers) tag = `> ${Math.round(active.maxFollowers / 1000)}k`;
          else if (item.engagement_rate < active.minEngagement) tag = 'Low ER';
          else tag = 'FAIL';
        }
        return {
          name: item.name,
          loc: item.location || 'Global',
          status: item.qualification_status || 'PASS',
          pass: item.qualification_status === 'PASSED',
          tag,
        };
      });
      setFeedItems(feed);
    } catch (err) {
      console.error('Filter execution failed:', err);
    } finally {
      setFilterLoading(false);
    }
  };

  // Unified Filter Change Handler
  const handleFilterChange = (updates: Partial<FilterState>) => {
    setFilters((prev) => {
      const next = { ...prev, ...updates };
      // Sync scale bounds if scale was explicitly changed without manual bounds
      if (updates.scale && updates.minFollowers === undefined && updates.maxFollowers === undefined) {
        if (updates.scale.includes('Nano')) {
          next.minFollowers = 1000;
          next.maxFollowers = 5000;
        } else if (updates.scale.includes('Macro')) {
          next.minFollowers = 100000;
          next.maxFollowers = 10000000;
        } else {
          next.minFollowers = 5000;
          next.maxFollowers = 100000;
        }
      }
      runPipelineFilter(next);
      return next;
    });
  };

  const refreshTrackerStats = async () => {
    try {
      const res = await api.getTrackerStats();
      setSentCount(res.stats.total_logged);
      if (res.stats.mail_sent !== undefined) setMailCount(res.stats.mail_sent);
      if (res.stats.dm_sent !== undefined) setDmCount(res.stats.dm_sent);
    } catch {}
  };

  return (
    <div className="min-h-screen py-4 sm:py-8 px-3 sm:px-6 lg:px-8 max-w-[1340px] w-full mx-auto relative box-border overflow-x-hidden">
      {/* Background Gradient & Grid Pattern */}
      <BackgroundPattern />

      {/* Top Corner GitHub Source Code Link */}
      <div className="absolute top-3 right-3 sm:top-5 sm:right-6 lg:right-8 z-30">
        <a
          href="https://github.com/honoursbhaduria/exspo-mailing-agent"
          target="_blank"
          rel="noopener noreferrer"
          title="View Source Code on GitHub"
          className="inline-flex items-center gap-1.5 sm:gap-2 px-2.5 py-1 sm:px-3 sm:py-1.5 rounded-full bg-white/90 hover:bg-white border border-slate-200/90 hover:border-slate-300 shadow-[0_2px_6px_rgba(0,0,0,0.04)] hover:shadow-[0_4px_12px_rgba(0,0,0,0.08)] transition-all duration-200 text-slate-700 hover:text-black group backdrop-blur-sm"
          aria-label="View source code on GitHub"
        >
          <svg
            className="w-4 h-4 text-slate-800 group-hover:scale-110 transition-transform duration-200"
            viewBox="0 0 24 24"
            fill="currentColor"
            aria-hidden="true"
          >
            <path
              fillRule="evenodd"
              clipRule="evenodd"
              d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"
            />
          </svg>
          <span className="text-[11px] sm:text-xs font-semibold text-slate-700 group-hover:text-slate-900 tracking-tight hidden sm:inline">
            Source Code
          </span>
        </a>
      </div>

      {/* 1. Hero Header with Database Status Badge */}
      <HeroHeader dbStatus={dbStatus} />

      {/* 2. Triple Card Showcase (DashboardControlCard first on mobile) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-4 sm:gap-5 mb-6 sm:mb-8 items-stretch">
        <div className="order-2 lg:order-1 lg:col-span-3">
          <AudienceReachCard
            totalCount={totalCount}
            avgFollowers={avgFollowers}
            avgReach={avgReach}
            topCreators={topCreators}
          />
        </div>
        <div className="order-1 lg:order-2 lg:col-span-6">
          <DashboardControlCard
            totalCount={totalCount}
            passedCount={passedCount}
            sentCount={sentCount}
            mailCount={mailCount}
            dmCount={dmCount}
            filters={filters}
            onFilterChange={handleFilterChange}
            countries={countries}
          />
        </div>
        <div className="order-3 lg:order-3 lg:col-span-3">
          <FeedActivityCard items={feedItems} geo={filters.geo} />
        </div>
      </div>

      {/* 3. Modular Workspace Tabs */}
      <div className="mb-8">
        <TabsSection
          filters={filters}
          onFilterChange={handleFilterChange}
          filteredResults={filteredResults}
          passedInfluencers={passedInfluencers}
          failedInfluencers={failedInfluencers}
          filterLoading={filterLoading}
          onRunFilter={runPipelineFilter}
          countries={countries}
          allInfluencers={allInfluencers}
          onRefreshTracker={refreshTrackerStats}
        />
      </div>
    </div>
  );
};

export default App;
