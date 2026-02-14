# test_rag_agent.py
from rag_agent import get_agent_response

def main():
    print("RAG Agent Terminal Chat. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        response = get_agent_response(user_input)
        print("Agent:", response)

if __name__ == "__main__":
    main()