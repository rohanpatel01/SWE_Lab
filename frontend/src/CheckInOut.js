// src/CheckInOut.js
import React, { useState } from 'react';
import './CheckInOut.css'; 


const CheckInOut = ({ onLogout, username, password }) => {
  const [hwSet1, setHwSet1] = useState({ capacity: '', available: '', request: '' });
  const [hwSet2, setHwSet2] = useState({ capacity: '', available: '', request: '' });

const [defaultProjectID, setDefaultProjectID] = useState(1);

const connectToClient = () => {
  console.log("attempt connection to mongoDB client")
}

const handleCheckOut = async () => {
  // connectToClient()
  console.log("Amoutn to check in: " + hwSet1.request)

  const baseUrl = process.env.REACT_APP_API_URL.replace(/\/+$/, '');

  // Make query to python flask back end and console.log the availability we have for a given hardware set
  try {
    const response = await fetch(`${baseUrl}/CheckOut`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify({
        projectID: defaultProjectID,
        HW_Set_1_Request: hwSet1.request,
        HW_Set_2_Request: hwSet2.request
      }),
    });


    const data = await response.json();
    if (response.ok) {
      console.log("Printing Data: " + data)
    } else {
      console.log("Error: Bad JSON response");
    }


  } catch (error) {
    console.log("Error")
    // setMessage("An error occurred. Please try again.");
  }
};

const handleCheckIn = async () => {

  const baseUrl = process.env.REACT_APP_API_URL.replace(/\/+$/, '');
  
  try {
    const response = await fetch(`${baseUrl}/CheckIn`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify({
        projectID: defaultProjectID,
        HW_Set_1_Request: hwSet1.request,
        HW_Set_2_Request: hwSet2.request
      }),
    });


    const data = await response.json();
    if (response.ok) {
      console.log("Printing Data: " + data)
    } else {
      console.log("Error: Bad JSON response");
    }


  } catch (error) {
    console.log("Error: " + error)
    // setMessage("An error occurred. Please try again.");
  }
};

  return (
    <div className="check-in-out-container">
      <h1>{username}</h1>
      <h1>Check Out/In</h1>
      <div className="hardware-set">
        <div className="row">
          <div>HW Set 1</div>
          <input
            type="text"
            placeholder="Capacity"
            value={hwSet1.capacity}
            onChange={(e) => setHwSet1({ ...hwSet1, capacity: e.target.value })}
          />
          <input
            type="text"
            placeholder="Available"
            value={hwSet1.available}
            onChange={(e) => setHwSet1({ ...hwSet1, available: e.target.value })}
          />
          <input
            type="text"
            placeholder="Request"
            value={hwSet1.request}
            onChange={(e) => setHwSet1({ ...hwSet1, request: e.target.value })}
          />
        </div>
        <div className="row">
          <div>HW Set 2</div>
          <input
            type="text"
            placeholder="Capacity"
            value={hwSet2.capacity}
            onChange={(e) => setHwSet2({ ...hwSet2, capacity: e.target.value })}
          />
          <input
            type="text"
            placeholder="Available"
            value={hwSet2.available}
            onChange={(e) => setHwSet2({ ...hwSet2, available: e.target.value })}
          />
          <input
            type="text"
            placeholder="Request"
            value={hwSet2.request}
            onChange={(e) => setHwSet2({ ...hwSet2, request: e.target.value })}
          />
        </div>
      </div>
      <div className="button-group">
        <button onClick={handleCheckIn}>Check In</button>
        <button onClick={handleCheckOut}>Check Out</button>
        <button className="logout-button" onClick={onLogout}>Log Out</button>
      </div>
    </div>
  );
};

export default CheckInOut;
