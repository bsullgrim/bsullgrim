---
layout: single
title: "Requirements a pipeline can verify"
excerpt: "How I rebuilt a 32-line informal requirements list for a guidance-system simulation into a traced, reviewed draft specification in which requirements say how they are verified and, where automation fits, when a CI pipeline would check them."
permalink: /work/sim-requirements-ci/
header:
  teaser: /assets/images/card-sim-ci.png
toc: true
toc_sticky: true
---

## The problem

The requirements for a guidance-system simulation I work on began as a 32-line informal list that mostly described how the simulation should be built and managed, including a line asking for continuous integration testing that named no trigger, scope, or pass criterion. My task lead wanted requirements the team's CI pipeline could verify, as many as possible by test, and would not commit to performance numbers while the real system was in development, which left open how to judge fidelity without data from that system.

## Constraints

The specification is an unbaselined draft whose quantities are all placeholders, chosen so requirements can be reviewed, so I kept placeholder, derived, and agreed values as separately marked states. The pipeline runs on shared runners whose start times and load the team doesn't control, which ruled out timing checks that could fail a merge for reasons unrelated to the change.

## What I did

I worked the approach out in AI-assisted sessions, where the assistant drafted much of the text and built the workbook and scripts to my direction while I decided what went in and took each revision through review with the task lead and simulation lead.

I aligned the set with ISO/IEC/IEEE 29148 and the INCOSE Guide for Writing Requirements and added the project's 58-item use case catalogue as a second source, since it described what the simulation does. Every source line carries a recorded disposition, every requirement records its origin, and each traces forward to a use case or carries a status explaining why not, as a constraint, a derived requirement, or a deletion candidate.

The two leads marked nearly all 127 requirements in the draft to keep, reword, or remove, and I actioned their review into a revision that withdrew 46 and added one by splitting a requirement in two, leaving 82. Each withdrawal went to a register with its last text, basis, reviewers, and the requirement now carrying its content, and because no identifier was reused, every review comment still resolves against its row, and a later team pass restored four of them from that register, bringing the current draft to 86.

Asking for as many tests as possible joined two separate attributes, since some requirements verified by test need a scenario run too long for a merge gate while some verified by inspection reduce to a script checking every file header. I kept the verification method as the contractual letter and added a CI gate field for when an automated check runs and an artifact field for what it asserts, so a requirement is pipeline-ready once it has both. I proposed gates for 42 of the 82 (26 per merge, 14 nightly, one on release, and one at a milestone), kept timing checks nightly so runner load couldn't fail merges, and wrote a requirement making per-merge checks blocking.

I then catalogued the pipeline's 47 jobs against the requirements each appeared to evidence, with a confidence on every mapping. Most analysis-stage jobs generated plots, which pass whenever the plot is produced unless they assert something inside, so that stage produced material for review and gated nothing, and nothing covered the fidelity requirements. A use case categorized as optional extra scope ran on every commit, which kept its requirements mandatory, and the pipeline deliberately let one compliance check fail without blocking, which the blocking requirement as drafted prohibited, so the team kept the rule binding and added a recorded-waiver path.

I separated fidelity, which compares the simulation against the design already held in the system model, from accuracy, which compares output against reference truth and must wait for real-system data. The staged approach checks that models conform to the design, matches closed-form answers under simplified conditions, enforces conservation and dimensional invariants, and holds fidelity metrics to a no-degradation ratchet whose baseline moves only with a recorded justification, trading how good is good enough for whether the model got worse, while accuracy thresholds wait on a stated trigger. Review cut two of the seven stages I brought, and none of the rest is implemented in the pipeline yet.

The AI-assisted consistency checks cover referential integrity in both directions, requirement text against register values, near-duplicates, and revision-to-revision changes, most written in answer to a defect the work had produced and each required to fail on a planted defect before a clean result counted. I also directed an AI-assisted rewrite of an earlier draft V&V plan to carry what the requirements delegate to it, and it remains a draft.

## How I knew it worked

