import React from 'react';
import { Activity } from 'lucide-react';

interface AudienceReachCardProps {
  totalCount?: number;
  avgFollowers?: string;
  avgReach?: string;
}

export const AudienceReachCard: React.FC<AudienceReachCardProps> = ({
  totalCount = 65,
  avgFollowers = '35K',
  avgReach = '11K',
}) => {
  return (
    <div className="bg-white border border-[#E2E8F0] hover:border-[#BAE6FD] rounded-[20px] p-5 shadow-[0_8px_24px_-6px_rgba(0,0,0,0.04)] hover:shadow-[0_12px_28px_-6px_rgba(2,132,199,0.08)] transition-all h-full flex flex-col justify-between">
      <div>
        <div className="flex justify-between items-center mb-4">
          <span className="font-extrabold text-base text-black">Audience Reach</span>
          <span className="inline-flex items-center gap-1.5 bg-[#F1F5F9] text-black border border-[#CBD5E1] text-xs font-bold px-2.5 py-0.5 rounded-full">
            <Activity className="w-3 h-3 text-black" /> LIVE
          </span>
        </div>

        <div className="flex justify-between items-baseline mb-4">
          <div>
            <div className="text-2xl font-black text-black font-mono leading-none">{totalCount}</div>
            <div className="text-xs font-bold text-[#333333] mt-1">Discovered</div>
          </div>
          <div>
            <div className="text-2xl font-black text-black font-mono leading-none">{avgFollowers}</div>
            <div className="text-xs font-bold text-[#333333] mt-1">Avg Followers</div>
          </div>
          <div>
            <div className="text-2xl font-black text-black font-mono leading-none">{avgReach}</div>
            <div className="text-xs font-bold text-[#333333] mt-1">Avg Reach</div>
          </div>
        </div>

        {/* Light Azure Wave Trajectory Curves */}
        <div className="my-3">
          <svg viewBox="0 0 240 50" className="w-full h-12 overflow-visible">
            <path d="M 0,38 Q 60,8 120,26 T 240,12" fill="none" stroke="#0284C7" strokeWidth="2.5" strokeLinecap="round" />
            <path d="M 0,46 Q 70,40 140,18 T 240,36" fill="none" stroke="#7DD3FC" strokeWidth="2" strokeLinecap="round" opacity="0.6" />
          </svg>
        </div>
      </div>

      <div>
        <div className="text-[11px] font-extrabold text-black uppercase tracking-wider mb-2">
          Top Qualified Creators
        </div>

        <div className="space-y-1.5">
          <div className="bg-[#F8FAFC] border border-[#E2E8F0] rounded-xl px-3 py-2 flex justify-between items-center">
            <span className="text-sm font-bold text-black">Nazima Mogra</span>
            <span className="font-mono text-xs font-extrabold text-black">62.0K</span>
          </div>
          <div className="bg-[#F8FAFC] border border-[#E2E8F0] rounded-xl px-3 py-2 flex justify-between items-center">
            <span className="text-sm font-bold text-black">Isabella Quintero</span>
            <span className="font-mono text-xs font-extrabold text-black">36.8K</span>
          </div>
          <div className="bg-[#F8FAFC] border border-[#BAE6FD] rounded-xl px-3 py-2 flex justify-between items-center">
            <span className="text-sm font-extrabold text-black">Dhanu Gunathissa</span>
            <span className="font-mono text-xs font-black text-black">92.0K</span>
          </div>
          <div className="bg-[#F8FAFC] border border-[#E2E8F0] rounded-xl px-3 py-2 flex justify-between items-center">
            <span className="text-sm font-bold text-black">Rashonda Wisner</span>
            <span className="font-mono text-xs font-extrabold text-black">24.5K</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AudienceReachCard;
