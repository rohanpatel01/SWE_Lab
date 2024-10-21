import React, { useState } from "react";
import LoginPage from "./LoginPage"; // Import the LoginPage component
import CheckInOut from "./CheckInOut"; // Import the CheckInOut component

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false); // Track login status

  const handleLogin = () => {
    setIsLoggedIn(true);  
  };


  const handleLogout = () => {
    setIsLoggedIn(false); 
  };

  return (
    <div>
      {isLoggedIn ? (
        <CheckInOut onLogout={handleLogout} /> 
      ) : (
        <LoginPage onLogin={handleLogin} />  
      )}
    </div>
  );
}

export default App;

