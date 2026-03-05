from dotenv import load_dotenv
import os

load_dotenv()

from elasticsearch import Elasticsearch

client = Elasticsearch(
    hosts=[os.getenv("ELASTICSEARCH_URL")], api_key=os.getenv("ELASTIC_API_KEY")
)


def search_transcripts(query, index_name, size=10):
    search_body = {
        "size": size,
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
    }

    response = client.search(index=index_name, body=search_body)
    hits = response["hits"]["hits"]
    return hits


if __name__ == "__main__":
    index_name = input("Enter the name of the Elasticsearch index to search: ")
    query = input("Enter your search query: ")

    results = search_transcripts(query, index_name)

    print(f"Total documents including the query: {len(results)}")
    for hit in results:
        src = hit["_source"]
        t = int(src["start_seconds"])
        url = f"https://youtube.com/watch?v={src['video_id']}&t={t}s"
        print(f"[{hit['_score']:.2f}] {src['video_id']} @ {src['start_time']}")
        print(f"URL: {url}")
        print(f"Text: {src['text']}\n")
