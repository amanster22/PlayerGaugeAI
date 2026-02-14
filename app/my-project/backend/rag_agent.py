import os
import json
from dotenv import load_dotenv

from langchain_community.agent_toolkits import SQLDatabaseToolkit, create_sql_agent
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.vectorstores import FAISS

from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document


# ----------------------------
# Load Environment
# ----------------------------
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# ----------------------------
# Paths
# ----------------------------
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "nba_dataV3.db")
db_uri = f"sqlite:///{db_path}"


# ----------------------------
# Global LLM (Completion Model)
# ----------------------------
llm = OpenAI(temperature=0)


# ----------------------------
# Quantitative Agent (SQL) - Cached
# ----------------------------
_quantitative_agent_cache = None

def create_quantitative_agent():
    global _quantitative_agent_cache

    if _quantitative_agent_cache is None:
        db = SQLDatabase.from_uri(db_uri)
        sql_toolkit = SQLDatabaseToolkit(db=db, llm=llm)

        _quantitative_agent_cache = create_sql_agent(
            llm=llm,
            toolkit=sql_toolkit,
            verbose=False,
            handle_parsing_errors=True
        )

    return _quantitative_agent_cache


# ----------------------------
# Qualitative Agent (RAG)
# ----------------------------
def load_and_vectorize_reports():
    json_path = os.path.join(base_dir, "analyst_reports.json")

    with open(json_path, "r") as f:
        data = json.load(f)

    documents = [
        Document(
            page_content=(
                f"Player: {item['player_name']}\n"
                f"Rank: #{item['rank']}\n"
                f"Source: {item['source']}\n"
                f"Report: {item['summary']}"
            ),
            metadata={"player": item['player_name']}
        )
        for item in data
    ]

    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(documents, embeddings)
    return vector_store.as_retriever()


rag_retriever = load_and_vectorize_reports()

qualitative_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are an expert NBA analyst.

Use the analyst reports below to answer the question qualitatively.

Reports:
{context}

Question:
{question}

Answer:
"""
)

def qualitative_agent_fn(question):
    try:
        docs = rag_retriever.invoke(question)
        context = "\n\n".join([doc.page_content for doc in docs])

        prompt = qualitative_prompt.format(
            context=context,
            question=question
        )

        response = llm.invoke(prompt)
        return response
    except Exception as e:
        print("RAG ERROR:", str(e))
        return "Qualitative analysis unavailable."


# ----------------------------
# Summarizer Agent
# ----------------------------
summarizer_prompt = PromptTemplate(
    input_variables=["sql_answer", "rag_answer", "question"],
    template="""
You are a senior NBA analyst.

User Question:
{question}

Quantitative Data:
{sql_answer}

Qualitative Analysis:
{rag_answer}

Provide a clear, well-structured final answer that combines both insights.
"""
)

def summarizer_agent(question, sql_answer=None, rag_answer=None):
    try:
        response = llm.invoke(
            summarizer_prompt.format(
                question=question,
                sql_answer=sql_answer or "Not used.",
                rag_answer=rag_answer or "Not used."
            )
        )
        return response
    except Exception as e:
        print("SUMMARIZER ERROR:", str(e))
        return "An error occurred while generating the final response."


# ----------------------------
# Orchestrator Agent
# ----------------------------

# IMPORTANT: Short schema to prevent token explosion
schema = """
Table: player_data

Columns:
PLAYER_NAME
PTS
REB
AST
TEAM
AGE
GP
"""


orchestrator_prompt = PromptTemplate(
    input_variables=["schema", "question"],
    template="""
You are an expert NBA system orchestrator.

You have access to:

1. SQL Database for 2024-2025 NBA season (stats, contracts, numeric data)
Schema:
{schema}

2. Analyst Reports (qualitative scouting)

Rules:
- Use SQL if stats/numbers are needed.
- Use RAG if scouting/playstyle analysis is needed.
- Use BOTH if both are required.
- Use UNABLE if the question is outside scope.

Respond ONLY with one word:
SQL
RAG
BOTH
UNABLE

Question:
{question}

Tool:
"""
)


def orchestrator_agent(question):
    raw_decision = llm.invoke(
        orchestrator_prompt.format(
            schema=schema,
            question=question
        )
    )

    decision = str(raw_decision).strip().upper()
    print("Decision:", repr(decision))

    sql_answer = None
    rag_answer = None

    if decision == "SQL":
        try:
            quantitative_agent = create_quantitative_agent()
            sql_response = quantitative_agent.invoke({"input": question})
            sql_answer = sql_response["output"]
        except Exception as e:
            print("SQL FAILED:", str(e))
            return "I attempted to retrieve statistical data but encountered an internal error."

    elif decision == "RAG":
        rag_answer = qualitative_agent_fn(question)

    elif decision == "BOTH":
        try:
            quantitative_agent = create_quantitative_agent()
            sql_response = quantitative_agent.invoke({"input": question})
            sql_answer = sql_response["output"]
        except Exception as e:
            print("SQL FAILED:", str(e))
            sql_answer = "Statistical data unavailable due to query failure."

        rag_answer = qualitative_agent_fn(question)

    elif decision == "UNABLE":
        return (
            "I'm unable to determine the appropriate data source "
            "for this question. Please rephrase or ask about "
            "specific NBA stats or player analysis."
        )

    else:
        return f"Tool routing failed. Model returned: {decision}"

    return summarizer_agent(question, sql_answer, rag_answer)


# ----------------------------
# Public Function
# ----------------------------
def get_agent_response(user_query):
    return orchestrator_agent(user_query)
