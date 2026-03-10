import requests
import json

ENDPOINT_URL = "http://localhost:5000/search"
INDEX = "neetcode-250"
K = 10

QUERIES = [
    "binary search",
    "topological sort",
    "dijkstra algorithm",
    "breadth first search",
    "union find",
    "dynamic programming",
    "greedy algorithm",
    "sliding window",
    "two pointer",
    "backtracking",
    "stock span",
    "longest substring",
    "merge sorted lists",
    "lowest common ancestor",
    "scheduling problem",
]


def fetch_and_export(output_json="to_annotate.json"):
    data = []
    for query in QUERIES:
        resp = requests.get(
            ENDPOINT_URL, params={"q": query, "size": K, "index": INDEX}
        )
        response = resp.json()
        for rank, result in enumerate(response["results"], start=1):
            result["rank"] = rank
            result["relevance"] = None
        data.append(response)
    with open(output_json, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Exported {len(data)} queries to {output_json}")


if __name__ == "__main__":
    fetch_and_export()
