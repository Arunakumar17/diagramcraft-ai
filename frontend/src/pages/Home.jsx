import React, { useState } from 'react';
import { api } from '../services/api';
import DiagramTypeSelector from '../components/DiagramTypeSelector';
import PromptInput from '../components/PromptInput';
import PDFViewer from '../components/PDFViewer';
import LatexEditor from '../components/LatexEditor';
import ExportPanel from '../components/ExportPanel';
import HistoryPanel from '../components/HistoryPanel';

function Home() {
    const [selectedType, setSelectedType] = useState('flowchart');
    const [currentDiagram, setCurrentDiagram] = useState(null);
    const [isGenerating, setIsGenerating] = useState(false);
    const [error, setError] = useState(null);

    const handleGenerate = async (prompt) => {
        setIsGenerating(true);
        setError(null);
        setCurrentDiagram(null);

        try {
            const diagram = await api.generateDiagram(selectedType, prompt);
            setCurrentDiagram(diagram);
        } catch (err) {
            setError(err.response?.data?.detail || err.message || 'Failed to generate diagram');
        } finally {
            setIsGenerating(false);
        }
    };

    const handleSelectFromHistory = async (diagramId) => {
        try {
            const diagram = await api.getDiagram(diagramId);
            setCurrentDiagram(diagram);
            setSelectedType(diagram.diagram_type);
        } catch (err) {
            console.error('Failed to load diagram:', err);
        }
    };

    return (
        <div className="container" style={styles.container}>
            <div style={styles.grid}>
                {/* Left Column */}
                <div style={styles.leftColumn}>
                    <DiagramTypeSelector
                        selectedType={selectedType}
                        onTypeSelect={setSelectedType}
                    />

                    <PromptInput
                        selectedType={selectedType}
                        onGenerate={handleGenerate}
                        isGenerating={isGenerating}
                    />

                    <HistoryPanel onSelectDiagram={handleSelectFromHistory} />
                </div>

                {/* Right Column */}
                <div style={styles.rightColumn}>
                    <PDFViewer
                        diagram={currentDiagram}
                        isLoading={isGenerating}
                        error={error}
                    />

                    {currentDiagram && (
                        <>
                            <ExportPanel diagram={currentDiagram} />
                            <LatexEditor diagram={currentDiagram} />
                        </>
                    )}
                </div>
            </div>
        </div>
    );
}

const styles = {
    container: {
        paddingTop: '2rem',
        paddingBottom: '4rem',
    },
    grid: {
        display: 'grid',
        gridTemplateColumns: '1fr 1.5fr',
        gap: '2rem',
    },
    leftColumn: {
        display: 'flex',
        flexDirection: 'column',
    },
    rightColumn: {
        display: 'flex',
        flexDirection: 'column',
    },
    '@media (max-width: 1024px)': {
        grid: {
            gridTemplateColumns: '1fr',
        },
    },
};

export default Home;
