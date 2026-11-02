import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from lib import *

OUT = os.path.join(os.path.dirname(__file__), "src")
os.makedirs(OUT, exist_ok=True)


def save(name, s):
    with open(os.path.join(OUT, name), "w", encoding="utf8") as f:
        f.write(s.svg())


# ---------------------------------------------------------------- card: interface control
def card_interface_control():
    s = SVG(1600, 900)
    cx, cw, ch = 800, 620, 330
    x0, y0 = cx - cw / 2, 450 - ch / 2
    # satellites
    sw_, sh_ = 470, 190
    sats = [
        (50, 70, "Rationale", "why the value is what it is"),
        (1080, 70, "Open-items ledger", "questions and closure criteria, keyed to the clause"),
        (50, 640, "Revision history", "what changed, and when"),
        (1080, 640, "Archives", "superseded draft content, dated"),
    ]
    # connectors first so boxes sit on top
    s.line([(50 + sw_, 70 + sh_ / 2), (x0 + 60, y0)], color=LINE, sw=3)
    s.line([(1080, 70 + sh_ / 2), (x0 + cw - 60, y0)], color=LINE, sw=3)
    s.line([(50 + sw_, 640 + sh_ / 2), (x0 + 60, y0 + ch)], color=LINE, sw=3)
    s.line([(1080, 640 + sh_ / 2), (x0 + cw - 60, y0 + ch)], color=LINE, sw=3)
    for x, y, t, sub in sats:
        s.block(x, y, sw_, sh_, t, sub, tsize=40, ssize=27)
    # centre clause
    s.rect(x0, y0, cw, ch, fill=EMPH, stroke=EMPH, rx=20)
    s.text(cx, y0 + 92, "Clause value", 50, fill=WHITE, weight="bold", anchor="middle")
    s.text(cx, y0 + 145, "what the interface is, and nothing else", 27, fill=ON_EMPH, anchor="middle")
    chips = ["Committed", "TBR", "TBD"]
    cwid = [width(c, 28, "bold") + 44 for c in chips]
    total = sum(cwid) + 24 * 2
    x = cx - total / 2
    for c, w in zip(chips, cwid):
        s.rect(x, y0 + 200, w, 64, fill=WHITE, stroke=WHITE, rx=32)
        s.text(x + w / 2, y0 + 242, c, 28, fill=EMPH, weight="bold", anchor="middle")
        x += w + 24
    save("card-interface-control.svg", s)


# ---------------------------------------------------------------- card: test cells (also a page figure)
def card_test_cells():
    s = SVG(1600, 900)
    s.text(800, 100, "Four views from one viewpoint, applied to every test cell", 32, fill=MUTED, anchor="middle")
    bw, bh, gap, y = 330, 230, 50, 170
    xs = [65 + i * (bw + gap) for i in range(4)]
    labels = [
        ("Stakeholder concerns", "what each reviewer needs answered"),
        ("Operational", "the cell as the boundary, with use cases for each scenario"),
        ("Behavioral", "activities with swimlanes for stimulus, response, and recording"),
        ("Structural / interface", "equipment, and its proxy-port interfaces to the unit under test"),
    ]
    for i, (x, (t, sub)) in enumerate(zip(xs, labels)):
        if i == 0:
            s.block(x, y, bw, bh, t, sub, tsize=34, ssize=24, fill=PAPER, stroke=LINE, dash="10 8")
        else:
            s.block(x, y, bw, bh, t, sub, tsize=34, ssize=24, fill=NAVY_T1, stroke=NAVY_T3)
        if i < 3:
            s.line([(x + bw + 4, y + bh / 2), (x + bw + gap - 6, y + bh / 2)], color=NAVY, sw=4, marker="arrN")
    # traceability band
    ty = 590
    for x in xs[1:]:
        s.line([(x + bw / 2, y + bh), (x + bw / 2, ty)], color=NAVY_T3, sw=3, dash="8 7")
        s.add(f'<circle cx="{x + bw / 2}" cy="{ty}" r="7" fill="{NAVY}"/>')
    s.rect(65, ty, 1470, 200, fill=EMPH, stroke=EMPH, rx=18)
    s.text(800, ty + 82, "Requirements traceability", 40, fill=WHITE, weight="bold", anchor="middle")
    s.text(800, ty + 135, "each requirement traced through use cases and activities to the structure, with gaps marked",
           26, fill=ON_EMPH, anchor="middle")
    save("card-test-cells.svg", s)


