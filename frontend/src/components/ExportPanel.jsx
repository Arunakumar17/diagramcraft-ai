import React from 'react';

function ExportPanel({ diagram }) {
    if (!diagram) {
        return null;
    }

    const downloadFile = (url, filename) => {
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    return (
        <div style={styles.container} className="glass-card">
            <h3 style={styles.title}>
                <span style={styles.titleIcon}>💾</span>
                Export Diagram
            </h3>

            <div style={styles.buttonGrid}>
                <button
                    onClick={() => downloadFile(diagram.pdf_url, 'diagram.pdf')}
                    style={styles.exportBtn}
                    className="btn btn-secondary"
                >
                    <span style={styles.btnIcon}>📄</span>
                    Download PDF
                </button>

                <button
                    onClick={() => downloadFile(diagram.png_url, 'diagram.png')}
                    style={styles.exportBtn}
                    className="btn btn-secondary"
                >
                    <span style={styles.btnIcon}>🖼️</span>
                    Download PNG
                </button>

                {diagram.svg_url && (
                    <button
                        onClick={() => downloadFile(diagram.svg_url, 'diagram.svg')}
                        style={styles.exportBtn}
                        className="btn btn-secondary"
                    >
                        <span style={styles.btnIcon}>🎨</span>
                        Download SVG
                    </button>
                )}
            </div>
        </div>
    );
}

const styles = {
    container: {
        marginBottom: '2rem',
    },
    title: {
        fontSize: '1.25rem',
        fontWeight: '600',
        color: 'rgba(255, 255, 255, 0.9)',
        display: 'flex',
        alignItems: 'center',
        gap: '0.5rem',
        marginBottom: '1rem',
    },
    titleIcon: {
        fontSize: '1.5rem',
    },
    buttonGrid: {
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
        gap: '1rem',
    },
    exportBtn: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        gap: '0.5rem',
        padding: '1rem',
    },
    btnIcon: {
        fontSize: '1.5rem',
    },
};

export default ExportPanel;
