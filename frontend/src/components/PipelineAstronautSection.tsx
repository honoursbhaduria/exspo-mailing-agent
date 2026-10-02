import React, { useState } from 'react';
import { Search, Users, CheckCircle2, Sparkles, Send, Database, ArrowRight, RefreshCw } from 'lucide-react';

interface StageInfo {
  id: string;
  step: number;
  title: string;
  subtitle: string;
  description: string;
  metric: string;
  status: string;
  technologies: string[];
}

const STAGES: StageInfo[] = [
  {
    id: 'discovery',
    step: 1,
    title: 'Scrapy Discovery',
    subtitle: 'Crawls & parses authentic creator profiles',
    description: 'High-speed asynchronous crawling engine collecting public metrics, handles, platforms, follower counts, and locations.',
    metric: '273 Profiles Indexed',
    status: 'ACTIVE PIPELINE',
    technologies: ['Scrapy', 'Playwright', 'FastAPI'],
  },
  {
    id: 'enrichment',
    step: 2,
    title: 'Profile Enrichment',
    subtitle: 'Extracts bio themes & demographics',
    description: 'Enriches raw creator records with verified audience age cohorts, gender breakdown, verified brand contact emails, and NLP content themes.',
    metric: '100% Verified Fields',
    status: 'ENRICHED',
    technologies: ['NLP Parser', 'Zero-Hallucination Email', 'Geo Mapping'],
  },
  {
    id: 'classification',
    step: 3,
    title: 'Classification Engine',
    subtitle: 'Quantitative filtering & eligibility',
    description: 'Enforces strict micro-influencer bounds (5k - 100k), minimum 0.8% engagement threshold, platform compatibility, and regional audience targeting.',
    metric: 'Deterministic Filtering',
    status: 'AUTOMATED',
    technologies: ['Config Rules', 'Multi-Factor Scorer', 'Audience Geo'],
  },
  {
    id: 'personalization',
    step: 4,
    title: 'Gemini AI Studio',
    subtitle: 'Dual-pitch hyper-personalization',
    description: 'Dynamic LLM pipeline generating tailored Email pitches (60–90 words) and high-conversion Instagram DMs (15–30 words) customized to creator themes.',
    metric: 'Exact Word-Count Enforced',
    status: 'INTELLIGENT',
    technologies: ['Google Gemini', 'Pydantic Validators', 'NLP Hooks'],
  },
  {
    id: 'outreach',
    step: 5,
    title: 'Dispatch & Audit Tracker',
    subtitle: 'Transactional delivery & deduplication',
    description: 'Dispatches live emails through Resend API (or safe sandbox) and routes Instagram DM messages with duplicate contact prevention and audit logging.',
    metric: '173 Logged Events',
    status: 'DISPATCHED',
    technologies: ['Resend API', 'Deduplication Hash', 'SQLite Tracker'],
  },
];

