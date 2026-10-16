# Meeting notes

One file per meeting, named `YYYY-MM-DD-topic.md`.

## The rule that matters

**Answers do not live here.** A supervisor answer recorded only in a meeting note is lost
knowledge — nobody reads old meeting notes when deciding what to build.

Per `CLAUDE.md`, every answer propagates:

| What was learned | Goes to |
|---|---|
| A fact about what the project requires | `PROJECT_CONTEXT.md` — update the fact, remove it from *Open Questions* |
| A decision now settled by the supervisor | `DECISIONS.md` — new row, evidence "supervisor, <date>", status `Fixed` |
| A resolved question or a new task | `TODO.md` — tick the box or add the task |
| A change to staging or scope | `RESEARCH_PLAN.md` |

The meeting note stays as the dated record of *what was said*. The other files carry *what is
now true*. Keep the note short; put the effort into propagation.

## Convention

Each note should contain: date, attendees, the questions asked, the answers given, and an
explicit **Propagation** section listing which files were updated as a result. If the
propagation section is empty, the meeting has not been processed yet.
