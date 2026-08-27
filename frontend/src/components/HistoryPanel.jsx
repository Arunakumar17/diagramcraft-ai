import React, { useEffect, useState } from 'react';
import { api } from '../services/api';

function HistoryPanel({ onSelectDiagram }) {
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadHistory();
    }, []);

    const loadHistory = async () => {
        try {
            setLoading(true);
            const data = await api.getHistory(10);
            setHistory(data.history || []);
        } catch (error) {
            console.error('Failed to load history:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async (diagramId, e) => {
        e.stopPropagation();
        if (confirm('Are you sure you want to delete this diagram?')) {
            try {
                await api.deleteDiagram(diagramId);
                loadHistory();
            } catch (error) {
                console.error('Failed to delete diagram:', error);
            }
        }
    };

    const formatDate = (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
        });
    };

    if (loading) {
        return (
            <div style={styles.container} className="glass-card">
                <h3 style={styles.title}>📜 History</h3>
                <div style={styles.loading}>
                    <div className="spinner" style={{ width: '30px', height: '30px', borderWidth: '3px' }} />
                </div>
            </div>
        );
    }

    return (
        <div style={styles.container} className="glass-card">
            <div style={styles.header}>
                <h3 style={styles.title}>📜 History</h3>
                <button onClick={loadHistory} style={styles.refreshBtn} className="btn-secondary">
                    🔄
                </button>
            </div>

            {history.length === 0 ? (
                <p style={styles.empty}>No diagrams yet. Create your first one!</p>
            ) : (
                <div style={styles.list}>
                    {history.map((item) => (
                        <div
                            key={item.id}
                            onClick={() => onSelectDiagram(item.id)}
                            style={styles.historyItem}
                            className="glass-card"
                        >
                            <div style={styles.thumbnail}>
                                <img src={item.png_url} alt="Diagram" style={styles.thumbnailImg} />
                            </div>
                            <div style={styles.itemInfo}>
                                <div style={styles.itemType}>{item.diagram_type.replace('_', ' ')}</div>
                                <div style={styles.itemPrompt}>{item.user_prompt.substring(0, 50)}...</div>
                                <div style={styles.itemDate}>{formatDate(item.created_at)}</div>
                            </div>
                            <button
                                onClick={(e) => handleDelete(item.id, e)}
                                style={styles.deleteBtn}
                                className="btn-secondary"
                            >
                                🗑️
                            </button>
                        </div>
                    ))}
                </div>
            )}
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
        margin: 0,
    },
    refreshBtn: {
        width: '36px',
        height: '36px',
        padding: '0',
        fontSize: '1rem',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
    },
    loading: {
        display: 'flex',
        justifyContent: 'center',
        padding: '2rem',
    },
    empty: {
        textAlign: 'center',
        color: 'rgba(255, 255, 255, 0.5)',
        padding: '2rem',
    },
    list: {
        display: 'flex',
        flexDirection: 'column',
        gap: '0.75rem',
        maxHeight: '500px',
        overflowY: 'auto',
    },
    historyItem: {
        display: 'flex',
        alignItems: 'center',
        gap: '1rem',
        padding: '0.875rem',
        cursor: 'pointer',
        transition: 'all 0.2s ease',
    },
    thumbnail: {
        width: '60px',
        height: '60px',
        borderRadius: '8px',
        overflow: 'hidden',
        flexShrink: 0,
        background: 'rgba(255, 255, 255, 0.05)',
    },
    thumbnailImg: {
        width: '100%',
        height: '100%',
        objectFit: 'cover',
    },
    itemInfo: {
        flex: 1,
        minWidth: 0,
    },
    itemType: {
        fontSize: '0.875rem',
        fontWeight: '600',
        color: 'var(--primary-light)',
        marginBottom: '0.25rem',
        textTransform: 'capitalize',
    },
    itemPrompt: {
        fontSize: '0.875rem',
        color: 'rgba(255, 255, 255, 0.7)',
        whiteSpace: 'nowrap',
        overflow: 'hidden',
        textOverflow: 'ellipsis',
        marginBottom: '0.25rem',
    },
    itemDate: {
        fontSize: '0.75rem',
        color: 'rgba(255, 255, 255, 0.5)',
    },
    deleteBtn: {
        width: '36px',
        height: '36px',
        padding: '0',
        fontSize: '1rem',
        flexShrink: 0,
    },
};

export default HistoryPanel;
