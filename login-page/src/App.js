import React from "react";
import "./LoginPage.css"; // This is where we import the CSS

const LoginPage = () => {
  return (
    <div className="login-page">
      {/* Wavy background */}
      <div className="wavy-bg"></div>

      <div className="login-box">
        <h1 className="title">HELLO.</h1>
        
        {/* Dots like in the image */}
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
            <button className="continue-button">Continue</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
