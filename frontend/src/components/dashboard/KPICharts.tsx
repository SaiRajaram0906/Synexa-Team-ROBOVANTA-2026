'use client';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';

const data = [
  { name: 'Jan', revenue: 4000, leads: 2400 },
  { name: 'Feb', revenue: 3000, leads: 1398 },
  { name: 'Mar', revenue: 2000, leads: 9800 },
  { name: 'Apr', revenue: 2780, leads: 3908 },
  { name: 'May', revenue: 1890, leads: 4800 },
  { name: 'Jun', revenue: 2390, leads: 3800 },
];

export function RevenueTrend() {
  return (
    <div className="h-64 w-full bg-white p-4 shadow rounded-lg">
      <h3 className="mb-4 font-semibold text-gray-700">Revenue Trend</h3>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="revenue" stroke="#2563eb" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export function LeadFunnel() {
  return (
    <div className="h-64 w-full bg-white p-4 shadow rounded-lg">
      <h3 className="mb-4 font-semibold text-gray-700">Lead Generation</h3>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="leads" fill="#16a34a" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
