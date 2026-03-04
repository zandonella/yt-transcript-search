from elasticsearch import Elasticsearch
client = Elasticsearch('http://localhost:9200')

def search_transcripts(query, index_name):
    search_body = {
        "query": {
            "match": {
                "text": query
            }
        }
    }
    
    response = client.search(index=index_name, body=search_body)
    return response


if __name__ == "__main__":
    index_name = input("Enter the name of the Elasticsearch index to search: ")
    query = input("Enter your search query: ")
    
    response = search_transcripts(query, index_name)
    
    print(f"Total documents including the query: {len(response['hits']['hits'])}")
    for hit in response['hits']['hits']:
        print(f"Video ID: {hit['_source']['video_id']}, Start Time: {hit['_source']['start_time']}, End Time: {hit['_source']['end_time']}")
        print(f"Text: {hit['_source']['text']}\n")