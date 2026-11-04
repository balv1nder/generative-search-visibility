"""Objective GEO impression metrics and paired-output comparisons."""
# reads the answer and its citations, then calculates WC and PAWC.
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable, Mapping


@dataclass(frozen=True)
class SentenceAttribution:
    text: str
    source_ids: tuple[str, ...]
    citation_field_missing: bool = False


@dataclass(frozen=True)
class ImpressionScores:
    word_count: float
    position_adjusted_word_count: float


def _word_count(text: str) -> int:
    # Whitespace-delimited tokens are a transparent operationalization of |s|.
    return len(text.split())


def score_impressions(
    sentences: Iterable[SentenceAttribution], source_ids: Iterable[str]
) -> dict[str, ImpressionScores]:
    """Compute GEO Word Count and Position-Adjusted Word Count per source.

    Sentence position is zero-based response order; a sentence attributed to
    multiple sources contributes an equal share to each. These conventions are
    made explicit because the paper's formulas do not prescribe a tokenizer or
    indexing convention.
    """
    sentence_list = list(sentences)
    source_list = list(source_ids)
    if len(source_list) != len(set(source_list)):
        raise ValueError("source_ids must be unique")
    valid_sources = set(source_list)
    total_words = sum(_word_count(sentence.text) for sentence in sentence_list)
    total_sentences = len(sentence_list)
    word_scores = {source_id: 0.0 for source_id in source_list}
    position_scores = {source_id: 0.0 for source_id in source_list}

    for position, sentence in enumerate(sentence_list):
        if not sentence.text.strip():
            raise ValueError("sentence text must not be empty")
        cited_sources = tuple(dict.fromkeys(sentence.source_ids))
        unknown_sources = set(cited_sources) - valid_sources
        if unknown_sources:
            raise ValueError(f"Unknown cited source ids: {sorted(unknown_sources)}")
        if not cited_sources:
            continue
        words = _word_count(sentence.text)
        share = words / len(cited_sources)
        adjusted_share = share * math.exp(-position / total_sentences)
        for source_id in cited_sources:
            word_scores[source_id] += share
            position_scores[source_id] += adjusted_share

    if total_words:
        return {
            source_id: ImpressionScores(
                word_count=word_scores[source_id] / total_words,
                position_adjusted_word_count=position_scores[source_id] / total_words,
            )
            for source_id in source_list
        }
    return {
        source_id: ImpressionScores(word_count=0.0, position_adjusted_word_count=0.0)
        for source_id in source_list
    }


def paired_visibility_changes(
    baseline: Iterable[Mapping[str, object]],
    revised: Iterable[Mapping[str, object]],
) -> list[dict[str, object]]:
    """Compare paired query/source outputs; this measures change, not causality."""
    key_fields = ("query_id", "doc_id")
    metric_fields = ("word_count", "position_adjusted_word_count")

    def index(rows: Iterable[Mapping[str, object]]) -> dict[tuple[object, object], Mapping[str, object]]:
        indexed: dict[tuple[object, object], Mapping[str, object]] = {}
        for row in rows:
            key = (row.get(key_fields[0]), row.get(key_fields[1]))
            if None in key:
                raise ValueError("each visibility row must include query_id and doc_id")
            if key in indexed:
                raise ValueError(f"duplicate query/source pair: {key!r}")
            indexed[key] = row
        return indexed

    baseline_by_pair = index(baseline)
    revised_by_pair = index(revised)
    if baseline_by_pair.keys() != revised_by_pair.keys():
        raise ValueError("baseline and revised outputs must contain identical query/source pairs")

    changes: list[dict[str, object]] = []
    for key in baseline_by_pair:
        change: dict[str, object] = {
            "query_id": key[0],
            "doc_id": key[1],
        }
        for metric in metric_fields:
            old_value = baseline_by_pair[key].get(metric)
            new_value = revised_by_pair[key].get(metric)
            if not isinstance(old_value, (int, float)) or not isinstance(new_value, (int, float)):
                raise ValueError(f"paired rows must contain numeric {metric!r} values")
            delta = float(new_value) - float(old_value)
            change[f"{metric}_delta"] = delta
            change[f"{metric}_relative_change_pct"] = (
                None if old_value == 0 else delta / float(old_value) * 100
            )
        changes.append(change)
    return changes
