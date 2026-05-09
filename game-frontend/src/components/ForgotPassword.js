import React, { useState } from 'react';
import { forgotPassword } from '../api/authApi';

const ForgotPassword = () => {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [focusedInput, setFocusedInput] = useState(null);
  const [hoveredButton, setHoveredButton] = useState(null);

  const onSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setMessage('');
    
    try {
      const response = await forgotPassword(email);
      setMessage(response.message || 'Password reset link has been sent to your email!');
      setIsSuccess(true);
    } catch (error) {
      setMessage('Failed to send password reset link. Please check your email and try again.');
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
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    opacity: '0.1',
    bottom: '-100px',
    left: '-100px'
  };

  const decorativeCircle2Style = {
    position: 'absolute',
    width: '150px',
    height: '150px',
    borderRadius: '50%',
    background: 'linear-gradient(135deg, #764ba2 0%, #667eea 100%)',
    opacity: '0.08',
    top: '-75px',
    right: '-75px'
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

  const inputFocusStyle = {
    ...inputStyle,
    borderColor: '#667eea',
    boxShadow: '0 0 0 3px rgba(102, 126, 234, 0.1)'
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

  const backButtonStyle = {
    width: '100%',
    padding: '12px',
    fontSize: '14px',
    fontWeight: '600',
    color: '#667eea',
    backgroundColor: '#fff',
    border: '2px solid #667eea',
    borderRadius: '10px',
    cursor: 'pointer',
    transition: 'all 0.3s ease',
    marginTop: '15px',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
  };

  const backButtonHoverStyle = {
    ...backButtonStyle,
    backgroundColor: '#f8f9ff',
    transform: 'translateY(-2px)',
    boxShadow: '0 5px 15px rgba(102, 126, 234, 0.2)'
  };

  const messageStyle = {
    padding: '12px',
    borderRadius: '10px',
    marginTop: '20px',
    textAlign: 'center',
    fontSize: '14px',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
    animation: 'slideIn 0.3s ease'
  };

  const successMessageStyle = {
    ...messageStyle,
    backgroundColor: '#d4edda',
    color: '#155724',
    border: '1px solid #c3e6cb'
  };

  const errorMessageStyle = {
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

  const illustrationStyle = {
    textAlign: 'center',
    marginBottom: '20px'
  };

  return (
    <div style={containerStyle}>
      <div style={formContainerStyle}>
        <div style={decorativeCircleStyle}></div>
        <div style={decorativeCircle2Style}></div>
        
        <div style={illustrationStyle}>
          <div style={iconStyle}>🔐</div>
        </div>
        
        <h2 style={titleStyle}>Forgot Password?</h2>
        <p style={subtitleStyle}>
          No worries! Enter your email address below and we'll send you a link to reset your password.
        </p>
        
        {!isSuccess ? (
          <form onSubmit={onSubmit}>
            <div style={inputGroupStyle}>
              <label style={labelStyle}>Email Address</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                onFocus={() => setFocusedInput('email')}
                onBlur={() => setFocusedInput(null)}
                style={focusedInput === 'email' ? inputFocusStyle : inputStyle}
                placeholder="Enter your registered email"
                required
              />
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
              {isLoading ? 'Sending...' : 'Send Reset Link'}
            </button>
            
            <button
              type="button"
              onClick={() => window.location.href = '/login'}
              style={hoveredButton === 'back' ? backButtonHoverStyle : backButtonStyle}
              onMouseEnter={() => setHoveredButton('back')}
              onMouseLeave={() => setHoveredButton(null)}
            >
              Back to Login
            </button>
          </form>
        ) : (
          <div>
            <div style={successMessageStyle}>
              <div style={{ fontSize: '24px', marginBottom: '10px' }}>✅</div>
              <strong>Check your email!</strong>
              <p style={{ marginTop: '10px', marginBottom: '0' }}>
                We've sent a password reset link to {email}
              </p>
            </div>
            
            <button
              type="button"
              onClick={() => window.location.href = '/login'}
              style={
                hoveredButton === 'login' ? buttonHoverStyle : buttonStyle
              }
              onMouseEnter={() => setHoveredButton('login')}
              onMouseLeave={() => setHoveredButton(null)}
            >
              Return to Login
            </button>
            
            <div style={{ textAlign: 'center', marginTop: '20px', fontSize: '14px', color: '#666' }}>
              Didn't receive the email? Check your spam folder or{' '}
              <a 
                href="#" 
                onClick={(e) => {
                  e.preventDefault();
                  setIsSuccess(false);
                  setMessage('');
                }}
                style={linkStyle}
              >
                try again
              </a>
            </div>
          </div>
        )}
        
        {message && !isSuccess && (
          <div style={errorMessageStyle}>
            {message}
          </div>
        )}
        
        <div style={{ textAlign: 'center', marginTop: '30px', fontSize: '13px', color: '#999' }}>
          Remember your password?{' '}
          <a href="/login" style={linkStyle}>Sign in</a>
        </div>
      </div>
      
      <style>{`
        @keyframes slideIn {
          from {
            opacity: 0;
            transform: translateY(-10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
      `}</style>
    </div>
  );
};

export default ForgotPassword;