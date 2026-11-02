---
layout: single
title: "ShipWall: a system that fails by silence"
excerpt: "A live ship-traffic display I built and run by myself at my family's cottage on the St. Lawrence Seaway, and what twenty logged failures taught me about systems whose worst failures make no noise."
permalink: /work/shipwall/
header:
  teaser: /assets/images/card-shipwall.jpg
toc: true
toc_sticky: true
---

## What it does

ShipWall is a 128×64 LED panel at my family's cottage on the St. Lawrence Seaway that shows the commercial traffic on the river as a departure-board register of the last 18 hours, with detail cards carrying each ship's funnel markings, and logs the large ships that cross in front of the cottage to leaderboards on a small public web page. The page's Hall of Fame tab adds a dataset I merged from my own decade of hand-logged sightings and a second observer's log from along the Great Lakes, 4,323 sightings of 806 ships from 290 fleets between 2016 and 2026, which the page labels as the historical spotting log, apart from ShipWall's own detections.

I wrote the first code in early June 2026 and left the system running unattended in early July, and since I am its only developer and run it from home in Massachusetts, the failures that cost me most were the quiet ones, where the panel kept showing an old frame, the feed went silent without closing the connection, or a service reported healthy while the part doing the work had stopped.

## How it's built

{% include figure image_path="/assets/images/shipwall-architecture.png" alt="Block diagram of ShipWall: the AISStream feed into async Python services on a Raspberry Pi, JSON frames over USB serial to an ESP32-S3 driving the LED panel, with the browser mock, web page, backups and watchdogs alongside" caption="The Pi makes every decision; the ESP32-S3 only renders." %}

A Raspberry Pi 3B runs asyncio Python services that subscribe to the AISStream WebSocket feed, keep a register of ships, and every ten seconds send a compact JSON frame as one line over USB serial to an Adafruit MatrixPortal ESP32-S3, which drives the HUB75 panel and does nothing else; its parser ignores input until it sees an opening brace, a rule I added after a board reset mid-frame left every later frame misaligned. AIS coverage has a hole right at the cottage, so crossings are inferred by projecting each position fix onto an axis along the river and watching for a ship's progress to pass the home value, in `crossing.py`, a shared state machine that every detection path imports.

I designed the interface between the Pi and the firmware before the panel arrived: `register_panel.py` renders frames in a browser the way the panel should, I ported the firmware to match it pixel for pixel, and `FRAME_SCHEMA.md` records the wire format as a contract that the frame builder, the schema and the firmware change together. Treating the mock as an executable interface spec meant a Great Lakes map screen I added in late June was checked against a PNG from a mock harness of the firmware before it went near the board.

## Running it from far away

Tailscale carries my SSH from home and serves the public page through Funnel. Three layers watch liveness: the firmware prints a heartbeat once a second, the service reboots the board through the serial port if its pushes succeed but no heartbeat has come for 90 seconds, and a systemd timer runs `panel-watchdog.sh` every minute as the backstop, restarting the service once the heartbeat has been stale for 180 seconds. `deploy.sh` stashes local edits, pulls fast-forward-only so that divergence stops it, compiles every tracked Python file before touching the running service, and polls until each service reports active. An hourly timer runs `backup.sh`, which pushes the data files to a separate private repository and refuses any file containing null bytes, and `restore.sh` puts checked copies onto a fresh card; the backups came out of a June SD card that cracked and a July power cut I recovered from over SSH.

## What went wrong

My numbered incident log has 20 entries, each with the symptom, the wrong hypotheses, the root cause, the fix and the lesson, and these three carry most of what I learned.

### The feed that went quiet (Incident 13)

One June morning the panel showed ships twelve hours stale while every watchdog reported healthy. I saved the logs before restarting anything and ran three probe subscriptions, one of them for the English Channel, which received nothing in 40 seconds even on a fresh key, while an independent monitor confirmed a provider-wide outage, so what I had to own was that nothing in my system had noticed: the ingest loop used `async for raw in ws`, which waits indefinitely when a server stops sending without closing the socket, and all three watchdog layers were watching mechanisms while none watched the data. I added `asyncio.wait_for` on every receive with a 600-second limit that raises into the reconnect handler, and it fired against that same outage at 601 seconds.

