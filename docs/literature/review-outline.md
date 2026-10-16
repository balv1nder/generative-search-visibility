# Literature Review — working outline

**Status:** adopted structure, not yet written.

## Provenance and assessment

This outline was produced with Perplexity and supplied by the team on 2026-10-16. Its
substantive claims were checked against the GEO paper, read in full the same day
(arXiv:2311.09735). **The outline is accurate** on every checkable point:

| Outline claim | Verified against GEO paper |
|---|---|
| Word-count impression metric | ✅ `Imp_wc`, §2.2.1 |
| Position-adjusted word count | ✅ `Imp_pwc`, exponential position decay |
| Seven subjective dimensions, named | ✅ Exactly seven, names match |
| Nine optimization strategies, named | ✅ All nine match |
| Nine GEO-bench source families | ✅ Match ("debate-oriented questions" = Davinci-Debate) |
| Evidence-additions strongest; keyword stuffing fails | ✅ Confirmed |
| Lower-ranked sources benefit disproportionately | ✅ Confirmed, and larger than implied |

**Decision: adopt this structure rather than rewrite it.** See `DECISIONS.md`.

Three sections are added below, each marked **[ADDED]**, covering gaps in the original. The
original section numbering is preserved so the two can be diffed.

> **Known weakness:** the supplied outline's bibliography was a single URL. The reference list
> is now in `01-geo-aggarwal-2024.md`, `02-liu-verifiability-2023.md` and
> `03-supporting-literature.md`, with verification status per field.

---

## Structure

### Abstract
Shift from ranked-link search to generative search with source-grounded answers. Visibility is
no longer only rank: it includes retrieval, use in the answer, citation, position, and
contribution to generated text. Position GEO alongside retrieval, learning-to-rank, grounded
generation, citation evaluation and content optimization. Close on the gap this project
addresses: predicting retrieval and citation visibility from query–document features in a
controlled pipeline.

### 1. Introduction
1.1 **From search engines to generative engines** — ranked results vs. retrieve-synthesize-cite;
the user may never visit the source; implications for creators and attribution.
1.2 **Research problem** — given a query and candidate document, can we predict whether it is
retrieved, used, and cited? Separate the three outcomes. Explain why retrieval rank alone is
insufficient.
1.3 **Scope and contributions** — what this review synthesizes, and the project's empirical
direction.

### 2. Generative Search Engines
2.1 **Architecture** — query reformulation → retrieval → optional summarization → generation →
inline citation. Roles of retriever, reranker, generator, citation mechanism. Controlled vs.
commercial black-box systems.
2.2 **Grounded answer generation** — grounding, hallucination risk, citation precision and
recall as trustworthiness measures.
2.3 **Conversational and multi-turn search** — brief; justify restricting this project to
single-turn.

### 3. Retrieval and Document Ranking
3.1 **Classical IR** — BM25 as interpretable baseline; relevance and ranking scores; rank and
retrieval score as visibility signals that do not fully determine citation.
3.2 **Dense retrieval** — embeddings, DPR; lexical vs. semantic matching; semantic similarity as
a candidate feature.
3.3 **Learning to rank** — pointwise/pairwise/listwise; why it applies when documents compete
for the same query; MRR, Recall@k, nDCG and their limits here.
3.4 **Retrieval versus citation** — a highly ranked source may go uncited if redundant, less
specific, less trustworthy or harder to use. Frame separate models for `P(retrieved)`,
`P(cited | retrieved)`, and visibility given citation.

### 4. Citation Quality and Verifiability
4.1 **Citation precision** — an attached source truly supports its claim; attribution
correctness, not visibility.
4.2 **Citation recall** — important claims receive adequate evidence; completeness of grounding.
4.3 **Implications for visibility research** — optimization must not trade accuracy for
visibility; a visibility predictor should be evaluated alongside factual grounding; risks of
optimizing text merely to attract citations.

### 5. Generative Engine Optimization
5.1 **Definition and motivation** — GEO vs. SEO; black-box assumptions.
5.2 **Visibility and impression metrics** — 5.2.1 word-count impression; 5.2.2
position-adjusted word count; 5.2.3 subjective impression and its seven dimensions, with the
benefits and limits of LLM-as-judge.
5.3 **Content optimization strategies** — the nine GEO strategies; distinguish
evidence-enriching from purely stylistic interventions; state the ethical constraint that
changes preserve meaning and avoid fabricated statistics, quotations or references.

