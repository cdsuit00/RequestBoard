import React, { useState, useEffect, useContext } from 'react';
import { apiFetch } from '../api/client';
import AuthContext from '../contexts/AuthContext';
import RequestCard from './RequestCard';

export default function RequestList() {
  const [page, setPage] = useState(1);
  const [perPage] = useState(10);
  const [data, setData] = useState({ items: [], total:0 });
  const { token } = useContext(AuthContext);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    let mounted = true;
    setLoading(true);
    apiFetch(`/requests?page=${page}&per_page=${perPage}`)
      .then(res => { if (mounted) setData(res); })
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
    return () => { mounted = false; };
  }, [page, perPage, token]);

  return (
    <div>
      {loading ? <div>Loading…</div> : (
        <>
          <div className="request-grid">
            {data.items.map(r => <RequestCard key={r.id} request={r} />)}
          </div>
          <div className="pagination">
            <button disabled={page<=1} onClick={()=>setPage(p=>p-1)}>Prev</button>
            <span>Page {page} — {data.total} total</span>
            <button disabled={page>=data.pages} onClick={()=>setPage(p=>p+1)}>Next</button>
          </div>
        </>
      )}
    </div>
  );
}
