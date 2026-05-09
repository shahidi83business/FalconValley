import React, { useContext } from 'react';
import { GameContext } from '../context/GameContext';
import ChoiceButton from '../components/ChoiceButton';
import { submitDecision } from '../api/scenarioApi';

const DecisionPanel = () => {
    const { state, dispatch } = useContext(GameContext);

    const handleDecision = async (choice) => {
        try {
            const result = await submitDecision({ choice });
            dispatch({ type: 'SET_ROUND_STATE', payload: result });
        } catch (error) {
            console.error('Failed to submit decision:', error);
        }
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

    const buttonContainerStyle = {
        display: 'flex',
        flexDirection: 'column',
        gap: '15px',
        width: '100%',
        maxWidth: '400px',
        margin: '0 auto'
    };

    return (
        <div style={containerStyle}>
            <h1 style={titleStyle}>Decision Panel</h1>
            <p style={{ color: '#ffffff', marginBottom: '30px' }}>Choose your action:</p>
            <div style={buttonContainerStyle}>
                <ChoiceButton label="Choice A" onClick={() => handleDecision('A')} />
                <ChoiceButton label="Choice B" onClick={() => handleDecision('B')} />
                <ChoiceButton label="Choice C" onClick={() => handleDecision('C')} />
            </div>
        </div>
    );
};

export default DecisionPanel;