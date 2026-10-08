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

**Status: not obtained.** Which subset, in what format, and when, is an open supervisor question —
see `TODO.md`. [DOSSIER] states the dataset is public on Hugging Face at `GEO-Optim/geo-bench`;
**we have not verified this and the brief gives no location.**

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

LLM responses are cached on disk, keyed by a hash of (model, prompt, parameters). The cache is
git-ignored but is **the most expensive artefact in the project** — it represents real API spend
against a limited budget. Back it up outside the repository, and never delete it casually.

## Rules

- **Never commit raw data, processed data, caches, or credentials.**
- Record provenance for every dataset: where it came from, when, which version, under what licence.
- Every processed artefact must be regenerable from `raw/` plus a config in `experiments/configs/`.
- Record the git commit alongside any dataset used to produce a reported result.
- If data is shared between teammates, share it out-of-band and document the method here — do not
  work around `.gitignore`.
