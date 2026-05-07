import React from 'react';

const ChoiceButton = ({ label, onClick }) => {
    return (
        <button onClick={onClick} className="choice-button">
            {label}
        </button>
    );
};

export default ChoiceButton;