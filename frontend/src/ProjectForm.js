import React from 'react';
import './ProjectForm.css';

const ProjectForm = ({ onMake, onJoin, onLogout }) => {
  return (
    <div className="project-page">
      <div className="project-box">
        <h1 className="title">Projects</h1>
        <h2>Create</h2>
        <form className="create-form">
          <div className="input-field">
            <label htmlFor="id">ID</label>
            <input type="text" id="id" placeholder="Enter ID" />
          </div>
          <div className="input-field">
            <label htmlFor="name">Name</label>
            <input type="text" id="name" placeholder="Enter Name" />
          </div>
          <div className="input-field">
            <label htmlFor="description">Description</label>
            <textarea id="description" placeholder="Enter Description"></textarea>
          </div>
          <button type="button" className="action-button" onClick={onMake}>Make</button>
        </form>
        <h2>Join</h2>
        <form className="join-form">
          <select className="dropdown-menu">
            <option>Select Project</option>
            {/* Add options dynamically here */}
          </select>
          <input type="text" placeholder="Enter ID here" />
          <button type="button" className="action-button" onClick={onJoin}>Join</button>
          <button type="button" className="logout-button" onClick={onLogout}>Logout</button>
        </form>
      </div>
    </div>
  );
};

export default ProjectForm;