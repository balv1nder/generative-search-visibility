# RESEARCH_PLAN.md

Staged research plan for **P11 — Understanding and Optimizing Content Visibility in Generative
Search Engines**.

Labelling follows `PROJECT_CONTEXT.md`: **[BRIEF]** = in the official brief; **[DOSSIER]** =
from the dossier's third-party P11 analysis; **[INFERENCE]** / **[RECOMMENDATION]** = ours;
**[UNSPECIFIED]** = not specified in the project dossier, clarify with supervisor.

## The one structural fact that governs this plan

[BRIEF] The brief organises the work into **five levels of increasing difficulty** and states
explicitly:

> "These extensions are deliberately open-ended: students are not expected to investigate all of
> them. The exact research direction will be selected according to the first experimental
> results, progress and interests of the team."

**Therefore this plan deliberately does not commit to completing every advanced direction.**
Phases 1–5 map to the brief's own levels and are **essential**. Phase 6 is a menu from which
the brief requires **at least one** item. Phase 7 is delivery.

## Essential vs. optional at a glance

| Phase | Maps to brief level | Status |
|-------|---------------------|--------|
| 0 — Supervisor clarification | not in brief; [RECOMMENDATION] | **Essential, blocking** |
| 1 — Literature review | Level 1 (first half) | **Essential** |
| 2 — Reproduction / baseline pipeline | Level 1 (second half) | **Essential** |
| 3 — Experimental dataset and evaluation protocol | Level 2 | **Essential** |
| 4 — Baseline modelling | Level 3 | **Essential — this is the project's core** |
| 5 — Analysis | Level 4 | **Essential** |
| 6 — Advanced research directions | Level 5 | **At least one required; the rest optional** |
| 7 — Final experiments and reporting | Deliverables | **Essential** |

[UNSPECIFIED] No timeline, start date, end date or interim deadline is given in the brief. The
week numbers below come from the dossier's suggested roadmap and are **indicative only** until
the real schedule is confirmed — see `TODO.md`.

---

## Phase 0 — Supervisor clarification

**Not in the brief.** [RECOMMENDATION] This phase exists because several things the brief offers
("a subset of existing GEO datasets will be provided", "initial code examples can be provided")
have no concrete form yet, and because building the wrong thing is cheap to avoid now and
expensive to discover later.

**Blocking outputs needed before Phase 2 can start:**
- Which GEO dataset subset is provided, in what format, when. Is `GEO-Optim/geo-bench` the
  intended source? [BRIEF names GEO-bench; the HF path is DOSSIER-sourced and unverified]
- What initial code exists, so we do not rebuild it. [BRIEF offers it]
- Which LLM the controlled pipeline should use — commercial API or locally hosted open model.
  This drives cost and reproducibility. [UNSPECIFIED]
- How the $500 budget is accessed, and whether it is per project or per student. [BRIEF states
  the amount only]

**Non-blocking but direction-setting:** publication aims, whether the intervention experiment is
in scope, priority between predictive model and content-optimisation system, open-sourcing,
dual-use discussion, team size, timeline and assessment.

Full question list: `TODO.md` → *Supervisor Questions*.

**Exit criterion:** the four blocking items above are answered, and the answers are written into
`PROJECT_CONTEXT.md` and `DECISIONS.md`.

**Work that can proceed in parallel without waiting:** Phase 1 literature review, repository
scaffolding, and reading GEO-bench's public documentation.

---

## Phase 1 — Literature review

[BRIEF] Level 1: "Study the relevant literature."

**Core, named in the brief (highest priority):**
- Aggarwal et al., *GEO: Generative Engine Optimization*, KDD 2024 — the foundational paper and
  the source of GEO-bench.
- Liu, Zhang, Liang et al., *Evaluating Verifiability in Generative Search Engines*,
  Findings of the ACL, 2023.

[BRIEF] "Additional recent literature on generative search, retrieval, learning-to-rank and
LLM-based evaluation will be investigated during the project." — so the brief explicitly
anticipates going beyond these two, in those four areas.

**[DOSSIER] suggests additionally**: Lewis et al. (RAG), Karpukhin et al. (DPR), Nogueira & Cho
(BERT re-ranking), Gao et al. (ALCE), Burges (LambdaMART), Thakur et al. (BEIR). See
`docs/literature/README.md` for what we need from each and the priority assigned.

**[DOSSIER]** also notes that GEO is fast-moving and that checking for recent follow-up work is
part of week one. [RECOMMENDATION] Do a targeted novelty check early: what has been published on
GEO since Aggarwal et al.? This bounds what counts as a contribution.