# ---------------------------------------------------------------- figure: traceability pattern
def traceability_pattern():
    s = SVG(1600, 900)
    # requirement
    rx_, ry_, rw, rh = 590, 70, 420, 190
    s.rect(rx_, ry_, rw, rh, fill=NAVY_T1, stroke=NAVY, sw=3, rx=6)
    s.text(800, ry_ + 50, "«requirement»", 24, fill=MUTED, anchor="middle")
    s.text(800, ry_ + 98, "Test cell requirement", 32, weight="bold", anchor="middle")
    s.line([(rx_, ry_ + 125), (rx_ + rw, ry_ + 125)], color=NAVY_T3, sw=2)
    s.text(800, ry_ + 165, "id, text", 24, fill=MUTED, anchor="middle")
    # use case
    ucx, ucy = 330, 560
    s.ellipse(ucx, ucy, 250, 105, fill=FILL, stroke=INK, sw=2.5)
    s.text(ucx, ucy - 8, "Verification scenario", 30, weight="bold", anchor="middle")
    s.text(ucx, ucy + 32, "use case", 24, fill=MUTED, anchor="middle")
    # block
    bx, by, bw, bh = 1130, 470, 400, 170
    s.rect(bx, by, bw, bh, fill=FILL, stroke=INK, sw=2.5, rx=6)
    s.text(bx + bw / 2, by + 52, "«block»", 24, fill=MUTED, anchor="middle")
    s.text(bx + bw / 2, by + 100, "Test cell equipment", 30, weight="bold", anchor="middle")
    s.text(bx + bw / 2, by + 140, "structure", 24, fill=MUTED, anchor="middle")
    # activity
    ax, ay, aw, ah = 1130, 735, 400, 120
    s.rect(ax, ay, aw, ah, fill=FILL, stroke=INK, sw=2.5, rx=40)
    s.text(ax + aw / 2, ay + 52, "Test function", 30, weight="bold", anchor="middle")
    s.text(ax + aw / 2, ay + 88, "activity", 24, fill=MUTED, anchor="middle")
    # dependencies (client -> supplier, dashed with open arrowhead)
    s.line([(ucx + 120, ucy - 92), (rx_ + 60, ry_ + rh)], color=INK, sw=2.5, dash="12 9", marker="open")
    s.text(525, 362, "«refine»", 30, weight="semibold", anchor="end")
    s.line([(bx + 140, by), (rx_ + rw - 60, ry_ + rh)], color=INK, sw=2.5, dash="12 9", marker="open")
    s.text(1150, 352, "«satisfy»", 30, weight="semibold", anchor="start")
    s.line([(ax + aw / 2, ay), (bx + bw / 2, by + bh)], color=INK, sw=2.5, dash="12 9", marker="open")
    s.text(ax + aw / 2 - 24, ay - 30, "«allocate»", 30, weight="semibold", anchor="end")
    s.text(60, 860, "Dashed arrows run from the element that does the work to the element it serves.", 24, fill=MUTED)
    save("test-cells-traceability-pattern.svg", s)


# ---------------------------------------------------------------- figure: family taxonomy
def family_taxonomy():
    s = SVG(1600, 820)
    tx, ty, tw, th = 530, 40, 540, 350
    s.rect(tx, ty, tw, th, fill=NAVY_T1, stroke=NAVY, sw=3, rx=6)
    s.text(800, ty + 46, "«block»", 24, fill=MUTED, anchor="middle")
    s.text(800, ty + 92, "Test Cell", 34, weight="bold", anchor="middle", italic=True)
    s.line([(tx, ty + 120), (tx + tw, ty + 120)], color=NAVY_T3, sw=2)
    s.text(tx + 28, ty + 160, "parts", 22, fill=MUTED, italic=True)
    s.text(tx + 28, ty + 196, "support equipment", 26)
    s.text(tx + 28, ty + 230, "data recording", 26)
    s.line([(tx, ty + 250), (tx + tw, ty + 250)], color=NAVY_T3, sw=2)
    s.text(tx + 28, ty + 288, "references", 22, fill=MUTED, italic=True)
    s.text(tx + 28, ty + 324, "unit under test : proxy ports", 26)
    # variants
    vw, vh, gap, vy = 300, 150, 60, 600
    x0 = (1600 - (4 * vw + 3 * gap)) / 2
    bus = 480
    for i, n in enumerate("ABCD"):
        x = x0 + i * (vw + gap)
        s.rect(x, vy, vw, vh, fill=FILL, stroke=INK, sw=2.5, rx=6)
        s.text(x + vw / 2, vy + 52, "«block»", 22, fill=MUTED, anchor="middle")
        s.text(x + vw / 2, vy + 98, f"Test cell {n}", 30, weight="bold", anchor="middle")
        s.line([(x + vw / 2, vy), (x + vw / 2, bus)], color=INK, sw=2.5)
    s.line([(x0 + vw / 2, bus), (x0 + 3 * (vw + gap) + vw / 2, bus)], color=INK, sw=2.5)
    s.line([(800, bus), (800, ty + th)], color=INK, sw=2.5, marker="tri")
    s.text(830, 430, "each variant specializes the common block", 24, fill=MUTED, italic=True)
    save("test-cells-family-taxonomy.svg", s)


