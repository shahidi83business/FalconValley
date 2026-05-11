import React, { useState, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const { handleLogin } = useContext(AuthContext);
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const onSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      await handleLogin({ username, password });
      navigate('/', { replace: true });
    } catch (error) {
      console.error('Login failed:', error);
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
    top: '-100px',
    right: '-100px'
  };

  const titleStyle = {
    fontSize: '32px',
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

  const forgotPasswordStyle = {
    textAlign: 'center',
    marginTop: '20px',
    fontSize: '14px',
    color: '#666',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
  };

  const linkStyle = {
    color: '#667eea',
    textDecoration: 'none',
    fontWeight: '600',
    transition: 'color 0.3s ease'
  };

  const dividerStyle = {
    display: 'flex',
    alignItems: 'center',
    margin: '25px 0',
    color: '#999',
    fontSize: '14px',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
  };

  const dividerLineStyle = {
    flex: 1,
    height: '1px',
    backgroundColor: '#e1e8ed'
  };

  const dividerTextStyle = {
    padding: '0 15px',
    color: '#999'
  };

  const socialButtonStyle = {
    width: '100%',
    padding: '12px',
    fontSize: '14px',
    fontWeight: '600',
    color: '#333',
    backgroundColor: '#fff',
    border: '2px solid #e1e8ed',
    borderRadius: '10px',
    cursor: 'pointer',
    transition: 'all 0.3s ease',
    marginBottom: '10px',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center'
  };

  const [hoveredButton, setHoveredButton] = useState(null);
  const [focusedInput, setFocusedInput] = useState(null);

  return (
    <div style={containerStyle}>
      <div style={formContainerStyle}>
        <div style={decorativeCircleStyle}></div>
        
        <h2 style={titleStyle}>Welcome Back</h2>
        <p style={subtitleStyle}>Please enter your credentials to continue</p>
        
        <form onSubmit={onSubmit}>
          <div style={inputGroupStyle}>
            <label style={labelStyle}>Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              onFocus={() => setFocusedInput('username')}
              onBlur={() => setFocusedInput(null)}
              style={focusedInput === 'username' ? inputFocusStyle : inputStyle}
              placeholder="Enter your username"
              required
            />
          </div>
          
          <div style={inputGroupStyle}>
            <label style={labelStyle}>Password</label>
            <input
              type={showPassword ? "text" : "password"}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              onFocus={() => setFocusedInput('password')}
              onBlur={() => setFocusedInput(null)}
              style={focusedInput === 'password' ? {...inputFocusStyle, paddingRight: '45px'} : passwordInputStyle}
              placeholder="Enter your password"
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
            {isLoading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        <div style={forgotPasswordStyle}>
          <a href="/forgot-password" style={linkStyle}>Forgot your password?</a>
        </div>

        <div style={dividerStyle}>
          <div style={dividerLineStyle}></div>
          <span style={dividerTextStyle}>OR</span>
          <div style={dividerLineStyle}></div>
        </div>

        <button 
          style={{
            ...socialButtonStyle,
            backgroundColor: hoveredButton === 'google' ? '#f8f9fa' : '#fff'
          }}
          onMouseEnter={() => setHoveredButton('google')}
          onMouseLeave={() => setHoveredButton(null)}
        >
          <span style={{ marginRight: '8px' }}>🔍</span>
          Continue with Google
        </button>

        <button 
          style={{
            ...socialButtonStyle,
            backgroundColor: hoveredButton === 'github' ? '#f8f9fa' : '#fff'
          }}
          onMouseEnter={() => setHoveredButton('github')}
          onMouseLeave={() => setHoveredButton(null)}
        >
          <span style={{ marginRight: '8px' }}>💻</span>
          Continue with GitHub
        </button>

        <div style={{ textAlign: 'center', marginTop: '20px', fontSize: '14px', color: '#666' }}>
          Don't have an account? <a href="/register" style={linkStyle}>Sign up</a>
        </div>
      </div>
    </div>
  );
};

export default Login;
