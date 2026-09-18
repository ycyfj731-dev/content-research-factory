from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable


class SemanticEngineUnavailable(RuntimeError):
    pass


@dataclass(frozen=True)
class SemanticClusterResult:
    labels: list[int]
    probabilities: list[float | None]
    topic_info: list[dict[str, Any]]


class SentenceTransformerSimilarity:
    def __init__(
        self,
        model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    ) -> None:
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise SemanticEngineUnavailable(
                "sentence-transformers is not installed; install the 'semantic' extra"
            ) from exc

        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def similarity_matrix(self, texts: Iterable[str]):
        values = list(texts)
        if not values:
            return []
        embeddings = self.model.encode(values, normalize_embeddings=True)
        matrix = embeddings @ embeddings.T
        if hasattr(matrix, "tolist"):
            return matrix.tolist()
        return matrix


class BERTopicEngine:
    def __init__(
        self,
        *,
        language: str = "multilingual",
        min_topic_size: int = 5,
    ) -> None:
        try:
            from bertopic import BERTopic
        except ImportError as exc:
            raise SemanticEngineUnavailable(
                "bertopic is not installed; install the 'semantic' extra"
            ) from exc

        self.model = BERTopic(
            language=language,
            min_topic_size=min_topic_size,
            calculate_probabilities=True,
            verbose=False,
        )

    def fit(self, texts: Iterable[str]) -> SemanticClusterResult:
        docs = [str(text) for text in texts if str(text).strip()]
        if not docs:
            return SemanticClusterResult(labels=[], probabilities=[], topic_info=[])

        topics, probs = self.model.fit_transform(docs)
        probabilities: list[float | None] = []
        if probs is None:
            probabilities = [None] * len(topics)
        else:
            for index, topic in enumerate(topics):
                if topic == -1:
                    probabilities.append(None)
                    continue
                try:
                    probabilities.append(float(probs[index][topic]))
                except (IndexError, TypeError, ValueError):
                    try:
                        probabilities.append(float(max(probs[index])))
                    except Exception:
                        probabilities.append(None)

        info = self.model.get_topic_info()
        topic_info = info.to_dict(orient="records") if hasattr(info, "to_dict") else []
        return SemanticClusterResult(
            labels=[int(topic) for topic in topics],
            probabilities=probabilities,
            topic_info=topic_info,
        )