# ---------------------------------------------------------------- card: sim CI gate ladder
def card_sim_ci():
    s = SVG(1600, 900)
    lx, lw, rh, gap, top = 260, 900, 150, 30, 100
    rungs = [
        ("Milestone", "acceptance set when its trigger arrives", EMPH, WHITE, ON_EMPH),
        ("On release", "measured figures recorded with the release", NAVY_T3, INK, INK),
        ("Nightly", "timing ratios and longer runs, kept off merges so runner load can't fail them", NAVY_T2, INK, MUTED),
        ("Per merge", "fast static and short-run checks that block the merge", NAVY_T1, INK, MUTED),
    ]
    for i, (name, desc, fill, tcol, dcol) in enumerate(rungs):
        y = top + i * (rh + gap)
        s.rect(lx, y, lw, rh, fill=fill, stroke=fill if fill != NAVY_T1 else NAVY_T3, rx=16)
        s.text(lx + 40, y + rh / 2 + 14, name, 40, fill=tcol, weight="bold")
        dl = wrap(desc, 27, lw - 340 - 40)
        lh = 36
        base = y + rh / 2 - (len(dl) - 1) * lh / 2 + 10
        s.lines(lx + 340, base, dl, 27, lh=lh, fill=dcol)
    bottom = top + 4 * rh + 3 * gap
    s.line([(170, bottom), (170, top + 6)], color=NAVY, sw=5, marker="arrN")
    s.text(130, (top + bottom) / 2, "longer to run, later to report", 28, fill=MUTED, anchor="middle", rotate=-90)
    # method tag
    mx, my, mw, mh = 1250, 330, 300, 230
    s.rect(mx, my, mw, mh, fill=AMBER_T, stroke=AMBER, sw=2.5, rx=16)
    s.text(mx + mw / 2, my + 62, "Method letter", 30, weight="bold", fill=AMBER, anchor="middle")
    s.text(mx + mw / 2, my + 130, "T / D / A / I", 44, weight="bold", anchor="middle")
    s.text(mx + mw / 2, my + 182, "contractual", 26, fill=MUTED, anchor="middle")
    s.line([(mx, my + mh / 2), (lx + lw + 6, my + mh / 2)], color=AMBER, sw=3, dash="10 8")
    s.text(mx + mw / 2, my + mh + 50, "does not set the rung", 26, fill=AMBER, anchor="middle", italic=True)
    save("card-sim-ci.svg", s)


# ---------------------------------------------------------------- card: NLP (simplified)
def card_nlp():
    s = SVG(1600, 900)
    # inputs
    s.block(50, 150, 380, 150, "Requirements", "full sentences, from JAMA", tsize=38, ssize=26)
    s.block(50, 400, 380, 150, "Model activities", "short verb-noun names", tsize=38, ssize=26)
    # scorers
    sx, sw_, shh, sg = 640, 380, 92, 22
    names = ["BM25", "Semantic similarity", "Domain knowledge", "Query expansion"]
    ys = [130 + i * (shh + sg) for i in range(4)]
    bus_l, bus_r = 560, 1110
    s.line([(430, 225), (bus_l, 225)], color=NAVY, sw=4)
    s.line([(430, 475), (bus_l, 475)], color=NAVY, sw=4)
    s.line([(bus_l, ys[0] + shh / 2), (bus_l, ys[3] + shh / 2)], color=NAVY, sw=4)
    for y, n in zip(ys, names):
        s.line([(bus_l, y + shh / 2), (sx - 4, y + shh / 2)], color=NAVY, sw=4, marker="arrN")
        s.rect(sx, y, sw_, shh, fill=NAVY_T1, stroke=NAVY_T3, rx=46)
        s.text(sx + sw_ / 2, y + shh / 2 + 12, n, 32, weight="semibold", anchor="middle")
        s.line([(sx + sw_, y + shh / 2), (bus_r, y + shh / 2)], color=NAVY, sw=4)
    s.line([(bus_r, ys[0] + shh / 2), (bus_r, ys[3] + shh / 2)], color=NAVY, sw=4)
    mid = (ys[0] + ys[3] + shh) / 2
    s.line([(bus_r, mid), (1176, mid)], color=NAVY, sw=4, marker="arrN")
    s.rect(1180, mid - 130, 370, 260, fill=EMPH, stroke=EMPH, rx=18)
    s.text(1365, mid - 52, "Ranked matches", 36, fill=WHITE, weight="bold", anchor="middle")
    s.lines(1365, mid + 6, ["top five per requirement,", "each with its reasons"], 26, lh=36, fill=ON_EMPH, anchor="middle")
    # quality lane
    qy = 690
    s.line([(50, 225), (24, 225), (24, qy + 75), (636, qy + 75)], color=TEAL, sw=4, marker="arrT")
    s.rect(640, qy, 380, 150, fill=TEAL_T, stroke=TEAL, sw=2.5, rx=16)
    s.text(830, qy + 66, "Quality grader", 34, weight="bold", fill=TEAL, anchor="middle")
    s.text(830, qy + 110, "INCOSE writing rules", 26, fill=MUTED, anchor="middle")
    s.line([(1020, qy + 75), (1176, qy + 75)], color=TEAL, sw=4, marker="arrT")
    s.rect(1180, qy, 370, 150, fill=TEAL_T, stroke=TEAL, sw=2.5, rx=16)
    s.text(1365, qy + 66, "Graded defects", 34, weight="bold", fill=TEAL, anchor="middle")
    s.text(1365, qy + 110, "issues and suggested fixes", 26, fill=MUTED, anchor="middle")
    save("card-nlp.svg", s)


