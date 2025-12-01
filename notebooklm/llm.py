"""Lightweight summarization helpers."""

from __future__ import annotations

import math
import re
from collections import Counter
from typing import Iterable, List

SENTENCE_SPLIT = re.compile(r"(?<=[.!?]) +")
WORD_RE = re.compile(r"\b\w+\b")


def _tokenize(text: str) -> Iterable[str]:
    for match in WORD_RE.finditer(text.lower()):
        yield match.group(0)


def summarize(text: str, max_sentences: int = 3) -> List[str]:
    """Return a list of key sentences extracted from the text.

    The algorithm ranks sentences by TF-IDF-like weighting using
    per-sentence term frequency and inverse sentence frequency.
    """

    sentences = [s.strip() for s in SENTENCE_SPLIT.split(text) if s.strip()]
    if not sentences:
        return []

    sentence_tokens = [list(_tokenize(sentence)) for sentence in sentences]
    if not sentence_tokens:
        return []

    sentence_counts = [Counter(tokens) for tokens in sentence_tokens]
    document_frequency = Counter(token for tokens in sentence_tokens for token in set(tokens))
    num_sentences = len(sentences)

    def sentence_score(idx: int) -> float:
        tokens = sentence_tokens[idx]
        if not tokens:
            return 0.0
        tf_idf = 0.0
        for token in tokens:
            tf = sentence_counts[idx][token] / len(tokens)
            idf = math.log(num_sentences / (1 + document_frequency[token]))
            tf_idf += tf * idf
        return tf_idf

    ranked = sorted(range(num_sentences), key=sentence_score, reverse=True)
    selected = sorted(ranked[:max_sentences])
    return [sentences[i] for i in selected]
