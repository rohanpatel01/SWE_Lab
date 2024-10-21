// src/LoginPage.js
import React from "react";
import "./LoginPage.css"; // Import the corresponding CSS for this component

const LoginPage = ({ onLogin }) => {  // Accept the onLogin function as a prop
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
            <div className="input-field">
              <label>Username</label>
              <input type="text" placeholder="Type here" />
            </div>
            <div className="input-field">
              <label>Password</label>
              <input type="password" placeholder="Type here" />
            </div>
            <div className="button-group">
              <button className="new-button">New Here?</button>
              <button className="continue-button" onClick={onLogin}>Continue</button>
            </div>
          </div>
        </div>
      </div>
    );
  };
  

export default LoginPage;
