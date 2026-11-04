# Understanding and Optimizing Content Visibility in Generative Search Engines

**MSc AI Lab Project — Project 11 (P11)**

Generative search engines and conversational assistants retrieve information from many sources
and generate a direct answer, citing only a small subset of what they read. This project studies
that selection step: it builds a controlled generative search pipeline, uses it to produce
labelled `(query, document)` citation data, and trains models to predict and explain which
documents get cited.

## Supervisor

**Yannick Le Cacheux** — Manifold Technology, and lecturer at CentraleSupélec
(`yannick.le-cacheux@centralesupelec.fr` / `lecacheux@manifold.fr`)

## Institution and programme

CentraleSupélec — **MSc in Artificial Intelligence**, Lab Project (Project 11).

## Research objective

As stated in the project brief:

> Build and evaluate models predicting the visibility of a document within a generative search engine.

The brief frames three research questions:

1. Can we predict whether a document will be selected or cited for a given query?
2. Which characteristics of the query and document are the most predictive?
3. Can such a predictive model subsequently be used to automatically suggest or generate better content?

This sits within the emerging area of **Generative Engine Optimization (GEO)**, which studies how
online content can be adapted to improve its visibility within generative search systems.

## Current status

**Foundation phase.** The repository now has a bounded, config-driven GEO pilot scaffold:
dataset normalization, paper-defined objective impression metrics, a provider-neutral generation
interface with an optional local Ollama adapter, caching, and focused tests. It is not yet a
validated reproduction or a trained predictive baseline.

One one-query engineering smoke test completed using a GEO-bench checkout and Ollama
`llama3.2:3b` available on the user's machine. The dataset was read-only outside this worktree;
the generated result is ignored and not included in this patch.

The immediate next step remains clarifying the blocking questions with the supervisor — which
GEO dataset subset will be provided, what starter code already exists, and which LLM should be
used. These are tracked in `TODO.md`; the scaffold deliberately does not settle those decisions.

**No research result or contribution is claimed.** The smoke test only verifies that the local
pipeline runs end to end.

## Running the bounded local pilot

`experiments/configs/pilot.toml` maps the GEO-bench JSONL schema inspected for this pilot
(`query`, and `sources` containing `cleaned_text` and `url`; IDs are assigned by row/source
position). The pilot rejects limits above 50 queries and defaults to 24 source-bearing queries.
It requires a running local Ollama service and an explicitly configured model tag; it never
downloads a model. The recorded rank is the source order supplied by the dataset, not a rank
produced by a new retriever; this scaffold does not compute retrieval scores.

```sh
export GEO_OLLAMA_MODEL='llama3.2:3b'  # or another model already installed in Ollama
PYTHONPATH=src python scripts/run_pilot.py \
  --config experiments/configs/pilot.toml \
  --dataset /path/to/geo-bench/test.jsonl \
  --query-limit 1 \
  --max-input-rows 1 \
  --source-char-limit 1000 \
  --output experiments/results/geo-pilot-tiny.json
```

The output and response cache are git-ignored. The pipeline records citation rate and per-source
Word Count (WC) and Position-Adjusted Word Count (PAWC); it does not calculate the paper's
subjective impression scores. WC and PAWC follow Aggarwal et al., *GEO: Generative Engine
Optimization*, KDD '24, DOI [10.1145/3637528.3671900](https://doi.org/10.1145/3637528.3671900).
The implementation counts whitespace-delimited tokens and uses zero-based sentence positions;
those operational conventions are explicit in `src/geo_visibility/metrics.py`.
The Ollama adapter looks up and records the model digest; cache keys include that digest so a
changed model build does not silently reuse prior outputs.

For JSONL inputs, `--max-input-rows` bounds reading before parsing all records, and `--dataset`,
`--query-limit`, and `--output` override their config values. `--source-char-limit` bounds each
source passage in the prompt for a quick smoke test; the output records whether source content was
truncated and saves the raw model answer plus parsed cited source IDs.

Content suggestions are only hypotheses. `generate_suggestion` requests a meaning-preserving edit
and `replace_query_source` applies it to a query's source set; rerun the same seeded pilot and use
`compare_pilot_outputs` for paired metric differences. Review meaning preservation and run
repeated, controlled baseline/revision generations before making any causal claim.

Run focused tests with:

```sh
PYTHONPATH=src python -m unittest discover -s tests -v
```

## High-level methodology

The project brief organises the work into **five levels of increasing difficulty**, and states
explicitly that students are *not* expected to investigate every extension — the research
direction is selected according to first experimental results, progress and the team's interests.

