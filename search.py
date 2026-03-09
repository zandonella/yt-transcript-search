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


def search_transcripts(query, index_name, size=30):
    search_body = {
        "size": size,
        "explain": True,
        "query": {
            "bool": {
                "should": [
                    # Exact phrase on unstemmed field — highest signal
                    {"match_phrase": {"text.exact": {"query": query, "boost": 4}}},
                    # Phrase on stemmed field — good for morphological variants
                    {"match_phrase": {"text": {"query": query, "boost": 2}}},
                    # Bag of words fallback — recall
                    {
                        "match": {
                            "text": {"query": query, "fuzziness": "AUTO", "boost": 1}
                        }
                    },
                ]
            }
        },
        "highlight": {
            "pre_tags": ["<hl>"],
            "post_tags": ["</hl>"],
            "fields": {
                "text": {
                    "number_of_fragments": 1,
                    "fragment_size": 160,
                }
            },
        },
    }

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
