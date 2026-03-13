#!/usr/bin/env python3
"""
Song 3 v3: "Beautiful Machines"
Key: Eb major | Tempo: 84 BPM | 4/4 | ~124 bars

v3 handcrafted changes — musical, not just technical:

STRUCTURE: Solo Piano Intro (16) → Verse 1 (16) → Verse 2 (16) → Chorus 1 (12)
           → Verse 3 (16) → Chorus 2 + Guitar Wall (12) → 2 bars near-silence
           → Instrumental Crescendo (16) → Decay/Outro (16) = 122 bars

HARMONIC:
- Chorus: Fm-Db-Ab-Eb (Db borrowed from Eb minor adds gravity)
- Crescendo bars 9-12: Cb major (enharmonic B, from Eb minor — startling)
- Crescendo bar 14-15: Eb sus4 → Eb resolution

MELODY:
- Verse 1 opens on Bb4 (the 5th) — conversational, intimate
- Chorus 1 peaks at C6; Chorus 2 peaks at Eb6 (gives it somewhere to go)
- Single sustained Bb5 vocal note in the 2-bar silence

ARRANGEMENT:
- Intro bar 8: "wrong" Db in Bb arpeggio (passing tone hint), bar 9 corrects
- 2 bars near-silence: piano holds Eb with pedal, barely-there pad, everything stops
- Crescendo lead: NEW rising-4th motif (Bb→Eb) — "victory theme" not heard before
- Decay: last sound is solo Eb4 piano note ringing 8 bars with sustain pedal

COUNTER-MELODY:
- Verse 3: synth lead plays simplified chorus melody haunting the verse
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from humanize import *

E = EventList()

def bt(bar_num):
    return bar_num * BAR4


# ============================================================
# CHORD VOICINGS
# ============================================================

# Verse: Eb - Cm - Ab - Bb (unchanged foundation)
VERSE_V = [
    [make_chord(N('Eb',4),'major'), make_chord(N('Eb',4),'add9'), make_chord(N('Eb',4),'sus2')],
    [make_chord(N('C',4),'minor'), make_chord(N('C',4),'min7'), [N('C',4),N('Eb',4),N('G',4)]],
    [make_chord(N('Ab',3),'major'), make_chord(N('Ab',3),'add9'), [N('Ab',3),N('C',4),N('Eb',4)]],
    [make_chord(N('Bb',3),'major'), make_chord(N('Bb',3),'sus4'), [N('Bb',3),N('D',4),N('F',4)]],
]
VERSE_BASS = [N('Eb',2), N('C',2), N('Ab',1), N('Bb',1)]

# Chorus: Fm - Db - Ab - Eb  (Db replaces Cm — borrowed from Eb minor)
CHORUS_V = [
    [make_chord(N('F',4),'minor'), make_chord(N('F',4),'min7')],
    [make_chord(N('Db',4),'major'), make_chord(N('Db',4),'add9')],
    [make_chord(N('Ab',3),'major'), make_chord(N('Ab',3),'add9')],
    [make_chord(N('Eb',4),'major'), make_chord(N('Eb',4),'add9')],
]
CHORUS_BASS = [N('F',2), N('Db',2), N('Ab',1), N('Eb',2)]

# Crescendo: Ab - Eb - Bb - Cm for bars 1-8, then Cb in bars 9-12
CRESC_V = [
    [make_chord(N('Ab',3),'major'), [N('Ab',3),N('C',4),N('Eb',4)]],
    [make_chord(N('Eb',4),'major'), make_chord(N('Eb',4),'add9')],
    [make_chord(N('Bb',3),'major'), make_chord(N('Bb',3),'sus4')],
    [make_chord(N('C',4),'minor'), make_chord(N('C',4),'min7')],
]
CRESC_BASS = [N('Ab',1), N('Eb',2), N('Bb',1), N('C',2)]

# Cb major — the startling borrowed chord from Eb minor
CB_CHORD = [make_chord(N('B',3),'major'), [N('B',3),N('Eb',4),N('Gb',4)]]  # Cb = B enharmonically
CB_BASS = N('B',1)  # Cb = B enharmonically

# Eb sus4 for the peak resolution
EBSUS4_CHORD = make_chord(N('Eb',4),'sus4')
EB_CHORD = make_chord(N('Eb',4),'major')

def gv(voicings, ci, bar):
    opts = voicings[ci]
    return opts[bar % len(opts)]


# ============================================================
# INSTRUMENT FUNCTIONS
# ============================================================

def piano_arp(bar_start, chord_notes, vel=50, bar_num=0, wrong_note=None):
    """Piano arpeggio. wrong_note: tuple (index, pitch) to substitute one note."""
    notes = list(chord_notes) + [chord_notes[0] + 12]
    if wrong_note:
        idx, pitch = wrong_note
        if idx < len(notes):
            notes[idx] = pitch
    patterns = [
        [0,1,2,3,2,1,0,3], [0,2,1,3,0,2,3,1], [3,2,1,0,1,2,3,2],
        [0,1,0,2,1,2,3,2], [0,3,1,2,0,3,2,1], [0,1,2,1,0,2,3,2],
    ]
    pat = patterns[bar_num % len(patterns)]
    bvel = breathing_vel(vel, bar_num, 8, 5)
    E.cc(0, 64, 100, h_time(bar_start, 3))
    for i in range(8):
        idx = pat[i] % len(notes)
        note = notes[idx]
        t = bar_start + i * EIGHTH + swing_offset(i, 10)
        v = bvel + accent_beat(i // 2) + (0 if i % 2 == 0 else -6)
        if i == 0 and bar_num % 5 == 3:
            E.note(0, note - 2, v - 15, t - SIXTEENTH, SIXTEENTH - 5, time_amount=5)
        E.note(0, note, v, t, EIGHTH - random.randint(15, 30), time_amount=6, vel_amount=3)
    E.cc(0, 64, 0, h_time(bar_start + BAR4 - 30, 3))


def piano_whole(bar_start, chord_notes, vel=42):
    E.cc(0, 64, 110, h_time(bar_start, 3))
    for n in chord_notes:
        E.note(0, n, vel, bar_start, BAR4 - 30, time_amount=12, vel_amount=5)
    E.cc(0, 64, 0, h_time(bar_start + BAR4 - 30, 3))


def piano_sustain(bar_start, note, vel=30, bars=1):
    """Single piano note held with sustain pedal — for silence/decay moments."""
    E.cc(0, 64, 120, h_time(bar_start, 3))
    E.note(0, note, vel, bar_start, BAR4 * bars - 30, time_amount=15, vel_amount=3)
    E.cc(0, 64, 0, h_time(bar_start + BAR4 * bars - 30, 3))


def pad_swell(bar_start, chord_notes, vel=38, bars=2, bar_num=0):
    steps = bars * 4
    for step in range(steps):
        t = bar_start + step * QUARTER
        swell = math.sin((step / steps) * math.pi)
        v = int(vel * 0.7 + vel * 0.3 * swell)
        E.cc(1, 11, max(40, min(127, int(v * 2.5))), h_time(t, 5))
    bvel = breathing_vel(vel, bar_num, 6, 4)
    for n in chord_notes:
        E.note(1, n, bvel, bar_start, BAR4 * bars - 30, time_amount=10, vel_amount=4)


def synth_arp(bar_start, chord_notes, vel=35, bar_num=0):
    notes = list(chord_notes) + [chord_notes[0] + 12]
    patterns = [
        lambda i, n: n[i % len(n)],
        lambda i, n: n[([0,1,2,3,2,1,0,1,2,3,2,1,0,1,2,3][i]) % len(n)],
        lambda i, n: n[([0,2,1,3,0,2,3,1,0,2,1,3,0,2,3,1][i]) % len(n)],
        lambda i, n: n[([3,1,2,0,3,1,0,2,3,1,2,0,3,2,1,0][i]) % len(n)],
        lambda i, n: n[([0,1,0,2,0,3,0,2,0,1,0,3,0,2,0,1][i]) % len(n)],
    ]
    get = patterns[bar_num % len(patterns)]
    bvel = breathing_vel(vel, bar_num, 6, 4)
    for i in range(16):
        note = get(i, notes)
        t = bar_start + i * SIXTEENTH
        v = bvel + (3 if i % 4 == 0 else -2) + random.randint(-2, 2)
        E.note(2, note, v, t, SIXTEENTH - random.randint(8, 15), time_amount=5, vel_amount=3)


def organ_drone(bar_start, chord_notes, vel=32, bars=4, bar_num=0):
    bvel = breathing_vel(vel, bar_num, 6, 3)
    for n in chord_notes:
        E.note(5, n, bvel, bar_start, BAR4 * bars - 30, time_amount=12, vel_amount=4)
    for step in range(bars * 8):
        t = bar_start + step * EIGHTH
        bend = int(70 * math.sin(step * 0.25))
        E.pitch_bend(5, bend, h_time(t, 3))
    E.pitch_bend(5, 0, bar_start + BAR4 * bars)


def clean_guitar(bar_start, chord_notes, vel=42, bar_num=0):
    bvel = breathing_vel(vel, bar_num, 8, 5)
    for n in [nn - 12 for nn in chord_notes]:
        v1 = bvel + random.randint(-3, 3)
        v2 = bvel - 5 + random.randint(-3, 3)
        E.note(3, n, v1, bar_start, HALF - random.randint(15, 25), time_amount=8, vel_amount=4)
        E.note(3, n, v2, bar_start + HALF, HALF - random.randint(15, 25), time_amount=10, vel_amount=4)


def dist_guitar(bar_start, root, vel=65, pattern='sustained', bar_num=0):
    pc = make_chord(root + 24, 'power')
    bvel = breathing_vel(vel, bar_num, 4, 5)
    if pattern == 'sustained':
        for n in pc:
            E.note(4, n, bvel + random.randint(-3, 3), bar_start, BAR4 - 25,
                   time_amount=8, vel_amount=5)
    elif pattern == 'wall':
        for n in pc:
            E.note(4, n, bvel + random.randint(-3, 3), bar_start, BAR4 - 15,
                   time_amount=6, vel_amount=5)
        E.note(4, root + 36, bvel - 8, bar_start, BAR4 - 15, time_amount=8, vel_amount=5)
    elif pattern == 'chug':
        for i in range(4):
            v = bvel + accent_beat(i) + random.randint(-4, 4)
            for n in pc:
                E.note(4, n, v, bar_start + i * QUARTER, QUARTER - random.randint(20, 35),
                       time_amount=6, vel_amount=4)


def bass_line(bar_start, root, vel=48, pattern='whole', bar_num=0, next_root=None):
    bvel = breathing_vel(vel, bar_num, 8, 4)
    if pattern == 'whole':
        E.note(6, root, bvel, bar_start, BAR4 - 30, time_amount=10, vel_amount=4)
        if next_root and bar_num % 3 == 2:
            approach = next_root - 1 if next_root > root else next_root + 1
            E.note(6, approach, bvel - 8, bar_start + HALF + QUARTER, QUARTER - 20,
                   time_amount=8, vel_amount=3)
    elif pattern == 'half':
        E.note(6, root, bvel, bar_start, HALF - 25, time_amount=8, vel_amount=4)
        E.note(6, root + 7, bvel - 5, bar_start + HALF, HALF - 25, time_amount=10, vel_amount=3)
    elif pattern == 'walking':
        steps = [root, root + 5, root + 7, root + 5]
        if bar_num % 3 == 1:
            steps = [root, root + 3, root + 7, root + 5]
        for j, n in enumerate(steps):
            v = bvel + accent_beat(j) + random.randint(-3, 3)
            E.note(6, n, v, bar_start + j * QUARTER, QUARTER - random.randint(15, 25),
                   time_amount=8, vel_amount=3)


def strings_swell(bar_start, chord_notes, vel=32, bars=4, bar_num=0):
    """Strings with expression swell."""
    steps = bars * 8
    for step in range(steps):
        t = bar_start + step * EIGHTH
        phase = step / steps
        swell = math.sin(phase * math.pi) ** 0.8
        v = max(30, min(120, int(40 + 80 * swell)))
        E.cc(7, 11, v, h_time(t, 3))
    bvel = breathing_vel(vel, bar_num, 8, 5)
    for n in [nn + 12 for nn in chord_notes]:
        E.note(7, n, bvel, bar_start, BAR4 * bars - 30, time_amount=12, vel_amount=5)


def drums(bar_start, pattern='sparse', bar_num=0):
    ch = 9
    kick, snare, hh_c, hh_o, ride, crash, rim = 36, 38, 42, 46, 51, 49, 37
    bvel = breathing_vel(48, bar_num, 8, 4)

    if pattern == 'sparse':
        E.note(ch, kick, bvel - 5, bar_start, QUARTER, time_amount=6, vel_amount=4)
        if bar_num % 2 == 0:
            E.note(ch, hh_c, 18 + random.randint(-3, 3), bar_start + QUARTER, EIGHTH, time_amount=10)
        E.note(ch, hh_c, 18 + random.randint(-3, 3), bar_start + HALF + QUARTER, EIGHTH, time_amount=10)
        if bar_num % 3 == 2:
            E.note(ch, rim, 15, bar_start + HALF, QUARTER, time_amount=12)

    elif pattern == 'verse':
        E.note(ch, kick, bvel, bar_start, QUARTER, time_amount=5, vel_amount=5)
        E.note(ch, snare, h_vel(30, 4), bar_start + QUARTER, QUARTER, time_amount=8, vel_amount=5)
        E.note(ch, kick, bvel - 5, bar_start + HALF, QUARTER, time_amount=6, vel_amount=5)
        E.note(ch, snare, h_vel(30, 4), bar_start + HALF + QUARTER, QUARTER, time_amount=8, vel_amount=5)
        for i in range(8):
            v = 20 + (4 if i % 2 == 0 else 0) + random.randint(-3, 3)
            E.note(ch, hh_c, v, bar_start + i * EIGHTH + swing_offset(i, 8), EIGHTH, time_amount=6)
        if bar_num % 2 == 0:
            E.note(ch, snare, 12, bar_start + EIGHTH + swing_offset(1, 8), EIGHTH, time_amount=12)

    elif pattern == 'chorus':
        E.note(ch, kick, bvel + 8, bar_start, QUARTER, time_amount=4, vel_amount=5)
        E.note(ch, snare, h_vel(42, 5), bar_start + QUARTER, QUARTER, time_amount=6, vel_amount=5)
        E.note(ch, kick, bvel + 3, bar_start + HALF, QUARTER, time_amount=5, vel_amount=5)
        E.note(ch, snare, h_vel(42, 5), bar_start + HALF + QUARTER, QUARTER, time_amount=6, vel_amount=5)
        for i in range(8):
            v = 28 + (4 if i % 2 == 0 else 0) + random.randint(-3, 3)
            E.note(ch, ride, v, bar_start + i * EIGHTH + swing_offset(i, 6), EIGHTH, time_amount=5)
        if bar_num % 2 == 1:
            E.note(ch, kick, bvel - 15, bar_start + QUARTER + EIGHTH, EIGHTH, time_amount=10)

    elif pattern == 'building':
        E.note(ch, kick, bvel + 12, bar_start, QUARTER, time_amount=4, vel_amount=5)
        E.note(ch, kick, bvel, bar_start + EIGHTH, EIGHTH, time_amount=8, vel_amount=4)
        E.note(ch, snare, h_vel(50, 5), bar_start + QUARTER, QUARTER, time_amount=5, vel_amount=5)
        E.note(ch, kick, bvel + 8, bar_start + HALF, QUARTER, time_amount=4, vel_amount=5)
        E.note(ch, snare, h_vel(50, 5), bar_start + HALF + QUARTER, QUARTER, time_amount=5, vel_amount=5)
        for i in range(16):
            v = 25 + (5 if i % 4 == 0 else 0) + random.randint(-3, 3)
            E.note(ch, hh_c, v, bar_start + i * SIXTEENTH, SIXTEENTH, time_amount=4)

    elif pattern == 'crash':
        E.note(ch, crash, 68, bar_start, QUARTER, time_amount=3)
        E.note(ch, kick, 68, bar_start, QUARTER, time_amount=3)

    elif pattern == 'fill':
        E.note(ch, kick, bvel + 10, bar_start, QUARTER, time_amount=4)
        for j, v in enumerate([35, 40, 45, 50, 55]):
            E.note(ch, snare, v, bar_start + QUARTER + j * EIGHTH // 1 + j * (EIGHTH + SIXTEENTH) // 2,
                   EIGHTH, time_amount=6)
        E.note(ch, crash, 65, bar_start + HALF + QUARTER, QUARTER, time_amount=4)


def voice(bar_start, phrase, vel=52, bar_num=0):
    t = bar_start
    prev = None
    for i, (note, dur) in enumerate(phrase):
        if note is not None:
            v = vel
            if prev and note > prev + 3: v += 5
            elif prev and note < prev - 3: v -= 2
            v = breathing_vel(v, bar_num + i, 6, 5)
            antic = -SIXTEENTH if random.random() < 0.12 and i > 0 else 0
            if prev and abs(note - prev) >= 4 and random.random() < 0.25:
                grace = prev + (1 if note > prev else -1)
                E.note(8, grace, v - 14, t + antic - SIXTEENTH, SIXTEENTH - 5, time_amount=10)
            E.note(8, note, v, t + antic, dur - random.randint(20, 40), time_amount=10, vel_amount=5)
            prev = note
        t += dur


# ============================================================
# BUILD THE SONG
# ============================================================

b = 0

# === SOLO PIANO INTRO (16 bars) ===
for i in range(16):
    ci = (i // 2) % 4
    vel = 33 + i  # gentle crescendo across the intro

    if i == 7:
        # Bar 8: the "wrong" note — Db instead of D natural in the Bb chord arpeggio
        # This passing tone hints at the darker Db harmony coming in the chorus
        bb_chord = gv(VERSE_V, 3, i)  # Bb major voicing
        # Find the D natural and replace with Db
        piano_arp(bt(i), bb_chord, vel=vel, bar_num=i,
                  wrong_note=(1, N('Db',4)))  # Db where D should be
    elif i == 8:
        # Bar 9: corrects itself — normal Eb chord, the listener relaxes
        piano_arp(bt(i), gv(VERSE_V, ci, i), vel=vel, bar_num=i)
    else:
        piano_arp(bt(i), gv(VERSE_V, ci, i), vel=vel, bar_num=i)

b = 16

# === VERSE 1: piano + bass + pad (16 bars) ===
# Melody starts on Bb4 (the 5th) — lower, conversational register
for i in range(16):
    ci = (i // 2) % 4
    nci = ((i+1) // 2) % 4
    piano_arp(bt(b+i), gv(VERSE_V, ci, i), vel=46, bar_num=i+16)
    if i >= 4:
        bass_line(bt(b+i), VERSE_BASS[ci], vel=38, pattern='whole', bar_num=i, next_root=VERSE_BASS[nci])
    if i >= 4 and i % 4 == 0:
        pad_swell(bt(b+i), gv(VERSE_V, ci, i+1), vel=26+i, bars=4, bar_num=i)

# Verse 1 melody — starts on Bb4 (the 5th), not Eb5
v1_mel = [
    [(N('Bb',4),HALF),(N('C',5),QUARTER+EIGHTH),(N('Eb',5),EIGHTH+HALF),(None,BAR4),
     (N('F',5),HALF),(N('Eb',5),QUARTER+EIGHTH),(N('D',5),EIGHTH+HALF),(None,HALF)],
    [(N('Bb',4),QUARTER),(N('C',5),QUARTER),(N('Eb',5),HALF+EIGHTH),(N('G',5),EIGHTH+QUARTER),(None,QUARTER),
     (N('F',5),QUARTER),(N('Eb',5),HALF+EIGHTH),(N('D',5),EIGHTH),(N('Bb',4),HALF+QUARTER),(None,QUARTER)],
    [(N('Eb',5),HALF),(N('F',5),HALF+EIGHTH),(N('G',5),EIGHTH+QUARTER),(None,QUARTER),
     (N('F',5),QUARTER),(N('Eb',5),QUARTER+EIGHTH),(N('D',5),EIGHTH),(N('Bb',4),HALF+QUARTER),(None,QUARTER)],
    [(N('C',5),QUARTER),(N('Eb',5),QUARTER),(N('F',5),HALF+QUARTER),(None,QUARTER+HALF),
     (N('Eb',5),QUARTER),(N('D',5),HALF+EIGHTH),(N('Bb',4),EIGHTH),(N('Bb',4),HALF+QUARTER),(None,QUARTER)],
]
for pi, phrase in enumerate(v1_mel):
    voice(bt(b + pi*4), phrase, vel=43, bar_num=pi+16)

b = 32

# === VERSE 2: + drums + synth arp (16 bars) ===
for i in range(16):
    ci = (i//2) % 4
    nci = ((i+1)//2) % 4
    piano_arp(bt(b+i), gv(VERSE_V, ci, i+16), vel=48, bar_num=i+32)
    bass_line(bt(b+i), VERSE_BASS[ci], vel=42, pattern='half', bar_num=i+16, next_root=VERSE_BASS[nci])
    if i % 2 == 0:
        pad_swell(bt(b+i), gv(VERSE_V, ci, i+3), vel=33, bars=2, bar_num=i+16)
    if i < 8:
        drums(bt(b+i), 'sparse', bar_num=i+32)
    elif i == 15:
        drums(bt(b+i), 'fill', bar_num=i+32)
    else:
        drums(bt(b+i), 'verse', bar_num=i+32)
    if i >= 8:
        synth_arp(bt(b+i), gv(VERSE_V, ci, i+5), vel=26, bar_num=i+32)

v2_mel = [
    [(N('G',5),QUARTER),(N('Ab',5),QUARTER),(N('Bb',5),HALF+EIGHTH),(N('C',6),EIGHTH+QUARTER),(None,QUARTER),
     (N('Bb',5),QUARTER),(N('Ab',5),HALF+EIGHTH),(N('G',5),EIGHTH),(N('F',5),HALF+QUARTER),(None,QUARTER)],
    [(N('Eb',5),QUARTER),(N('G',5),QUARTER),(N('Bb',5),HALF+EIGHTH),(N('Ab',5),EIGHTH+QUARTER),(None,QUARTER),
     (N('G',5),QUARTER),(N('F',5),QUARTER+EIGHTH),(N('Eb',5),EIGHTH),(N('F',5),HALF+QUARTER),(None,QUARTER)],
    [(N('Ab',5),HALF),(N('Bb',5),HALF+EIGHTH),(N('C',6),EIGHTH+QUARTER),(None,QUARTER),
     (N('Bb',5),QUARTER),(N('Ab',5),QUARTER+EIGHTH),(N('G',5),EIGHTH),(N('F',5),HALF+QUARTER),(None,QUARTER)],
    [(N('G',5),QUARTER),(N('Ab',5),QUARTER),(N('Bb',5),HALF+QUARTER),(None,QUARTER+HALF),
     (N('Ab',5),QUARTER),(N('G',5),HALF+EIGHTH),(N('F',5),EIGHTH),(N('Eb',5),HALF+QUARTER),(None,QUARTER)],
]
for pi, phrase in enumerate(v2_mel):
    voice(bt(b + pi*4), phrase, vel=48, bar_num=pi+32)

b = 48

# === CHORUS 1: full band (12 bars) ===
# Chorus now uses Fm-Db-Ab-Eb. Peaks at C6 (saving Eb6 for chorus 2).
drums(bt(b), 'crash', bar_num=48)
for i in range(12):
    ci = (i//2) % 4
    nci = ((i+2)//2) % 4
    piano_arp(bt(b+i), gv(CHORUS_V, ci, i), vel=53, bar_num=i+48)
    bass_line(bt(b+i), CHORUS_BASS[ci], vel=50, pattern='half', bar_num=i+24, next_root=CHORUS_BASS[nci])
    synth_arp(bt(b+i), gv(CHORUS_V, ci, i+2), vel=33, bar_num=i+48)
    drums(bt(b+i), 'chorus', bar_num=i+48)
    clean_guitar(bt(b+i), gv(CHORUS_V, ci, i), vel=40, bar_num=i+48)
    if i % 4 == 0:
        pad_swell(bt(b+i), gv(CHORUS_V, ci, i+1), vel=40, bars=4, bar_num=i+24)

# Chorus 1 melody — peaks at C6, NOT Eb6
ch1_mel = [
    [(N('Bb',5),HALF),(N('C',6),HALF+EIGHTH),(N('Db',6),EIGHTH+QUARTER),(N('C',6),HALF),
     (N('Ab',5),QUARTER),(N('Bb',5),HALF+EIGHTH),(N('C',6),EIGHTH),(N('Bb',5),HALF+QUARTER),(None,QUARTER)],
    [(N('C',6),HALF),(N('Bb',5),QUARTER+EIGHTH),(N('Ab',5),EIGHTH),(N('G',5),HALF),(None,HALF),
     (N('Ab',5),QUARTER),(N('G',5),HALF+EIGHTH),(N('F',5),EIGHTH),(N('Eb',5),HALF+QUARTER),(None,QUARTER)],
    [(N('F',5),QUARTER),(N('G',5),QUARTER),(N('Ab',5),HALF+EIGHTH),(N('Bb',5),EIGHTH+QUARTER),
     (N('Ab',5),QUARTER),(N('G',5),HALF+EIGHTH),(N('Eb',5),EIGHTH+WHOLE)],
]
for pi, phrase in enumerate(ch1_mel):
    voice(bt(b + pi*4), phrase, vel=56, bar_num=pi+48)

b = 60

# === VERSE 3: + organ + counter-melody (16 bars) ===
for i in range(16):
    ci = (i//2) % 4
    nci = ((i+1)//2) % 4
    piano_arp(bt(b+i), gv(VERSE_V, ci, i+32), vel=50, bar_num=i+60)
    bass_line(bt(b+i), VERSE_BASS[ci], vel=46, pattern='walking', bar_num=i+32, next_root=VERSE_BASS[nci])
    synth_arp(bt(b+i), gv(VERSE_V, ci, i+7), vel=30, bar_num=i+60)
    drums(bt(b+i), 'verse', bar_num=i+60)
    clean_guitar(bt(b+i), gv(VERSE_V, ci, i+4), vel=38, bar_num=i+60)
    if i % 4 == 0:
        organ_drone(bt(b+i), gv(VERSE_V, ci, i+2), vel=28, bars=4, bar_num=i+30)
        pad_swell(bt(b+i), gv(VERSE_V, ci, i+5), vel=36, bars=4, bar_num=i+30)

v3_mel = [
    [(N('Eb',5),HALF),(N('G',5),HALF+EIGHTH),(N('Ab',5),EIGHTH+QUARTER),(N('Bb',5),HALF),
     (N('C',6),HALF),(N('Bb',5),HALF+EIGHTH),(N('Ab',5),EIGHTH+QUARTER),(None,QUARTER)],
    [(N('G',5),QUARTER),(N('Ab',5),QUARTER),(N('Bb',5),HALF),(None,BAR4),
     (N('Ab',5),QUARTER),(N('G',5),QUARTER+EIGHTH),(N('F',5),EIGHTH),(N('Eb',5),HALF+QUARTER),(None,QUARTER)],
    [(N('Bb',5),HALF),(N('C',6),HALF+EIGHTH),(N('Db',6),EIGHTH),(N('C',6),HALF+QUARTER),
     (N('Bb',5),QUARTER),(N('Ab',5),HALF+EIGHTH),(N('G',5),EIGHTH),(N('Eb',5),HALF+QUARTER),(None,QUARTER)],
    [(N('G',5),QUARTER),(N('F',5),QUARTER),(N('Eb',5),HALF+QUARTER),(None,QUARTER+HALF),
     (N('F',5),QUARTER),(N('Eb',5),HALF+EIGHTH),(N('Eb',5),EIGHTH+WHOLE)],
]
for pi, phrase in enumerate(v3_mel):
    voice(bt(b + pi*4), phrase, vel=53, bar_num=pi+60)

# Counter-melody on synth lead: simplified chorus melody haunting the verse
# Uses the Db from the chorus harmony — it bleeds through, ghost-like
counter = [
    [(N('Bb',5),WHOLE),(None,BAR4),(N('C',6),HALF),(N('Db',6),HALF),(N('C',6),WHOLE)],
    [(None,BAR4*2),(N('Eb',6),HALF),(N('Db',6),HALF),(N('C',6),WHOLE)],
]
for pi, phrase in enumerate(counter):
    t = bt(b + pi*8)
    for note, dur in phrase:
        if note is not None:
            v = breathing_vel(36, pi, 4, 5)
            E.note(2, note, v, t, dur - 30, time_amount=10, vel_amount=4)
        t += dur

b = 76

# === CHORUS 2 + GUITAR WALL (12 bars) ===
# This chorus peaks at Eb6 — the high Eb the listener has been waiting for
drums(bt(b), 'crash', bar_num=76)
for i in range(12):
    ci = (i//2) % 4
    nci = ((i+2)//2) % 4
    piano_arp(bt(b+i), gv(CHORUS_V, ci, i+8), vel=56, bar_num=i+76)
    bass_line(bt(b+i), CHORUS_BASS[ci], vel=53, pattern='walking', bar_num=i+40, next_root=CHORUS_BASS[nci])
    synth_arp(bt(b+i), gv(CHORUS_V, ci, i+10), vel=36, bar_num=i+76)
    drums(bt(b+i), 'chorus', bar_num=i+76)
    dist_guitar(bt(b+i), CHORUS_BASS[ci], vel=58 + i, pattern='wall', bar_num=i+40)
    if i % 4 == 0:
        pad_swell(bt(b+i), gv(CHORUS_V, ci, i+3), vel=43, bars=4, bar_num=i+40)
        organ_drone(bt(b+i), gv(CHORUS_V, ci, i+6), vel=30, bars=4, bar_num=i+40)
    if i % 4 == 0:
        strings_swell(bt(b+i), gv(CHORUS_V, ci, i), vel=33, bars=4, bar_num=i+40)

# Chorus 2 melody — NOW peaks at Eb6 (the high Eb)
ch2_mel = [
    [(N('Bb',5),HALF),(N('C',6),HALF+EIGHTH),(N('Db',6),EIGHTH+QUARTER),(N('Eb',6),HALF),
     (N('Db',6),QUARTER),(N('C',6),HALF+EIGHTH),(N('Bb',5),EIGHTH),(N('Ab',5),HALF+QUARTER),(None,QUARTER)],
    [(N('C',6),HALF),(N('Bb',5),QUARTER+EIGHTH),(N('Ab',5),EIGHTH),(N('G',5),HALF),(None,HALF),
     (N('Ab',5),QUARTER),(N('Bb',5),HALF+EIGHTH),(N('Ab',5),EIGHTH),(N('G',5),HALF+QUARTER),(None,QUARTER)],
    [(N('F',5),QUARTER),(N('Ab',5),QUARTER),(N('Bb',5),HALF+EIGHTH),(N('C',6),EIGHTH+QUARTER),
     (N('Bb',5),QUARTER),(N('Ab',5),HALF+EIGHTH),(N('Eb',5),EIGHTH+WHOLE)],
]
for pi, phrase in enumerate(ch2_mel):
    voice(bt(b + pi*4), phrase, vel=63, bar_num=pi+76)

b = 88

# === 2 BARS OF NEAR-SILENCE (bars 88-89) ===
# Everything stops. Piano holds a single Eb with sustain pedal.
# Synth pad barely audible. A single vocal Bb5 hangs in space.
# This breath makes the crescendo hit harder.

# Piano: single Eb held with pedal
piano_sustain(bt(b), N('Eb',4), vel=28, bars=2)

# Barely-there pad — just a whisper of the Eb chord
E.cc(1, 11, 35, bt(b))
for n in make_chord(N('Eb',4),'major'):
    E.note(1, n, 14, bt(b), BAR4 * 2 - 30, time_amount=15, vel_amount=2)

# Vocal fragment: single sustained Bb5 hanging in space
E.note(8, N('Bb',5), 40, bt(b) + QUARTER, BAR4 * 2 - HALF, time_amount=12, vel_amount=4)

b = 90

# === INSTRUMENTAL CRESCENDO (16 bars) ===
# Bars 1-8: Ab-Eb-Bb-Cm as before
# Bars 9-12: Cb major (B major enharmonic) — startling, from outside the key
# Bars 13: Cm (return)
# Bar 14-15: Eb sus4 → Eb resolution at the absolute peak
# Bar 16: Eb resolution rings

drums(bt(b), 'crash', bar_num=90)

for i in range(16):
    # Determine chord for this bar
    if i < 8:
        # Normal crescendo chords
        ci = (i//2) % 4
        chord = gv(CRESC_V, ci, i)
        bass_root = CRESC_BASS[ci]
        nci = ((i+2)//2) % 4
        next_bass = CRESC_BASS[nci]
    elif i < 12:
        # Bars 9-12: Cb major — the startling chord from Eb minor
        chord = CB_CHORD[i % len(CB_CHORD)]
        bass_root = CB_BASS
        next_bass = N('C',2)
    elif i == 12:
        # Bar 13: Cm — crash back from Cb, "where are we?" resolves
        chord = make_chord(N('C',4),'minor')
        bass_root = N('C',2)
        next_bass = N('Eb',2)
    elif i == 13:
        # Bar 14: Eb sus4 — holds tension one beat longer at the absolute peak
        chord = EBSUS4_CHORD
        bass_root = N('Eb',2)
        next_bass = N('Eb',2)
    elif i == 14:
        # Bar 15: Eb major — the sus4 resolves, release
        chord = EB_CHORD
        bass_root = N('Eb',2)
        next_bass = N('Eb',2)
    else:
        # Bar 16: Eb rings out
        chord = EB_CHORD
        bass_root = N('Eb',2)
        next_bass = N('Eb',2)

    # Smooth intensity ramp
    intensity = i / 15.0
    pvel = int(53 + 25 * intensity)
    bvel = int(48 + 25 * intensity)
    svel = int(33 + 22 * intensity)
    dvel = int(55 + 35 * intensity)
    ovel = int(28 + 22 * intensity)

    piano_arp(bt(b+i), chord, vel=min(80, pvel), bar_num=i+90)
    bass_line(bt(b+i), bass_root, vel=min(75, bvel), pattern='walking', bar_num=i+48, next_root=next_bass)
    synth_arp(bt(b+i), chord, vel=min(55, svel), bar_num=i+90)
    drums(bt(b+i), 'building', bar_num=i+90)
    dist_guitar(bt(b+i), bass_root, vel=min(90, dvel), pattern='wall', bar_num=i+48)
    if i % 4 == 0:
        pad_swell(bt(b+i), chord, vel=min(58, int(38+20*intensity)), bars=4, bar_num=i+48)
        organ_drone(bt(b+i), chord, vel=min(50, ovel), bars=4, bar_num=i+48)
        strings_swell(bt(b+i), chord, vel=min(48, int(28+20*intensity)), bars=4, bar_num=i+48)

# Crescendo lead: NEW "victory theme" motif — rising 4th (Bb→Eb)
# This motif has NOT appeared anywhere else in the song until this moment.
# It repeats and builds, becoming the emotional climax.
cresc_lead = [
    # Bars 1-4: The motif emerges — simple rising 4th, tentative
    (N('Bb',5), HALF), (N('Eb',6), HALF), (None, WHOLE),
    (N('Bb',5), HALF), (N('Eb',6), WHOLE), (None, HALF),
    # Bars 5-8: Motif gains confidence, extends
    (N('Bb',5), QUARTER), (N('Eb',6), QUARTER), (N('F',6), HALF), (N('Eb',6), WHOLE),
    (N('Bb',5), HALF), (N('Eb',6), HALF), (N('F',6), HALF), (N('Eb',6), HALF),
    # Bars 9-12: Against the Cb chord — the motif becomes dissonant, searching
    (N('Bb',5), HALF), (N('Eb',6), WHOLE), (N('Db',6), HALF),
    (N('Bb',5), HALF), (N('Eb',6), HALF), (N('Db',6), HALF), (N('Cb',6), HALF),
    # Bars 13-14: Cm then sus4 — the motif finds its way back
    (N('C',6), HALF), (N('Eb',6), WHOLE), (N('F',6), HALF),
    # Bar 15-16: The sus4→major resolution, the motif soars to its peak
    (N('Eb',6), WHOLE), (N('Bb',5), HALF), (N('Eb',6), WHOLE + HALF),
]

t = bt(b)
prev = None
for note, dur in cresc_lead:
    if note is not None:
        v = 60
        if prev and note > prev: v += 5
        v = breathing_vel(v, 0, 4, 6)
        # Vibrato on sustained notes
        if dur >= WHOLE:
            for step in range(dur // SIXTEENTH):
                bend = int(300 * math.sin(step * 0.7))
                E.pitch_bend(2, bend, h_time(t + step * SIXTEENTH, 3))
            E.pitch_bend(2, 0, t + dur)
        E.note(2, note, v, t, dur - random.randint(15, 30), time_amount=8, vel_amount=5)
        prev = note
    t += dur

b = 106

# === DECAY/OUTRO (16 bars) — instruments drop one by one ===
# The crescendo's energy dissipates. Each instrument says goodbye separately.
for i in range(16):
    ci = (i//2) % 4
    nci = ((i+1)//2) % 4
    fade = max(20, 53 - i * 3)

    # Piano arpeggios fade and simplify (stop at bar 12 — only sustained notes after)
    if i < 12:
        piano_arp(bt(b+i), gv(VERSE_V, ci, i+50), vel=max(23, fade), bar_num=i+106)

    # Distorted guitar: first to go (4 bars)
    if i < 4:
        dist_guitar(bt(b+i), VERSE_BASS[ci], vel=max(28, 48-i*8), pattern='sustained', bar_num=i+56)

    # Drums thin out (6 bars)
    if i < 6:
        drums(bt(b+i), 'sparse' if i >= 3 else 'verse', bar_num=i+106)

    # Organ fades (8 bars)
    if i < 8 and i % 4 == 0:
        organ_drone(bt(b+i), gv(VERSE_V, ci, i+8), vel=max(18, 28-i*2), bars=4, bar_num=i+56)

    # Synth arp ghosts away (10 bars)
    if i < 10:
        synth_arp(bt(b+i), gv(VERSE_V, ci, i+10), vel=max(16, 28-i*2), bar_num=i+106)

    # Bass sustains, then goes (12 bars)
    if i < 12:
        bass_line(bt(b+i), VERSE_BASS[ci], vel=max(22, 38-i*3), pattern='whole', bar_num=i+56, next_root=VERSE_BASS[nci])

    # Pad breathes its last (14 bars)
    if i < 14 and i % 2 == 0:
        pad_swell(bt(b+i), gv(VERSE_V, ci, i+12), vel=max(14, 23-i), bars=2, bar_num=i+56)

# Bars 13-14: piano whole chords, getting quieter
for i in range(12, 14):
    piano_whole(bt(b+i), gv(VERSE_V, i%4, i+60), vel=max(18, 28-i))

# === THE LAST SOUND ===
# A single piano note — Eb4 — ringing for 8 bars with sustain pedal.
# No other instruments. The song fades into memory.
E.cc(0, 64, 127, bt(b + 14))  # sustain pedal fully down
E.note(0, N('Eb',4), 25, bt(b + 14), BAR4 * 8 - 30, time_amount=15, vel_amount=3)
# Don't release pedal — let it ring into infinity


# ============================================================
# OUTPUT
# ============================================================

build_midi(E, 'Beautiful Machines', bpm=84, total_bars=124,
           output_path='/home/user/music/compositions/v3/03_beautiful_machines.mid')
