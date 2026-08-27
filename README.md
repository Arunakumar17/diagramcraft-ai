# DiagramCraft.ai

<parameter name="🎨 AI-Powered LaTeX Diagram Generator

Generate professional, publication-quality diagrams using AI. Simply describe what you want, and let Groq AI create beautiful LaTeX/TikZ diagrams for you.

## ✨ Features

- **6 Diagram Types**: ER Diagrams, Flowcharts, Class Diagrams, State Diagrams, Gantt Charts, Mind Maps
- **AI-Powered**: Uses Groq API with Qwen 3.8 27B for intelligent LaTeX code generation
- **Professional Quality**: LaTeX/TikZ output suitable for academic papers and presentations
- **Multiple Export Formats**: PDF, PNG, and SVG
- **Modern UI**: Beautiful glassmorphic design with smooth animations
- **History**: Save and access your previously generated diagrams
- **LaTeX Editor**: View and copy the generated LaTeX code

## 🚀 Getting Started

### Prerequisites

- **Node.js** 18+ (for frontend)
- **Python** 3.10+ (for backend)
- **MongoDB** (running locally on port 27017)
- **LaTeX**: TeX Live or MiKTeX installed (for PDF compilation)
- **Groq API Key**: Get one from [console.groq.com](https://console.groq.com)

### Installation

#### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Ensure MongoDB is running:
```bash
# Check if MongoDB is running
mongod --version
```

4. Start the backend server:
```bash
python main.py
```

The backend API will be available at `http://localhost:8000`

#### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Using Docker (Optional)

If you prefer using Docker to avoid installing LaTeX locally:

```bash
# Start both backend and MongoDB using Docker Compose
docker-compose up -d

# The backend will be available at http://localhost:8000
```

**Note**: The Docker image is ~2-3GB due to the full TeX Live installation.

## 📖 Usage

1. **Select a Diagram Type**: Choose from ER Diagram, Flowchart, Class Diagram, State Diagram, Gantt Chart, or Mind Map

2. **Describe Your Diagram**: Enter a natural language description of what you want to create
   - Example: "Create an e-commerce database with users, products, and orders"

3. **Generate**: Click "Generate Diagram" and wait 10-30 seconds for the AI to create your diagram

4. **Export**: Download your diagram as PDF, PNG, or SVG

5. **View Code**: Check the LaTeX Editor section to see and copy the generated TikZ code

## 🎯 Example Prompts

- **ER Diagram**: "Design a social media database with users, posts, comments, and likes"
- **Flowchart**: "Create a user registration process with email verification"
- **Class Diagram**: "Model a banking system with Account, Customer, and Transaction classes"
- **State Diagram**: "Show the lifecycle of an online order from cart to delivery"
- **Gantt Chart**: "Plan a 6-month software development project with phases"
- **Mind Map**: "Organize concepts about artificial intelligence and machine learning"

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **Groq API**: AI inference for LaTeX code generation
- **Motor**: Async MongoDB driver
- **pdf2image**: PDF to PNG conversion
- **pdflatex**: LaTeX compilation engine

### Frontend
- **React 18**: UI library
- **Vite**: Build tool and dev server
- **Axios**: HTTP client
- **Custom CSS**: Glassmorphic design system

### Database
- **MongoDB**: Document storage for diagrams and history

## 📁 Project Structure

```
diagramcraft-ai/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Configuration & settings
│   ├── models/
│   │   └── diagram.py          # MongoDB models
│   ├── services/
│   │   ├── groq_service.py     # Groq AI integration
│   │   ├── latex_compiler.py   # LaTeX compilation
│   │   └── image_converter.py  # PDF to PNG/SVG
│   ├── templates/              # LaTeX templates
│   └── output/                 # Generated files
├── frontend/
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── pages/              # Page components
│   │   ├── services/           # API service
│   │   └── styles/             # CSS styles
│   └── index.html
└── docker-compose.yml
```

## 🔧 API Endpoints

- `POST /api/generate` - Generate diagram from prompt
- `GET /api/diagram/{id}` - Get diagram by ID
- `GET /api/history` - Get diagram history
- `DELETE /api/diagram/{id}` - Delete diagram
- `GET /api/health` - Health check

## 🐛 Troubleshooting

### LaTeX Compilation Errors

If you get LaTeX compilation errors:
- Ensure TeX Live or MiKTeX is properly installed
- Check that `pdflatex` is in your PATH
- Try running with Docker instead

### MongoDB Connection Issues

- Ensure MongoDB is running: `mongod --version`
- Check connection string in `.env` file
- Default: `mongodb://localhost:27017`

### Groq API Errors

- Verify your API key in `backend/.env`
- Check rate limits on your Groq account
- Ensure you have credits available

## 📝 License

MIT License - Feel free to use this project for your own purposes!

## 🙏 Acknowledgments

- **Groq** for lightning-fast AI inference
- **LaTeX/TikZ** for amazing diagram capabilities
- **FastAPI** for the excellent Python framework
- **React** for the powerful UI library

---