# ---------------------------------------------------------------- figure: NLP pipeline (portrait, readable in a narrow column)
def nlp_pipeline():
    s = SVG(1400, 1540)
    T, S = 30, 23
    # row 1 inputs
    y1, h1 = 50, 160
    ins = [(110, "Manual traces", "requirement to activities"), (420, "Activities", "name"),
           (730, "Requirements", "ID, name, text")]
    for x, t, sub in ins:
        s.block(x, y1, 280, h1, t, sub, tsize=T, ssize=S)
    # row 2 preparation
    y2, h2 = 290, 180
    s.block(110, y2, 420, h2, "Domain knowledge",
            "vocabulary, synonyms, abbreviations, and term relationships learned from manual traces", tsize=T, ssize=S,
            fill=NAVY_T1, stroke=NAVY_T3)
    s.block(590, y2, 420, h2, "Preprocess", "tokenize, lemmatize, expand abbreviations, extract terms and phrases",
            tsize=T, ssize=S, fill=NAVY_T1, stroke=NAVY_T3)
    s.line([(250, y1 + h1), (250, y2 - 4)], color=NAVY, sw=3, marker="arrN")
    s.line([(560, y1 + h1), (560, y1 + h1 + 40), (720, y1 + h1 + 40), (720, y2 - 4)], color=NAVY, sw=3, marker="arrN")
    s.line([(870, y1 + h1), (870, y2 - 4)], color=NAVY, sw=3, marker="arrN")
    # bus into scorers
    bus = 510
    s.line([(320, y2 + h2), (320, bus)], color=NAVY, sw=3)
    s.line([(800, y2 + h2), (800, bus)], color=NAVY, sw=3)
    s.line([(330, bus), (790, bus)], color=NAVY, sw=3)
    s.line([(110 + 210, bus), (110 + 210, bus)], color=NAVY, sw=3)
    # scorers 2x2
    sy1, sy2, sh = 560, 715, 125
    cols = [110, 575]
    scorers = [("Domain", "vocabulary and learned relationships"),
               ("Query expansion", "activity widened with synonyms"),
               ("BM25", "shared rare terms and acronyms"),
               ("Semantic", "spaCy or sentence-transformer similarity")]
    pos = [(cols[0], sy1), (cols[1], sy1), (cols[0], sy2), (cols[1], sy2)]
    s.line([(320, bus), (320, sy1 - 4)], color=NAVY, sw=3, marker="arrN")
    s.line([(785, bus), (785, sy1 - 4)], color=NAVY, sw=3, marker="arrN")
    for (x, y), (t, sub) in zip(pos, scorers):
        s.block(x, y, 435, sh, t, sub, tsize=T, ssize=S)
        s.rect(x + 435 - 78, y + 12, 64, 32, fill=PAPER, stroke=STROKE, rx=16)
        s.text(x + 435 - 46, y + 35, "0–1", 19, fill=MUTED, anchor="middle")
    # combination
    yc, hc = 900, 140
    s.line([(560, sy2 + sh), (560, yc - 4)], color=NAVY, sw=3, marker="arrN")
    s.rect(110, yc, 900, hc, fill=EMPH, stroke=EMPH, rx=16)
    s.text(560, yc + 60, "Weighted combination", T + 2, fill=WHITE, weight="bold", anchor="middle")
    s.text(560, yc + 102, "top five per requirement, with an explanation for every pair", S, fill=ON_EMPH, anchor="middle")
    # outputs
    yo, ho = 1110, 140
    s.line([(330, yc + hc), (330, yo - 4)], color=NAVY, sw=3, marker="arrN")
    s.line([(790, yc + hc), (790, yo - 4)], color=NAVY, sw=3, marker="arrN")
    s.block(110, yo, 435, ho, "Review workbook", "High, Medium, Low, and Detail tabs", tsize=T, ssize=S)
    s.block(575, yo, 435, ho, "Explanations", "JSON, one record per pair", tsize=T, ssize=S)
    # evaluation loop
    ye, he = 1330, 140
    s.line([(330, yo + ho), (330, ye - 4)], color=LINE, sw=3, dash="9 8", marker="arrG")
    s.block(110, ye, 900, he, "Evaluation", "Hit@k, MRR, and precision, recall, and F1 at k against the manual traces",
            tsize=T, ssize=S, fill=PAPER, stroke=LINE, dash="10 8")
    s.line([(110, ye + he / 2), (60, ye + he / 2), (60, y1 + h1 / 2), (106, y1 + h1 / 2)], color=LINE, sw=3, dash="9 8",
           marker="arrG")
    s.text(44, (ye + y1 + h1) / 2, "answer key", 22, fill=MUTED, anchor="middle", rotate=-90, italic=True)
    # quality grader lane
    gx, gw = 1080, 290
    s.line([(1010, y1 + h1 / 2), (gx + gw / 2, y1 + h1 / 2), (gx + gw / 2, sy1 - 4)], color=TEAL, sw=3, marker="arrT")
    s.block(gx, sy1, gw, sh + (sy2 - sy1), "Quality grader",
            "five dimensions, INCOSE pattern check, semantic pass, and a cap for critical defects",
            tsize=T, ssize=S, fill=TEAL_T, stroke=TEAL, tcolor=TEAL)
    s.line([(gx + gw / 2, sy2 + sh), (gx + gw / 2, yc - 4)], color=TEAL, sw=3, marker="arrT")
    s.block(gx, yc, gw, hc, "Quality report", "grade, issues, and suggested fixes", tsize=T, ssize=S, fill=TEAL_T,
            stroke=TEAL, tcolor=TEAL)
    save("nlp-pipeline.svg", s)


