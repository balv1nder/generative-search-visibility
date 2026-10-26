# src/citation

Placeholder. No implementation yet — see `RESEARCH_PLAN.md` and `CLAUDE.md`.
Implementation is deliberately deferred until the blocking supervisor questions in `TODO.md`
are answered, in particular what starter code the supervisor already has.

**Intended responsibility.** Parse which candidate documents the generated answer actually cited.

**This is the highest-leverage component in the repository.** Every label in the project is
produced here; a silent error contaminates every downstream result. It needs tests and manual
spot-checking before any dataset is generated at scale.
