import React, { createContext, useReducer, useEffect } from 'react';

const GameLoopContext = createContext();

const initialState = {
    currentPhase: 'lobby', // Possible phases: lobby, scenario, decision, outcome, summary
    scenarioData: null,
    decision: null,
    outcome: null,
    sessionActive: true,
};

const gameLoopReducer = (state, action) => {
    switch (action.type) {
        case 'SET_PHASE':
            return { ...state, currentPhase: action.payload };
        case 'SET_SCENARIO':
            return { ...state, scenarioData: action.payload };
        case 'SET_DECISION':
            return { ...state, decision: action.payload };
        case 'SET_OUTCOME':
            return { ...state, outcome: action.payload };
        case 'END_SESSION':
            return { ...state, sessionActive: false };
        default:
            return state;
    }
};

const GameLoopProvider = ({ children }) => {
    const [state, dispatch] = useReducer(gameLoopReducer, initialState);

    const startGameSession = () => {
        console.log('Starting game session...');
        dispatch({ type: 'SET_PHASE', payload: 'scenario' });
    };

    const initializeScenario = () => {
        console.log('Initializing scenario...');
        const scenario = { text: 'Default Scenario', options: ['Option 1', 'Option 2'] };
        dispatch({ type: 'SET_SCENARIO', payload: scenario });
        dispatch({ type: 'SET_PHASE', payload: 'decision' });
    };

    const makeDecision = (decision) => {
        console.log('Player decision:', decision);
        dispatch({ type: 'SET_DECISION', payload: decision });
        dispatch({ type: 'SET_PHASE', payload: 'outcome' });
    };

    const calculateOutcome = () => {
        console.log('Calculating outcome...');
        const outcome = { result: 'Win', score: 100 };
        dispatch({ type: 'SET_OUTCOME', payload: outcome });
        dispatch({ type: 'SET_PHASE', payload: 'summary' });
    };

    const endSession = () => {
        console.log('Ending session...');
        dispatch({ type: 'END_SESSION' });
    };

    useEffect(() => {
        if (state.currentPhase === 'lobby') {
            startGameSession();
        } else if (state.currentPhase === 'scenario') {
            initializeScenario();
        } else if (state.currentPhase === 'decision') {
            // Wait for player decision
        } else if (state.currentPhase === 'outcome') {
            calculateOutcome();
        } else if (state.currentPhase === 'summary') {
            endSession();
        }
    }, [state.currentPhase]);

    return (
        <GameLoopContext.Provider value={{ state, dispatch, makeDecision }}>
            {children}
        </GameLoopContext.Provider>
    );
};

export { GameLoopContext, GameLoopProvider };