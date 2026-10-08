# Literature

Reading list for **P11**. This file establishes the literature **explicitly named by the project**
first. A broad literature search has not been performed and is not needed yet.

## Rules for this file

**Do not fabricate bibliographic information.** Every entry below records where its details came
from. Details taken from the brief are reliable as *the brief's wording*; details taken from the
dossier are third-party and **unverified by us**. Before any of these are cited in a report,
**verify them against the actual publication**.

**Verification status** is tracked per entry:
- `brief-stated` — exactly as written in the official project brief
- `dossier-stated` — from the dossier's P11 section; not in the brief; **unverified**
- `verified` — we have checked the detail against the actual paper (none yet)

---

## Tier 1 — Named in the project brief

These two are the only papers the brief cites. Both are **High** priority.

### 1. GEO: Generative Engine Optimization

- **Authors (brief):** Aggarwal, P., Murahari, V., Rajpurohit, T., Kalyan, A., Narasimhan, K. & Deshpande, A.
- **Venue (brief):** Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, 2024
- **Verification status:** `brief-stated`
- **Additional identifier:** `dossier-stated` — arXiv:2311.09735. **Unverified.**

**Why it is relevant, according to the brief.** The brief states the project "will build upon
existing research on GEO, in particular GEO-bench, a benchmark containing 10,000 queries and
associated web sources." [DOSSIER] identifies this paper as the source of GEO-bench and "the
foundational paper".

**What we need to learn from it.**
- What exactly GEO-bench contains: query provenance, document provenance, fields, size, licence.
- How the paper defines and measures **visibility** — the brief requires reproducing "a subset of
  existing GEO results and visibility metrics", and the brief itself never enumerates them, so
  this paper is our main route to knowing what the reproduction target is.
- Which specific effects/results are reported, so we can choose a defensible reproduction subset.
- What content modifications the paper claims improve visibility, and how it validates them.
- How its pipeline is constructed — the brief asks for a pipeline "inspired by existing literature".

**Priority: High.** Blocking for Phases 1–3 of `RESEARCH_PLAN.md`.

---

### 2. Evaluating Verifiability in Generative Search Engines

- **Authors (brief):** Liu, N. F., Zhang, T., Liang, P. et al.
- **Venue (brief):** Findings of the Association for Computational Linguistics, 2023
- **Verification status:** `brief-stated`
- ⚠️ **Known discrepancy.** The dossier refers to this paper's venue as *Findings of EMNLP 2023*
  in one place and *Findings of ACL 2023* in another; the brief says only "Findings of the
  Association for Computational Linguistics, 2023". **Do not resolve this by guessing** — check
  the actual publication before citing it.

**Why it is relevant, according to the brief.** Listed as one of the project's two references.
[DOSSIER] describes it as "the citation-quality side of the same problem, and methodologically
the more careful of the two."

**What we need to learn from it.**
- How to evaluate whether a generated statement is actually supported by the source it cites —
  directly relevant to the correctness of our citation-parsing and labelling step.
- Its measurement methodology for citation precision/recall, which may inform our evaluation protocol.
- What is known about how real generative search engines cite, which is our point of comparison
  for the controlled setup.

**Priority: High.**

---

## Tier 2 — Anticipated by the brief, not yet named

The brief states: *"Additional recent literature on generative search, retrieval,
learning-to-rank and LLM-based evaluation will be investigated during the project."*

So four areas are explicitly in scope without specific papers attached:

| Area | Priority | Why |
|---|---|---|
| Generative search | High | The system we are building |
| Retrieval | High | The pipeline's first stage, and the source of the brief-named `retrieval score` and `ranking position` features |
| Learning-to-rank | Medium | Named in the brief as a possible advanced direction only |
| LLM-based evaluation | Medium | Relevant to both labelling quality and any LLM-as-judge component |

**Task — Medium priority.** Novelty check: what has been published on GEO **since** Aggarwal et al.?
[DOSSIER] notes the field is fast-moving, that several follow-up papers already exist, and that
"several 2026 papers on GEO citation failure and GEO measurement have appeared". We have not
verified any such paper. This check should produce a short, dated note in this directory.

---

## Tier 3 — Suggested by the dossier only

**None of the following is named in the project brief.** They are the dossier's recommendations.
All details below are `dossier-stated` and **unverified by us**. Read them only if the direction
we choose actually needs them — several map to optional extensions we may never pursue.

| Paper (as stated by the dossier) | Dossier's stated relevance | Our priority | Gate |
|---|---|---|---|
| Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*, NeurIPS 2020 | "the architecture you are building" | **Medium** | Useful background for Phase 2 regardless of direction |
| Gao et al., *Enabling Large Language Models to Generate Text with Citations* (ALCE), EMNLP 2023 | "the standard benchmark for citation generation and directly relevant to your labelling step" | **Medium** | Most relevant Tier-3 item — it touches the labelling step, which gates everything |
| Karpukhin et al., *Dense Passage Retrieval*, EMNLP 2020 | dense retrieval | **Medium** | Needed only if we use a dense retriever — currently undecided |
| Nogueira & Cho, *Passage Re-ranking with BERT*, 2019 | "the cross-encoder approach" | **Low** | Only if we pursue the transformer-comparison extension |
| Burges, *From RankNet to LambdaRank to LambdaMART*, MSR-TR-2010-82 | learning-to-rank | **Low** | Only if we pursue the learning-to-rank extension |
| Thakur et al., *BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models*, NeurIPS D&B 2021 | "retrieval evaluation practice" | **Low** | Background for evaluation design |

---

## Datasets and resources

| Resource | Source of the claim | Status |
|---|---|---|
| **GEO-bench** — "a benchmark containing 10,000 queries and associated web sources" | `brief-stated` | The brief says a subset "will be provided or identified at the beginning of the project" — confirm with supervisor |
| GEO-bench hosted on Hugging Face at `GEO-Optim/geo-bench` | `dossier-stated` | **Unverified.** Confirm with supervisor before relying on it — see `TODO.md` |

---

## Notes directory

Per-paper reading notes go in this directory as `NN-short-name.md`, one file per paper. Each note
should record: what the paper does; what we take from it for P11; what we deliberately do not
take; and the **verified** bibliographic record once checked.

No notes have been written yet.
