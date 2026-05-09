import React, { useContext, useEffect, useState } from 'react';
import { GameContext } from '../context/GameContext';
import { fetchScenarios } from '../api/scenarioApi';
import { useNavigate } from 'react-router-dom';

const ScenarioView = () => {
    const { state, dispatch } = useContext(GameContext);
    const [scenarios, setScenarios] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedScenario, setSelectedScenario] = useState(null);
    const [hoveredCard, setHoveredCard] = useState(null);
    const [filter, setFilter] = useState('all');
    const navigate = useNavigate();

    useEffect(() => {
        const loadScenarios = async () => {
            try {
                setLoading(true);
                const data = await fetchScenarios();
                setScenarios(data);
            } catch (error) {
                console.error('Failed to load scenarios:', error);
            } finally {
                setLoading(false);
            }
        };

        loadScenarios();
    }, []);

    const handleSelectScenario = (scenario) => {
        setSelectedScenario(scenario);
        dispatch({ type: 'SET_SCENARIO', payload: scenario });
        
        // Navigate to decision panel after selection
        setTimeout(() => {
            navigate('/decision');
        }, 500);
    };

    const containerStyle = {
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        padding: '20px',
        position: 'relative'
    };

    const backgroundPatternStyle = {
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        opacity: 0.05,
        backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.4'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
        pointerEvents: 'none'
    };

    const headerStyle = {
        textAlign: 'center',
        marginBottom: '40px',
        animation: 'fadeInDown 0.8s ease'
    };

    const titleStyle = {
        fontSize: '42px',
        fontWeight: 'bold',
        color: '#ffffff',
        marginBottom: '10px',
        textShadow: '2px 2px 4px rgba(0, 0, 0, 0.2)',
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    };

    const subtitleStyle = {
        fontSize: '18px',
        color: 'rgba(255, 255, 255, 0.9)',
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    };

    const filterContainerStyle = {
        display: 'flex',
        justifyContent: 'center',
        gap: '10px',
        marginBottom: '30px',
        animation: 'fadeIn 0.8s ease 0.2s both'
    };

    const filterButtonStyle = {
        padding: '10px 20px',
        backgroundColor: 'rgba(255, 255, 255, 0.2)',
        color: '#ffffff',
        border: 'none',
        borderRadius: '25px',
        cursor: 'pointer',
        fontSize: '14px',
        fontWeight: '600',
        transition: 'all 0.3s ease',
        backdropFilter: 'blur(10px)',
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    };

    const filterButtonActiveStyle = {
        ...filterButtonStyle,
        backgroundColor: '#ffffff',
        color: '#667eea',
        transform: 'scale(1.05)'
    };

    const scenariosGridStyle = {
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))',
        gap: '25px',
        maxWidth: '1200px',
        margin: '0 auto',
        animation: 'fadeInUp 0.8s ease 0.3s both'
    };

    const scenarioCardStyle = {
        backgroundColor: '#ffffff',
        borderRadius: '15px',
        overflow: 'hidden',
        boxShadow: '0 10px 30px rgba(0, 0, 0, 0.2)',
        transition: 'all 0.3s ease',
        cursor: 'pointer',
        position: 'relative'
    };

    const scenarioCardHoverStyle = {
        ...scenarioCardStyle,
        transform: 'translateY(-5px) scale(1.02)',
        boxShadow: '0 15px 40px rgba(0, 0, 0, 0.3)'
    };

    const scenarioCardSelectedStyle = {
        ...scenarioCardStyle,
        transform: 'scale(0.98)',
        boxShadow: '0 5px 20px rgba(102, 126, 234, 0.5)',
        border: '3px solid #667eea'
    };

    const scenarioImageStyle = {
        width: '100%',
        height: '200px',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontSize: '64px',
        position: 'relative',
        overflow: 'hidden'
    };

    const scenarioContentStyle = {
        padding: '20px'
    };

    const scenarioTitleStyle = {
        fontSize: '20px',
        fontWeight: 'bold',
        color: '#333',
        marginBottom: '10px',
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    };

    const scenarioDescriptionStyle = {
        fontSize: '14px',
        color: '#666',
        lineHeight: '1.6',
        marginBottom: '15px',
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    };

    const scenarioMetaStyle = {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        paddingTop: '15px',
        borderTop: '1px solid #e1e8ed'
    };

    const difficultyBadgeStyle = {
        padding: '5px 12px',
        borderRadius: '20px',
        fontSize: '12px',
        fontWeight: '600',
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    };

    const playButtonStyle = {
        padding: '8px 16px',
        backgroundColor: '#667eea',
        color: '#ffffff',
        border: 'none',
        borderRadius: '8px',
        fontSize: '14px',
        fontWeight: '600',
        cursor: 'pointer',
        transition: 'all 0.3s ease',
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    };

    const playButtonHoverStyle = {
        ...playButtonStyle,
        backgroundColor: '#764ba2',
        transform: 'translateY(-2px)',
        boxShadow: '0 5px 15px rgba(102, 126, 234, 0.3)'
    };

    const loadingStyle = {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '400px'
    };

    const spinnerStyle = {
        width: '60px',
        height: '60px',
        border: '4px solid rgba(255, 255, 255, 0.3)',
        borderTop: '4px solid #ffffff',
        borderRadius: '50%',
        animation: 'spin 1s linear infinite'
    };

    const emptyStateStyle = {
        textAlign: 'center',
        padding: '60px 20px',
        color: '#ffffff'
    };

    const getDifficultyColor = (difficulty) => {
        switch (difficulty?.toLowerCase()) {
            case 'easy': return '#00b894';
            case 'medium': return '#fdcb6e';
            case 'hard': return '#e17055';
            case 'expert': return '#d63031';
            default: return '#74b9ff';
        }
    };

    const getScenarioIcon = (type) => {
        switch (type?.toLowerCase()) {
            case 'adventure': return '🗺️';
            case 'puzzle': return '🧩';
            case 'strategy': return '♟️';
            case 'action': return '⚔️';
            case 'mystery': return '🔍';
            default: return '🎮';
        }
    };

    // Mock data for scenarios if none are loaded
    const mockScenarios = scenarios.length > 0 ? scenarios : [
        { id: 1, title: 'The Lost Temple', description: 'Explore ancient ruins and uncover hidden treasures in this thrilling adventure.', difficulty: 'Easy', type: 'adventure', duration: '15 min' },
        { id: 2, title: 'Corporate Espionage', description: 'Navigate the world of corporate intrigue and make decisions that will shape your company\'s future.', difficulty: 'Medium', type: 'strategy', duration: '30 min' },
        { id: 3, title: 'Survival Island', description: 'Stranded on a deserted island, make critical choices to survive and find your way home.', difficulty: 'Hard', type: 'action', duration: '45 min' },
        { id: 4, title: 'The Time Paradox', description: 'Your decisions ripple through time. Choose wisely to prevent a catastrophic future.', difficulty: 'Expert', type: 'puzzle', duration: '60 min' },
        { id: 5, title: 'Murder Mystery Manor', description: 'A classic whodunit scenario where every choice brings you closer to solving the crime.', difficulty: 'Medium', type: 'mystery', duration: '25 min' },
        { id: 6, title: 'Space Colony Crisis', description: 'Lead humanity\'s first Mars colony through critical decisions that will determine its survival.', difficulty: 'Hard', type: 'strategy', duration: '40 min' }
    ];

    const filteredScenarios = filter === 'all' 
        ? mockScenarios 
        : mockScenarios.filter(s => s.difficulty?.toLowerCase() === filter);

    return (
        <div style={containerStyle}>
            <div style={backgroundPatternStyle}></div>
            
            <div style={headerStyle}>
                <h1 style={titleStyle}>🎯 Choose Your Scenario</h1>
                <p style={subtitleStyle}>Select a scenario to begin your adventure</p>
            </div>

            <div style={filterContainerStyle}>
                {['all', 'easy', 'medium', 'hard', 'expert'].map((level) => (
                    <button
                        key={level}
                        style={filter === level ? filterButtonActiveStyle : filterButtonStyle}
                        onClick={() => setFilter(level)}
                    >
                        {level.charAt(0).toUpperCase() + level.slice(1)}
                    </button>
                ))}
            </div>

            {loading ? (
                <div style={loadingStyle}>
                    <div style={spinnerStyle}></div>
                    <p style={{ color: '#ffffff', marginTop: '20px', fontSize: '18px' }}>Loading scenarios...</p>
                </div>
            ) : filteredScenarios.length === 0 ? (
                <div style={emptyStateStyle}>
                    <div style={{ fontSize: '64px', marginBottom: '20px' }}>📭</div>
                    <h2 style={{ fontSize: '24px', marginBottom: '10px' }}>No Scenarios Found</h2>
                    <p style={{ fontSize: '16px', opacity: 0.9 }}>Try adjusting your filters or check back later for new content!</p>
                </div>
            ) : (
                <div style={scenariosGridStyle}>
                    {filteredScenarios.map((scenario) => (
                        <div
                            key={scenario.id}
                            style={
                                selectedScenario?.id === scenario.id ? scenarioCardSelectedStyle :
                                hoveredCard === scenario.id ? scenarioCardHoverStyle : scenarioCardStyle
                            }
                            onMouseEnter={() => setHoveredCard(scenario.id)}
                            onMouseLeave={() => setHoveredCard(null)}
                            onClick={() => handleSelectScenario(scenario)}
                        >
                            <div style={scenarioImageStyle}>
                                <span style={{ fontSize: '72px', filter: 'drop-shadow(2px 2px 4px rgba(0,0,0,0.3))' }}>
                                    {getScenarioIcon(scenario.type)}
                                </span>
                                <div style={{
                                    position: 'absolute',
                                    top: 0,
                                    left: 0,
                                    right: 0,
                                    bottom: 0,
                                    background: 'radial-gradient(circle at center, transparent 0%, rgba(0,0,0,0.3) 100%)'
                                }}></div>
                            </div>
                            
                            <div style={scenarioContentStyle}>
                                <h3 style={scenarioTitleStyle}>{scenario.title}</h3>
                                <p style={scenarioDescriptionStyle}>{scenario.description}</p>
                                
                                <div style={scenarioMetaStyle}>
                                    <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
                                        <span style={{
                                            ...difficultyBadgeStyle,
                                            backgroundColor: getDifficultyColor(scenario.difficulty),
                                            color: '#ffffff'
                                        }}>
                                            {scenario.difficulty}
                                        </span>
                                        {scenario.duration && (
                                            <span style={{ fontSize: '12px', color: '#999' }}>
                                                ⏱️ {scenario.duration}
                                            </span>
                                        )}
                                    </div>
                                    <button
                                        style={hoveredCard === scenario.id ? playButtonHoverStyle : playButtonStyle}
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            handleSelectScenario(scenario);
                                        }}
                                    >
                                        Play →
                                    </button>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            <style>{`
                @keyframes fadeInDown {
                    from {
                        opacity: 0;
                        transform: translateY(-30px);
                    }
                    to {
                        opacity: 1;
                        transform: translateY(0);
                    }
                }

                @keyframes fadeInUp {
                    from {
                        opacity: 0;
                        transform: translateY(30px);
                    }
                    to {
                        opacity: 1;
                        transform: translateY(0);
                    }
                }

                @keyframes fadeIn {
                    from {
                        opacity: 0;
                    }
                    to {
                        opacity: 1;
                    }
                }

                @keyframes spin {
                    from {
                        transform: rotate(0deg);
                    }
                    to {
                        transform: rotate(360deg);
                    }
                }
            `}</style>
        </div>
    );
};

export default ScenarioView;