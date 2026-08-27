import React, { useState } from 'react';

function LatexEditor({ diagram }) {
    const [copied, setCopied] = useState(false);

    if (!diagram) {
        return null;
    }

    const copyToClipboard = () => {
        navigator.clipboard.writeText(diagram.latex_code);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    return (
        <div style={styles.container} className="glass-card">
            <div style={styles.header}>
                <h3 style={styles.title}>
                    <span style={styles.titleIcon}>📝</span>
                    LaTeX Code
                </h3>
                <button onClick={copyToClipboard} style={styles.copyBtn} className="btn-secondary">
                    {copied ? '✓ Copied!' : '📋 Copy Code'}
                </button>
            </div>

            <div style={styles.codeContainer}>
                <pre style={styles.code}>
                    <code>{diagram.latex_code}</code>
                </pre>
            </div>

            <p style={styles.hint}>
                💡 You can copy this code and use it in your LaTeX documents
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
    copyBtn: {
        padding: '0.5rem 1rem',
        fontSize: '0.875rem',
    },
    codeContainer: {
        background: 'rgba(0, 0, 0, 0.3)',
        borderRadius: '8px',
        padding: '1rem',
        marginBottom: '1rem',
        maxHeight: '300px',
        overflow: 'auto',
    },
    code: {
        color: '#22D3EE',
        fontFamily: 'Monaco, Consolas, "Courier New", monospace',
        fontSize: '0.875rem',
        lineHeight: '1.5',
        margin: 0,
        whiteSpace: 'pre-wrap',
        wordBreak: 'break-word',
    },
    hint: {
        fontSize: '0.875rem',
        color: 'rgba(255, 255, 255, 0.5)',
        margin: 0,
        textAlign: 'center',
    },
};

export default LatexEditor;
