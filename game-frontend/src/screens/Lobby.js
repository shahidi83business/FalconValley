import React, { useState, useContext, useEffect } from 'react';
import { AuthContext } from '../context/AuthContext';
import { Navigate, useNavigate } from 'react-router-dom';

const Lobby = () => {
    const { isAuthenticated, user } = useContext(AuthContext);
    const navigate = useNavigate();
    const [hoveredCard, setHoveredCard] = useState(null);
    const [selectedMode, setSelectedMode] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        // Add entrance animation
        document.body.style.overflow = 'hidden';
        return () => {
            document.body.style.overflow = 'auto';
        };
    }, []);

    if (!isAuthenticated) {
        return <Navigate to="/login" replace />;
    }

    const handleStartGame = (mode) => {
        setSelectedMode(mode);
        setIsLoading(true);
        
        // Simulate loading and navigation
        setTimeout(() => {
            navigate('/scenario');
        }, 1500);
    };

    const containerStyle = {
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        padding: '20px',
        position: 'relative',
        overflow: 'hidden'
    };

    const backgroundPatternStyle = {
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        opacity: 0.1,
        background: `
            radial-gradient(circle at 20% 50%, rgba(255, 255, 255, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(255, 255, 255, 0.2) 0%, transparent 50%),
            radial-gradient(circle at 40% 20%, rgba(255, 255, 255, 0.2) 0%, transparent 50%)
        `,
        pointerEvents: 'none'
    };

    const headerStyle = {
        textAlign: 'center',
        marginBottom: '50px',
        animation: 'fadeInDown 0.8s ease'
    };

    const titleStyle = {
        fontSize: '48px',
        fontWeight: 'bold',
        color: '#ffffff',
        marginBottom: '10px',
        textShadow: '2px 2px 4px rgba(0, 0, 0, 0.2)',
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    };

    const subtitleStyle = {
        fontSize: '20px',
        color: 'rgba(255, 255, 255, 0.9)',
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    };

    const welcomeMessageStyle = {
        fontSize: '16px',
        color: 'rgba(255, 255, 255, 0.8)',
        marginTop: '10px',
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    };

    const cardsContainerStyle = {
        display: 'flex',
        justifyContent: 'center',
        gap: '30px',
        flexWrap: 'wrap',
        maxWidth: '1200px',
        margin: '0 auto',
        animation: 'fadeInUp 0.8s ease 0.2s both'
    };

    const cardStyle = {
        backgroundColor: '#ffffff',
        borderRadius: '20px',
        padding: '30px',
        width: '300px',
        boxShadow: '0 10px 30px rgba(0, 0, 0, 0.2)',
        transition: 'all 0.3s ease',
        cursor: 'pointer',
        position: 'relative',
        overflow: 'hidden'
    };

    const cardHoverStyle = {
        ...cardStyle,
        transform: 'translateY(-10px) scale(1.02)',
        boxShadow: '0 20px 40px rgba(0, 0, 0, 0.3)'
    };

    const cardIconStyle = {
        fontSize: '64px',
        marginBottom: '20px',
        textAlign: 'center'
    };

    const cardTitleStyle = {
        fontSize: '24px',
        fontWeight: 'bold',
        color: '#333',
        marginBottom: '15px',
        textAlign: 'center',
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    };

    const cardDescriptionStyle = {
        fontSize: '14px',
        color: '#666',
        lineHeight: '1.6',
        textAlign: 'center',
        marginBottom: '20px',
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    };

    const cardButtonStyle = {
        width: '100%',
        padding: '12px',
        fontSize: '16px',
        fontWeight: '600',
        color: '#ffffff',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        border: 'none',
        borderRadius: '10px',
        cursor: 'pointer',
        transition: 'all 0.3s ease',
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    };

    const cardButtonHoverStyle = {
        ...cardButtonStyle,
        transform: 'translateY(-2px)',
        boxShadow: '0 5px 15px rgba(102, 126, 234, 0.3)'
    };

    const statsContainerStyle = {
        display: 'flex',
        justifyContent: 'center',
        gap: '40px',
        marginTop: '60px',
        animation: 'fadeIn 0.8s ease 0.4s both'
    };

    const statBoxStyle = {
        backgroundColor: 'rgba(255, 255, 255, 0.1)',
        backdropFilter: 'blur(10px)',
        borderRadius: '15px',
        padding: '20px 30px',
        textAlign: 'center',
        border: '1px solid rgba(255, 255, 255, 0.2)'
    };

    const statNumberStyle = {
        fontSize: '32px',
        fontWeight: 'bold',
        color: '#ffffff',
        marginBottom: '5px',
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    };

    const statLabelStyle = {
        fontSize: '14px',
        color: 'rgba(255, 255, 255, 0.8)',
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    };

    const loadingOverlayStyle = {
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.7)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 1000,
        backdropFilter: 'blur(5px)'
    };

    const loadingContentStyle = {
        backgroundColor: '#ffffff',
        borderRadius: '20px',
        padding: '40px',
        textAlign: 'center',
        animation: 'scaleIn 0.3s ease'
    };

    const spinnerStyle = {
        width: '50px',
        height: '50px',
        border: '4px solid #e1e8ed',
        borderTop: '4px solid #667eea',
        borderRadius: '50%',
        margin: '0 auto 20px',
        animation: 'spin 1s linear infinite'
    };

    const gameModes = [
        {
            id: 'quick',
            icon: '⚡',
            title: 'Quick Play',
            description: 'Jump into a fast-paced game with random scenarios. Perfect for a quick gaming session!',
            color: '#00b894'
        },
        {
            id: 'campaign',
            icon: '🎯',
            title: 'Campaign Mode',
            description: 'Experience the full story with progressive challenges and unlock new content.',
            color: '#6c5ce7'
        },
        {
            id: 'multiplayer',
            icon: '👥',
            title: 'Multiplayer',
            description: 'Challenge other players online and climb the global leaderboard.',
            color: '#fdcb6e'
        },
        {
            id: 'custom',
            icon: '⚙️',
            title: 'Custom Game',
            description: 'Create your own scenarios with custom rules and settings.',
            color: '#e17055'
        }
    ];

    return (
        <div style={containerStyle}>
            <div style={backgroundPatternStyle}></div>
            
            <div style={headerStyle}>
                <h1 style={titleStyle}>🎮 Game Lobby</h1>
                <p style={subtitleStyle}>Choose Your Adventure</p>
                {user && (
                    <p style={welcomeMessageStyle}>
                        Welcome back, <strong>{user.username || 'Player'}</strong>! Ready for a new challenge?
                    </p>
                )}
            </div>

            <div style={cardsContainerStyle}>
                {gameModes.map((mode) => (
                    <div
                        key={mode.id}
                        style={hoveredCard === mode.id ? cardHoverStyle : cardStyle}
                        onMouseEnter={() => setHoveredCard(mode.id)}
                        onMouseLeave={() => setHoveredCard(null)}
                        onClick={() => handleStartGame(mode.id)}
                    >
                        <div style={{ ...cardIconStyle, color: mode.color }}>
                            {mode.icon}
                        </div>
                        <h3 style={cardTitleStyle}>{mode.title}</h3>
                        <p style={cardDescriptionStyle}>{mode.description}</p>
                        <button
                            style={hoveredCard === mode.id ? cardButtonHoverStyle : cardButtonStyle}
                        >
                            Play Now
                        </button>
                        
                        {/* Decorative element */}
                        <div style={{
                            position: 'absolute',
                            top: '-50px',
                            right: '-50px',
                            width: '100px',
                            height: '100px',
                            borderRadius: '50%',
                            background: mode.color,
                            opacity: '0.1'
                        }}></div>
                    </div>
                ))}
            </div>

            <div style={statsContainerStyle}>
                <div style={statBoxStyle}>
                    <div style={statNumberStyle}>42</div>
                    <div style={statLabelStyle}>Games Played</div>
                </div>
                <div style={statBoxStyle}>
                    <div style={statNumberStyle}>85%</div>
                    <div style={statLabelStyle}>Win Rate</div>
                </div>
                <div style={statBoxStyle}>
                    <div style={statNumberStyle}>1,250</div>
                    <div style={statLabelStyle}>Total Score</div>
                </div>
                <div style={statBoxStyle}>
                    <div style={statNumberStyle}>#12</div>
                    <div style={statLabelStyle}>Global Rank</div>
                </div>
            </div>

            {isLoading && (
                <div style={loadingOverlayStyle}>
                    <div style={loadingContentStyle}>
                        <div style={spinnerStyle}></div>
                        <h3 style={{ color: '#333', marginBottom: '10px' }}>Loading Game...</h3>
                        <p style={{ color: '#666', fontSize: '14px' }}>
                            Preparing your {selectedMode === 'quick' ? 'Quick Play' : 
                                          selectedMode === 'campaign' ? 'Campaign' :
                                          selectedMode === 'multiplayer' ? 'Multiplayer' : 'Custom'} experience
                        </p>
                    </div>
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

                @keyframes scaleIn {
                    from {
                        opacity: 0;
                        transform: scale(0.8);
                    }
                    to {
                        opacity: 1;
                        transform: scale(1);
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

export default Lobby;