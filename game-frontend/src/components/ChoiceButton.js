import React, { useState } from 'react';

const ChoiceButton = ({ label, onClick }) => {
    const [isHovered, setIsHovered] = useState(false);

    const buttonStyle = {
        padding: '12px 20px',
        backgroundColor: '#667eea',
        color: '#ffffff',
        border: 'none',
        borderRadius: '10px',
        cursor: 'pointer',
        transition: 'all 0.3s ease',
        fontSize: '16px',
        fontWeight: '600',
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
        boxShadow: '0 4px 10px rgba(0, 0, 0, 0.2)',
        width: '100%',
        margin: '10px 0'
    };

    const buttonHoverStyle = {
        ...buttonStyle,
        backgroundColor: '#764ba2',
        transform: 'translateY(-2px)',
        boxShadow: '0 6px 15px rgba(0, 0, 0, 0.3)'
    };

    return (
        <button
            onClick={onClick}
            style={isHovered ? buttonHoverStyle : buttonStyle}
            onMouseEnter={() => setIsHovered(true)}
            onMouseLeave={() => setIsHovered(false)}
        >
            {label}
        </button>
    );
};

export default ChoiceButton;
