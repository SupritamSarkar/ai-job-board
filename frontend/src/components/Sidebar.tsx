import React from 'react';
import { Search, Briefcase, DollarSign, Calendar, RotateCcw } from 'lucide-react';

interface FilterState {
  location: string;
  experience: string;
  isRemote: boolean;
  isHybrid: boolean;
  isOnsite: boolean;
  site: string;
  salaryDisclosed: boolean;
  company: string;
  daysAgo: string;
  countryFilter: string;
}

interface SidebarProps {
  filters: FilterState;
  setFilters: React.Dispatch<React.SetStateAction<FilterState>>;
  onClearFilters: () => void;
  totalJobs: number;
  filteredCount: number;
}

const Sidebar: React.FC<SidebarProps> = ({ filters, setFilters, onClearFilters, totalJobs, filteredCount }) => {

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    if (type === 'checkbox') {
      setFilters(prev => ({ ...prev, [name]: (e.target as HTMLInputElement).checked }));
    } else {
      setFilters(prev => ({ ...prev, [name]: value }));
    }
  };

  const hasActiveFilters =
    filters.location !== '' ||
    filters.experience !== '' ||
    filters.isRemote ||
    filters.salaryDisclosed ||
    filters.company !== '' ||
    filters.daysAgo !== '';

  return (
    <aside className="w-full md:w-72 md:shrink-0 h-fit md:sticky md:top-24 md:max-h-[calc(100vh-120px)] md:overflow-y-auto no-scrollbar">
      <div className="space-y-5 rounded-xl border border-zinc-800 bg-zinc-900/60 p-5">

        {/* Header with Stats */}
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-bold text-white">Filters</h2>
            <p className="text-xs text-zinc-500 mt-0.5">
              {filteredCount} of {totalJobs} jobs
            </p>
          </div>
          {hasActiveFilters && (
            <button
              onClick={onClearFilters}
              className="flex items-center gap-1.5 rounded-lg bg-zinc-800 px-2.5 py-1.5 text-xs font-medium text-zinc-400 transition-colors hover:bg-zinc-700 hover:text-white"
            >
              <RotateCcw className="h-3 w-3" />
              Clear
            </button>
          )}
        </div>

        {/* Divider */}
        <div className="h-px bg-zinc-800"></div>

        {/* Company Search */}
        <div className="space-y-2">
          <label className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-zinc-400">
            <Search className="h-3.5 w-3.5" />
            Company
          </label>
          <input
            type="text"
            name="company"
            value={filters.company}
            onChange={handleChange}
            placeholder="Search by company..."
            className="w-full rounded-lg border border-zinc-800 bg-zinc-900 px-3 py-2.5 text-sm text-zinc-300 placeholder-zinc-600 transition-colors focus:border-zinc-600 focus:outline-none"
          />
        </div>

        {/* Location Search */}
        <div className="space-y-2">
          <label className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-zinc-400">
            <svg className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            Location
          </label>
          <input
            type="text"
            name="location"
            value={filters.location}
            onChange={handleChange}
            placeholder="e.g. Bangalore, New York"
            className="w-full rounded-lg border border-zinc-800 bg-zinc-900 px-3 py-2.5 text-sm text-zinc-300 placeholder-zinc-600 transition-colors focus:border-zinc-600 focus:outline-none"
          />
        </div>

        {/* Experience */}
        <div className="space-y-2">
          <label className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-zinc-400">
            <Briefcase className="h-3.5 w-3.5" />
            Experience
          </label>
          <select
            name="experience"
            value={filters.experience}
            onChange={handleChange}
            className="w-full rounded-lg border border-zinc-800 bg-zinc-900 px-3 py-2.5 text-sm text-zinc-300 transition-colors focus:border-zinc-600 focus:outline-none cursor-pointer"
          >
            <option value="">Any Experience</option>
            <option value="Fresher">Freshers (0-1 Years)</option>
            <option value="1-3">Early Career (1-3 Years)</option>
            <option value="3-5">Mid Level (3-5 Years)</option>
            <option value="5-10">Senior (5-10 Years)</option>
            <option value="10+">Expert (10+ Years)</option>
          </select>
        </div>

        {/* Posted Within */}
        <div className="space-y-2">
          <label className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-zinc-400">
            <Calendar className="h-3.5 w-3.5" />
            Posted Within
          </label>
          <select
            name="daysAgo"
            value={filters.daysAgo}
            onChange={handleChange}
            className="w-full rounded-lg border border-zinc-800 bg-zinc-900 px-3 py-2.5 text-sm text-zinc-300 transition-colors focus:border-zinc-600 focus:outline-none cursor-pointer"
          >
            <option value="">Any Time</option>
            <option value="1">Last 24 Hours</option>
            <option value="3">Last 3 Days</option>
            <option value="7">Last 7 Days</option>
            <option value="14">Last 14 Days</option>
          </select>
        </div>

        {/* Divider */}
        <div className="h-px bg-zinc-800"></div>

        {/* Toggle Filters */}
        <div className="space-y-3">
          {/* Remote Toggle */}
          <label className="flex items-center justify-between cursor-pointer group">
            <span className="text-sm text-zinc-400 group-hover:text-white transition-colors">Remote Only</span>
            <div className="relative">
              <input
                type="checkbox"
                name="isRemote"
                checked={filters.isRemote}
                onChange={handleChange}
                className="peer sr-only"
              />
              <div className="h-6 w-11 rounded-full bg-zinc-800 peer-checked:bg-white transition-all"></div>
              <div className="absolute left-1 top-1 h-4 w-4 rounded-full bg-zinc-500 transition-all peer-checked:translate-x-5 peer-checked:bg-black"></div>
            </div>
          </label>

          {/* Salary Disclosed Toggle */}
          <label className="flex items-center justify-between cursor-pointer group">
            <div className="flex items-center gap-2">
              <DollarSign className="h-4 w-4 text-zinc-500 group-hover:text-emerald-400 transition-colors" />
              <span className="text-sm text-zinc-400 group-hover:text-white transition-colors">Salary Disclosed</span>
            </div>
            <div className="relative">
              <input
                type="checkbox"
                name="salaryDisclosed"
                checked={filters.salaryDisclosed}
                onChange={handleChange}
                className="peer sr-only"
              />
              <div className="h-6 w-11 rounded-full bg-zinc-800 peer-checked:bg-emerald-500 transition-all"></div>
              <div className="absolute left-1 top-1 h-4 w-4 rounded-full bg-zinc-500 transition-all peer-checked:translate-x-5 peer-checked:bg-white"></div>
            </div>
          </label>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;