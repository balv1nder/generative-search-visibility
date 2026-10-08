# PROJECT_CONTEXT.md

Shared, authoritative project context for **Project 11 (P11)**.
This file is the single source of truth for *what the project is*. It is written so that a
teammate or a future Claude session can understand the project without any prior conversation.

## Source hierarchy and labelling convention

Three distinct levels of authority are used throughout this repository. Never collapse them.

| Tag | Meaning |
|-----|---------|
| **[BRIEF]** | Stated explicitly in the official P11 project brief (`docs/project-brief/P11 - Lab project - ....docx`). Authoritative. Quoted or closely paraphrased. |
| **[DOSSIER]** | Stated in the *MSc AI Lab Project Dossier* (212-page analysis report, 27 Sept 2026), P11 section, pp. 63–69 and 167–171. This document is **third-party analysis of the brief, not a statement by the supervisor.** Useful and well-researched, but it is interpretation. |
| **[INFERENCE]** | Our own reading of the brief, not stated by it. |
| **[RECOMMENDATION]** | Our own proposal. Carries no authority at all. |
| **[UNSPECIFIED]** | Not specified in the project dossier — clarify with supervisor. |

> **Important caveat about the dossier.** The dossier is an analytical companion document that
> covers all 15 lab projects. Its P11 section contains both direct quotations from the brief
> (authoritative) and a large volume of its own recommendations, roadmaps, experiment lists and
> risk assessments (not authoritative). Where this file cites **[DOSSIER]**, that content has
> **not** been endorsed by Yannick Le Cacheux and must be treated as a well-informed outside
> opinion until confirmed.

---

# Project

**Title** [BRIEF]
> Understanding and Optimizing Content Visibility in Generative Search Engines

Internal identifier: **P11**. Repository name: `generative-search-visibility`.

# Supervisor

[BRIEF]
- **Yannick LE CACHEUX**
- Email: `yannick.le-cacheux@centralesupelec.fr` / `lecacheux@manifold.fr`
- Institution: **Manifold Technology** (& lecturer at **CentraleSupélec**)

[DOSSIER] The same supervisor also proposes P12 (*Adaptive Prompt Compression for Efficient LLM
Inference*); the two projects are described as sharing infrastructure and representing
complementary angles on LLM systems.

[DOSSIER] Manifold Technology's involvement indicates direct commercial interest in the topic.
Whether that commercial interest constrains the research direction or publication is
**[UNSPECIFIED]** — clarify with supervisor.

# Problem

[BRIEF] Large Language Models are changing how users access information online. Generative search
engines and conversational assistants (ChatGPT, Claude, Gemini, Perplexity) retrieve information
from multiple sources and directly generate an answer, **citing only a subset of these sources**.

[BRIEF] This creates a new research problem for content creators: *what makes a source likely to
be retrieved, used and cited by a generative engine?* The emerging field of **Generative Engine
Optimization (GEO)** studies how online content can be adapted to improve its visibility within
such systems.

[DOSSIER] The gap is that GEO is new, largely practitioner-driven, and thin on controlled
evidence — most of what circulates is marketing advice. A controlled experimental environment
where one property can be varied at a time is what the area lacks.

# Research Questions

[BRIEF] The brief poses three questions verbatim:

1. **Can we predict whether a document will be selected or cited for a given query?**
2. **Which characteristics of the query and document are the most predictive?**
3. **Can such a predictive model subsequently be used to automatically suggest or generate better content?**

[BRIEF] Stated as an objective rather than a question:
> "build and evaluate models predicting the visibility of a document within a generative search engine"

