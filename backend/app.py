import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)

# -----------------------------
# Load knowledge base
# -----------------------------
with open("docs.json", "r", encoding="utf-8") as f:
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
        return ["Hello 👋 How can I help you today?"]

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

    # Get top 5 relevant docs
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

        user_message = data.get("message", "")

        print("User:", user_message)

        # check small talk
        small_talk = handle_small_talk(user_message)

        if small_talk:
            return jsonify({"responses": small_talk})

        # retrieve knowledge
        results = search_similar(user_message)

        return jsonify({"responses": results})

    except Exception as e:

        print("SERVER ERROR:", e)

        return jsonify({"responses": ["Server error occurred"]})


# -----------------------------
# Health check route
# -----------------------------
@app.route("/")
def home():
    return jsonify({"message": "GenAI Chat Assistant Backend Running"})


# -----------------------------
# Run server
# -----------------------------
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port)