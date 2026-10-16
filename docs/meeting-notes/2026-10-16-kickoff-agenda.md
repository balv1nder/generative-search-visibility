# Kickoff meeting — agenda

**Date:** 2026-10-16 · **Supervisor:** Yannick Le Cacheux · **Project:** P11

> Printable agenda. Questions ordered by how much they unblock. After the meeting, record
> answers and propagate them per `docs/meeting-notes/README.md`.

## Opening — confirm our understanding (60 seconds)

> "We build a controlled generative search pipeline — retrieve candidates, have an LLM write a
> cited answer, parse which documents it cited. That gives us free supervised labels for every
> (query, document) pair. We then train an interpretable model to predict and explain citation,
> and optionally use it to suggest content rewrites. Is that the project?"

---

## 1 · Blocking — nothing can be built without these

1. **Which GEO-bench subset will you provide, and when?** Does the provided subset retain the
   cleaned source text? *(The GEO paper confirms the benchmark ships cleaned top-5 Google
   results as text, so no scraping should be needed — just confirming the subset keeps it.)*
   Is the Hugging Face path `GEO-Optim/geo-bench` the intended source? *(That path is
   dossier-sourced and unverified; the paper gives `generative-engines.com/GEO/`.)*
2. **What starter code and guidance exists?** [BRIEF] offers "initial code examples and
   guidance for the controlled generative-search pipeline" — we would rather not rebuild it.
3. **Which LLM should the pipeline use?** [BRIEF] permits commercial API or locally hosted open
   model. **The GEO paper used `gpt-3.5-turbo`, which is now deprecated — what do we substitute
   for a faithful reproduction?** This is a real reproducibility problem, not a preference.
   → *Proposal to put to him:* use a **local open-weights model as the primary workhorse**
   (free after setup, fixed weights, no endpoint drift, seeds controllable) and reserve API
   budget for a **cross-model transfer check** — which is itself one of the brief's listed
   extensions. This turns the budget constraint into a research contribution.
4. **Is the ~$500 per project or per student?** How do we access it — shared key, our own
   accounts, reimbursement? What would justify an increase?

## 2 · Midterm — a December evaluation is confirmed

The brief contains no timeline at all: zero mentions of "midterm", "deadline", "month" or
"assess". Everything here is `[UNSPECIFIED]`.

5. **What exactly is expected at the December midterm** — a report, a demo, a presentation,
   results, or a combination?
6. **Is this a fair December target?** Brief Levels 1–2 complete (pipeline producing labels +
   experimental dataset), a measured label-stability number, and a *preliminary* Level 3
   baseline — rather than full Levels 3–4.
7. **Would you accept a negative result** — content features adding nothing beyond retrieval
   rank — **as a valid finding?** Worth agreeing in advance. *(GEO's own data shows rank-5
   sources gaining 115.1% while rank-1 lost 30.3%, so position effects are large.)*
8. **Is the midterm graded, and individually or jointly?**
9. **What is the full timeline** — final deadline, any other checkpoints?

## 3 · Design decisions the papers surfaced

10. **What exactly do we predict?** [BRIEF] says "selected **and/or** cited", which does not
    settle it. GEO's own visibility metric is **continuous** — the share of answer text
    attributed to a source — not a binary citation flag. Options: binary `cited`; continuous
    `Imp_pwc`; or a four-way multi-class (not retrieved / retrieved-not-cited / cited-low /
    cited-high). **This determines the dataset schema, so it should be settled before we build.**
11. **Do we reproduce the Subjective Impression metric?** It needs a G-Eval LLM-judge call per
    citation per response, sampled repeatedly — potentially the largest single cost line.
    `Imp_wc` and `Imp_pwc` need no judge at all.
12. **Should we mirror GEO's exact setup** for the reproduction — top-5 sources, temperature
    0.7, 5 samples × 5 seeds?
13. **Which published GEO results should the reproduction target?** The brief says "a subset of
    existing GEO results and visibility metrics" without naming them.
14. **Is our novelty predicting visibility *before* modification?** The GEO paper contains zero
    occurrences of "predict" — it only measures the effect of modifications. Does that match
    how you see the contribution?
15. **Should we condition explicitly on retrieval rank**, given the rank asymmetry above?

## 4 · Scope and direction

16. If time forces a choice, **predictive model or content-optimisation system?**
17. **Is the intervention experiment in scope** — rewrite a document per the model's drivers,
    rerun the pipeline, measure the citation change?
18. **Has anyone measured run-to-run citation stability?**
19. **Is publication an aim?** Venue and deadline?
20. Should we attempt **real commercial engines**, or is the controlled setup sufficient?
    [BRIEF] marks this optional.

## 5 · Context and logistics

21. **Team size, and who is my teammate?**
22. **Has a previous student worked on this?** Can we see it?
23. **Is Manifold's commercial interest shaping direction?** Can code and results be
    **published openly**? *(Repository is private by default pending this answer.)*
24. Does Manifold have **real-world GEO data** that could validate whether controlled findings
    hold commercially?
25. **How should we handle the dual-use aspect?** This is in substance SEO for LLMs. *(The GEO
    paper has a Limitations section but no ethics or broader-impact section — there is a visible
    gap in the literature here.)*

## 6 · Closing

26. **What would a great outcome look like to you in six months?**
27. **What would disappoint you?**

---

## Answers

*(fill in during/after the meeting)*

## Propagation

*(list which files were updated — empty means the meeting has not been processed)*
