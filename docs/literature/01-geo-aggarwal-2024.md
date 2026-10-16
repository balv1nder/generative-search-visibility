# Aggarwal et al. — GEO: Generative Engine Optimization

**The anchor paper for this project.** Named in the brief, and the source of GEO-bench.

## Verified bibliographic record

| Field | Value | Status |
|---|---|---|
| Title | GEO: Generative Engine Optimization | `verified` |
| Authors | Pranjal Aggarwal, Vishvak Murahari, Tanmay Rajpurohit, Ashwin Kalyan, Karthik Narasimhan, Ameet Deshpande | `verified` |
| Venue | KDD '24 — Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, August 25–29 2024, Barcelona, Spain | `verified` |
| arXiv | 2311.09735 (v1 16 Nov 2023; v2 28 May 2024; v3 28 Jun 2024) | `verified` |
| Code/data | `https://generative-engines.com/GEO/` (stated in the paper) | `verified` as stated; link not tested |

Verified by fetching `https://arxiv.org/abs/2311.09735` and extracting the full 12-page PDF
on 2026-10-16. All figures below are quoted from that text.

---

## Section-wise summary

### §1 Introduction — the problem framing
Generative engines synthesize answers from multiple sources and summarize them with LLMs.
This benefits users and engine operators but disadvantages a third stakeholder — **website and
content creators** — who, given the "black-box and fast-moving nature of generative engines",
have "little to no control over when and how their content is displayed". GEO is presented as
"the first novel paradigm to aid content creators in improving their content visibility in
generative engine responses through a flexible black-box optimization framework".

> **Note the word black-box.** The entire paper operates without access to engine internals.
> This is direct support for our project's methodology — see `docs/literature/README.md`
> and the reasoning note in the kickoff agenda.

### §2.2.1 Impression (visibility) metrics — the most reusable part

The paper argues SEO-style average ranking does not apply, because generative engines
"combine information from multiple sources in a single response". Metrics are designed to be
(1) relevant to creators, (2) explainable, (3) comprehensible.

**1. Word Count — `Imp_wc(c_i, r)`**

```
Imp_wc(c_i, r) = ( Σ_{s ∈ S_ci} |s| ) / ( Σ_{s ∈ S_r} |s| )
```

where `S_ci` is the set of sentences citing source `c_i`, `S_r` all sentences in response `r`,
and `|s|` the word count of sentence `s`. **When a sentence cites multiple sources, the word
count is shared equally among them.**

**2. Position-Adjusted Word Count — `Imp_pwc(c_i, r)`**

```
Imp_pwc(c_i, r) = ( Σ_{s ∈ S_ci} |s| · e^( −pos(s) / |S| ) ) / ( Σ_{s ∈ S_r} |s| )
```

Exponential decay by citation position: earlier citations weigh more. Justified by studies
showing click-through rates follow a power law in rank. A source cited at the top can have
higher impression than one with more words further down.

**3. Subjective Impression** — seven sub-metrics, scored by an LLM judge:
relevance · influence · uniqueness · subjective position · subjective count ·
likelihood of clicking · diversity.

Measured with **G-Eval using GPT-3.5**. Because "G-Eval scores are poorly calibrated", scores
are normalised to the same mean and variance as `Imp_pwc`.

All impression metrics are normalised so the impressions of all citations in a response sum
to 1. Improvement is reported relative:

```
Improvement_si = ( Imp_si(r') − Imp_si(r) ) / Imp_si(r) × 100
```

### §2.2.2 The nine GEO methods

A GEO method is a function `f : W → W'` on web content. Applied via an LLM prompted to make
specific stylistic/content changes. One source per query is randomly selected for
optimization and held constant across methods.

1. **Authoritative** — more persuasive, authoritative style
2. **Statistics Addition** — quantitative statistics instead of qualitative discussion
3. **Keyword Stuffing** — more query keywords (classical SEO)
4. **Cite Sources** — add citations from credible sources
5. **Quotation Addition** — add relevant quotations
6. **Easy-to-Understand** — simplify language
7. **Fluency Optimization** — improve fluency
8. **Unique Words** — add unique words
9. **Technical Terms** — add technical terms

Methods 3, 4 and 5 may require *additional content*; the rest only re-present existing content.

### §3.1 Experimental pipeline — our reproduction target

- Two-step design: fetch sources → LLM generates response
- **Top 5 sources** from Google per query, due to context-length and quadratic cost
- **No summarisation** — whole source content provided
- Generator: **`gpt-3.5-turbo`**
- **Temperature 0.7**, **5 sampled responses**, averaged over **5 random seeds**
- Stated to mimic you.com and perplexity.ai

### §3.2 GEO-bench

**10K queries**, split **8K train / 1K validation / 1K test**, from nine sources:

| # | Source | Nature |
|---|---|---|
| 1 | MS MARCO | Real Bing/Google user queries |
| 2 | ORCAS-1 | Real user queries |
| 3 | Natural Questions | Real user queries |
| 4 | AllSouls | Essay questions, All Souls College Oxford — require aggregation across sources |
| 5 | LIMA | Challenging questions requiring reasoning |
| 6 | Davinci-Debate | Debate questions for testing generative engines |
| 7 | Perplexity.ai Discover | Trending platform queries |
| 8 | ELI-5 | ELI5 subreddit — complex questions, layman answers |
| 9 | GPT-4 Generated | Synthetic, for domain/intent/difficulty diversity |

