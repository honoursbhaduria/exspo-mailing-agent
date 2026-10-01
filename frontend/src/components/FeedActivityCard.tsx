import React from 'react';
import { Globe, CheckCircle2, XCircle } from 'lucide-react';

export const FeedActivityCard: React.FC = () => {
  const feedItems = [
    { name: 'Alina Paziuk', loc: 'London, UK', status: 'PASS', pass: true, tag: 'PASS' },
    { name: 'Cameron Stokes', loc: 'Athens, US', status: 'PASS', pass: true, tag: 'PASS' },
    { name: 'Katarina Durcakova', loc: 'Slovakia', status: 'FAIL', pass: false, tag: '< 5k' },
    { name: 'Allee-Sutton H.', loc: 'Nashville, US', status: 'PASS', pass: true, tag: 'PASS' },
    { name: 'Jordy Boulet-Viau', loc: 'Montreal, CA', status: 'FAIL', pass: false, tag: '> 100k' },
  ];

  return (
    <div className="bg-white border border-[#E2E8F0] hover:border-[#BAE6FD] rounded-[20px] p-5 shadow-[0_4px_20px_rgba(0,0,0,0.04)] hover:shadow-[0_12px_28px_-6px_rgba(2,132,199,0.08)] transition-all h-full flex flex-col justify-between">
      <div>
        <div className="flex justify-between items-center mb-4">
          <span className="font-extrabold text-base text-black">Feed & Activity</span>
          <span className="inline-flex items-center gap-1.5 bg-[#F1F5F9] text-black border border-[#CBD5E1] text-xs font-bold px-2.5 py-0.5 rounded-full">
            <Globe className="w-3 h-3 text-black" /> Global
          </span>
        </div>

        <div className="divide-y divide-[#E2E8F0]">
          {feedItems.map((item, idx) => (
            <div key={idx} className="py-2.5 flex justify-between items-center first:pt-0 last:pb-0">
              <div>
                <div className="text-sm font-bold text-black">{item.name}</div>
                <div className="font-mono text-xs font-semibold text-[#333333]">{item.loc}</div>
              </div>
              <span
                className={`inline-flex items-center gap-1 text-xs font-black px-2.5 py-0.5 rounded-full border ${
                  item.pass
                    ? 'bg-[#DCFCE7] text-black border-[#86EFAC]'
                    : 'bg-[#FEE2E2] text-black border-[#FCA5A5]'
                }`}
              >
                {item.pass ? (
                  <CheckCircle2 className="w-3 h-3 text-black" />
                ) : (
                  <XCircle className="w-3 h-3 text-black" />
                )}
                {item.tag}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default FeedActivityCard;
