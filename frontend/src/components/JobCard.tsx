import React from 'react';
import type { Job } from '../types';
import { MapPin, Briefcase, ExternalLink, DollarSign, Clock, Building2 } from 'lucide-react';

interface JobCardProps {
  job: Job;
}

const JobCard: React.FC<JobCardProps> = ({ job }) => {
  // Helper to determine badge styles based on site
  const getSiteBadgeStyles = (site: string) => {
    if (site.includes('Indeed')) {
      return 'bg-blue-500/20 text-blue-400 border-blue-500/30';
    }
    if (site.includes('Naukri')) {
      return 'bg-orange-500/20 text-orange-400 border-orange-500/30';
    }
    return 'bg-zinc-500/20 text-zinc-400 border-zinc-500/30';
  };

  // Check if job was posted today
  const isNew = job.Last_Updated.includes(new Date().toISOString().split('T')[0]);

  // Get salary display text
  const getSalaryDisplay = () => {
    if (job.Salary === "Not Disclosed" || !job.Salary) {
      return "Salary Not Disclosed";
    }
    return job.Salary;
  };

  // Get company initials for avatar
  const getCompanyInitials = () => {
    if (!job.Company) return '?';
    return job.Company.split(' ')
      .slice(0, 2)
      .map(word => word[0])
      .join('')
      .toUpperCase();
  };

  return (
    <div className="group relative flex flex-col justify-between rounded-xl border border-zinc-800 bg-zinc-900/60 p-5 transition-all duration-300 hover:border-zinc-600 hover:bg-zinc-900/80 hover-lift">

      {/* New Badge */}
      {isNew && (
        <div className="absolute -top-2 -right-2 z-10">
          <span className="inline-flex items-center gap-1 rounded-full bg-white px-2.5 py-0.5 text-xs font-semibold text-black shadow-lg">
            NEW
          </span>
        </div>
      )}

      {/* Top Section */}
      <div>
        {/* Header: Site Badge & Date */}
        <div className="mb-4 flex items-start justify-between">
          <span className={`inline-flex items-center rounded-full border px-2.5 py-1 text-xs font-medium ${getSiteBadgeStyles(job.Site)}`}>
            {job.Site.replace(' (USA)', '').replace(' (India)', '')}
          </span>
          <div className="flex items-center gap-1.5 text-xs text-zinc-500">
            <Clock className="h-3 w-3" />
            <span>{job.Last_Updated.split(' ')[0]}</span>
          </div>
        </div>

        {/* Company Avatar & Info */}
        <div className="mb-4 flex items-start gap-3">
          <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-lg bg-zinc-800 border border-zinc-700">
            <span className="text-sm font-bold text-zinc-400">{getCompanyInitials()}</span>
          </div>
          <div className="min-w-0 flex-1">
            <h3
              className="mb-0.5 text-base font-semibold text-zinc-100 line-clamp-1 group-hover:text-white transition-colors"
              title={job.Title}
            >
              {job.Title || 'Untitled Position'}
            </h3>
            <div className="flex items-center gap-1.5 text-sm text-zinc-400">
              <Building2 className="h-3.5 w-3.5 text-zinc-500" />
              <span className="truncate">{job.Company || 'Company Not Listed'}</span>
            </div>
          </div>
        </div>

        {/* Metadata Grid */}
        <div className="mb-4 space-y-2">
          <div className="flex items-center gap-2 text-sm text-zinc-400">
            <MapPin className="h-4 w-4 text-zinc-500" />
            <span className="truncate">{job.Location || 'Location Not Specified'}</span>
          </div>
          <div className="flex items-center gap-2 text-sm text-zinc-400">
            <Briefcase className="h-4 w-4 text-zinc-500" />
            <span className="truncate">{job.Experience || 'Experience Not Specified'}</span>
          </div>
          <div className="flex items-center gap-2 text-sm text-zinc-400">
            <DollarSign className="h-4 w-4 text-zinc-500" />
            <span className={`truncate ${job.Salary !== "Not Disclosed" ? 'text-emerald-400' : ''}`}>
              {getSalaryDisplay()}
            </span>
          </div>
        </div>

        {/* Description Snippet */}
        {job.Description && job.Description !== "See Link" && (
          <p className="mb-4 text-sm text-zinc-500 line-clamp-2">
            {job.Description}
          </p>
        )}
      </div>

{/* Bottom Section: Action Button */}
      <a
        href={job.Link}
        target="_blank"
        rel="noopener noreferrer"
        className="mt-auto flex w-full items-center justify-center gap-2 rounded-lg border border-zinc-300 px-4 py-2.5 text-sm font-semibold text-zinc-900 transition-all duration-200 hover:bg-zinc-600"
      >
        Apply Now

        <ExternalLink className="h-4 w-4 text-white" />
      </a>
    </div>
  );
};

export default JobCard;