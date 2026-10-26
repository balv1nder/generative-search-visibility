# TODO.md

Working task list for **P11 — Understanding and Optimizing Content Visibility in Generative
Search Engines**.

**Convention.** Items written as tasks (`- [ ]`) are actions we can justify from the project
brief. Items that are genuinely uncertain are written as **questions**, not tasks — we do not
turn an assumption into work. Evidence tags follow `PROJECT_CONTEXT.md`.

Status as of **2026-10-16**: repository initialised, no supervisor contact yet, no code written.
Literature base populated for both brief-named papers. **A December 2026 midterm is confirmed.**

---

## Immediate

- [ ] Every team member reads `PROJECT_CONTEXT.md`, `RESEARCH_PLAN.md`, `DECISIONS.md`, `TODO.md`
- [ ] Read the original brief in `docs/project-brief/` directly — not only our summary
- [ ] Agree who owns which workstream (pipeline / modelling / literature / writing) and record it
- [ ] **Take `docs/meeting-notes/2026-10-16-kickoff-agenda.md` into the kickoff meeting**, then
      record answers and propagate them per `docs/meeting-notes/README.md`
- [ ] **Start the literature review now** — it is the only workstream not blocked on supervisor
      answers, and a complete midterm artefact on its own. Structure:
      `docs/literature/review-outline.md`
- [ ] Send the **Supervisor Questions** below to Yannick Le Cacheux, prioritising the four
      blocking ones. [BRIEF offers a dataset subset and initial code examples but neither has a
      concrete form yet — asking is the single highest-value action available right now]
- [ ] Set up Python environment and pin dependencies; add `requirements.txt` / `pyproject.toml`
- [ ] Create `.env.example` listing required variable **names** only (never values)
- [ ] Confirm `.gitignore` covers every path where API keys or raw data could land

---

## Supervisor Questions

The four marked **BLOCKING** gate Phase 2 of `RESEARCH_PLAN.md`.

**Resources and setup**
- [x] ~~Does GEO-bench include full document text, or only URLs?~~ **RESOLVED 2026-10-16** —
      it ships cleaned full text. GEO paper §3.2: "Each query is augmented with the cleaned text
      content of the top 5 search results from the Google search engine." No scraping needed
- [ ] **BLOCKING** — Which subset of GEO datasets/benchmarks will be provided, in what format,
      and when? Does the subset retain the cleaned source text? Is `GEO-Optim/geo-bench` the
      intended source? *[the HF path is [DOSSIER]-sourced and still unverified; the paper gives
      `generative-engines.com/GEO/`]*
- [ ] **BLOCKING** — What **initial code examples and guidance** already exist for the controlled
      generative-search pipeline? *[BRIEF offers these explicitly — we should not rebuild them]*
- [ ] **BLOCKING** — Which **LLM** should the controlled pipeline use: a commercial API or a
      locally hosted open model? **GEO used `gpt-3.5-turbo`, now deprecated — what substitutes
      for a faithful reproduction?** *[BRIEF permits either; drives cost and reproducibility]*
      → *proposal: local open-weights model as primary workhorse, API budget reserved for a
      cross-model transfer check*
