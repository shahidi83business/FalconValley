import React, { useContext, useEffect, useState } from 'react';
import { GameContext } from '../context/GameContext';
import { fetchScenarios } from '../api/scenarioApi';

const ScenarioView = () => {
    const { state, dispatch } = useContext(GameContext);
    const [scenarios, setScenarios] = useState([]);

    useEffect(() => {
        const loadScenarios = async () => {
            try {
                const data = await fetchScenarios();
                setScenarios(data);
            } catch (error) {
                console.error('Failed to load scenarios:', error);
            }
        };

        loadScenarios();
    }, []);

    return (
        <div className="scenario-view">
            <h1>Scenario View</h1>
            <ul>
                {scenarios.map((scenario) => (
                    <li key={scenario.id}>{scenario.title}</li>
                ))}
            </ul>
        </div>
    );
};

export default ScenarioView;