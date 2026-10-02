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
        const [dbRes, geoRes, rawRes, trackerRes] = await Promise.all([
          api.getDatabaseStatus().catch(() => null),
          api.getCountries().catch(() => null),
          api.getRawInfluencers().catch(() => null),
          api.getTrackerStats().catch(() => null),
        ]);

        if (dbRes) setDbStatus(dbRes);
        if (geoRes?.countries?.length) setCountries(geoRes.countries);
        if (rawRes?.influencers?.length) {
          setAllInfluencers(rawRes.influencers);
          setTotalCount(rawRes.total || rawRes.influencers.length);
        }
        if (trackerRes?.stats) {
          setSentCount(trackerRes.stats.total_logged);
          if (trackerRes.stats.mail_sent !== undefined) setMailCount(trackerRes.stats.mail_sent);
          if (trackerRes.stats.dm_sent !== undefined) setDmCount(trackerRes.stats.dm_sent);
        }

        await runPipelineFilter(filters);
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
