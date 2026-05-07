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

    return (
        <div className="decision-panel">
            <h1>Decision Panel</h1>
            <ChoiceButton label="Choice A" onClick={() => handleDecision('A')} />
            <ChoiceButton label="Choice B" onClick={() => handleDecision('B')} />
            <ChoiceButton label="Choice C" onClick={() => handleDecision('C')} />
        </div>
    );
};

export default DecisionPanel;