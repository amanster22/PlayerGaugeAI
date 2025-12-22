import os
from dotenv import load_dotenv

# Validated imports for newest LangChain version
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.agent_toolkits import create_sql_agent 
from langchain_openai import ChatOpenAI 
# REMOVED the conflicting AgentType import

# Load secrets
load_dotenv()

# --- CONFIGURATION ---
# Ensure your API Key is loaded
if not os.getenv("OPENAI_API_KEY"):
    print("❌ Error: OPENAI_API_KEY not found. Make sure .env is created or key is hardcoded.")

# 1. Connect to the Database
db = SQLDatabase.from_uri("sqlite:///nba_dataV3.db")

# 2. Initialize the LLM
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

# 3. Create the Toolkit
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# 4. Create the Agent using a STRING instead of the imported class
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type="zero-shot-react-description",  # <--- WE CHANGED THIS to a string
    handle_parsing_errors=True
)

def get_agent_response(user_query: str) -> str:
    """
    Takes a user question, runs the SQL Agent, and returns the answer.
    """
    try:
        prompt = (
            "You are an expert NBA Data Analyst. "
            "You have access to a table 'player_data' with columns: "
            "PLAYER_NAME, TEAM_ABBREVIATION, SALARY, PREDICTED_SALARY, "
            "SALARY_DIFF, SALARY_PCT_CHANGE, PPG, RPG, APG. "
            "If asked about value, compare SALARY vs PREDICTED_SALARY. "
            f"User Question: {user_query}"
        )
        
        response = agent_executor.run(prompt)
        return response
    except Exception as e:
        return f"Agent Error: {str(e)}"