from typing import Dict, List, Any, Optional, TypedDict, Annotated, Literal
from uuid import UUID, uuid4
import json
from datetime import datetime

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import Document
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint import MemorySaver

# Import the memory type analyzer tool
from memory_type_analyzer import memory_type_node

# Import your repository and memory models
from src.database.repository.meta.user_history_repository_meta import UserHistoryRepositoryMeta
from src.database.repository.memory_repo import (
    ProceduralMemoryRepository,
    SemanticMemoryRepository,
    EpisodicMemoryRepository
)

# Define state for the agent
class AgentState(TypedDict):
    messages: List[Any]  # All messages in the conversation
    user_id: str
    user_input: str
    current_memory_type: Optional[Literal["episodic", "semantic", "procedural", "none"]]
    memory_type_confidence: Optional[float]
    memory_type_reasoning: Optional[str]
    memory_results: List[Dict[str, Any]]
    context: List[Document]
    response: Optional[str]

# Memory Query - Queries the appropriate memory repository
async def query_memory(state: AgentState, 
                      semantic_repo: SemanticMemoryRepository,
                      episodic_repo: EpisodicMemoryRepository,
                      procedural_repo: ProceduralMemoryRepository) -> AgentState:
    """
    Queries the appropriate memory repository based on the detected memory type
    """
    user_id = state["user_id"]
    memory_type = state["current_memory_type"]
    user_input = state["user_input"]
    results = []
    
    if memory_type == "semantic":
        # Query semantic memory
        memory = await semantic_repo.get_user_memory(user_id)
        if memory:
            results.append({
                "type": "semantic",
                "name": memory.name,
                "preferences": memory.preferences,
                "learned_facts": memory.learned_facts
            })
    
    elif memory_type == "episodic":
        # Query episodic memory
        events = await episodic_repo.get_user_events(user_id)
        for event in events:
            # Simple relevance check (could be more sophisticated)
            if any(keyword in user_input.lower() for keyword in event.event_name.lower().split()):
                results.append({
                    "type": "episodic",
                    "event_id": event.event_id,
                    "event_name": event.event_name,
                    "event_description": event.event_description,
                    "created_at": event.created_at.isoformat() if event.created_at else None
                })
    
    elif memory_type == "procedural":
        # Query procedural memory based on keywords in input
        skills = await procedural_repo.get_all_skills()
        for skill in skills:
            # Simple relevance check (could be more sophisticated)
            if skill.skill_name.lower() in user_input.lower():
                results.append({
                    "type": "procedural",
                    "skill_name": skill.skill_name,
                    "steps": skill.steps
                })
    
    return {**state, "memory_results": results}

# Check if relevant data was found
def check_relevant_data(state: AgentState) -> Literal["rag_search", "add_to_context"]:
    """
    Checks if relevant memory data was found
    """
    if not state["memory_results"]:
        return "rag_search"
    return "add_to_context"

# RAG Context Search
async def rag_search(state: AgentState) -> AgentState:
    """
    Performs a RAG search when no relevant memory data is found
    """
    # Here you would implement your RAG retrieval logic
    # This is a placeholder for demonstration
    context_docs = [
        Document(page_content="This is a placeholder RAG retrieved document", metadata={"source": "rag"})
    ]
    
    return {**state, "context": context_docs}

# Add Memory Data to Context
def add_to_context(state: AgentState) -> AgentState:
    """
    Adds memory data to the context
    """
    memory_results = state["memory_results"]
    context_docs = []
    
    for result in memory_results:
        memory_type = result["type"]
        if memory_type == "semantic":
            content = f"User Preferences: {json.dumps(result['preferences'])}\n"
            content += f"Learned Facts: {json.dumps(result['learned_facts'])}"
            doc = Document(page_content=content, metadata={"source": "semantic_memory"})
            context_docs.append(doc)
        
        elif memory_type == "episodic":
            content = f"Previous Event: {result['event_name']}\n"
            content += f"Description: {result['event_description']}\n"
            content += f"When: {result['created_at']}"
            doc = Document(page_content=content, metadata={"source": "episodic_memory"})
            context_docs.append(doc)
        
        elif memory_type == "procedural":
            content = f"How to {result['skill_name']}:\n{result['steps']}"
            doc = Document(page_content=content, metadata={"source": "procedural_memory"})
            context_docs.append(doc)
    
    return {**state, "context": context_docs}

