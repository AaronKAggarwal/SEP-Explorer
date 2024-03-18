import openai
import json
import time
import os

openai.api_key = os.getenv('OPENAI_API_KEY')

# Load the cleaned and tokenised JSON data
input_file = 'data/Stanford Plato train cleaned.json'
with open(input_file, 'r') as file:
    articles = json.load(file)

embeddings_with_titles = []
tokens_per_minute_limit = 1000000
requests_per_minute_limit = 3000


# Function to estimate tokens
def estimate_tokens(text):
    return len(text) / 4


def can_make_request(tokens_required):
    return tokens_required <= tokens_per_minute_limit


# Initialising counters and timers for rate limiting
tokens_this_minute = 0
requests_this_minute = 0
start_time = time.time()

for article in articles:
    text = article['text']
    title = article['title']

    tokens_required = estimate_tokens(text)
    if not can_make_request(tokens_required):
        print(f"Skipping article {title} due to token limit per minute.")
        continue

    # Rate limiting based on tokens and requests per minute
    if tokens_this_minute + tokens_required > tokens_per_minute_limit or requests_this_minute >= requests_per_minute_limit:
        time_since_start = time.time() - start_time
        if time_since_start < 60:
            time.sleep(60 - time_since_start)
        # Reset counters and timer after waiting
        tokens_this_minute = 0
        requests_this_minute = 0
        start_time = time.time()

    # API call to generate embeddings
    try:
        response = openai.Embedding.create(
            input=text,
            model="text-embedding-3-large"
        )
        embedding = response['data'][0]['embedding']
        embeddings_with_titles.append({'title': title, 'embedding': embedding})
        tokens_this_minute += tokens_required
        requests_this_minute += 1
    except Exception as e:
        print(f"An error occurred: {e}")

# Save the embeddings to a JSON file
output_file = 'data/Stanford Plato train cleaned embedded.json'
with open(output_file, 'w') as file:
    json.dump(embeddings_with_titles, file)

print(f"Embeddings have been saved to '{output_file}'")
