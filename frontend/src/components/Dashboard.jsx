import { useState, useEffect } from 'react';
import axios from 'axios';
import RequestCard from './RequestCard';
import { Link } from 'react-router-dom';

const Dashboard = () => {
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    fetchRequests();
  }, [currentPage]);

  const fetchRequests = async () => {
    try {
      setLoading(true);
      const response = await axios.get(
        `http://localhost:5000/api/requests?page=${currentPage}&per_page=10`
      );
      
      setRequests(response.data.requests);
      setTotalPages(response.data.pages);
    } catch (error) {
      console.error('Error fetching requests:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (requestId) => {
    if (window.confirm('Are you sure you want to delete this request?')) {
      try {
        await axios.delete(`http://localhost:5000/api/requests/${requestId}`);
        fetchRequests(); // Refresh the list
      } catch (error) {
        console.error('Error deleting request:', error);
      }
    }
  };

  if (loading) return <div className="loading">Loading...</div>;

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>My Requests</h1>
        <Link to="/requests/new" className="btn btn-primary">
          Create New Request
        </Link>
      </div>

      <div className="requests-grid">
        {requests.map(request => (
          <RequestCard
            key={request.id}
            request={request}
            onDelete={handleDelete}
          />
        ))}
      </div>

      {totalPages > 1 && (
        <div className="pagination">
          <button
            onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
            disabled={currentPage === 1}
          >
            Previous
          </button>
          <span>Page {currentPage} of {totalPages}</span>
          <button
            onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
            disabled={currentPage === totalPages}
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
};

export default Dashboard;