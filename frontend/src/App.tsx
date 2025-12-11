import { useState, useMemo } from 'react';
import JobCard from './components/JobCard';
import Sidebar from './components/Sidebar';
import InternCard from './components/InternCard';
import InternSidebar from './components/InternSidebar';
import type { Job, Internship } from './types';
import jobsData from './jobs.json';
import internsData from './intern.json';
import { Search, MapPin, Globe, Sparkles, X, Briefcase, GraduationCap } from 'lucide-react';

// Filter out empty/invalid jobs
const validJobs = (jobsData as Job[]).filter(job => job.Title && job.Company);
const validInterns = (internsData as Internship[]).filter(intern => intern.Title && intern.Company);

function App() {
  // Tab state: 'jobs' or 'internships'
  const [activeTab, setActiveTab] = useState<'jobs' | 'internships'>('jobs');

  const [searchTerm, setSearchTerm] = useState('');
  const [internSearchTerm, setInternSearchTerm] = useState('');

  // Job Filter State
  const [filters, setFilters] = useState({
    location: '',
    experience: '',
    isRemote: false,
    site: 'All',
    salaryDisclosed: false,
    company: '',
    daysAgo: '',
    countryFilter: '' // 'USA' or 'India' or ''
  });

  // Internship Filter State
  const [internFilters, setInternFilters] = useState({
    location: '',
    site: 'All',
    salaryDisclosed: false,
    company: '',
    daysAgo: '',
    isPaid: false,
    countryFilter: '' // 'USA' or 'India' or ''
  });

  // Quick filter state for location (to track active state)
  const [activeLocationFilter, setActiveLocationFilter] = useState<string | null>(null);
  const [internActiveLocationFilter, setInternActiveLocationFilter] = useState<string | null>(null);

  // Load Data
  const [jobs] = useState<Job[]>(validJobs);
  const [interns] = useState<Internship[]>(validInterns);

  // Helper: Parse experience range from string like "2-5 Yrs" or "5+ Years"
  const parseExperience = (expStr: string): { min: number; max: number } | null => {
    if (!expStr || expStr === 'N/A') return null;

    // Handle "X+ Years" format
    const plusMatch = expStr.match(/(\d+)\+/);
    if (plusMatch) {
      return { min: parseInt(plusMatch[1]), max: 99 };
    }

    // Handle "X-Y Yrs" format
    const rangeMatch = expStr.match(/(\d+)\s*[-–]\s*(\d+)/);
    if (rangeMatch) {
      return { min: parseInt(rangeMatch[1]), max: parseInt(rangeMatch[2]) };
    }

    // Handle single number
    const singleMatch = expStr.match(/(\d+)/);
    if (singleMatch) {
      return { min: parseInt(singleMatch[1]), max: parseInt(singleMatch[1]) };
    }

    return null;
  };

  // Helper: Check if job experience matches filter
  const matchesExperience = (jobExp: string, filterExp: string): boolean => {
    if (!filterExp) return true;

    const jobRange = parseExperience(jobExp);
    if (!jobRange) return filterExp === 'Fresher';

    switch (filterExp) {
      case 'Fresher':
        return jobRange.min === 0 || jobRange.min === 1;
      case '1-3':
        return jobRange.min <= 3 && jobRange.max >= 1;
      case '3-5':
        return jobRange.min <= 5 && jobRange.max >= 3;
      case '5-10':
        return jobRange.min <= 10 && jobRange.max >= 5;
      case '10+':
        return jobRange.max >= 10;
      default:
        return true;
    }
  };

  // Helper: Check if job was posted within X days
  const isWithinDays = (dateStr: string, days: number): boolean => {
    if (!days) return true;
    const jobDate = new Date(dateStr.split(' ')[0]);
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - jobDate.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays <= days;
  };

  // Job Filtering Logic
  const filteredJobs = useMemo(() => {
    return jobs.filter(job => {
      // 1. Search Term
      const matchesSearch =
        searchTerm === '' ||
        job.Title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        job.Company.toLowerCase().includes(searchTerm.toLowerCase()) ||
        job.Description.toLowerCase().includes(searchTerm.toLowerCase());

      // 2. Location Filter
      const matchesLocation =
        filters.location === '' ||
        job.Location.toLowerCase().includes(filters.location.toLowerCase());

      // 3. Site Filter
      const matchesSite =
        filters.site === 'All' ||
        job.Site.toLowerCase().includes(filters.site.toLowerCase());

      // 4. Remote Filter
      const matchesRemote =
        !filters.isRemote ||
        job.Location.toLowerCase().includes('remote') ||
        job.Description.toLowerCase().includes('remote') ||
        job.Title.toLowerCase().includes('remote') ||
        job.Location.toLowerCase().includes('hybrid');

      // 5. Experience Filter
      const matchesExp = matchesExperience(job.Experience, filters.experience);

      // 6. Salary Disclosed Filter
      const matchesSalary =
        !filters.salaryDisclosed ||
        (job.Salary !== 'Not Disclosed' && job.Salary !== '');

      // 7. Company Filter
      const matchesCompany =
        filters.company === '' ||
        job.Company.toLowerCase().includes(filters.company.toLowerCase());

      // 8. Posted Within Filter
      const matchesDays =
        filters.daysAgo === '' ||
        isWithinDays(job.Last_Updated, parseInt(filters.daysAgo));

      // 9. Country Filter (USA/India based on Site attribute)
      const matchesCountry = (() => {
        if (!filters.countryFilter) return true;
        const siteLower = job.Site.toLowerCase();
        if (filters.countryFilter === 'USA') {
          return siteLower.includes('usa');
        } else if (filters.countryFilter === 'India') {
          return siteLower.includes('india') || siteLower.includes('naukri');
        }
        return true;
      })();

      return matchesSearch && matchesLocation && matchesSite && matchesRemote &&
        matchesExp && matchesSalary && matchesCompany && matchesDays && matchesCountry;
    });
  }, [jobs, searchTerm, filters]);

  // Internship Filtering Logic
  const filteredInterns = useMemo(() => {
    return interns.filter(intern => {
      // 1. Search Term
      const matchesSearch =
        internSearchTerm === '' ||
        intern.Title.toLowerCase().includes(internSearchTerm.toLowerCase()) ||
        intern.Company.toLowerCase().includes(internSearchTerm.toLowerCase()) ||
        intern.Description.toLowerCase().includes(internSearchTerm.toLowerCase());

      // 2. Location Filter
      const matchesLocation =
        internFilters.location === '' ||
        intern.Location.toLowerCase().includes(internFilters.location.toLowerCase());

      // 3. Site Filter
      const matchesSite =
        internFilters.site === 'All' ||
        intern.Site.toLowerCase().includes(internFilters.site.toLowerCase());

      // 4. Salary Disclosed Filter
      const matchesSalary =
        !internFilters.salaryDisclosed ||
        (intern.Salary !== 'Not Disclosed' && intern.Salary !== '' && intern.Salary !== 'Unpaid');

      // 5. Company Filter
      const matchesCompany =
        internFilters.company === '' ||
        intern.Company.toLowerCase().includes(internFilters.company.toLowerCase());

      // 6. Posted Within Filter
      const matchesDays =
        internFilters.daysAgo === '' ||
        isWithinDays(intern.Last_Updated, parseInt(internFilters.daysAgo));

      // 7. Paid Only Filter
      const matchesPaid =
        !internFilters.isPaid ||
        (intern.Salary !== 'Unpaid' && intern.Salary !== 'Not Disclosed' && intern.Salary !== '');

      // 8. Country Filter (USA/India based on Site attribute)
      const matchesCountry = (() => {
        if (!internFilters.countryFilter) return true;
        const siteLower = intern.Site.toLowerCase();
        if (internFilters.countryFilter === 'USA') {
          return siteLower.includes('usa');
        } else if (internFilters.countryFilter === 'India') {
          return siteLower.includes('india') || siteLower.includes('naukri');
        }
        return true;
      })();

      return matchesSearch && matchesLocation && matchesSite && matchesSalary && matchesCompany && matchesDays && matchesPaid && matchesCountry;
    });
  }, [interns, internSearchTerm, internFilters]);

  // Quick Filter Handlers - Jobs
  const applyQuickFilter = (type: string) => {
    if (type === 'Remote') {
      setFilters(prev => ({ ...prev, isRemote: !prev.isRemote }));
    } else if (type === 'USA') {
      if (activeLocationFilter === 'USA') {
        setActiveLocationFilter(null);
        setFilters(prev => ({ ...prev, countryFilter: '' }));
      } else {
        setActiveLocationFilter('USA');
        setFilters(prev => ({ ...prev, countryFilter: 'USA' }));
      }
    } else if (type === 'India') {
      if (activeLocationFilter === 'India') {
        setActiveLocationFilter(null);
        setFilters(prev => ({ ...prev, countryFilter: '' }));
      } else {
        setActiveLocationFilter('India');
        setFilters(prev => ({ ...prev, countryFilter: 'India' }));
      }
    }
  };

  // Quick Filter Handlers - Internships
  const applyInternQuickFilter = (type: string) => {
    if (type === 'Remote') {
      setInternFilters(prev => ({ ...prev, location: prev.location.includes('Remote') ? '' : 'Remote' }));
    } else if (type === 'USA') {
      if (internActiveLocationFilter === 'USA') {
        setInternActiveLocationFilter(null);
        setInternFilters(prev => ({ ...prev, countryFilter: '' }));
      } else {
        setInternActiveLocationFilter('USA');
        setInternFilters(prev => ({ ...prev, countryFilter: 'USA' }));
      }
    } else if (type === 'India') {
      if (internActiveLocationFilter === 'India') {
        setInternActiveLocationFilter(null);
        setInternFilters(prev => ({ ...prev, countryFilter: '' }));
      } else {
        setInternActiveLocationFilter('India');
        setInternFilters(prev => ({ ...prev, countryFilter: 'India' }));
      }
    }
  };

  // Clear All Filters - Jobs
  const clearAllFilters = () => {
    setSearchTerm('');
    setActiveLocationFilter(null);
    setFilters({
      location: '',
      experience: '',
      isRemote: false,
      site: 'All',
      salaryDisclosed: false,
      company: '',
      daysAgo: '',
      countryFilter: ''
    });
  };

  // Clear All Filters - Internships
  const clearAllInternFilters = () => {
    setInternSearchTerm('');
    setInternActiveLocationFilter(null);
    setInternFilters({
      location: '',
      site: 'All',
      salaryDisclosed: false,
      company: '',
      daysAgo: '',
      isPaid: false,
      countryFilter: ''
    });
  };

  return (
    <div className="min-h-screen bg-[#09090b] text-zinc-100 font-sans">

      {/* Navbar */}
      <nav className="border-b border-zinc-800/50 bg-[#09090b]/90 backdrop-blur-lg sticky top-0 z-50">
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-white">
              <Sparkles className="h-4 w-4 text-black" />
            </div>
            <span className="text-xl font-bold tracking-tight">Job Finder</span>
          </div>

          {/* Tab Buttons in Navbar */}
          <div className="flex items-center gap-2">
            <button
              onClick={() => setActiveTab('jobs')}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${activeTab === 'jobs'
                ? 'bg-white text-black'
                : 'bg-zinc-800 text-zinc-400 hover:bg-zinc-700 hover:text-white'
                }`}
            >
              <Briefcase className="h-4 w-4" />
              Jobs
            </button>
            <button
              onClick={() => setActiveTab('internships')}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${activeTab === 'internships'
                ? 'bg-purple-500 text-white'
                : 'bg-zinc-800 text-zinc-400 hover:bg-zinc-700 hover:text-white'
                }`}
            >
              <GraduationCap className="h-4 w-4" />
              Internships
            </button>
          </div>
        </div>
      </nav>

      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">

        {/* === JOBS TAB === */}
        {activeTab === 'jobs' && (
          <>
            {/* Header Section */}
            <div className="mb-10 text-center md:text-left">
              <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight text-white mb-2">
                Find your next <span className="text-zinc-400">AI Challenge.</span>
              </h1>

              {/* Search Bar & Quick Filters Container */}
              <div className="flex flex-col gap-4">

                {/* Main Search Input */}
                <div className="relative w-full md:max-w-2xl group">
                  <div className="absolute inset-y-0 left-0 flex items-center pl-4 pointer-events-none">
                    <Search className="h-5 w-5 text-zinc-500 group-focus-within:text-white transition-colors" />
                  </div>
                  <input
                    type="text"
                    className="block w-full rounded-xl border border-zinc-800 bg-zinc-900/60 py-4 pl-12 pr-12 text-zinc-200 placeholder-zinc-600 focus:border-zinc-600 focus:outline-none transition-all text-base"
                    placeholder="Search by job title, company, or keywords..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                  />
                  {searchTerm && (
                    <button
                      onClick={() => setSearchTerm('')}
                      className="absolute inset-y-0 right-0 flex items-center pr-4 text-zinc-500 hover:text-white transition-colors"
                    >
                      <X className="h-5 w-5" />
                    </button>
                  )}
                </div>

                {/* Quick Action Buttons */}
                <div className="flex flex-wrap gap-2">
                  <button
                    onClick={() => applyQuickFilter('Remote')}
                    className={`flex items-center gap-2 whitespace-nowrap rounded-full border px-4 py-2.5 text-sm font-medium transition-all duration-200 ${filters.isRemote
                      ? 'bg-white text-black border-white'
                      : 'border-zinc-800 bg-zinc-900/50 text-zinc-400 hover:border-zinc-600 hover:text-white'
                      }`}
                  >
                    <Globe className="h-4 w-4" /> Remote
                  </button>
                  <button
                    onClick={() => applyQuickFilter('USA')}
                    className={`flex items-center gap-2 whitespace-nowrap rounded-full border px-4 py-2.5 text-sm font-medium transition-all duration-200 ${activeLocationFilter === 'USA'
                      ? 'bg-white text-black border-white'
                      : 'border-zinc-800 bg-zinc-900/50 text-zinc-400 hover:border-zinc-600 hover:text-white'
                      }`}
                  >
                    <MapPin className="h-4 w-4" /> USA Jobs
                  </button>
                  <button
                    onClick={() => applyQuickFilter('India')}
                    className={`flex items-center gap-2 whitespace-nowrap rounded-full border px-4 py-2.5 text-sm font-medium transition-all duration-200 ${activeLocationFilter === 'India'
                      ? 'bg-white text-black border-white'
                      : 'border-zinc-800 bg-zinc-900/50 text-zinc-400 hover:border-zinc-600 hover:text-white'
                      }`}
                  >
                    <MapPin className="h-4 w-4" /> India Jobs
                  </button>
                </div>
              </div>
            </div>

            {/* Content Layout */}
            <div className="flex flex-col md:flex-row gap-8">

              {/* Left Sidebar */}
              <Sidebar
                filters={filters}
                setFilters={setFilters}
                onClearFilters={clearAllFilters}
                totalJobs={jobs.length}
                filteredCount={filteredJobs.length}
              />

              {/* Right Job Grid */}
              <div className="flex-1 min-w-0">
                <div className="mb-6 flex items-center justify-between">
                  <span className="text-sm text-zinc-500">
                    Showing <span className="font-semibold text-white">{filteredJobs.length}</span> jobs
                  </span>
                </div>

                {filteredJobs.length > 0 ? (
                  <div className="grid gap-5 sm:grid-cols-1 lg:grid-cols-2">
                    {filteredJobs.map((job, index) => (
                      <div
                        key={`${job.Link}-${index}`}
                        className="animate-fade-in"
                        style={{ animationDelay: `${Math.min(index * 30, 300)}ms` }}
                      >
                        <JobCard job={job} />
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="flex h-80 flex-col items-center justify-center rounded-xl border border-dashed border-zinc-800 bg-zinc-900/30 text-center px-6">
                    <div className="w-16 h-16 rounded-full bg-zinc-800/50 flex items-center justify-center mb-4">
                      <Search className="h-8 w-8 text-zinc-600" />
                    </div>
                    <h3 className="text-lg font-semibold text-zinc-300 mb-1">No jobs found</h3>
                    <p className="text-zinc-500 text-sm mb-4">Try adjusting your filters or search terms</p>
                    <button
                      onClick={clearAllFilters}
                      className="rounded-lg bg-white px-5 py-2.5 text-sm font-semibold text-black transition-all hover:bg-zinc-200"
                    >
                      Clear all filters
                    </button>
                  </div>
                )}
              </div>
            </div>
          </>
        )}

        {/* === INTERNSHIPS TAB === */}
        {activeTab === 'internships' && (
          <>
            {/* Header Section */}
            <div className="mb-10 text-center md:text-left">
              <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight text-white mb-2">
                Find your next <span className="text-purple-400">Internship.</span>
              </h1>

              {/* Search Bar & Quick Filters Container */}
              <div className="flex flex-col gap-4">

                {/* Main Search Input */}
                <div className="relative w-full md:max-w-2xl group">
                  <div className="absolute inset-y-0 left-0 flex items-center pl-4 pointer-events-none">
                    <Search className="h-5 w-5 text-zinc-500 group-focus-within:text-purple-400 transition-colors" />
                  </div>
                  <input
                    type="text"
                    className="block w-full rounded-xl border border-purple-900/50 bg-zinc-900/60 py-4 pl-12 pr-12 text-zinc-200 placeholder-zinc-600 focus:border-purple-500 focus:outline-none transition-all text-base"
                    placeholder="Search by internship title, company, or keywords..."
                    value={internSearchTerm}
                    onChange={(e) => setInternSearchTerm(e.target.value)}
                  />
                  {internSearchTerm && (
                    <button
                      onClick={() => setInternSearchTerm('')}
                      className="absolute inset-y-0 right-0 flex items-center pr-4 text-zinc-500 hover:text-purple-400 transition-colors"
                    >
                      <X className="h-5 w-5" />
                    </button>
                  )}
                </div>

                {/* Quick Action Buttons */}
                <div className="flex flex-wrap gap-2">
                  <button
                    onClick={() => applyInternQuickFilter('Remote')}
                    className={`flex items-center gap-2 whitespace-nowrap rounded-full border px-4 py-2.5 text-sm font-medium transition-all duration-200 ${internFilters.location.includes('Remote')
                      ? 'bg-purple-500 text-white border-purple-500'
                      : 'border-purple-900/50 bg-zinc-900/50 text-zinc-400 hover:border-purple-500 hover:text-white'
                      }`}
                  >
                    <Globe className="h-4 w-4" /> Remote
                  </button>
                  <button
                    onClick={() => applyInternQuickFilter('USA')}
                    className={`flex items-center gap-2 whitespace-nowrap rounded-full border px-4 py-2.5 text-sm font-medium transition-all duration-200 ${internActiveLocationFilter === 'USA'
                      ? 'bg-purple-500 text-white border-purple-500'
                      : 'border-purple-900/50 bg-zinc-900/50 text-zinc-400 hover:border-purple-500 hover:text-white'
                      }`}
                  >
                    <MapPin className="h-4 w-4" /> USA Internships
                  </button>
                  <button
                    onClick={() => applyInternQuickFilter('India')}
                    className={`flex items-center gap-2 whitespace-nowrap rounded-full border px-4 py-2.5 text-sm font-medium transition-all duration-200 ${internActiveLocationFilter === 'India'
                      ? 'bg-purple-500 text-white border-purple-500'
                      : 'border-purple-900/50 bg-zinc-900/50 text-zinc-400 hover:border-purple-500 hover:text-white'
                      }`}
                  >
                    <MapPin className="h-4 w-4" /> India Internships
                  </button>
                </div>
              </div>
            </div>

            {/* Content Layout */}
            <div className="flex flex-col md:flex-row gap-8">

              {/* Left Sidebar */}
              <InternSidebar
                filters={internFilters}
                setFilters={setInternFilters}
                onClearFilters={clearAllInternFilters}
                totalInterns={interns.length}
                filteredCount={filteredInterns.length}
              />

              {/* Right Internship Grid */}
              <div className="flex-1 min-w-0">
                <div className="mb-6 flex items-center justify-between">
                  <span className="text-sm text-zinc-500">
                    Showing <span className="font-semibold text-purple-400">{filteredInterns.length}</span> internships
                  </span>
                </div>

                {filteredInterns.length > 0 ? (
                  <div className="grid gap-5 sm:grid-cols-1 lg:grid-cols-2">
                    {filteredInterns.map((intern, index) => (
                      <div
                        key={`${intern.Link}-${index}`}
                        className="animate-fade-in"
                        style={{ animationDelay: `${Math.min(index * 30, 300)}ms` }}
                      >
                        <InternCard intern={intern} />
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="flex h-80 flex-col items-center justify-center rounded-xl border border-dashed border-purple-900/50 bg-zinc-900/30 text-center px-6">
                    <div className="w-16 h-16 rounded-full bg-purple-900/30 flex items-center justify-center mb-4">
                      <Search className="h-8 w-8 text-purple-500" />
                    </div>
                    <h3 className="text-lg font-semibold text-zinc-300 mb-1">No internships found</h3>
                    <p className="text-zinc-500 text-sm mb-4">Try adjusting your filters or search terms</p>
                    <button
                      onClick={clearAllInternFilters}
                      className="rounded-lg bg-purple-500 px-5 py-2.5 text-sm font-semibold text-white transition-all hover:bg-purple-600"
                    >
                      Clear all filters
                    </button>
                  </div>
                )}
              </div>
            </div>
          </>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-zinc-800/50 mt-16 py-8">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 text-center">
          <p className="text-sm text-zinc-600">
            © 2024 Polaris.ai • Powered by AI • All rights reserved
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;