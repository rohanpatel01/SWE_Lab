import React, { useState } from "react";
import LoginPage from "./LoginPage";
import CheckInOut from "./CheckInOut";
import SignUpPage from "./SignUpPage";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [message, setMessage] = useState("");
  const [isSignUp, setIsSignUp] = useState(false);

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
        setIsLoggedIn(true);
      } else {
        setMessage(data.message);
      }
    } catch (error) {
      setMessage("An error occurred. Please try again.");
    }
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setMessage(""); // Clear message on logout
  };

  const handleSignUp = async (username, password) => {
    try {
      const response = await fetch("http://127.0.0.1:5000/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
      });
      const data = await response.json();
      if (response.ok) {
        setMessage("Sign up successful. Please log in.");
        setIsSignUp(false);
      } else {
        setMessage(data.message);
      }
    } catch (error) {
      setMessage("An error occurred during sign up. Please try again.");
    }
  };

  const switchToSignUp = () => {
    setIsSignUp(true);
    setMessage(""); // Clear message when switching to sign up
  };

  const switchToLogin = () => {
    setIsSignUp(false);
    setMessage(""); // Clear message when switching to login
  };

  return (
    <div>
      {isLoggedIn ? (
        <CheckInOut onLogout={handleLogout} />
      ) : isSignUp ? (
        <SignUpPage onSignUp={handleSignUp} onBackToLogin={switchToLogin} message={message} />
      ) : (
        <LoginPage onLogin={handleLogin} message={message} onSignUp={switchToSignUp} />
      )}
    </div>
  );
}

export default App;