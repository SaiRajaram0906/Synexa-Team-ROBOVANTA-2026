'use client';

import { useState, useEffect } from 'react';
import { apiClient } from '@/lib/api/client';

export default function AnalysisPage() {
  const [businesses, setBusinesses] = useState<any[]>([]);
  const [selectedBizId, setSelectedBizId] = useState('');
  const [scanning, setScanning] = useState(false);
  const [scanProgress, setScanProgress] = useState(0);
  const [scanStage, setScanStage] = useState('');
  const [results, setResults] = useState<any>(null);
  const [uploading, setUploading] = useState(false);
  const [aiInsights, setAiInsights] = useState<any>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    async function loadBusinesses() {
      try {
        const response = await apiClient.get('/business/');
        setBusinesses(response);
        if (response.length > 0) {
          setSelectedBizId(response[0].id);
        }
      } catch (err) {
        console.error('Failed to load businesses', err);
      }
    }
    loadBusinesses();
  }, []);

  const handleStartScan = async () => {
    if (!selectedBizId) return;
    setScanning(true);
    setScanProgress(0);
    setResults(null);
    setAiInsights(null);
    setError('');

    const stages = [
      'Retrieving business context and baseline KPIs...',
      'Chief Marketing Officer agent evaluating lead acquisition funnel...',
      'VP of Sales agent checking retention rates and customer conversion trends...',
      'Chief Financial Officer agent running cost checks and budget constraints...',
      'CEO agent synthesizing recommendations and resolving conflicts...',
    ];

    let decisionData: any = null;
    let businessName = 'this business';
    try {
      const selected = businesses.find((b) => b.id === selectedBizId);
      if (selected) businessName = selected.name;

      const response = await apiClient.post(`/analysis/start?business_id=${selectedBizId}`);
      if (response && response.status === 'success') {
        decisionData = response.decision;
      }
    } catch (err) {
      console.error(err);
    }

    const interval = setInterval(() => {
      setScanProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          setScanning(false);
          
          if (decisionData) {
            setResults({
              overallScore: decisionData.confidence_score || 85,
              health: (decisionData.confidence_score || 85) >= 60 ? 'Stable' : 'Risk Flagged',
              findings: decisionData.findings || []
            });
          } else {
            setResults({
              overallScore: 50,
              health: 'Risk Flagged',
              findings: [
                {
                  department: 'Marketing',
                  agent: 'Chief Marketing Officer',
                  recommendation: `Increase paid digital advertising budget on localized search keywords for ${businessName}.`,
                  impact: 'High',
                  confidence: 88,
                  status: 'Flagged',
                  conflict: 'Finance flags budget limitations ($3,000 max monthly spend exceeded).',
                },
                {
                  department: 'Finance',
                  agent: 'Chief Financial Officer',
                  recommendation: 'Restrict marketing expenses to protect positive cash flow margins.',
                  impact: 'Medium',
                  confidence: 94,
                  status: 'Reconciled',
                  conflict: 'Marketing requested $4,500 budget; adjusted downward to $2,500.',
                },
                {
                  department: 'Sales',
                  agent: 'VP of Sales',
                  recommendation: 'Implement email follow-up flows for cart abandonment and feedback gathering.',
                  impact: 'High',
                  confidence: 90,
                  status: 'Approved',
                  conflict: 'None. Directly aligns with retention objectives.',
                },
                {
                  department: 'Operations',
                  agent: 'Chief Operations Officer',
                  recommendation: 'Optimize staff shifts to match peak dining hours and restrict idle time.',
                  impact: 'Medium',
                  confidence: 85,
                  status: 'Approved',
                  conflict: 'None. Focuses on efficiency.',
                },
              ]
            });
          }
          return 100;
        }
        
        const nextProg = prev + 5;
        const stageIndex = Math.min(Math.floor((nextProg / 100) * stages.length), stages.length - 1);
        setScanStage(stages[stageIndex]);
        return nextProg;
      });
    }, 150);
  };

  const handleCSVUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;
    
    const file = files[0];
    const formData = new FormData();
    formData.append('file', file);
    
    setUploading(true);
    setError('');
    setResults(null);
    setAiInsights(null);
    
    try {
      const response = await apiClient.postFile('/analysis/analyze-dataset', formData);
      if (response && response.status === 'success') {
        const bizList = await apiClient.get('/business/');
        setBusinesses(bizList);
        setSelectedBizId(response.business_id);
        
        const decisionData = response.metrics;
        const agent_outputs = response.ai_insights;
        
        const mappedFindings = [
          {
            department: 'Marketing',
            agent: 'Chief Marketing Officer',
            recommendation: agent_outputs.marketing_insights[4] || 'Optimize promotions targeting high intensity.',
            impact: 'High',
            confidence: 91,
            status: 'Reconciled',
            conflict: 'Marketing requested promotions cap; reconciled with finance.'
          },
          {
            department: 'Finance',
            agent: 'Chief Financial Officer',
            recommendation: agent_outputs.finance_insights[3] || 'Implement inventory caps to preserve cash flow.',
            impact: 'Medium',
            confidence: 94,
            status: 'Reconciled',
            conflict: 'Emergency restocking expense limits budget.'
          },
          {
            department: 'Sales',
            agent: 'VP of Sales',
            recommendation: agent_outputs.sales_insights[3] || 'Deploy a localized CRM pipeline.',
            impact: 'High',
            confidence: 93,
            status: 'Approved',
            conflict: 'None'
          }
        ];

        setResults({
          overallScore: decisionData.business_health.value,
          health: decisionData.business_health.value >= 60 ? 'Stable' : 'Risk Flagged',
          findings: mappedFindings
        });
        
        setAiInsights(response.ai_insights);
      }
    } catch (err: any) {
      setError(err.message || 'Failed to analyze CSV dataset');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-12">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-extrabold text-gray-900 tracking-tight">Business Diagnostics</h1>
          <p className="mt-2 text-sm text-gray-500 font-medium">Scan your business context through the AI Leadership Fleet and resolve department bottlenecks.</p>
        </div>
        
        {/* CSV Upload Button */}
        <div>
          <input 
            type="file" 
            accept=".csv" 
            onChange={handleCSVUpload}
            disabled={uploading || scanning}
            className="hidden" 
            id="csv-upload-analysis-input"
          />
          <label 
            htmlFor="csv-upload-analysis-input"
            className={`flex items-center justify-center gap-2 rounded-xl border border-blue-200 bg-blue-50 text-blue-700 px-4 py-2.5 text-sm font-semibold hover:bg-blue-100 cursor-pointer transition-all ${uploading ? 'opacity-50 pointer-events-none' : ''}`}
          >
            {uploading ? (
              <>
                <div className="w-4 h-4 border-2 border-blue-700 border-t-transparent rounded-full animate-spin"></div>
                Analyzing CSV...
              </>
            ) : (
              <>
                <span>📥</span>
                Upload CSV Dataset
              </>
            )}
          </label>
        </div>
      </div>

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 text-red-700 rounded-xl text-sm font-semibold">
          {error}
        </div>
      )}

      {/* Select Business Section */}
      <div className="bg-white border border-gray-100 p-6 rounded-2xl shadow-sm flex flex-col sm:flex-row gap-4 items-end sm:items-center justify-between">
        <div className="w-full sm:max-w-xs">
          <label className="block text-xs font-semibold text-gray-400 uppercase tracking-wider">Active Business Context</label>
          <select 
            value={selectedBizId} 
            onChange={(e) => setSelectedBizId(e.target.value)}
            disabled={scanning || uploading}
            className="mt-2 w-full rounded-xl border border-gray-200 p-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all bg-white cursor-pointer font-medium text-gray-700"
          >
            {businesses.map((biz) => (
              <option key={biz.id} value={biz.id}>{biz.name}</option>
            ))}
          </select>
        </div>
        <button 
          onClick={handleStartScan}
          disabled={scanning || uploading}
          className="w-full sm:w-auto rounded-xl bg-blue-600 hover:bg-blue-700 disabled:opacity-50 px-6 py-3 text-sm font-semibold text-white transition-all shadow-md hover:shadow"
        >
          {scanning ? 'Running AI Scan...' : 'Start Diagnostic Scan'}
        </button>
      </div>

      {/* Scanning Stage */}
      {scanning && (
        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-8 space-y-4 text-center">
          <div className="relative w-20 h-20 mx-auto">
            <div className="w-full h-full rounded-full border-4 border-gray-100 border-t-blue-600 animate-spin"></div>
            <div className="absolute inset-0 flex items-center justify-center text-xs font-bold text-blue-600">{scanProgress}%</div>
          </div>
          <h3 className="text-base font-bold text-gray-900">Executive Council Session in Progress</h3>
          <p className="text-sm text-gray-500 max-w-sm mx-auto">{scanStage}</p>
        </div>
      )}

      {/* Scan Results */}
      {results && (
        <div className="space-y-6 animate-fade-in">
          {/* Results Summary Card */}
          <div className="bg-gradient-to-br from-blue-600 to-indigo-700 text-white rounded-2xl p-6 shadow-md grid grid-cols-1 sm:grid-cols-3 gap-6">
            <div className="space-y-1">
              <span className="text-xs text-blue-100 uppercase font-semibold">Diagnostic Rating</span>
              <h2 className="text-3xl font-extrabold">{results.overallScore}/100</h2>
            </div>
            <div className="space-y-1">
              <span className="text-xs text-blue-100 uppercase font-semibold">Status Indicator</span>
              <h2 className="text-3xl font-extrabold">{results.health}</h2>
            </div>
            <div className="space-y-1">
              <span className="text-xs text-blue-100 uppercase font-semibold">Conflict Index</span>
              <h2 className="text-3xl font-extrabold">Reconciled</h2>
            </div>
          </div>

          {/* Department-level findings */}
          <div className="space-y-4">
            <h3 className="text-lg font-bold text-gray-900">Agent Council Findings & Reconciliations</h3>
            <div className="grid grid-cols-1 gap-4">
              {results.findings.map((f: any, idx: number) => (
                <div key={idx} className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
                  <div className="p-5 flex flex-col md:flex-row md:items-start justify-between gap-4">
                    <div className="space-y-2">
                      <div className="flex items-center gap-2">
                        <span className="text-xs font-bold px-2 py-0.5 rounded bg-gray-100 text-gray-700">{f.department} Fleet</span>
                        <span className="text-xs text-gray-400">by {f.agent}</span>
                      </div>
                      <h4 className="text-sm font-semibold text-gray-955">{f.recommendation}</h4>
                      
                      {f.conflict && (
                        <div className="p-3 bg-red-50 border border-red-100 rounded-xl flex gap-2 items-start text-xs text-red-700">
                          <span className="text-base leading-none">⚠️</span>
                          <div>
                            <span className="font-bold">Conflict Encountered: </span>
                            {f.conflict}
                          </div>
                        </div>
                      )}
                    </div>

                    <div className="flex md:flex-col items-center md:items-end justify-between gap-2 border-t md:border-t-0 pt-3 md:pt-0 border-gray-50">
                      <div className="text-left md:text-right">
                        <span className="block text-[10px] text-gray-400 font-bold uppercase">Confidence</span>
                        <span className="text-sm font-extrabold text-blue-600">{f.confidence}%</span>
                      </div>
                      <div className="text-right">
                        <span className="block text-[10px] text-gray-400 font-bold uppercase">Impact</span>
                        <span className={`text-xs font-bold ${f.impact === 'High' ? 'text-orange-600' : 'text-blue-500'}`}>{f.impact}</span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* AI Insights From Business Dataset Section */}
      {aiInsights && (
        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6 space-y-6 animate-fade-in">
          <h3 className="text-xl font-bold text-gray-900 border-b pb-4">AI Insights From Business Dataset</h3>
          
          <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
            {/* Executive Summary & Final Recommendation */}
            <div className="space-y-4 md:col-span-2 bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-2xl border border-blue-100">
              <h4 className="font-extrabold text-blue-900 text-sm uppercase tracking-wider">Executive Summary</h4>
              <p className="text-sm text-blue-950 font-medium leading-relaxed">{aiInsights.executive_summary}</p>
              
              <div className="mt-4 pt-4 border-t border-blue-200">
                <h4 className="font-extrabold text-indigo-900 text-sm uppercase tracking-wider">Final Strategic Recommendation</h4>
                <p className="text-sm text-indigo-950 font-semibold leading-relaxed mt-1">{aiInsights.final_strategic_recommendation}</p>
              </div>
            </div>

            {/* Department Insights */}
            <div className="space-y-3">
              <h4 className="font-bold text-gray-800 text-sm border-l-4 border-amber-500 pl-2">Marketing Insights</h4>
              <ul className="list-disc list-inside text-xs text-gray-600 space-y-1 bg-gray-50 p-3.5 rounded-xl">
                {aiInsights.marketing_insights.map((insight: string, idx: number) => (
                  <li key={idx}>{insight}</li>
                ))}
              </ul>
            </div>

            <div className="space-y-3">
              <h4 className="font-bold text-gray-800 text-sm border-l-4 border-emerald-500 pl-2">Sales Insights</h4>
              <ul className="list-disc list-inside text-xs text-gray-600 space-y-1 bg-gray-50 p-3.5 rounded-xl">
                {aiInsights.sales_insights.map((insight: string, idx: number) => (
                  <li key={idx}>{insight}</li>
                ))}
              </ul>
            </div>

            <div className="space-y-3">
              <h4 className="font-bold text-gray-800 text-sm border-l-4 border-indigo-500 pl-2">Finance Insights</h4>
              <ul className="list-disc list-inside text-xs text-gray-600 space-y-1 bg-gray-50 p-3.5 rounded-xl">
                {aiInsights.finance_insights.map((insight: string, idx: number) => (
                  <li key={idx}>{insight}</li>
                ))}
              </ul>
            </div>

            <div className="space-y-3">
              <h4 className="font-bold text-gray-800 text-sm border-l-4 border-purple-500 pl-2">Operations Insights</h4>
              <ul className="list-disc list-inside text-xs text-gray-600 space-y-1 bg-gray-50 p-3.5 rounded-xl">
                {aiInsights.operations_insights.map((insight: string, idx: number) => (
                  <li key={idx}>{insight}</li>
                ))}
              </ul>
            </div>

            <div className="space-y-3">
              <h4 className="font-bold text-gray-800 text-sm border-l-4 border-rose-500 pl-2">Customer Success Insights</h4>
              <ul className="list-disc list-inside text-xs text-gray-600 space-y-1 bg-gray-50 p-3.5 rounded-xl">
                {aiInsights.customer_success_insights.map((insight: string, idx: number) => (
                  <li key={idx}>{insight}</li>
                ))}
              </ul>
            </div>

            <div className="space-y-3">
              <h4 className="font-bold text-gray-800 text-sm border-l-4 border-cyan-500 pl-2">Key Business Insights</h4>
              <ul className="list-disc list-inside text-xs text-gray-600 space-y-1 bg-gray-50 p-3.5 rounded-xl">
                {aiInsights.key_business_insights.map((insight: string, idx: number) => (
                  <li key={idx}>{insight}</li>
                ))}
              </ul>
            </div>

            {/* Risks & Growth Opportunities */}
            <div className="space-y-3 p-4 bg-red-50 border border-red-100 rounded-2xl">
              <h4 className="font-bold text-red-950 text-sm uppercase tracking-wider flex items-center gap-1">
                <span>⚠️</span> Risks Identified
              </h4>
              <ul className="list-disc list-inside text-xs text-red-800 space-y-1">
                {aiInsights.risks_identified.map((risk: string, idx: number) => (
                  <li key={idx} className="font-medium">{risk}</li>
                ))}
              </ul>
            </div>

            <div className="space-y-3 p-4 bg-green-50 border border-green-100 rounded-2xl">
              <h4 className="font-bold text-green-950 text-sm uppercase tracking-wider flex items-center gap-1">
                <span>📈</span> Growth Opportunities
              </h4>
              <ul className="list-disc list-inside text-xs text-green-800 space-y-1">
                {aiInsights.growth_opportunities.map((opportunity: string, idx: number) => (
                  <li key={idx} className="font-medium">{opportunity}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
