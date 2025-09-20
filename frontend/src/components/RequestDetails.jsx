import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

const RequestDetail = () => {
  const { id } = useParams();
  const [request, setRequest] = useState(null);
  const [responses, setResponses] = useState([]);
  const [newResponse, setNewResponse] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchRequest();
  }, [id]);

  const fetchRequest = async () => {
    try {
      const response = await axios.get(`http://localhost:5000/api/requests/${id}`);
      setRequest(response.data);
      setResponses(response.data.responses || []);
    } catch (error) {
      console.error('Error fetching request:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddResponse = async (e) => {
    e.preventDefault();
    if (!newResponse.trim()) return;

    try {
      await axios.post(`http://localhost:5000/api/requests/${id}/responses`, {
        content: newResponse
      });
      
      setNewResponse('');
      fetchRequest(); // Refresh to get new response
    } catch (error) {
      console.error('Error adding response:', error);
    }
  };

  const updateStatus = async (newStatus) => {
    try {
      await axios.patch(`http://localhost:5000/api/requests/${id}`, {
        status: newStatus
      });
      
      setRequest(prev => ({ ...prev, status: newStatus }));
    } catch (error) {
      console.error('Error updating status:', error);
    }
  };

  if (loading) return <div className="loading">Loading...</div>;
  if (!request) return <div>Request not found</div>;

  return (
    <div className="request-detail">
      <div className="request-header">
        <h1>{request.title}</h1>
        <div className="request-meta">
          <span className={`priority ${request.priority}`}>
            {request.priority.toUpperCase()}
          </span>
          <select
            value={request.status}
            onChange={(e) => updateStatus(e.target.value)}
            className="status-select"
          >
            <option value="open">Open</option>
            <option value="in_progress">In Progress</option>
            <option value="completed">Completed</option>
            <option value="cancelled">Cancelled</option>
          </select>
        </div>
      </div>

      <div className="request-content">
        <p>{request.description}</p>
        <small>Created: {new Date(request.date_created).toLocaleDateString()}</small>
      </div>

      <div className="responses-section">
        <h3>Responses ({responses.length})</h3>
        
        <form onSubmit={handleAddResponse} className="add-response">
          <textarea
            value={newResponse}
            onChange={(e) => setNewResponse(e.target.value)}
            placeholder="Add a response..."
            rows="3"
          />
          <button type="submit" disabled={!newResponse.trim()}>
            Add Response
          </button>
        </form>

        <div className="responses-list">
          {responses.map(response => (
            <div key={response.id} className="response-item">
              <p>{response.content}</p>
              <small>{new Date(response.date_created).toLocaleString()}</small>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default RequestDetail;