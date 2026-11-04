# Data

**No data is present in this repository yet.** Nothing here has been obtained, generated or
verified. This file documents what we expect, and what must be recorded once data exists.

Everything in `raw/` and `processed/` is **git-ignored**. Data is reproduced from its source and
from the pipeline, never from version control.

## Layout

```
data/
├── raw/        Source datasets as obtained, unmodified. Git-ignored.
└── processed/  Derived datasets and features produced by our code. Git-ignored.
```

Keep `raw/` immutable: never edit a file in place. Everything derived belongs in `processed/` and
must be regenerable by running code in `src/` against `raw/`.

## Expected source data

**GEO-bench** — [BRIEF] the project "will build upon existing research on GEO, in particular
GEO-bench, a benchmark containing **10,000 queries and associated web sources**."

[BRIEF] "A subset of existing GEO datasets and benchmarks will be provided or identified at the
beginning of the project."

**Status:** a local GEO-bench checkout outside this worktree was inspected for a one-query smoke
run; it was not copied or modified. The files include `train.jsonl`, `val.jsonl`, and
`test.jsonl`; the inspected test rows have a `query` string and five `sources` with
`cleaned_text` and `url`. There are no explicit query or source IDs, so the pilot assigns
row/source-position IDs. Whether this is the supervisor-provided subset and which split should be
used for research remain supervisor questions — see `TODO.md`. [DOSSIER] gives a public dataset
location; the brief itself does not.

The pilot loader accepts one query per row in JSON, JSONL, or CSV. The inspected GEO-bench split
uses `query` and a `sources` array of objects containing `cleaned_text` and `url`; it has no
explicit query/source IDs, so stable row/source-position IDs are generated. These fields are
mapped in `experiments/configs/pilot.toml`. Use `--max-input-rows` for a JSONL smoke test without
reading the whole file. For another delivered subset, inspect it and update the mapping; do not
download or transform the full benchmark as part of a smoke test.

**Licence and redistribution terms: [UNSPECIFIED].** Confirm before publishing any derived
dataset or including source documents in a report.

## Expected generated data

[BRIEF] Level 2 of the project requires "an experimental dataset associating queries, candidate
documents, retrieval information and citation/visibility outcomes."

Running the pipeline over queries produces one record per `(query, document)` pair. The planned
schema — to be finalised when the pipeline is built:

| Field | Description |
|---|---|
| `query_id`, `query` | From the source benchmark |
| `doc_id`, `doc` | Candidate document identifier and content reference |
| `retrieved` | Whether the document entered the generator's context |
| `rank` | Retrieval rank *[BRIEF names "ranking position" as a baseline feature]* |
| `retrieval_score` | Retriever score *[BRIEF names "retrieval score" as a baseline feature]* |
| `cited` | Whether the generated answer cited this document — **the label** |
| `retriever`, `retriever_version` | Reproducibility |
| `llm_model`, `llm_version` | Reproducibility — endpoints drift |
| `temperature`, `top_p`, `seed` | Sampling parameters |
| `run_id`, `repetition` | Supports the label-stability study |
| `timestamp`, `git_commit` | Provenance |

[DOSSIER] estimates the scale at roughly 10⁵ labelled pairs for 10,000 queries × 5–10 candidates,
a few GB with embeddings — small in storage terms. **The binding constraint is LLM API calls, not
data volume.**

## LLM response cache

LLM responses are cached on disk, keyed by a hash of provider, model tag, prompt, and sampling
parameters. The cache is git-ignored but is **the most expensive artefact in the project** — it
represents real API spend against a limited budget. Back it up outside the repository, and never
delete it casually.

The local pilot uses an Ollama model tag configured through `GEO_OLLAMA_MODEL` and writes cache
entries under `.llm_cache/`. The provider-neutral interface is in `src/geo_visibility/providers.py`;
the Ollama adapter does not select or download a model automatically and records the model digest.

## Rules

- **Never commit raw data, processed data, caches, or credentials.**
- Record provenance for every dataset: where it came from, when, which version, under what licence.
- Every processed artefact must be regenerable from `raw/` plus a config in `experiments/configs/`.
- Record the git commit alongside any dataset used to produce a reported result.
- If data is shared between teammates, share it out-of-band and document the method here — do not
  work around `.gitignore`.
