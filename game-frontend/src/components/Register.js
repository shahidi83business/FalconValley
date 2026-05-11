import React, { useState, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';

const Register = () => {
  const { handleRegister } = useContext(AuthContext);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [errors, setErrors] = useState({});
  const [successMessage, setSuccessMessage] = useState('');

  const validateForm = () => {
    const newErrors = {};
    
    if (!username || username.length < 3) {
      newErrors.username = 'Username must be at least 3 characters';
    }
    
    if (!email || !/\S+@\S+\.\S+/.test(email)) {
      newErrors.email = 'Please enter a valid email address';
    }
    
    if (!password || password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters';
    }
    
    if (password !== confirmPassword) {
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
    
    try {
      await handleRegister({ username, password, email });
      setSuccessMessage('Registration successful! Redirecting to login...');
      setTimeout(() => {
        window.location.href = '/login';
      }, 2000);
    } catch (error) {
      setErrors({ general: error.userMessage || 'Registration failed. Please try again.' });
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
    maxWidth: '480px',
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
    width: '250px',
    height: '250px',
    borderRadius: '50%',
    background: 'linear-gradient(135deg, #764ba2 0%, #667eea 100%)',
    opacity: '0.1',
    top: '-125px',
    left: '-125px'
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

  const successMessageStyle = {
    backgroundColor: '#00b894',
    color: '#fff',
    padding: '12px',
    borderRadius: '10px',
    marginBottom: '20px',
    textAlign: 'center',
    fontSize: '14px',
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

  const [hoveredButton, setHoveredButton] = useState(null);
  const [focusedInput, setFocusedInput] = useState(null);

  const getPasswordStrength = () => {
    if (!password) return 0;
    let strength = 0;
    if (password.length >= 8) strength++;
    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
    if (/\d/.test(password)) strength++;
    if (/[!@#$%^&*]/.test(password)) strength++;
    return strength;
  };

  const passwordStrength = getPasswordStrength();

  return (
    <div style={containerStyle}>
      <div style={formContainerStyle}>
        <div style={decorativeCircleStyle}></div>
        
        <h2 style={titleStyle}>Create Account</h2>
        <p style={subtitleStyle}>Join us today and start your journey</p>
        
        {successMessage && (
          <div style={successMessageStyle}>
            {successMessage}
          </div>
        )}
        
        {errors.general && (
          <div style={{ ...successMessageStyle, backgroundColor: '#ff4757' }}>
            {errors.general}
          </div>
        )}
        
        <form onSubmit={onSubmit}>
          <div style={inputGroupStyle}>
            <label style={labelStyle}>Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              onFocus={() => setFocusedInput('username')}
              onBlur={() => setFocusedInput(null)}
              style={
                errors.username ? inputErrorStyle :
                focusedInput === 'username' ? inputFocusStyle : inputStyle
              }
              placeholder="Choose a username"
              required
            />
            {errors.username && <div style={errorMessageStyle}>{errors.username}</div>}
          </div>
          
          <div style={inputGroupStyle}>
            <label style={labelStyle}>Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              onFocus={() => setFocusedInput('email')}
              onBlur={() => setFocusedInput(null)}
              style={
                errors.email ? inputErrorStyle :
                focusedInput === 'email' ? inputFocusStyle : inputStyle
              }
              placeholder="Enter your email"
              required
            />
            {errors.email && <div style={errorMessageStyle}>{errors.email}</div>}
          </div>
          
          <div style={inputGroupStyle}>
            <label style={labelStyle}>Password</label>
            <input
              type={showPassword ? "text" : "password"}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              onFocus={() => setFocusedInput('password')}
              onBlur={() => setFocusedInput(null)}
              style={
                errors.password ? {...inputErrorStyle, paddingRight: '45px'} :
                focusedInput === 'password' ? {...inputFocusStyle, paddingRight: '45px'} : passwordInputStyle
              }
              placeholder="Create a password"
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
            
            {password && (
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
            <label style={labelStyle}>Confirm Password</label>
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
              placeholder="Confirm your password"
              required
            />
            {errors.confirmPassword && <div style={errorMessageStyle}>{errors.confirmPassword}</div>}
          </div>
          
          <div style={{ marginBottom: '20px', fontSize: '14px', color: '#666' }}>
            <label style={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}>
              <input
                type="checkbox"
                required
                style={{ marginRight: '8px' }}
              />
              I agree to the <a href="/terms" style={{ ...linkStyle, marginLeft: '5px' }}>Terms of Service</a>
            </label>
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
            {isLoading ? 'Creating Account...' : 'Sign Up'}
          </button>
        </form>

        <div style={{ textAlign: 'center', marginTop: '20px', fontSize: '14px', color: '#666' }}>
          Already have an account? <a href="/login" style={linkStyle}>Sign in</a>
        </div>
      </div>
    </div>
  );
};

export default Register;
