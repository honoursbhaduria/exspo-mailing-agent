import React, { useState, useEffect } from 'react';
import HeroHeader from './components/HeroHeader';
import AudienceReachCard from './components/AudienceReachCard';
import DashboardControlCard from './components/DashboardControlCard';
import FeedActivityCard from './components/FeedActivityCard';
import TabsSection from './components/TabsSection';
import FooterGlobe from './components/FooterGlobe';
import { api } from './services/api';

export const App: React.FC = () => {
  const [totalCount, setTotalCount] = useState(65);
  const [passedCount, setPassedCount] = useState(29);
  const [sentCount, setSentCount] = useState(173);

  const refreshCounts = async () => {
    try {
      const rawRes = await api.getRawInfluencers(100);
      setTotalCount(rawRes.total);

      const trackerRes = await api.getTrackerStats();
      setSentCount(trackerRes.stats.total_logged);

      const filterRes = await api.filterInfluencers({
        min_followers: 5000,
        max_followers: 100000,
        min_engagement: 2.0,
        target_niche: 'Fashion',
      });
      setPassedCount(filterRes.passed_count);
    } catch (e) {
      console.log('Using default cached counts');
    }
  };

  useEffect(() => {
    refreshCounts();
  }, []);

  return (
    <div className="min-h-screen py-8 px-4 sm:px-6 lg:px-8 max-w-[1340px] mx-auto">
      {/* 1. Hero Header */}
      <HeroHeader />

      {/* 2. Triple Card Showcase Matching image.png */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 mb-8 items-stretch">
        <div className="lg:col-span-3">
          <AudienceReachCard totalCount={totalCount} avgFollowers="35K" avgReach="11K" />
        </div>
        <div className="lg:col-span-6">
          <DashboardControlCard
            totalCount={totalCount}
            passedCount={passedCount}
            sentCount={sentCount}
            onRefresh={refreshCounts}
          />
        </div>
        <div className="lg:col-span-3">
          <FeedActivityCard />
        </div>
      </div>

      {/* 3. Modular Workspace Tabs (Underline Navigation, No Box Div) */}
      <div className="mb-8">
        <TabsSection />
      </div>

      {/* 4. Footer: Interactive 3D WebGL Globe */}
      <FooterGlobe />
    </div>
  );
};

export default App;
