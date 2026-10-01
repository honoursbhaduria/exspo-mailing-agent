import React from 'react';
import { ChevronLeft, ChevronRight, ChevronsLeft, ChevronsRight, ChevronDown } from 'lucide-react';

export interface PaginationProps {
  currentPage: number;
  totalPages: number;
  pageSize: number;
  totalItems: number;
  pageSizeOptions?: number[];
  onPageChange: (page: number) => void;
  onPageSizeChange?: (size: number) => void;
  itemLabel?: string;
}

export const Pagination: React.FC<PaginationProps> = ({
  currentPage,
  totalPages,
  pageSize,
  totalItems,
  pageSizeOptions = [10, 20, 50, 100],
  onPageChange,
  onPageSizeChange,
  itemLabel = 'records',
}) => {
  const safeTotalPages = Math.max(1, totalPages);
  const startItem = totalItems === 0 ? 0 : (currentPage - 1) * pageSize + 1;
  const endItem = Math.min(currentPage * pageSize, totalItems);

  // Generate page numbers with ellipses
  const getPageNumbers = () => {
    const pages: (number | string)[] = [];
    if (safeTotalPages <= 7) {
      for (let i = 1; i <= safeTotalPages; i++) {
        pages.push(i);
      }
    } else {
      pages.push(1);
      if (currentPage > 3) {
        pages.push('...');
      }
      const start = Math.max(2, currentPage - 1);
      const end = Math.min(safeTotalPages - 1, currentPage + 1);
      for (let i = start; i <= end; i++) {
        pages.push(i);
      }
      if (currentPage < safeTotalPages - 2) {
        pages.push('...');
      }
      pages.push(safeTotalPages);
    }
    return pages;
  };

  return (
    <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-4 mt-2 border-t border-[#E2E8F0]">
      {/* Left: Summary text */}
      <div className="flex items-center gap-3">
        <span className="text-xs font-black text-black">
          Showing <span className="underline decoration-[#38BDF8] decoration-2">{startItem}</span> to{' '}
          <span className="underline decoration-[#38BDF8] decoration-2">{endItem}</span> of{' '}
          <span className="font-mono bg-[#E0F2FE] px-1.5 py-0.5 rounded border border-[#BAE6FD] text-black">
            {totalItems}
          </span>{' '}
          {itemLabel}
        </span>

        {/* Page Size Selector */}
        {onPageSizeChange && (
          <div className="flex items-center gap-1.5 ml-2">
            <span className="text-xs font-black text-black">Rows:</span>
            <div className="relative">
              <select
                value={pageSize}
                onChange={(e) => {
                  onPageSizeChange(Number(e.target.value));
                  onPageChange(1);
                }}
                className="appearance-none bg-[#F8FAFC] hover:bg-white focus:bg-white border border-[#CBD5E1] hover:border-black focus:border-black rounded-lg px-2.5 py-1 pr-6 text-xs font-black text-black cursor-pointer shadow-xs transition-all focus:outline-none"
              >
                {pageSizeOptions.map((opt) => (
                  <option key={opt} value={opt} className="bg-white text-black font-bold">
                    {opt}
                  </option>
                ))}
              </select>
              <div className="pointer-events-none absolute right-1.5 top-1/2 -translate-y-1/2 flex items-center">
                <ChevronDown className="w-3.5 h-3.5 text-black stroke-[2.5]" />
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Right: Interactive Navigation Buttons */}
      <div className="flex items-center gap-1.5">
        {/* First Page */}
        <button
          onClick={() => onPageChange(1)}
          disabled={currentPage === 1}
          title="First Page"
          className="p-1.5 rounded-lg border border-[#CBD5E1] bg-white text-black hover:bg-[#F0F9FF] disabled:opacity-30 disabled:hover:bg-white disabled:cursor-not-allowed transition-all cursor-pointer"
        >
          <ChevronsLeft className="w-4 h-4 text-black stroke-[2.5]" />
        </button>

        {/* Prev Page */}
        <button
          onClick={() => onPageChange(currentPage - 1)}
          disabled={currentPage === 1}
          title="Previous Page"
          className="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg border border-[#CBD5E1] bg-white text-black font-black text-xs hover:bg-[#F0F9FF] disabled:opacity-30 disabled:hover:bg-white disabled:cursor-not-allowed transition-all cursor-pointer"
        >
          <ChevronLeft className="w-3.5 h-3.5 text-black stroke-[2.5]" />
          <span>Prev</span>
        </button>

        {/* Page Number Buttons */}
        <div className="hidden sm:flex items-center gap-1">
          {getPageNumbers().map((p, idx) => {
            if (p === '...') {
              return (
                <span key={`ellipsis-${idx}`} className="px-2 py-1 text-xs font-black text-black">
                  ...
                </span>
              );
            }
            const isCurrent = p === currentPage;
            return (
              <button
                key={`page-${p}`}
                onClick={() => onPageChange(p as number)}
                className={`min-w-8 h-8 px-2 text-xs font-black rounded-lg border transition-all cursor-pointer ${
                  isCurrent
                    ? 'bg-[#BAE6FD] border-black text-black shadow-sm scale-105'
                    : 'bg-white border-[#CBD5E1] hover:bg-[#F0F9FF] hover:border-black text-black'
                }`}
              >
                {p}
              </button>
            );
          })}
        </div>

        {/* Next Page */}
        <button
          onClick={() => onPageChange(currentPage + 1)}
          disabled={currentPage >= safeTotalPages}
          title="Next Page"
          className="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg border border-[#CBD5E1] bg-white text-black font-black text-xs hover:bg-[#F0F9FF] disabled:opacity-30 disabled:hover:bg-white disabled:cursor-not-allowed transition-all cursor-pointer"
        >
          <span>Next</span>
          <ChevronRight className="w-3.5 h-3.5 text-black stroke-[2.5]" />
        </button>

        {/* Last Page */}
        <button
          onClick={() => onPageChange(safeTotalPages)}
          disabled={currentPage >= safeTotalPages}
          title="Last Page"
          className="p-1.5 rounded-lg border border-[#CBD5E1] bg-white text-black hover:bg-[#F0F9FF] disabled:opacity-30 disabled:hover:bg-white disabled:cursor-not-allowed transition-all cursor-pointer"
        >
          <ChevronsRight className="w-4 h-4 text-black stroke-[2.5]" />
        </button>
      </div>
    </div>
  );
};

export default Pagination;
