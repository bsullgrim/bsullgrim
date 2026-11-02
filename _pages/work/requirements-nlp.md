---
layout: single
title: "Tracing requirements with NLP"
excerpt: "How I built an explainable NLP pipeline that suggests requirement traces for SysML model activities on Blue Origin's Sustaining Lunar Development program, grades the requirements it reads against INCOSE writing rules, and measured it against our engineers' manual traces."
permalink: /work/requirements-nlp/
header:
  teaser: /assets/images/card-nlp.png
toc: true
toc_sticky: true
---

## The problem

On Blue Origin's Sustaining Lunar Development program, our team traced activities in the SysML mission model to the JAMA requirements they satisfy, which for one mission phase meant 395 activities across two vehicles against 758 requirements in seven JAMA documents. We traced by hand in an Excel workbook at about twelve hours per hundred activities, and the result was inconsistent for activities that appeared more than once, left many activities with no clear trace, and went stale whenever the requirements changed. I wanted a tool that could propose traces quickly enough to rerun after each change, explain each proposal well enough that an engineer could judge it without repeating the search, and surface the recurring gaps nobody had time to hunt for.

## Constraints

The program's data could not leave the program, so the public repository and every example on this page use demo data from my AOMS capstone. On the program the tool had to read CSV exports from JAMA and the model, write an Excel workbook, and run on our workstations without downloading models from the internet, and its only labeled data was our team's manual traces, which had to serve as both the source of domain knowledge and the answer key. The inputs were lopsided as well, since a requirement is a full sentence with conditions and numbers while an activity is a short verb-noun phrase like "Monitor Thermal Environment."

## What I did

The first of the two Python tools I built was a matcher that scored every requirement-activity pair four ways and combined the normalized scores with weights, because each measure alone failed on different pairs. BM25 keyword scoring rewards rare technical terms and acronyms on both sides, and I weighted it most heavily because when one side is three words long an exact shared term is the strongest evidence available; spaCy or sentence-transformer similarity catches pairs that say the same thing in different words; and a domain score draws on an aerospace vocabulary and on term relationships learned from our manual traces, so the team's tracing by hand became the tool's domain knowledge. Query expansion mattered most on real data, widening each terse activity with domain synonyms before comparison so that "monitor" also carried "track," "observe," "watch," and "check."

{% include figure image_path="/assets/images/nlp-pipeline.png" alt="Requirement and activity exports flowing through four scorers into a ranked, explained review workbook, with a parallel requirements quality grader" caption="The matching pipeline and quality grader, drawn from the public code." %}

I scoped the tool to rank candidates and leave each decision to an engineer, and since engineers needed to see why a candidate was suggested before they would act on it, every score carried its reasons into a review workbook with high, medium, and low confidence tabs. For demo requirement F.19 and demo activity "1.2.5 Transmit Data to Ground Control," the explanation lists the shared terms and learned relationships and shows the expanded activity covering seven of the requirement's nine key terms, missing only latency and quality.

{% include figure image_path="/assets/images/nlp-f19-explanation.png" alt="Match explanation for demo requirement F.19 and activity 1.2.5, showing each scorer's evidence and the combined score" caption="One match explanation, rendered from the AOMS demo data in the public repository." %}

The second tool graded the requirements themselves, since many weak matches traced back to weakly written requirements, by scoring five quality dimensions and checking each requirement against the patterns in the INCOSE Guide to Writing Requirements for missing required parts. Averaging the dimensions proved too forgiving, so I capped any requirement lacking a subject or a verifiable criterion at a poor grade, which is why demo requirement I.4, "The system shall accommodate resupply of raw materials and retrieval of finished products via standard cargo spacecraft," grades poor despite reading clearly.

My manager asked whether the tools could also find activities with no requirement behind them, and across the full phase they surfaced 166 orphans and 1,482 quality issues in the 758 requirements. I presented that gap analysis at Blue Origin's company-wide Requirements Summit, where it prompted adoption of JAMA-based traceability from system functions to requirements, so that requirement quality gaps surface earlier.

## How I knew it worked

I evaluated the matcher against our manual traces on 120 program requirements, and its top suggestion matched a manual trace for 31.7% of them, its top three held a match for 50.8%, and its top five for 63.3%, the figure that says whether the shortlist is worth opening. Mean reciprocal rank was 0.423, which rewards a correct answer near the top but counts zero when all five miss, so it partly repeats what Hit@5 reports. Precision at five was 0.173, recall at five 0.494, and F1 at five 0.232, and the gap between that F1 and the hit rate suggests many requirements have several valid activities and the tool usually found one of them, while precision was capped by requirements with only one or two traced activities and lowered further by a similarity threshold I had set too low. All of these numbers measure agreement with traces I have already called inconsistent and incomplete, so some suggestions scored as wrong may be traces we missed.

I report this run instead of the July 2025 runs on the 73-requirement demo set, which reached 78% at Hit@5 and an MRR of 0.59, because the program data is the real test and the demo run's domain knowledge had been learned from the same traces it was scored against. The 30% reduction in tracing effort on my resume is an estimate from Hit@1, reasoning that engineers can confirm the third of requirements whose top suggestion is right instead of searching for them, and since I never measured time saved and the hit rate is per requirement while the baseline is per hundred activities, I treat it as rough.

## What went wrong and what I learned

Calibration gave me the most trouble, since early versions summed raw scores that ran from zero to four and other versions bunched around 0.5 without separating good candidates from bad, which taught me to calibrate each measure on its own before trusting the ensemble. The JAMA exports needed more cleaning than I expected, down to ± and ° mangled by encoding, and the grader's attempts to rewrite requirements into INCOSE templates never worked well enough to use. The low scores also said something about the program, because requirements and activities had been developed by groups not working from each other's material, so some of the misses were the very gaps the tool was meant to find. Next time I would get the manual traces first, start on a smaller slice, build gap detection in from the beginning because phase leads wanted their phase's coverage against their own requirements, and tune the weights with engineers in the room.

At closeout I proposed precision tuning through a higher threshold and per-component testing, LLM drafting of bridge requirements for groups of orphan activities with retrieval limited to the program's own requirements, which was my team's idea, and conversion of requirements to SysML v2 textual notation from the components the grader already extracts.

## Artifacts

- [github.com/bsullgrim/Req-Act-NLP](https://github.com/bsullgrim/Req-Act-NLP) holds the matcher, quality grader, evaluation harness, workbook generator, and the AOMS demo data behind every example and figure on this page.
