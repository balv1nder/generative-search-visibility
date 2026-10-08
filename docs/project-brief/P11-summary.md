# P11 — Project Brief Summary

A faithful summary of **only** the P11 material from the MSc AI Lab project sources.

**Sources used**
1. `P11 - Lab project - Understanding and Optimizing Content Visibility in Generative Search Engines.docx`
   — the official brief, in this directory. **Authoritative.**
2. *MSc AI Lab Project Dossier* (212 pp., 27 Sept 2026), P11 section — pp. 63–69 (full analysis)
   and pp. 167–171 (scope, roadmap, literature, supervisor questions), plus comparative tables on
   pp. 92–108 and the one-page summary on p. 195. **Third-party analysis, not written by the
   supervisor.** Material taken from it is marked **[DOSSIER]** throughout and carries no
   authority over project requirements.

Everything marked **[INTERPRETATION]** or **[RECOMMENDATION]** is ours.
The full dossier is not reproduced here — only its P11 content is summarised.

---

## 1. Identification

| Field | Value |
|---|---|
| Title | Understanding and Optimizing Content Visibility in Generative Search Engines |
| Project ID | P11 |
| Proposed by | Yannick LE CACHEUX |
| Contact | `yannick.le-cacheux@centralesupelec.fr` / `lecacheux@manifold.fr` |
| Institution | Manifold Technology (& lecturer @ CentraleSupélec) |

---

## 2. Context (brief, condensed)

LLMs are changing how users access information online. Generative search engines and
conversational assistants such as ChatGPT, Claude, Gemini or Perplexity retrieve information from
multiple sources and directly generate an answer, **citing only a subset of these sources**.

This creates a new research problem for content creators: *what makes a source likely to be
retrieved, used and cited by a generative engine?* The emerging field of **Generative Engine
Optimization (GEO)** studies how online content can be adapted to improve its visibility within
such systems.

From a machine-learning perspective the brief poses three questions:

1. Can we predict whether a document will be selected or cited for a given query?
2. Which characteristics of the query and document are the most predictive?
3. Can such a predictive model subsequently be used to automatically suggest or generate better content?

The project investigates these in a **controlled experimental environment**, building upon
existing GEO research, in particular **GEO-bench**, a benchmark containing **10,000 queries and
associated web sources**.

---

## 3. Goals (brief)

**Main objective:** build and evaluate models predicting the visibility of a document within a
generative search engine.

**Stage 1 — simplified generative search pipeline.** Implement a pipeline inspired by existing
literature. Given a user query and a collection of candidate documents, retrieve relevant
documents and use an LLM to generate a grounded answer with source citations. This controlled
environment makes it possible to generate experimental data and reproduce a subset of existing
GEO results and visibility metrics.

**Stage 2 — the core ML task.** Predict, for a given **(query, document)** pair, whether the
document will be **selected and/or cited** by the generative engine. Students *first* develop a
simple and interpretable baseline using manually designed features — semantic similarity,
document length, retrieval score, ranking position — combined with standard ML algorithms. More
advanced approaches *may* subsequently be investigated: transformer-based representations,
learning-to-rank methods, interpretability analyses, or LLM-based models.

**Stage 3 — content optimization (conditional).** The predictive model *may* serve as the basis
for a content optimization system able to identify strengths and weaknesses of a document and
suggest modifications expected to improve its visibility **while preserving its original meaning**.

**Scope control, quoted because it governs the whole project:**
> "These extensions are deliberately open-ended: students are not expected to investigate all of
> them. The exact research direction will be selected according to the first experimental
> results, progress and interests of the team."

---

## 4. Expected work — the brief's five levels

> "The project will be organized with increasing levels of difficulty:"

1. Study the relevant literature and reproduce a simplified version of an existing
   generative-engine pipeline and GEO evaluation protocol.
2. Build an experimental dataset associating queries, candidate documents, retrieval information
   and citation/visibility outcomes.
3. Design and evaluate an interpretable ML baseline predicting document visibility.
4. Analyze the model and identify which document/query properties influence visibility.
5. Investigate **at least one** more advanced research direction.

**Possible extensions, listed verbatim in the brief:**
- comparing classical ML with transformer- or LLM-based models
- separating retrieval probability from citation probability
- automatically optimizing document content
- studying robustness to query paraphrases
- measuring whether conclusions obtained with one generative model transfer to another

**Optional, explicitly not a requirement:**
> "If progress permits, experiments may also be conducted with existing commercial generative
> engines in order to compare the controlled experimental setup with real-world systems. This is
> considered an optional extension rather than a requirement of the project."

---

## 5. Deliverables (brief, verbatim)

> "The final deliverables will include the implemented experimental pipeline, reproducible
> experiments and code, an analysis of the results, and the final report and presentation."

---

## 6. Technical aspects (brief)

- Mainly **Python** with standard ML/NLP libraries: **scikit-learn**, **PyTorch**,
  **Hugging Face Transformers**.
- Students may use **commercial or open-source LLMs** through APIs or locally hosted models.
- **No previous expertise in LLMs or information retrieval is required.** The initial baseline is
  "intentionally designed to be accessible using concepts from standard machine-learning
  courses", while allowing substantially more advanced approaches for interested students.

---

## 7. References (brief)

Exactly two papers are named:

1. Aggarwal, P., Murahari, V., Rajpurohit, T., Kalyan, A., Narasimhan, K. & Deshpande, A.
   **GEO: Generative Engine Optimization.** *Proceedings of the 30th ACM SIGKDD Conference on
   Knowledge Discovery and Data Mining*, 2024.
