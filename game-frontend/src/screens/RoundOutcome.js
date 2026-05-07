import React, { useContext } from 'react';
import { GameContext } from '../context/GameContext';

const RoundOutcome = () => {
    const { state } = useContext(GameContext);

    return (
        <div className="round-outcome">
            <h1>Round Outcome</h1>
            {state.roundState ? (
                <div>
                    <p>Outcome: {state.roundState.outcome}</p>
                    <p>Score: {state.roundState.score}</p>
                </div>
            ) : (
                <p>No outcome available yet.</p>
            )}
        </div>
    );
};

export default RoundOutcome;