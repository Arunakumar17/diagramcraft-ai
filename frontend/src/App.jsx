import React, { useState } from 'react';
import Home from './pages/Home';
import './styles/index.css';

function App() {
    return (
        <div className="App">
            {/* Header */}
            <header style={styles.header}>
                <div className="container" style={styles.headerContent}>
                    <div style={styles.logo}>
                        <span style={styles.logoIcon}>✨</span>
                        <h1 style={styles.logoText}>DiagramCraft.ai</h1>
                    </div>
                    <p style={styles.tagline}>AI-Powered LaTeX Diagram Generator</p>
                </div>
            </header>

            {/* Main Content */}
            <main>
                <Home />
            </main>

            {/* Footer */}
            <footer style={styles.footer}>
                <div className="container text-center">
                    <p style={styles.footerText}>
                        Powered by Groq AI • Professional LaTeX Diagrams
                    </p>
                </div>
            </footer>
        </div>
    );
}

const styles = {
    header: {
        padding: '2rem 0',
        borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
        marginBottom: '2rem',
    },
    headerContent: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: '0.5rem',
    },
    logo: {
        display: 'flex',
        alignItems: 'center',
        gap: '0.75rem',
    },
    logoIcon: {
        fontSize: '2rem',
    },
    logoText: {
        fontSize: '2rem',
        fontWeight: '800',
        background: 'linear-gradient(135deg, #8B5CF6 0%, #06B6D4 100%)',
        WebkitBackgroundClip: 'text',
        WebkitTextFillColor: 'transparent',
        backgroundClip: 'text',
    },
    tagline: {
        color: 'rgba(255, 255, 255, 0.6)',
        fontSize: '0.95rem',
    },
    footer: {
        padding: '2rem 0',
        marginTop: '4rem',
        borderTop: '1px solid rgba(255, 255, 255, 0.1)',
    },
    footerText: {
        color: 'rgba(255, 255, 255, 0.5)',
        fontSize: '0.9rem',
    },
};

export default App;
