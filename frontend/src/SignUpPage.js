import React, { useState } from "react";
import "./SignUpPage.css";

const SignUpPage = ({ onSignUp, onBackToLogin, message }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    onSignUp(username, password);
  };

  return (
    <div className="signup-page">
      <div className="signup-box">
        <h2 className="title">Sign Up</h2>
        <form onSubmit={handleSubmit}>
          <div className="input-field">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Choose a username"
              required
            />
          </div>
          <div className="input-field">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Choose a password"
              required
            />
          </div>
          <div className="button-group">
            <button type="button" className="back-button" onClick={onBackToLogin}>Back</button>
            <button type="submit" className="signup-button">Sign Up</button>
          </div>
        </form>
        {message && <p className="message">{message}</p>}
      </div>
      <div className="wavy-bg"></div>
    </div>
  );
};

export default SignUpPage;