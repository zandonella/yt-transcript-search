from dotenv import load_dotenv
import os

load_dotenv()

from elasticsearch import Elasticsearch
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/search": {"origins": "http://localhost:5173"}})

client = Elasticsearch(
    hosts=[os.getenv("ELASTICSEARCH_URL")], api_key=os.getenv("ELASTIC_API_KEY")
)


def build_search_query(query, size):
    query_terms = query.split()
    is_short_query = len(query_terms) <= 3

    default_clauses = [
        # Exact phrase on unstemmed field
        {"match_phrase": {"text.exact": {"query": query, "boost": 5}}},
        # Phrase on stemmed field
        {"match_phrase": {"text": {"query": query, "slop": 2, "boost": 3}}},
        # Match title exact phrase
        {"match_phrase": {"video_title": {"query": query, "boost": 2.5}}},
        # Match title bag of words
        {"match": {"video_title": {"query": query, "operator": "or", "boost": 1.2}}},
    ]

    if is_short_query:
        # For short queries, also add a bag-of-words match on the text to increase recall
        default_clauses.append(
            {"match": {"text": {"query": query, "operator": "and", "boost": 1.5}}}
        )
    else:
        default_clauses.append(
            {
                "match": {
                    "text": {
                        "query": query,
                        "minimum_should_match": "75%",
                        "boost": 1.2,
                    }
                }
            }
        )

    return {
        "size": size,
        "explain": True,
        "query": {
            "bool": {
                "should": default_clauses,
                "minimum_should_match": 1,
            }
        },
        "highlight": {
            "pre_tags": ["<hl>"],
            "post_tags": ["</hl>"],
            "fields": {
                "text": {
                    "number_of_fragments": 1,
                    "fragment_size": 160,
                },
                "video_title": {},
            },
        },
    }


def search_transcripts(query, index_name, size=30):
    search_body = build_search_query(query, size)

    response = client.search(index=index_name, body=search_body)
    hits = response["hits"]["hits"]
    results = []
    for hit in hits:
        src = hit["_source"]
        t = int(src["start_seconds"])
        url = f"https://youtube.com/watch?v={src['video_id']}&t={t}s"

        highlighted_text = None
        if "highlight" in hit and "text" in hit["highlight"]:
            highlighted_text = hit["highlight"]["text"][0]

        highlighted_title = None
        if "highlight" in hit and "video_title" in hit["highlight"]:
            highlighted_title = hit["highlight"]["video_title"][0]

        results.append(
            {
                "score": hit["_score"],
                "video_id": src["video_id"],
                "start_time": src["start_time"],
                "end_time": src["end_time"],
                "start_seconds": src["start_seconds"],
                "end_seconds": src["end_seconds"],
                "text": src["text"],
                "highlighted_text": highlighted_text,
                "highlighted_title": highlighted_title,
                "url": url,
                "video_title": src["video_title"],
            }
        )
    return results


@app.get("/search")
def search():
    query = request.args.get("q", "").strip()
    index_name = request.args.get("index", "").strip()
    size = request.args.get("size", default=10, type=int)

    if not query:
        return jsonify({"error": "Missing query parameter: q"}), 400

    if not index_name:
        return jsonify({"error": "Missing query parameter: index"}), 400

    try:
        results = search_transcripts(query, index_name, size=size)
        return jsonify(
            {
                "query": query,
                "index": index_name,
                "count": len(results),
                "results": results,
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run()
