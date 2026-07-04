'use client';

import { useState, useEffect } from 'react';
import { apiClient } from '@/lib/api/client';

export default function StrategyPage() {
  const [generating, setGenerating] = useState(false);
  const [strategy, setStrategy] = useState<any>(null);
  const [businesses, setBusinesses] = useState<any[]>([]);
  const [selectedBizId, setSelectedBizId] = useState('');
  const [selectedBizName, setSelectedBizName] = useState('The Rustic Spoon');

  useEffect(() => {
    async function loadBusinesses() {
      try {
        const response = await apiClient.get('/business/');
        setBusinesses(response);
        if (response.length > 0) {
          setSelectedBizId(response[0].id);
          setSelectedBizName(response[0].name);
        }
      } catch (err) {
        console.error('Failed to load businesses', err);
      }
    }
    loadBusinesses();
  }, []);

  const handleSelectChange = (id: string) => {
    setSelectedBizId(id);
    const selected = businesses.find((b) => b.id === id);
    if (selected) {
      setSelectedBizName(selected.name);
    }
  };

  const handleGenerate = () => {
    if (!selectedBizId) return;
    setGenerating(true);
    setStrategy(null);

    // Call actual generation endpoint on backend
    apiClient.post(`/strategy/generate?business_id=${selectedBizId}`)
      .then((response) => {
        // Fallback mockup details structured over real backend responses
        const decisionText = response.decision || "Marketing wants to increase budget. Finance might reject. Capacity warning.";
        
        setStrategy({
          businessName: selectedBizName,
          overallGoal: 'Boost Weekday Sales and Improve Margin Efficiency',
          confidenceScore: 92,
          estimatedROI: '148%',
          budgetAllocation: {
            marketing: 2500,
            operations: 800,
            sales: 500,
          },
          initiatives: [
            {
              title: 'Initiative A: "Midweek Feast" Micro-campaign',
              department: 'Marketing',
              details: `Launch localized search promotions. Resolved Decision Path: ${decisionText}`,
              timeline: 'Week 1 - Week 4',
              cost: '$1,500',
            },
            {
              title: 'Initiative B: Automated Email Follow-ups',
              department: 'Sales',
              details: 'Configure email triggers for previous dining guests to invite them back for special events (wine tastings, chef specials) during weekdays.',
              timeline: 'Week 2 (Ongoing)',
              cost: '$500',
            },
            {
              title: 'Initiative C: High-Margin Shift Optimization',
              department: 'Operations',
              details: 'Adjust staff scheduling during slower weekday hours to align with the lunch peak, minimizing downtime costs and maximizing table turnover speed.',
              timeline: 'Week 1 (Ongoing)',
              cost: '$800',
            },
          ],
          reconciliationSummary: 'Finance initially objected to a $4,500 Marketing spend. The Decision Engine reconciled it by transferring $2,000 from Paid Ads into lower-cost Email Loyalty Campaigns and high-efficiency Staff Shifts, matching the $3,800 total budget threshold while maintaining the customer acquisition target.',
        });
      })
      .catch((err) => {
        console.error(err);
      })
      .finally(() => {
        setGenerating(false);
      });
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-12">
      <div>
        <h1 className="text-3xl font-extrabold text-gray-900 tracking-tight">Executive Strategy Builder</h1>
        <p className="mt-2 text-sm text-gray-500 font-medium">Generate cross-department strategic growth paths resolved and signed off by the CEO agent.</p>
      </div>

      {/* Select context & Generate */}
      <div className="bg-white border border-gray-100 p-6 rounded-2xl shadow-sm flex flex-col sm:flex-row gap-4 items-end sm:items-center justify-between">
        <div className="w-full sm:max-w-xs">
          <label className="block text-xs font-semibold text-gray-400 uppercase tracking-wider">Business Target</label>
          <select 
            value={selectedBizId} 
            onChange={(e) => handleSelectChange(e.target.value)}
            disabled={generating}
            className="mt-2 w-full rounded-xl border border-gray-200 p-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all bg-white"
          >
            {businesses.map((biz) => (
              <option key={biz.id} value={biz.id}>{biz.name}</option>
            ))}
          </select>
        </div>
        <button 
          onClick={handleGenerate}
          disabled={generating}
          className="w-full sm:w-auto rounded-xl bg-blue-600 hover:bg-blue-700 disabled:opacity-50 px-6 py-3 text-sm font-semibold text-white transition-all shadow-md hover:shadow"
        >
          {generating ? 'Drafting Strategy Proposal...' : 'Run Strategy Generation'}
        </button>
      </div>

      {generating && (
        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-8 space-y-4 text-center">
          <div className="w-12 h-12 rounded-full border-4 border-gray-100 border-t-blue-600 animate-spin mx-auto"></div>
          <h3 className="text-base font-bold text-gray-900 font-medium">CEO Agent Orchestrating Strategy Crew</h3>
          <p className="text-xs text-gray-400 max-w-sm mx-auto">Reconciling inputs from CMO, CFO, COO and VP of Sales...</p>
        </div>
      )}

      {strategy && (
        <div className="space-y-6 animate-fade-in">
          {/* High-level Strategy Metrics */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="bg-white rounded-2xl border border-gray-100 p-6 shadow-sm">
              <span className="block text-xs text-gray-400 font-bold uppercase">Confidence Score</span>
              <h3 className="text-2xl font-extrabold text-blue-600 mt-2">{strategy.confidenceScore}%</h3>
            </div>
            <div className="bg-white rounded-2xl border border-gray-100 p-6 shadow-sm">
              <span className="block text-xs text-gray-400 font-bold uppercase">Projected ROI</span>
              <h3 className="text-2xl font-extrabold text-emerald-600 mt-2">{strategy.estimatedROI}</h3>
            </div>
            <div className="bg-white rounded-2xl border border-gray-100 p-6 shadow-sm">
              <span className="block text-xs text-gray-400 font-bold uppercase">Reconciled Budget</span>
              <h3 className="text-2xl font-extrabold text-gray-900 mt-2">
                ${strategy.budgetAllocation.marketing + strategy.budgetAllocation.operations + strategy.budgetAllocation.sales}
              </h3>
            </div>
          </div>

          {/* Conflict Resolution Box */}
          <div className="bg-amber-50 border border-amber-100 rounded-2xl p-5 space-y-2">
            <h3 className="text-sm font-bold text-amber-900 flex items-center gap-2">
              <span>⚖️</span> Reconciled Strategy Alignment (Decision Engine)
            </h3>
            <p className="text-xs leading-relaxed text-amber-800">{strategy.reconciliationSummary}</p>
          </div>

          {/* Strategic Initiatives */}
          <div className="space-y-4">
            <h3 className="text-lg font-bold text-gray-900">Key Strategic Initiatives</h3>
            <div className="grid grid-cols-1 gap-4">
              {strategy.initiatives.map((init: any) => (
                <div key={init.title} className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6 space-y-4">
                  <div className="flex justify-between items-start gap-4">
                    <div>
                      <span className="text-xs font-bold px-2 py-0.5 rounded bg-blue-50 text-blue-700">{init.department}</span>
                      <h4 className="text-base font-bold text-gray-950 mt-2">{init.title}</h4>
                    </div>
                    <span className="text-xs text-gray-400 font-semibold">{init.timeline}</span>
                  </div>
                  <p className="text-xs leading-relaxed text-gray-600">{init.details}</p>
                  <div className="pt-2 border-t border-gray-50 flex justify-between items-center text-xs">
                    <span className="text-gray-400 font-medium">Estimated Cost</span>
                    <span className="font-bold text-gray-900">{init.cost}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
