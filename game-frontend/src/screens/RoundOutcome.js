import React from 'react';
import { useContext } from 'react';
import { GameContext } from '../context/GameContext';
import { useNavigate } from 'react-router-dom';

const RoundOutcome = () => {
    const { state } = useContext(GameContext);
    const navigate = useNavigate();

    const handleNextRound = () => {
        navigate('/next-round');
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

    const outcomeStyle = {
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
            <h1 style={titleStyle}>Round Outcome</h1>
            <p style={outcomeStyle}>Your decision has been processed!</p>
            <button style={buttonStyle} onClick={handleNextRound}>Next Round</button>
        </div>
    );
};

export default RoundOutcome;