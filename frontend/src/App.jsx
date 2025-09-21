import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import AuthForm from "./components/AuthForm";
import Dashboard from "./components/Dashboard";

function App() {
  // helper: check if user is logged in
  const isAuthenticated = () => {
    return !!localStorage.getItem("access_token");
  };

  return (
    <Router>
      <Routes>
        {/* Login/Signup */}
        <Route path="/auth" element={<AuthForm />} />

        {/* Protected Dashboard */}
        <Route
          path="/dashboard"
          element={
            isAuthenticated() ? <Dashboard /> : <Navigate to="/auth" />
          }
        />

        {/* Default route → go to login/signup */}
        <Route path="*" element={<Navigate to="/auth" />} />
      </Routes>
    </Router>
  );
}

export default App;
