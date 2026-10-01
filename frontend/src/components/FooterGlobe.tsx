import React from 'react';
import Globe3DDemo from './ui/Globe3DDemo';

export const FooterGlobe: React.FC = () => {
  return (
    <div className="mt-8 mb-10">
      <div className="bg-white border border-[#E2E8F0] rounded-[20px] p-6 shadow-[0_8px_24px_-6px_rgba(0,0,0,0.04)] mb-4">
        <div className="flex justify-between items-center">
          <div>
            <h3 className="text-lg font-black text-black">Global Creator Outreach Radar</h3>
            <p className="text-xs font-semibold text-[#222222] mt-1">
              Interactive 3D WebGL Globe rendering active influencer hubs across North America, Europe, Asia, and Oceania.
            </p>
          </div>
          <span className="font-mono text-xs font-black bg-[#F1F5F9] border border-[#CBD5E1] text-black px-3 py-1 rounded-full">
            3D WebGL Powered
          </span>
        </div>
      </div>

      <div className="bg-white border border-[#E2E8F0] rounded-[20px] p-4 shadow-[0_8px_24px_-6px_rgba(0,0,0,0.04)] overflow-hidden">
        <Globe3DDemo />
      </div>
    </div>
  );
};

export default FooterGlobe;
