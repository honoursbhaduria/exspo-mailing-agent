import React, { useState, useEffect } from 'react';
import HeroHeader from './components/HeroHeader';
import AudienceReachCard, { type CreatorHighlight } from './components/AudienceReachCard';
import DashboardControlCard from './components/DashboardControlCard';
import FeedActivityCard, { type FeedItem } from './components/FeedActivityCard';
import TabsSection from './components/TabsSection';
import BackgroundPattern from './components/ui/BackgroundPattern';
import { api } from './services/api';

export const App: React.FC = () => {
  const [totalCount, setTotalCount] = useState(65);
  const [passedCount, setPassedCount] = useState(21);
  const [sentCount, setSentCount] = useState(15);
  const [mailCount, setMailCount] = useState(9);
  const [dmCount, setDmCount] = useState(6);
  const [avgFollowers, setAvgFollowers] = useState('35K');
  const [avgReach, setAvgReach] = useState('11K');
  const [topCreators, setTopCreators] = useState<CreatorHighlight[]>([]);
  const [feedItems, setFeedItems] = useState<FeedItem[]>([]);

  const [currentGeo, setCurrentGeo] = useState('Global (All Regions)');
  const [currentPlatform, setCurrentPlatform] = useState('Instagram & TikTok');
  const [currentNiche, setCurrentNiche] = useState('Fashion & Beauty');
  const [currentScale, setCurrentScale] = useState('Micro-Influencers (5k - 100k)');

  const refreshCounts = async (params?: { geo?: string; platform?: string; niche?: string; scale?: string }) => {
    const geo = params?.geo ?? currentGeo;
    const platform = params?.platform ?? currentPlatform;
    const niche = params?.niche ?? currentNiche;
    const scale = params?.scale ?? currentScale;

    if (params?.geo) setCurrentGeo(params.geo);
    if (params?.platform) setCurrentPlatform(params.platform);
    if (params?.niche) setCurrentNiche(params.niche);
    if (params?.scale) setCurrentScale(params.scale);

    try {
      const rawRes = await api.getRawInfluencers(100);
      setTotalCount(rawRes.total);

      const trackerRes = await api.getTrackerStats();
      setSentCount(trackerRes.stats.total_logged);
      if (trackerRes.stats.mail_sent !== undefined) setMailCount(trackerRes.stats.mail_sent);
      if (trackerRes.stats.dm_sent !== undefined) setDmCount(trackerRes.stats.dm_sent);

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
      setPassedCount(filterRes.passed_count);

      // Find matching creators for active geography
      const isGlobal = !geo || geo.toLowerCase().includes('global') || geo.toLowerCase().includes('all');
      const geoMatches = isGlobal
        ? filterRes.results
        : filterRes.results.filter(
            (r) => !r.qualification_reason || !r.qualification_reason.includes('does not match target')
          );

      const activeCreators = geoMatches.length > 0 ? geoMatches : filterRes.results;

      // Discovered count: region count if filtered, else total raw count
      if (!isGlobal && geoMatches.length > 0) {
        setTotalCount(geoMatches.length);
      } else {
        setTotalCount(rawRes.total || 93);
      }

      // Compute dynamic creator averages based on the active region
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
      if (filterRes.results && filterRes.results.length > 0) {
        const passedOnly = filterRes.results
          .filter((r) => r.qualification_status === 'PASSED')
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
            else if (item.follower_count < minF) tag = '< 5k';
            else if (item.follower_count > maxF) tag = '> 100k';
            else if (item.engagement_rate < 1.5) tag = 'Low ER';
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
      }
    } catch (e) {
      console.log('Using default cached counts');
    }
  };

  useEffect(() => {
    refreshCounts();
  }, []);

  return (
    <div className="min-h-screen py-8 px-4 sm:px-6 lg:px-8 max-w-[1340px] w-full mx-auto relative box-border">
      {/* Background Gradient & Grid Pattern with Blur */}
      <BackgroundPattern />

      {/* 1. Hero Header */}
      <HeroHeader />

      {/* 2. Triple Card Showcase Matching image.png */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 mb-8 items-stretch">
        <div className="lg:col-span-3">
          <AudienceReachCard
            totalCount={totalCount}
            avgFollowers={avgFollowers}
            avgReach={avgReach}
            topCreators={topCreators}
          />
        </div>
        <div className="lg:col-span-6">
          <DashboardControlCard
            totalCount={totalCount}
            passedCount={passedCount}
            sentCount={sentCount}
            mailCount={mailCount}
            dmCount={dmCount}
            onRefresh={refreshCounts}
          />
        </div>
        <div className="lg:col-span-3">
          <FeedActivityCard items={feedItems} geo={currentGeo} />
        </div>
      </div>

      {/* 3. Modular Workspace Tabs (Underline Navigation, No Box Div) */}
      <div className="mb-8">
        <TabsSection
          activeGeo={currentGeo}
          activePlatform={currentPlatform}
          activeNiche={currentNiche}
          activeScale={currentScale}
        />
      </div>
    </div>
  );
};

export default App;
