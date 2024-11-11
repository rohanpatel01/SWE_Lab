import React, { useState } from "react";
import "./LoginPage.css";

const LoginPage = ({ onLogin, setUser }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isSignUp, setIsSignUp] = useState(false);
  const [authorizedProjects, setAuthorizedProjects] = useState([]);

  const submitCredentials = async (event) => {
    event.preventDefault();

    const endpoint = isSignUp ? "sign_up" : "sign_in";
    const baseUrl = process.env.REACT_APP_API_URL.replace(/\/+$/, '');

    try {
      const response = await fetch(`${baseUrl}/${endpoint}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();
      console.log("Response from Flask:", data.message);

      if (data.status === "success") {
        if (isSignUp) {
          alert("Sign-up successful! You can now log in.");
          setIsSignUp(false);  // Switch back to login mode
        } else {
          setUsername(username);  // Save the logged-in user for the session
          setUser(username)
          // setAuthorizedProjects(data.authorizedProjects);
          onLogin(username);
        }
      } else {
        alert(data.message);  // Display error if sign-in/sign-up fails
      }
      
    } catch (error) {
      console.error("Error submitting credentials:", error);
      alert("There was an error. Please try again.");

    }
  };

  return (
    
    <div className="login-page">
      <div className="wavy-bg"></div>
      <div className="login-box">
        <h1 className="title">{isSignUp ? "Sign Up" : "Login"}</h1>
        
        <div className="login-form">
          <div className="input-field">
            <label>Username</label>
            <input
              type="text"
              placeholder="Type here"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>
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
            <button
              className="action-button"
              onClick={() => setIsSignUp((prev) => !prev)}
            >
              {isSignUp ? "Already have an account?" : "New Here?"}
            </button>
            <button className="action-button" onClick={submitCredentials}>
              Continue
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
