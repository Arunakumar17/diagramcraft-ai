import React, { useState } from 'react';

function PDFViewer({ diagram, isLoading, error }) {
    const [zoom, setZoom] = useState(100);

    if (error) {
        return (
            <div style={styles.container} className="glass-card">
                <div style={styles.error}>
                    <span style={styles.errorIcon}>❌</span>
                    <h3 style={styles.errorTitle}>Generation Failed</h3>
                    <p style={styles.errorMessage}>{error}</p>
                </div>
            </div>
        );
    }

    if (isLoading) {
        return (
            <div style={styles.container} className="glass-card">
                <div style={styles.loading}>
                    <div className="spinner" style={{ width: '60px', height: '60px', borderWidth: '4px' }} />
                    <h3 style={styles.loadingTitle}>Generating Your Diagram...</h3>
                    <p style={styles.loadingText}>
                        The AI is creating LaTeX code and compiling it to PDF. This may take 10-30 seconds.
                    </p>
                </div>
            </div>
        );
    }

    if (!diagram) {
        return (
            <div style={styles.container} className="glass-card">
                <div style={styles.placeholder}>
                    <span style={styles.placeholderIcon}>📐</span>
                    <h3 style={styles.placeholderTitle}>No Diagram Yet</h3>
                    <p style={styles.placeholderText}>
                        Select a diagram type and describe what you want to create
                    </p>
                </div>
            </div>
        );
    }

    return (
        <div style={styles.container} className="glass-card">
            <div style={styles.header}>
                <h3 style={styles.title}>
                    <span style={styles.titleIcon}>📊</span>
                    Generated Diagram
                </h3>
                <div style={styles.controls}>
                    <button
                        onClick={() => setZoom(Math.max(50, zoom - 10))}
                        style={styles.zoomBtn}
                        className="btn-secondary"
                    >
                        -
                    </button>
                    <span style={styles.zoomLevel}>{zoom}%</span>
                    <button
                        onClick={() => setZoom(Math.min(200, zoom + 10))}
                        style={styles.zoomBtn}
                        className="btn-secondary"
                    >
                        +
                    </button>
                </div>
            </div>

            <div style={styles.viewerContainer}>
                <img
                    src={diagram.png_url}
                    alt="Generated Diagram"
                    style={{
                        ...styles.image,
                        transform: `scale(${zoom / 100})`,
                    }}
                />
            </div>
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
        marginBottom: '1.5rem',
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
    controls: {
        display: 'flex',
        alignItems: 'center',
        gap: '0.5rem',
    },
    zoomBtn: {
        width: '36px',
        height: '36px',
        padding: '0',
        fontSize: '1.25rem',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
    },
    zoomLevel: {
        fontSize: '0.875rem',
        color: 'rgba(255, 255, 255, 0.7)',
        minWidth: '50px',
        textAlign: 'center',
    },
    viewerContainer: {
        background: 'rgba(255, 255, 255, 0.02)',
        borderRadius: '8px',
        padding: '2rem',
        minHeight: '400px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        overflow: 'auto',
    },
    image: {
        maxWidth: '100%',
        height: 'auto',
        transition: 'transform 0.3s ease',
        transformOrigin: 'center',
    },
    placeholder: {
        textAlign: 'center',
        padding: '4rem 2rem',
    },
    placeholderIcon: {
        fontSize: '4rem',
        display: 'block',
        marginBottom: '1rem',
    },
    placeholderTitle: {
        fontSize: '1.5rem',
        fontWeight: '600',
        marginBottom: '0.5rem',
        color: 'rgba(255, 255, 255, 0.8)',
    },
    placeholderText: {
        color: 'rgba(255, 255, 255, 0.5)',
        fontSize: '1rem',
    },
    loading: {
        textAlign: 'center',
        padding: '4rem 2rem',
    },
    loadingTitle: {
        fontSize: '1.5rem',
        fontWeight: '600',
        marginTop: '1.5rem',
        marginBottom: '0.5rem',
        color: 'rgba(255, 255, 255, 0.8)',
    },
    loadingText: {
        color: 'rgba(255, 255, 255, 0.5)',
        fontSize: '0.95rem',
    },
    error: {
        textAlign: 'center',
        padding: '4rem 2rem',
    },
    errorIcon: {
        fontSize: '4rem',
        display: 'block',
        marginBottom: '1rem',
    },
    errorTitle: {
        fontSize: '1.5rem',
        fontWeight: '600',
        marginBottom: '0.5rem',
        color: '#F59E0B',
    },
    errorMessage: {
        color: 'rgba(255, 255, 255, 0.7)',
        fontSize: '1rem',
    },
};

export default PDFViewer;