2. Liu, N. F., Zhang, T., Liang, P. et al. **Evaluating Verifiability in Generative Search
   Engines.** *Findings of the Association for Computational Linguistics*, 2023.

Plus: "Additional recent literature on generative search, retrieval, learning-to-rank and
LLM-based evaluation will be investigated during the project."

See `docs/literature/README.md` for notes, priorities and a caution about bibliographic details.

---

## 8. Resources made available (brief)

- "A subset of existing GEO datasets and benchmarks will be provided or identified at the
  beginning of the project."
- "Initial code examples and guidance for the controlled generative-search pipeline can also be
  provided."
- "A budget of approximately **$500** for LLM API usage will initially be made available and may
  be increased depending on the research direction and experimental needs."

---

## 9. What the dossier adds — clearly separated

Everything in this section is **[DOSSIER]**: analysis by a third-party companion document, not
statements by the supervisor. It is well-researched and worth engaging with, but it must not be
mistaken for a requirement.

**Characterisation.** Research-heavy: moderate. Engineering-heavy: high. Mathematical intensity:
low. Coding intensity: high. Compute intensity: low — "API spend is the real cost". Risk: low —
"among the safest projects here: data exists, budget is stated, difficulty is graded". Scope
flexibility: very high — "explicitly designed in levels". Industry relevance: very high.
Publication potential: moderate.

**Dataset location.** GEO-bench is stated to be publicly available on Hugging Face at
`GEO-Optim/geo-bench`. *We have not verified this; the brief does not give a location.*

**Self-generated labels.** The dossier emphasises that most of the training data is generated by
us: running the pipeline over queries produces `(query, document, retrieved?, cited?)` records at
whatever scale the budget allows — on the order of 10⁵ labelled pairs for 10,000 queries ×
5–10 candidates. The binding constraint is LLM calls, not data volume.

**Two structural suggestions the dossier argues for:**
- The **retrieval/citation decomposition** — model `P(retrieved)` and `P(cited | retrieved)`
  separately, since a document must first be retrieved and then chosen. Called "the cleanest
  structural idea available in this project". *Note: this extension is named in the brief, so the
  idea is in scope; the dossier's contribution is arguing it should be central.*
- A **rank-only control baseline** — retrieval rank may dominate everything else, so a rank-only
  comparator is needed to isolate what content features add. Called "the single most important
  metric in the project and it is easy to forget to compute". *This is not in the brief.*

**Proposed evaluation metrics** (none of which appear in the brief): AUC-ROC and average
precision; calibration (Brier score, reliability curves); NDCG/MRR under a ranking framing; lift
over the rank-only baseline; citation-rate change after intervention; semantic similarity between
original and rewritten documents; label stability across repeated runs; cross-model agreement.

**Risks identified.** Label noise — stochastic citation may cap achievable accuracy, and this is
"the risk most likely to be discovered too late"; measure it early. Rank dominance — content
features may add little once position is controlled for. Fast-moving field — several GEO
follow-up papers exist; recheck novelty at the start. Budget ceiling — $500 "constrains
experimental scale more than it first appears". Modest novelty as scoped — "reproduction plus a
classifier is not a contribution". Commercial framing — an industrial partner may prefer
commercially useful directions over scientifically interesting ones.

**Dual-use.** The dossier notes that the project's applied goal is in substance SEO for LLMs,
with the attendant possibility of contributing to content manipulation, that the brief does not
discuss this, and that an honest limitations section would strengthen the report.

**Suggested roadmap** (indicative only — the brief gives no timeline, and no schedule has been
confirmed): weeks 1–2 literature, dataset and API access; 3–5 build the pipeline; 6
label-stability study and GEO reproduction; 7–9 dataset at scale, features, baseline plus
rank-only control; 10–12 interpretability and the retrieval-vs-citation decomposition; 13–16
advanced models; 17–20 intervention experiments; 21–22 cross-model transfer and paraphrase
robustness; 23–24 demo, report, presentation.

---

## 10. Our interpretation and recommendations

**[INTERPRETATION]** The project's defining structural feature is that the pipeline is a *label
factory*. Building the retrieval → generation → citation-parsing loop converts an open-ended
question about generative search into an ordinary supervised learning problem with cheap labels.
This means the citation-parsing step is the highest-leverage component in the repository: every
label in the project passes through it, and an error there is invisible but contaminates
everything downstream.

**[INTERPRETATION]** The brief's ordering is deliberate and should be respected. The interpretable
baseline is the required core, not a warm-up; advanced approaches are explicitly "may".

**[INTERPRETATION]** The brief's own words make the advanced directions a *menu*, not a backlog.
Level 5 asks for "at least one". Treating all five extensions as committed scope would contradict
the brief.

**[RECOMMENDATION]** Measure label stability early. The entire supervised framing assumes the
labels are reproducible, and nothing in the brief guarantees they are.

**[RECOMMENDATION]** Build the rank-only control baseline at the same time as the first model,
not afterwards. Without it, no claim that *content* matters can be supported.

**[RECOMMENDATION]** Cache every LLM response from the very first run. With a ~$500 ceiling, an
uncached pipeline makes every rerun a fresh purchase.

**[RECOMMENDATION]** Ask about the offered starter code and dataset subset before building
anything. The brief offers both; rebuilding them is avoidable waste.

**[RECOMMENDATION]** Include a dual-use limitations discussion, and raise it with the supervisor
rather than deciding unilaterally.