- [ ] **BLOCKING** — Is the **~$500 API budget per project or per student**? How do we access it
      (shared key, our own accounts, reimbursement)? What would justify an increase?
      *[BRIEF states the amount and that it "may be increased depending on the research direction
      and experimental needs", but not the mechanism]*

**Midterm — December 2026, confirmed**
- [ ] What is expected at the December midterm — report, demo, presentation, or results?
- [ ] Is "Levels 1–2 plus a preliminary Level 3 baseline" a fair December target?
- [ ] Would you accept a **negative result** (content adding nothing beyond rank) as valid?
- [ ] Is the midterm graded, and individually or jointly?
- [ ] What is the full timeline and final deadline?

**Design decisions raised by reading the papers**
- [ ] **What exactly do we predict** — binary `cited`, continuous `Imp_pwc`, or a four-way
      multi-class? *[BRIEF's "selected and/or cited" does not settle it; GEO's metric is
      continuous. Determines the dataset schema]*
- [ ] Do we reproduce **Subjective Impression**? It needs a G-Eval LLM judge per citation per
      response — potentially the largest cost line
- [ ] Mirror GEO's exact setup (top-5 sources, temp 0.7, 5 samples × 5 seeds)?
- [ ] Is the novelty **predicting visibility before modification**? *[The GEO paper contains zero
      occurrences of "predict"]*
- [ ] Should we condition explicitly on **retrieval rank**? *[rank-5 +115.1% vs rank-1 −30.3%]*

**Scope and direction**
- [ ] Which **visibility metrics** and which **published GEO results** should the reproduction
      target? *[BRIEF refers to "visibility metrics" and a "GEO evaluation protocol" without
      enumerating them — [UNSPECIFIED]]*
- [ ] If time forces a choice, would you prioritise the **predictive model** or the
      **content-optimisation system**? *[BRIEF presents the latter as "may serve as the basis for"]*
- [ ] Is the **intervention experiment** — rewrite a document according to the model's drivers,
      rerun the pipeline, measure the citation change — in scope?
      *[BRIEF lists "automatically optimizing document content" as a possible extension]*
- [ ] Should we attempt comparison against **real commercial generative engines**, or is the
      controlled setup sufficient? *[BRIEF calls this "an optional extension rather than a
      requirement"]*
- [ ] Has anyone measured **run-to-run stability** of citation behaviour in your experience?
      *[Not in the brief; this bounds the accuracy any model can reach]*

**Context, constraints and output**
- [ ] Is **publication** an aim? If so, which venue and what deadline? *[UNSPECIFIED]*
- [ ] Is **Manifold Technology's commercial interest** shaping the research direction? Can code
      and results be **published openly**, or should the repository stay private? *[UNSPECIFIED;
      repository is currently private by default]*
- [ ] How should we handle the **dual-use aspect** — this is in substance SEO for LLMs. Would you
      like a limitations discussion of content manipulation in the report? *[Not mentioned in the
      brief; [DOSSIER] recommends it]*
- [ ] **Team size and composition**, **project start and end dates**, **interim deadlines**,
      **expected report length and presentation format**, and **assessment criteria** — all
      *[UNSPECIFIED]*. We cannot schedule anything without these.

---

## Literature

[BRIEF] Level 1 requires studying the relevant literature. See `docs/literature/README.md` for
per-paper notes, relevance and priority.

**Named in the brief — High priority**
- [x] ~~Read Aggarwal et al., *GEO*, KDD 2024~~ **DONE 2026-10-16** — full section-wise notes in
      `docs/literature/01-geo-aggarwal-2024.md`
- [x] ~~Verify bibliographic details of both papers~~ **DONE** — GEO is arXiv:2311.09735, KDD 2024;
      Liu et al. is arXiv:2304.09848, **Findings of EMNLP 2023** (discrepancy resolved)
- [ ] **Read Liu et al. in full** — the note is currently built from the abstract. Methodology
      (annotator counts, query counts, rating scales) is marked `UNVERIFIED` and must not be
      cited until checked
- [ ] Read **Gao et al., ALCE** (EMNLP 2023) — promoted to High. It specifies the
      citation-parsing and labelling step we are building. See `03-supporting-literature.md`

**Writing the review**
- [ ] Draft the review following `docs/literature/review-outline.md`, including the three
      added sections (rank-only control, label stability, cost model)
- [ ] Resolve the outstanding verification tasks listed at the foot of
      `docs/literature/README.md` before any citation reaches the report

**Anticipated by the brief — Medium priority**
- [ ] [BRIEF] "Additional recent literature on generative search, retrieval, learning-to-rank and
      LLM-based evaluation will be investigated during the project" — survey these four areas
- [ ] Novelty check: what has been published on GEO *since* Aggarwal et al.? *[DOSSIER flags the
      field as fast-moving and recommends this in week one]*

**Suggested by the dossier only — Medium/Low, see `docs/literature/README.md`**
- [ ] Decide which of the dossier-suggested papers (RAG, DPR, BERT re-ranking, ALCE, LambdaMART,
      BEIR) are actually needed, based on the directions we choose

**Output**
- [ ] Write a short synthesis: what the published GEO evaluation protocol is, and what gap our
      controlled setup addresses

---

## Data

- [ ] Obtain the GEO-bench subset (gated on supervisor question 1)
- [ ] Document in `data/README.md`: provenance, licence, schema, and how to regenerate everything
- [ ] Define the schema for our generated records: `(query, document, retrieved?, rank,
      retrieval_score, cited?)` plus generation metadata (model, version, temperature, seed,
      timestamp, commit) *[BRIEF Level 2: "an experimental dataset associating queries, candidate
      documents, retrieval information and citation/visibility outcomes"]*
- [ ] Confirm raw data stays out of git and document how a teammate obtains it

**Questions, not tasks**
- Is there a licence or terms-of-use constraint on GEO-bench web sources that affects what we may
  redistribute or publish? *[UNSPECIFIED]*
- Is any Manifold proprietary data available or in scope? *[UNSPECIFIED]*

---

## Engineering

**Do not start these until the relevant blocking supervisor questions are answered** — per
`CLAUDE.md`, and because the brief offers initial code we should not duplicate.

- [ ] `src/retrieval` — index candidate documents, retrieve top-k, record score and rank
      *[BRIEF names retrieval score and ranking position as baseline features, so both must be
      recorded from the start]*
- [ ] `src/generation` — prompt an LLM with retrieved documents to produce a grounded answer with
      source citations *[BRIEF]*
- [ ] `src/citation` — parse which documents the generated answer actually cited. **This step
      manufactures every label in the project; its correctness gates everything downstream**
- [ ] LLM response caching keyed by (model, prompt, parameters) — makes reruns free and
      reproducible, and protects the budget *[RECOMMENDATION]*
- [ ] Cost-estimation and spend-tracking utility; log cumulative spend against the ~$500 budget
      *[RECOMMENDATION, driven by the BRIEF budget]*
- [ ] `src/features` — the four brief-named features first (semantic similarity, document length,
      retrieval score, ranking position), then any additions, clearly marked as our additions
- [ ] `src/models` — interpretable baseline, plus a **rank-only control baseline**
- [ ] Config-driven experiment runner reading `experiments/configs/`; seeds and commit hash
      recorded with every result

---

## Experiments

Ordered by `RESEARCH_PLAN.md`. Nothing here should run before a written cost estimate exists.

- [ ] End-to-end smoke run on a tiny query subset — establishes cost per query and exposes
      integration problems early *[RECOMMENDATION]*
- [ ] Reproduce a subset of published GEO results and visibility metrics *[BRIEF Level 1 —
      which subset is a supervisor question]*
- [ ] **Label-stability study**: repeat identical queries at fixed sampling parameters and measure
      citation-decision variability. Establishes the accuracy ceiling. *[INFERENCE — not in the
      brief, but the whole supervised framing depends on it; [DOSSIER] calls it the risk most
      likely to be discovered too late]*
- [ ] Generate the experimental dataset at scale, within budget *[BRIEF Level 2]*
- [ ] Train and evaluate the interpretable baseline against the rank-only control *[BRIEF Level 3]*
- [ ] Feature-importance and interpretability analysis; answer "which characteristics are most
      predictive" *[BRIEF Level 4 and research question 2]*
- [ ] Choose **at least one** advanced direction and record the choice with its evidence in
      `DECISIONS.md` *[BRIEF Level 5 — the brief says this choice follows first results]*

**Questions, not tasks**
- Should the two-stage decomposition (`P(retrieved)` vs. `P(cited | retrieved)`) be our default
  advanced direction? It is named in the brief as a possible extension and costs no extra API
  spend, but the choice is meant to follow first results, so we should not pre-commit.
- What minimum number of repeated runs makes the label-stability estimate trustworthy at
  acceptable cost?
- Is a commercial-engine comparison worth any of the budget, given the brief marks it optional?

---

## Reporting

[BRIEF] Deliverables: the implemented experimental pipeline; reproducible experiments and code;
an analysis of the results; the final report and presentation.

- [ ] Keep `reports/` updated as results arrive rather than writing at the end
- [ ] Maintain figures from `experiments/results/` with the commit and config that produced them
- [ ] Draft the limitations section early, covering: the label-noise ceiling; that conclusions
      apply to our controlled pipeline and may not transfer to commercial engines; and the
      **dual-use aspect** *[RECOMMENDATION; [DOSSIER] recommends it; not in the brief — confirm
      with Yannick]*
- [ ] Verify the headline results reproduce from a clean checkout before submission
- [ ] Final report and presentation

**Questions, not tasks**
- Report length, format, language, and deadline — all *[UNSPECIFIED]*
- Is an interim/midterm deliverable expected? *[UNSPECIFIED]*
- Does the pipeline need to be runnable by an assessor, or is code inspection sufficient?
