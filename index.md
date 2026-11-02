---
layout: splash
permalink: /
title: "Ben Grimsley"
header:
  overlay_color: "#1f3864"
  actions:
    - label: "Resume (PDF)"
      url: "/docs/B.Grimsley_resume.pdf"
    - label: "Email me"
      url: "mailto:grimsley.ben@gmail.com"
excerpt: "Systems engineer working on MBSE, interface control, and the tooling that checks engineering work automatically."

# --- Selected work: one full-width row per case study, alternating image side ---
feature_row_gd:
  - image_path: /assets/images/card-interface-control.png   # generic diagram of the ICD lifecycle, no program content
    alt: "Diagram of an interface moving from working draft to released ICD"
    title: "Interface control on a defense space program"
    excerpt: "How I structure and run interface control for Draper's part of a defense space program, keeping what an interface is separate from why it is that way, so a working draft can be walked to a baseline one value at a time."
    url: "/work/interface-control/"
    btn_label: "Read the case study"
    btn_class: "btn--primary"
feature_row_tc:
  - image_path: /assets/images/card-test-cells.png          # the four-view method as a diagram
    alt: "Diagram of the four-view architecture method"
    title: "An architecture description for guidance system test cells"
    excerpt: "A four-view ISO/IEC/IEEE 42010 architecture description in SysML for the Trident II D5LE2 MK 8 guidance system's integration and test cells, proved on one cell with a walkthrough reviewers could follow, then applied across the priority cells and carried into System Functional Review."
    url: "/work/test-cell-architecture/"
    btn_label: "Read the case study"
    btn_class: "btn--primary"
feature_row_nlp:
  - image_path: /assets/images/card-nlp.png                 # pipeline diagram, or a match explanation from the public demo data
    alt: "Diagram of the NLP requirements traceability pipeline"
    title: "Tracing requirements with NLP"
    excerpt: "On Blue Origin's Sustaining Lunar Development program, I built an explainable NLP pipeline that ranks likely JAMA requirement traces for SysML model activities and grades requirements against INCOSE writing rules, then measured it against our team's manual traces and reported where it fell short."
    url: "/work/requirements-nlp/"
    btn_label: "Read the case study"
    btn_class: "btn--primary"
feature_row_sim:
  - image_path: /assets/images/card-sim-ci.png              # the per-merge / nightly / release / milestone gate ladder
    alt: "Diagram of verification gates from per-merge to milestone"
    title: "Requirements a pipeline can verify"
    excerpt: "I turned a 32-line informal requirements list for a guidance-system simulation into a traced, reviewed draft specification that separates how each requirement is verified from when a CI pipeline could check it, and that judges fidelity before real-system data exists."
    url: "/work/sim-requirements-ci/"
    btn_label: "Read the case study"
    btn_class: "btn--primary"

# --- Side projects: three smaller cards ---
feature_row_side:
  - image_path: /assets/images/card-shipwall.jpg
    alt: "ShipWall LED display showing the freighter CSL Niagara underway"
    title: "ShipWall"
    excerpt: "A live AIS ship-traffic display I built and run alone at my family's cottage on the St. Lawrence Seaway, with three layers of watchdogs, gated deploys, and a 20-entry incident log."
    url: "/work/shipwall/"
    btn_label: "Read more"
  - image_path: /assets/images/card-aoms.png                # screenshot of the published SysML model
    alt: "Screenshot of the AOMS SysML model"
    title: "An orbital factory, modeled"
    excerpt: "My Johns Hopkins capstone, an MBSE-driven concept for automated ZBLAN fiber production in orbit, with the full SysML model published to click through."
    url: "/work/aoms/"
    btn_label: "Explore the model"
  - image_path: /assets/images/card-ledger.png              # the Ledger masthead
    alt: "The Holliston Ledger masthead"
    title: "The Holliston Ledger"
    excerpt: "An independent civic news publication on my town's government, backed by a pipeline that transcribes unminuted board meetings for human fact-checking."
    url: "https://www.hollistonledger.com/"
    btn_label: "Read the Ledger"
