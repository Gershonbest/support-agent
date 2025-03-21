from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware  # Add this import
from typing import Optional
from datetime import datetime
import uvicorn, time
from contextlib import asynccontextmanager

from langchain_core.messages import HumanMessage
from src.agent import app as chat_app  # initialize_environment
from src.vector_database.vector_db import VectorDatabase

# Initialize environment on startup
# initialize_environment()

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4096, description="User input message")
    thread_id: Optional[int] = Field(default=42, description="Thread ID for conversation tracking")

class ChatResponse(BaseModel):
    response: str = Field(..., description="Assistant's response")
    timestamp: datetime = Field(default_factory=datetime.now)

class HealthResponse(BaseModel):
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(default_factory=datetime.now)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up the application...")
    yield
    # Shutdown
    print("Shutting down the application...")

app = FastAPI(
    title="HappyAI Chat API",
    description="API for interacting with HappyAI's customer support assistant",
    version="1.0.0",
    lifespan=lifespan
)

def generate_response(message: str, skin_type: str):
    # Simulate AI processing response in chunks
    responses = [
        f"Analyzing your message for {skin_type} skin...",
        "Finding the best skincare advice...",
        "Here’s a great tip: Hydration is key for healthy skin!",
        "Would you like more product recommendations?"
    ]
    for chunk in responses:
        yield chunk + " "
        time.sleep(1)  # Simulating delay

# Add CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/health", 
         response_model=HealthResponse,
         status_code=status.HTTP_200_OK,
         tags=["Health"])
async def health_check():
    """
    Endpoint to check if the service is running.
    Returns a 200 OK response if the service is healthy.
    """
    try:
        return HealthResponse(
            status="healthy",
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Service health check failed: {str(e)}"
        )
@app.get("/create_index", tags=["Documents"])
async def create_index():
    """
    Endpoint to add new documents to the vector database.
    """
    # Add new documents to the vector database
    try:
        vector_db = VectorDatabase(index_name="supportbot")
        vector_db.deploy_vectordatabase()
        return {"message": "New documents added to the vector database."}
    except Exception as e:
        raise Exception("Error adding new documents to the vector database")
    
@app.get("/ingest-documents", tags=["Documents"])
async def create_index():
    """
    Endpoint to add new documents to the vector database.
    """
    # Add new documents to the vector database
    try:
        vector_db = VectorDatabase(index_name="supportbot")
        response = vector_db.ingest_index()
        return {"message": response}
    except Exception as e:
        raise Exception("Error adding new documents to the vector database")
    
@app.post("/chat", 
          response_model=ChatResponse,
          status_code=status.HTTP_200_OK,
          tags=["Chat"])
async def chat_endpoint(request: ChatRequest):
    """
    Endpoint to interact with the chat model.
    Accepts a message and optional thread_id, returns the model's response.
    """
    try:
        # Initialize the state with the user's message
        initial_state = {
            "messages": [
                HumanMessage(content=request.message)
            ]
        }
        
        # Configuration for the chat
        config = {
            "configurable": {
                "thread_id": request.thread_id
            }
        }

        # Process the message through the LangGraph app
        response = None
        for event in chat_app.stream(initial_state, config=config):
            if event.get("agent"):
                msg = event['agent']['messages'][-1].content
                if msg:
                    response = msg
                    break

        if not response:
            raise ValueError("No response generated from the model")

        return ChatResponse(
            response=response,
            timestamp=datetime.now()
        )

    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat request: {str(e)}"
        )
    
@app.post("/chat-stream",
          status_code=status.HTTP_200_OK,
          tags=["Chat"])
async def chat_stream_endpoint(request: ChatRequest):
    """
    Endpoint to interact with the chat model.
    Accepts a message and optional thread_id, returns the model's response.
    """
    try:
        # Initialize the state with the user's message
        initial_state = {
            "messages": [
                HumanMessage(content=request.message)
            ]
        }
        
        # Configuration for the chat
        config = {
            "configurable": {
                "thread_id": request.thread_id
            }
        }

        # Process the message through the LangGraph app
        response = None
        for event in chat_app.stream(initial_state, config=config):
            if event.get("agent"):
                msg = event['agent']['messages'][-1].content
                if msg:
                    response = msg
                    break

        if not response:
            raise ValueError("No response generated from the model")

        return ChatResponse(
            response=response,
            timestamp=datetime.now()
        )

    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat request: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        workers=1
    )