1. **Literature and reproduction** — study the relevant literature; reproduce a simplified
   generative-engine pipeline and GEO evaluation protocol.
2. **Experimental dataset** — build a dataset associating queries, candidate documents, retrieval
   information and citation/visibility outcomes. Running the pipeline over queries generates its
   own supervised labels.
3. **Interpretable baseline** — predict document visibility from manually designed features such
   as semantic similarity, document length, retrieval score and ranking position, using standard
   machine-learning algorithms.
4. **Analysis** — identify which document and query properties influence visibility.
5. **At least one advanced direction** — for example separating retrieval probability from
   citation probability, comparing classical ML with transformer- or LLM-based models,
   automatically optimising document content, testing robustness to query paraphrases, or
   measuring whether conclusions transfer across generative models.

Comparison against real commercial generative engines is described in the brief as an optional
extension rather than a requirement.

**Stack:** Python, scikit-learn, PyTorch, Hugging Face Transformers. LLMs are used through APIs
or locally hosted models. The brief states that no prior expertise in LLMs or information
retrieval is required.

## Repository structure

```
generative-search-visibility/
├── README.md               This file
├── CLAUDE.md               Instructions for Claude sessions working on this repository
├── PROJECT_CONTEXT.md      What the project is — the shared source of truth
├── RESEARCH_PLAN.md        Staged plan; what is essential vs. optional
├── DECISIONS.md            Decision log with evidence
├── TODO.md                 Tasks and outstanding supervisor questions
│
├── docs/
│   ├── project-brief/      The official P11 brief and a faithful summary of it
│   └── literature/         Reading list, per-paper notes, priorities
│
├── data/
│   ├── raw/                Source datasets (git-ignored)
│   ├── processed/          Derived features and datasets (git-ignored)
│   └── README.md           Provenance, schema, and how to regenerate
│
├── src/
│   ├── retrieval/          Indexing and retrieval; records score and rank
│   ├── generation/         LLM answer generation with source citations
│   ├── citation/           Parsing which documents were actually cited — the labelling step
│   ├── features/           Feature engineering for the visibility models
│   ├── models/             Predictive models and baselines
│   └── geo_visibility/     Normalized data, metrics, providers and bounded pilot
│
├── experiments/
│   ├── configs/            Experiment configurations — experiments are config-driven
│   ├── results/            Outputs, tagged with the commit and config that produced them
│   └── notebooks/          Exploratory analysis
│
├── scripts/                Entry points and utilities
├── tests/                  Focused unit tests
└── reports/                Analysis write-ups, figures, final report material
```

## Reproducibility philosophy

Reproducible experiments and code are a **named deliverable** of this project, not an afterthought.

- **Experiments are config-driven.** Every run is defined by a file in `experiments/configs/`,
  never by edited constants.
- **Everything that affects a result is recorded**: random seeds, model names *and* versions,
  LLM sampling parameters, and the git commit that produced each result.
- **All LLM responses are cached** on disk, keyed by a hash of (model, prompt, parameters). This
  makes reruns free, protects a limited API budget, and keeps results reproducible even when a
  provider's endpoint changes underneath us.
- **Cost is estimated before it is spent.** The project has a limited LLM API budget, which is
  the real constraint on experimental scale; no API-spending experiment runs without a written
  estimate first.
- **Stochasticity is reported, not hidden.** LLM citation behaviour varies between runs, so
  results are reported over repeated runs with the number of repetitions stated, and the
  measured label-noise ceiling is reported alongside model accuracy.
- **Secrets are never committed.** Credentials live in a git-ignored `.env`; only variable names
  are tracked, in `.env.example`.
- **Raw data is not committed.** `data/README.md` documents how to obtain and regenerate it.

## A note on sources

Two source documents inform this repository, with different authority, and the distinction is
maintained throughout:

- The **official project brief** written by the supervisor — authoritative. Summarised in
  `docs/project-brief/P11-summary.md`.
- A separate **analytical dossier** covering all of the programme's lab projects — useful, but
  third-party interpretation that was not written by the supervisor.

Project documents tag statements as **[BRIEF]**, **[DOSSIER]**, **[INFERENCE]**,
**[RECOMMENDATION]** or **[UNSPECIFIED]** so that a reader can always tell a requirement from an
opinion. Anything not specified in the source documents is marked as such rather than filled in.

## About

This is an **MSc AI Lab project** — a supervised student research project, not a production
system and not a published research contribution. It is work in progress.
