import React, {useState, useEffect} from 'react';
import './ProjectForm.css';

const ProjectForm = ({ onMake, onJoin, onLogout, username, setUser, authorizedProjects = [], setJoinedProject}) => {
  const baseUrl = process.env.REACT_APP_API_URL.replace(/\/+$/, '');
  const [projectid, setProjectid] = useState("");
  const [projectName, setProjectName] = useState("");
  const [projectDescription, setProjectDescription] = useState("");
  const [joinid, setJoinid] = useState("");
  const [selectedProject, setSelectedProject] = useState("");

  useEffect(() => {
    console.log("Authorized Projects Updated:", authorizedProjects);
  }, [authorizedProjects]);

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
        alert(`Project ${projectName} created by ${username} with project ID ${projectid}`);
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
  
  const handleProjectSelect = (event) => {
    const projectID = event.target.value;
    setSelectedProject(projectID);
    setJoinid("");
  }

  const handleInputChange = (e) => {
    setJoinid(e.target.value);
    setSelectedProject(""); // Clear dropdown selection when user types in joinid input
  };

  const resetDropdown = () => {
    setSelectedProject("");
  };

  const handleJoin = async (event) => {

    // Check if neither is filled
    if (!joinid) {
        alert("Please enter a specific ID.");
        return;
    }
    const projectToJoin = joinid; // Use either dropdown selection or input ID
    console.log("Going to project with ID:", projectToJoin);
    
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
          projectid:projectToJoin
        }),
      });

      const data = await response.json();
      console.log("Response from Flask:", data.message);

      if (data.status === "success") {
        alert(`Joining project with project ID ${projectToJoin}`);
        setJoinedProject(projectToJoin);
        onJoin();  // Successfully created project
        resetDropdown();
        setJoinid("");

      } else {
        alert(data.message); // Display error if project creation fails
      }

    }
    catch (error) {
      console.error("Error joining project:", error);
      alert("There was an error. Please try again.");
    }
  };

  const handleGoTo = async (event) => {

    if (!selectedProject) {
        alert("Please select a project from the dropdown menu.");
        return;
    }
    const projectToJoin = selectedProject; // Use either dropdown selection or input ID
    console.log("Going to project with ID:", projectToJoin);
    
    event.preventDefault();
    const endpoint = 'goto_project';

    try {
      const response = await fetch(`${baseUrl}/${endpoint}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username,
          projectid:projectToJoin
        }),
      });

      const data = await response.json();
      console.log("Response from Flask:", data.message);

      if (data.status === "success") {
        alert(`Going to project with project ID ${projectToJoin}`);
        setJoinedProject(projectToJoin);
        onJoin();  // Successfully created project
        resetDropdown();
        setJoinid("");

      } else {
        alert(data.message); // Display error if project creation fails
      }

    }
    catch (error) {
      console.error("Error going to project:", error);
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
        <h2>Create New Project</h2>
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
        <h2>Go To Authorized Project</h2>
        <form className="join-form">
          <div className="dropdown-section">
          <button type="button" className="clear-button" onClick={resetDropdown}>Clear Dropdown</button>
            <div className="dropdown-container">
            <select className="dropdown-menu" 
              value={selectedProject} 
              onChange={handleProjectSelect}
            >
              <option value="" disabled>Select a project</option>
              {authorizedProjects.map((project) => {
              console.log("Project ID:", project.ID);
              console.log("Project Name:", project.Project_Name);
              return (
                <option key={project._id} value={project.ID}>
                  {project.Project_Name}
                </option>
              );
              })}
            </select>

            <button type="button" className="goto-button" onClick={handleGoTo}>Go To Project</button>
            </div>
          </div>
          <h2>Join Project with Specific ID</h2>
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