### 6. GEO-bench and Experimental Evaluation
6.1 **Benchmark design** — diversity by domain, difficulty, intent; the nine source families.
6.2 **Experimental pipeline** — two-stage setup; reproducibility choices: fixed retrieval
depth, fixed prompts, model settings, multiple samples, controlled source content.
6.3 **Evaluation metrics** — retrieval (Recall@k, MRR, nDCG); citation/grounding (precision,
recall); visibility (word count, position-adjusted, subjective); prediction (precision, recall,
F1, ROC-AUC, PR-AUC, calibration).
6.4 **Main findings from GEO** — evidence-oriented additions strongest; keyword stuffing does
not transfer; domain dependence; lower-ranked sources benefit disproportionately.

### 7. Predicting Document Visibility
7.1 **Task formulation** — input is a query–document pair plus retrieval context. Targets:
binary retrieved; binary cited; continuous visibility score; or four-way multi-class
(not retrieved / retrieved-not-cited / cited-low-visibility / cited-high-visibility).
7.2 **Interpretable feature baseline** — semantic similarity; lexical overlap and BM25; rank and
score margin; length and passage structure; readability and fluency; presence of numbers,
quotations and external citations; named entities, technical terms, topical specificity;
redundancy or novelty relative to competing documents. Logistic regression, trees, random
forests, gradient boosting. Feature importance, partial dependence, error analysis.
7.3 **Advanced models** — cross-encoder rerankers; transformer classifiers; pairwise/listwise
LTR; LLM-based feature extraction or prediction; graph or set-aware models accounting for
competing documents. Trade-offs in performance, cost, reproducibility, interpretability.
7.4 **Robustness and generalization** — query paraphrases; transfer across domains and intents;
transfer across generative models; optional comparison with a commercial engine as an
external-validity check.

### 8. Research Gaps and Project Positioning
### 9. Conclusion

---

## [ADDED] A. Rank-only control baseline

**Belongs in §6.3 and §7.2.** The supplied outline lists retrieval rank as a *feature* but never
as a *baseline*.

The GEO paper makes this non-optional. Cite Sources produced a **+115.1%** visibility increase
for rank-5 sources while **the top-ranked source lost 30.3%** on average. Position effects are
large and **non-monotonic**.

[INFERENCE] A classifier can therefore score well while having learned only "rank 1 gets cited".
The project's central question — *does content matter beyond position?* — is answered only by
training a model on **rank alone** and reporting **lift** of the full model over it.

Report: full-model AP/AUC, rank-only AP/AUC, and the difference with a confidence interval.

## [ADDED] B. Label stability and the noise ceiling

**Belongs in §6.2 and as a limitation throughout.** Absent from the supplied outline.

The GEO paper samples **5 responses at temperature 0.7 across 5 random seeds** specifically to
reduce variance. Citation is stochastic.

[INFERENCE] If identical queries yield different citations across runs, there is an accuracy
ceiling no model can exceed, and every reported metric must be read against it. A model at 0.70
AUC against a 0.72 ceiling is near-perfect; the same number against a 0.95 ceiling is poor.

Measure early — the cost is small and it reframes everything downstream. Report the ceiling
beside every accuracy number.

## [ADDED] C. Experimental cost model

**Belongs in §6.2.** Absent from the supplied outline, and the budget is ~$500 [BRIEF].

Specific trap: GEO's **Subjective Impression** uses G-Eval with an LLM judge, scored **per
citation per response, sampled multiple times**. Across 1K test queries × 5 sources × 5 samples
this could dominate total spend.

[RECOMMENDATION] Reproduce `Imp_wc` and `Imp_pwc` — which need no LLM judge — and treat
Subjective Impression as optional, costed before committing. Record calls, tokens, model
pricing and cumulative spend per `CLAUDE.md`.

---

## [ADDED] D. Open design decision — what exactly do we predict?

The supplied outline's §7.1 is **more correct than our own `PROJECT_CONTEXT.md`**, which leans
binary cited/not-cited.

**GEO's visibility metric is continuous** — the share of answer text attributed to a source —
not a binary citation flag. Three viable targets:

| Target | Pros | Cons |
|---|---|---|
| Binary `cited` | Simplest; standard classification metrics; matches the brief's wording | Discards magnitude; a one-clause mention equals a dominant source |
| Continuous `Imp_pwc` | Matches GEO's own metric; reproduction is directly comparable | Regression; noisier; calibration harder |
| Four-way multi-class | Preserves the retrieval/citation distinction *and* magnitude | More classes, sparser data, harder to interpret |

[BRIEF] says predict whether a document is "selected **and/or** cited" — which does not settle
it. **This is a supervisor question** (kickoff agenda Q9); it determines the dataset schema,
the metric set and the loss function, so it should be settled before Phase 3.
