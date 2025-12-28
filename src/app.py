from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import build_app
import tempfile
import os

app = FastAPI()

agent = build_app()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

# Store conversation state per session
conversations = {}

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """Handle PDF file upload"""
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        # Initialize conversation state if needed
        if "default" not in conversations:
            conversations["default"] = {
                "messages": [],
                "data": None,
                "content": None
            }
        
        state = conversations["default"]
        
        # Load the PDF using your agent's logic
        from langchain_core.messages import HumanMessage
        state["messages"].append(HumanMessage(content=f"pdf {tmp_path}"))
        
        # Invoke agent to process the PDF
        result = agent.invoke(state)
        conversations["default"] = result
        
        # Clean up temp file
        os.unlink(tmp_path)
        
        return {"response": result["messages"][-1].content, "filename": file.filename}
    except Exception as e:
        return {"error": str(e)}

@app.post("/chat")
async def chat(request: ChatRequest):
    # For now, using a single conversation state
    # In production, you'd use session IDs
    if "default" not in conversations:
        conversations["default"] = {
            "messages": [],
            "data": None,
            "content": None
        }
    
    state = conversations["default"]
    
    # Add user message
    from langchain_core.messages import HumanMessage
    state["messages"].append(HumanMessage(content=request.message))
    
    # Invoke agent
    result = agent.invoke(state)
    
    # Update state
    conversations["default"] = result
    
    # Return the last message
    return {"response": result["messages"][-1].content}

@app.get("/")
async def root():
    return {"status": "ok"}

@app.post("/reset")
async def reset():
    """Reset the conversation"""
    conversations["default"] = {
        "messages": [],
        "data": None,
        "content": None
    }
    return {"status": "reset"}