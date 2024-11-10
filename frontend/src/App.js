import React, { useState } from "react";
import LoginPage from "./LoginPage";
import ProjectForm from "./ProjectForm";
import CheckInOut from "./CheckInOut";

function App() {
  const [page, setPage] = useState("login");
  const [user, setUser] = useState(""); // Save the logged-in user for the session
  const [authorizedProjects, setAuthorizedProjects] = useState([]);
  
  const handleUser = (username) => {
    setUser(username);
  };

  const handleLogin = async (user) => {
    setUser(user);
    const baseUrl = process.env.REACT_APP_API_URL.replace(/\/+$/, '');
    const response = await fetch(`${baseUrl}/fetch_authorized_projects`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({user}),
    });
    const data = await response.json();
    if (data.status === "success") {
      setAuthorizedProjects(data.authorizedProjects);
      console.log(authorizedProjects);
      console.log(user);
      setPage("projectForm");
    } else {
      alert("Failed to fetch authorized projects");
    }
  };

  const handleNavigation = (destination) => {
    setPage(destination);
  };

  return (
    <div>
      {page === "login" && (
        <LoginPage 
        setUser={handleUser}
        onLogin={handleLogin} 
        setAuthorizedProjects={authorizedProjects}
        />
      )}
      {page === "projectForm" && (
        <ProjectForm 
          onMake={() => handleNavigation("checkInOut")} 
          onJoin={() => handleNavigation("checkInOut")} 
          onLogout={() => handleNavigation("login")}
          username={user}
          setUser={handleUser}
          authorizedProjects={authorizedProjects}
        />
      )}
      {page === "checkInOut" && (
        <CheckInOut 
          username={user}
          onBack={() => handleNavigation("projectForm")} 
        />
      )}
    </div>
  );
}

export default App;