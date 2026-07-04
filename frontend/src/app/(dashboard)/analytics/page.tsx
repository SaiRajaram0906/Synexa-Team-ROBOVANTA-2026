'use client';

import { useState } from 'react';
import { 
  ResponsiveContainer, 
  AreaChart, 
  Area, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  BarChart, 
  Bar, 
  Legend 
} from 'recharts';

export default function AnalyticsPage() {
  const [selectedBiz, setSelectedBiz] = useState('The Rustic Spoon');

  const businesses = ['The Rustic Spoon', 'Lumina Apparel', 'IronCore Fitness'];

  // Mock charts data
  const revenueHistory = [
    { month: 'Jan', revenue: 28000, expenses: 19000 },
    { month: 'Feb', revenue: 29500, expenses: 18500 },
    { month: 'Mar', revenue: 30000, expenses: 20000 },
    { month: 'Apr', revenue: 32000, expenses: 21000 },
    { month: 'May', revenue: 35000, expenses: 22000 },
    { month: 'Jun', revenue: 39500, expenses: 23000 },
  ];

  const acquisitionMetrics = [
    { channel: 'Search Ads', cac: 45, ltv: 350 },
    { channel: 'Social Media', cac: 60, ltv: 420 },
    { channel: 'Email loyalty', cac: 12, ltv: 580 },
    { channel: 'Referrals', cac: 8, ltv: 650 },
  ];

  return (
    <div className="max-w-6xl mx-auto space-y-6 pb-12">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-extrabold text-gray-900 tracking-tight">Analytics & Trends</h1>
          <p className="mt-2 text-sm text-gray-500 font-medium">Verify historical performance vectors, customer acquisition cost, and revenue margins.</p>
        </div>

        <select 
          value={selectedBiz} 
          onChange={(e) => setSelectedBiz(e.target.value)}
          className="rounded-xl border border-gray-200 p-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all bg-white"
        >
          {businesses.map((biz) => (
            <option key={biz} value={biz}>{biz}</option>
          ))}
        </select>
      </div>

      {/* Analytics Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white rounded-2xl border border-gray-100 p-6 shadow-sm">
          <span className="block text-xs text-gray-400 font-bold uppercase">Customer Lifetime Value (LTV)</span>
          <h3 className="text-2xl font-extrabold text-gray-900 mt-2">$480</h3>
          <span className="text-xs text-emerald-600 font-semibold mt-1 inline-block">↑ 12% vs last quarter</span>
        </div>
        <div className="bg-white rounded-2xl border border-gray-100 p-6 shadow-sm">
          <span className="block text-xs text-gray-400 font-bold uppercase">Average Acquisition Cost (CAC)</span>
          <h3 className="text-2xl font-extrabold text-gray-900 mt-2">$31</h3>
          <span className="text-xs text-emerald-600 font-semibold mt-1 inline-block">↓ 8% optimization</span>
        </div>
        <div className="bg-white rounded-2xl border border-gray-100 p-6 shadow-sm">
          <span className="block text-xs text-gray-400 font-bold uppercase">LTV:CAC Ratio</span>
          <h3 className="text-2xl font-extrabold text-blue-600 mt-2">15.4x</h3>
          <span className="text-xs text-blue-600 font-semibold mt-1 inline-block">High growth health</span>
        </div>
      </div>

      {/* Main Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Revenue Growth Chart */}
        <div className="bg-white rounded-2xl border border-gray-100 p-6 shadow-sm space-y-4">
          <div>
            <h3 className="text-base font-bold text-gray-900">Revenue vs. Expenses Trend</h3>
            <p className="text-xs text-gray-400">Monthly breakdown of gross revenue against department cost budgets.</p>
          </div>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={revenueHistory}>
                <defs>
                  <linearGradient id="colorRevenue" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#2563eb" stopOpacity={0.2}/>
                    <stop offset="95%" stopColor="#2563eb" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="month" stroke="#94a3b8" fontSize={11} />
                <YAxis stroke="#94a3b8" fontSize={11} />
                <Tooltip />
                <Legend verticalAlign="top" height={36} iconType="circle" />
                <Area type="monotone" dataKey="revenue" stroke="#2563eb" strokeWidth={2} fillOpacity={1} fill="url(#colorRevenue)" name="Gross Revenue" />
                <Area type="monotone" dataKey="expenses" stroke="#f43f5e" strokeWidth={2} fill="none" name="Expenses" strokeDasharray="5 5" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* CAC vs LTV Comparison */}
        <div className="bg-white rounded-2xl border border-gray-100 p-6 shadow-sm space-y-4">
          <div>
            <h3 className="text-base font-bold text-gray-900">CAC vs. Lifetime Value (LTV) by Channel</h3>
            <p className="text-xs text-gray-400">Compare customer acquisition efficiency against projected value yields.</p>
          </div>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={acquisitionMetrics}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="channel" stroke="#94a3b8" fontSize={11} />
                <YAxis stroke="#94a3b8" fontSize={11} />
                <Tooltip />
                <Legend verticalAlign="top" height={36} iconType="circle" />
                <Bar dataKey="cac" fill="#f43f5e" name="Acquisition Cost (CAC)" radius={[4, 4, 0, 0]} />
                <Bar dataKey="ltv" fill="#10b981" name="Customer Lifetime Value (LTV)" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
