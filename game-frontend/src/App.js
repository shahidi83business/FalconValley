import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { GameProvider } from './context/GameContext';
import Lobby from './screens/Lobby';
import ScenarioView from './screens/ScenarioView';
import DecisionPanel from './screens/DecisionPanel';
import RoundOutcome from './screens/RoundOutcome';
import SessionSummary from './screens/SessionSummary';

const App = () => {
    return (
        <GameProvider>
            <Router>
                <Routes>
                    <Route path="/" element={<Lobby />} />
                    <Route path="/scenario" element={<ScenarioView />} />
                    <Route path="/decision" element={<DecisionPanel />} />
                    <Route path="/outcome" element={<RoundOutcome />} />
                    <Route path="/summary" element={<SessionSummary />} />
                </Routes>
            </Router>
        </GameProvider>
    );
};

export default App;
