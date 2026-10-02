import React from 'react';
import NavbarActionButton from './ui/NavbarActionButton';
import { Database } from 'lucide-react';
import type { DatabaseStatus } from '../services/api';

export interface HeroHeaderProps {
  dbStatus?: DatabaseStatus | null;
}

export const HeroHeader: React.FC<HeroHeaderProps> = ({ dbStatus }) => {
  return (
    <div className="flex flex-col items-center text-center pb-6">
      <div className="flex flex-wrap items-center justify-center gap-2 mb-3">
        <div className="inline-flex items-center gap-2.5 bg-white border border-[#BAE6FD] px-4 py-1.5 rounded-full shadow-[0_2px_8px_rgba(0,0,0,0.03)]">
          <NavbarActionButton />
          <span className="font-bold text-sm text-black tracking-tight">Goscraping &nbsp;|&nbsp; EDXSO</span>
        </div>

        {dbStatus && (
          <div className="inline-flex items-center gap-1.5 bg-white border border-[#CBD5E1] px-3 py-1.5 rounded-full shadow-[0_2px_8px_rgba(0,0,0,0.02)]">
            <span className="w-2 h-2 rounded-full bg-emerald-500 inline-block animate-pulse" />
            <Database className="w-3.5 h-3.5 text-black" />
            <span className="font-black text-xs text-black font-mono">
              {dbStatus.engine} ({dbStatus.total_records} records)
            </span>
          </div>
        )}
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