# ---------------------------------------------------------------- figure: ShipWall architecture
def shipwall_architecture():
    s = SVG(1800, 1040)
    T, S = 26, 21
    # cloud
    s.block(30, 170, 270, 130, "AISStream", "WebSocket feed", tsize=T + 2, ssize=S)
    # Pi container
    px, py, pw, ph = 380, 60, 760, 760
    s.rect(px, py, pw, ph, fill=CONTAINER, stroke=NAVY_T3, sw=2.5, rx=22)
    s.text(px + 28, py + 40, "Raspberry Pi 3B", 28, weight="bold", fill=NAVY)
    s.rect(px + 15, 112, 730, 190, fill="none", stroke=NAVY_T3, sw=1.5, rx=12, dash="6 6")
    s.text(px + 30, 288, "register_service.py", 20, fill=MUTED, mono=True)
    by, bh = 120 + 0, 120
    by = 125
    s.block(px + 30, by + 0, 190, bh, "Ingest", None, tsize=T)
    s.block(px + 270, by + 0, 210, bh, "Vessel register", None, tsize=T)
    s.block(px + 530, by + 0, 200, bh, "Frame builder", None, tsize=T)
    # data path arrows (navy)
    s.line([(300, 235), (px + 26, by + bh / 2)], color=NAVY, sw=4, marker="arrN")
    s.text(165, 336, "position and static reports", S, fill=MUTED, anchor="middle")
    s.line([(px + 220, by + bh / 2), (px + 266, by + bh / 2)], color=NAVY, sw=4, marker="arrN")
    s.line([(px + 480, by + bh / 2), (px + 526, by + bh / 2)], color=NAVY, sw=4, marker="arrN")
    s.badge(340, 200, 4)
    # stores and crossing
    s.cylinder(px + 30, 330, 200, 120, "Register and MMSI data")
    s.line([(px + 330, by + bh), (px + 330, 380), (px + 234, 380)], color=LINE, sw=3, marker="arrG")
    s.block(px + 270, 470, 210, 120, "crossing.py", "shared crossing state machine", tsize=T - 2, ssize=S - 2, tmono=True,
            tweight="bold")
    s.line([(px + 400, by + bh), (px + 400, 466)], color=NAVY, sw=3, marker="arrN")
    s.cylinder(px + 30, 495, 200, 110, "Passage log")
    s.line([(px + 270, 530), (px + 234, 530)], color=LINE, sw=3, marker="arrG")
    s.block(px + 530, 330, 200, 140, "webapp.py", "live mirror and passage stats", tsize=T - 2, ssize=S - 2, tmono=True)
    s.line([(px + 130, 605), (px + 130, 625), (px + 630, 625), (px + 630, 474)], color=LINE, sw=3, marker="arrG")
    # ops strip
    oy, oh = 660, 130
    s.block(px + 30, oy, 220, oh, "deploy.sh", "ff-only pull, compile gate", tsize=T - 3, ssize=S - 2, tmono=True,
            fill=PAPER)
    s.block(px + 270, oy, 210, oh, "backup.sh", "hourly timer", tsize=T - 3, ssize=S - 2, tmono=True, fill=PAPER)
    s.block(px + 495, oy, 245, oh, "panel-watchdog.sh", "systemd timer, every minute", tsize=19, ssize=S - 2,
            tmono=True, fill=PAPER)
    s.badge(px + 722, oy + 6, 3)
    # display band
    ex, ew = 1480, 290
    s.block(ex, 125, ew, 130, "ESP32-S3", "MatrixPortal, renders frames", tsize=T + 2, ssize=S)
    s.badge(ex + ew - 6, 125, 1)
    s.line([(px + 730, by + 45), (ex - 4, by + 45)], color=NAVY, sw=4, marker="arrN")
    s.line([(ex, by + 92), (px + 734, by + 92)], color=LINE, sw=3, marker="arrG")
    s.lines(1310, by + 25, ["JSON frame, one line every 10 s"], S, fill=INK, anchor="middle")
    s.lines(1310, by + 128, ["heartbeat 1/s"], S, fill=MUTED, anchor="middle")
    s.badge(px + 778, by + 92, 2)
    s.text(1310, by + 160, "USB serial, 115200", S, fill=MUTED, anchor="middle")
    s.block(ex, 330, ew, 120, "HUB75 panel", "128 × 64 LEDs", tsize=T + 2, ssize=S)
    s.line([(ex + ew / 2, 255), (ex + ew / 2, 326)], color=NAVY, sw=4, marker="arrN")
    # contract + mock
    s.rect(1215, 330, 190, 120, fill=AMBER_T, stroke=AMBER, sw=2.5, rx=8)
    s.text(1310, 380, "FRAME_SCHEMA.md", 20, fill=AMBER, weight="bold", anchor="middle", mono=True)
    s.text(1310, 416, "wire contract", S, fill=INK, anchor="middle")
    s.line([(1310, 330), (1310, by + 170)], color=AMBER, sw=2.5, dash="8 7")
    s.block(ex, 520, ew, 140, "register_panel.py", "browser mock, the reference renderer", tsize=T - 3, ssize=S - 1,
            tmono=True, fill=PAPER, stroke=AMBER, dash="10 8")
    s.line([(ex, 590), (1310, 590), (1310, 454)], color=AMBER, sw=2.5, dash="8 7")
    s.text(1310, 630, "implements the same contract", S, fill=AMBER, anchor="middle", italic=True)
    # outbound
    oy2 = 880
    s.block(px + 30, oy2, 330, 120, "Private data repo", "hourly; refuses null-byte files", tsize=T - 2, ssize=S - 2)
    s.line([(px + 375, oy + oh), (px + 375, 845), (px + 195, 845), (px + 195, oy2 - 4)], color=LINE, sw=3,
           marker="arrG")
    s.block(820, oy2, 240, 120, "Tailscale", None, tsize=T)
    s.line([(940, py + ph), (940, oy2 - 4)], color=LINE, sw=3, marker="arrG", marker_start="arrG")
    s.block(1150, oy2, 240, 120, "SSH", "me, from Massachusetts", tsize=T - 2, ssize=S - 2)
    s.block(1480, oy2, 290, 120, "Public web page", "served through Funnel", tsize=T - 2, ssize=S - 2)
    s.line([(1060, oy2 + 60), (1146, oy2 + 60)], color=LINE, sw=3, marker="arrG")
    s.line([(1060, oy2 + 100), (1100, oy2 + 100), (1100, 1020), (1625, 1020), (1625, oy2 + 124)], color=LINE, sw=3,
           marker="arrG")
    # legend for badges
    s.text(30, 440, "Watchdogs", 24, weight="bold", fill=AMBER)
    items = ["firmware heartbeat, once a second", "service reboots the board after 90 s of silence",
             "systemd timer restarts the service after 180 s", "reconnect a silent feed after 600 s"]
    yy = 480
    for i, it in enumerate(items, 1):
        s.badge(48, yy, i, r=16)
        ls = wrap(it, 20, 270)
        s.lines(76, yy + 7, ls, 20, lh=26, fill=INK)
        yy += 26 * len(ls) + 22
    save("shipwall-architecture.svg", s)


