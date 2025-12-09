import React from 'react';
import { Briefcase, MapPin, Clock } from 'lucide-react';
import type { Job } from '../types';

const JobCard: React.FC<{ job: Job }> = ({ job }) => {
  // Dummy tags for visual appeal
  const tags = ["AI/ML", "Python", "Data Science"];

  return (
    <div className="group bg-[#161b22] rounded-xl p-5 border border-[#30363d] hover:border-blue-500 hover:shadow-lg hover:shadow-blue-900/20 transition-all duration-300 cursor-pointer relative">
      
      {/* Top Section: Header & Logo */}
      <div className="flex justify-between items-start mb-3">
        <div className="flex-1 pr-4">
          <h3 className="text-lg font-bold text-gray-100 leading-tight group-hover:text-blue-400 transition-colors">
            {job.Title}
          </h3>
          <p className="text-sm font-semibold text-gray-400 mt-1">{job.Company}</p>
        </div>
        
        {/* Logo Placeholder (Dark Box) */}
        <div className="w-10 h-10 bg-[#21262d] rounded-lg border border-[#30363d] flex items-center justify-center text-xs font-bold text-gray-500 shrink-0">
           {job.Company.slice(0, 1)}
        </div>
      </div>

      {/* Meta Details Row */}
      <div className="flex flex-wrap items-center gap-3 text-xs text-gray-400 font-medium mb-4">
        <div className="flex items-center gap-1">
          <Briefcase size={14} className="text-gray-500" />
          <span>{job.Experience}</span>
        </div>
        <span className="text-gray-600">•</span>
        <div className="flex items-center gap-1">
          <span className="text-gray-500 font-bold">₹</span>
          <span>Not Disclosed</span>
        </div>
        <span className="text-gray-600">•</span>
        <div className="flex items-center gap-1">
          <MapPin size={14} className="text-gray-500" />
          <span>{job.Location}</span>
        </div>
      </div>

      {/* Description Snippet */}
      <p className="text-sm text-gray-400 line-clamp-2 mb-4 leading-relaxed">
        {job.Description}
      </p>

      {/* Tags Section */}
      <div className="flex flex-wrap gap-2 mb-4">
        {tags.map((tag, i) => (
          <span key={i} className="text-xs px-2 py-1 bg-[#21262d] text-blue-300 rounded-md border border-[#30363d]">
            {tag}
          </span>
        ))}
      </div>

      {/* Footer: Date & Save */}
      <div className="flex justify-between items-center pt-3 border-t border-[#30363d] text-xs text-gray-500">
        <div className="flex items-center gap-1">
          <Clock size={12} />
          <span>{job.Last_Updated}</span>
        </div>
        
      </div>
      
      {/* Invisible Full Card Link */}
      <a href={job.Link} target="_blank" rel="noopener noreferrer" className="absolute inset-0 z-10" />
    </div>
  );
};

export default JobCard;