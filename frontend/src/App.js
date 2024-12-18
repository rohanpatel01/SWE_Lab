import React, { useState } from "react";
import LoginPage from "./LoginPage";
import ProjectForm from "./ProjectForm";
import CheckInOut from "./CheckInOut";

function App() {
  const [page, setPage] = useState("login");
  const [user, setUser] = useState(""); // Save the logged-in user for the session
  const [projectid, setProjectID] = useState(-1);
  const [authorizedProjects, setAuthorizedProjects] = useState([]);
  
  const handleUser = (username) => {
    setUser(username);
  };

  const handleProjectid = (projectid) => {
    setProjectID(projectid)
  }

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
          setJoinedProject={handleProjectid}
        />
      )}
      {page === "checkInOut" && (
        <CheckInOut 
          username={user}
          onBack={() => {
            setAuthorizedProjects(authorizedProjects)
            handleLogin(user)
            // handleUser()
            handleNavigation("projectForm")} 
          }
            projectId={projectid}
        />
      )}
    </div>
  );
}

export default App;