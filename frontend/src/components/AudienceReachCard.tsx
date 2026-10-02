import React from 'react';
import { Activity } from 'lucide-react';

export interface CreatorHighlight {
  name: string;
  follower_str: string;
}

interface AudienceReachCardProps {
  totalCount?: number;
  avgFollowers?: string;
  avgReach?: string;
  topCreators?: CreatorHighlight[];
}

export const AudienceReachCard: React.FC<AudienceReachCardProps> = ({
  totalCount = 65,
  avgFollowers = '35K',
  avgReach = '11K',
  topCreators,
}) => {
  const defaultCreators: CreatorHighlight[] = [
    { name: 'Nazima Mogra', follower_str: '62.0K' },
    { name: 'Isabella Quintero', follower_str: '36.8K' },
    { name: 'Dhanu Gunathissa', follower_str: '92.0K' },
    { name: 'Rashonda Wisner', follower_str: '24.5K' },
  ];

  const creatorsToDisplay = topCreators && topCreators.length > 0 ? topCreators.slice(0, 4) : defaultCreators;

  return (
    <div className="bg-white border border-[#E2E8F0] hover:border-[#BAE6FD] rounded-[20px] p-5 shadow-[0_4px_20px_rgba(0,0,0,0.04)] hover:shadow-[0_12px_28px_-6px_rgba(2,132,199,0.08)] transition-all h-full flex flex-col justify-between">
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

        <div className="border-t border-[#E2E8F0] my-3"></div>
      </div>

      <div>
        <div className="text-[11px] font-extrabold text-black uppercase tracking-wider mb-2">
          Top Qualified Creators
        </div>

        <div className="space-y-1.5">
          {creatorsToDisplay.map((creator, idx) => (
            <div
              key={idx}
              className={`bg-[#F8FAFC] border rounded-xl px-3 py-2 flex justify-between items-center transition-all ${
                idx === 2 ? 'border-[#BAE6FD]' : 'border-[#E2E8F0]'
              }`}
            >
              <span className="text-sm font-bold text-black">{creator.name}</span>
              <span className="font-mono text-xs font-black text-black">{creator.follower_str}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AudienceReachCard;
