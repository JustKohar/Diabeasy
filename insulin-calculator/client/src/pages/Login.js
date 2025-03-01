// src/pages/Login.js
import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom'; // <-- Change this

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate(); // <-- Replace useHistory()

  const handleLogin = async () => {
    try {
      const response = await axios.post('/api/auth/login', { email, password });
      if (response.status === 200) {
        navigate('/dashboard'); // <-- Use navigate() instead of history.push()
      }
    } catch (error) {
      console.error('Login failed', error);
    }
  };

  return (
    <div>
      {/* ... rest of your JSX ... */}
    </div>
  );
};

export default Login;