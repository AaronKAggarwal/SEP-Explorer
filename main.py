from flask import Flask, render_template, request, redirect, url_for
import openai
import faiss
import numpy as np
import json
import os
import time


app = Flask(__name__)


# Load FAISS index and documents data
def load_faiss_index(index_path):
    return faiss.read_index(index_path)


def load_documents_data(documents_json_path):
    with open(documents_json_path, "r") as file:
        documents_data = json.load(file)
    return documents_data

# Generate an embedding for the search query using OpenAI's embedding model
# Should upgrade using asynchronous programming
def generate_query_embedding(query, openai_api_key, retries=3, backoff_factor=2):
    attempt = 0     # Retry logic with exponential backoff to handle rate limits or other errors
    while attempt < retries:
        try:
            openai.api_key = openai_api_key
            response = openai.Embedding.create(
                input=query,
                model="text-embedding-3-large"
            )
            embedding = np.array(response['data'][0]['embedding']).astype('float32')
            return embedding
        except openai.error.RateLimitError as e:
            print(f"Rate limit exceeded, retrying... Attempt {attempt + 1}")
            time.sleep((backoff_factor ** attempt))
        except openai.error.OpenAIError as e:
            print(f"OpenAI API error: {e}")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            break
        attempt += 1

# Search over FAISS index using embedded query
# Returns the distances and indexes of the top k closest documents
def search_faiss_index(query_embedding, faiss_index, top_k=12):
    distances, indices = faiss_index.search(np.array([query_embedding]), top_k)
    return distances[0], indices[0]



# Paths and keys
index_path = 'data/Stanford Plato train cleaned.index'
documents_json_path = 'data/Stanford Plato with all data.json'
openai_api_key = os.getenv('OPENAI_API_KEY')

faiss_index = load_faiss_index(index_path)
documents_data = load_documents_data(documents_json_path)

@app.route('/', methods=['GET', 'POST'])
def search():
    """
    Handles the search page
    On GET, display the search form
    On POST, redirect to the search results page for the given query
    """
    if request.method == 'POST':
        query = request.form['query']
        return redirect(url_for('search_results', query=query))
    return render_template('search.html')


@app.route('/search_results/<query>')
def search_results(query):
    """
    Display the search results for a given query
    This involves generating a query embedding, searching the FAISS index, and formatting results
    """
    query_embedding = generate_query_embedding(query, openai_api_key)
    distances, indices = search_faiss_index(query_embedding, faiss_index, top_k=12)

    results = []
    for idx, distance in zip(indices, distances):
        document = documents_data[idx]

        # Process the document preamble for display
        preamble = ' '.join(document['preamble']).replace('[', '').replace(']', '').replace('\\n', ' ').replace('\\',
                                                                                                                '').strip()
        preamble = ' '.join(preamble.split())  # Clean up whitespace

        result = {
            'title': document['title'],
            'url': f"https://plato.stanford.edu/entries/{document['shorturl']}",
            'snippet': preamble,
            'distance': distance
        }
        results.append(result)

    return render_template('search_results.html', results=results, query=query)

@app.route('/map')
def map():
    return render_template('map.html')


if __name__ == '__main__':
    app.run(debug=True) # Start the Flask application with debugging enabled
