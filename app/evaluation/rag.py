import json
import math
from pathlib import Path
from typing import Any

from app.rag.retrieval import Retriever


class RAGEvaluator:

    def __init__(
        self,
        retriever: Retriever | None = None,
    ) -> None:
        self.retriever = retriever or Retriever()

    def evaluate(
        self,
        dataset_path: str,
        k: int = 5,
    ) -> dict[str, Any]:

        path = Path(dataset_path)

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:
            dataset = json.load(file)

        recall_scores = []
        reciprocal_ranks = []
        ndcg_scores = []

        details = []

        for item in dataset:

            question = item["question"]
            expected_source = item["expected_source"]

            results = self.retriever.search(
                query=question,
                top_k=k,
            )

            sources = [
                result.source
                for result in results
            ]

            recall = self._recall_at_k(
                sources,
                expected_source,
            )

            reciprocal_rank = self._reciprocal_rank(
                sources,
                expected_source,
            )

            ndcg = self._ndcg_at_k(
                sources,
                expected_source,
            )

            recall_scores.append(recall)
            reciprocal_ranks.append(reciprocal_rank)
            ndcg_scores.append(ndcg)

            details.append(
                {
                    "id": item["id"],
                    "question": question,
                    "expected_source": expected_source,
                    "retrieved_sources": sources,
                    "recall_at_k": recall,
                    "reciprocal_rank": reciprocal_rank,
                    "ndcg_at_k": ndcg,
                }
            )

        return {
            "k": k,
            "recall_at_k": self._mean(recall_scores),
            "mrr": self._mean(reciprocal_ranks),
            "ndcg_at_k": self._mean(ndcg_scores),
            "details": details,
        }

    @staticmethod
    def _recall_at_k(
        sources: list[str],
        expected_source: str,
    ) -> float:

        return float(
            expected_source in sources
        )

    @staticmethod
    def _reciprocal_rank(
        sources: list[str],
        expected_source: str,
    ) -> float:

        for rank, source in enumerate(
            sources,
            start=1,
        ):
            if source == expected_source:
                return 1.0 / rank

        return 0.0

    @staticmethod
    def _ndcg_at_k(
        sources: list[str],
        expected_source: str,
    ) -> float:

        relevance = [
            1 if source == expected_source else 0
            for source in sources
        ]

        dcg = 0.0

        for rank, rel in enumerate(
            relevance,
            start=1,
        ):
            if rel > 0:
                dcg += rel / math.log2(rank + 1)

        ideal_relevance = sorted(
            relevance,
            reverse=True,
        )

        idcg = 0.0

        for rank, rel in enumerate(
            ideal_relevance,
            start=1,
        ):
            if rel > 0:
                idcg += rel / math.log2(rank + 1)

        if idcg == 0.0:
            return 0.0

        ndcg = dcg / idcg

        return min(ndcg, 1.0)

    @staticmethod
    def _mean(
        values: list[float],
    ) -> float:

        if not values:
            return 0.0

        return sum(values) / len(values)