[DOSSIER] A sharpened research-question formulation proposed by the dossier (**not** the
supervisor's wording): *which query and document properties causally determine citation by a
generative engine, can they be predicted from features available before generation, and do
interventions suggested by the predictive model actually increase citation without changing
meaning?*

# Goals

[BRIEF] **Main objective:** build and evaluate models predicting the visibility of a document
within a generative search engine.

[BRIEF] Three sequential goals:

1. **Simplified generative search pipeline.** Implement a pipeline inspired by existing
   literature. Given a user query and a collection of candidate documents, the system retrieves
   relevant documents and uses an LLM to generate a grounded answer with source citations. This
   controlled environment makes it possible to generate experimental data and reproduce a subset
   of existing GEO results and visibility metrics.
2. **Core ML task.** Predict, for a given **(query, document)** pair, whether the document will
   be **selected and/or cited** by the generative engine. Students first develop a *simple and
   interpretable baseline* using manually designed features (semantic similarity, document
   length, retrieval score, ranking position) with standard ML algorithms. More advanced
   approaches may subsequently be investigated: transformer-based representations,
   learning-to-rank, interpretability analyses, LLM-based models.
3. **Content optimization system (may).** The predictive model *may* serve as the basis for a
   system able to identify strengths and weaknesses of a document and suggest modifications
   expected to improve its visibility **while preserving its original meaning**.

[BRIEF] **Explicit scope control — quoted, and important:**
> "These extensions are deliberately open-ended: students are not expected to investigate all of
> them. The exact research direction will be selected according to the first experimental
> results, progress and interests of the team."

# Expected Methodology

[BRIEF] "The project will be organized with increasing levels of difficulty":

| Level | Stated work |
|-------|-------------|
| 1 | Study the relevant literature and reproduce a simplified version of an existing generative-engine pipeline and GEO evaluation protocol |
| 2 | Build an experimental dataset associating queries, candidate documents, retrieval information and citation/visibility outcomes |
| 3 | Design and evaluate an interpretable ML baseline predicting document visibility |
| 4 | Analyze the model and identify which document/query properties influence visibility |
| 5 | Investigate **at least one** more advanced research direction |

[BRIEF] **Possible extensions**, listed verbatim in the brief:
- comparing classical ML with transformer- or LLM-based models
- **separating retrieval probability from citation probability**
- automatically optimizing document content
- studying robustness to query paraphrases
- measuring whether conclusions obtained with one generative model transfer to another

[BRIEF] **Optional extension, explicitly not a requirement:**
> "If progress permits, experiments may also be conducted with existing commercial generative
> engines in order to compare the controlled experimental setup with real-world systems. This is
> considered an optional extension rather than a requirement of the project."

[DOSSIER] The dossier singles out the retrieval/citation separation as deserving to be central:
a document must first be *retrieved*, then *chosen by the generator*; lumping them together
confuses two mechanisms. It calls the two-stage formulation "the cleanest structural idea
available in this project". **This is dossier opinion, not a supervisor instruction.**

# Technical Concepts

[BRIEF] Required technical environment:
- **Python** and standard ML/NLP libraries: **scikit-learn**, **PyTorch**, **Hugging Face Transformers**
- Students may use **commercial or open-source LLMs** through APIs or locally hosted models
- **No previous expertise in LLMs or information retrieval is required.** The initial baseline is
  "intentionally designed to be accessible using concepts from standard machine-learning
  courses", while allowing substantially more advanced approaches.

[DOSSIER] Concept inventory by tier (dossier's own categorisation):
- *Essential*: standard supervised ML and feature engineering; Python, scikit-learn; text
  embeddings and cosine similarity; basic IR (BM25, dense retrieval, top-k); prompting an LLM
  through an API.
- *Useful*: RAG pipeline construction; learning-to-rank (pointwise, pairwise, listwise);
  transformer fine-tuning with Hugging Face; interpretability (SHAP, permutation importance);
  citation-attribution parsing; experimental design for causal claims.
- *Can learn during*: vector databases (FAISS, Chroma); LLM-as-judge evaluation; controlled text
  rewriting with preserved meaning; robustness testing against paraphrase; cost control for API
  experiments.

# Algorithms / Models

| Component | [BRIEF] says | [DOSSIER] suggests (not authoritative) |
|-----------|--------------|-----------------------------------------|
| Pipeline | "simplified generative search pipeline inspired by existing literature" | BM25 + a dense retriever (sentence-transformers or BGE); FAISS; one open model and one commercial model to test transferability |
| Baseline predictor | "manually designed features such as semantic similarity, document length, retrieval score or ranking position, combined with standard machine-learning algorithms" | Logistic regression and gradient boosting; **include a rank-only baseline**, because retrieval rank will likely dominate |
| Advanced | "transformer-based representations, learning-to-rank methods, interpretability analyses, or LLM-based models" | Cross-encoder over (query, document); LambdaMART for listwise ranking; an LLM asked directly to predict its own citation behaviour |
| Two-stage | "separating retrieval probability from citation probability" | Model `P(retrieved)` and `P(cited | retrieved)` separately |
| Content optimisation | "identify strengths and weaknesses of a document and suggest modifications" | LLM-based rewriting conditioned on learned feature importances, with an NLI/embedding semantic-equivalence check to enforce the brief's "preserving its original meaning" constraint |
| Interpretability | "interpretability analyses" | SHAP, permutation importance, and direct intervention experiments |

**Which specific retriever, embedding model, LLM and classifier to use is [UNSPECIFIED] in the
brief** — the brief deliberately leaves this to the team. See Open Questions.

# Data

[BRIEF] **GEO-bench** — the project "will build upon existing research on GEO, in particular
GEO-bench, a benchmark containing **10,000 queries and associated web sources**."

[BRIEF] Resources made available:
> "A subset of existing GEO datasets and benchmarks will be provided or identified at the
> beginning of the project. Initial code examples and guidance for the controlled
> generative-search pipeline can also be provided."

[DOSSIER] GEO-bench is publicly available on Hugging Face at `GEO-Optim/geo-bench`.
**This URL comes from the dossier, not the brief — verify before relying on it.**

[DOSSIER] Crucially, **most of the training data is generated by us**: running the pipeline over
queries produces `(query, document, retrieved?, cited?)` records at whatever scale the API budget
allows. Rough scale: 10,000 queries × ~5–10 candidate documents ≈ 10⁵ labelled pairs; a few GB
with embeddings. The binding constraint is **LLM calls, not data volume**.

[UNSPECIFIED] Which subset of GEO-bench will be provided, in what format, and when.
[UNSPECIFIED] Whether any Manifold proprietary data is available or in scope.

# Evaluation

[BRIEF] The brief refers to reproducing "a subset of existing GEO results and **visibility
metrics**" and to the "GEO evaluation protocol", but **does not enumerate specific metrics**.
The concrete metric list below is therefore **not from the brief**.

[DOSSIER] Proposed evaluation metrics:
- **AUC-ROC and average precision** for citation prediction. AP matters more because citation is
  imbalanced — most retrieved documents are not cited.
- **Calibration** (Brier score, reliability curves) — a content-optimisation tool that says "80%
  chance of citation" must mean it.
- **NDCG / MRR** if treated as ranking rather than classification, which is the more natural
  framing when a fixed number of sources will be cited.
- **Lift over the rank-only baseline** — described by the dossier as "the single most important
  metric in the project and it is easy to forget to compute". Answers whether content matters at
  all beyond position.
- **Citation-rate change after intervention** — the causal outcome; report with a statistical test.
- **Semantic similarity between original and rewritten documents** — the constraint metric that
  guards against rewriting a document into a different document.
- **Label stability across repeated runs** — bounds achievable accuracy.
- **Cross-model agreement** — whether conclusions transfer between generative engines.

[UNSPECIFIED] The authoritative definition of "visibility metrics" and which published GEO
metrics the supervisor expects us to reproduce. **This is a priority question.**

# Deliverables

[BRIEF] Verbatim:
> "The final deliverables will include the implemented experimental pipeline, reproducible
> experiments and code, an analysis of the results, and the final report and presentation."

So, four items:
1. The implemented experimental pipeline
2. Reproducible experiments and code
3. An analysis of the results
4. The final report and presentation

[UNSPECIFIED] Deadlines, report length, presentation format, assessment weighting, whether an
interim/midterm deliverable is expected.

# Constraints / Resources

[BRIEF]
- **LLM API budget: approximately $500**, "initially be made available and may be increased
  depending on the research direction and experimental needs."
- A subset of existing GEO datasets/benchmarks will be provided or identified at project start.
- Initial code examples and guidance for the controlled pipeline "can also be provided".
- No prior LLM or IR expertise required.

[DOSSIER]
- Compute: laptop plus API keys. Compute intensity Low — **API spend is the real cost.**
- The dossier rates P11 as among the lowest-risk projects in the directory: data exists, budget
  is stated in writing, difficulty is explicitly graded.
- Dossier-identified risks: **label noise** (stochastic citation caps achievable accuracy — "the
  risk most likely to be discovered too late"); **rank dominance** (content features may add
  little once retrieval position is controlled); **fast-moving field** (recheck novelty at
  start); **budget ceiling** ($500 constrains experimental scale more than it first appears);
  **modest novelty as scoped** (reproduction plus a classifier is not a contribution);
  **commercial framing** (an industrial partner may prefer commercially useful directions).

[DOSSIER] **Dual-use note.** The project's applied goal is in substance *SEO for LLMs*, with the
attendant possibility of contributing to content manipulation. The brief does not discuss this.
The dossier recommends a short, honest limitations section on the dual-use aspect.
**[RECOMMENDATION] We should adopt that, and should raise it with Yannick rather than decide
unilaterally.**

[UNSPECIFIED] Whether the $500 is per project or per student. Team size and composition.
Project start and end dates. Whether code and results may be published openly.

# Current Understanding

Status as of **2026-10-08**: repository initialised; no implementation started; no contact with
the supervisor yet on any open question.

What we believe the project is, in one paragraph [INFERENCE, grounded in BRIEF]:

> We will build a controlled, self-hosted imitation of a generative search engine — retrieve
> candidate documents for a query, feed them to an LLM, have it write a cited answer, and parse
> which documents it actually cited. That pipeline manufactures its own supervised labels:
> for every `(query, document)` pair we learn whether it was retrieved and whether it was cited.
> On top of that dataset we train an interpretable classifier to predict citation, inspect which
> features drive it, and — if time and results permit — use those findings to rewrite documents
> and test whether citation actually increases.

Three things we are confident about from the brief alone:
1. The **interpretable baseline is the required core**, not an optional warm-up. The brief is
   explicit that standard ML concepts suffice to start.
2. The project is **explicitly staged**, and **not all extensions are expected to be completed**.
   Choosing a direction after seeing first results is the stated intent.
3. **Reproducibility is a named deliverable**, not a nice-to-have.

Three things that are our inference and should be confirmed:
1. [INFERENCE] The retrieval/citation separation is likely to be the most valuable extension,
   because the brief lists it and the dossier argues it is structurally correct.
2. [INFERENCE] Label stability must be measured early, because the entire supervised framing
   assumes the labels are reproducible. The brief does not mention this.
3. [INFERENCE] A rank-only control baseline is essential to make any claim that *content* matters.
   The brief does not mention this either.

# Open Questions

Questions that must be clarified with Yannick Le Cacheux. Full list with priority in `TODO.md`.

**Blocking or near-blocking**
1. Which **GEO dataset subset** will be provided, in what format, and when? Is `GEO-Optim/geo-bench`
   on Hugging Face the intended source?
2. What **initial code examples** exist? The brief offers them; we should not rebuild what exists.
3. Is the **$500 budget per project or per student**, how is it accessed (shared key, our own
   accounts, reimbursement), and what would justify an increase?
4. Which **LLM should the controlled pipeline use** — a commercial API or a locally hosted open
   model? This drives both cost and reproducibility.

**Scope and direction**
5. Which **visibility metrics** and which **published GEO results** should the reproduction target?
6. If time forces a choice, would you prioritise the **predictive model** or the **content
   optimization system**?
7. Is the **intervention experiment** (rewrite → rerun → measure) in scope?
8. Should we test against **real commercial engines**, or is the controlled setup sufficient?
9. Is **publication** an aim? If so, at which venue and deadline?

**Context and constraints**
10. Has anyone measured **run-to-run stability** of citation behaviour?
11. Is **Manifold Technology's commercial interest** shaping the direction, and can results and
    code be **published openly**?
12. How should we handle the **dual-use aspect** — do you want a limitations discussion of
    content manipulation in the report?
13. **Team size, project timeline, deadlines, and assessment criteria** — all [UNSPECIFIED].

> Questions 1–12 overlap substantially with the dossier's own "Questions for the supervisor"
> list (p. 171). That list was independently generated and is a useful cross-check, but it is not
> a supervisor-endorsed agenda.
