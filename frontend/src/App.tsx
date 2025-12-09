import React, { useState, useMemo } from 'react';
import JobCard from './components/JobCard';
import type { Job }  from './types';
import jobData from './jobs.json';
import { Search, Filter, X } from 'lucide-react';

const App: React.FC = () => {
  const [allJobs] = useState<Job[]>(jobData as Job[]);
  const [searchTerm, setSearchTerm] = useState("");
  
  // Filter States
  const [showFilters, setShowFilters] = useState(false);
  const [selectedWorkMode, setSelectedWorkMode] = useState<string[]>([]);
  const [selectedExp, setSelectedExp] = useState<string[]>([]);

  // --- HELPER: Extract Minimum Experience from string ---
  // Converts "0-5 Yrs" -> 0
  // Converts "2-7 Yrs" -> 2
  // Converts "Fresher" -> 0
  const getMinExperience = (expString: string): number => {
    const cleanStr = expString.toLowerCase();
    if (cleanStr.includes('fresh')) return 0;
    
    // Find the first number in the string
    const match = cleanStr.match(/(\d+)/);
    return match ? parseInt(match[0], 10) : 0;
  };

  // --- THE FILTERING LOGIC ---
  const filteredJobs = useMemo(() => {
    return allJobs.filter(job => {
      // 1. Search Filter
      const searchLower = searchTerm.toLowerCase();
      const matchesSearch = 
        job.Title.toLowerCase().includes(searchLower) ||
        job.Company.toLowerCase().includes(searchLower) ||
        job.Description.toLowerCase().includes(searchLower);

      if (!matchesSearch) return false;

      // 2. Work Mode Filter
      if (selectedWorkMode.length > 0) {
        const jobText = (job.Location + job.Description).toLowerCase();
        const matchesMode = selectedWorkMode.some(mode => {
          if (mode === "Remote") return jobText.includes("remote");
          if (mode === "Hybrid") return jobText.includes("hybrid");
          if (mode === "On-site") return !jobText.includes("remote") && !jobText.includes("hybrid");
          return false;
        });
        if (!matchesMode) return false;
      }

      // 3. Experience Filter (FIXED LOGIC)
      if (selectedExp.length > 0) {
        const jobMinExp = getMinExperience(job.Experience);

        // Check if the job matches ANY of the selected experience ranges
        const matchesExp = selectedExp.some(filterTag => {
          if (filterTag === "Fresher") return jobMinExp === 0; // Strictly 0 start
          if (filterTag === "0-1 Years") return jobMinExp <= 1; // 0, 1 are okay
          if (filterTag === "1-3 Years") return jobMinExp >= 1 && jobMinExp <= 3;
          if (filterTag === "3-5 Years") return jobMinExp >= 3 && jobMinExp <= 5;
          if (filterTag === "5+ Years") return jobMinExp >= 5;
          return false;
        });
        
        if (!matchesExp) return false;
      }

      return true;
    });
  }, [allJobs, searchTerm, selectedWorkMode, selectedExp]);

  // Handler
  const toggleFilter = (item: string, setFn: React.Dispatch<React.SetStateAction<string[]>>) => {
    setFn(prev => prev.includes(item) ? prev.filter(i => i !== item) : [...prev, item]);
  };

  return (
    <div className="min-h-screen bg-[#0d1117] font-sans text-gray-300 selection:bg-blue-900 selection:text-white flex flex-col">
      
      {/* HEADER */}
      <header className="bg-[#161b22] border-b border-[#30363d] sticky top-0 z-50">
        <div className="w-full px-6 h-16 flex items-center justify-between">
          <div className="font-bold text-xl text-white tracking-tight flex items-center gap-2">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center text-white font-bold">AI</div>
            <span>Jobs<span className="text-blue-500">.board</span></span>
          </div>
          
          <div className="hidden md:flex flex-1 max-w-2xl mx-8 items-center bg-[#0d1117] rounded-xl px-4 py-2.5 border border-[#30363d] focus-within:border-blue-500 focus-within:ring-1 focus-within:ring-blue-900 transition-all">
            <Search size={18} className="text-gray-500 mr-3" />
            <input 
              type="text" 
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search by role, company, or skill..." 
              className="bg-transparent border-none outline-none text-sm w-full text-gray-200 placeholder-gray-600"
            />
            {searchTerm && <button onClick={() => setSearchTerm("")}><X size={16} /></button>}
          </div>

          <div className="flex items-center gap-4">
             <button 
               onClick={() => setShowFilters(!showFilters)}
               className={`flex items-center gap-2 text-sm font-medium px-4 py-2 rounded-lg border transition-colors ${showFilters ? 'bg-blue-600 border-blue-500 text-white' : 'bg-[#21262d] border-[#30363d] text-gray-300 hover:bg-[#30363d]'}`}
             >
               <Filter size={16} />
               Filters
             </button>
          </div>
        </div>
      </header>

      <div className="flex flex-1 w-full relative">
        
        {/* SIDEBAR */}
        {showFilters && (
          <aside className="w-72 bg-[#161b22] border-r border-[#30363d] p-6 hidden md:block sticky top-16 h-[calc(100vh-64px)] overflow-y-auto">
            <div className="flex justify-between items-center mb-6">
              <h2 className="font-bold text-white">Filters</h2>
              <button onClick={() => {setSelectedExp([]); setSelectedWorkMode([]);}} className="text-xs text-blue-400 hover:text-blue-300">Clear All</button>
            </div>

            <div className="mb-6">
              <h3 className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-3">Work Mode</h3>
              {["Remote", "Hybrid", "On-site"].map(mode => (
                <label key={mode} className="flex items-center gap-3 mb-2 cursor-pointer group">
                  <input 
                    type="checkbox" 
                    className="accent-blue-600 w-4 h-4 rounded border-gray-600 bg-[#0d1117]"
                    checked={selectedWorkMode.includes(mode)}
                    onChange={() => toggleFilter(mode, setSelectedWorkMode)}
                  />
                  <span className="text-sm text-gray-400 group-hover:text-white transition-colors">{mode}</span>
                </label>
              ))}
            </div>

            <div className="mb-6">
              <h3 className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-3">Experience</h3>
              {/* NOTE: These strings must match the logic inside filteredJobs exactly */}
              {["Fresher", "0-1 Years", "1-3 Years", "3-5 Years", "5+ Years"].map(exp => (
                <label key={exp} className="flex items-center gap-3 mb-2 cursor-pointer group">
                   <input 
                    type="checkbox" 
                    className="accent-blue-600 w-4 h-4 rounded border-gray-600 bg-[#0d1117]"
                    checked={selectedExp.includes(exp)}
                    onChange={() => toggleFilter(exp, setSelectedExp)}
                  />
                  <span className="text-sm text-gray-400 group-hover:text-white transition-colors">
                    {exp}
                  </span>
                </label>
              ))}
            </div>
          </aside>
        )}

        {/* FEED */}
        <main className="flex-1 p-6">
          <div className="mb-4 flex items-center justify-between">
            <h1 className="text-xl font-bold text-white">
              {filteredJobs.length} <span className="text-gray-500 font-normal">Jobs Found</span>
            </h1>
          </div>

          <div className={`grid gap-6 ${showFilters ? 'grid-cols-1 lg:grid-cols-2 xl:grid-cols-3' : 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4'}`}>
            {filteredJobs.length > 0 ? (
              filteredJobs.map((job, index) => (
                <JobCard key={index} job={job} />
              ))
            ) : (
              <div className="col-span-full py-20 text-center border-2 border-dashed border-[#30363d] rounded-xl">
                <p className="text-gray-500 text-lg">No jobs match your filters.</p>
                <button 
                  onClick={() => {setSearchTerm(""); setSelectedExp([]); setSelectedWorkMode([]);}}
                  className="mt-4 text-blue-400 hover:underline"
                >
                  Clear all filters
                </button>
              </div>
            )}
          </div>
        </main>

      </div>
    </div>
  );
}

export default App;