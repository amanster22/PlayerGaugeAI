from flask import Flask, request, jsonify
from flask_cors import CORS
from rag_agent import get_agent_response

app = Flask(__name__)
CORS(app)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_query = data.get('query')
    
    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    print(f"🤖 Processing Query: {user_query}")
    
    answer = get_agent_response(user_query)
    
    return jsonify({
        "answer": answer,
        "sql_query": "Generated securely on backend"
    })

if __name__ == '__main__':
    print("🚀 Python AI Server running on http://localhost:5000")
    app.run(debug=True, port=5000)