# ---------------------------------------------------------------- chart: ShipWall incidents by month
def shipwall_incidents(data):
    s = SVG(1200, 640, bg=CHART_BG)
    left, right, top, bottom = 120, 1150, 70, 540
    ymax = 15
    def yv(v): return bottom - (bottom - top) * v / ymax
    for t in range(0, ymax + 1, 5):
        y = yv(t)
        s.line([(left, y), (right, y)], color=GRID if t else AXIS, sw=1.5 if t else 2)
        s.text(left - 16, y + 8, str(t), 22, fill=MUTED, anchor="end")
    s.text(40, (top + bottom) / 2, "Incidents logged", 22, fill=MUTED, anchor="middle", rotate=-90)
    n = len(data)
    slot = (right - left) / n
    bw = min(120, slot * 0.5)
    for i, (m, v) in enumerate(data):
        cx = left + slot * (i + 0.5)
        y = yv(v)
        r = 4
        s.add(f'<path d="M{cx - bw / 2},{bottom} L{cx - bw / 2},{y + r} Q{cx - bw / 2},{y} {cx - bw / 2 + r},{y} '
              f'L{cx + bw / 2 - r},{y} Q{cx + bw / 2},{y} {cx + bw / 2},{y + r} L{cx + bw / 2},{bottom} Z" fill="{BAR}"/>')
        s.text(cx, y - 14, str(v), 26, fill=INK, weight="semibold", anchor="middle")
        s.text(cx, bottom + 38, m, 24, fill=INK, anchor="middle")
    # unattended marker between first and second month
    mx = left + slot
    s.line([(mx, top - 20), (mx, bottom)], color=AXIS, sw=2, dash="7 6")
    s.text(mx + 12, top - 6, "running unattended from early July", 21, fill=MUTED)
    s.text(left + slot * 0.5, bottom + 74, "includes bench bring-up", 20, fill=MUTED, anchor="middle", italic=True)
    save("shipwall-incidents-by-month.svg", s)


if __name__ == "__main__":
    card_interface_control()
    card_test_cells()
    traceability_pattern()
    family_taxonomy()
    card_sim_ci()
    card_nlp()
    nlp_pipeline()
    shipwall_architecture()
    shipwall_incidents([("June", 14), ("July", 4), ("August", 2), ("September", 1)])
    print("ok", sorted(os.listdir(OUT)))


