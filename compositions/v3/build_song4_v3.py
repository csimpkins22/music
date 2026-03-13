#!/usr/bin/env python3
"""
Song 4 v3: "Last Signal Home"
Key: G major | Tempo: 58 BPM | 3/4 | ~4:27

v3 changes — real songwriting decisions:
- Bridge harmony: Am-Em-F-C-D (F major borrowed from mixolydian — drifting away)
- Final Chorus: 10 bars — 8 normal + 2 bars of E MAJOR (parallel major surprise)
  The G# in E major (where G natural has lived all song) = the emotional climax
- Verse 1 melody: waltz phrasing — notes land on beat 1, sustain through 2-3
- Bridge melody: highest note E6 appears on the F chord (peak on wrongest chord)
- Final chorus vocal: sustains B5 over E major (the 5th — "maybe it's okay")
- Pedal steel: plays G# over E major — the ONE note that changes
- Organ outro: pitch wobble drifts ±60 → ±200 cents (signal fading)
- Strings: enter for all 10 bars of final chorus, swell through E major
- Last sound: single fingerpicked G, alone. The tonic. Home.

Structure: Intro(8) V1(16) Ch1(8) V2(16) Ch2(8) Bridge(12) Final Ch(10) Outro(8) = 86 bars
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from humanize import *

E = EventList()

def bt(bar_num):
    return bar_num * BAR3


# ============================================================
# CHORD VOICINGS
# ============================================================

VERSE_V = [
    [make_chord(N('G',4),'major'), make_chord(N('G',4),'add9'), make_chord(N('G',4),'sus2')],
    [make_chord(N('E',4),'minor'), make_chord(N('E',4),'min7'), [N('E',4),N('G',4),N('B',4)]],
    [make_chord(N('C',4),'major'), make_chord(N('C',4),'add9'), [N('C',4),N('E',4),N('G',4)]],
    [make_chord(N('D',4),'major'), make_chord(N('D',4),'sus4'), [N('D',4),N('F#',4),N('A',4)]],
]
VERSE_BASS = [N('G',2), N('E',2), N('C',2), N('D',2)]

CHORUS_V = [
    [make_chord(N('E',4),'minor'), make_chord(N('E',4),'min7')],
    [make_chord(N('C',4),'major'), make_chord(N('C',4),'add9')],
    [make_chord(N('G',4),'major'), make_chord(N('G',4),'add9')],
    [make_chord(N('D',4),'major'), make_chord(N('D',4),'sus4')],
]
CHORUS_BASS = [N('E',2), N('C',2), N('G',2), N('D',2)]

# v3: Bridge uses F major instead of G — borrowed from mixolydian/C major
# Am - Em - F - C - D
BRIDGE_V = [
    [make_chord(N('A',3),'minor'), make_chord(N('A',3),'min7')],
    [make_chord(N('E',4),'minor'), [N('E',4),N('G',4),N('B',4)]],
    [make_chord(N('F',4),'major'), make_chord(N('F',4),'add9')],   # F major — the drift
    [make_chord(N('C',4),'major'), make_chord(N('C',4),'add9')],
    [make_chord(N('D',4),'major'), make_chord(N('D',4),'sus4')],
]
BRIDGE_BASS = [N('A',1), N('E',2), N('F',2), N('C',2), N('D',2)]  # F in bass too

# v3: E MAJOR chord for the final chorus surprise (parallel major of Em)
E_MAJOR_CHORD = make_chord(N('E',4), 'major')  # E-G#-B
E_MAJOR_BASS = N('E',2)

def gv(voicings, ci, bar):
    opts = voicings[ci]
    return opts[bar % len(opts)]


# ============================================================
# INSTRUMENT FUNCTIONS
# ============================================================

def fingerpick(bar_start, chord_notes, vel=46, bar_num=0):
    """Waltz fingerpicking with varied patterns and dynamics."""
    bass = chord_notes[0] - 12
    r, m, t = chord_notes[0], chord_notes[1], chord_notes[2]
    bvel = breathing_vel(vel, bar_num, 8, 5)

    patterns = [
        [(bass, bvel), (m, bvel-8), (t, bvel-10)],
        [(bass, bvel), (r, bvel-5), (m, bvel-8)],
        [(bass, bvel), (t, bvel-5), (m, bvel-8)],
        [(bass, bvel), (m, bvel-8), (r, bvel-10)],
    ]
    pat = patterns[bar_num % len(patterns)]

    for beat, (note, v) in enumerate(pat):
        v = v + accent_beat(beat, 'waltz') + random.randint(-3, 3)
        sw = swing_offset(beat, 6) if beat == 2 else 0
        dur = QUARTER - random.randint(12, 22)
        E.note(3, note, v, bar_start + beat * QUARTER + sw, dur, time_amount=8, vel_amount=3)

    if bar_num % 5 == 3:
        extra = chord_notes[1] - 1
        E.note(3, extra, bvel - 15, bar_start + HALF + EIGHTH, EIGHTH - 10,
               time_amount=10, vel_amount=3)


def waltz_bass(bar_start, root, vel=48, bar_num=0, next_root=None):
    bvel = breathing_vel(vel, bar_num, 8, 4)
    v1 = bvel + accent_beat(0, 'waltz') + random.randint(-3, 3)
    v2 = bvel + accent_beat(1, 'waltz') + random.randint(-3, 3)

    E.note(6, root, v1, bar_start, QUARTER - 15, time_amount=8, vel_amount=4)
    E.note(6, root + 7, v2, bar_start + QUARTER, QUARTER - 15, time_amount=10, vel_amount=3)

    if next_root and bar_num % 3 == 2:
        approach = next_root - 1 if next_root > root else next_root + 1
        E.note(6, approach, v2 - 5, bar_start + HALF, QUARTER - 15, time_amount=10, vel_amount=3)
    else:
        E.note(6, root + 7, v2 - 3, bar_start + HALF, QUARTER - 15, time_amount=8, vel_amount=3)


def pad_swell(bar_start, chord_notes, vel=38, bars=2, bar_num=0):
    steps = bars * 3
    for step in range(steps):
        t = bar_start + step * QUARTER
        swell = math.sin((step / steps) * math.pi)
        v = int(vel * 0.7 + vel * 0.3 * swell)
        E.cc(1, 11, max(40, min(127, int(v * 2.5))), h_time(t, 5))
    bvel = breathing_vel(vel, bar_num, 6, 4)
    for n in chord_notes:
        E.note(1, n, bvel, bar_start, BAR3 * bars - 30, time_amount=10, vel_amount=4)


def pedal_steel(bar_start, phrase, vel=45, bar_num=0):
    """Pedal steel with pitch bend for bending effect."""
    t = bar_start
    for i, (note, dur) in enumerate(phrase):
        if note is not None:
            v = breathing_vel(vel, bar_num + i, 4, 5)
            bend_dur = min(dur // 4, EIGHTH)
            E.pitch_bend(2, -2048, h_time(t - 5, 2))
            E.note(2, note, v, t, dur - 20, time_amount=8, vel_amount=4)
            steps = max(1, bend_dur // SIXTEENTH)
            for step in range(steps + 1):
                bend_val = int(-2048 + 2048 * (step / steps))
                E.pitch_bend(2, bend_val, h_time(t + step * SIXTEENTH, 3))
            if dur >= HALF:
                vib_start = t + bend_dur
                for step in range((dur - bend_dur) // SIXTEENTH):
                    vib = int(150 * math.sin(step * 0.6))
                    E.pitch_bend(2, vib, h_time(vib_start + step * SIXTEENTH, 3))
            E.pitch_bend(2, 0, t + dur)
        t += dur


def pedal_steel_sustained(bar_start, note, dur, vel=45, bar_num=0):
    """Pedal steel playing a single long sustained note — no bend-up, just vibrato.
    Used for the G# in the E major surprise."""
    v = breathing_vel(vel, bar_num, 4, 5)
    E.pitch_bend(2, 0, h_time(bar_start - 5, 2))
    E.note(2, note, v, bar_start, dur - 20, time_amount=6, vel_amount=4)
    # Deep, slow vibrato for emotional sustain
    for step in range(dur // SIXTEENTH):
        vib = int(200 * math.sin(step * 0.4))
        E.pitch_bend(2, vib, h_time(bar_start + step * SIXTEENTH, 3))
    E.pitch_bend(2, 0, bar_start + dur)


def waltz_drums(bar_start, pattern='basic', bar_num=0):
    ch = 9
    kick, snare, hh_c, hh_o, ride, crash, rim = 36, 38, 42, 46, 51, 49, 37
    bvel = breathing_vel(45, bar_num, 8, 4)

    if pattern == 'basic':
        E.note(ch, kick, bvel + accent_beat(0,'waltz'), bar_start, QUARTER,
               time_amount=6, vel_amount=4)
        v2 = 22 + random.randint(-3, 3)
        v3 = 20 + random.randint(-3, 3)
        E.note(ch, hh_c, v2, bar_start + QUARTER, QUARTER, time_amount=8, vel_amount=3)
        E.note(ch, hh_c, v3, bar_start + HALF, QUARTER, time_amount=8, vel_amount=3)

    elif pattern == 'verse':
        E.note(ch, kick, bvel + accent_beat(0,'waltz'), bar_start, QUARTER,
               time_amount=5, vel_amount=4)
        E.note(ch, hh_c, 23 + random.randint(-3,3), bar_start + QUARTER, QUARTER,
               time_amount=8, vel_amount=3)
        E.note(ch, rim, 28 + random.randint(-4,4), bar_start + HALF, QUARTER,
               time_amount=8, vel_amount=4)
        if bar_num % 3 == 1:
            E.note(ch, kick, bvel - 20, bar_start + QUARTER + EIGHTH, EIGHTH,
                   time_amount=12, vel_amount=3)

    elif pattern == 'chorus':
        E.note(ch, kick, bvel + 5 + accent_beat(0,'waltz'), bar_start, QUARTER,
               time_amount=4, vel_amount=4)
        E.note(ch, ride, 28 + random.randint(-3,3), bar_start, QUARTER,
               time_amount=6, vel_amount=3)
        E.note(ch, ride, 23 + random.randint(-3,3), bar_start + QUARTER, QUARTER,
               time_amount=7, vel_amount=3)
        E.note(ch, snare, 38 + random.randint(-4,4), bar_start + HALF, QUARTER,
               time_amount=6, vel_amount=4)
        E.note(ch, ride, 23 + random.randint(-3,3), bar_start + HALF, QUARTER,
               time_amount=7, vel_amount=3)

    elif pattern == 'brush':
        E.note(ch, kick, bvel - 8, bar_start, QUARTER, time_amount=8, vel_amount=4)
        for i in range(6):
            v = 13 + random.randint(-2, 3)
            E.note(ch, hh_c, v, bar_start + i * EIGHTH, EIGHTH, time_amount=8, vel_amount=2)

    elif pattern == 'crash':
        E.note(ch, crash, 60, bar_start, QUARTER, time_amount=3)
        E.note(ch, kick, 60, bar_start, QUARTER, time_amount=3)


def piano_waltz(bar_start, chord_notes, vel=43, bar_num=0):
    bvel = breathing_vel(vel, bar_num, 6, 4)
    E.cc(0, 64, 100, h_time(bar_start, 3))
    for i, n in enumerate(chord_notes):
        v = bvel + accent_beat(i, 'waltz') + random.randint(-3, 3)
        E.note(0, n, v, bar_start + i * QUARTER, QUARTER - random.randint(12, 20),
               time_amount=8, vel_amount=3)
    E.cc(0, 64, 0, h_time(bar_start + BAR3 - 30, 3))


def organ(bar_start, chord_notes, vel=30, bars=4, bar_num=0, wobble_cents=60):
    """Organ with configurable pitch wobble. wobble_cents controls bend amplitude."""
    bvel = breathing_vel(vel, bar_num, 6, 3)
    for n in chord_notes:
        E.note(5, n, bvel, bar_start, BAR3 * bars - 30, time_amount=12, vel_amount=4)
    for step in range(bars * 6):
        t = bar_start + step * EIGHTH
        bend = int(wobble_cents * math.sin(step * 0.3))
        E.pitch_bend(5, bend, h_time(t, 3))
    E.pitch_bend(5, 0, bar_start + BAR3 * bars)


def organ_fading(bar_start, chord_notes, vel=30, bars=8, bar_num=0):
    """Outro organ: pitch wobble drifts from ±60 to ±200 cents over bars.
    The signal fading, literally going out of tune."""
    bvel = breathing_vel(vel, bar_num, 6, 3)
    for n in chord_notes:
        E.note(5, n, bvel, bar_start, BAR3 * bars - 30, time_amount=12, vel_amount=4)
    total_steps = bars * 6
    for step in range(total_steps):
        t = bar_start + step * EIGHTH
        # Wobble grows from 60 to 200 cents across the outro
        progress = step / max(1, total_steps - 1)
        wobble = 60 + (200 - 60) * progress
        bend = int(wobble * math.sin(step * 0.3))
        E.pitch_bend(5, bend, h_time(t, 3))
    E.pitch_bend(5, 0, bar_start + BAR3 * bars)


def strings_swell(bar_start, chord_notes, vel=30, bars=4, bar_num=0):
    """Strings with expression swell."""
    steps = bars * 6
    for step in range(steps):
        t = bar_start + step * EIGHTH
        swell = math.sin((step / steps) * math.pi) ** 0.8
        v = max(30, min(120, int(40 + 80 * swell)))
        E.cc(7, 11, v, h_time(t, 3))
    bvel = breathing_vel(vel, bar_num, 8, 5)
    for n in [nn + 12 for nn in chord_notes]:
        E.note(7, n, bvel, bar_start, BAR3 * bars - 30, time_amount=12, vel_amount=5)


def strings_crescendo(bar_start, chord_notes, vel_start=20, vel_end=55, bars=10, bar_num=0):
    """Strings that crescendo over many bars — for the final chorus.
    Swells from quiet to full through the E major surprise."""
    steps = bars * 6
    for step in range(steps):
        t = bar_start + step * EIGHTH
        # Gradual crescendo with a slight exponential curve
        progress = (step / max(1, steps - 1)) ** 1.2
        expr = int(40 + 87 * progress)  # expression 40 → 127
        E.cc(7, 11, min(127, expr), h_time(t, 3))
    for n in [nn + 12 for nn in chord_notes[:3]]:  # Use first 3 notes of chord
        v = vel_start
        E.note(7, n, v, bar_start, BAR3 * bars - 30, time_amount=12, vel_amount=5)


def voice(bar_start, phrase, vel=50, bar_num=0):
    t = bar_start
    prev = None
    for i, (note, dur) in enumerate(phrase):
        if note is not None:
            v = vel
            if prev and note > prev + 3: v += 5
            elif prev and note < prev - 3: v -= 2
            v = breathing_vel(v, bar_num + i, 6, 5)
            antic = -SIXTEENTH if random.random() < 0.1 and i > 0 else 0
            if prev and abs(note - prev) >= 4 and random.random() < 0.2:
                grace = prev + (1 if note > prev else -1)
                E.note(8, grace, v - 14, t + antic - SIXTEENTH, SIXTEENTH - 5, time_amount=10)
            E.note(8, note, v, t + antic, dur - random.randint(20, 40), time_amount=10, vel_amount=5)
            prev = note
        t += dur


# ============================================================
# BUILD THE SONG — 86 bars total
# ============================================================

b = 0

# === INTRO (8 bars) ===
for i in range(8):
    ci = (i // 2) % 4
    fingerpick(bt(i), gv(VERSE_V, ci, i), vel=40, bar_num=i)
    if i >= 2:
        pedal_steel(bt(i), [(gv(VERSE_V, ci, i)[2] + 12, DOTTED_HALF)], vel=35, bar_num=i)
    if i >= 4 and i % 2 == 0:
        pad_swell(bt(i), gv(VERSE_V, ci, i), vel=23, bars=2, bar_num=i)

b = 8

# === VERSE 1 (16 bars) ===
# v3: waltz-phrased melody — notes land on beat 1, sustain through beats 2-3
for i in range(16):
    ci = (i // 2) % 4
    nci = ((i+1) // 2) % 4
    fingerpick(bt(b+i), gv(VERSE_V, ci, i), vel=44, bar_num=i+8)
    if i >= 4:
        waltz_bass(bt(b+i), VERSE_BASS[ci], vel=40, bar_num=i, next_root=VERSE_BASS[nci])
    if i >= 8:
        waltz_drums(bt(b+i), 'verse', bar_num=i+8)
    if i % 4 == 0:
        pad_swell(bt(b+i), gv(VERSE_V, ci, i+1), vel=28, bars=4, bar_num=i)

# v3 verse 1 melody: waltz phrasing — long notes on beat 1, breathe with 3/4
# Notes land on the downbeat and SUSTAIN. Fewer short notes, more weight.
v1 = [
    # Phrase 1: G lands on beat 1, holds through the bar, resolves to B
    [(N('G',5), DOTTED_HALF),
     (N('B',5), HALF), (N('D',6), QUARTER)],
    # Phrase 2: settle down — A holds, then G breathes across the bar
    [(N('A',5), DOTTED_HALF),
     (N('G',5), DOTTED_HALF)],
    # Phrase 3: E lifts to G, holds, A reaches up
    [(N('E',5), DOTTED_HALF),
     (N('G',5), HALF), (N('A',5), QUARTER)],
    # Phrase 4: resolve back — A sinks to G, then F# settles to G
    [(N('A',5), HALF), (N('G',5), QUARTER),
     (N('G',5), DOTTED_HALF)],
    # Phrase 5: second half — G reaches up to D, C pulls back
    [(N('G',5), DOTTED_HALF),
     (N('D',6), HALF), (N('C',6), QUARTER)],
    # Phrase 6: B holds, sinks to A — weight on the downbeats
    [(N('B',5), DOTTED_HALF),
     (N('A',5), DOTTED_HALF)],
    # Phrase 7: E holds, steps up to G
    [(N('E',5), DOTTED_HALF),
     (N('G',5), HALF), (None, QUARTER)],
    # Phrase 8: final phrase — G to F# resolve to D, all sustained
    [(N('G',5), HALF), (N('F#',5), QUARTER),
     (N('D',5), DOTTED_HALF)],
]
for pi, phrase in enumerate(v1):
    voice(bt(b + pi*2), phrase, vel=46, bar_num=pi+8)

b = 24

# === CHORUS 1 (8 bars) ===
waltz_drums(bt(b), 'crash', bar_num=24)
for i in range(8):
    ci = (i // 2) % 4
    nci = ((i+2) // 2) % 4
    fingerpick(bt(b+i), gv(CHORUS_V, ci, i), vel=48, bar_num=i+24)
    waltz_bass(bt(b+i), CHORUS_BASS[ci], vel=46, bar_num=i+8, next_root=CHORUS_BASS[nci])
    waltz_drums(bt(b+i), 'chorus', bar_num=i+24)
    if i % 2 == 0:
        pad_swell(bt(b+i), gv(CHORUS_V, ci, i+1), vel=36, bars=2, bar_num=i+8)
    piano_waltz(bt(b+i), gv(CHORUS_V, ci, i+2), vel=40, bar_num=i+24)

ch_mel = [
    [(N('B',5),HALF+EIGHTH),(N('D',6),EIGHTH),
     (N('E',6),HALF),(N('D',6),QUARTER)],
    [(N('C',6),QUARTER),(N('B',5),HALF),
     (N('A',5),DOTTED_HALF)],
    [(N('G',5),QUARTER),(N('B',5),QUARTER+EIGHTH),(N('D',6),EIGHTH),
     (N('C',6),HALF),(N('B',5),QUARTER)],
    [(N('A',5),QUARTER),(N('G',5),HALF),
     (N('G',5),DOTTED_HALF)],
]
for pi, phrase in enumerate(ch_mel):
    voice(bt(b + pi*2), phrase, vel=53, bar_num=pi+24)

# Pedal steel counter-melody for chorus
pedal_steel(bt(b), [(n, d) for n, d in zip(
    [N('G',5),N('F#',5),N('E',5),N('D',5),N('E',5),N('G',5),N('F#',5),N('D',5)],
    [DOTTED_HALF]*8)], vel=36, bar_num=24)

b = 32

# === VERSE 2 (16 bars) ===
for i in range(16):
    ci = (i // 2) % 4
    nci = ((i+1) // 2) % 4
    fingerpick(bt(b+i), gv(VERSE_V, ci, i+16), vel=46, bar_num=i+32)
    waltz_bass(bt(b+i), VERSE_BASS[ci], vel=42, bar_num=i+16, next_root=VERSE_BASS[nci])
    if i >= 4:
        waltz_drums(bt(b+i), 'verse', bar_num=i+32)
    if i % 4 == 0:
        pad_swell(bt(b+i), gv(VERSE_V, ci, i+3), vel=30, bars=4, bar_num=i+16)

v2m = [
    [(N('B',5),QUARTER),(N('A',5),QUARTER+EIGHTH),(N('G',5),EIGHTH),
     (N('D',5),HALF),(N('E',5),QUARTER)],
    [(N('G',5),QUARTER),(N('A',5),HALF),
     (N('B',5),DOTTED_HALF)],
    [(N('D',6),QUARTER),(N('C',6),QUARTER+EIGHTH),(N('B',5),EIGHTH),
     (N('A',5),HALF),(None,QUARTER)],
    [(N('G',5),QUARTER),(N('F#',5),QUARTER+EIGHTH),(N('E',5),EIGHTH),
     (N('G',5),DOTTED_HALF)],
    [(N('A',5),QUARTER),(N('B',5),QUARTER+EIGHTH),(N('D',6),EIGHTH),
     (N('E',6),HALF),(N('D',6),QUARTER)],
    [(N('C',6),QUARTER),(N('B',5),HALF),
     (N('A',5),DOTTED_HALF)],
    [(N('G',5),QUARTER),(N('A',5),QUARTER+EIGHTH),(N('B',5),EIGHTH),
     (N('C',6),HALF),(None,QUARTER)],
    [(N('B',5),QUARTER),(N('A',5),QUARTER+EIGHTH),(N('G',5),EIGHTH),
     (N('G',5),DOTTED_HALF)],
]
for pi, phrase in enumerate(v2m):
    voice(bt(b + pi*2), phrase, vel=48, bar_num=pi+32)

b = 48

# === CHORUS 2 (8 bars) + organ ===
waltz_drums(bt(b), 'crash', bar_num=48)
for i in range(8):
    ci = (i // 2) % 4
    nci = ((i+2) // 2) % 4
    fingerpick(bt(b+i), gv(CHORUS_V, ci, i+8), vel=50, bar_num=i+48)
    waltz_bass(bt(b+i), CHORUS_BASS[ci], vel=48, bar_num=i+24, next_root=CHORUS_BASS[nci])
    waltz_drums(bt(b+i), 'chorus', bar_num=i+48)
    piano_waltz(bt(b+i), gv(CHORUS_V, ci, i+4), vel=43, bar_num=i+48)
    if i % 2 == 0:
        pad_swell(bt(b+i), gv(CHORUS_V, ci, i+5), vel=38, bars=2, bar_num=i+24)
    if i % 4 == 0:
        organ(bt(b+i), gv(CHORUS_V, ci, i+3), vel=26, bars=4, bar_num=i+24)

for pi, phrase in enumerate(ch_mel):
    voice(bt(b + pi*2), phrase, vel=56, bar_num=pi+48)

b = 56

# === BRIDGE (12 bars) — Am-Em-F-C-D with F major borrowed chord ===
# v3: F replaces G. The F natural against G major key = drifting away from home.
bridge_seq = [0,1,2,3,4, 0,1,2,3,4, 0,1]
for i in range(12):
    ci = bridge_seq[i]
    piano_waltz(bt(b+i), gv(BRIDGE_V, ci, i), vel=50, bar_num=i+56)
    waltz_bass(bt(b+i), BRIDGE_BASS[ci], vel=46, bar_num=i+32,
               next_root=BRIDGE_BASS[bridge_seq[min(i+1,11)]])
    waltz_drums(bt(b+i), 'brush', bar_num=i+56)
    if i % 2 == 0:
        pad_swell(bt(b+i), gv(BRIDGE_V, ci, i+1), vel=33, bars=2, bar_num=i+32)
    # Guitar plays whole chords with rubato timing
    for n in gv(BRIDGE_V, ci, i+2):
        E.note(3, n - 12, breathing_vel(36, i, 6, 4), bt(b+i), BAR3 - 25,
               time_amount=15, vel_amount=5)

# v3 bridge melody: E6 (highest note of the song) appears on the F chord
# The melody reaching its peak on the "wrongest" chord is devastating
br = [
    # Am: start low, yearning
    [(N('E',5),QUARTER),(N('G',5),QUARTER+EIGHTH),(N('A',5),EIGHTH),
     (N('B',5),HALF),(N('A',5),QUARTER)],
    # Em: settle
    [(N('G',5),DOTTED_HALF),
     (N('E',5),DOTTED_HALF)],
    # F MAJOR: the peak — E6 on the wrongest chord. Devastating.
    [(N('C',6),QUARTER),(N('E',6),HALF),          # E6 arrives HERE, on F major
     (N('E',6),DOTTED_HALF)],                      # Hold it — let it ring against F
    # C: coming down from the peak
    [(N('D',6),DOTTED_HALF),
     (N('C',6),DOTTED_HALF)],
    # D: resolution attempt
    [(N('B',5),HALF+EIGHTH),(N('A',5),EIGHTH),
     (N('A',5),QUARTER),(N('G',5),HALF)],
    # Am-Em: final bridge phrases, winding down
    [(N('E',5),DOTTED_HALF),
     (N('G',5),DOTTED_HALF)],
]
for pi, phrase in enumerate(br):
    voice(bt(b + pi*2), phrase, vel=50, bar_num=pi+56)

# Pedal steel — bridge counter-melody
pedal_steel(bt(b), [(n, d) for n, d in zip(
    [N('A',5),N('B',5),N('G',5),N('E',5),N('E',5),N('G',5),
     N('A',5),N('B',5),N('D',6),N('B',5),N('A',5),N('G',5)],
    [DOTTED_HALF]*12)], vel=40, bar_num=56)

b = 68

# === FINAL CHORUS (10 bars) — 8 normal + 2 bars E MAJOR surprise ===
# v3: Strings enter for ALL 10 bars (not just last 4). They swell through E major.

waltz_drums(bt(b), 'crash', bar_num=68)

# --- First 8 bars: normal Em-C-G-D chorus ---
for i in range(8):
    ci = (i // 2) % 4
    nci = ((i+2) // 2) % 4
    fingerpick(bt(b+i), gv(CHORUS_V, ci, i+16), vel=53, bar_num=i+68)
    waltz_bass(bt(b+i), CHORUS_BASS[ci], vel=50, bar_num=i+40, next_root=CHORUS_BASS[nci])
    waltz_drums(bt(b+i), 'chorus', bar_num=i+68)
    piano_waltz(bt(b+i), gv(CHORUS_V, ci, i+6), vel=48, bar_num=i+68)
    if i % 2 == 0:
        pad_swell(bt(b+i), gv(CHORUS_V, ci, i+7), vel=40, bars=2, bar_num=i+40)
    if i % 4 == 0:
        organ(bt(b+i), gv(CHORUS_V, ci, i+5), vel=30, bars=4, bar_num=i+40)

# v3: Strings enter here — all 10 bars of the final chorus, crescendo through E major
# Start with the Em chord voicing, will re-voice for E major bars below
strings_crescendo(bt(b), gv(CHORUS_V, 0, 0), vel_start=20, vel_end=55, bars=10, bar_num=68)

# Vocal for first 8 bars (normal chorus melody)
for pi, phrase in enumerate(ch_mel):
    voice(bt(b + pi*2), phrase, vel=60, bar_num=pi+68)

# Pedal steel counter for normal chorus bars
pedal_steel(bt(b), [(n, d) for n, d in zip(
    [N('G',5),N('F#',5),N('E',5),N('D',5),N('E',5),N('G',5),N('F#',5),N('D',5)],
    [DOTTED_HALF]*8)], vel=38, bar_num=68)

# --- THE E MAJOR SURPRISE: bars 8-9 of the final chorus (2 extra bars) ---
# E major (E-G#-B) — the parallel major of Em. The "last signal" arrives.
e_bar = b + 8  # bar 76 absolute

# E major in the piano — the surprise chord
E.cc(0, 64, 110, h_time(bt(e_bar), 3))
for n in E_MAJOR_CHORD:
    E.note(0, n, 55, bt(e_bar), BAR3 * 2 - 30, time_amount=8, vel_amount=4)
E.cc(0, 64, 0, h_time(bt(e_bar + 2) - 30, 3))

# E major in the guitar — gentle arpeggio
for beat in range(3):
    E.note(3, E_MAJOR_CHORD[beat % 3] - 12, 42 + accent_beat(beat, 'waltz'),
           bt(e_bar) + beat * QUARTER, QUARTER - 15, time_amount=8, vel_amount=3)
# Second bar: let it ring
E.note(3, E_MAJOR_CHORD[0] - 12, 38, bt(e_bar + 1), DOTTED_HALF - 30,
       time_amount=10, vel_amount=3)

# Bass: E — low, grounding
waltz_bass(bt(e_bar), E_MAJOR_BASS, vel=48, bar_num=76)
waltz_bass(bt(e_bar + 1), E_MAJOR_BASS, vel=44, bar_num=77)

# Drums: gentle crash into sustained ride
waltz_drums(bt(e_bar), 'crash', bar_num=76)
waltz_drums(bt(e_bar + 1), 'chorus', bar_num=77)

# Pad swell on E major
pad_swell(bt(e_bar), E_MAJOR_CHORD, vel=42, bars=2, bar_num=76)

# Organ on E major
organ(bt(e_bar), E_MAJOR_CHORD, vel=32, bars=2, bar_num=76)

# v3: PEDAL STEEL plays G# — THE note that changes.
# All song long it's been G natural. Now it's G#. This half-step is the whole ending.
pedal_steel_sustained(bt(e_bar), N('G#',5), BAR3 * 2, vel=48, bar_num=76)

# v3: VOCAL sustains B5 over E major — the 5th. "Maybe it's going to be okay."
E.note(8, N('B',5), 58, bt(e_bar), BAR3 * 2 - 40, time_amount=6, vel_amount=4)

# Additional strings voicing for the E major bars specifically (E-G#-B an octave up)
for n in [N('E',5), N('G#',5), N('B',5)]:
    E.note(7, n + 12, 45, bt(e_bar), BAR3 * 2 - 30, time_amount=10, vel_amount=5)

b = 78  # 68 + 10

# === OUTRO (8 bars) ===
# v3: organ slowly drifts out of tune (wobble ±60 → ±200 cents)
for i in range(8):
    ci = (i // 2) % 4
    fade = max(20, 46 - i * 4)
    fingerpick(bt(b+i), gv(VERSE_V, ci, i+78), vel=fade, bar_num=i+78)
    if i < 6:
        waltz_bass(bt(b+i), VERSE_BASS[ci], vel=max(23, 38-i*4), bar_num=i+48)
    if i < 4:
        waltz_drums(bt(b+i), 'brush', bar_num=i+78)
    if i < 6 and i % 2 == 0:
        pad_swell(bt(b+i), gv(VERSE_V, ci, i+10), vel=max(16, 28-i*3), bars=2, bar_num=i+48)

# v3: Organ with fading signal — pitch wobble drifts from ±60 to ±200 cents
organ_fading(bt(b), gv(VERSE_V, 0, 0), vel=24, bars=8, bar_num=78)

# Pedal steel final bend
pedal_steel(bt(b+4), [(N('D',5), DOTTED_HALF*4)], vel=33, bar_num=82)

# Final piano chord — G add9
E.cc(0, 64, 110, h_time(bt(b+5), 3))
for n in make_chord(N('G',4), 'add9'):
    E.note(0, n, 26, bt(b+5), BAR3 * 2 - 30, time_amount=12, vel_amount=4)
E.cc(0, 64, 0, h_time(bt(b+7) - 30, 3))

# v3: THE LAST SOUND — a single fingerpicked G, completely alone. The tonic. Home.
# Everything else has faded. Just this one note.
last_bar = b + 7
E.note_raw(3, N('G',4), 40, bt(last_bar) + HALF, DOTTED_HALF)


# ============================================================
# OUTPUT
# ============================================================

build_midi(E, 'Last Signal Home', bpm=58, time_sig_num=3, total_bars=86,
           channel_names={
               0: 'Piano', 1: 'Synth Pad', 2: 'Pedal Steel Synth', 3: 'Clean Guitar',
               4: 'Distorted Guitar', 5: 'Organ', 6: 'Bass', 7: 'Strings',
               8: 'Vocal Melody', 9: 'Drums',
           },
           output_path='/home/user/music/compositions/v3/04_last_signal_home.mid')
