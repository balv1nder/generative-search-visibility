# Liu, Zhang & Liang — Evaluating Verifiability in Generative Search Engines

The second of the two papers named in the project brief. Methodologically the more careful
of the pair, and the source of the citation-quality vocabulary this project needs.

## Verified bibliographic record

| Field | Value | Status |
|---|---|---|
| Title | Evaluating Verifiability in Generative Search Engines | `verified` |
| Authors | Nelson F. Liu, Tianyi Zhang, Percy Liang | `verified` |
| Venue | **Findings of the Association for Computational Linguistics: EMNLP 2023** | `verified` |
| arXiv | 2304.09848 (v1 19 Apr 2023; v2 23 Oct 2023) | `verified` |
| Companion code | `github.com/nelson-liu/evaluating-verifiability-in-generative-search-engines` | `verified` as listed in search results; not fetched |

> ### Venue discrepancy — RESOLVED
> The project brief cites this as "Findings of the Association for Computational Linguistics,
> 2023". The dossier gave *Findings of EMNLP 2023* in one place and *Findings of ACL 2023* in
> another. `docs/literature/README.md` previously flagged this as unresolved and warned against
> guessing.
>
> **It is Findings of EMNLP 2023**, confirmed from the arXiv record and the Semantic Scholar
> entry on 2026-10-16. Cite it that way.

---

## Summary

### The concept: verifiability
A trustworthy generative search engine must cite **comprehensively** and **accurately**. The
paper decomposes this into two metrics that have since become standard vocabulary:

- **Citation recall** — "all statements are fully supported by citations"
- **Citation precision** — "every cite supports its associated statement"

### Method
Human evaluation auditing **four deployed generative search engines**:

1. Bing Chat
2. NeevaAI
3. Perplexity.ai
4. YouChat

Queries drawn from a deliberately diverse set of sources, including historical Google user
queries and dynamically-collected open-ended questions from Reddit.

*Annotator counts, query counts and rating scales are not stated on the abstract page and were
not verified — read the full paper before quoting methodology details.* `UNVERIFIED`

### Headline findings

| Metric | Result |
|---|---|
| Generated sentences fully supported by citations | **51.5%** |
| Citations that support their associated sentence | **74.5%** |

The authors' framing: responses "are fluent and appear informative, but frequently contain
unsupported statements and inaccurate citations, increasing their potential to mislead users."

> The dossier reported this as "74%". The verified figure is **74.5%**.

---

## Why it matters to our project

### It separates two things our label conflates
Our pipeline produces a binary `cited` label. This paper shows that **being cited and being
supported are different properties**: roughly a quarter of real citations do not support the
statement attached to them.

[INFERENCE] So `cited = 1` is a **visibility signal, not a correctness signal**. A document can
win visibility while contributing nothing factually. Our predictive model will happily learn
whatever drives citation, including whatever drives *spurious* citation.

### It is the empirical basis for the dual-use limitations section
If citation does not reliably track support, then optimising content for citation is not the
same as optimising for usefulness — and a content-optimisation system could increase visibility
while degrading answer quality. The brief does not raise this; [DOSSIER] recommends a
limitations discussion; this paper supplies the evidence for it.

### It gives us a quality check we can actually run
[RECOMMENDATION] Measuring citation precision/recall on our own generated answers tells us
whether our controlled pipeline behaves like deployed engines, and gives a sanity check on the
labels before they are used as classifier targets. The operational machinery for doing this
automatically is in ALCE — see `03-supporting-literature.md`.

### What we take
- The **citation recall / citation precision** vocabulary, used consistently in our report
- The **51.5% / 74.5%** figures as the deployed-engine reference point
- The **four audited engines** as the natural comparison set, if the optional
  commercial-engine extension is pursued
- The verifiability framing for our limitations section

### What we do not take
- The **human-evaluation methodology**. It is expensive and outside our budget and timeline.
  ALCE's automatic NLI-based equivalent is the practical substitute.

## Still to read in full
This note is built from the abstract and verified metadata. Before citing methodology details
(annotation protocol, per-engine breakdown, query counts), **read the full paper** and update
this file. Items currently marked `UNVERIFIED` above must not appear in the report until then.
