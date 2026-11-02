---
layout: single
title: "The Holliston Ledger: a one-person newsroom with checks"
excerpt: "The pipeline behind The Holliston Ledger, the civic news publication I run on my own, which drafts from town feeds and meeting recordings with AI, checks every number, quote, and date against its source, and leaves every publishing decision to me."
permalink: /work/holliston-ledger/
header:
  teaser: /assets/images/card-ledger.png
toc: true
toc_sticky: true
---

## What it is

Holliston, the Massachusetts town where I live, runs its government through a long list of boards and committees, and while most of them post a recording of each meeting within a day or two, approved minutes can take weeks, so for most of that time the recording is the only account of what a board decided. I started [The Holliston Ledger](https://www.hollistonledger.com/) in October 2026 to cover town government from that public record, and in its first two weeks it published a voter guide for the fall Town Meeting, an explainer on the groundwater bylaw article, a recurring briefing and a *This Week at Town Hall* wrap-up, meeting notes from the Planning Board and the Zoning Board of Appeals, results from Town Meeting the morning after, and a hub page that pulls 88 scattered town filings on a Chapter 40B apartment proposal into one readable account.

I run it alone, around a full-time engineering job, which is only possible because a pipeline does the reading and drafting while I do the judging. The pipeline, which I call the Mudville Wire, has two halves, a morning job that turns the town's feeds into a review queue and an overnight job that turns meeting recordings into transcripts I can check, and both end at the same place, with me deciding what is true enough to publish.

{% include figure image_path="/assets/images/ledger-pipeline.png" alt="Diagram of the Ledger pipeline: a morning job turns town feeds into checked drafts on a review sheet, an overnight job turns meeting recordings into transcripts and checklists, and both end with a human check before publishing" caption="Two halves, one gate: everything reaches readers only after I have checked it." %}

## How it's built

The morning job runs on GitHub Actions on Monday, Wednesday, and Friday mornings. It reads the town's RSS feeds for news, alerts, and meeting agendas, along with the local paper's feed and a Google Alert, keeps anything from the last ten days that it hasn't seen before, and asks Claude to sort each item into a section and draft three headline options for it, one straight, one sharp, and one wry, along with a supporting quote from the source, the event date, and a newsworthiness score from one to five. The results land in a Google Sheet, where I choose the headlines and build each post from a menu I wrote in Apps Script, and because the API credit is prepaid with automatic reload turned off, the job can never spend more than I have put in, which in practice has been about half a cent per item.

The same run scans the town's Agenda Center for meetings from the last sixty days that have a recording and no minutes, puts the priority boards first, and adds them to a Meetings tab. Overnight, a script on my own PC downloads those recordings, transcribes them with WhisperX primed with a vocabulary file of local names and terms so that board members and street names come out spelled correctly, labels the speakers with pyannote, and writes two files for each meeting, a transcript and a checklist of every motion, vote, dollar figure, and recusal with its time in the recording. I draft each brief from those two files in a Claude project, and the checklist becomes the list of things I verify before anything goes out.

## Keeping a person between the model and the reader

Every draft goes through checks that don't depend on a model before I see it. The supporting quote has to appear word for word in the source, every number in a headline has to appear in the source text, a vote tally like 5–0 has to appear as that same pair of numbers, any quoted words have to be in the source, and the event date has to be there too. A second, smaller model then reads each headline option looking for overstatement of certainty or size, and the row lands on the sheet marked Use, Hold with a note saying what failed, option by option, or Spike, for items the model judged not worth running, like a statewide press release or an event that has already happened, which stay on the sheet with the reason so I can see what was dropped as well as what was kept.

I made the checks strict on purpose and accept that they flag good items, since "five to nothing" in a source and "5–0" in a headline agree but fail a literal comparison. A row marked Use can still be wrong, because the checks only catch numbers, quotes, and dates that aren't in the source, so I read every one before it goes into a post. Anything written from a meeting without approved minutes says so, with the time in the recording ("From the recording, at 1:12:40. Minutes have not been approved."), every motion and vote in it is checked by listening, because Whisper regularly hears "aye" as "I", and when the minutes are finally posted the morning job fills in their link on the Meetings tab with a note to check the brief against them, and I correct it in place. The tests run on every push, against sample feeds and a stand-in for the model, with no network access and no API key.

## What went wrong and what I learned

The Agenda Center reader was first written from a description of the page rather than its actual HTML, because the town's site couldn't be reached from where it was being written, so the first real dry run was also the first time it saw the page, and I had to compare its output line by line against the Agenda Center and rework it around the real markup, where an amended agenda's date heading reads like a board name and the audio and video links carry the same label. The same meeting can also arrive twice, once from the Agenda Center and once from the town calendar under a different title, and agenda items whose feed text carries no date come in flagged until I fill the date in from the agenda.

The bigger lesson was about where the work actually goes, since drafting turned out to be the cheap part and nearly all of the design effort went into making each claim cheap to check, by carrying its source text, its quote, or its time in the recording along with it, so that verifying a post means confirming a short list of specific things instead of rereading everything the pipeline read.

## How it's going

As of October 20, ten days after the first posts, most posts had drawn between about 100 and 300 views, and the main posts had been opened by 55 to 72 percent of the subscribers they were emailed to.

## Links

- [The Holliston Ledger](https://www.hollistonledger.com/)
- The pipeline's code is private.
