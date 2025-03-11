import os
from pathlib import Path
from dotenv import load_dotenv
import sys
import logging


# load_dotenv()
# WORKDIR=os.getenv("WORKDIR")
# os.chdir(WORKDIR)
# sys.path.append(WORKDIR)

from langchain_core.tools import tool
from typing import Literal
import pandas as pd
import json
from langchain_community.tools.tavily_search import TavilySearchResults

from src.validators.agent_validators import *
from src.vector_database.vector_db import PineconeManagment
from src.models import format_retrieved_docs


pinecone_conn = PineconeManagment()
pinecone_conn.loading_vdb(index_name="supportbot")

websearch_tool = TavilySearchResults(max_results=2)


@tool
def retrieve_faq_info(question: str):
    """
    Retrieves information about the HappyAI platform from relevant documents.

    Use this tool to answer queries about HappyAI, such as:
    - "What are HappyAI's main services?"
    - "How long has HappyAI been operating?"
    - "What is HappyAI's expertise?"

    Parameters:
        question (str): The query about HappyAI to look up

    Returns:
        Information retrieved from the RAG chain based on the query
    """
    logging.info("Searching for revelant document from Vector database..")
    retriever = pinecone_conn.vdb.as_retriever(
        search_type="similarity", search_kwargs={"k": 1}
    )
    rag_chain = retriever | format_retrieved_docs
    return rag_chain.invoke(question)


@tool
def perform_web_search(query: str) -> str:
    """
    Performs a web search to find relevant information.

    Parameters:
        query (str): The search query

    Returns:
        A list of titles from the web search results
    """
    logging.info("Performing web search..")
    results = websearch_tool.run(query)
    return "\n\n".join(result["title"] for result in results)


@tool
def addision(number_1: int, number_2: int):
    """
    Performs addition of two numbers.

    Parameters:
        number_1 (int): The first number
        number_2 (int): The second number

    Returns:
        The sum of the two numbers
    """
    logging.info("Performing addition..")
    return number_1 + number_2


@tool
def multiplication(number_1: int, number_2: int):
    """
    Performs multiplication of two numbers.

    Parameters:
        number_1 (int): The first number
        number_2 (int): The second number

    Returns:
        The product of the two numbers
    """
    logging.info("Performing multiplication..")
    return number_1 * number_2
