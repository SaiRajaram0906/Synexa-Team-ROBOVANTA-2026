'use client';

import { useState } from 'react';

export default function SettingsPage() {
  const [apiKey, setApiKey] = useState('●●●●●●●●●●●●●●●●●●●●●●●●');
  const [model, setModel] = useState('gemini-1.5-pro-latest');
  const [temperature, setTemperature] = useState(0.7);
  const [activeAgents, setActiveAgents] = useState({
    cmo: true,
    cfo: true,
    coo: true,
    cso: true,
    cs: false,
  });
  const [saved, setSaved] = useState(false);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-12">
      <div>
        <h1 className="text-3xl font-extrabold text-gray-900 tracking-tight">System Settings</h1>
        <p className="mt-2 text-sm text-gray-500">Configure your Synexa Growth OS AI orchestrators, database, and API keys.</p>
      </div>

      <form onSubmit={handleSave} className="space-y-6">
        {/* LLM Config Card */}
        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6 space-y-6">
          <div className="border-b border-gray-100 pb-4">
            <h2 className="text-lg font-bold text-gray-900">LLM Provider Configuration</h2>
            <p className="text-xs text-gray-400">Manage connections to Google Generative AI.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700">Google API Key</label>
              <input 
                type="password" 
                value={apiKey} 
                onChange={(e) => setApiKey(e.target.value)}
                className="mt-2 w-full rounded-xl border border-gray-200 p-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700">Select Model Version</label>
              <select 
                value={model} 
                onChange={(e) => setModel(e.target.value)}
                className="mt-2 w-full rounded-xl border border-gray-200 p-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all bg-white"
              >
                <option value="gemini-1.5-pro-latest">Gemini 1.5 Pro (Recommended)</option>
                <option value="gemini-1.5-flash-latest">Gemini 1.5 Flash</option>
                <option value="gemini-1.0-pro">Gemini 1.0 Pro</option>
              </select>
            </div>
          </div>

          <div>
            <div className="flex justify-between items-center">
              <label className="block text-sm font-semibold text-gray-700">Temperature: {temperature}</label>
              <span className="text-xs text-gray-400">{temperature === 0 ? 'Deterministic' : temperature > 0.8 ? 'Creative' : 'Balanced'}</span>
            </div>
            <input 
              type="range" 
              min="0" 
              max="1" 
              step="0.1" 
              value={temperature} 
              onChange={(e) => setTemperature(parseFloat(e.target.value))}
              className="mt-3 w-full accent-blue-600"
            />
          </div>
        </div>

        {/* AI Agent Toggles Card */}
        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6 space-y-6">
          <div className="border-b border-gray-100 pb-4">
            <h2 className="text-lg font-bold text-gray-900">Active Executive Agent Fleet</h2>
            <p className="text-xs text-gray-400">Toggle specialized AI executives active in the Strategy Generation Crew.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex items-center justify-between p-4 rounded-xl border border-gray-50 hover:border-gray-100 transition-all bg-gray-50/30">
              <div>
                <h4 className="text-sm font-semibold text-gray-950">Chief Marketing Officer (CMO)</h4>
                <p className="text-xs text-gray-400 mt-1">Generates customer acquisition campaigns</p>
              </div>
              <input 
                type="checkbox" 
                checked={activeAgents.cmo} 
                onChange={(e) => setActiveAgents({ ...activeAgents, cmo: e.target.checked })}
                className="w-4 h-4 rounded text-blue-600 focus:ring-blue-500" 
              />
            </div>

            <div className="flex items-center justify-between p-4 rounded-xl border border-gray-50 hover:border-gray-100 transition-all bg-gray-50/30">
              <div>
                <h4 className="text-sm font-semibold text-gray-950">Chief Financial Officer (CFO)</h4>
                <p className="text-xs text-gray-400 mt-1">Estimates ROI and checks budget safety</p>
              </div>
              <input 
                type="checkbox" 
                checked={activeAgents.cfo} 
                onChange={(e) => setActiveAgents({ ...activeAgents, cfo: e.target.checked })}
                className="w-4 h-4 rounded text-blue-600 focus:ring-blue-500" 
              />
            </div>

            <div className="flex items-center justify-between p-4 rounded-xl border border-gray-50 hover:border-gray-100 transition-all bg-gray-50/30">
              <div>
                <h4 className="text-sm font-semibold text-gray-950">Chief Operations Officer (COO)</h4>
                <p className="text-xs text-gray-400 mt-1">Evaluates capacity and constraints</p>
              </div>
              <input 
                type="checkbox" 
                checked={activeAgents.coo} 
                onChange={(e) => setActiveAgents({ ...activeAgents, coo: e.target.checked })}
                className="w-4 h-4 rounded text-blue-600 focus:ring-blue-500" 
              />
            </div>

            <div className="flex items-center justify-between p-4 rounded-xl border border-gray-50 hover:border-gray-100 transition-all bg-gray-50/30">
              <div>
                <h4 className="text-sm font-semibold text-gray-950">Chief Strategy Officer (CSO)</h4>
                <p className="text-xs text-gray-400 mt-1">Translates data to core OKRs</p>
              </div>
              <input 
                type="checkbox" 
                checked={activeAgents.cso} 
                onChange={(e) => setActiveAgents({ ...activeAgents, cso: e.target.checked })}
                className="w-4 h-4 rounded text-blue-600 focus:ring-blue-500" 
              />
            </div>
          </div>
        </div>

        {/* Action Button */}
        <div className="flex justify-end items-center gap-4">
          {saved && (
            <span className="text-sm font-medium text-emerald-600 animate-fade-in">
              ✓ Settings saved successfully!
            </span>
          )}
          <button 
            type="submit" 
            className="rounded-xl bg-blue-600 hover:bg-blue-700 px-6 py-3 text-sm font-semibold text-white shadow-md transition-all hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-blue-500/20"
          >
            Save Configuration
          </button>
        </div>
      </form>
    </div>
  );
}