**Outputs:** `docs/literature/` populated with per-paper notes; a short synthesis of what the GEO
evaluation protocol and "visibility metrics" actually are in the published work; a novelty-check
note.

**Exit criterion:** we can state, in our own words, what GEO-bench contains, how Aggarwal et al.
measure visibility, and what the gap is that our work addresses.

---

## Phase 2 — Reproduction / baseline pipeline

[BRIEF] Level 1: "reproduce a simplified version of an existing generative-engine pipeline and
GEO evaluation protocol."

[BRIEF] The pipeline, as described: given a user query and a collection of candidate documents,
retrieve relevant documents and use an LLM to generate a grounded answer with source citations.

**Components to build** (`src/retrieval`, `src/generation`, `src/citation`):
1. **Retrieval** — index the candidate documents, retrieve top-k for a query, record retrieval
   score and rank. [BRIEF names "retrieval score or ranking position" as features, so these must
   be recorded.] [DOSSIER recommends BM25 + a dense retriever; [UNSPECIFIED] in the brief.]
2. **Generation** — prompt an LLM with the retrieved documents, obtain a grounded answer with
   inline source citations.
3. **Citation parsing** — parse which candidate documents the answer actually cited. This is the
   step that manufactures the labels, so its correctness gates everything downstream.
4. **Response caching** — [RECOMMENDATION] cache every LLM response keyed by
   (model, prompt, parameters). Protects the budget and makes reruns reproducible.

**Reproduction target:** a subset of existing GEO results and visibility metrics. [BRIEF]
**Which** subset and metrics is [UNSPECIFIED] — Phase 0 question 5.

[DOSSIER] rationale worth adopting: "If your pipeline does not reproduce known effects, your
labels are suspect."

**Exit criterion:** an end-to-end run on a small query subset produces
`(query, document, retrieved?, rank, retrieval_score, cited?)` records, within a known and
documented cost per query.

**[RECOMMENDATION] Get one complete low-quality end-to-end run as early as possible**, before any
component is polished. It exposes integration problems while there is still time to fix them.

---

## Phase 3 — Experimental dataset and evaluation protocol

[BRIEF] Level 2: "Build an experimental dataset associating queries, candidate documents,
retrieval information and citation/visibility outcomes."

**Dataset construction:**
- Scale the pipeline run across GEO-bench queries, within budget.
- Record, per `(query, document)` pair: retrieval information (score, rank, retriever used),
  citation outcome, generation metadata (model, version, temperature, seed, timestamp), and the
  commit that produced it.
- Document the schema in `data/README.md`; keep raw records in `data/raw/`, derived features in
  `data/processed/`.

**Evaluation protocol — define it before modelling.** [RECOMMENDATION]
- Decide train/validation/test splits. [RECOMMENDATION] **Split by query, not by pair** — the
  same query's candidate documents are not independent, and a random pair-level split leaks.
- Fix the metric set in advance. [DOSSIER proposes AUC-ROC, average precision, calibration,
  NDCG/MRR, and lift over a rank-only baseline. The brief does not name metrics — [UNSPECIFIED].]
- Define the **rank-only control baseline** now. [DOSSIER argues this is the single most
  important comparator: it answers whether content matters at all beyond retrieval position.]

