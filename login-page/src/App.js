import React, { useState } from "react";

import "./LoginPage.css"; // This is where we import the CSS

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault(); // Prevent the page from refreshing

    console.log("Form Submitted");
    console.log("Username:", username);
    console.log("Password:", password);
    
    try {
      // Corrected URL to point to the Flask backend running on port 5000
      const response = await fetch('http://localhost:5000/submit_credentials', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();
      console.log('Response from Flask:', data.message);

      // Clear the fields after successful submission
      setUsername(''); // Clear the username field
      setPassword(''); // Clear the password field

    } catch (error) {
      console.error('Error submitting credentials:', error);
    }
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
          <form onSubmit={handleSubmit}>
            <div className="input-field">
              <label>Username</label>
              <input 
                type="text" 
                value={username} 
                onChange={(e) => setUsername(e.target.value)} 
                placeholder="Type here" 
              />
            </div>
            <div className="input-field">
              <label>Password</label>
              <input 
                type="password" 
                value={password} 
                onChange={(e) => setPassword(e.target.value)} 
                placeholder="Type here" 
              />
            </div>
            <div className="button-group">
              <button type="submit" className="continue-button">Continue</button>
            </div>
          </form>
        </div>
      </div>

    </div>
  );
}

export default App;