export const PipelineAstronautSection: React.FC = () => {
  const [activeStageIndex, setActiveStageIndex] = useState<number>(0);
  const activeStage = STAGES[activeStageIndex];

  // Circular coordinates for 5 nodes on a 520x520 canvas with center (260, 260) and radius 180
  const center = 260;
  const radius = 175;
  
  // Angles in degrees starting from top (-90 deg) going clockwise: -90, -18, 54, 126, 198
  const angles = [-90, -18, 54, 126, 198];
  const nodePositions = angles.map((deg) => {
    const rad = (deg * Math.PI) / 180;
    return {
      x: Math.round(center + radius * Math.cos(rad)),
      y: Math.round(center + radius * Math.sin(rad)),
    };
  });

  const getStageIcon = (step: number) => {
    switch (step) {
      case 1: return <Search className="w-4 h-4" />;
      case 2: return <Users className="w-4 h-4" />;
      case 3: return <CheckCircle2 className="w-4 h-4" />;
      case 4: return <Sparkles className="w-4 h-4" />;
      case 5: return <Send className="w-4 h-4" />;
      default: return <Database className="w-4 h-4" />;
    }
  };

  return (
    <div className="bg-white border border-[#E2E8F0] hover:border-[#BAE6FD] rounded-[20px] p-5 sm:p-6 shadow-[0_4px_24px_rgba(0,0,0,0.04)] mb-8 transition-all">
      {/* Header matching standard dashboard card typography */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-[#E2E8F0] pb-4 mb-6">
        <div>
          <div className="text-[11px] font-bold text-[#64748B] uppercase tracking-wider mb-1">
            Automated Pipeline Architecture
          </div>
          <h2 className="text-xl font-black text-black tracking-tight">
            End-to-End Autonomous Outreach Flow
          </h2>
          <p className="text-xs font-semibold text-[#333333] mt-0.5">
            Circular multi-phase workflow orbiting around autonomous AI orchestration
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => setActiveStageIndex((prev) => (prev + 1) % STAGES.length)}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-[#F8FAFC] hover:bg-white border border-[#CBD5E1] hover:border-black text-xs font-black text-black rounded-xl transition-all cursor-pointer shadow-xs"
          >
            <RefreshCw className="w-3.5 h-3.5 text-black" />
            <span>Next Phase</span>
          </button>
        </div>
      </div>

      {/* Main Grid: Circular Flowchart (Left/Center) + Active Stage Info (Right) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
        {/* Circular Flowchart Orbit Section */}
        <div className="lg:col-span-7 flex flex-col items-center justify-center relative select-none">
          <div className="relative w-full max-w-[440px] aspect-square flex items-center justify-center">
            {/* SVG Orbit Tracks & Directional Flow */}
            <svg
              className="absolute inset-0 w-full h-full pointer-events-none"
              viewBox="0 0 520 520"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              {/* Outer Guide Ring */}
              <circle
                cx="260"
                cy="260"
                r="175"
                stroke="#E2E8F0"
                strokeWidth="2"
                strokeDasharray="4 4"
              />

              {/* Inner Active Pulse Ring */}
              <circle
                cx="260"
                cy="260"
                r="105"
                stroke="#BAE6FD"
                strokeWidth="1.5"
                strokeDasharray="6 6"
                className="opacity-70"
              />

              {/* Orbital Connecting Curved Segments */}
              {nodePositions.map((pos, i) => {
                const nextPos = nodePositions[(i + 1) % nodePositions.length];
                const isActiveTransition = i === activeStageIndex;
                return (
                  <path
                    key={`orbit-path-${i}`}
                    d={`M ${pos.x} ${pos.y} A 175 175 0 0 1 ${nextPos.x} ${nextPos.y}`}
                    stroke={isActiveTransition ? '#0284C7' : '#CBD5E1'}
                    strokeWidth={isActiveTransition ? '3' : '1.5'}
                    fill="none"
                    strokeLinecap="round"
                  />
                );
              })}
            </svg>

            {/* Center Astronaut Illustration with Smooth Floating CSS Animation */}
            <div className="relative z-10 flex flex-col items-center justify-center p-3 rounded-full bg-white border border-[#CBD5E1] shadow-[0_6px_20px_rgba(0,0,0,0.06)] w-36 h-36 sm:w-44 sm:h-44 transition-all">
              <div className="animate-astronaut-float flex flex-col items-center justify-center">
                {/* Clean Vector Astronaut SVG (Zero Gradients, Crisp Black & White Vector) */}
                <svg
                  width="72"
                  height="72"
                  viewBox="0 0 64 64"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                  className="w-14 h-14 sm:w-16 sm:h-16"
                >
                  {/* Helmet Dome */}
                  <circle cx="32" cy="20" r="13" fill="#FFFFFF" stroke="#000000" strokeWidth="2.5" />
                  
                  {/* Visor */}
                  <rect x="23" y="14" width="18" height="11" rx="5.5" fill="#0284C7" stroke="#000000" strokeWidth="2" />
                  <path d="M26 17 C 28 15, 33 15, 36 17" stroke="#FFFFFF" strokeWidth="1.5" strokeLinecap="round" opacity="0.9" />

                  {/* Helmet Antenna */}
                  <line x1="32" y1="7" x2="32" y2="4" stroke="#000000" strokeWidth="2" strokeLinecap="round" />
                  <circle cx="32" cy="3" r="1.5" fill="#000000" />

                  {/* Spacesuit Torso */}
                  <path d="M20 33 C20 28, 44 28, 44 33 L45 47 C45 49, 43 51, 40 51 L24 51 C21 51, 19 49, 19 47 Z" fill="#FFFFFF" stroke="#000000" strokeWidth="2.5" />

                  {/* Life Support Chest Pack */}
                  <rect x="25" y="32" width="14" height="11" rx="2" fill="#F8FAFC" stroke="#000000" strokeWidth="1.5" />
                  <circle cx="29" cy="36" r="1.5" fill="#0284C7" />
                  <circle cx="35" cy="36" r="1.5" fill="#22C55E" />
                  <line x1="28" y1="40" x2="36" y2="40" stroke="#000000" strokeWidth="1.2" strokeLinecap="round" />

                  {/* Arms */}
                  <path d="M19 33 C14 36, 12 42, 14 47 C14.5 48, 16 48, 17 47 C16 43, 18 39, 21 37" fill="#FFFFFF" stroke="#000000" strokeWidth="2" />
                  <path d="M45 33 C50 36, 52 42, 50 47 C49.5 48, 48 48, 47 47 C48 43, 46 39, 43 37" fill="#FFFFFF" stroke="#000000" strokeWidth="2" />

                  {/* Legs */}
                  <path d="M24 51 L23 60 C23 61, 25 62, 27 62 L29 62 C29 60, 29 55, 29 51" fill="#FFFFFF" stroke="#000000" strokeWidth="2" />
                  <path d="M40 51 L41 60 C41 61, 39 62, 37 62 L35 62 C35 60, 35 55, 35 51" fill="#FFFFFF" stroke="#000000" strokeWidth="2" />

                  {/* Backpack Tanks */}
                  <rect x="15" y="30" width="5" height="15" rx="2.5" fill="#F1F5F9" stroke="#000000" strokeWidth="1.8" />
                  <rect x="44" y="30" width="5" height="15" rx="2.5" fill="#F1F5F9" stroke="#000000" strokeWidth="1.8" />
                </svg>

                <div className="text-[10px] font-black text-black tracking-tight text-center mt-1">
                  EDXSO CORE
                </div>
                <div className="text-[9px] font-bold text-[#0284C7] uppercase tracking-wider text-center">
                  Autonomous AI
                </div>
              </div>
            </div>

            {/* Orbiting Flowchart Nodes Surrounding Astronaut */}
            {STAGES.map((stage, idx) => {
              const pos = nodePositions[idx];
              const isSelected = activeStageIndex === idx;

              // Calculate percentages for responsive placement
              const leftPercent = (pos.x / 520) * 100;
              const topPercent = (pos.y / 520) * 100;

              return (
                <button
                  key={stage.id}
                  type="button"
                  onClick={() => setActiveStageIndex(idx)}
                  style={{
                    left: `${leftPercent}%`,
                    top: `${topPercent}%`,
                    transform: 'translate(-50%, -50%)',
                  }}
                  className={`absolute z-20 flex items-center gap-2 px-2.5 sm:px-3 py-1.5 sm:py-2 rounded-xl transition-all cursor-pointer shadow-xs border ${
                    isSelected
                      ? 'bg-black text-white border-black scale-105 shadow-md'
                      : 'bg-white hover:bg-[#F8FAFC] text-black border-[#CBD5E1] hover:border-black'
                  }`}
                >
                  <div
                    className={`w-6 h-6 rounded-lg flex items-center justify-center shrink-0 ${
                      isSelected ? 'bg-white text-black' : 'bg-[#E0F2FE] text-[#0284C7]'
                    }`}
                  >
                    {getStageIcon(stage.step)}
                  </div>
                  <div className="text-left hidden sm:block">
                    <div className="text-[11px] font-black leading-tight whitespace-nowrap">
                      {stage.step}. {stage.title}
                    </div>
                  </div>
                  <div className="sm:hidden font-mono text-[11px] font-black">
                    {stage.step}
                  </div>
                </button>
              );
            })}
          </div>

          <div className="text-[11px] font-bold text-[#64748B] mt-2 text-center">
            Click any orbiting node to inspect pipeline phase
          </div>
        </div>

        {/* Right Column: Selected Flowchart Stage Detail Card */}
        <div className="lg:col-span-5 bg-[#F8FAFC] border border-[#CBD5E1] rounded-2xl p-4 sm:p-5 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between gap-2 mb-2">
              <span className="font-mono text-xs font-black text-black bg-white border border-[#CBD5E1] px-2.5 py-1 rounded-md">
                PHASE 0{activeStage.step} OF 05
              </span>
              <span className="text-[10px] font-black text-[#0284C7] bg-[#E0F2FE] border border-[#BAE6FD] px-2.5 py-1 rounded-md">
                {activeStage.status}
              </span>
            </div>

            <h3 className="text-lg font-black text-black flex items-center gap-2 mt-2">
              {getStageIcon(activeStage.step)}
              {activeStage.title}
            </h3>
            <p className="text-xs font-bold text-[#0284C7] mt-0.5">
              {activeStage.subtitle}
            </p>

            <p className="text-xs font-medium text-[#222222] mt-3 leading-relaxed">
              {activeStage.description}
            </p>

            <div className="border-t border-[#E2E8F0] my-4" />

            <div className="space-y-2">
              <div className="text-[11px] font-extrabold text-black uppercase tracking-wider">
                Key Deliverable / Metric
              </div>
              <div className="font-mono text-sm font-black text-black bg-white border border-[#CBD5E1] px-3 py-2 rounded-xl">
                {activeStage.metric}
              </div>
            </div>

            <div className="mt-4">
              <div className="text-[11px] font-extrabold text-black uppercase tracking-wider mb-2">
                Engine &amp; Technologies
              </div>
              <div className="flex flex-wrap gap-1.5">
                {activeStage.technologies.map((tech) => (
                  <span
                    key={tech}
                    className="text-[10px] font-bold text-black bg-white border border-[#CBD5E1] px-2 py-0.5 rounded-md"
                  >
                    {tech}
                  </span>
                ))}
              </div>
            </div>
          </div>

          <div className="mt-5 pt-3 border-t border-[#E2E8F0] flex items-center justify-between">
            <span className="text-xs font-bold text-[#333333]">Next in sequence:</span>
            <button
              type="button"
              onClick={() => setActiveStageIndex((prev) => (prev + 1) % STAGES.length)}
              className="inline-flex items-center gap-1 text-xs font-black text-black hover:underline cursor-pointer"
            >
              <span>{STAGES[(activeStageIndex + 1) % STAGES.length].title}</span>
              <ArrowRight className="w-3.5 h-3.5 text-black" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PipelineAstronautSection;
