import React from 'react';
import { useContext } from 'react';
import { GameContext } from '../context/GameContext';
import { useNavigate } from 'react-router-dom';

const SessionSummary = () => {
    const { state } = useContext(GameContext);
    const navigate = useNavigate();

    const handleRestart = () => {
        navigate('/lobby');
    };

    const containerStyle = {
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        padding: '20px'
    };

    const titleStyle = {
        fontSize: '36px',
        fontWeight: 'bold',
        color: '#ffffff',
        marginBottom: '20px',
        textAlign: 'center',
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    };

    const summaryStyle = {
        fontSize: '24px',
        color: '#ffffff',
        marginBottom: '30px',
        textAlign: 'center',
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    };

    const buttonStyle = {
        padding: '12px 20px',
        backgroundColor: '#ffffff',
        color: '#667eea',
        border: 'none',
        borderRadius: '10px',
        cursor: 'pointer',
        transition: 'all 0.3s ease',
        fontSize: '16px',
        fontWeight: '600',
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    };

    const buttonHoverStyle = {
        ...buttonStyle,
        backgroundColor: '#667eea',
        color: '#ffffff'
    };

    return (
        <div style={containerStyle}>
            <h1 style={titleStyle}>Session Summary</h1>
            <p style={summaryStyle}>Your session has ended. Here are your results:</p>
            <p style={summaryStyle}>Score: {state.score}</p>
            <p style={summaryStyle}>Total Decisions: {state.totalDecisions}</p>
            <button style={buttonStyle} onClick={handleRestart}>Restart Game</button>
        </div>
    );
};

export default SessionSummary;