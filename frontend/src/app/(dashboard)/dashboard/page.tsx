'use client';

import { useEffect, useState } from 'react';
import { 
  RevenueTrend, 
  LeadFunnel, 
  DemandForecastChart,
  MarketingPerformanceChart,
  InventoryHealthChart,
  SupplyChainPerformanceChart,
  CustomerSatisfactionChart
} from '@/components/dashboard/KPICharts';
import { apiClient } from '@/lib/api/client';

export default function DashboardPage() {
  const [businesses, setBusinesses] = useState<any[]>([]);
  const [selectedBizId, setSelectedBizId] = useState('');
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState('');
  const [loadingMetrics, setLoadingMetrics] = useState(false);
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    async function loadBusinesses() {
      try {
        const response = await apiClient.get('/business/');
        setBusinesses(response);
        if (response.length > 0) {
          setSelectedBizId(response[0].id);
        }
      } catch (err: any) {
        setError(err.message);
      }
    }
    loadBusinesses();
  }, []);

  useEffect(() => {
    if (!selectedBizId) return;
    async function loadDashboardData() {
      setLoadingMetrics(true);
      try {
        const response = await apiClient.get(`/dashboard?business_id=${selectedBizId}`);
        setData(response);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoadingMetrics(false);
      }
    }
    loadDashboardData();
  }, [selectedBizId]);

  const handleCSVUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;
    
    const file = files[0];
    const formData = new FormData();
    formData.append('file', file);
    
    setUploading(true);
    setError('');
    
    try {
      const response = await apiClient.postFile('/analysis/analyze-dataset', formData);
      if (response && response.status === 'success') {
        const bizList = await apiClient.get('/business/');
        setBusinesses(bizList);
        setSelectedBizId(response.business_id);
        
        setData({
          metrics: response.metrics,
          charts: response.charts
        });
      }
    } catch (err: any) {
      setError(err.message || 'Failed to upload and analyze CSV');
    } finally {
      setUploading(false);
    }
  };

  if (error) return <div className="p-8 text-red-500 font-medium">Error: {error}</div>;
  if (businesses.length === 0) return <div className="p-8">Loading businesses list...</div>;

  return (
    <div className="space-y-6 pb-12">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-extrabold text-gray-900 tracking-tight">Executive Dashboard</h1>
          <p className="mt-2 text-sm text-gray-500 font-medium">Consolidated view of your enterprise and active growth indicators.</p>
        </div>
        
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 w-full md:w-auto">
          {/* CSV File Upload Section */}
          <div className="relative">
            <input 
              type="file" 
              accept=".csv" 
              onChange={handleCSVUpload}
              disabled={uploading}
              className="hidden" 
              id="csv-upload-input"
            />
            <label 
              htmlFor="csv-upload-input"
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

          {/* Active Business Select Dropdown */}
          <div className="bg-white border border-gray-100 p-2.5 rounded-xl shadow-sm w-full sm:w-64">
            <select 
              value={selectedBizId} 
              onChange={(e) => setSelectedBizId(e.target.value)}
              className="w-full rounded-lg border border-gray-200 p-2 text-sm font-medium focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 bg-white cursor-pointer"
            >
              {businesses.map((biz) => (
                <option key={biz.id} value={biz.id}>{biz.name}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {loadingMetrics || !data ? (
        <div className="p-8 text-gray-500 font-medium">Loading KPI metrics...</div>
      ) : (
        <>
          {/* Metrics Grid */}
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-4 animate-fade-in">
            <div className="rounded-2xl bg-white p-6 shadow-sm border border-gray-100 hover:shadow-md transition-all">
              <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wider">Business Health</h3>
              <p className="mt-2 text-3xl font-extrabold text-green-600">{data.metrics.business_health.value}/100</p>
            </div>
            <div className="rounded-2xl bg-white p-6 shadow-sm border border-gray-100 hover:shadow-md transition-all">
              <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wider">Growth Score</h3>
              <p className="mt-2 text-3xl font-extrabold text-blue-600">{data.metrics.growth_score.value}/100</p>
            </div>
            <div className="rounded-2xl bg-white p-6 shadow-sm border border-gray-100 hover:shadow-md transition-all">
              <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wider">Revenue Opportunity</h3>
              <p className="mt-2 text-3xl font-extrabold text-gray-900">${data.metrics.revenue_opportunity.value.toLocaleString()}</p>
            </div>
            <div className="rounded-2xl bg-white p-6 shadow-sm border border-gray-100 hover:shadow-md transition-all">
              <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wider">Risk Alerts</h3>
              <p className="mt-2 text-3xl font-extrabold text-red-600">{data.metrics.risk_alerts.value} Warnings</p>
            </div>
          </div>

          {/* Charts Grid */}
          <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
            <div className="lg:col-span-2">
              <RevenueTrend data={data.charts.revenue_trend} />
            </div>
            <div>
              <LeadFunnel data={data.charts.revenue_trend} />
            </div>
            <div className="lg:col-span-3 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {data.charts.demand_forecast && <DemandForecastChart data={data.charts.demand_forecast} />}
              {data.charts.marketing_performance && <MarketingPerformanceChart data={data.charts.marketing_performance} />}
              {data.charts.inventory_health && <InventoryHealthChart data={data.charts.inventory_health} />}
              {data.charts.supply_chain_performance && <SupplyChainPerformanceChart data={data.charts.supply_chain_performance} />}
              {data.charts.customer_satisfaction && <CustomerSatisfactionChart data={data.charts.customer_satisfaction} />}
            </div>
          </div>

          {/* AI Executive Summary */}
          <div className="rounded-2xl bg-white p-6 shadow-sm border border-gray-100 hover:shadow-md transition-all">
            <h2 className="mb-4 text-xl font-bold text-gray-900">AI Executive Summary</h2>
            <p className="text-gray-600 leading-relaxed">{data.metrics.executive_summary}</p>
          </div>
        </>
      )}
    </div>
  );
}
