#!/usr/bin/env python3
"""Run the locally configured, query-capped GEO pilot."""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
import sys
import tomllib
from typing import Mapping

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "src"))

from geo_visibility.pilot import run_pilot  # noqa: E402
from geo_visibility.providers import (  # noqa: E402
    CachedProvider,
    LLMRequest,
    OllamaConfig,
    OllamaProvider,
)
from geo_visibility.schema import DatasetColumns, QueryExample, load_dataset  # noqa: E402


def _summary(records: list[dict[str, object]], query_count: int) -> dict[str, object]:
    return {
        "queries": query_count,
        "source_records": len(records),
        "cited_rate": (
            sum(bool(record["cited"]) for record in records) / len(records)
            if records
            else 0.0
        ),
        "mean_word_count": (
            sum(float(record["word_count"]) for record in records) / len(records)
            if records
            else 0.0
        ),
        "mean_position_adjusted_word_count": (
            sum(float(record["position_adjusted_word_count"]) for record in records)
            / len(records)
            if records
            else 0.0
        ),
    }


def _write_json_atomic(path: Path, result: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_name(path.name + ".tmp")
    temporary_path.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    temporary_path.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--dataset", type=Path, help="Override dataset_path in the config")
    parser.add_argument("--output", type=Path, help="Override output_path in the config")
    parser.add_argument("--cache-dir", type=Path, help="Override cache_dir in the config")
    parser.add_argument(
        "--query-id",
        help="Run only this query ID (useful for isolating a slow input row)",
    )
    parser.add_argument("--query-limit", type=int, help="Override the configured query limit")
    parser.add_argument(
        "--max-input-rows",
        type=int,
        help="Read at most this many rows (useful for a tiny smoke test)",
    )
    parser.add_argument(
        "--source-char-limit",
        type=int,
        help="Truncate each source to this many characters in the model prompt",
    )
    parser.add_argument(
        "--ollama-timeout-seconds",
        type=float,
        help="Override the Ollama request timeout in seconds (default: config value or 600)",
    )
    parser.add_argument(
        "--max-output-tokens",
        type=int,
        help="Maximum tokens generated per answer (default: config value or 512)",
    )
    args = parser.parse_args()
    with args.config.open("rb") as file:
        config = tomllib.load(file)

    repo_root = Path.cwd()
    dataset_path = args.dataset or repo_root / config["dataset_path"]
    output_path = args.output or repo_root / config["output_path"]
    cache_dir = args.cache_dir or repo_root / config.get("cache_dir", ".llm_cache")
    columns = DatasetColumns(**config.get("columns", {}))
    queries = load_dataset(dataset_path, columns, max_rows=args.max_input_rows)
    if args.query_id is not None:
        queries = [query for query in queries if query.id == args.query_id]
        if not queries:
            raise ValueError(
                f"Query ID {args.query_id!r} was not found in the loaded dataset rows"
            )
    ollama_config = OllamaConfig.from_env()
    ollama_timeout_seconds = (
        args.ollama_timeout_seconds
        if args.ollama_timeout_seconds is not None
        else float(config.get("ollama_timeout_seconds", 600.0))
    )
    max_output_tokens = (
        args.max_output_tokens
        if args.max_output_tokens is not None
        else int(config.get("max_output_tokens", 512))
    )
    provider = CachedProvider(
        OllamaProvider(ollama_config, timeout_seconds=ollama_timeout_seconds),
        cache_dir,
    )
    query_limit = (
        args.query_limit
        if args.query_limit is not None
        else int(config.get("query_limit", 24))
    )
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    git_status = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    metadata: dict[str, object] = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "git_commit": commit,
        "dataset_path": str(dataset_path.resolve()),
        "git_worktree_dirty": bool(git_status.strip()),
        "query_limit": query_limit,
        "max_input_rows": args.max_input_rows,
        "source_char_limit": (
            args.source_char_limit
            if args.source_char_limit is not None
            else config.get("source_char_limit")
        ),
        "max_output_tokens": max_output_tokens,
        "ollama_timeout_seconds": ollama_timeout_seconds,
        "seed": int(config.get("seed", 20261104)),
        "temperature": float(config.get("temperature", 0.0)),
        "top_p": float(config["top_p"]) if "top_p" in config else None,
        "provider": "ollama",
        "model": ollama_config.model,
    }
    partial_output_path = output_path.with_name(output_path.name + ".partial")
    checkpoint_written = False

    def log_query_start(query: QueryExample, request: LLMRequest) -> None:
        is_cached = provider.is_cached(request)
        status = "cache hit" if is_cached else "generating"
        print(
            f"{status}: query {query.id} with {len(query.sources)} sources "
            f"({len(request.prompt)} prompt characters)",
            flush=True,
        )

    def save_checkpoint(
        records: list[dict[str, object]],
        completed_query_ids: list[str],
        answers: list[dict[str, object]],
    ) -> None:
        nonlocal checkpoint_written
        checkpoint = {
            **metadata,
            "status": "in_progress",
            "completed_queries": len(completed_query_ids),
            "selected_query_ids": completed_query_ids,
            "answers": answers,
            "records": records,
            "summary": _summary(records, len(completed_query_ids)),
        }
        _write_json_atomic(partial_output_path, checkpoint)
        checkpoint_written = True
        print(
            f"Checkpoint saved after query {completed_query_ids[-1]}: "
            f"{partial_output_path}",
            flush=True,
        )

    try:
        records, selected_query_ids, answers = run_pilot(
            queries=queries,
            provider=provider,
            model=ollama_config.model,
            query_limit=query_limit,
            seed=int(config.get("seed", 20261104)),
            temperature=float(config.get("temperature", 0.0)),
            top_p=float(config["top_p"]) if "top_p" in config else None,
            source_char_limit=(
                args.source_char_limit
                if args.source_char_limit is not None
                else config.get("source_char_limit")
            ),
            max_output_tokens=max_output_tokens,
            on_query_start=log_query_start,
            on_query_complete=save_checkpoint,
        )
    except Exception:
        if checkpoint_written:
            print(
                f"Run stopped; completed-query checkpoint is at {partial_output_path}",
                file=sys.stderr,
            )
        raise

    result = {
        **metadata,
        "status": "complete",
        "completed_queries": len(selected_query_ids),
        "selected_query_ids": selected_query_ids,
        "answers": answers,
        "records": records,
        "summary": _summary(records, len(selected_query_ids)),
    }
    _write_json_atomic(output_path, result)
    partial_output_path.unlink(missing_ok=True)
    print(json.dumps(result["summary"], indent=2))
    print(f"Saved pilot output to {output_path}")


if __name__ == "__main__":
    main()
