import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { GameProvider } from './context/GameContext';
import { GameLoopProvider } from './context/GameLoopContext';
import { AuthProvider } from './context/AuthContext';
import Lobby from './screens/Lobby';
import ForgotPassword from './components/ForgotPassword';
import ResetPassword from './components/ResetPassword';
import ScenarioView from './screens/ScenarioView';
import DecisionPanel from './screens/DecisionPanel';
import RoundOutcome from './screens/RoundOutcome';
import SessionSummary from './screens/SessionSummary';
import Login from './components/Login';
import Register from './components/Register';
import ProtectedRoute from './components/ProtectedRoute';

const App = () => {
    return (
        <GameLoopProvider>
            <GameProvider>
                <AuthProvider>
                    <Router>
                        <Routes>
                            <Route path="/" element={<Lobby />} />
                            <Route path="/scenario" element={<ScenarioView />} />
                            <Route path="/decision" element={<DecisionPanel />} />
                            <Route path="/outcome" element={<RoundOutcome />} />
                            <Route path="/summary" element={<SessionSummary />} />
                            <Route path="/login" element={<Login />} />
                            <Route path="/forgot-password" element={<ForgotPassword />} />
                            <Route path="/reset-password" element={<ResetPassword />} />
                            <Route path="/register" element={<Register />} />
                            <Route
                                path="/protected"
                                element={
                                    <ProtectedRoute>
                                        <div>Protected Content</div>
                                    </ProtectedRoute>
                                }
                            />
                        </Routes>
                    </Router>
                </AuthProvider>
            </GameProvider>
        </GameLoopProvider>
    );
};

export default App;
