import React from 'react';
import NavbarActionButton from './ui/NavbarActionButton';
import type { DatabaseStatus } from '../services/api';

export interface HeroHeaderProps {
  dbStatus?: DatabaseStatus | null;
}

export const HeroHeader: React.FC<HeroHeaderProps> = () => {
  return (
    <div className="flex flex-col items-center text-center pb-4 sm:pb-6 px-2">
      <div className="flex flex-wrap items-center justify-center gap-2 mb-2.5 sm:mb-3">
        <div className="inline-flex items-center gap-2 bg-white border border-[#BAE6FD] px-3 py-1 sm:px-4 sm:py-1.5 rounded-full shadow-[0_2px_8px_rgba(0,0,0,0.03)]">
          <NavbarActionButton />
          <span className="font-bold text-xs sm:text-sm text-black tracking-tight">Goscraping &nbsp;|&nbsp; EDXSO</span>
        </div>
      </div>

      <h1 className="text-2xl sm:text-4xl md:text-5xl font-black text-black tracking-[-0.8px] sm:tracking-[-1.2px] m-0 leading-tight">
        Dashboard scraping
      </h1>
      <p className="text-xs sm:text-sm md:text-base font-semibold text-[#222222] mt-1.5 sm:mt-2 max-w-xl leading-relaxed px-2">
        Dashboard is developed for scraping data from multiple known platforms
      </p>
    </div>
  );
};

export default HeroHeader;
