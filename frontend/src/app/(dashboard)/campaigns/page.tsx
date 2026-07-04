'use client';

import { useState } from 'react';

export default function CampaignsPage() {
  const [campaigns, setCampaigns] = useState([
    {
      id: 1,
      title: 'Tues-Wed Local Lunch Promotion',
      department: 'Marketing',
      budget: 1500,
      status: 'draft',
      details: 'Targeted Instagram and local search ads offering weekday lunch bundle discounts.',
    },
    {
      id: 2,
      title: 'Corporate Catering Email Outreach',
      department: 'Sales',
      budget: 500,
      status: 'draft',
      details: 'Re-engage local corporate profiles for group events and holiday catering orders.',
    },
    {
      id: 3,
      title: 'Staff Scheduling Shift Matching',
      department: 'Operations',
      budget: 800,
      status: 'active',
      details: 'Sync front-of-house staff shifts closer to the 12:00 PM - 2:00 PM peak periods.',
    },
    {
      id: 4,
      title: 'Weekday Happy Hour Loyalty Campaign',
      department: 'Marketing',
      budget: 1000,
      status: 'completed',
      details: 'Launch double loyalty points during 4 PM - 6 PM on Mondays to Thursdays.',
    },
  ]);

  const handleMoveStatus = (id: number, newStatus: string) => {
    setCampaigns((prev) =>
      prev.map((c) => (c.id === id ? { ...c, status: newStatus } : c))
    );
  };

  const columns = [
    { title: 'Draft Recommendations', id: 'draft', border: 'border-t-amber-500' },
    { title: 'Active Campaigns', id: 'active', border: 'border-t-blue-500' },
    { title: 'Completed Outcomes', id: 'completed', border: 'border-t-emerald-500' },
  ];

  return (
    <div className="max-w-6xl mx-auto space-y-6 pb-12">
      <div>
        <h1 className="text-3xl font-extrabold text-gray-900 tracking-tight">Campaign Execution</h1>
        <p className="mt-2 text-sm text-gray-500 font-medium">Manage and run marketing, sales, and operational initiatives derived from AI recommendations.</p>
      </div>

      {/* Kanban Board Container */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {columns.map((col) => {
          const colCampaigns = campaigns.filter((c) => c.status === col.id);
          return (
            <div key={col.id} className="bg-gray-50/50 rounded-2xl p-4 flex flex-col gap-4 border border-gray-100 min-h-[500px]">
              <div className={`border-t-4 ${col.border} pt-2 pb-1`}>
                <h3 className="text-sm font-bold text-gray-900 flex justify-between items-center">
                  {col.title}
                  <span className="text-xs bg-white text-gray-400 font-semibold px-2 py-0.5 rounded border border-gray-100">{colCampaigns.length}</span>
                </h3>
              </div>

              <div className="flex flex-col gap-3">
                {colCampaigns.length === 0 ? (
                  <div className="text-center p-8 border border-dashed border-gray-200 rounded-xl text-xs text-gray-400">
                    No campaigns in this stage
                  </div>
                ) : (
                  colCampaigns.map((camp) => (
                    <div key={camp.id} className="bg-white rounded-xl border border-gray-100 p-4 shadow-sm hover:shadow transition-all space-y-3">
                      <div className="flex justify-between items-start">
                        <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-gray-50 text-gray-600 uppercase tracking-wider">{camp.department}</span>
                        <span className="text-xs font-bold text-gray-900">${camp.budget}</span>
                      </div>
                      <h4 className="text-sm font-bold text-gray-950 leading-snug">{camp.title}</h4>
                      <p className="text-xs text-gray-500 leading-normal">{camp.details}</p>

                      <div className="pt-3 border-t border-gray-50 flex gap-2 justify-end">
                        {col.id === 'draft' && (
                          <button 
                            onClick={() => handleMoveStatus(camp.id, 'active')}
                            className="w-full text-xs font-bold py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-all shadow-sm"
                          >
                            Approve & Launch
                          </button>
                        )}
                        {col.id === 'active' && (
                          <button 
                            onClick={() => handleMoveStatus(camp.id, 'completed')}
                            className="w-full text-xs font-bold py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg transition-all shadow-sm"
                          >
                            Mark Completed
                          </button>
                        )}
                        {col.id === 'completed' && (
                          <span className="w-full text-center text-xs font-bold py-2 text-emerald-600 bg-emerald-50 rounded-lg">
                            ✓ Success Outcome
                          </span>
                        )}
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
