const API_BASE = typeof window !== 'undefined' ? '' : 'http://localhost:8000';

export function getToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('access_token');
}

export function setTokens(access: string, refresh?: string) {
  localStorage.setItem('access_token', access);
  if (refresh) localStorage.setItem('refresh_token', refresh);
}

export function clearTokens() {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
}

export async function apiFetch(path: string, options: RequestInit = {}): Promise<Response> {
  const token = getToken();
  const headers: Record<string, string> = {
    ...(options.headers as Record<string, string> || {}),
  };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  if (!(options.body instanceof FormData) && !headers['Content-Type']) {
    headers['Content-Type'] = 'application/json';
  }

  let res = await fetch(`${API_BASE}${path}`, { ...options, headers });

  if (res.status === 401 && typeof window !== 'undefined') {
    const refreshed = await tryRefresh();
    if (refreshed) {
      headers['Authorization'] = `Bearer ${getToken()}`;
      res = await fetch(`${API_BASE}${path}`, { ...options, headers });
    }
  }
  return res;
}

async function tryRefresh(): Promise<boolean> {
  const refresh = localStorage.getItem('refresh_token');
  if (!refresh) return false;
  try {
    const res = await fetch(`${API_BASE}/api/refresh`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh_token: refresh }),
    });
    if (!res.ok) return false;
    const data = await res.json();
    setTokens(data.access_token, data.refresh_token);
    return true;
  } catch {
    return false;
  }
}

export interface UserProfile {
  id: number;
  email: string;
  plan: string;
  subscription_status: string | null;
  usage: {
    plan: string;
    plan_name: string;
    plan_name_en: string;
    uploads_used: number;
    uploads_limit: number | null;
    exports_used: number;
    exports_limit: number | null;
    max_file_size_mb: number;
    formats: string[];
  };
  plans: Record<string, { name: string; name_en: string; price_monthly: number }>;
}

export async function fetchProfile(): Promise<UserProfile | null> {
  const res = await apiFetch('/api/profile');
  if (!res.ok) return null;
  return res.json();
}
