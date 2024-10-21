// src/SignUpPage.js
import React, { useState } from "react";
import "./SignUpPage.css";

const SignUpPage = ({ onSignUp, message, onLoginRedirect }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const sendInfo = () => {
    onSignUp(username, password); 
  };

  return (
    <div className="signup-page">
      <div className="wavy-bg"></div>
      <div className="signup-box">
        <h1 className="title">WELCOME</h1>

        <div className="dot-group">
          <span className="dot active"></span>
          <span className="dot"></span>
          <span className="dot"></span>
        </div>

        <div className="signup-form">
          <h2>SIGN UP.</h2>

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
            <button className="back-button" onClick={onLoginRedirect}>
              Have Account?
            </button>
            <button className="signup-button" onClick={sendInfo}>
              Sign Up
            </button>
          </div>
        </div>

        <p className="signup-message">{message}</p>
      </div>
    </div>
  );
};

export default SignUpPage;
