import React, { useContext, useEffect, useState } from 'react';
import { GameContext } from '../context/GameContext';
import ChoiceButton from '../components/ChoiceButton';
import { submitDecision } from '../api/scenarioApi';

const DecisionPanel = () => {
    const { state, dispatch } = useContext(GameContext);
    const [timeLeft, setTimeLeft] = useState(30); // default 30 seconds

    const scenario = state?.roundState?.scenario;
    const opponents = state?.roundState?.opponents || [];
    const user = state?.roundState?.user;
    const decisionTimeLimit = state?.roundState?.decision_time_limit || 30;

    useEffect(() => {
        setTimeLeft(decisionTimeLimit);
    }, [decisionTimeLimit, scenario?.id]);

    useEffect(() => {
        if (timeLeft <= 0) return;

        const timer = setInterval(() => {
            setTimeLeft((prev) => prev - 1);
        }, 1000);

        return () => clearInterval(timer);
    }, [timeLeft]);

    useEffect(() => {
        if (timeLeft === 0) {
            handleDecision('NO_RESPONSE');
        }
    }, [timeLeft]);

    const handleDecision = async (choice) => {
        try {
            const result = await submitDecision({ choice });
            dispatch({ type: 'SET_ROUND_STATE', payload: result });
        } catch (error) {
            console.error('Failed to submit decision:', error);
        }
    };

    const formatTime = (seconds) => {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    };

    return (
        <div style={containerStyle}>
            <h1 style={titleStyle}>Decision Panel</h1>

            {/* Timer */}
            <div style={timerStyle}>
                ⏳ Time Left: {formatTime(timeLeft)}
            </div>

            {/* User Status */}
            {user && (
                <div style={userStatusStyle}>
                    <h2>Your Status</h2>
                    <div style={statsGridStyle}>
                        <div style={statCardStyle}>
                            <span style={statLabelStyle}>Wealth</span>
                            <span style={statValueStyle}>{user.wealth}</span>
                        </div>
                        <div style={statCardStyle}>
                            <span style={statLabelStyle}>Trust</span>
                            <span style={statValueStyle}>{user.trust}</span>
                        </div>
                        <div style={statCardStyle}>
                            <span style={statLabelStyle}>Reputation</span>
                            <span style={statValueStyle}>{user.reputation}</span>
                        </div>
                        <div style={statCardStyle}>
                            <span style={statLabelStyle}>Risk</span>
                            <span style={statValueStyle}>{user.risk_level}</span>
                        </div>
                    </div>
                </div>
            )}

            {/* Scenario */}
            {scenario && (
                <div style={scenarioStyle}>
                    <h2>Scenario</h2>
                    <p>{scenario.description}</p>
                </div>
            )}

            {/* Opponents */}
            {opponents.length > 0 && (
                <div style={opponentSectionStyle}>
                    <h2>Opponents</h2>
                    <div style={opponentContainerStyle}>
                        {opponents.map((opponent) => (
                            <div key={opponent.id} style={opponentCardStyle}>
                                <strong>{opponent.name}</strong>
                                <p>Strategy: {opponent.strategy}</p>
                                <p>Wealth: {opponent.wealth}</p>
                                <p>Trust: {opponent.trust}</p>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Decision Buttons */}
            <p style={{ color: '#ffffff', marginBottom: '20px' }}>
                Choose your action:
            </p>

            <div style={buttonContainerStyle}>
                <ChoiceButton
                    label="Choice A"
                    onClick={() => handleDecision('A')}
                    disabled={timeLeft <= 0}
                />
                <ChoiceButton
                    label="Choice B"
                    onClick={() => handleDecision('B')}
                    disabled={timeLeft <= 0}
                />
                <ChoiceButton
                    label="Choice C"
                    onClick={() => handleDecision('C')}
                    disabled={timeLeft <= 0}
                />
            </div>
        </div>
    );
};

/* styles */

const containerStyle = {
    minHeight: '100vh',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    padding: '20px',
    color: '#fff'
};

const titleStyle = {
    fontSize: '36px',
    fontWeight: 'bold',
    marginBottom: '20px',
    textAlign: 'center'
};

const timerStyle = {
    fontSize: '24px',
    fontWeight: 'bold',
    background: 'rgba(255,255,255,0.15)',
    padding: '12px 24px',
    borderRadius: '12px',
    marginBottom: '20px'
};

const userStatusStyle = {
    width: '100%',
    maxWidth: '800px',
    background: 'rgba(255,255,255,0.1)',
    padding: '20px',
    borderRadius: '12px',
    marginBottom: '25px'
};

const statsGridStyle = {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))',
    gap: '15px',
    marginTop: '15px'
};

const statCardStyle = {
    background: 'rgba(255,255,255,0.12)',
    padding: '15px',
    borderRadius: '10px',
    textAlign: 'center'
};

const statLabelStyle = {
    display: 'block',
    fontSize: '14px',
    opacity: 0.8,
    marginBottom: '8px'
};

const statValueStyle = {
    fontSize: '22px',
    fontWeight: 'bold'
};

const scenarioStyle = {
    width: '100%',
    maxWidth: '800px',
    background: 'rgba(255,255,255,0.1)',
    padding: '20px',
    borderRadius: '12px',
    marginBottom: '25px'
};

const opponentSectionStyle = {
    width: '100%',
    maxWidth: '800px',
    marginBottom: '30px'
};

const opponentContainerStyle = {
    display: 'flex',
    gap: '15px',
    flexWrap: 'wrap',
    justifyContent: 'center'
};

const opponentCardStyle = {
    background: 'rgba(255,255,255,0.12)',
    padding: '15px',
    borderRadius: '10px',
    minWidth: '180px'
};

const buttonContainerStyle = {
    display: 'flex',
    flexDirection: 'column',
    gap: '15px',
    width: '100%',
    maxWidth: '400px'
};

export default DecisionPanel;
