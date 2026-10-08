# CLAUDE.md — Instructions for Claude sessions on this repository

## Read this first

Before undertaking any substantial work on this project, **read these four files**:

1. `PROJECT_CONTEXT.md` — what the project is, what the brief says, what is unspecified
2. `RESEARCH_PLAN.md` — the staged plan and where we currently are
3. `DECISIONS.md` — decisions already taken, with their evidence
4. `TODO.md` — current actionable tasks and outstanding supervisor questions

Do not reconstruct project knowledge from conversation context. These files exist precisely so
that project understanding does not depend on any single conversation.

## What this project is

**Project 11 (P11) — "Understanding and Optimizing Content Visibility in Generative Search Engines"**

An MSc AI Lab project at CentraleSupélec. Generative search engines (ChatGPT, Claude, Gemini,
Perplexity) retrieve many sources and cite only a few. This project builds a *controlled*
generative search pipeline, uses it to generate labelled `(query, document, retrieved?, cited?)`
data, and trains models to predict and explain which documents get cited — and, optionally, to
suggest content modifications that improve visibility while preserving meaning.

**Research objective** (from the brief): *build and evaluate models predicting the visibility of
a document within a generative search engine.*

**Supervisor:** Yannick Le Cacheux — Manifold Technology, and lecturer at CentraleSupélec
(`yannick.le-cacheux@centralesupelec.fr` / `lecacheux@manifold.fr`).

This is a **collaborative** project. Changes you make will be read by teammates who were not
present for the conversation that produced them. Write for that audience.

## How to behave on this project

### The dossier and the brief are the primary sources for requirements

Two source documents exist, and they do **not** have equal authority:

- **`docs/project-brief/P11 - Lab project - ....docx`** — the official brief written by the
  supervisor. **Authoritative.** `docs/project-brief/P11-summary.md` is a faithful summary of it.
- **The *MSc AI Lab Project Dossier* PDF** — a 212-page analytical companion document covering
  all 15 lab projects (P11 is on pp. 63–69 and 167–171). It quotes the brief accurately, but the
  large majority of its P11 content is **its own analysis, roadmap, experiment proposals, metric
  choices and risk assessment**. It was **not written by the supervisor** and carries no
  authority over project requirements.

Do not invent or assume project requirements that are not supported by these documents. If a
requirement is not in the brief, it is not a requirement.

### Always distinguish source facts from inference and recommendation

Use the labels established in `PROJECT_CONTEXT.md` in all project documents and in your replies:

- **[BRIEF]** — stated in the official project brief
- **[DOSSIER]** — stated in the dossier's P11 analysis (third-party interpretation)
- **[INFERENCE]** — our reading, not stated
- **[RECOMMENDATION]** — our proposal, no authority
- **[UNSPECIFIED]** — "Not specified in the project dossier — clarify with supervisor."

Never silently fill a gap with general knowledge. When something is not specified, say so
explicitly and route it to the supervisor-questions section of `TODO.md`.

### Never fabricate academic citations

Do not produce a paper title, author list, venue, year, arXiv ID or DOI unless you have verified
it from a source in this repository or from a document you have actually read in this session.
If you are not certain of a bibliographic detail, write the detail you are certain of and mark
the rest as unverified. A plausible-looking fake citation in an MSc report is a serious problem.

`docs/literature/README.md` records which bibliographic details are verified against the brief
and which came from the dossier and still need checking against the actual papers.

### Persist important project knowledge in repository files

If a session establishes something that matters beyond that session — a decision, a measured
result, a supervisor answer, a changed constraint — write it to the appropriate file:

| Kind of knowledge | Goes in |
|---|---|
| A decision and why it was taken | `DECISIONS.md` |
| A change to what we know the project requires | `PROJECT_CONTEXT.md` |
| A change to the plan or its staging | `RESEARCH_PLAN.md` |
| A new task or a resolved question | `TODO.md` |
| A supervisor answer | `PROJECT_CONTEXT.md` (update the fact) **and** `DECISIONS.md` (record it as evidence) |
| Experimental findings | `experiments/results/` and `reports/` |

Knowledge that exists only in a conversation is lost knowledge.

### Expensive LLM/API experiments require a cost estimate first

The project has a stated budget of **approximately $500** for LLM API usage. That is the real
binding constraint — not compute, not storage.

**Before running any experiment that makes LLM API calls, produce a written cost estimate** and
put it in the experiment's config or in `experiments/configs/`. State:
- number of API calls
- estimated input and output tokens per call
- the model and its per-token price
- total estimated cost, and cumulative spend to date against the $500

Default to the cheapest viable path: run on a small subset first, cache every response, make
reruns free. Never launch a full-scale run that has not been costed and dry-run on a sample.
If an estimate exceeds roughly 10% of the remaining budget in one go, ask the user before running.

### Experiments must be reproducible

Reproducibility is a **named deliverable** in the brief, not a nicety.

- Every experiment is driven by a config file in `experiments/configs/`, not by edited constants.
- Set and record random seeds. Record model names *and* versions/snapshots — LLM endpoints drift.
- Record the LLM sampling parameters (temperature, top-p, seed if supported) for every run.
- **Cache all LLM responses to disk**, keyed by a hash of (model, prompt, parameters). This makes
  reruns free, protects the budget, and makes results reproducible even if an endpoint changes.
- Log the exact git commit for every result written to `experiments/results/`.
- Pin dependency versions.
- Because LLM citation behaviour is stochastic, prefer reporting over repeated runs with a
  stated number of repetitions rather than single-run numbers.

### Never commit API keys or secrets

- Secrets live in `.env`, which is git-ignored. Never create a tracked file containing a key.
- Never hard-code a key in source, a notebook, a config or a log.
- Never print a key to stdout or paste one into a commit message, an issue or a report.
- Before committing, check that no key, token or credential is in the diff.
- If a key is ever committed, say so immediately and clearly — it must be rotated, not just removed.

### Do not begin implementation until the research scope is sufficiently understood

This project is **explicitly staged**, and the brief states that students are *not* expected to
investigate all extensions, and that the research direction will be chosen based on first
experimental results. Premature implementation of an advanced direction is wasted work.

Specifically:
- Do not start building until the Phase 0 supervisor questions in `TODO.md` that block a given
  piece of work have been answered — in particular which dataset subset is provided, what
  initial code already exists, and which LLM to use.
- Do not rebuild something the supervisor has offered to provide. Ask first.
- Advanced directions (content optimisation, cross-model transfer, commercial-engine comparison)
  are **optional**. Do not treat them as committed scope. Do not start them before the
  interpretable baseline and its analysis exist.
- When unsure whether something is in scope, check `RESEARCH_PLAN.md` and ask rather than build.

### Working style

- Prefer small, reviewable changes with clear commit messages.
- Keep `src/` importable and config-driven; keep exploratory work in `experiments/notebooks/`
  and promote it into `src/` once it stabilises.
- Raw data is git-ignored; document how to obtain and regenerate it in `data/README.md`.
- When you report a result, report it faithfully, including when it is negative or inconclusive.
  A finding that content features add nothing beyond retrieval rank is a legitimate result and
  must not be dressed up.
