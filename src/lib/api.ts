export type ApiResult<T> = { ok: true; data: T } | { ok: false; error: string };

export async function api<T>(path: string, init?: RequestInit): Promise<ApiResult<T>> {
  try {
    const res = await fetch(`/api${path}`, {
      headers: { 'Content-Type': 'application/json', ...(init?.headers || {}) },
      ...init,
    });
    if (!res.ok) return { ok: false, error: `HTTP ${res.status}` };
    const data = await res.json();
    return { ok: true, data } as ApiResult<T>;
  } catch (e: any) {
    return { ok: false, error: e?.message || 'Network error' };
  }
}
