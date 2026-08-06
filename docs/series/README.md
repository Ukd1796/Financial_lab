# Designing an Adaptive System

A writing series about an adaptive trading system I built for Indian equities, one
that runs five strategies together, and the more general lesson underneath it: **in a
system of any real complexity, the architecture decides the behavior more than any
individual component does.**

Each post takes one place where what the system *actually did* diverged from what I
*designed it to do*, and the engineering lesson underneath. The opener lays out the
architecture; every episode after it is one of the surprises the diagnostic turned up.

This README is the general index and idea board. Each episode is drafted in its own
file (`episode-0N-*.md`) as it gets written.

## Roadmap

| # | Title | What it shows | Draft |
|---|---|---|---|
| 1 | Architecture Matters More Than Algorithms | Design judgment (the anchor) | [episode-01-architecture.md](./episode-01-architecture.md) |
| 2 | When Diversification Is a Config Lie | Behavior ≠ config | — |
| 3 | Behavior Lives in Execution Order | Emergent behavior | — |
| 4 | Your Pipeline Is a Decision | Input selection is the decision | — |
| 5 | Intuitive Filters, Counterintuitive Results | Feature engineering backfires | — |
| 6 | Correctness Is Scale Dependent | Right for one, wrong for many | — |
| 7 | Every Deliberate Tradeoff Has a Hidden Cost | Deliberate lag | — |
| 8 | Knowing When to Stop Optimizing | The system is the constraint | — |

## Assets

- `architecture-diagram.svg` — publishing-grade system diagram (hero image for Episode 1).
- `architecture-diagram.excalidraw` — editable version for Excalidraw.
- `architecture-diagram.mmd` — Mermaid source (renders on GitHub).

## Voice notes

- Write for engineers, not traders. Every paragraph should teach someone who doesn't
  care about finance.
- Strong opinions, stated plainly. End each section with one memorable lesson.
- No dashes in the prose.
