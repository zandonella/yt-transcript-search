import numpy as np
import json
from collections import defaultdict

CATEGORIES = {
    "algorithm": [
        "binary search",
        "topological sort",
        "dijkstra algorithm",
        "breadth first search",
        "union find",
    ],
    "concept": [
        "dynamic programming",
        "greedy algorithm",
        "sliding window",
        "two pointer",
        "backtracking",
    ],
    "problem": [
        "stock span",
        "longest substring",
        "merge sorted lists",
        "lowest common ancestor",
        "scheduling problem",
    ],
}


def dcg(relevances):
    return sum(rel / np.log2(rank + 1) for rank, rel in enumerate(relevances, start=1))


def ndcg(relevances):
    actual = dcg(relevances)
    ideal = dcg(sorted(relevances, reverse=True))
    return actual / ideal if ideal > 0 else 0.0


def compute_ndcg(annotated_file):
    with open(annotated_file, "r") as f:
        data = json.load(f)

    scores = {}
    for entry in data:
        query = entry["query"]
        rels = [r["relevance"] for r in entry["results"]]
        scores[query] = ndcg(rels)

    return scores


if __name__ == "__main__":
    annotated_file = input("Enter the path to the annotated file: ")
    scores = compute_ndcg(annotated_file)

    print("\nNDCG Scores:")
    for query, score in scores.items():
        print(f"{query}: {score:.4f}")

    category_scores = defaultdict(list)
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in scores:
                category_scores[category].append(scores[keyword])
    print("\nAverage NDCG Scores by Category:")
    for category, vals in category_scores.items():
        avg_score = np.mean(vals) if vals else 0.0
        print(f"{category}: {avg_score:.4f}")

    print("\nOverall Average NDCG Score:")
    overall_avg = np.mean(list(scores.values())) if scores else 0.0
    print(f"Overall: {overall_avg:.4f}")