- **25 domains**, 9 query types, 7 tag categories
- Query-intent distribution preserved: **80% informational, 10% transactional, 10% navigational**
- Tagged with GPT-4, manually verified on the test split

> **Critical practical fact:** *"Each query is augmented with the cleaned text content of the
> top 5 search results from the Google search engine."* **GEO-bench ships full cleaned document
> text, not URLs.** No scraping pipeline is required.

### §4 Results

Absolute Position-Adjusted Word Count (baseline = 19.3):

| Method | Word | Position | Overall | Subj. avg |
|---|---|---|---|---|
| *No Optimization* | 19.5 | 19.3 | **19.3** | 19.3 |
| Keyword Stuffing | 17.8 | 17.7 | **17.7** | 20.2 |
| Unique Words | 20.7 | 20.5 | 20.5 | 20.4 |
| Easy-to-Understand | 22.2 | 22.4 | 22.0 | 20.5 |
| Authoritative | 21.8 | 21.3 | 21.3 | 22.9 |
| Technical Terms | 23.1 | 22.7 | 22.7 | 21.4 |
| Fluency Optimization | 25.1 | 24.6 | 24.7 | 21.9 |
| Cite Sources | 24.9 | 24.5 | 24.6 | 21.9 |
| Statistics Addition | 25.9 | 25.4 | 25.2 | 23.7 |
| **Quotation Addition** | 27.8 | 27.3 | **27.2** | **24.7** |

- Best methods improve on baseline by **+41%** (`Imp_pwc`) and **+28%** (Subjective Impression)
- Top performers — Cite Sources, Quotation Addition, Statistics Addition — gain **30–40%** on
  `Imp_pwc` and **15–30%** on Subjective Impression
- Stylistic changes (Fluency, Easy-to-Understand) also gain **15–30%**:
  "Generative Engines value not only content but also information presentation"
- **Keyword Stuffing scores *below* baseline.** Classic SEO does not transfer

### §5.1 Domain dependence
Authoritative → debate-style and historical queries. Cite Sources → factual questions.
Statistics Addition → 'Law & Government' and 'Opinion'. Quotation Addition → 'People &
Society', 'Explanation', 'History'.

### §5.2 Rank asymmetry — the most important finding for our design

> Cite Sources produced a **115.1% increase** in visibility for websites ranked **fifth** in
> the SERP, while **the visibility of the top-ranked website decreased by 30.3% on average**.

Framed by the authors as democratising: lower-ranked sites, typically small creators, gain most.

**For us this means retrieval position effects are large and non-monotonic, and a rank-only
control baseline is mandatory before any claim that content matters.**

### §5.3 Combinations
Pairs of the top-4 methods were tested. Best combination (**Fluency Optimization + Statistics
Addition**) beats any single method by **>5.5%**. Cite Sources is weak alone (8% below
Quotation Addition) but strong in combination (**average 31.4%**). *Caveat: run on a 200-example
subset due to cost, so these numbers differ from Table 1.*

### §6 GEO in the wild — Perplexity.ai

| Method | `Imp_pwc` | Subjective |
|---|---|---|
| No Optimization | 24.1 | 24.7 |
| Keyword Stuffing | 21.9 | 28.1 |
| Quotation Addition | **29.1** | 32.1 |
| Statistics Addition | 26.2 | **33.9** |

Quotation Addition **+22%**; Keyword Stuffing **−10%** vs baseline. Conclusions transfer across
engines — evidence the cross-model transfer extension is tractable.

### §9 Limitations (as stated by the authors)
- Methods may need to adapt as generative engines evolve, mirroring SEO
- Query distributions change over time; the benchmark needs updating
- **They did not evaluate how GEO methods affect conventional search rankings**
- Tagging may contain errors from subjective interpretation
- Larger context windows may reduce the impact of search rank over time

**There is no ethics or broader-impact section.** Section numbering runs 1, 2, 3, 4, 5, 7
(Related Work), 8 (Conclusion), 9 (Limitations), 10 (Acknowledgements).

---

## What this means for our project

### The novelty finding
**The paper contains zero occurrences of the word "predict"**, against 51 occurrences of
"visibility". It measures the *effect of modifications* on visibility. It never predicts
visibility *before* modification from query–document features.

That is precisely our project's framing. [INFERENCE] Our predictive task is therefore not
already solved by the foundational paper. This is a stronger novelty position than
`PROJECT_CONTEXT.md` originally assumed, and should be stated carefully — it is an absence in
*this* paper, not proof that no follow-up work has done it. A novelty check against post-2024
GEO literature is still required.

### What we take
- **`Imp_wc` and `Imp_pwc`** — directly implementable, no LLM judge needed. These are the
  "visibility metrics" the brief asks us to reproduce.
- **GEO-bench**, including the fact that it ships cleaned source text.
- **The pipeline configuration** as a reproduction target: top-5 sources, temp 0.7, 5 samples,
  5 seeds.
- **The nine methods** as the intervention menu, if we pursue the content-optimisation extension.
- **The rank asymmetry**, as the motivation for a rank-only control baseline.
- **The variance protocol** (5 samples × 5 seeds) as evidence that citation is stochastic and
  label stability must be measured.

### What we do not take
- **Subjective Impression / G-Eval** — requires an LLM-judge call per citation per response,
  sampled multiple times. Against a ~$500 budget this could dominate spend. Treat as optional
  and cost it before committing. See the kickoff agenda.

### Reproduction problem to flag
`gpt-3.5-turbo` is deprecated. A faithful reproduction needs an agreed substitute, and the
choice will affect results. This is a supervisor question, not something to decide silently.
