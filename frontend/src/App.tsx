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

  const refreshCounts = async () => {
    try {
      const rawRes = await api.getRawInfluencers(100);
      setTotalCount(rawRes.total);

      const trackerRes = await api.getTrackerStats();
      setSentCount(trackerRes.stats.total_logged);
      if (trackerRes.stats.mail_sent !== undefined) setMailCount(trackerRes.stats.mail_sent);
      if (trackerRes.stats.dm_sent !== undefined) setDmCount(trackerRes.stats.dm_sent);

      const filterRes = await api.filterInfluencers({
        min_followers: 5000,
        max_followers: 100000,
        min_engagement: 2.0,
        target_niche: 'Fashion',
      });
      setPassedCount(filterRes.passed_count);

      // Compute dynamic creator averages
      if (rawRes.influencers && rawRes.influencers.length > 0) {
        const totalFollowers = rawRes.influencers.reduce((acc, cur) => acc + (cur.follower_count || 0), 0);
        const avgF = Math.round(totalFollowers / rawRes.influencers.length);
        setAvgFollowers(`${Math.round(avgF / 1000)}K`);

        const totalReach = rawRes.influencers.reduce(
          (acc, cur) => acc + (cur.follower_count || 0) * ((cur.engagement_rate || 2.5) / 100),
          0
        );
        const avgR = Math.round(totalReach / rawRes.influencers.length);
        setAvgReach(`${Math.max(1, Math.round(avgR / 1000))}K`);
      }

      // Top 4 qualified creators sorted by followers
      if (filterRes.results && filterRes.results.length > 0) {
        const passedOnly = filterRes.results
          .filter((r) => r.qualification_status === 'PASSED')
          .sort((a, b) => b.follower_count - a.follower_count);

        const highlights: CreatorHighlight[] = (passedOnly.length > 0 ? passedOnly : filterRes.results)
          .slice(0, 4)
          .map((c) => ({
            name: c.name,
            follower_str: `${(c.follower_count / 1000).toFixed(1)}K`,
          }));
        setTopCreators(highlights);

        // Feed Activity items: First 5 evaluated records
        const feed: FeedItem[] = filterRes.results.slice(0, 5).map((item) => {
          let tag = 'PASS';
          if (item.qualification_status !== 'PASSED') {
            if (item.follower_count < 5000) tag = '< 5k';
            else if (item.follower_count > 100000) tag = '> 100k';
            else if (item.engagement_rate < 2.0) tag = 'Low ER';
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
    <div className="min-h-screen py-8 px-4 sm:px-6 lg:px-8 max-w-[1340px] mx-auto relative">
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
          <FeedActivityCard items={feedItems} />
        </div>
      </div>

      {/* 3. Modular Workspace Tabs (Underline Navigation, No Box Div) */}
      <div className="mb-8">
        <TabsSection />
      </div>
    </div>
  );
};

export default App;
