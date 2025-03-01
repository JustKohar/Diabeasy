import React, { useState } from 'react';
import axios from 'axios';
import api from '../api.js';

const Dashboard = () => {
  const [timeOfDay, setTimeOfDay] = useState('');
  const [bloodSugar, setBloodSugar] = useState('');
  const [dose, setDose] = useState(null);

  const calculateDose = async () => {
    try {
      const response = await axios.get('/api/insulin/calculate', {
        params: { userId: '123', timeOfDay, bloodSugar },
      });
      setDose(response.data.dose);
    } catch (error) {
      console.error('Calculation failed', error);
    }
  };

  return (
    <div>
      <select value={timeOfDay} onChange={(e) => setTimeOfDay(e.target.value)}>
        <option value="morning">Morning</option>
        <option value="afternoon">Afternoon</option>
        <option value="evening">Evening</option>
      </select>
      <input type="number" placeholder="Blood Sugar" value={bloodSugar} onChange={(e) => setBloodSugar(e.target.value)} />
      <button onClick={calculateDose}>Calculate</button>
      {dose && <p>Insulin Dose: {dose} units</p>}
    </div>
  );
};

export default Dashboard;