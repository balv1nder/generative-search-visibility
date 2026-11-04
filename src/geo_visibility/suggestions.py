"""Prompt construction for meaning-preserving visibility suggestions."""
# prepares a possible edit to an article and supports comparing the original and edited versions under the same query.
from __future__ import annotations

import json
from dataclasses import dataclass

from .providers import LLMProvider, LLMRequest, LLMResponse
from .schema import QueryExample, SourceDocument

def build_suggestion_prompt(query: str, document: str) -> str:
    """Build a proposal prompt; its expected effect requires paired evaluation."""
    return (
        "Suggest a small, meaning-preserving edit to the source document that could make its "
        "relevant information clearer for answering the query. Do not add facts, statistics, "
        "citations, or claims absent from the source. Return JSON with 'rationale' and "
        "'revised_document' string fields. This is a hypothesis, not a prediction of visibility.\n"
        f"Query: {query}\n"
        f"Source document JSON: {json.dumps(document, ensure_ascii=False)}"
    )


@dataclass(frozen=True)
class ContentSuggestion:
    rationale: str
    revised_document: str
    model: str
    provider: str
    provider_version: str | None


def generate_suggestion(
    provider: LLMProvider,
    model: str,
    query: str,
    document: str,
    temperature: float = 0.0,
    top_p: float | None = None,
    seed: int | None = None,
) -> ContentSuggestion:
    response: LLMResponse = provider.generate(
        LLMRequest(
            prompt=build_suggestion_prompt(query, document),
            model=model,
            temperature=temperature,
            top_p=top_p,
            seed=seed,
            response_format="json",
        )
    )
    try:
        value = json.loads(response.text)
    except json.JSONDecodeError as error:
        raise ValueError(f"Suggestion response must be valid JSON: {error}") from error
    if not isinstance(value, dict):
        raise ValueError("Suggestion response must be a JSON object")
    rationale = value.get("rationale")
    revised_document = value.get("revised_document")
    if not isinstance(rationale, str) or not rationale.strip():
        raise ValueError("Suggestion response must include a non-empty rationale")
    if not isinstance(revised_document, str) or not revised_document.strip():
        raise ValueError("Suggestion response must include a non-empty revised_document")
    return ContentSuggestion(
        rationale=rationale.strip(),
        revised_document=revised_document.strip(),
        model=response.model,
        provider=response.provider,
        provider_version=response.provider_version,
    )


def replace_query_source(
    query: QueryExample, source_id: str, revised_document: str
) -> QueryExample:
    if not revised_document.strip():
        raise ValueError("revised_document must not be empty")
    if not any(source.id == source_id for source in query.sources):
        raise ValueError(f"Query {query.id!r} does not contain source {source_id!r}")
    revised_sources = tuple(
        SourceDocument(
            id=source.id,
            text=revised_document if source.id == source_id else source.text,
            title=source.title,
            url=source.url,
        )
        for source in query.sources
    )
    return QueryExample(id=query.id, query=query.query, sources=revised_sources)
