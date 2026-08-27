import React, { useState } from 'react';

const EXAMPLE_PROMPTS = {
    er_diagram: 'Create an e-commerce database with users, products, orders, and payments',
    flowchart: 'Create a user authentication flow with login, signup, and password reset',
    class_diagram: 'Design a library management system with Book, User, and Loan classes',
    state_diagram: 'Create a state machine for an online order process',
    gantt_chart: 'Create a project timeline for developing a mobile app in 3 months',
    mindmap: 'Create a mind map about machine learning concepts',
};

function PromptInput({ selectedType, onGenerate, isGenerating }) {
    const [prompt, setPrompt] = useState('');

    const handleGenerate = () => {
        if (prompt.trim() && selectedType) {
            onGenerate(prompt);
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
            handleGenerate();
        }
    };

    const useExample = () => {
        setPrompt(EXAMPLE_PROMPTS[selectedType] || '');
    };

    return (
        <div style={styles.container} className="glass-card">
            <div style={styles.header}>
                <h3 style={styles.title}>
                    <span style={styles.titleIcon}>✍️</span>
                    Describe Your Diagram
                </h3>
                {selectedType && (
                    <button onClick={useExample} style={styles.exampleBtn} className="btn-secondary">
                        Use Example
                    </button>
                )}
            </div>

            <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder={
                    selectedType
                        ? `Describe the ${selectedType.replace('_', ' ')} you want to create...`
                        : 'Please select a diagram type first...'
                }
                disabled={!selectedType || isGenerating}
                style={styles.textarea}
                className="textarea"
            />

            <div style={styles.footer}>
                <div style={styles.charCount}>
                    {prompt.length} characters
                </div>
                <button
                    onClick={handleGenerate}
                    disabled={!prompt.trim() || !selectedType || isGenerating}
                    style={styles.generateBtn}
                    className="btn btn-primary"
                >
                    {isGenerating ? (
                        <>
                            <div className="spinner" style={{ width: '20px', height: '20px', borderWidth: '2px', marginRight: '0.5rem' }} />
                            Generating...
                        </>
                    ) : (
                        <>
                            <span style={styles.btnIcon}>✨</span>
                            Generate Diagram
                        </>
                    )}
                </button>
            </div>

            <p style={styles.hint}>
                💡 Tip: Press <kbd style={styles.kbd}>Ctrl+Enter</kbd> to generate
            </p>
        </div>
    );
}

const styles = {
    container: {
        marginBottom: '2rem',
    },
    header: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '1rem',
    },
    title: {
        fontSize: '1.25rem',
        fontWeight: '600',
        color: 'rgba(255, 255, 255, 0.9)',
        display: 'flex',
        alignItems: 'center',
        gap: '0.5rem',
        margin: 0,
    },
    titleIcon: {
        fontSize: '1.5rem',
    },
    exampleBtn: {
        padding: '0.5rem 1rem',
        fontSize: '0.875rem',
    },
    textarea: {
        minHeight: '120px',
        marginBottom: '1rem',
    },
    footer: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '0.5rem',
    },
    charCount: {
        fontSize: '0.875rem',
        color: 'rgba(255, 255, 255, 0.5)',
    },
    generateBtn: {
        display: 'flex',
        alignItems: 'center',
        gap: '0.5rem',
    },
    btnIcon: {
        fontSize: '1.25rem',
    },
    hint: {
        fontSize: '0.875rem',
        color: 'rgba(255, 255, 255, 0.5)',
        margin: 0,
        textAlign: 'center',
    },
    kbd: {
        background: 'rgba(255, 255, 255, 0.1)',
        padding: '0.125rem 0.375rem',
        borderRadius: '4px',
        fontFamily: 'monospace',
        fontSize: '0.875rem',
    },
};

export default PromptInput;