# ---------------------------------------------------------------- figure: F.19 match explanation (from Ben's run)
def chips(s, x, y, maxw, items, size=22, filled=True, gap=10, h=40, fill=NAVY_T1, stroke=NAVY_T3, tcol=INK,
          outline_items=()):
    cx, cy = x, y
    for it in items:
        w = width(it, size, "medium") + 28
        if cx + w > x + maxw:
            cx, cy = x, cy + h + gap
        if it in outline_items:
            s.rect(cx, cy, w, h, fill=PAPER, stroke=LINE, sw=2, rx=h / 2, dash="5 4")
            s.text(cx + w / 2, cy + h / 2 + 8, it, size, fill=MUTED, weight="medium", anchor="middle")
        else:
            s.rect(cx, cy, w, h, fill=fill, stroke=stroke, sw=1.5, rx=h / 2)
            s.text(cx + w / 2, cy + h / 2 + 8, it, size, fill=tcol, weight="medium", anchor="middle")
        cx += w + gap
    return cy + h


def nlp_f19():
    s = SVG(1600, 1030)
    # header band
    s.rect(40, 30, 1520, 190, fill=NAVY_T1, stroke=NAVY_T3, rx=18)
    s.text(80, 82, "Requirement F.19", 24, fill=MUTED, weight="semibold")
    req = "The system shall transmit quality control data to Earth in real-time with a latency of no more than 2 seconds."
    s.lines(80, 124, wrap(req, 28, 800), 28, lh=38, weight="medium")
    s.line([(930, 135), (1000, 135)], color=NAVY, sw=4, marker="arrN", marker_start="arrN")
    s.text(1040, 82, "Activity", 24, fill=MUTED, weight="semibold")
    s.lines(1040, 124, wrap("1.2.5 Transmit Data to Ground Control", 30, 480, weight="bold"), 30, lh=40, weight="bold")
    # cards
    cw, gap, top, ch = 352, 37, 255, 600
    xs = [40 + i * (cw + gap) for i in range(4)]
    cards = [("BM25", 0.808, "Shared rare terms"), ("Semantic", 0.770, "Word-vector similarity"),
             ("Domain", 1.000, "Vocabulary and learned relationships"), ("Query expansion", 0.778, "Activity widened with synonyms")]
    for x, (name, sc, sub) in zip(xs, cards):
        s.rect(x, top, cw, ch, fill=PAPER, stroke=STROKE, rx=16)
        s.text(x + 28, top + 56, name, 32, weight="bold")
        s.lines(x + 28, top + 94, wrap(sub, 22, cw - 56), 22, lh=28, fill=MUTED)
        bw = cw - 56 - 86
        s.rect(x + 28, top + 140, bw, 14, fill=TRACK, stroke=TRACK, sw=0, rx=7)
        s.rect(x + 28, top + 140, max(14, bw * sc), 14, fill=EMPH, stroke=EMPH, sw=0, rx=7)
        s.text(x + cw - 28, top + 157, f"{sc:.2f}", 30, weight="bold", fill=NAVY, anchor="end")
    inner = cw - 56
    # BM25
    x = xs[0] + 28
    s.text(x, top + 208, "3 shared terms", 22, fill=MUTED, weight="semibold")
    y = chips(s, x, top + 226, inner, ["control", "datum", "transmit"])
    s.text(x, y + 50, "aerospace boost", 22, fill=MUTED, weight="semibold")
    chips(s, x, y + 68, inner, ["control"], fill=AMBER_T, stroke=AMBER, tcol=AMBER)
    # Semantic
    x = xs[1] + 28
    s.lines(x, top + 214, wrap("spaCy compares the two texts as wholes, which credits pairs that say the same thing in different words, the case the other three scorers can miss.", 23, inner), 23, lh=32, fill=INK)
    # Domain
    x = xs[2] + 28
    s.text(x, top + 208, "learned from manual traces", 22, fill=MUTED, weight="semibold")
    rel = [("latency", "control, ground, datum, transmit"), ("transmit", "control, ground, datum"),
           ("control", "transmit, ground, datum")]
    yy = top + 250
    for k, v in rel:
        s.text(x, yy, k + " →", 23, weight="semibold")
        ls = wrap(v, 22, inner - 16)
        s.lines(x + 16, yy + 32, ls, 22, lh=28, fill=MUTED)
        yy += 32 + 28 * len(ls) + 14
    s.lines(x, yy + 14, wrap("+0.10 for multiple kinds of evidence", 22, inner, italic=True), 22, lh=28, fill=MUTED, italic=True)
    # Query expansion
    x = xs[3] + 28
    s.text(x, top + 208, "7 of 9 terms covered", 22, fill=MUTED, weight="semibold")
    terms = ["control", "real", "transmit", "datum", "latency", "system", "second", "time", "quality"]
    y = chips(s, x, top + 226, inner, terms, outline_items=("latency", "quality"))
    s.lines(x, y + 44, wrap("after widening the activity with 32 synonyms; dashed terms were not covered", 21, inner), 21, lh=28,
            fill=MUTED, italic=True)
    # footer
    fy = top + ch + 40
    s.rect(40, fy, 1520, 110, fill=EMPH, stroke=EMPH, rx=18)
    s.text(80, fy + 68, "Ranked first of the five candidates the matcher kept for F.19", 30, fill=WHITE, weight="bold")
    s.text(1520, fy + 68, "terms are lemmas, so data appears as datum", 22, fill=ON_EMPH, anchor="end", italic=True)
    save("nlp-f19-explanation.svg", s)