Because the specification is a draft, my evidence concerns whether the definition work holds together, and none of it yet shows the simulation meeting the requirements. The checks caught defects in the work itself, including a register value changed without its requirement text during the build that introduced the value check, and 51 referential findings in an already-issued revision. The reviewed revision ran clean on every check, and its coverage states the gaps, with 41 of the 58 use cases covered, 8 on candidate mappings, 3 out of scope by reviewer statement, and 6 uncovered.

## What went wrong and what I learned

The revision that introduced the separation of method from automation also moved fourteen requirements from inspection to test because their evidence was automated, breaking the rule in the change log that stated it, and nine requirements in the reviewed draft still carry that change. Nothing caught it because no check reads the method letter, and the proposed control is a column naming the clause each letter rests on, with relettering left to the leads.

I first mapped the pipeline by job name from a screenshot, until a job log showed that a job I had read as a plain scenario run compared outputs against a truth reference, using thresholds that as far as I know rest on engineering judgment. That narrowed the fidelity gap to the acceptance threshold, and I now treat a mapping by name as triage to confirm against configuration and logs.

Early on, a change log claimed a sizing conflict was resolved by a requirement whose value did not resolve it, because each number looked defensible alone while the set was inconsistent, and the fix was formula-derived quantities and the value check. The review later retired most of that sizing once the simulation lead replaced a baseless campaign size, and I would now get those real inputs before building on placeholders.

## An example you can look at

The workbook isn't public, so here are invented requirements for a generic simulation, written to the same pattern, with every value a placeholder and none of the text drawn from the program. The verification method stays the contractual letter, and the gate and the check say separately when an automated check runs and what it asserts.

{% include figure image_path="/assets/images/card-sim-ci.png" alt="Gate ladder from per-merge through nightly and on-release to milestone, with the contractual method letter set apart because it does not set the gate" caption="Where a check runs depends on how long it takes and when its answer is needed, and the contractual method letter stays separate from that choice." %}

| ID | Requirement *(invented)* | Method | CI gate | What the check asserts |
|---|---|---|---|---|
| EX-01 | The simulation shall reject a configuration file that omits a required parameter, naming the missing parameter in its error message. | T | Per merge | A unit test feeds a file missing one parameter and asserts the error names it |
| EX-02 | Every source file shall begin with the project's standard header block. | I | Per merge | A lint script reads each file's opening lines and fails on any missing field |
| EX-03 | A nominal scenario shall run to completion within [placeholder] times the duration of the accepted baseline run. | T | Nightly | The ratio of run time to the baseline's, kept off merges so shared-runner load can't fail them |
| EX-04 | In the free-flight reference case, total energy shall be conserved to within [placeholder]. | A | Nightly | An invariant check on the energy history against the analytic answer |
| EX-05 | Fidelity metrics shall not degrade from the accepted baseline without a recorded justification. | T | On release | A comparison against the stored baseline that only a justified re-baseline can move |

EX-02 shows why the two fields are separate, since an inspection requirement can be the cheapest thing to automate on every merge, while EX-03 is verified by test and still has no business blocking a merge.

A withdrawn requirement keeps its row in the register, so every review comment still resolves against it.

| Withdrawn | Last text | Basis | Reviewers | Content now carried by |
|---|---|---|---|---|
| EX-09 | The simulation shall be easy to configure. | Not verifiable as written; the underlying need is covered by the configuration-error requirement | Task lead, simulation lead | EX-01 |

Each consistency check on the workbook earned its place the same way before its clean result counted.

{% include figure image_path="/assets/images/sim-ci-proving-a-check.png" alt="Five-step loop for an invented check: plant a defect, the check must fail, remove the defect, the check must pass, then the check is trusted" caption="Proving an invented check before trusting it. A check that passes with the defect in place gets fixed and planted again." %}

## Artifacts

I can't share the documents, and any diagrams here are illustrations with no program data.

- A draft requirements workbook with its registers and pipeline mapping
- A review delta of old and new text
- AI-assisted consistency checks, each tested against a planted defect
- A draft V&V plan
