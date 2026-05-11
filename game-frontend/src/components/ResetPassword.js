import React, { useState } from 'react';
import { resetPassword } from '../api/authApi';
import { useSearchParams } from 'react-router-dom';

const ResetPassword = () => {
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [errors, setErrors] = useState({});
  const [focusedInput, setFocusedInput] = useState(null);
  const [hoveredButton, setHoveredButton] = useState(null);

  const validateForm = () => {
    const newErrors = {};
    
    if (!newPassword || newPassword.length < 6) {
      newErrors.password = 'Password must be at least 6 characters';
    }
    
    if (newPassword !== confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }
    
    return newErrors;
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    
    const newErrors = validateForm();
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }
    
    setErrors({});
    setIsLoading(true);
    setMessage('');
    
    try {
      const response = await resetPassword(token, newPassword);
      setMessage(response.message || 'Password has been reset successfully!');
      setIsSuccess(true);
    } catch (error) {
      setMessage(error.userMessage || 'Failed to reset password. The link may have expired.');
      setIsSuccess(false);
    } finally {
      setIsLoading(false);
    }
  };

  const containerStyle = {
    minHeight: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    padding: '20px'
  };

  const formContainerStyle = {
    maxWidth: '420px',
    width: '100%',
    backgroundColor: '#ffffff',
    borderRadius: '20px',
    boxShadow: '0 20px 60px rgba(0, 0, 0, 0.3)',
    padding: '40px',
    position: 'relative',
    overflow: 'hidden'
  };

  const decorativeCircleStyle = {
    position: 'absolute',
    width: '200px',
    height: '200px',
    borderRadius: '50%',
    background: 'linear-gradient(135deg, #764ba2 0%, #667eea 100%)',
    opacity: '0.1',
    top: '-100px',
    right: '-100px'
  };

  const iconStyle = {
    fontSize: '48px',
    textAlign: 'center',
    marginBottom: '20px'
  };

  const titleStyle = {
    fontSize: '28px',
    fontWeight: 'bold',
    color: '#333',
    marginBottom: '10px',
    textAlign: 'center',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
  };

  const subtitleStyle = {
    fontSize: '14px',
    color: '#666',
    marginBottom: '30px',
    textAlign: 'center',
    lineHeight: '1.5',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
  };

  const inputGroupStyle = {
    marginBottom: '20px',
    position: 'relative'
  };

  const labelStyle = {
    display: 'block',
    fontSize: '14px',
    fontWeight: '600',
    color: '#555',
    marginBottom: '8px',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
  };

  const inputStyle = {
    width: '100%',
    padding: '12px 15px',
    fontSize: '16px',
    border: '2px solid #e1e8ed',
    borderRadius: '10px',
    outline: 'none',
    transition: 'all 0.3s ease',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
    boxSizing: 'border-box'
  };

  const inputErrorStyle = {
    ...inputStyle,
    borderColor: '#ff4757'
  };

  const inputFocusStyle = {
    ...inputStyle,
    borderColor: '#667eea',
    boxShadow: '0 0 0 3px rgba(102, 126, 234, 0.1)'
  };

  const passwordInputStyle = {
    ...inputStyle,
    paddingRight: '45px'
  };

  const eyeButtonStyle = {
    position: 'absolute',
    right: '15px',
    top: '38px',
    background: 'none',
    border: 'none',
    cursor: 'pointer',
    padding: '5px',
    color: '#666',
    fontSize: '18px'
  };

  const errorMessageStyle = {
    color: '#ff4757',
    fontSize: '12px',
    marginTop: '5px',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
  };

  const buttonStyle = {
    width: '100%',
    padding: '14px',
    fontSize: '16px',
    fontWeight: '600',
    color: '#ffffff',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    border: 'none',
    borderRadius: '10px',
    cursor: 'pointer',
    transition: 'all 0.3s ease',
    marginTop: '10px',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
    position: 'relative',
    overflow: 'hidden'
  };

  const buttonHoverStyle = {
    ...buttonStyle,
    transform: 'translateY(-2px)',
    boxShadow: '0 10px 20px rgba(102, 126, 234, 0.3)'
  };

  const buttonDisabledStyle = {
    ...buttonStyle,
    opacity: '0.7',
    cursor: 'not-allowed'
  };

  const messageStyle = {
    padding: '12px',
    borderRadius: '10px',
    marginBottom: '20px',
    textAlign: 'center',
    fontSize: '14px',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
  };

  const successMessageStyle = {
    ...messageStyle,
    backgroundColor: '#d4edda',
    color: '#155724',
    border: '1px solid #c3e6cb'
  };

  errorMessageStyle = {
    ...messageStyle,
    backgroundColor: '#f8d7da',
    color: '#721c24',
    border: '1px solid #f5c6cb'
  };

  const linkStyle = {
    color: '#667eea',
    textDecoration: 'none',
    fontWeight: '600',
    transition: 'color 0.3s ease'
  };

  const progressBarStyle = {
    display: 'flex',
    justifyContent: 'space-between',
    marginBottom: '30px'
  };

  const progressStepStyle = {
    flex: 1,
    height: '4px',
    backgroundColor: '#e1e8ed',
    marginRight: '5px',
    borderRadius: '2px',
    transition: 'background-color 0.3s ease'
  };

  const progressStepActiveStyle = {
    ...progressStepStyle,
    backgroundColor: '#667eea'
  };

  const getPasswordStrength = () => {
    if (!newPassword) return 0;
    let strength = 0;
    if (newPassword.length >= 8) strength++;
    if (/[a-z]/.test(newPassword) && /[A-Z]/.test(newPassword)) strength++;
    if (/\d/.test(newPassword)) strength++;
    if (/[!@#$%^&*]/.test(newPassword)) strength++;
    return strength;
  };

  const passwordStrength = getPasswordStrength();

  if (!token) {
    return (
      <div style={containerStyle}>
        <div style={formContainerStyle}>
          <div style={decorativeCircleStyle}></div>
          
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '48px', marginBottom: '20px' }}>⚠️</div>
            <h2 style={titleStyle}>Invalid Reset Link</h2>
            <p style={subtitleStyle}>
              The password reset link is invalid or has expired. Please request a new one.
            </p>
            
            <button
              onClick={() => window.location.href = '/forgot-password'}
              style={
                hoveredButton === 'forgot' ? buttonHoverStyle : buttonStyle
              }
              onMouseEnter={() => setHoveredButton('forgot')}
              onMouseLeave={() => setHoveredButton(null)}
            >
              Request New Link
            </button>
            
            <div style={{ textAlign: 'center', marginTop: '20px', fontSize: '14px', color: '#666' }}>
              Remember your password? <a href="/login" style={linkStyle}>Sign in</a>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div style={containerStyle}>
      <div style={formContainerStyle}>
        <div style={decorativeCircleStyle}></div>
        
        <div style={{ textAlign: 'center' }}>
          <div style={iconStyle}>🔑</div>
        </div>
        
        <h2 style={titleStyle}>Reset Your Password</h2>
        <p style={subtitleStyle}>
          Enter your new password below. Make sure it's strong and secure!
        </p>
        
        {message && (
          <div style={isSuccess ? successMessageStyle : errorMessageStyle}>
            {message}
          </div>
        )}
        
        {!isSuccess ? (
          <form onSubmit={onSubmit}>
            <div style={inputGroupStyle}>
              <label style={labelStyle}>New Password</label>
              <input
                type={showPassword ? "text" : "password"}
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                onFocus={() => setFocusedInput('password')}
                onBlur={() => setFocusedInput(null)}
                style={
                  errors.password ? {...inputErrorStyle, paddingRight: '45px'} :
                  focusedInput === 'password' ? {...inputFocusStyle, paddingRight: '45px'} : passwordInputStyle
                }
                placeholder="Enter new password"
                required
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                style={eyeButtonStyle}
                aria-label="Toggle password visibility"
              >
                {showPassword ? '👁️' : '👁️‍🗨️'}
              </button>
              {errors.password && <div style={errorMessageStyle}>{errors.password}</div>}
              
              {newPassword && (
                <div style={{ marginTop: '10px' }}>
                  <div style={{ fontSize: '12px', color: '#666', marginBottom: '5px' }}>
                    Password strength
                  </div>
                  <div style={progressBarStyle}>
                    {[1, 2, 3, 4].map((step) => (
                      <div
                        key={step}
                        style={step <= passwordStrength ? progressStepActiveStyle : progressStepStyle}
                      />
                    ))}
                  </div>
                </div>
              )}
            </div>
            
            <div style={inputGroupStyle}>
              <label style={labelStyle}>Confirm New Password</label>
              <input
                type={showPassword ? "text" : "password"}
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                onFocus={() => setFocusedInput('confirmPassword')}
                onBlur={() => setFocusedInput(null)}
                style={
                  errors.confirmPassword ? inputErrorStyle :
                  focusedInput === 'confirmPassword' ? inputFocusStyle : inputStyle
                }
                placeholder="Confirm new password"
                required
              />
              {errors.confirmPassword && <div style={errorMessageStyle}>{errors.confirmPassword}</div>}
            </div>
            
            <button 
              type="submit"
              disabled={isLoading}
              style={
                isLoading ? buttonDisabledStyle : 
                hoveredButton === 'submit' ? buttonHoverStyle : buttonStyle
              }
              onMouseEnter={() => setHoveredButton('submit')}
              onMouseLeave={() => setHoveredButton(null)}
            >
              {isLoading ? 'Resetting...' : 'Reset Password'}
            </button>
          </form>
        ) : (
          <div>
            <div style={{ textAlign: 'center', marginBottom: '20px' }}>
              <div style={{ fontSize: '48px', marginBottom: '10px' }}>✅</div>
              <p style={{ color: '#155724', fontWeight: '600' }}>
                Your password has been reset successfully!
              </p>
            </div>
            
            <button
              onClick={() => window.location.href = '/login'}
              style={
                hoveredButton === 'login' ? buttonHoverStyle : buttonStyle
              }
              onMouseEnter={() => setHoveredButton('login')}
              onMouseLeave={() => setHoveredButton(null)}
            >
              Go to Login
            </button>
          </div>
        )}
        
        <div style={{ textAlign: 'center', marginTop: '30px', fontSize: '13px', color: '#999' }}>
          Need help? <a href="/support" style={linkStyle}>Contact Support</a>
        </div>
      </div>
    </div>
  );
};

export default ResetPassword;
