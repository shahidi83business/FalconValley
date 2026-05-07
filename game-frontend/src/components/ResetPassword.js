import React, { useState } from 'react';
import { resetPassword } from '../api/authApi';
import { useSearchParams } from 'react-router-dom';

const ResetPassword = () => {
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token');
  const [newPassword, setNewPassword] = useState('');
  const [message, setMessage] = useState('');

  const onSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await resetPassword(token, newPassword);
      setMessage(response.message);
    } catch (error) {
      setMessage('Failed to reset password.');
    }
  };

  return (
    <div>
      <h2>Reset Password</h2>
      <form onSubmit={onSubmit}>
        <div>
          <label>New Password:</label>
          <input
            type="password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
          />
        </div>
        <button type="submit">Reset Password</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default ResetPassword;