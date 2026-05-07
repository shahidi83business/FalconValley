import React, { createContext, useReducer } from 'react';

const GameContext = createContext();

const initialState = {
    sessionState: null,
    roundState: null,
    playerHistory: [],
    trustIndicators: {},
};

const gameReducer = (state, action) => {
    switch (action.type) {
        case 'SET_SESSION_STATE':
            return { ...state, sessionState: action.payload };
        case 'SET_ROUND_STATE':
            return { ...state, roundState: action.payload };
        case 'ADD_PLAYER_HISTORY':
            return { ...state, playerHistory: [...state.playerHistory, action.payload] };
        case 'SET_TRUST_INDICATORS':
            return { ...state, trustIndicators: action.payload };
        default:
            return state;
    }
};

const GameProvider = ({ children }) => {
    const [state, dispatch] = useReducer(gameReducer, initialState);

    return (
        <GameContext.Provider value={{ state, dispatch }}>
            {children}
        </GameContext.Provider>
    );
};

export { GameContext, GameProvider };