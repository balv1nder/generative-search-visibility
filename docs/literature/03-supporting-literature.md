# Supporting literature

Six papers not named in the project brief. [BRIEF] anticipates them in principle —
*"Additional recent literature on generative search, retrieval, learning-to-rank and LLM-based
evaluation will be investigated during the project"* — and [DOSSIER] suggested this specific
set.

All bibliographic details below were verified by fetching arXiv, ACL Anthology or publisher
pages on 2026-10-16. Fields that could not be confirmed are marked `UNVERIFIED` and **must not
be cited until checked**.

---

## 1. Gao et al. — ALCE ⭐ highest priority of this group

| Field | Value | Status |
|---|---|---|
| Title | Enabling Large Language Models to Generate Text with Citations | `verified` |
| Authors | Tianyu Gao, Howard Yen, Jiatong Yu, Danqi Chen | `verified` |
| Venue | Proceedings of EMNLP 2023, **pp. 6465–6488** | `verified` |
| DOI | 10.18653/v1/2023.emnlp-main.398 | `verified` |
| arXiv | 2305.14627 (24 May 2023; rev. 31 Oct 2023) | `verified` |
| Code | `github.com/princeton-nlp/ALCE` | `verified` |

**What it does.** Proposes **ALCE** (*Automatic LLMs' Citation Evaluation*), the first
reproducible benchmark for LLM generation with inline citations. Prior work depended on
commercial search engines and human evaluation, blocking reproducibility — ALCE replaces this
with automatic metrics validated against human judgement. Systems must retrieve evidence and
generate an answer whose sentences carry inline citations. Headline: even the best systems
"lack complete citation support 50% of the time" on ELI5.

**Three evaluation axes.**
1. **Fluency** — MAUVE over question + output, truncated to 100 words. Authors note it is
   length-sensitive and can be unstable.
2. **Correctness** — dataset-specific. ASQA: exact-match recall of gold short answers.
   QAMPARI: precision/recall against gold entity lists (recall = 100% if ≥5 correct).
   ELI5: claim recall over generated sub-claims verified by NLI.
3. **Citation quality** — recall and precision, below.

**Citation quality mechanics — the part we should copy.**
- Output is **segmented by sentence**; each sentence `s_i` is a statement with citation set
  `C_i`. The authors argue "almost all sentences that LLMs output provide valuable information
  and require citations", so essentially every sentence is treated as citation-worthy.
  (QAMPARI uses each generated list entity as a statement instead.)
- **At most 3 citations per statement.** Multiple cited passages are **concatenated**
  (newline-separated) and judged jointly.
- Entailment judge `φ` is **TRUE**: a T5-11B fine-tuned on SNLI, MNLI, FEVER, SciTail, PAWS and
  VitaminC. Prompted `premise: {PREMISE} hypothesis: {HYPOTHESIS}`, outputs 1 for entailment.
- **Citation recall** = 1 for a statement iff it has ≥1 citation **and**
  `φ(concat(C_i), s_i) = 1`. Averaged over statements.
- **Citation precision**: citation `c_ij` is **irrelevant** iff `φ(c_ij, s_i) = 0`
  (alone it doesn't support the statement) **and** `φ(concat(C_i \ {c_ij}), s_i) = 1`
  (the rest still fully support it). Scored only where citation recall = 1. The two-condition
  design deliberately tolerates jointly-but-not-individually supporting citations.
- **Datasets:** ASQA and QAMPARI over a 21M-passage corpus; ELI5 over the 899M-passage Sphere
  corpus. 1,000 randomly selected evaluation examples each.

**Relevance to us — this is our labelling step, already specified.** The
sentence-segmentation and citation-parsing procedure is exactly the "parse which documents got
cited" component in `src/citation/`. [RECOMMENDATION] Adopt the ≤3-citations prompt constraint
and the concat-then-entail convention verbatim: it saves us designing them, and it makes our
citation-quality numbers comparable to published work. Running citation recall/precision over
our own generated answers is the practical, automatic substitute for Liu et al.'s human audit.

**Priority: High** — promoted above its [DOSSIER] "Medium", because it bears directly on the
component that manufactures every label in the project.

---

## 2. Lewis et al. — Retrieval-Augmented Generation

| Field | Value | Status |
|---|---|---|
| Title | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks | `verified` |
| Authors | Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, Sebastian Riedel, Douwe Kiela | `verified` |
| arXiv | 2005.11401 (22 May 2020) | `verified` |
| Venue | arXiv comments field states "Accepted at NeurIPS 2020" | `verified` |
| Proceedings page numbers | — | `UNVERIFIED` |

Combines parametric memory (pre-trained seq2seq) with non-parametric memory (dense Wikipedia
index via a neural retriever). Retriever is DPR; generator is BART-large. Two formulations:
**RAG-Sequence** uses the same document for every target token; **RAG-Token** can use a
different document per token.

**Key contribution:** treating the retrieved document as a latent variable marginalised out
during generation, so query encoder and generator train end-to-end on downstream supervision
alone. The **document encoder and index stay fixed**.

**Relevance:** the canonical citation for the retrieve-then-generate architecture we are
building. The fixed-index design is the standard justification for treating the retriever as a
frozen component while studying downstream behaviour — which is what our controlled engine does.
**Priority: Medium.**

---

## 3. Karpukhin et al. — Dense Passage Retrieval

| Field | Value | Status |
|---|---|---|
| Title | Dense Passage Retrieval for Open-Domain Question Answering | `verified` |
| Authors | Vladimir Karpukhin, Barlas Oğuz, Sewon Min, Patrick Lewis, Ledell Wu, Sergey Edunov, Danqi Chen, Wen-tau Yih | `verified` |
| Venue | EMNLP 2020, **pp. 6769–6781** | `verified` |
| DOI | 10.18653/v1/2020.emnlp-main.550 | `verified` |
| arXiv | 2004.04906 (v1 10 Apr 2020; v3 30 Sep 2020) | `verified` |

Dual-encoder: two independent BERT-base-uncased encoders (768-d, `[CLS]` pooling), similarity
as **dot product**, trained with negative log-likelihood of the positive passage. Reports
**9–19% absolute improvement** over Lucene-BM25 in top-20 passage retrieval accuracy.

**Key contribution:** a dual-encoder trained on few question–passage pairs suffices, via
**in-batch negatives** (a B×B similarity matrix gives B² pairs per batch) plus **one BM25 hard
negative** per question. FAISS for the inference-time index.

**Relevance:** the dense retriever we would realistically use for `src/retrieval/`. Also
motivates the similarity-score features (dot product, BM25 score) feeding the interpretable
classifier. **Priority: Medium** — needed only if we use a dense retriever, currently undecided.

---

## 4. Nogueira & Cho — Passage Re-ranking with BERT

| Field | Value | Status |
|---|---|---|
| Title | Passage Re-ranking with BERT | `verified` |
| Authors | Rodrigo Nogueira, Kyunghyun Cho | `verified` |
| arXiv | 1901.04085 (v1 13 Jan 2019; v5 14 Apr 2020) | `verified` |
| **Venue** | No venue or comments field on the arXiv page | **`UNVERIFIED`** |
| Code | `github.com/nyu-dl/dl4marco-bert` | `verified` |

> ⚠️ **Cite as an arXiv preprint, 2019** until a published venue is confirmed.

BERT as a query–passage **cross-encoder** for re-ranking in a two-stage pipeline (BM25
candidates → BERT re-ranking). State of the art on TREC-CAR and top of the MS MARCO passage
leaderboard at the time, **+27% relative MRR@10** over the previous best.

**Key contribution:** establishing the BERT cross-encoder (query and passage jointly encoded,
relevance as a classification output) as the standard second-stage re-ranker.

**Relevance:** justifies inserting a re-ranking stage so the LLM sees a controlled, ordered
candidate set; the re-ranker score is an obvious feature. The cross-encoder is also the natural
"advanced model" for the brief's Level-5 transformer comparison. **Priority: Low** until that
extension is chosen.

---

## 5. Burges — From RankNet to LambdaRank to LambdaMART

| Field | Value | Status |
|---|---|---|
| Title | From RankNet to LambdaRank to LambdaMART: An Overview | `verified` |
| Author | Chris J.C. Burges | `verified` |
| Report | **MSR-TR-2010-82**, Microsoft Research Technical Report | `verified` |
| Date | June 2010 | `verified` |
| PDF | `microsoft.com/en-us/research/wp-content/uploads/2016/02/MSR-TR-2010-82.pdf` | `verified` |

Tutorial-style report consolidating three learning-to-rank algorithms. Derives RankNet (pairwise
neural ranker over a probabilistic cost on document pairs), then LambdaRank, then LambdaMART —
"the boosted tree version of LambdaRank". Notes an ensemble of LambdaMART rankers won Track 1 of
the 2010 Yahoo! Learning To Rank Challenge.

**Key contribution:** the **λ-gradient** — specify gradients directly, scaled by the change in
the target IR metric from swapping a pair, rather than deriving them from a differentiable
loss. This allows non-smooth ranking metrics to be optimised.

**Relevance:** the reference point for "learn a model over query/document features to predict
ranking outcomes". Our interpretable classifier sits in this lineage but simpler; citing it lets
us position a transparent model against the standard feature-based LTR paradigm.
**Priority: Low** until the learning-to-rank extension is chosen.

---

## 6. Thakur et al. — BEIR

| Field | Value | Status |
|---|---|---|
| Title | BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | `verified` |
| Authors | Nandan Thakur, Nils Reimers, Andreas Rücklé, Abhishek Srivastava, Iryna Gurevych | `verified` |
| arXiv | 2104.08663 (17 Apr 2021; v4 21 Oct 2021) | `verified` |
| Venue | NeurIPS 2021 Datasets and Benchmarks Track | `verified` |
| Proceedings page numbers | — | `UNVERIFIED` |
| Code | `github.com/UKPLab/beir` | `verified` |

> ⚠️ **Title spelling differs between versions.** arXiv reads "**Heterogenous**"; the NeurIPS
> proceedings page reads "**Heterogeneous**". Use the proceedings spelling when citing the
> published version.

**18 English datasets across 9 heterogeneous retrieval tasks** (fact checking, citation
prediction, duplicate-question retrieval, argument retrieval, news retrieval, QA, tweet
retrieval, biomedical IR, entity retrieval), evaluating 10 systems spanning lexical, sparse,
dense, late-interaction and re-ranking architectures. Finding: consistent cross-dataset
performance is hard; **BM25 is a robust baseline**; re-ranking and late-interaction give the
best average zero-shot performance at high computational cost.

**Evaluation practice it establishes:**
- **Strictly zero-shot** — models trained elsewhere (typically MS MARCO), evaluated with no
  in-domain training data
- **A single standardised metric: nDCG@10**, chosen as "a good balance suitable for both tasks
  involving binary and graded relevance judgements"
- A shared framework so lexical, dense and re-ranking systems are compared on identical corpora

**Relevance:** supplies the protocol (don't tune the retriever on your eval queries) and the
metric (**nDCG@10**) for reporting our retrieval stage comparably to the literature.
**Priority: Medium** — it shapes how we report Phase 3 retrieval numbers.

---

## Outstanding verification tasks

| Item | Action |
|---|---|
| Nogueira & Cho venue | Check whether it was ever formally published; otherwise cite as preprint |
| RAG proceedings pages | Fetch the NeurIPS 2020 proceedings entry |
| BEIR proceedings pages | Fetch the NeurIPS D&B 2021 proceedings entry |
| BEIR title spelling | Decide arXiv vs proceedings version and use one consistently |
| Liu et al. methodology | Read the full paper; see `02-liu-verifiability-2023.md` |
