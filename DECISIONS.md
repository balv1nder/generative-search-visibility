# DECISIONS.md

Decision log for **P11 — Understanding and Optimizing Content Visibility in Generative Search Engines**.

**How to use this file.** One row per decision. Add a new row rather than editing history. When a
decision is superseded, mark the old row `Superseded` and link to the new one. Record the
*evidence* that drove the decision, not just the outcome — a future reader needs to know whether
a decision came from the brief, from the supervisor, from data, or from our own judgement.

**Status values:** `Fixed` (settled by the brief or the supervisor — not ours to change) ·
`Adopted` (our decision, in force) · `Provisional` (our working assumption, expected to change) ·
`Open` (not yet decided) · `Superseded`.

**Evidence tags** follow `PROJECT_CONTEXT.md`: **[BRIEF]** · **[DOSSIER]** · **[INFERENCE]** ·
**[RECOMMENDATION]** · **[UNSPECIFIED]**.

> This log is deliberately short. It contains only decisions that are actually supported by the
> project brief/dossier, or that were genuinely taken while setting up this repository. Research
> and modelling decisions are **not** pre-populated — they will be recorded as they are made,
> which, per the brief, happens after first experimental results.

| Date | Decision | Evidence/Reason | Alternatives | Status |
|------|----------|-----------------|--------------|--------|
| 2026-10-08 | Adopt **P11** as scoped: build a controlled generative search pipeline, generate `(query, document)` citation labels from it, and model document visibility | [BRIEF] — the brief's stated main objective is "build and evaluate models predicting the visibility of a document within a generative search engine" | None — this is the project | Fixed |
| 2026-10-08 | Work in **Python**, using scikit-learn, PyTorch and Hugging Face Transformers | [BRIEF] "The project will mainly use Python and standard machine-learning/NLP libraries such as scikit-learn, PyTorch and Hugging Face Transformers" | Other languages/stacks | Fixed |
| 2026-10-08 | Follow the brief's **five levels of increasing difficulty** as the project's spine, and treat levels 1–4 as essential and level 5 as "at least one advanced direction" | [BRIEF] the brief organises the work this way and states "students are not expected to investigate all of them" | A flat plan committing to all extensions — rejected because the brief explicitly warns against it | Fixed |
| 2026-10-08 | The **interpretable, manually-featured baseline is the required core**, not an optional warm-up; advanced models come after it | [BRIEF] "Students will first develop a simple and interpretable baseline based on manually designed features… More advanced approaches **may** subsequently be investigated" | Starting directly with transformer/LLM-based models — contradicts the brief's ordering | Fixed |
| 2026-10-08 | Use the four feature families the brief names as the baseline's starting feature set: **semantic similarity, document length, retrieval score, ranking position** | [BRIEF] these four are named explicitly | A feature set designed from scratch | Fixed (as a floor; additions are ours) |
| 2026-10-08 | Target **GEO-bench** as the primary dataset | [BRIEF] "will build upon existing research on GEO, in particular GEO-bench, a benchmark containing 10,000 queries and associated web sources" | Constructing a query/document corpus ourselves | Fixed |
| 2026-10-08 | Treat the **~$500 LLM API budget as the project's binding constraint**, and require a written cost estimate before any API-spending experiment | [BRIEF] states the budget; [DOSSIER] assesses compute as low and API spend as "the real cost" and warns the ceiling "constrains experimental scale more than it first appears" | Treating budget as a late-stage concern | Adopted |
| 2026-10-08 | Treat **commercial-engine experiments as an optional stretch item**, not committed scope | [BRIEF] "This is considered an optional extension rather than a requirement of the project" | Planning for them as a deliverable | Fixed |
| 2026-10-08 | Treat **reproducibility as a first-class deliverable**: config-driven experiments, recorded seeds and model versions, cached LLM responses, commit-tagged results | [BRIEF] deliverables include "reproducible experiments and code" | Ad-hoc scripts | Adopted |
| 2026-10-08 | Adopt a **three-level source-labelling convention** ([BRIEF] / [DOSSIER] / [INFERENCE] / [RECOMMENDATION] / [UNSPECIFIED]) across all project documents | [INFERENCE] — the brief and the 212-page dossier differ sharply in authority; the dossier's P11 section mixes direct quotation with a large volume of its own analysis, and conflating them would turn outside opinion into project requirements | A single undifferentiated project description | Adopted |
| 2026-10-08 | Repository scaffolded with the structure in `README.md`; `PROJECT_CONTEXT.md`, `RESEARCH_PLAN.md`, `DECISIONS.md`, `TODO.md` as the shared knowledge base | User instruction for this setup task; [BRIEF] collaborative project with named deliverables | A single README | Adopted |
| 2026-10-08 | **GitHub repository is private** | User instruction ("Prefer a PRIVATE repository"); also [UNSPECIFIED] whether results and code may be published openly, and Manifold Technology has a commercial interest — so private is the safe default until asked | Public from the start | Adopted — revisit after supervisor Q11 |
| 2026-10-08 | **Raw data, the full 212-page dossier PDF, and all generated artefacts are git-ignored**; the P11 brief `.docx` is committed under `docs/project-brief/` | [INFERENCE] the dossier covers all 15 lab projects including other supervisors' material and is personal to the team member who holds it; the P11 brief is specific to this project and small | Committing everything | Adopted |
| 2026-10-08 | No implementation code written yet | [BRIEF] "The exact research direction will be selected according to the first experimental results"; and several Phase 0 questions (provided dataset subset, existing code, which LLM) are unanswered and would change what gets built | Starting the pipeline immediately | Adopted — revisit once Phase 0 blockers clear |

## Decisions deliberately left Open

These are real choices the project must make. They are **not** decided, and nothing in the brief
decides them. Recording them here prevents them from being made by accident.

| Decision | Why it is open | Status |
|----------|----------------|--------|
| Which **LLM** the controlled pipeline uses (commercial API vs. locally hosted open model) | [UNSPECIFIED] — the brief permits either: "Students may use commercial or open-source LLMs through APIs or locally hosted models". Drives both cost and reproducibility | Open — supervisor Q4 |
| Which **retriever(s)** and embedding model | [UNSPECIFIED] — the brief names "retrieval score or ranking position" as features but no specific retriever. [DOSSIER] suggests BM25 + a dense retriever, which is a recommendation only | Open |
| Which **visibility metrics** and which published GEO results the reproduction targets | [UNSPECIFIED] — the brief refers to "visibility metrics" and "GEO evaluation protocol" without enumerating them | Open — supervisor Q5 |
| Which **advanced direction** to pursue for the brief's level 5 | [BRIEF] explicitly says this is chosen based on first experimental results | Open by design — do not pre-decide |
| Whether the **content-optimisation / intervention experiment** is in scope | [BRIEF] frames it as "may serve as the basis for"; cost is high | Open — supervisor Q6/Q7 |
| Whether **publication** is an aim, and whether code/results can be released openly | [UNSPECIFIED] | Open — supervisor Q9/Q11 |
| How to handle the **dual-use aspect** (this is in substance SEO for LLMs) | Not mentioned in the brief at all; [DOSSIER] recommends a limitations discussion | Open — supervisor Q12 |
