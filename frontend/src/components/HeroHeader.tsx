import React from 'react';
import NavbarActionButton from './ui/NavbarActionButton';

export const HeroHeader: React.FC = () => {
  return (
    <div className="flex flex-col items-center text-center pb-6">
      <div className="inline-flex items-center gap-2.5 bg-white border border-[#BAE6FD] px-4 py-1.5 rounded-full shadow-[0_2px_8px_rgba(0,0,0,0.03)] mb-3">
        <NavbarActionButton />
        <span className="font-bold text-sm text-black tracking-tight">Goscraping &nbsp;|&nbsp; EDXSO</span>
      </div>
      <h1 className="text-4xl md:text-5xl font-black text-black tracking-[-1.2px] m-0 leading-tight">
        Dashboard scraping
      </h1>
      <p className="text-base font-semibold text-[#222222] mt-2 max-w-xl leading-relaxed">
        Dashboard is developed for scraping data from multiple known platforms
      </p>
    </div>
  );
};

export default HeroHeader;
