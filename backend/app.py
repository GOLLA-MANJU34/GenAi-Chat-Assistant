import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)

# -----------------------------
# Load documents
# -----------------------------
with open("docs.json", "r") as f:
    documents = json.load(f)

doc_texts = [doc["content"] for doc in documents]

# -----------------------------
# Create TF-IDF embeddings
# -----------------------------
vectorizer = TfidfVectorizer()
doc_vectors = vectorizer.fit_transform(doc_texts)

# -----------------------------
# Small talk handler
# -----------------------------
def handle_small_talk(message):

    message = message.lower().strip()

    greetings = ["hello", "hi", "hey"]
    thanks = ["thanks", "thank you"]
    goodbye = ["bye", "goodbye"]

    if message in greetings:
        return ["Hello 👋 How can I assist you today?"]

    if message in thanks:
        return ["You're welcome! Let me know if you need anything else."]

    if message in goodbye:
        return ["Goodbye! Have a great day."]

    return None


# -----------------------------
# Retrieve similar documents
# -----------------------------
def search_similar(query):

    query_vector = vectorizer.transform([query])

    similarities = cosine_similarity(query_vector, doc_vectors)

    top_indices = similarities.argsort()[0][-5:][::-1]

    results = [documents[i]["content"] for i in top_indices]

    return results


# -----------------------------
# Chat API
# -----------------------------
@app.route("/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json()

        user_message = data["message"]

        print("User:", user_message)

        # Check greetings
        small = handle_small_talk(user_message)

        if small:
            return jsonify({"responses": small})

        # RAG retrieval
        results = search_similar(user_message)

        return jsonify({"responses": results})

    except Exception as e:

        print("SERVER ERROR:", e)

        return jsonify({"responses": ["Server error occurred"]})


# -----------------------------
# Run server
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)