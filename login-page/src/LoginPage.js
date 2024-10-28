// src/LoginPage.js
import React, { useState } from "react";
import "./LoginPage.css";

const LoginPage = ({ onLogin, message, onSignUp }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    onLogin(username, password);
  };

  return (
    <div className="login-page">
      <div className="login-box">
        <h2 className="title">Login</h2>
        <form onSubmit={handleSubmit}>
          <div className="input-field">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter your username"
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
              placeholder="Enter your password"
              required
            />
          </div>
          <div className="button-group">
            <button type="button" className="action-button" onClick={onSignUp}>Sign Up</button>
            <button type="submit" className="action-button">Login</button>
          </div>
        </form>
        {message && <p className="message">{message}</p>}
      </div>
      <div className="wavy-bg"></div>
    </div>
  );
};

export default LoginPage;