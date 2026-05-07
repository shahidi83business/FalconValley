import React, { useContext } from 'react';
import { GameContext } from '../context/GameContext';

const SessionSummary = () => {
    const { state } = useContext(GameContext);

    return (
        <div className="session-summary">
            <h1>Session Summary</h1>
            {state.playerHistory.length > 0 ? (
                <ul>
                    {state.playerHistory.map((entry, index) => (
                        <li key={index}>{entry}</li>
                    ))}
                </ul>
            ) : (
                <p>No session history available.</p>
            )}
        </div>
    );
};

export default SessionSummary;