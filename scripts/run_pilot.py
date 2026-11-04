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

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "src"))

from geo_visibility.pilot import run_pilot  # noqa: E402
from geo_visibility.providers import CachedProvider, OllamaConfig, OllamaProvider  # noqa: E402
from geo_visibility.schema import DatasetColumns, load_dataset  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--dataset", type=Path, help="Override dataset_path in the config")
    parser.add_argument("--output", type=Path, help="Override output_path in the config")
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
    args = parser.parse_args()
    with args.config.open("rb") as file:
        config = tomllib.load(file)

    repo_root = Path.cwd()
    dataset_path = args.dataset or repo_root / config["dataset_path"]
    output_path = args.output or repo_root / config["output_path"]
    cache_dir = repo_root / config.get("cache_dir", ".llm_cache")
    columns = DatasetColumns(**config.get("columns", {}))
    queries = load_dataset(dataset_path, columns, max_rows=args.max_input_rows)
    ollama_config = OllamaConfig.from_env()
    provider = CachedProvider(OllamaProvider(ollama_config), cache_dir)
    query_limit = (
        args.query_limit
        if args.query_limit is not None
        else int(config.get("query_limit", 24))
    )
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
    result = {
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
        "seed": int(config.get("seed", 20261104)),
        "temperature": float(config.get("temperature", 0.0)),
        "top_p": float(config["top_p"]) if "top_p" in config else None,
        "provider": "ollama",
        "model": ollama_config.model,
        "selected_query_ids": selected_query_ids,
        "answers": answers,
        "records": records,
        "summary": {
            "queries": len(selected_query_ids),
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
        },
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], indent=2))
    print(f"Saved pilot output to {output_path}")


if __name__ == "__main__":
    main()
