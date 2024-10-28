// src/LoginPage.js
import React from "react";
import "./LoginPage.css"; // Import the corresponding CSS for this component

const LoginPage = ({ onLogin }) => {  // Accept the onLogin function as a prop

  //TODO: use the below hooks to capture username and password data
  const [username, setUsername] = React.useState(''); // Track username input
  const [password, setPassword] = React.useState(''); // Track password input

  const submitCredentials = async (event) => {
    event.preventDefault(); // Prevent the page from refreshing
    
    try {
      const response = await fetch('${process.env.REACT_APP_API_URL}/submit_credentials', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();
      console.log('Response from Flask:', data.message);

    } catch (error) {
      console.error('Error submitting credentials:', error);
    }
  };

  // Tie together sending data and bool to change login state. TEMP/BANDAID for integration purposes
  const handleButtonClick = async (event) => {
    await submitCredentials(event); 
    onLogin();                 
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
            <div className="input-field">
              <label>Username</label>
              <input type="text" placeholder="Type here" value={username} onChange={(e) => setUsername(e.target.value)}/>
            </div>
            <div className="input-field">
              <label>Password</label>
              <input type="password" placeholder="Type here" value={password} onChange={(e) => setPassword(e.target.value)}/>
            </div>
            <div className="button-group">
              <button className="new-button">New Here?</button>
              <button className="continue-button" onClick={handleButtonClick}>Continue</button>
            </div>
          </div>
        </div>
      </div>
    );
  };
  

export default LoginPage;
