const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

export async function apiFetch(path, { method='GET', body=null, token=null, headers={} }={}) {
  const opts = { method, headers: { ...headers } };
  if (body) {
    opts.body = JSON.stringify(body);
    opts.headers['Content-Type'] = 'application/json';
  }
  if (token) opts.headers['Authorization'] = `Bearer ${token}`;
  const res = await fetch(`${API_BASE}${path}`, opts);
  const json = await res.json().catch(()=>null);
  if (!res.ok) {
    const err = json || { error: res.statusText };
    throw err;
  }
  return json;
}
