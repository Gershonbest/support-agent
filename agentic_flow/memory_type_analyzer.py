from typing import Dict, List, Any, Optional, TypedDict, Literal, Union
from langchain_core.tools import BaseTool, tool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
import re
import os
import sys
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

class MemoryType(BaseModel):
    """Type of memory to store in the chat."""
    memory_type: Literal["EPISODIC","SEMANTIC","PROCEDURAL","NONE"]
    confidence: float
    reasoning: str = Field(description="Brief explanation of why this memory type is most relevant")

class MemoryTypeAnalyzerTool(BaseTool):
    """Tool for analyzing which type of memory is needed for a user query."""
    
    name:str = "memory_type_analyzer"
    description:str = "Analyzes a user query to determine which type of memory (episodic, semantic, procedural) is most relevant"
    llm: Optional[ChatOpenAI] = None 
    prompt: Optional[ChatPromptTemplate] = None
    parser: Optional[JsonOutputParser] = None

    def __init__(self, llm=None):
        """Initialize the memory type analyzer tool."""
        super().__init__()
        self.llm = llm or ChatOpenAI(model="gpt-4o-mini", temperature=0)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """
            You are an AI memory classifier that determines which type of memory would be most useful for responding to a user query.
            
            Memory Types:
            - EPISODIC: Facts about specific past events, experiences, or interactions with this user.
              Examples: "What did we talk about last time?", "Do you remember when I told you about my dog?", "What was that restaurant I mentioned?"
            
            - SEMANTIC: General knowledge, facts, preferences about the user or user information that isn't tied to specific experiences.
              Examples: "What are my preferences?", "Do I like chocolate?", "What's my name?", "What's my job?"
              
            - PROCEDURAL: Step-by-step instructions, how-to knowledge, or skills about the user. 
              Examples: "How do I make pasta?", "What's the process for changing a tire?", "How should I prepare for an interview?"
              
            - NONE: General conversation that doesn't require accessing any specific memory type.
              Examples: "How are you today?", "Tell me a joke", "What's the weather like?"
              
            Analyze the user query and respond with a JSON object containing:
            1. The primary memory type needed (EPISODIC, SEMANTIC, PROCEDURAL, or NONE)
            2. A confidence score (0.0-1.0)
            3. A brief explanation of your reasoning
            

            """),
            ("user", "{query}")
        ])
    
    def _run(self, query: str) -> Dict[str, Any]:
        """Run the memory type analyzer on the user query."""
        try:
     
            chain = self.prompt | self.llm.with_structured_output(MemoryType)
            result = chain.invoke({"query": query})
            print(result)
            return result.model_dump()
        except Exception as e:
            return {
                "memory_type": "NONE",
                "confidence": 0.5,
                "reasoning": f"Error processing query: {str(e)}"
            }


# Function version using the @tool decorator
@tool
def analyze_memory_type(query: str) -> Dict[str, Any]:
    """
    Analyzes a user query to determine which type of memory (episodic, semantic, procedural) is most relevant.
    
    Args:
        query: The user's input message or query
        
    Returns:
        A dictionary with the memory type, confidence score, and reasoning
    """
    analyzer = MemoryTypeAnalyzerTool()
    return analyzer._run(query)


# Integrated version for LangGraph
def memory_type_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    LangGraph node that analyzes the user input to determine memory type.
    
    Args:
        state: The current state of the LangGraph
        
    Returns:
        Updated state with memory_type information
    """
    user_input = state.get("user_input", "")
    analyzer = MemoryTypeAnalyzerTool()
    result = analyzer._run(user_input)
    
    return {
        **state,
        "current_memory_type": result["memory_type"].lower(),
        "memory_type_confidence": result["confidence"],
        "memory_type_reasoning": result["reasoning"]
    }


# Usage example
if __name__ == "__main__":
    # Test with a few example queries
    test_queries = [
        # "What did we talk about last time?",
        # "Do I like chocolate?",
        # "How do I make pasta?",
        # "Tell me a joke",
        # "how do i make rice",
        "Remember when I told you about my job?",
        "My name is Gershon"
        "who is the president of America",
        "I got a new job",
    ]
    
    analyzer = MemoryTypeAnalyzerTool()
    
    for query in test_queries:
        result = analyzer._run(query)
        print(f"Query: '{query}'")
        print(f"Result: {result}")
        print(f"Memory Type: {result['memory_type']}")
        print(f"Confidence: {result['confidence']}")
        print(f"Reasoning: {result['reasoning']}")
        print("-" * 50)