import React from 'react';
import type { Internship } from '../types';
import { MapPin, Briefcase, ExternalLink, DollarSign, Clock, Building2 } from 'lucide-react';

interface InternCardProps {
    intern: Internship;
}

const InternCard: React.FC<InternCardProps> = ({ intern }) => {
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

    // Check if internship was posted today
    const isNew = intern.Last_Updated.includes(new Date().toISOString().split('T')[0]);

    // Get salary display text
    const getSalaryDisplay = () => {
        if (intern.Salary === "Not Disclosed" || !intern.Salary || intern.Salary === "Unpaid") {
            return intern.Salary || "Salary Not Disclosed";
        }
        return intern.Salary;
    };

    // Get company initials for avatar
    const getCompanyInitials = () => {
        if (!intern.Company) return '?';
        return intern.Company.split(' ')
            .slice(0, 2)
            .map(word => word[0])
            .join('')
            .toUpperCase();
    };

    return (
        <div className="group relative flex flex-col justify-between rounded-xl border border-purple-900/50 bg-zinc-900/60 p-5 transition-all duration-300 hover:border-purple-500/60 hover:bg-zinc-900/80 hover-lift">

            {/* New Badge */}
            {isNew && (
                <div className="absolute -top-2 -right-2 z-10">
                    <span className="inline-flex items-center gap-1 rounded-full bg-purple-500 px-2.5 py-0.5 text-xs font-semibold text-white shadow-lg">
                        NEW
                    </span>
                </div>
            )}

            {/* Top Section */}
            <div>
                {/* Header: Site Badge & Date */}
                <div className="mb-4 flex items-start justify-between">
                    <span className={`inline-flex items-center rounded-full border px-2.5 py-1 text-xs font-medium ${getSiteBadgeStyles(intern.Site)}`}>
                        {intern.Site.replace(' (USA)', '').replace(' (India)', '')}
                    </span>
                    <div className="flex items-center gap-1.5 text-xs text-zinc-500">
                        <Clock className="h-3 w-3" />
                        <span>{intern.Last_Updated.split(' ')[0]}</span>
                    </div>
                </div>

                {/* Company Avatar & Info */}
                <div className="mb-4 flex items-start gap-3">
                    <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-lg bg-purple-900/30 border border-purple-700/50">
                        <span className="text-sm font-bold text-purple-400">{getCompanyInitials()}</span>
                    </div>
                    <div className="min-w-0 flex-1">
                        <h3
                            className="mb-0.5 text-base font-semibold text-zinc-100 line-clamp-1 group-hover:text-white transition-colors"
                            title={intern.Title}
                        >
                            {intern.Title || 'Untitled Position'}
                        </h3>
                        <div className="flex items-center gap-1.5 text-sm text-zinc-400">
                            <Building2 className="h-3.5 w-3.5 text-zinc-500" />
                            <span className="truncate">{intern.Company || 'Company Not Listed'}</span>
                        </div>
                    </div>
                </div>

                {/* Metadata Grid */}
                <div className="mb-4 space-y-2">
                    <div className="flex items-center gap-2 text-sm text-zinc-400">
                        <MapPin className="h-4 w-4 text-zinc-500" />
                        <span className="truncate">{intern.Location || 'Location Not Specified'}</span>
                    </div>
                    <div className="flex items-center gap-2 text-sm text-zinc-400">
                        <Briefcase className="h-4 w-4 text-purple-500" />
                        <span className="truncate text-purple-400">{intern.Experience || 'Internship'}</span>
                    </div>
                    <div className="flex items-center gap-2 text-sm text-zinc-400">
                        <DollarSign className="h-4 w-4 text-zinc-500" />
                        <span className={`truncate ${intern.Salary !== "Not Disclosed" && intern.Salary !== "Unpaid" ? 'text-emerald-400' : ''}`}>
                            {getSalaryDisplay()}
                        </span>
                    </div>
                </div>

                {/* Description Snippet */}
                {intern.Description && intern.Description !== "See Link" && (
                    <p className="mb-4 text-sm text-zinc-500 line-clamp-2">
                        {intern.Description}
                    </p>
                )}
            </div>

            {/* Bottom Section: Action Button */}
            <a
                href={intern.Link}
                target="_blank"
                rel="noopener noreferrer"
                className="mt-auto flex w-full items-center justify-center gap-2 rounded-lg border border-purple-500/50 bg-purple-500/10 px-4 py-2.5 text-sm font-semibold text-purple-300 transition-all duration-200 hover:bg-purple-500/20 hover:border-purple-400"
            >
                Apply Now
                <ExternalLink className="h-4 w-4" />
            </a>
        </div>
    );
};

export default InternCard;
