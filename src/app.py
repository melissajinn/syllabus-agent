from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .agent import build_app
import tempfile
import os

app = FastAPI()

agent = build_app()

# connects frontend and backend, lets frontend access backend api
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"], # allows data retrieval, updates, delition
    allow_headers=["*"], # allows headers (metadata) to be sent to backend
)

class ChatRequest(BaseModel): # pydantic model to validate chat as valid string
    message: str

# store conversation here
conversations = {}

# upload pdf function
@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """Handle PDF file upload"""
    try:
        # save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=True, suffix=".pdf") as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file.flush()
            tmp_path = tmp_file.name
        
            # Initialize conversation state if needed
            if "default" not in conversations:
                conversations["default"] = {
                    "messages": [],
                    "data": None,
                    "content": None
                }
        
            state = conversations["default"]
        
            # load pdf
            from langchain_core.messages import HumanMessage
            state["messages"].append(HumanMessage(content="pdf " + tmp_path))
        
            # invoke agent
            result = agent.invoke(state)
            conversations["default"] = result
        
        return {"response": result["messages"][-1].content, "filename": file.filename}
    except Exception as e:
        return {"error": str(e)}

# actual chat
@app.post("/chat")
async def chat(request: ChatRequest):
    # using single default conversation rne
    if "default" not in conversations:
        conversations["default"] = {
            "messages": [],
            "data": None,
            "content": None
        }
    
    state = conversations["default"]
    
    # user message
    from langchain_core.messages import HumanMessage
    state["messages"].append(HumanMessage(content=request.message))

    result = agent.invoke(state)
    conversations["default"] = result
    return {"response": result["messages"][-1].content}

# check that server is running
@app.get("/")
async def root():
    return {"status": "running"}

@app.post("/reset")
async def reset():
    """Reset the conversation"""
    conversations["default"] = {
        "messages": [],
        "data": None,
        "content": None
    }
    return {"status": "reset"}