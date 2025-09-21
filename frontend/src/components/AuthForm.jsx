import { useState } from "react";
import { signupUser, loginUser } from "../api";
import { useNavigate } from "react-router-dom";

export default function AuthForm() {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: ""
  });
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (isLogin) {
        // login
        const response = await loginUser({
          username: formData.username,
          password: formData.password
        });
        localStorage.setItem("access_token", response.data.access_token);
        setMessage("Login successful!");
        navigate("/dashboard"); // 🚀 redirect after login
      } else {
        // signup
        await signupUser(formData);
        setMessage("Signup successful! Please log in.");
        setIsLogin(true);
        setFormData({ username: "", email: "", password: "" }); // reset form
      }
    } catch (error) {
      setMessage(error.response?.data?.error || "Something went wrong");
    }
  };

  return (
    <div style={{ maxWidth: "400px", margin: "2rem auto" }}>
      <h2>{isLogin ? "Login" : "Signup"}</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Username</label>
          <input
            name="username"
            value={formData.username}
            onChange={handleChange}
            required
          />
        </div>
        {!isLogin && (
          <div>
            <label>Email</label>
            <input
              name="email"
              type="email"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </div>
        )}
        <div>
          <label>Password</label>
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>
        <button type="submit">
          {isLogin ? "Login" : "Signup"}
        </button>
      </form>
      <p
        style={{ marginTop: "1rem", cursor: "pointer", color: "blue" }}
        onClick={() => setIsLogin(!isLogin)}
      >
        {isLogin
          ? "Don't have an account? Signup"
          : "Already have an account? Login"}
      </p>
      {message && <p>{message}</p>}
    </div>
  );
}
