// src/CheckInOut.js
import React, { useState } from 'react';
import './CheckInOut.css'; 

const CheckInOut = ({ onLogout, username, password }) => {
  const [hwSet1, setHwSet1] = useState({ capacity: '', available: '', request: '' });
  const [hwSet2, setHwSet2] = useState({ capacity: '', available: '', request: '' });

  const handleCheckIn = () => {
    console.log('Checked In:', hwSet1, hwSet2, 'User:', username, 'Password:', password);
    // Handle check-in logic here when it's added
  };

  const handleCheckOut = () => {
    console.log('Checked Out:', hwSet1, hwSet2, 'User:', username, 'Password:', password);
    // Handle check-out logic here when it's added
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
