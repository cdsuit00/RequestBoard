import { useState } from 'react';
export default function ResponseForm({ onSubmit }) {
  const [content, setContent] = useState('');
  const [sending, setSending] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    if (!content.trim()) return;
    setSending(true);
    await onSubmit(content);
    setContent('');
    setSending(false);
  };

  return (
    <form onSubmit={submit}>
      <textarea value={content} onChange={e=>setContent(e.target.value)} />
      <button disabled={sending}>Add response</button>
    </form>
  );
}