### Configured, but never exercised (Incident 18)

On paper, the backups and `restore.sh` let the system lose its card and come back. In late July a routine deploy failed at the compile gate, the first sign of ext4 damage left twelve days earlier by an unclean power-off, and the forced fsck that repaired it also cut loose Tailscale's state and the saved clock, so the Pi booted believing it was April, TLS failed, and recovery took a monitor and keyboard at the cottage. The fresh clone I had used to work around the damage was the first rebuild from the repo since I wrote `restore.sh`, and `backup.sh` came out of it without the executable bit git had never recorded, so systemd failed it with `203/EXEC`, while my manual test the day before had passed only because I ran it as `bash backup.sh`. The live unit files had also drifted from the repo's copies, the backup timer restarted its count at every reboot, and `restore.sh` would have skipped the udev rule, the executable bits and the watchdog timers, all of which now live in the repo or the script.

### The bug that came back three times (Incident 15)

In its first three weeks crossing detection failed four times, and I fixed the first three by adjusting a key or a threshold: a dedup key and margin for a triple-logged transit, a shared helper for duplicates after restarts, and a six-hour window for a transit logged on two days. On July 1 one ship's single transit was logged as five crossings, and that investigation found that the live detector, the in-service backfill and a standalone script had drifted into three copies of the same test, each firing on one pair of fixes straddling the home point, one missing the margin and none limiting the time between fixes. I replaced the copies with `crossing.py`, which needs two consecutive fixes on the new side and rejects gaps over 24 hours, a cap set from data where real crossings topped out near 15.7 hours, and no later incident on the log is a crossing failure. My first cleanup made things worse, turning 182 live rows into 5 by regenerating them from a source too sparse for the job and, because I hadn't chained the commands with `&&`, emptying `passages.csv`, which I restored from the `.bak` before scrubbing only the 47 bad rows.

### How the incident rate changed

{% include figure image_path="/assets/images/shipwall-incidents-by-month.png" alt="Bar chart of ShipWall incidents per month, June through September 2026" caption="Incidents per month. June includes bench bring-up; the system ran unattended from early July." %}

The log has 14 incidents in June, 4 in July, 2 in August and 1 in September. June includes bench bring-up, so part of that drop is the move from building the system to running it, and the counts hide that incidents got more expensive as they got rarer, since what was left by late summer was filesystem corruption, a router change and a Pi that stopped answering on every remote path at once, all below the layers my watchdogs could see, and September's one incident was a service outage that lasted about a month.

## What I learned

Most of my lessons come back to treating "configured" and "working" as separate claims, which I first learned from persistent logging I set up in June that had been writing to RAM all along, overridden by a drop-in file Raspberry Pi OS ships, and I now verify by observed behavior, such as a previous boot actually showing up in `journalctl --list-boots`. I layer watchdogs so each covers another's blind spot and at least one watches the output a person sees, and when a bug comes back I look for duplicated logic before I touch a threshold.

The weak point I am working on now is remote access. The late-August incident left SSH, Tailscale and the public page all unreachable while Tailscale's control plane still had a heartbeat from the Pi, and this fall the Pi again shows as connected in Tailscale while SSH times out, so it is coming home in November for a high-endurance SD card and a round of maintenance, and a self-healing watchdog on the remote-access path is the next piece of work before it goes back, since I still plan around physical access at the cottage as a hard requirement for recovery.

## Code and artifacts

The source is at [github.com/bsullgrim/shipwall](https://github.com/bsullgrim/shipwall), with these as the places to start:

- **`register_service.py`**: ingest, the register, the frame builder and the watchdog checks
- **`crossing.py`**: the shared crossing state machine
- **`register_panel.py`**, **`FRAME_SCHEMA.md`**, **`register_esp32/`**: the mock, the wire contract and the firmware
- **`deploy.sh`**, **`backup.sh`**, **`restore.sh`**, **`systemd/`**: deployment and recovery

