import { useState, useEffect, useContext } from 'react';
import { apiFetch } from '../api/client';
import AuthContext from '../contexts/AuthContext';
import ResponseForm from './ResponseForm';

export default function RequestDetail({ requestId }) {
  const { token } = useContext(AuthContext);
  const [req, setReq] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    apiFetch(`/requests/${requestId}`).then(res => setReq(res)).finally(()=>setLoading(false));
  }, [requestId]);

  const addResponse = async (content) => {
    // optimistic UI: add temporary response locally
    const temp = { id: `temp-${Date.now()}`, content, date_created: new Date().toISOString(), optimistic: true };
    setReq(r => ({ ...r, responses: [ ...(r.responses || []), temp ] }));

    try {
      const res = await apiFetch(`/responses`, { method: 'POST', body: { content, request_id: requestId }, token });
      // replace temp with real response
      setReq(r => ({ ...r, responses: r.responses.map(x => x.id===temp.id ? res : x) }));
    } catch (err) {
      // rollback: remove temp and show error
      setReq(r => ({ ...r, responses: r.responses.filter(x => x.id !== temp.id) }));
      alert(err.error || 'Failed to add response');
    }
  };

  if (loading) return <div>Loading…</div>;
  if (!req) return <div>Not found</div>;

  return (
    <div>
      <h1>{req.title}</h1>
      <p>{req.description}</p>
      <h3>Responses</h3>
      <ul>
        {(req.responses || []).map(r => <li key={r.id}>{r.content} {r.optimistic ? ' (sending...)' : ''}</li>)}
      </ul>

      <ResponseForm onSubmit={addResponse} />
    </div>
  );
}