nlp_f19()


# ---------------------------------------------------------------- example (invented): swimlane activity for a test cell
def example_activity():
    s = SVG(1600, 760)
    s.text(40, 52, "Invented example: a power-on functional test, drawn the way each test cell's behavioral view is", 24, fill=MUTED, italic=True)
    lanes = [("Test operator", 90), ("Test cell", 300), ("Unit under test", 510)]
    lh = 210
    for name, y in lanes:
        s.rect(40, y, 1540, lh, fill=PAPER, stroke=STROKE, rx=0, sw=1.5)
        s.rect(40, y, 170, lh, fill=FILL, stroke=STROKE, rx=0, sw=1.5)
        s.lines(125, y + lh / 2 - (len(wrap(name, 24, 140, weight="semibold")) - 1) * 15 + 8,
                wrap(name, 24, 140, weight="semibold"), 24, lh=30, anchor="middle", weight="semibold")
    cy = {"op": 195, "cell": 405, "uut": 615}
    w, h = 180, 104
    steps = [("op", 280, "Start the procedure"), ("cell", 490, "Apply power to the unit"),
             ("uut", 700, "Run built-in test and report status"), ("cell", 910, "Evaluate status against limits"),
             ("cell", 1120, "Record test data"), ("op", 1330, "Review the results")]
    # initial and final nodes
    s.add(f'<circle cx="246" cy="{cy["op"]}" r="13" fill="{INK}"/>')
    s.line([(259, cy["op"]), (276, cy["op"])], color=NAVY, sw=3, marker="arrN")
    for i, (lane, x, t) in enumerate(steps):
        y = cy[lane] - h / 2
        s.block(x, y, w, h, t, None, tsize=22, fill=NAVY_T1, stroke=NAVY_T3, rx=26, pad=14, tweight="semibold")
        if i + 1 < len(steps):
            nl, nx, _ = steps[i + 1]
            x1, y1, x2, y2 = x + w, cy[lane], nx, cy[nl]
            xm = (x1 + x2) / 2
            pts = [(x1, y1), (x2 - 4, y2)] if y1 == y2 else [(x1, y1), (xm, y1), (xm, y2), (x2 - 4, y2)]
            s.line(pts, color=NAVY, sw=3, marker="arrN")
    fx = 1330 + w + 40
    s.line([(1330 + w, cy["op"]), (fx - 20, cy["op"])], color=NAVY, sw=3, marker="arrN")
    s.add(f'<circle cx="{fx}" cy="{cy["op"]}" r="16" fill="none" stroke="{INK}" stroke-width="3"/>')
    s.add(f'<circle cx="{fx}" cy="{cy["op"]}" r="9" fill="{INK}"/>')
    tags = [(490, "stimulus"), (700, "response"), (910, "evaluation"), (1120, "recording")]
    for x, t in tags:
        lane_y = cy["uut"] if t == "response" else cy["cell"]
        s.text(x + w / 2, lane_y + h / 2 + 32, t, 20, fill=AMBER, anchor="middle", italic=True)
    save("test-cells-example-activity.svg", s)


# ---------------------------------------------------------------- example (invented): proving a check before trusting it
def example_proving_check():
    s = SVG(1600, 460)
    s.text(40, 52, "Invented example: a check that every requirement's verification method is one of T, D, A, or I", 24, fill=MUTED, italic=True)
    steps = [("Plant a defect", "set one requirement's method to X"), ("The check must fail", "and name that requirement"),
             ("Remove the defect", "restore the original value"), ("The check must pass", "on the clean workbook"),
             ("Trusted", "a clean result now means something")]
    w, h, gap, y = 270, 170, 50, 110
    x0 = (1600 - (5 * w + 4 * gap)) / 2
    for i, (t, sub) in enumerate(steps):
        x = x0 + i * (w + gap)
        if i == 4:
            s.rect(x, y, w, h, fill=EMPH, stroke=EMPH, rx=18)
            s.text(x + w / 2, y + 72, t, 32, fill=WHITE, weight="bold", anchor="middle")
            s.lines(x + w / 2, y + 112, wrap(sub, 22, w - 40), 22, lh=28, fill=ON_EMPH, anchor="middle")
        else:
            s.block(x, y, w, h, t, sub, tsize=28, ssize=22, fill=NAVY_T1, stroke=NAVY_T3)
        if i < 4:
            s.line([(x + w + 4, y + h / 2), (x + w + gap - 6, y + h / 2)], color=NAVY, sw=4, marker="arrN")
    # failure loop under steps 1-2
    x1 = x0 + w / 2; x2 = x0 + (w + gap) + w / 2; yb = y + h + 70
    s.line([(x2, y + h + 4), (x2, yb), (x1, yb), (x1, y + h + 8)], color=AMBER, sw=3, dash="9 7", marker="arrG")
    s.lines((x1 + x2) / 2, yb + 44, ["passes with the defect in place?", "fix the check, then plant again"], 22, lh=30,
            fill=AMBER, anchor="middle", italic=True)
    save("sim-ci-proving-a-check.svg", s)


example_activity()
example_proving_check()
