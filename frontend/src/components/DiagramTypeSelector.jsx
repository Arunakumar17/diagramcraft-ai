import React from 'react';

const DIAGRAM_TYPES = [
    { id: 'er_diagram', name: 'ER Diagram', icon: '🗂️', description: 'Entity-Relationship' },
    { id: 'flowchart', name: 'Flowchart', icon: '📊', description: 'Process Flow' },
    { id: 'class_diagram', name: 'Class Diagram', icon: '🏗️', description: 'UML Classes' },
    { id: 'state_diagram', name: 'State Diagram', icon: '🔄', description: 'State Machine' },
    { id: 'gantt_chart', name: 'Gantt Chart', icon: '📅', description: 'Timeline' },
    { id: 'mindmap', name: 'Mind Map', icon: '🧠', description: 'Ideas & Concepts' },
];

function DiagramTypeSelector({ selectedType, onTypeSelect }) {
    return (
        <div style={styles.container}>
            <h3 style={styles.title}>Select Diagram Type</h3>
            <div style={styles.grid}>
                {DIAGRAM_TYPES.map((type) => (
                    <button
                        key={type.id}
                        onClick={() => onTypeSelect(type.id)}
                        style={{
                            ...styles.typeCard,
                            ...(selectedType === type.id ? styles.typeCardActive : {}),
                        }}
                        className="glass-card"
                    >
                        <span style={styles.icon}>{type.icon}</span>
                        <div style={styles.typeInfo}>
                            <h4 style={styles.typeName}>{type.name}</h4>
                            <p style={styles.typeDesc}>{type.description}</p>
                        </div>
                        {selectedType === type.id && (
                            <div style={styles.activeIndicator}>✓</div>
                        )}
                    </button>
                ))}
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
        marginBottom: '1rem',
        color: 'rgba(255, 255, 255, 0.9)',
    },
    grid: {
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: '1rem',
    },
    typeCard: {
        display: 'flex',
        alignItems: 'center',
        gap: '1rem',
        padding: '1.25rem',
        background: 'none',
        border: 'none',
        cursor: 'pointer',
        position: 'relative',
        transition: 'all 0.3s ease',
    },
    typeCardActive: {
        background: 'rgba(139, 92, 246, 0.15)',
        borderColor: 'rgba(139, 92, 246, 0.5)',
    },
    icon: {
        fontSize: '2rem',
    },
    typeInfo: {
        flex: 1,
        textAlign: 'left',
    },
    typeName: {
        fontSize: '1rem',
        fontWeight: '600',
        color: 'white',
        marginBottom: '0.25rem',
    },
    typeDesc: {
        fontSize: '0.875rem',
        color: 'rgba(255, 255, 255, 0.5)',
        margin: 0,
    },
    activeIndicator: {
        position: 'absolute',
        top: '0.5rem',
        right: '0.5rem',
        width: '24px',
        height: '24px',
        background: 'linear-gradient(135deg, #8B5CF6 0%, #06B6D4 100%)',
        borderRadius: '50%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontSize: '0.875rem',
        fontWeight: 'bold',
    },
};

export default DiagramTypeSelector;
