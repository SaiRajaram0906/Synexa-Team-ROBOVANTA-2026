import { RevenueTrend, LeadFunnel } from '@/components/dashboard/KPICharts';

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Executive Dashboard</h1>
      
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-4">
        <div className="rounded-lg bg-white p-6 shadow-sm border border-gray-100">
          <h3 className="text-sm font-medium text-gray-500">Business Health</h3>
          <p className="mt-2 text-3xl font-semibold text-green-600">Excellent</p>
        </div>
        <div className="rounded-lg bg-white p-6 shadow-sm border border-gray-100">
          <h3 className="text-sm font-medium text-gray-500">Growth Score</h3>
          <p className="mt-2 text-3xl font-semibold text-blue-600">84/100</p>
        </div>
        <div className="rounded-lg bg-white p-6 shadow-sm border border-gray-100">
          <h3 className="text-sm font-medium text-gray-500">Revenue Opportunity</h3>
          <p className="mt-2 text-3xl font-semibold text-gray-900">$124,500</p>
        </div>
        <div className="rounded-lg bg-white p-6 shadow-sm border border-gray-100">
          <h3 className="text-sm font-medium text-gray-500">Risk Alerts</h3>
          <p className="mt-2 text-3xl font-semibold text-red-600">2 Warnings</p>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <RevenueTrend />
        <LeadFunnel />
      </div>

      <div className="rounded-lg bg-white p-6 shadow-sm border border-gray-100">
        <h2 className="mb-4 text-xl font-bold">AI Executive Summary</h2>
        <p className="text-gray-600">
          TODO: This panel will display the final output from the CEO Agent, summarizing the findings from Marketing, Finance, and Operations regarding current campaigns.
        </p>
      </div>
    </div>
  );
}
