---
layout: single
title: "Interface control on a defense space program"
excerpt: "How I structure and run interface control for Draper's part of a defense space program, keeping what an interface is separate from why it is that way, so a working draft can be walked to a baseline one value at a time."
permalink: /work/interface-control/
header:
  teaser: /assets/images/card-interface-control.png
toc: true
toc_sticky: true
---

## The problem

When I joined a Draper team on a defense space program as its Interface Control Manager, I took on the avionics specification and the interface control documents for Draper's part of the program, which meant defining how a central unit and a long list of peripherals connect electrically, mechanically, and in data and timing, across several build configurations and with vendors, subsystem leads, a prime contractor, and the customer's reference architecture all holding a piece of the answer. On a program moving this quickly, the risk I'm there to manage is the one every interface manager will recognize, which is that the working drafts, the agreements reached in interface working group meetings, the system model, and the eventual baseline gradually stop describing the same system, and nobody notices until two teams build to two different versions of the same interface.

## Constraints

- I joined a program already in motion, with a customer-defined reference architecture above Draper's work and a prime contractor's schedule around it, so the interfaces had to stay consistent with commitments made before I arrived.
- Most values had to be written down before anyone with the authority to confirm them was available, because vendors, subsystem leads, and interface working groups come online at different times.
- The team is distributed, with my task lead in a different Draper office and an explicit expectation that I would run the interface work with a good deal of autonomy.
- I work remotely and in short, focused blocks, so the document has to let me, or anyone else, pick up any interface cold and see where it stands without rereading its history.

## What I did

### Built a pattern before building the document

Before writing anything for the program, I built myself an onboarding kit of cross-linked reference notes: a job aid covering what an interface control manager is responsible for across the lifecycle, a primer on the kinds of interfaces I would be managing, and a fully worked starter document that carries one example interface through all four interface artifacts in the NASA Systems Engineering Handbook (the interface requirements document, interface control document, interface definition document, and interface control plan) along with their management annexes. With that pattern in hand I wrote the first full draft of the ICD within weeks of joining the program.

### Separated what an interface is from why it is that way

The decision that shaped everything else was treating every value in the ICD as a contract statement, so a clause carries only what the interface is (a number, a range, a protocol, a named standard, or an explicit TBD) and none of the reasoning that produced it. The reasoning still exists, but each kind lives in exactly one place: derivations and trade reasoning go in a companion rationale document, open questions and their closure criteria go in a ledger keyed to the clause they affect, change history goes in the revision table, and superseded draft content goes into dated archive files so it can be recovered without cluttering the baseline. Anyone reading a clause sees the commitment, and anyone who needs the because knows exactly where to find it.

### Made the status of every value honest

I gave the document a closed status vocabulary of three words. A value is Committed only when it comes from an external standard or is physically forced by the hardware or environment, it is TBR when it is my working position awaiting confirmation by a vendor, a subsystem lead, or a working group, and it is TBD when its structure or applicability hasn't been decided. Qualifiers like "proposed" or "under review" belong in the ledger, never in the status column, which means a reader can trust the status of any value at a glance and the open work is always countable.

### Defined shared infrastructure once

The ICD defines the electrical, data, timing, mechanical, and failure-handling infrastructure that the peripherals share in one common section, and each peripheral's clauses reference it, so a change to shared infrastructure is made once and reviewed against every interface that depends on it. An applicability matrix records which interfaces apply to which build configuration, and a running set of cross-clause consistency notes tracks where one part of the document depends on another.

### Planned the path from draft to baseline

Because almost everything starts as a working position, I planned for a catch-up baselining event in which I walk every open value with whoever holds the authority for it and leave each one confirmed as written, renegotiated to a new committed value, or still open with an updated closure driver, with individual working groups baselining their own interfaces as they convene. Decisions from the first interface working group were recorded in a decision register inside the ICD itself, where the next reader will find them. Alongside the document I model and simulate Draper's system against the government reference architecture and decompose functions from L3 to L4, so each interface traces back to a function the customer defined.

## How I knew it was working

Over its first three months the draft went through more than thirty logged working revisions, each recorded in the revision table with what changed, and because the reasoning, open questions, and history each had a fixed home, none of those revisions required untangling a clause before it could be changed. The status vocabulary meant I could say at any point exactly how many values were committed, how many were awaiting confirmation, and what each open item needed to close, which is the question a task lead asks most often and the one a loosely written ICD can't answer.

## What went wrong and what I learned

The steepest part of the learning curve was avionics itself, since most of my earlier interface work, on DARPA's Otter satellite and the Trident MK 8 guidance system, sat at the system level, and owning an avionics specification asks for more depth on the electrical and data side of an interface than I had needed before. The broader lesson is one I keep relearning on every program, which is that the time spent building a worked pattern before the first real document pays for itself many times over, because it turns each new interface area from a blank page into a comparison against something already thought through.

## An example you can look at

The program's documents aren't public, so here is the same structure applied to an interface I invented for this page, between a payload camera and the flight computer on a small satellite, with every value made up and none of it taken from a real program.

{% include figure image_path="/assets/images/card-interface-control.png" alt="Diagram of a clause value with its status, surrounded by the rationale document, open-items ledger, revision history, and archives that hold everything else" caption="Each clause carries only its value and status, and everything else about it has exactly one home." %}

The clauses say what the interface is and nothing more, each with one of the three statuses.

| Clause | Parameter | Value | Status |
|---|---|---|---|
| 3.1.1 | Command link signaling | RS-422, per TIA-422-B | Committed |
| 3.1.2 | Command link data rate | 115.2 kbit/s | TBR |
| 3.1.3 | Housekeeping telemetry rate | 1 Hz | TBR |
| 3.2.1 | Image data link | TBD | TBD |
| 3.3.1 | Camera input voltage | 28 V ± 4 V, from the spacecraft bus | TBR |
| 3.5.1 | Connector | TBD | TBD |

Clause 3.1.1 is Committed because its value comes from a published standard and no program decision can change it, while 3.1.2 is a working position that a vendor or the working group still has to confirm. The open-items ledger holds the questions, keyed to the clause they affect, with the evidence that would close each one.

| Item | Clause | Open question | Closes when |
|---|---|---|---|
| OI-04 | 3.1.2 | Can the camera's controller sustain 115.2 kbit/s with command acknowledgment? | The vendor confirms in writing, or a bench test at that rate drops no frames |
| OI-07 | 3.2.1 | SpaceWire or LVDS for image data? | The working group chooses after the flight computer team sizes its input card |

The reasoning lives in the rationale document, where a reviewer who wants the because can find it without it cluttering the contract.

> **R-3.1.2.** 115.2 kbit/s is the highest standard rate the flight computer's serial ports support without a dedicated controller. 57.6 kbit/s was considered and set aside because uploading a full command table would overrun the two-second command window.

The revision history records what changed and what it replaced.

| Rev | Change | Replaces |
|---|---|---|
| —.4 | 3.1.2 raised from 57.6 to 115.2 kbit/s; derivation moved to R-3.1.2 | the —.3 value |

At baselining, OI-04 closes one of three ways: the vendor confirms 115.2 kbit/s and the clause becomes Committed as written, the parties settle on a different rate and it becomes Committed at that value, or more information is needed and it stays TBR with its closure driver updated.

## Artifacts

The framework behind the document set is described in the NASA Systems Engineering Handbook (NASA/SP-2016-6105 Rev 2), section 6.3, Interface Management.
