import React, { useState } from "react";
import LoginPage from "./LoginPage";
import ProjectForm from "./ProjectForm";
import CheckInOut from "./CheckInOut";

function App() {
  const [page, setPage] = useState("login");
  const [user, setUser] = useState(""); // Save the logged-in user for the session

  const handleUser = (username) => {
    setUser(username);
  };

  const handleLogin = () => {
    setPage("projectForm");
  };

  const handleNavigation = (destination) => {
    setPage(destination);
  };

  return (
    <div>
      {page === "login" && <LoginPage onLogin={handleLogin} setUser={handleUser}/>}
      {page === "projectForm" && (
        <ProjectForm 
          onMake={() => handleNavigation("checkInOut")} 
          onJoin={() => handleNavigation("checkInOut")} 
          onLogout={() => handleNavigation("login")}
          username={user}
          setUser={handleUser}
        />
      )}
      {page === "checkInOut" && (
        <CheckInOut onBack={() => handleNavigation("projectForm")} />
      )}
    </div>
  );
}

export default App;