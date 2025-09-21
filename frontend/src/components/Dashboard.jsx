import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

export default function Dashboard() {
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    priority: "Low",
  });
  const [editingId, setEditingId] = useState(null);
  const [message, setMessage] = useState("");
  const [currentUser, setCurrentUser] = useState(null);
  const [responseText, setResponseText] = useState({}); // store responses by request id

  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    navigate("/auth");
  };

  const fetchCurrentUser = async () => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await axios.get("/api/me", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setCurrentUser(response.data);
    } catch (error) {
      console.error("Error fetching current user:", error);
      handleLogout();
    }
  };

  const fetchRequests = async () => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await axios.get("/api/requests", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setRequests(response.data.data);
    } catch (error) {
      console.error("Error fetching requests:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCurrentUser();
    fetchRequests();
  }, []);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem("access_token");
      if (editingId) {
        await axios.put(`/api/requests/${editingId}`, formData, {
          headers: { Authorization: `Bearer ${token}` },
        });
        setMessage("Request updated successfully!");
      } else {
        await axios.post("/api/requests", formData, {
          headers: { Authorization: `Bearer ${token}` },
        });
        setMessage("Request created successfully!");
      }
      setFormData({ title: "", description: "", priority: "Low" });
      setEditingId(null);
      fetchRequests();
    } catch (error) {
      console.error("Error saving request:", error);
      setMessage("Failed to save request.");
    }
  };

  const handleEdit = (req) => {
    setFormData({
      title: req.title,
      description: req.description,
      priority: req.priority,
    });
    setEditingId(req.id);
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this request?")) return;
    try {
      const token = localStorage.getItem("access_token");
      await axios.delete(`/api/requests/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setMessage("Request deleted successfully!");
      fetchRequests();
    } catch (error) {
      console.error("Error deleting request:", error);
      setMessage("Failed to delete request.");
    }
  };

  const handleResponseChange = (id, text) => {
    setResponseText({ ...responseText, [id]: text });
  };

  const handleAddResponse = async (id) => {
    try {
      const token = localStorage.getItem("access_token");
      await axios.post(
        `/api/requests/${id}/responses`,
        { content: responseText[id] },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setMessage("Response added!");
      setResponseText({ ...responseText, [id]: "" });
      fetchRequests(); // refresh requests to get updated responses
    } catch (error) {
      console.error("Error adding response:", error);
      setMessage("Failed to add response.");
    }
  };

  if (loading || !currentUser) {
    return <p>Loading...</p>;
  }

  return (
    <div style={{ maxWidth: "600px", margin: "2rem auto" }}>
      <h2>Dashboard</h2>
      <p>Welcome, {currentUser.username}</p>
      <button onClick={handleLogout} style={{ marginBottom: "1rem" }}>
        Logout
      </button>

      {/* Create/Edit Request Form */}
      <h3>{editingId ? "Edit Request" : "Create a New Request"}</h3>
      <form onSubmit={handleSubmit} style={{ marginBottom: "2rem" }}>
        <div>
          <label>Title</label>
          <input
            name="title"
            value={formData.title}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>Description</label>
          <textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>Priority</label>
          <select
            name="priority"
            value={formData.priority}
            onChange={handleChange}
          >
            <option value="Low">Low</option>
            <option value="Medium">Medium</option>
            <option value="High">High</option>
          </select>
        </div>
        <button type="submit">
          {editingId ? "Update Request" : "Create Request"}
        </button>
        {editingId && (
          <button
            type="button"
            onClick={() => {
              setFormData({ title: "", description: "", priority: "Low" });
              setEditingId(null);
            }}
            style={{ marginLeft: "1rem" }}
          >
            Cancel
          </button>
        )}
      </form>
      {message && <p>{message}</p>}

      {/* Requests & Responses */}
      <h3>All Requests</h3>
      {requests.length === 0 ? (
        <p>No requests found.</p>
      ) : (
        <ul>
          {requests.map((req) => (
            <li key={req.id} style={{ marginBottom: "2rem" }}>
              <strong>{req.title}</strong> — {req.status}
              <p>{req.description}</p>
              <small>Priority: {req.priority}</small>
              <br />
              {req.user_id === currentUser.id && (
                <>
                  <button onClick={() => handleEdit(req)}>Edit</button>
                  <button
                    onClick={() => handleDelete(req.id)}
                    style={{ marginLeft: "0.5rem" }}
                  >
                    Delete
                  </button>
                </>
              )}

              {/* Responses */}
              <div style={{ marginTop: "1rem", paddingLeft: "1rem" }}>
                <h4>Responses</h4>
                {req.responses && req.responses.length > 0 ? (
                  <ul>
                    {req.responses.map((res) => (
                      <li key={res.id}>
                        <strong>{res.user?.username || "Anonymous"}:</strong>{" "}
                        {res.content}
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p>No responses yet.</p>
                )}

                {/* Add Response Form */}
                <textarea
                  placeholder="Write a response..."
                  value={responseText[req.id] || ""}
                  onChange={(e) =>
                    handleResponseChange(req.id, e.target.value)
                  }
                  style={{ width: "100%", marginTop: "0.5rem" }}
                />
                <button
                  onClick={() => handleAddResponse(req.id)}
                  style={{ marginTop: "0.5rem" }}
                >
                  Add Response
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
