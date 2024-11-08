import React, {useState} from 'react';
import './ProjectForm.css';

const ProjectForm = ({ onMake, onJoin, onLogout, username, setUser}) => {
  const baseUrl = process.env.REACT_APP_API_URL.replace(/\/+$/, '');
  const [projectid, setProjectid] = useState("");
  const [projectName, setProjectName] = useState("");
  const [projectDescription, setProjectDescription] = useState("");
  const [joinid, setJoinid] = useState("");

  const handleMake = async (event) => {
    event.preventDefault();
    const endpoint = 'create_project';

    try {
      const response = await fetch(`${baseUrl}/${endpoint}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          projectid,
          projectName,
          projectDescription,
          username
        }),
      });

      const data = await response.json();
      console.log("Response from Flask:", data.message);

      if (data.status === "success") {
        alert(`Project ${projectName} created with project ID ${projectid}`);
        onMake();  // Successfully created project
      } else {
        alert(data.message); // Display error if project creation fails
      }

    }
    catch (error) {
      console.error("Error making project:", error);
      alert("There was an error. Please try again.");
    }

  };

  const handleJoin = async (event) => {
    event.preventDefault();
    const endpoint = 'join_project';

    try {
      const response = await fetch(`${baseUrl}/${endpoint}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username,
          joinid
        }),
      });

      const data = await response.json();
      console.log("Response from Flask:", data.message);

      if (data.status === "success") {
        alert(`Joined project with project ID ${joinid}`);
        onJoin();  // Successfully created project
      } else {
        alert(data.message); // Display error if project creation fails
      }

    }
    catch (error) {
      console.error("Error joining project:", error);
      alert("There was an error. Please try again.");
    }
  };

  const handleLogout = async (event) => {
    event.preventDefault();
    setUser(""); // Clear the logged-in user
    onLogout();
  };


  
  return (
    <div className="project-page">
      <div className="project-box">
        <h1 className="title">Projects</h1>
        <h2>Create</h2>
        <form className="create-form">
          <div className="input-field">
            <label htmlFor="id">ID</label>
            <input
              type="text"
              id="id"
              placeholder="Enter ID"
              onChange={(e) => setProjectid(e.target.value)}
            />
          </div>
          <div className="input-field">
            <label htmlFor="name">Name</label>
            <input
              type="text"
              id="name"
              placeholder="Enter Name"
              onChange={(e) => setProjectName(e.target.value)}
            />
          </div>
          <div className="input-field">
            <label htmlFor="description">Description</label>
            <textarea
              id="description"
              placeholder="Enter Description"
              onChange={(e) => setProjectDescription(e.target.value)}
            ></textarea>
          </div>
          <button type="button" className="action-button" onClick={handleMake}>Make</button>
        </form>
        <h2>Join</h2>
        <form className="join-form">
          <select className="dropdown-menu">
            <option>Select Project</option>
            {/* Add options dynamically here */}
          </select>
          <input
            type="text"
            placeholder="Enter ID here"
            value={joinid}
            onChange={(e) => setJoinid(e.target.value)}
          />
          <button type="button" className="action-button" onClick={handleJoin}>Join</button>
          <button type="button" className="logout-button" onClick={handleLogout}>Logout</button>
        </form>
      </div>
    </div>
  );
};

export default ProjectForm;