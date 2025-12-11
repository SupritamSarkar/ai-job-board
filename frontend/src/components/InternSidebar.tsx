import React from 'react';
import { Search, Calendar, RotateCcw } from 'lucide-react';

interface InternFilterState {
    location: string;
    site: string;
    salaryDisclosed: boolean;
    company: string;
    daysAgo: string;
    isPaid: boolean;
    countryFilter: string;
}

interface InternSidebarProps {
    filters: InternFilterState;
    setFilters: React.Dispatch<React.SetStateAction<InternFilterState>>;
    onClearFilters: () => void;
    totalInterns: number;
    filteredCount: number;
}

const InternSidebar: React.FC<InternSidebarProps> = ({ filters, setFilters, onClearFilters, totalInterns, filteredCount }) => {

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
        filters.site !== 'All' ||
        filters.salaryDisclosed ||
        filters.company !== '' ||
        filters.daysAgo !== '' ||
        filters.isPaid;

    return (
        <aside className="w-full md:w-72 md:shrink-0 h-fit md:sticky md:top-24 md:max-h-[calc(100vh-120px)] md:overflow-y-auto no-scrollbar">
            <div className="space-y-5 rounded-xl border border-purple-900/50 bg-zinc-900/60 p-5">

                {/* Header with Stats */}
                <div className="flex items-center justify-between">
                    <div>
                        <h2 className="text-lg font-bold text-white">Filters</h2>
                        <p className="text-xs text-zinc-500 mt-0.5">
                            {filteredCount} of {totalInterns} internships
                        </p>
                    </div>
                    {hasActiveFilters && (
                        <button
                            onClick={onClearFilters}
                            className="flex items-center gap-1.5 rounded-lg bg-purple-900/30 px-2.5 py-1.5 text-xs font-medium text-purple-300 transition-colors hover:bg-purple-800/40 hover:text-white"
                        >
                            <RotateCcw className="h-3 w-3" />
                            Clear
                        </button>
                    )}
                </div>

                {/* Divider */}
                <div className="h-px bg-purple-900/50"></div>

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
                        className="w-full rounded-lg border border-purple-900/50 bg-zinc-900 px-3 py-2.5 text-sm text-zinc-300 placeholder-zinc-600 transition-colors focus:border-purple-500 focus:outline-none"
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
                        className="w-full rounded-lg border border-purple-900/50 bg-zinc-900 px-3 py-2.5 text-sm text-zinc-300 placeholder-zinc-600 transition-colors focus:border-purple-500 focus:outline-none"
                    />
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
                        className="w-full rounded-lg border border-purple-900/50 bg-zinc-900 px-3 py-2.5 text-sm text-zinc-300 transition-colors focus:border-purple-500 focus:outline-none cursor-pointer"
                    >
                        <option value="">Any Time</option>
                        <option value="1">Last 24 Hours</option>
                        <option value="3">Last 3 Days</option>
                        <option value="7">Last 7 Days</option>
                        <option value="14">Last 14 Days</option>
                    </select>
                </div>

                {/* Site Source */}
                <div className="space-y-2">
                    <label className="text-xs font-semibold uppercase tracking-wider text-zinc-400">Source</label>
                    <div className="flex gap-2">
                        {['All', 'Indeed', 'Naukri'].map((site) => (
                            <button
                                key={site}
                                onClick={() => setFilters(prev => ({ ...prev, site }))}
                                className={`flex-1 rounded-lg px-2 py-2 text-xs font-medium transition-all duration-200 ${filters.site === site
                                    ? 'bg-purple-500 text-white'
                                    : 'bg-zinc-800 text-zinc-400 hover:bg-zinc-700 hover:text-white'
                                    }`}
                            >
                                {site}
                            </button>
                        ))}
                    </div>
                </div>

                {/* Divider */}
                <div className="h-px bg-purple-900/50"></div>

                {/* Toggle Filters */}
                <div className="space-y-3">
                    {/* Paid Only Toggle */}
                    <label className="flex items-center justify-between cursor-pointer group">
                        <span className="text-sm text-zinc-400 group-hover:text-white transition-colors">Paid Only</span>
                        <div className="relative">
                            <input
                                type="checkbox"
                                name="isPaid"
                                checked={filters.isPaid}
                                onChange={handleChange}
                                className="peer sr-only"
                            />
                            <div className="h-6 w-11 rounded-full bg-zinc-800 peer-checked:bg-purple-500 transition-all"></div>
                            <div className="absolute left-1 top-1 h-4 w-4 rounded-full bg-zinc-500 transition-all peer-checked:translate-x-5 peer-checked:bg-white"></div>
                        </div>
                    </label>

                    {/* Salary Disclosed Toggle */}
                    <label className="flex items-center justify-between cursor-pointer group">
                        <span className="text-sm text-zinc-400 group-hover:text-white transition-colors">Salary Disclosed</span>
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

export default InternSidebar;