---

I'm a systems engineer at Draper, working from Holliston, Massachusetts, on the models, requirements, and interface definitions that missile defense, guidance, and space programs are built and tested against, and increasingly on the Python tooling that checks that work automatically so the people reviewing it can spend their attention on the judgment calls.

## Selected work

{% include feature_row id="feature_row_gd" type="left" %}

{% include feature_row id="feature_row_tc" type="right" %}

{% include feature_row id="feature_row_nlp" type="left" %}

{% include feature_row id="feature_row_sim" type="right" %}

## How I work

These are the principles I keep coming back to, each learned on something I built, ran, or had to defend in a review.

**Show reviewers one scenario they can follow end to end.** When I briefed the four-view method for the MK 8 test cells, I walked a single scenario from use case through behavior and interfaces to the requirements matrix, with the draft items named up front, because reviewers are persuaded more by one path they can follow than by coverage they have to take on trust, and the method was endorsed and carried across the priority cells into System Functional Review.

**Keep what an interface is apart from why it is that way.** Every value in the interface control document I own on a defense space program is a contract statement with a closed status of Committed, TBR, or TBD, while its reasoning, open questions, and history each live in exactly one other place, so the document can be walked to a baseline one value at a time.

<!-- Keep this one only once question 5 in the NLP notes is confirmed. -->
**Score a tool against the hardest honest test available, and say what that test cannot see.** I reported the NLP pipeline's run on program data over earlier demo runs that scored higher, because the demo run's domain knowledge had been learned from the same traces it was graded against, and I said on the record that the answer key was the same inconsistent manual tracing the tool was built to improve.

**A check earns trust only once something can fail it.** Every consistency check on the simulation requirements workbook had to fail on a planted defect before its clean result counted, and the one rule with no check behind it, keeping the verification method separate from automation, was broken in fourteen requirements by the same revision that stated it.

**A recovery path is untested until it has rebuilt something real.** On ShipWall, the first rebuild from the repository after I wrote the restore script showed that the backup script had lost its executable bit, the backup timer reset on every reboot, and the restore skipped three install steps, none of which reading the configuration files had shown.

## Side projects

{% include feature_row id="feature_row_side" %}

## Writing

{% if site.posts.size > 0 %}
{% for post in site.posts limit: 3 %}
  {% include archive-single.html %}
{% endfor %}
{% else %}
Write-ups on NLP for requirements traceability, Python for systems engineers, and lessons from putting MBSE on real programs are on the way.
{% endif %}

## Programs

The short version of where I've worked, with the full detail in my [resume](/docs/B.Grimsley_resume.pdf).

- **Defense space program** – Interface Control Manager, owning the avionics specification and ICDs, modeling the system against the government reference architecture, and decomposing functions from L3 to L4
- **Trident II D5LE2 MK 8 Guidance System** – MBSE lead for the integration and test cells, and author of the guidance system CONOPS, which I took through 26 reviewers and 144 comments
- **Blue Origin lunar lander** – MBSE for human and cargo landing CONOPS, modeling liaison for on-orbit refueling, and the NLP traceability pipeline
- **DARPA Otter VLEO satellite** – 200+ system and subsystem requirements and the ICDs behind them for the System Requirements Review
- **Conventional Prompt Strike** – Trade studies for M-Code GPS receiver integration ahead of successful flight tests in 2024 and 2025
- **U.S. Navy robotics at Boston Engineering** – Automated coating QA for flight decks, hull inspection, USV anchoring, and an EOD tether-management ROV
- **U.S. Air Force, 2016–2021** – Launch facility engineering and vehicle integration at Vandenberg, then base-defense acquisition at Hanscom, leaving as a Captain

## Get in touch

Email is the fastest way to reach me at [grimsley.ben@gmail.com](mailto:grimsley.ben@gmail.com), and I'm also on [LinkedIn](https://linkedin.com/in/bengrimsley) and [GitHub](https://github.com/bsullgrim).
