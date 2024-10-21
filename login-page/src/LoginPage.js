// src/LoginPage.js
import React, { useState } from "react";
import "./LoginPage.css";

const LoginPage = ({ onLogin, message, onSignUp }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = () => {
    onLogin(username, password); // Send both credentials to App.js
  };

  return (
    <div className="login-page">
      <div className="wavy-bg"></div>
      <div className="login-box">
        <h1 className="title">HELLO.</h1>

        <div className="dot-group">
          <span className="dot active"></span>
          <span className="dot"></span>
          <span className="dot"></span>
        </div>

        <div className="login-form">
          <h2>Login.</h2>

          {/* Username Input */}
          <div className="input-field">
            <label>Username</label>
            <input
              type="text"
              placeholder="Type here"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>

          {/* Password Input */}
          <div className="input-field">
            <label>Password</label>
            <input
              type="password"
              placeholder="Type here"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <div className="button-group">
            <button className="new-button" onClick={onSignUp}>
              New Here?
            </button>
            <button className="continue-button" onClick={handleSubmit}>
              Log In
            </button>
          </div>
        </div>

        {/* Display Login Message */}
        <p className="login-message">{message}</p>
      </div>
    </div>
  );
};

export default LoginPage;
