"""Input normalization for query/source datasets."""
# checks that the input rows have the fields the program
# expects, such as a query and source text.
from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from itertools import islice
from pathlib import Path
from typing import Any, Mapping


@dataclass(frozen=True)
class DatasetColumns:
    """Column names for one-query-per-row JSON, JSONL, or CSV input."""

    query_id: str | None = "query_id"
    query: str = "query"
    sources: str = "sources"
    source_id: str | None = "id"
    source_text: str = "text"
    source_title: str | None = "title"
    source_url: str = "url"


@dataclass(frozen=True)
class SourceDocument:
    id: str
    text: str
    title: str | None = None
    url: str | None = None


@dataclass(frozen=True)
class QueryExample:
    id: str
    query: str
    sources: tuple[SourceDocument, ...]


def _read_rows(path: Path, max_rows: int | None = None) -> list[Mapping[str, Any]]:
    suffix = path.suffix.lower()
    if suffix == ".jsonl":
        rows: list[Mapping[str, Any]] = []
        with path.open(encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                if not line.strip():
                    continue
                if max_rows is not None and len(rows) >= max_rows:
                    break
                try:
                    row = json.loads(line)
                except json.JSONDecodeError as error:
                    raise ValueError(f"{path}:{line_number}: invalid JSON: {error}") from error
                if not isinstance(row, dict):
                    raise ValueError(f"{path}:{line_number}: each JSONL row must be an object")
                rows.append(row)
        return rows

    if suffix == ".json":
        with path.open(encoding="utf-8") as file:
            value = json.load(file)
        if not isinstance(value, list) or not all(isinstance(row, dict) for row in value):
            raise ValueError(f"{path}: JSON input must be an array of objects")
        return value if max_rows is None else value[:max_rows]

    if suffix == ".csv":
        with path.open(encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            return list(reader if max_rows is None else islice(reader, max_rows))

    raise ValueError(f"Unsupported dataset format {suffix!r}; use .json, .jsonl, or .csv")


def _required_text(row: Mapping[str, Any], key: str, where: str) -> str:
    value = row.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{where}: {key!r} must be a non-empty string")
    return value.strip()


def _required_id(row: Mapping[str, Any], key: str, where: str) -> str:
    value = row.get(key)
    if isinstance(value, bool) or not isinstance(value, (str, int)):
        raise ValueError(f"{where}: {key!r} must be a non-empty string or integer")
    normalized = str(value).strip()
    if not normalized:
        raise ValueError(f"{where}: {key!r} must be a non-empty string or integer")
    return normalized


def _optional_text(row: Mapping[str, Any], key: str) -> str | None:
    value = row.get(key)
    if value is None or value == "":
        return None
    if not isinstance(value, str):
        raise ValueError(f"{key!r} must be a string when provided")
    return value.strip() or None


def load_dataset(
    path: str | Path,
    columns: DatasetColumns = DatasetColumns(),
    max_rows: int | None = None,
) -> list[QueryExample]:
    """Load query rows and normalize their nested source records.

    The raw GEO-bench schema is intentionally not assumed; callers can map its
    field names after the provided subset and format have been confirmed.
    """
    dataset_path = Path(path)
    if not dataset_path.is_file():
        raise FileNotFoundError(f"Dataset file does not exist: {dataset_path}")
    if max_rows is not None and max_rows < 1:
        raise ValueError("max_rows must be positive when provided")

    queries: list[QueryExample] = []
    seen_query_ids: set[str] = set()
    for row_number, row in enumerate(_read_rows(dataset_path, max_rows), start=1):
        where = f"{dataset_path}:row {row_number}"
        query_id = (
            _required_id(row, columns.query_id, where)
            if columns.query_id
            else f"query-{row_number}"
        )
        query = _required_text(row, columns.query, where)
        if query_id in seen_query_ids:
            raise ValueError(f"{where}: duplicate query id {query_id!r}")
        seen_query_ids.add(query_id)

        raw_sources = row.get(columns.sources)
        if isinstance(raw_sources, str):
            try:
                raw_sources = json.loads(raw_sources)
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"{where}: {columns.sources!r} must contain a JSON array: {error}"
                ) from error
        if not isinstance(raw_sources, list):
            raise ValueError(f"{where}: {columns.sources!r} must be an array of source objects")

        sources: list[SourceDocument] = []
        seen_source_ids: set[str] = set()
        for source_number, raw_source in enumerate(raw_sources, start=1):
            source_where = f"{where}, source {source_number}"
            if not isinstance(raw_source, dict):
                raise ValueError(f"{source_where}: source must be an object")
            source_id = (
                _required_id(raw_source, columns.source_id, source_where)
                if columns.source_id
                else f"source-{source_number}"
            )
            source_text = _required_text(raw_source, columns.source_text, source_where)
            if source_id in seen_source_ids:
                raise ValueError(f"{source_where}: duplicate source id {source_id!r}")
            seen_source_ids.add(source_id)
            sources.append(
                SourceDocument(
                    id=source_id,
                    text=source_text,
                    title=(
                        _optional_text(raw_source, columns.source_title)
                        if columns.source_title
                        else None
                    ),
                    url=_optional_text(raw_source, columns.source_url),
                )
            )
        queries.append(QueryExample(id=query_id, query=query, sources=tuple(sources)))
    return queries
