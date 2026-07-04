'use client';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, Legend } from 'recharts';

export function RevenueTrend({ data }: { data: any[] }) {
  return (
    <div className="h-72 w-full bg-white p-5 shadow rounded-2xl border border-gray-100">
      <h3 className="mb-4 font-semibold text-gray-700 font-sans">Revenue Trend ($)</h3>
      <ResponsiveContainer width="100%" height="80%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f3f4f6" />
          <XAxis dataKey="name" stroke="#9ca3af" fontSize={12} />
          <YAxis stroke="#9ca3af" fontSize={12} />
          <Tooltip />
          <Line type="monotone" dataKey="revenue" stroke="#2563eb" strokeWidth={3} activeDot={{ r: 8 }} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export function LeadFunnel({ data }: { data: any[] }) {
  return (
    <div className="h-72 w-full bg-white p-5 shadow rounded-2xl border border-gray-100">
      <h3 className="mb-4 font-semibold text-gray-700 font-sans">Lead Generation</h3>
      <ResponsiveContainer width="100%" height="80%">
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f3f4f6" />
          <XAxis dataKey="name" stroke="#9ca3af" fontSize={12} />
          <YAxis stroke="#9ca3af" fontSize={12} />
          <Tooltip />
          <Bar dataKey="leads" fill="#16a34a" radius={[6, 6, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export function DemandForecastChart({ data }: { data: any[] }) {
  return (
    <div className="h-72 w-full bg-white p-5 shadow rounded-2xl border border-gray-100">
      <h3 className="mb-4 font-semibold text-gray-700 font-sans">Demand Forecast vs Actuals</h3>
      <ResponsiveContainer width="100%" height="80%">
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f3f4f6" />
          <XAxis dataKey="name" stroke="#9ca3af" fontSize={12} />
          <YAxis stroke="#9ca3af" fontSize={12} />
          <Tooltip />
          <Legend />
          <Bar dataKey="forecasted" fill="#3b82f6" name="Forecasted" radius={[4, 4, 0, 0]} />
          <Bar dataKey="actual" fill="#10b981" name="Actual" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export function MarketingPerformanceChart({ data }: { data: any[] }) {
  return (
    <div className="h-72 w-full bg-white p-5 shadow rounded-2xl border border-gray-100">
      <h3 className="mb-4 font-semibold text-gray-700 font-sans">Marketing Performance (Spend per Promo)</h3>
      <ResponsiveContainer width="100%" height="80%">
        <BarChart data={data} layout="vertical">
          <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#f3f4f6" />
          <XAxis type="number" stroke="#9ca3af" fontSize={12} />
          <YAxis dataKey="name" type="category" stroke="#9ca3af" fontSize={12} />
          <Tooltip />
          <Bar dataKey="spend" fill="#f59e0b" name="Spend ($)" radius={[0, 4, 4, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export function InventoryHealthChart({ data }: { data: any[] }) {
  return (
    <div className="h-72 w-full bg-white p-5 shadow rounded-2xl border border-gray-100">
      <h3 className="mb-4 font-semibold text-gray-700 font-sans">Inventory Health Metrics</h3>
      <ResponsiveContainer width="100%" height="80%">
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f3f4f6" />
          <XAxis dataKey="name" stroke="#9ca3af" fontSize={12} />
          <YAxis stroke="#9ca3af" fontSize={12} />
          <Tooltip />
          <Bar dataKey="value" fill="#ec4899" radius={[6, 6, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export function SupplyChainPerformanceChart({ data }: { data: any[] }) {
  return (
    <div className="h-72 w-full bg-white p-5 shadow rounded-2xl border border-gray-100">
      <h3 className="mb-4 font-semibold text-gray-700 font-sans">Supply Chain Performance</h3>
      <ResponsiveContainer width="100%" height="80%">
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f3f4f6" />
          <XAxis dataKey="name" stroke="#9ca3af" fontSize={12} />
          <YAxis stroke="#9ca3af" fontSize={12} />
          <Tooltip />
          <Bar dataKey="value" fill="#8b5cf6" radius={[6, 6, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export function CustomerSatisfactionChart({ data }: { data: any[] }) {
  return (
    <div className="h-72 w-full bg-white p-5 shadow rounded-2xl border border-gray-100">
      <h3 className="mb-4 font-semibold text-gray-700 font-sans">Customer Satisfaction & Return Rates (%)</h3>
      <ResponsiveContainer width="100%" height="80%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f3f4f6" />
          <XAxis dataKey="name" stroke="#9ca3af" fontSize={12} />
          <YAxis stroke="#9ca3af" fontSize={12} />
          <Tooltip />
          <Line type="monotone" dataKey="value" stroke="#ef4444" strokeWidth={3} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
