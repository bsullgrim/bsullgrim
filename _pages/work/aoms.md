---
layout: single
title: "An orbital factory, modeled"
excerpt: "My Johns Hopkins capstone, an MBSE-driven concept for an automated platform that manufactures ZBLAN optical fiber in orbit, carried from stakeholder needs through functional analysis, a thermal trade study, and an A-level specification, with the full SysML model published to click through."
permalink: /work/aoms/
header:
  teaser: /assets/images/card-aoms.png
toc: true
toc_sticky: true
---

## The problem

ZBLAN is a fluoride glass whose optical fiber could carry a signal thousands of kilometers between laser repeaters where today's silica fiber needs one every few hundred, but drawn on the ground it forms crystal defects that limit its performance, and experiments on the International Space Station have shown that drawing it in microgravity works, producing more than seven miles of fiber in a single month with individual draws over 700 meters. With ZBLAN fiber selling for $175 to $1,000 a meter and a kilogram of glass yielding about 2.2 kilometers of it, the value of each kilogram returned from orbit can run well past the cost of launching it, which made it a good first product for asking what a dedicated, automated orbital factory would need to be.

The Advanced Orbital Manufacturing System (AOMS) was my answer to that question for the capstone of the Master of Science in Systems Engineering at Johns Hopkins, completed in November 2024. I took the concept through the whole Concept Definition phase, from needs analysis through concept exploration to a defined concept, building the work in a SysML model so that each design decision traces back through it to the stakeholder need it serves.

{% include figure image_path="/assets/images/aoms-ov1.jpg" alt="AOMS operational view showing the platform's lifecycle from design and launch through on-orbit assembly, manufacturing, resupply, product return, recovery, and decommissioning" caption="The AOMS OV-1, following the platform through ten lifecycle phases, from Earth-based design and launch to on-orbit assembly, manufacturing, resupply, product return, and decommissioning." %}

## Constraints

The platform had to run in low Earth orbit with as little human intervention as possible, which put autonomy, fault recovery, and remote quality control at the center of the concept, and it had to close a business case for investors as well as satisfy regulators and the customers who would buy the fiber, so stakeholder needs pulled in different directions from the start. The project ran on a fixed academic schedule that I tracked with earned value management alongside a full-time job, so the method had to keep the model organized enough that each later report could be built from it rather than written from scratch.

## What I did

### Needs, stakeholders, and a concept of operations

I started with a stakeholder analysis covering the fiber's end users, investors focused on economic viability, and regulatory bodies, and traced their needs into a single mission need and a set of program objectives. Lynn Harper, a strategic integration advisor at NASA, helped me refine those needs against what NASA and the in-space manufacturing market were actually looking for, which kept the concept honest about what would close the business case. I organized the model around a requirements meta model that links stakeholder needs, system functions, architecture elements, and verification methods, so a trace can be followed in any direction and the impact of a change can be found by walking the model.

The concept of operations describes a platform that is initialized in orbit, monitors its own production, performs routine maintenance, takes on raw material from resupply vehicles, and sends finished fiber home in return capsules, with operators on the ground working through telemetry, cameras, and diagnostics while the system detects and corrects its own faults.

### Functional analysis

I decomposed the system into eight top-level functions, each written in verb-object form: conduct autonomous orbital manufacturing operations, maintain operational availability of the platform, ensure compliance with regulatory and safety standards, manage resources and logistics, recover from faults and accept remote override, monitor and analyze system performance, assemble, activate, and upgrade on orbit, and manage orbital position and attitude. Functional flow block diagrams and activity diagrams carry the sequences and decision points, N² diagrams capture the interfaces between functions, and a traceability matrix ties every function to the requirements it supports.

### A thermal trade study

Thermal stability is critical while fiber is being drawn, so the trade study I gave the most attention to was the platform's heat rejection. I compared three radiators, the ISS Heat Rejection System Radiator, the Alpha Radiator, and a Deployable Panel Radiator, weighting four criteria through pairwise comparison and scoring each alternative on utility curves.

| Criterion | Weight | ISS HRSR | Alpha Radiator | Deployable Panel Radiator |
|---|---|---|---|---|
| Heat rejection (W/kg) | 0.58 | 10.78 | 54.82 | 55.97 |
| Mass (kg) | 0.17 | 1,487.75 | 273.60 | 288.00 |
| Deployed area (m²) | 0.15 | 106.70 | 48.48 | 36.96 |
| N+2 redundancy penalty (kg) | 0.10 | 270.50 | 45.60 | 72.00 |
| **Weighted utility** | | **0.103** | **0.884** | **0.891** |

The Deployable Panel Radiator came out ahead, but only just ahead of the Alpha Radiator, and a margin that thin is why I ran a sensitivity analysis before carrying the result into the design, and why the choice is worth revisiting as better data arrives.

### Architecture, risk, verification, and the specification

The conceptual design allocates the functions to twelve major subsystems, including power, thermal, communications, software, propulsion, and the manufacturing elements, and describes each internal and external interface by the data, energy, and material that cross it, with matrices tracing functions to physical elements and interfaces so that no function is left without something to perform it. The risk assessment followed five risks from initial to final likelihood and consequence once mitigations were in place, bringing the highest, instability in the microgravity manufacturing process, from 4×4 down to 2×2.

The test plan integrates the subsystems through a series of builds and finishes with qualification in thermal vacuum, vibration, and electromagnetic interference testing. The A-level specification turns the analysis into measurable requirements, 70 percent of them quantitative, written to state performance without prescribing solutions, and it sets key performance parameters such as fewer than one crystallization defect per kilometer of fiber, five years of operation without physical human intervention, 95 percent operational availability, at least 500 meters of fiber a day at 95 percent usable yield, and an automatic restart within ten minutes of a broken draw.

## What I learned

Starting from a reference architecture saved me more time than anything else, and Sanford Friedenthal's *Architecting Spacecraft with SysML*, which works the FireSat example from *Space Mission Analysis and Design*, gave me a model structure that mirrors how real spacecraft programs organize their work. Defining a meta model before building the model kept it consistent as it grew and gave stakeholders who don't read SysML a simpler way to see how the pieces relate, and organizing the content into viewpoints mapped to stakeholder concerns under ISO/IEC/IEEE 42010 made the reports far easier to build, which became the first step toward generating them automatically with the Velocity Template Language.

The lesson I carried furthest is that tracing requirements to functions is where the real work begins, because the first pass always leaves functions and requirements without clear relationships, and the temptation to force a "good enough" link hides exactly the gaps the trace exists to find. The earned value tracking told a related story, since the schedule fell behind during the heavy setup and research at the start and recovered by late October, once the model was mature enough that later reports could be drawn from it.

After finishing the degree I briefed the results to Draper's in-space servicing, assembly, and manufacturing leads, and the requirements and activities from this model now serve as the public demo data for my [requirements traceability pipeline](/work/requirements-nlp/).

## Artifacts

- [The final report](/docs/AOMS_Final_Report.pdf)
- [The presentation](/docs/AOMS_Presentation.pdf)
- [The SysML model](https://bsullgrim.github.io/AOMS/AOMS.html), which you can click through in a browser
