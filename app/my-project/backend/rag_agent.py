import os
import json
from dotenv import load_dotenv

# --- IMPORTS FOR SQL ---
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.agent_toolkits import create_sql_agent 
from langchain_openai import ChatOpenAI 

# --- IMPORTS FOR RAG ---
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# --- IMPORTS FOR TOOLS ---
from langchain_core.documents import Document  
from langchain_core.tools import Tool

# Load secrets
load_dotenv()

# --- CONFIGURATION ---
if not os.getenv("OPENAI_API_KEY"):
    print("❌ Error: OPENAI_API_KEY not found. Make sure .env is created or key is hardcoded.")

# 1. SETUP THE SQL TOOL (Left Brain - Logic/Stats)
db = SQLDatabase.from_uri("sqlite:///nba_dataV3.db")
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
sql_toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# 2. SETUP THE RAG TOOL (Right Brain - Text/Qualitative)
def load_and_vectorize_reports():
    """Reads the JSON file and creates a searchable vector store."""
    try:
        # Load the raw JSON data
        with open("analyst_reports.json", "r") as f:
            data = json.load(f)
        
        # Convert JSON objects into LangChain 'Documents'
        documents = []
        for item in data:
            text_content = (
                f"Player: {item['player_name']}\n"
                f"Rank: #{item['rank']}\n"
                f"Source: {item['source']}\n"
                f"Report: {item['summary']}"
            )
            doc = Document(
                page_content=text_content,
                metadata={"player": item['player_name'], "rank": item['rank']}
            )
            documents.append(doc)
            
        embeddings = OpenAIEmbeddings()
        vector_store = FAISS.from_documents(documents, embeddings)
        return vector_store.as_retriever()
    except Exception as e:
        print(f"⚠️ Warning: Could not load analyst reports. RAG disabled. Error: {e}")
        return None

retriever = load_and_vectorize_reports()

extra_tools = []
if retriever:
    def search_reports(query: str):
        # Using invoke for modern LangChain
        docs = retriever.invoke(query)
        return "\n\n".join([d.page_content for d in docs])

    rag_tool = Tool(
        name="search_analyst_reports",
        func=search_reports,
        description="Searches for qualitative scouting reports, player analysis, and expert opinions. Use this when asked 'Why', 'How', or about a player's playstyle."
    )
    extra_tools.append(rag_tool)

# 3. CREATE THE HYBRID AGENT
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=sql_toolkit,
    verbose=True,
    agent_type="openai-tools",
    extra_tools=extra_tools,
    handle_parsing_errors=True
)

# --- 🧠 MEMORY SYSTEM (NEW) ---
# A simple list to store the conversation
chat_history = []

def get_agent_response(user_query: str) -> str:
    """
    Takes a user question, adds context from previous chats, and returns the answer.
    """
    global chat_history
    
    try:
        # 1. Format the last 2 turns of conversation into a string
        # We limit it to 2 to keep the context clean and cheap
        history_text = ""
        for q, a in chat_history[-2:]:
            history_text += f"User: {q}\nAI: {a}\n"

        # 2. Inject this history into the Prompt
        prompt = (
            "You are an expert NBA Analyst with access to two tools:\n"
            "1. SQL Database: For exact stats, salaries, and salary predictions.\n"
            "2. Analyst Reports: For scouting reports, playstyles, and qualitative analysis.\n\n"
            "Important: Use the 'Conversation History' below to understand context (like 'he', 'him', 'that player').\n"
            f"Conversation History:\n{history_text}\n"
            "Strategy:\n"
            "- If asked for numbers (highest salary, ppg), use SQL.\n"
            "- If asked 'Why' (e.g., why is he undervalued?), use Analyst Reports.\n"
            "- If asked both, combine them.\n\n"
            f"Current User Question: {user_query}"
        )
        
        # 3. Get Response
        response = agent_executor.run(prompt)
        
        # 4. Save to Memory
        chat_history.append((user_query, response))
        
        return response
    except Exception as e:
        return f"Agent Error: {str(e)}"