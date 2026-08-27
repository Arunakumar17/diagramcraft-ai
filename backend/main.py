from fastapi import FastAPI, HTTPException, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from bson import ObjectId
from contextlib import asynccontextmanager
import os
import uuid

from config import settings
from models.diagram import DiagramModel, DiagramResponse, GenerateRequest
from services.groq_service import groq_service
from services.latex_compiler import latex_compiler
from services.image_converter import image_converter

# MongoDB client
client = None
db = None
diagrams_collection = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global client, db, diagrams_collection
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]
    diagrams_collection = db.diagrams
    
    try:
        await client.admin.command('ping')
        print("✅ Connected to MongoDB successfully")
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        print("⚠️ Server will continue, but database features won't work")
    
    yield
    
    # Shutdown
    if client:
        client.close()
        print("📪 MongoDB connection closed")

app = FastAPI(title="DiagramCraft.ai API", version="1.0.0", lifespan=lifespan)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (generated diagrams)
app.mount("/output", StaticFiles(directory=settings.OUTPUT_DIR), name="output")

@app.get("/")
async def root():
    return {"message": "DiagramCraft.ai API", "version": "1.0.0"}

@app.post("/api/generate", response_model=DiagramResponse)
async def generate_diagram(request: GenerateRequest):
    """Generate a diagram from natural language prompt"""
    try:
        # Validate diagram type
        valid_types = ["er_diagram", "flowchart", "class_diagram", "state_diagram", "gantt_chart", "mindmap"]
        if request.diagram_type not in valid_types:
            raise HTTPException(status_code=400, detail=f"Invalid diagram type. Must be one of: {', '.join(valid_types)}")
        
        # Generate LaTeX code using Groq
        latex_code = groq_service.generate_latex_code(request.diagram_type, request.prompt)
        
        # Create unique ID for this diagram
        diagram_id = str(uuid.uuid4())
        
        # Compile LaTeX to PDF
        pdf_path = latex_compiler.compile_latex(latex_code, diagram_id, request.diagram_type)
        
        # Convert PDF to PNG
        png_path = image_converter.pdf_to_png(pdf_path, diagram_id)
        
        # Try to convert to SVG (optional)
        svg_path = image_converter.pdf_to_svg(pdf_path, diagram_id)
        
        # Create diagram document
        diagram_doc = {
            "diagram_type": request.diagram_type,
            "user_prompt": request.prompt,
            "latex_code": latex_code,
            "pdf_path": os.path.basename(pdf_path),
            "png_path": os.path.basename(png_path),
            "svg_path": os.path.basename(svg_path) if svg_path else None,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # Insert into MongoDB
        result = await diagrams_collection.insert_one(diagram_doc)
        
        # Return response
        return DiagramResponse(
            id=str(result.inserted_id),
            diagram_type=request.diagram_type,
            user_prompt=request.prompt,
            latex_code=latex_code,
            pdf_url=f"/output/{diagram_doc['pdf_path']}",
            png_url=f"/output/{diagram_doc['png_path']}",
            svg_url=f"/output/{diagram_doc['svg_path']}" if diagram_doc['svg_path'] else None,
            created_at=diagram_doc['created_at']
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/diagram/{diagram_id}", response_model=DiagramResponse)
async def get_diagram(diagram_id: str):
    """Get a diagram by ID"""
    try:
        diagram = await diagrams_collection.find_one({"_id": ObjectId(diagram_id)})
        if not diagram:
            raise HTTPException(status_code=404, detail="Diagram not found")
        
        return DiagramResponse(
            id=str(diagram["_id"]),
            diagram_type=diagram["diagram_type"],
            user_prompt=diagram["user_prompt"],
            latex_code=diagram["latex_code"],
            pdf_url=f"/output/{diagram['pdf_path']}",
            png_url=f"/output/{diagram['png_path']}",
            svg_url=f"/output/{diagram['svg_path']}" if diagram.get('svg_path') else None,
            created_at=diagram["created_at"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/history")
async def get_history(limit: int = 20):
    """Get user's diagram history"""
    try:
        cursor = diagrams_collection.find().sort("created_at", -1).limit(limit)
        diagrams = await cursor.to_list(length=limit)
        
        history = []
        for diagram in diagrams:
            history.append({
                "id": str(diagram["_id"]),
                "diagram_type": diagram["diagram_type"],
                "user_prompt": diagram["user_prompt"],
                "png_url": f"/output/{diagram['png_path']}",
                "created_at": diagram["created_at"]
            })
        
        return {"history": history, "total": len(history)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/diagram/{diagram_id}")
async def delete_diagram(diagram_id: str):
    """Delete a diagram"""
    try:
        # Find diagram
        diagram = await diagrams_collection.find_one({"_id": ObjectId(diagram_id)})
        if not diagram:
            raise HTTPException(status_code=404, detail="Diagram not found")
        
        # Delete files
        for file_key in ['pdf_path', 'png_path', 'svg_path']:
            if diagram.get(file_key):
                file_path = os.path.join(settings.OUTPUT_DIR, diagram[file_key])
                if os.path.exists(file_path):
                    os.remove(file_path)
        
        # Delete from database
        await diagrams_collection.delete_one({"_id": ObjectId(diagram_id)})
        
        return {"message": "Diagram deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "mongodb": "connected"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
