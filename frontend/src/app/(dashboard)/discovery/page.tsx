'use client';

import { useState } from 'react';
import { apiClient } from '@/lib/api/client';

export default function DiscoveryPage() {
  const [step, setStep] = useState(1);
  const [bizName, setBizName] = useState('');
  const [industry, setIndustry] = useState('SaaS');
  const [goals, setGoals] = useState('');
  const [kpis, setKpis] = useState({
    revenue: '',
    leads: '',
    retention: '',
    churn: '',
  });
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleNext = () => setStep((s) => s + 1);
  const handleBack = () => setStep((s) => s - 1);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const payload = {
        name: bizName,
        industry: industry,
        goals: goals ? [goals] : [],
        kpis: {
          current_revenue: kpis.revenue ? parseFloat(kpis.revenue) : 0,
          leads: kpis.leads ? parseInt(kpis.leads) : 0,
          customer_retention: kpis.retention ? parseFloat(kpis.retention) : 0.8,
          churn_rate: kpis.churn ? parseFloat(kpis.churn) : 0.1,
        }
      };
      await apiClient.post('/business/', payload);
      setSubmitted(true);
    } catch (err: any) {
      alert('Failed to save business profile: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const industries = [
    { name: 'SaaS', icon: '💻', desc: 'Software-as-a-Service startups and scaleups' },
    { name: 'Restaurant', icon: '🍳', desc: 'Dining establishments, cafes, and eateries' },
    { name: 'Retail', icon: '🛍️', desc: 'Boutiques, physical storefronts, and apparel stores' },
    { name: 'E-commerce', icon: '🛒', desc: 'Digital storefronts and direct-to-consumer brands' },
    { name: 'Gym & Fitness', icon: '💪', desc: 'Health clubs, yoga studios, and training facilities' },
    { name: 'Healthcare', icon: '🩺', desc: 'Medical clinics, wellness spaces, and dental offices' },
  ];

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-12">
      <div>
        <h1 className="text-3xl font-extrabold text-gray-900 tracking-tight">Business Discovery intake</h1>
        <p className="mt-2 text-sm text-gray-500">Discover and structure your business context. Set objectives for the AI agent fleet.</p>
      </div>

      {submitted ? (
        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-8 text-center space-y-4">
          <div className="w-16 h-16 bg-green-50 text-green-600 rounded-full flex items-center justify-center mx-auto text-2xl">✓</div>
          <h2 className="text-xl font-bold text-gray-900">Business Profile Created!</h2>
          <p className="text-sm text-gray-500 max-w-md mx-auto">
            Successfully generated context for <strong>{bizName}</strong> ({industry}). Specialized AI executives are now ready to run scans and draft strategy proposals.
          </p>
          <div className="pt-4 flex justify-center gap-4">
            <button 
              onClick={() => { setSubmitted(false); setStep(1); setBizName(''); }}
              className="px-4 py-2 border border-gray-200 rounded-xl text-sm font-semibold text-gray-700 hover:bg-gray-50"
            >
              Add Another Business
            </button>
            <a 
              href="/analysis"
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-sm font-semibold shadow-sm hover:shadow"
            >
              Proceed to Analysis
            </a>
          </div>
        </div>
      ) : (
        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
          {/* Progress bar */}
          <div className="h-1.5 bg-gray-50 flex">
            <div className={`h-full bg-blue-600 transition-all duration-300`} style={{ width: `${(step / 3) * 100}%` }}></div>
          </div>

          <div className="p-6 md:p-8 space-y-6">
            {/* Step 1: Basic Info */}
            {step === 1 && (
              <div className="space-y-6">
                <div className="border-b border-gray-100 pb-4">
                  <h3 className="text-lg font-bold text-gray-900">Step 1: Business Profile</h3>
                  <p className="text-xs text-gray-400">Introduce your business and select your industry vertical.</p>
                </div>

                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-semibold text-gray-700">Business Name</label>
                    <input 
                      type="text" 
                      placeholder="e.g. The Rustic Spoon"
                      value={bizName}
                      onChange={(e) => setBizName(e.target.value)}
                      className="mt-2 w-full rounded-xl border border-gray-200 p-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">Industry Sector</label>
                    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                      {industries.map((ind) => (
                        <div 
                          key={ind.name}
                          onClick={() => setIndustry(ind.name)}
                          className={`p-4 rounded-xl border-2 text-left cursor-pointer transition-all ${
                            industry === ind.name 
                              ? 'border-blue-600 bg-blue-50/10' 
                              : 'border-gray-100 hover:border-gray-200 hover:bg-gray-50/20'
                          }`}
                        >
                          <span className="text-2xl">{ind.icon}</span>
                          <h4 className="text-sm font-bold text-gray-950 mt-2">{ind.name}</h4>
                          <p className="text-xs text-gray-400 mt-1">{ind.desc}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                <div className="flex justify-end pt-4">
                  <button 
                    disabled={!bizName}
                    onClick={handleNext}
                    className="rounded-xl bg-blue-600 hover:bg-blue-700 disabled:opacity-50 px-6 py-3 text-sm font-semibold text-white transition-all shadow-sm hover:shadow"
                  >
                    Next Step: Target Objectives
                  </button>
                </div>
              </div>
            )}

            {/* Step 2: Goals */}
            {step === 2 && (
              <div className="space-y-6">
                <div className="border-b border-gray-100 pb-4">
                  <h3 className="text-lg font-bold text-gray-900">Step 2: Objectives & Obstacles</h3>
                  <p className="text-xs text-gray-400">Describe what you want to achieve and what holds you back.</p>
                </div>

                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-semibold text-gray-700">What are your primary growth goals?</label>
                    <textarea 
                      rows={4}
                      placeholder="e.g. Increase weekday lunch reservations by 20%, expand catering revenue, and reduce food waste."
                      value={goals}
                      onChange={(e) => setGoals(e.target.value)}
                      className="mt-2 w-full rounded-xl border border-gray-200 p-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all resize-none"
                    />
                  </div>

                  <div className="p-4 bg-amber-50/50 border border-amber-100 rounded-xl space-y-1">
                    <h4 className="text-xs font-bold text-amber-850">💡 Tips for business goals</h4>
                    <p className="text-[11px] text-amber-700">
                      Be as specific as possible (e.g. include target values, timeframes, or target customer segments) so the strategy generation agents can optimize recommendations.
                    </p>
                  </div>
                </div>

                <div className="flex justify-between pt-4">
                  <button 
                    onClick={handleBack}
                    className="px-6 py-3 border border-gray-200 rounded-xl text-sm font-semibold text-gray-700 hover:bg-gray-50 transition-all"
                  >
                    Back
                  </button>
                  <button 
                    onClick={handleNext}
                    className="rounded-xl bg-blue-600 hover:bg-blue-700 px-6 py-3 text-sm font-semibold text-white transition-all shadow-sm hover:shadow"
                  >
                    Next Step: Business Metrics
                  </button>
                </div>
              </div>
            )}

            {/* Step 3: KPIs */}
            {step === 3 && (
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="border-b border-gray-100 pb-4">
                  <h3 className="text-lg font-bold text-gray-900">Step 3: KPI Metrics Baseline</h3>
                  <p className="text-xs text-gray-400">Provide baseline numbers for calculating executive health indicators.</p>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-semibold text-gray-700">Monthly Revenue ($)</label>
                    <input 
                      type="number" 
                      placeholder="e.g. 35000"
                      value={kpis.revenue}
                      onChange={(e) => setKpis({ ...kpis, revenue: e.target.value })}
                      className="mt-2 w-full rounded-xl border border-gray-200 p-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-700">Monthly New Leads</label>
                    <input 
                      type="number" 
                      placeholder="e.g. 450"
                      value={kpis.leads}
                      onChange={(e) => setKpis({ ...kpis, leads: e.target.value })}
                      className="mt-2 w-full rounded-xl border border-gray-200 p-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-700">Customer Retention (%)</label>
                    <input 
                      type="number" 
                      step="0.01"
                      placeholder="e.g. 0.85"
                      value={kpis.retention}
                      onChange={(e) => setKpis({ ...kpis, retention: e.target.value })}
                      className="mt-2 w-full rounded-xl border border-gray-200 p-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-700">Churn Rate (%)</label>
                    <input 
                      type="number" 
                      step="0.01"
                      placeholder="e.g. 0.05"
                      value={kpis.churn}
                      onChange={(e) => setKpis({ ...kpis, churn: e.target.value })}
                      className="mt-2 w-full rounded-xl border border-gray-200 p-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all"
                    />
                  </div>
                </div>

                <div className="flex justify-between pt-4">
                  <button 
                    type="button"
                    onClick={handleBack}
                    className="px-6 py-3 border border-gray-200 rounded-xl text-sm font-semibold text-gray-700 hover:bg-gray-50 transition-all"
                  >
                    Back
                  </button>
                  <button 
                    type="submit"
                    disabled={loading}
                    className="rounded-xl bg-blue-600 hover:bg-blue-700 disabled:opacity-50 px-6 py-3 text-sm font-semibold text-white transition-all shadow-md hover:shadow-lg"
                  >
                    {loading ? 'Saving Context...' : 'Submit Business Context'}
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