**Label-stability study.** [INFERENCE — not in the brief, but the supervised framing depends on it]
Run the same queries repeatedly at fixed sampling parameters and measure how stable citation
decisions are. If citation is highly stochastic, there is an accuracy ceiling no model can
exceed, and every later result must be read against it. [DOSSIER flags this as "the risk most
likely to be discovered too late" and recommends doing it around week five, not week twenty.]

**Exit criterion:** a documented, versioned dataset; a written evaluation protocol in
`experiments/configs/`; a measured label-noise ceiling.

---

## Phase 4 — Baseline modelling

[BRIEF] Level 3: "Design and evaluate an interpretable ML baseline predicting document
visibility." **This is the core ML task of the project** and the brief is explicit that it should
be accessible with standard ML concepts.

**Features — those named in the brief:** semantic similarity, document length, retrieval score,
ranking position. [BRIEF] [RECOMMENDATION] Extend with other cheap, interpretable content
features (readability, presence of statistics/quotations/citations, structure), noting that any
feature beyond the four named is our addition.

**Models — [BRIEF] "standard machine-learning algorithms".** [DOSSIER suggests logistic
regression and gradient boosting.]

**Controls:** the rank-only baseline, plus a trivial majority-class baseline.

**Exit criterion:** a trained, evaluated interpretable baseline with the agreed metrics, reported
against the rank-only control, with the label-noise ceiling stated alongside.

---

## Phase 5 — Analysis

[BRIEF] Level 4: "Analyze the model and identify which document/query properties influence
visibility."

- Feature importances and partial-dependence / marginal-effect analysis.
- [DOSSIER suggests SHAP and permutation importance.]
- Answer the brief's second research question directly: *which characteristics of the query and
  document are the most predictive?*
- Report the lift over the rank-only baseline prominently.

**[INFERENCE] Be honest about the correlational limit.** Everything in this phase is
correlational. Claims of the form "documents with X get cited more" are associations within our
pipeline, not causal claims and not necessarily claims about commercial engines. Phase 6's
intervention direction is what would change that.

**Exit criterion:** a written analysis answering research question 2, with figures, stated
limitations, and an explicit statement of what the analysis cannot support.

---

## Phase 6 — Advanced research directions

[BRIEF] Level 5: "Investigate **at least one** more advanced research direction." The brief lists
five possible extensions and states that students are **not** expected to investigate all of them.

**The five extensions named in the brief**, with our read on each:

| # | Extension [BRIEF] | Our read |
|---|---|---|
| A | **Separating retrieval probability from citation probability** | [RECOMMENDATION] **Strongest default choice.** Structurally correct (a document must be retrieved before it can be cited), directly answers a mechanism question, and is cheap — it reuses the Phase 3 dataset with no additional API spend. [DOSSIER calls it "the cleanest structural idea available in this project".] |
| B | **Comparing classical ML with transformer- or LLM-based models** | Moderate cost, moderate insight. Natural second choice. Cross-encoders over (query, document); learning-to-rank. [DOSSIER] |
| C | **Automatically optimizing document content** | [BRIEF] frames this as "may serve as the basis for". Highest value *if* it works, and the only direction that produces causal evidence: rewrite → rerun pipeline → measure citation change. Requires a semantic-preservation check to honour the brief's "preserving its original meaning" constraint. **Most API-expensive.** |
| D | **Robustness to query paraphrases** | Cheap-ish, self-contained, good report material. |
| E | **Transfer across generative models** | Answers whether findings are about LLMs or about *one* LLM. Doubles generation cost for the queries tested. |

**[BRIEF] Optional, explicitly not a requirement:** comparison against existing commercial
generative engines. Treat as a stretch item only.

**[RECOMMENDATION] Selection strategy:** commit to **A** first (cheapest, highest structural
value, no new API spend). Choose the second direction *after* seeing Phase 4–5 results and after
checking remaining budget — which is exactly what the brief says to do. Do not pre-commit to C
or E before the budget position is known.

**Decision point:** record the chosen direction(s) in `DECISIONS.md` with the evidence that drove
the choice.

---

## Phase 7 — Final experiments and reporting

[BRIEF] Deliverables: "the implemented experimental pipeline, reproducible experiments and code,
an analysis of the results, and the final report and presentation."

- Freeze the pipeline; final runs with recorded seeds, model versions and commit hashes.
- Verify reproducibility end-to-end from a clean checkout using the cached responses and configs.
- Write the analysis and the final report; prepare the presentation.
- [RECOMMENDATION] Include a **limitations section**, covering: the label-noise ceiling; that
  conclusions are about our controlled pipeline and may not transfer to commercial engines; and
  the **dual-use aspect** — this work is in substance SEO for LLMs and could inform content
  manipulation. [DOSSIER recommends this; the brief does not mention it. Raise with Yannick.]

[UNSPECIFIED] Report length, presentation format, deadlines, assessment criteria.

**Exit criterion:** all four named deliverables complete, and a clean-checkout reproduction of
the headline results.

---

## Risks tracked across the plan

| Risk | Source | Where addressed |
|---|---|---|
| **Label noise** — stochastic citation caps achievable accuracy | [DOSSIER] | Phase 3 label-stability study, early |
| **Rank dominance** — content features may add nothing beyond retrieval position | [DOSSIER] | Phase 3 rank-only control; Phase 5 lift metric |
| **Budget ceiling** — $500 constrains scale more than it appears | [BRIEF] amount; [DOSSIER] assessment | Cost estimate before every run; response caching; subset-first |
| **Fast-moving field** — novelty may erode | [DOSSIER] | Phase 1 novelty check |
| **Modest novelty as scoped** — reproduction + classifier is not a contribution | [DOSSIER] | Phase 6 direction choice |
| **Scope creep into optional extensions** | [BRIEF] explicitly warns | This plan's essential/optional split |
| **Dual-use** | [DOSSIER]; not in brief | Phase 7 limitations; Phase 0 question |