# Generate Response
def generate_response(state: AgentState) -> AgentState:
    """
    Generates a response using the context and user input
    """
    llm = ChatOpenAI(model="gpt-4o-mini")
    
    context_text = "\n\n".join([doc.page_content for doc in state["context"]])
    memory_type = state["current_memory_type"]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
        You are an AI assistant with access to the user's memory. 
        Use the context information to personalize your response.
        
        Context:
        {context}
        
        Memory Type: {memory_type}
        """),
        ("user", "{user_input}")
    ])
    
    response = llm.invoke(
        prompt.format(
            context=context_text,
            memory_type=memory_type,
            user_input=state["user_input"]
        )
    ).content
    
    return {**state, "response": response}

# Store Memory
async def store_memory(state: AgentState,
                      semantic_repo: SemanticMemoryRepository,
                      episodic_repo: EpisodicMemoryRepository,
                      procedural_repo: ProceduralMemoryRepository,
                      user_history_repo: UserHistoryRepositoryMeta) -> AgentState:
    """
    Stores the conversation in memory for future reference
    """
    user_id = state["user_id"]
    user_input = state["user_input"]
    response = state["response"]
    
    # Store in chat history
    user_id_uuid = UUID(user_id) if isinstance(user_id, str) else user_id
    await user_history_repo.add_one(user_input, response, user_id_uuid)
    
    # Extract and store potential semantic memory
    # Simple example: extract preferences
    if "I like" in user_input or "I prefer" in user_input or "I enjoy" in user_input:
        memory = await semantic_repo.get_user_memory(user_id)
        if not memory:
            await semantic_repo.create_user_memory(user_id)
        
        # Simple preference extraction (in a real system, use NLP)
        if "I like" in user_input:
            preference = user_input.split("I like")[1].strip().rstrip(".")
            await semantic_repo.add_learned_fact(user_id, f"likes_{datetime.now().isoformat()}", preference)
    
    # Log significant interactions as episodic memories
    if len(user_input) > 100 or "remember" in user_input.lower():
        event_name = f"Conversation on {datetime.now().strftime('%Y-%m-%d')}"
        event_description = f"User said: {user_input[:100]}... and you responded about {state['current_memory_type']} information"
        await episodic_repo.add_event(user_id, str(uuid4()), event_name, event_description)
    
    return state

# Create the LangGraph
def create_memory_agent(
    semantic_repo: SemanticMemoryRepository,
    episodic_repo: EpisodicMemoryRepository,
    procedural_repo: ProceduralMemoryRepository,
    user_history_repo: UserHistoryRepositoryMeta
):
    """
    Creates a LangGraph agent with memory capabilities
    """
    # Create the workflow
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("analyze_memory", memory_type_node)  # Using our specialized tool
    workflow.add_node("query_memory", 
                     lambda state: query_memory(state, semantic_repo, episodic_repo, procedural_repo))
    workflow.add_node("rag_search", rag_search)
    workflow.add_node("add_to_context", add_to_context)
    workflow.add_node("generate_response", generate_response)
    workflow.add_node("store_memory", 
                     lambda state: store_memory(state, semantic_repo, episodic_repo, procedural_repo, user_history_repo))
    
    # Add edges
    workflow.add_edge(START, "analyze_memory")
    workflow.add_edge("analyze_memory", "query_memory")
    workflow.add_conditional_edges(
        "query_memory",
        check_relevant_data,
        {
            "rag_search": "rag_search",
            "add_to_context": "add_to_context"
        }
    )
    workflow.add_edge("rag_search", "generate_response")
    workflow.add_edge("add_to_context", "generate_response")
    workflow.add_edge("generate_response", "store_memory")
    workflow.add_edge("store_memory", END)
    
    # Compile the workflow
    return workflow.compile()