import { supabase } from '../supabase';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

async function fetchWithAuth(endpoint: string, options: RequestInit = {}, isMultipart: boolean = false) {
  const { data: { session } } = await supabase.auth.getSession();
  const token = session?.access_token;
  
  const headers = {
    ...(isMultipart ? {} : { 'Content-Type': 'application/json' }),
    Authorization: token ? `Bearer ${token}` : 'Bearer dummy-token',
    ...options.headers,
  };

  const response = await fetch(`${API_BASE}${endpoint}`, { ...options, headers });
  if (!response.ok) {
    throw new Error(`API Error: ${response.statusText}`);
  }
  return response.json();
}

export const apiClient = {
  get: (url: string) => fetchWithAuth(url, { method: 'GET' }),
  post: (url: string, data: any) => fetchWithAuth(url, { method: 'POST', body: JSON.stringify(data) }),
  postFile: (url: string, formData: FormData) => fetchWithAuth(url, { method: 'POST', body: formData }, true),
  put: (url: string, data: any) => fetchWithAuth(url, { method: 'PUT', body: JSON.stringify(data) }),
  delete: (url: string) => fetchWithAuth(url, { method: 'DELETE' }),
};
