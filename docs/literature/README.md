# Literature

Reading list and notes for **P11**.

## Files

| File | Contents |
|---|---|
| `review-outline.md` | The adopted literature-review structure, with three added sections |
| `01-geo-aggarwal-2024.md` | GEO (KDD 2024) — the anchor paper. Full section-wise notes |
| `02-liu-verifiability-2023.md` | Liu et al. (Findings of EMNLP 2023) — citation quality |
| `03-supporting-literature.md` | ALCE, RAG, DPR, BERT re-ranking, LambdaMART, BEIR |

## Rules for this directory

**Do not fabricate bibliographic information.** Every field carries a status:

- `verified` — confirmed from a page actually fetched; the source is named in the note
- `brief-stated` — exactly as written in the official project brief
- `dossier-stated` — from the dossier's P11 section; third-party, not confirmed
- `UNVERIFIED` — could not be confirmed. **Must not be cited until checked.**

---

## Tier 1 — Named in the project brief

### 1. Aggarwal et al., *GEO: Generative Engine Optimization* — **Priority: High**

`verified` — KDD 2024, arXiv:2311.09735. Full details and section-wise summary in
`01-geo-aggarwal-2024.md`.

The foundational paper and the source of GEO-bench. Defines the visibility metrics the brief
asks us to reproduce, the nine optimization strategies, and the experimental pipeline we are
replicating.

**Key facts established by reading it (2026-10-16):**
- GEO-bench: **10K queries**, 8K/1K/1K split, nine source datasets, 25 domains
- **GEO-bench ships cleaned full document text** — *"Each query is augmented with the cleaned
  text content of the top 5 search results from the Google search engine."* No scraping needed
- Pipeline: top-5 Google sources, `gpt-3.5-turbo`, temperature 0.7, 5 samples × 5 seeds
- Best methods: **+41%** on Position-Adjusted Word Count, **+28%** on Subjective Impression
- **Keyword Stuffing performs below baseline** — classic SEO does not transfer
- **Rank asymmetry:** Cite Sources gave **+115.1%** for rank-5 sources while the top-ranked
  source **lost 30.3%** on average
- **The paper never attempts prediction** — zero occurrences of "predict" against 51 of
  "visibility". It measures the effect of modifications, not visibility before modification

### 2. Liu, Zhang & Liang, *Evaluating Verifiability in Generative Search Engines* — **Priority: High**

`verified` — **Findings of EMNLP 2023**, arXiv:2304.09848. Details in
`02-liu-verifiability-2023.md`.

> **Venue discrepancy RESOLVED.** The brief says "Findings of the Association for Computational
> Linguistics, 2023"; the dossier said EMNLP in one place and ACL in another. Confirmed as
> **Findings of EMNLP 2023** on 2026-10-16.

Defines citation recall and citation precision. Audits Bing Chat, NeevaAI, Perplexity.ai and
YouChat: only **51.5%** of generated sentences are fully supported by citations, and only
**74.5%** of citations support their statement.

*The dossier reported 74%; the verified figure is 74.5%.*

**Still to do:** read the full paper for methodology (annotator counts, query counts, rating
scales) — currently `UNVERIFIED`.

---

## Tier 2 — Anticipated by the brief

[BRIEF] *"Additional recent literature on generative search, retrieval, learning-to-rank and
LLM-based evaluation will be investigated during the project."*

| Area | Priority | Why |
|---|---|---|
| Generative search | High | The system we are building |
| Retrieval | High | The pipeline's first stage, and the source of brief-named features |
| LLM-based evaluation | Medium | Bears on labelling quality and any LLM-as-judge component |
| Learning-to-rank | Medium | A possible advanced direction only |

**Outstanding task — novelty check.** What has been published on GEO *since* Aggarwal et al.?
[DOSSIER] notes the field moves fast and claims several 2026 papers on GEO citation failure and
measurement have appeared. **We have verified no such paper.** This check matters more now that
we know the foundational paper leaves the predictive framing open — the question is whether a
follow-up has closed it. Produce a short dated note here.

---

## Tier 3 — Supporting literature

Not named in the brief; suggested by [DOSSIER]. Full verified details in
`03-supporting-literature.md`.

| Paper | Priority | Gate |
|---|---|---|
| **Gao et al., ALCE** (EMNLP 2023) | **High** | Promoted from Medium — it specifies our citation-parsing and labelling step |
| Lewis et al., RAG (NeurIPS 2020) | Medium | Architecture background, needed regardless of direction |
| Thakur et al., BEIR (NeurIPS D&B 2021) | Medium | Sets our retrieval reporting protocol (zero-shot, nDCG@10) |
| Karpukhin et al., DPR (EMNLP 2020) | Medium | Only if we use a dense retriever — undecided |
| Nogueira & Cho (arXiv 2019) | Low | Only for the transformer-comparison extension. **Venue UNVERIFIED** |
| Burges, LambdaMART (MSR-TR-2010-82) | Low | Only for the learning-to-rank extension |

---

## Datasets and resources

| Resource | Claim | Status |
|---|---|---|
| **GEO-bench** — 10K queries, nine source datasets | `verified` from the GEO paper | Subset to be provided by supervisor — confirm |
| GEO-bench ships cleaned top-5 source text | `verified` from the GEO paper §3.2 | Removes the scraping risk |
| Hosted on Hugging Face at `GEO-Optim/geo-bench` | `dossier-stated` | **Still unverified.** The paper gives `generative-engines.com/GEO/` |

---

## Outstanding verification tasks

- [ ] Liu et al. — read in full; fill in methodology currently marked `UNVERIFIED`
- [ ] Nogueira & Cho — confirm whether formally published, or cite as preprint
- [ ] RAG and BEIR — fetch proceedings page numbers
- [ ] BEIR — pick arXiv ("Heterogenous") or proceedings ("Heterogeneous") spelling, use consistently
- [ ] Confirm the GEO-bench Hugging Face path with the supervisor
- [ ] Novelty check: post-2024 GEO literature
