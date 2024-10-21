// src/App.js
import React, { useState } from "react";
import LoginPage from "./LoginPage";
import CheckInOut from "./CheckInOut";
import SignUpPage from "./SignUpPage";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [message, setMessage] = useState("");
  const [isSignUp, setIsSignUp] = useState(false); // Track if on Sign Up page

  const handleLogin = async (username, password) => {
    try {
      const response = await fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      if (response.ok) {
        setIsLoggedIn(true); // Successful login
      } else {
        setMessage(data.message); 
      }
    } catch (error) {
      setMessage("An error occurred. Please try again.");
    }
  };

  const handleLogout = () => {
    setIsLoggedIn(false); // Logout user
  };

  const handleSignUp = (username, password) => {
    console.log("Sign Up:", username, password);
    setIsSignUp(false); 
  };

  return (
    <div>
      {isLoggedIn ? (
        <CheckInOut onLogout={handleLogout} />
      ) : isSignUp ? (
        <SignUpPage onSignUp={handleSignUp} message={message} onLoginRedirect={() => setIsSignUp(false)} />
      ) : (
        <LoginPage
          onLogin={handleLogin}
          message={message}
          onSignUp={() => setIsSignUp(true)} 
        />
      )}
    </div>
  );
}

export default App;
