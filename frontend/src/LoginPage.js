// src/LoginPage.js
import React, { useState } from "react";
import ProjectForm from "./ProjectForm";
import "./LoginPage.css";

const LoginPage = ({ onLogin, setUser}) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isSignUp, setIsSignUp] = useState(false);
  const [authorizedProjects, setProjects] = useState([]);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

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
          setUser(username);  // Save the logged-in user for the session
          setIsLoggedIn(true)
          // onLogin();  // Change app state to logged in
          // Fetch authorized projects after login
          const endPoint1 = 'fetch_authorized_projects';
          const projectsResponse = await fetch(`${baseUrl}/${endPoint1}`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ username }),
          });
          const projectsData = await projectsResponse.json();

          if (projectsData.status === "success") {
              console.log(authorizedProjects)
              setProjects(projectsData.authorizedProjects);  // Save authorized projects
          } else {
              console.error("Error fetching authorized projects:", projectsData.message);
              alert("Error fetching authorized projects.");
          }
        }
      } else {
        alert(data.message);  // Display error if sign-in/sign-up fails
      }
      
      // Clear the input fields
      // setUsername("");
      // setPassword("");
      
    } catch (error) {
      console.error("Error submitting credentials:", error);
      alert("There was an error. Please try again.");
      
      // Clear the input fields
      // setUsername("");
      // setPassword("");
    }
  };

  if (isLoggedIn) {
    // Render ProjectForm with authorizedProjects as a prop
    return (
      <ProjectForm
        onMake={() => console.log("Project Created")}
        onJoin={() => console.log("Project Joined")}
        onLogout={() => {
          setIsLoggedIn(false);
          setUsername("");
          setPassword("");
        }}
        username={username}
        setUser={setUser}
        authorizedProjects={authorizedProjects}
      />
    );
  }

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
