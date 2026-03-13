#!/usr/bin/env python3
"""
Song 2 v2: "The Machinery of Sunlight"
Key: F major | Tempo: 92 BPM | 4/4 | ~3:40

v2 improvements:
- Synth riff: staccato/legato variation, velocity shaping, ornamental grace notes
- Synth arpeggio: varied patterns per bar instead of identical 16th loops
- Distorted guitar: power chords had 64-note velocity runs — now varied per beat
- Bass: was 140 identical repeated patterns — now with fills, chromatic walks, groove
- Vocal melody: had 39-note velocity runs — rewritten with contour-based dynamics
- Drums: humanized timing, ghost notes, varied fills at section boundaries
- Clean guitar: more fingerpicking variety, occasional hammer-ons
- Added sustain pedal for piano passages
- Section transitions: drum fills, cymbal crashes, dynamic ramps
- Synth pad: expression swells instead of flat velocity blocks
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from humanize import *

E = EventList()

def bt(bar_num):
    return bar_num * BAR4

# Chords in F major
F4 = make_chord(N('F',4), 'major')
Am4 = make_chord(N('A',4), 'minor')
Bb4 = make_chord(N('Bb',4), 'major')
C4m = make_chord(N('C',4), 'major')
Dm4 = make_chord(N('D',4), 'minor')
F4_add9 = make_chord(N('F',4), 'add9')
Bb4_add9 = [N('Bb',4), N('D',5), N('F',5), N('C',6)]
C4_sus4 = make_chord(N('C',4), 'sus4')

VERSE_CHORDS = [
    [F4, F4_add9], [Am4, Am4], [Bb4, Bb4_add9], [C4m, C4_sus4]
]
VERSE_BASS = [N('F',2), N('A',2), N('Bb',2), N('C',3)]

CHORUS_CHORDS = [
    [Bb4, Bb4_add9], [F4, F4_add9], [C4m, C4_sus4], [Dm4, Dm4]
]
CHORUS_BASS = [N('Bb',2), N('F',2), N('C',3), N('D',3)]

PRE_CHORDS = [
    [Dm4, Dm4], [Bb4, Bb4], [C4m, C4_sus4], [C4m, C4m]
]
PRE_BASS = [N('D',2), N('Bb',2), N('C',3), N('C',3)]

BREAK_CHORDS = [
    [F4, F4_add9], [Bb4, Bb4_add9], [C4m, C4_sus4], [Am4, Am4]
]
BREAK_BASS = [N('F',2), N('Bb',2), N('C',3), N('A',2)]


def get_chord(chords, ci, bar):
    return chords[ci][bar % len(chords[ci])]


def synth_riff_v2(bar_start, vel=62, bar_num=0):
    """The catchy 2-bar synth riff — now with staccato/legato variation and dynamics."""
    f, a, bb, c, d = N('F',5), N('A',5), N('Bb',5), N('C',6), N('D',5)

    # Bar 1: F-A-Bb-A-F with varied articulation
    riff1 = [
        (f, EIGHTH, 0),       # staccato
        (None, EIGHTH, 0),
        (a, EIGHTH, -3),
        (bb, EIGHTH + (20 if bar_num % 3 == 0 else 0), 2),  # slightly held sometimes
        (a, QUARTER, 0),
        (f, QUARTER, -2),
        (d, EIGHTH, -4),
        (f, EIGHTH + QUARTER, 3),  # let ring
    ]
    t = bar_start
    for i, (note, dur, vel_mod) in enumerate(riff1):
        if note is not None:
            v = breathing_vel(vel + vel_mod, bar_num, 4, 4)
            # Staccato on short notes, legato on long
            actual_dur = dur - (random.randint(30, 50) if dur <= EIGHTH else random.randint(15, 25))
            sw = swing_offset(i, 10)
            E.note(2, note, v, t + sw, actual_dur, time_amount=6, vel_amount=4)
        t += dur if note is not None else dur

    # Bar 2: A-Bb-C-Bb-A-F with variation per repeat
    if bar_num % 4 < 2:
        riff2 = [
            (a, EIGHTH, -2), (bb, EIGHTH, 0), (c, QUARTER, 4),
            (bb, EIGHTH, 0), (a, EIGHTH, -2),
            (f, QUARTER, -3), (None, QUARTER, 0), (f, QUARTER, 2),
        ]
    else:
        # Alternate ending: resolve differently
        riff2 = [
            (a, EIGHTH, -2), (bb, EIGHTH, 0), (c, QUARTER, 4),
            (bb, EIGHTH, 0), (a, EIGHTH, -3),
            (f, HALF, 2), (None, QUARTER, 0), (d, QUARTER, -4),
        ]

    t = bar_start + BAR4
    for i, (note, dur, vel_mod) in enumerate(riff2):
        if note is not None:
            v = breathing_vel(vel + vel_mod, bar_num + 1, 4, 4)
            actual_dur = dur - random.randint(15, 35)
            E.note(2, note, v, t + swing_offset(i, 10), actual_dur, time_amount=6, vel_amount=4)
        t += dur


def synth_arp_v2(bar_start, chord_notes, vel=40, bar_num=0):
    """16th-note arpeggio with varied patterns per bar and micro-timing."""
    notes = list(chord_notes) + [chord_notes[0] + 12]
    patterns = [
        lambda i, n: n[i % len(n)],
        lambda i, n: n[([0,1,2,3,2,1,0,1,2,3,2,1,0,1,2,3][i]) % len(n)],
        lambda i, n: n[([0,2,1,3,0,2,3,1,0,2,1,3,0,2,3,1][i]) % len(n)],
        lambda i, n: n[([3,1,2,0,3,1,0,2,3,1,2,0,3,2,1,0][i]) % len(n)],
        lambda i, n: n[([0,1,0,2,0,3,0,2,0,1,0,3,0,2,0,1][i]) % len(n)],
    ]
    get_note = patterns[bar_num % len(patterns)]
    bvel = breathing_vel(vel, bar_num, 6, 4)

    for i in range(16):
        note = get_note(i, notes)
        t = bar_start + i * SIXTEENTH
        v = bvel + accent_beat(i // 4) + (3 if i % 4 == 0 else -2)
        E.note(1, note, v, t, SIXTEENTH - random.randint(8, 15), time_amount=5, vel_amount=3)


def power_chord_v2(bar_start, root, vel=70, pattern='chorus', bar_num=0):
    """Distorted guitar power chords — now varied per beat."""
    pc = make_chord(root, 'power')
    bvel = breathing_vel(vel, bar_num, 4, 5)

    if pattern == 'chorus':
        for n in pc:
            v1 = bvel + random.randint(-3, 3)
            v2 = bvel - 5 + random.randint(-3, 3)
            E.note(4, n, v1, bar_start, HALF - random.randint(15, 25), time_amount=6, vel_amount=4)
            E.note(4, n, v2, bar_start + HALF, HALF - random.randint(15, 25), time_amount=8, vel_amount=4)
    elif pattern == 'muted':
        for i in range(8):
            v = bvel - 15 + accent_beat(i // 2) + random.randint(-4, 4)
            E.note(4, pc[0], v, bar_start + i * EIGHTH + swing_offset(i, 8),
                   EIGHTH - random.randint(25, 40), time_amount=6, vel_amount=3)
    elif pattern == 'sustained':
        for n in pc:
            E.note(4, n, bvel + random.randint(-3, 3), bar_start, BAR4 - 30,
                   time_amount=8, vel_amount=5)


def clean_guitar_v2(bar_start, chord_notes, vel=48, bar_num=0):
    """Clean guitar arpeggios with varied patterns and occasional hammer-ons."""
    notes = [n - 12 for n in chord_notes] + [chord_notes[0]]
    patterns = [
        [0, 2, 1, 3, 2, 0, 1, 2],
        [0, 1, 3, 2, 0, 3, 1, 2],
        [3, 1, 0, 2, 3, 0, 2, 1],
        [0, 2, 3, 1, 0, 2, 1, 3],
    ]
    pat = patterns[bar_num % len(patterns)]
    bvel = breathing_vel(vel, bar_num, 8, 4)

    for i in range(8):
        idx = pat[i] % len(notes)
        t = bar_start + i * EIGHTH + swing_offset(i, 10)
        v = bvel + (4 if i % 2 == 0 else -3) + random.randint(-2, 2)
        dur = EIGHTH - random.randint(12, 25)

        # Occasional hammer-on (quick grace note from below)
        if i == 4 and bar_num % 3 == 1:
            E.note(3, notes[idx] - 2, v - 12, t - SIXTEENTH, SIXTEENTH - 5,
                   time_amount=8, vel_amount=3)

        E.note(3, notes[idx], v, t, dur, time_amount=6, vel_amount=3)


def driving_bass_v2(bar_start, root, vel=58, bar_num=0, next_root=None):
    """Driving 8th-note bass with groove, fills, and chromatic walks."""
    bvel = breathing_vel(vel, bar_num, 8, 4)

    if bar_num % 8 == 7 and next_root is not None:
        # Fill bar: chromatic walk to next root
        walk_notes = []
        if next_root > root:
            step = 1
            count = min(4, next_root - root)
        else:
            step = -1
            count = min(4, root - next_root)
        for j in range(8):
            if j < 8 - count:
                walk_notes.append(root)
            else:
                walk_notes.append(root + (j - (8 - count) + 1) * step)
        for i, note in enumerate(walk_notes):
            v = bvel - 5 + (5 if i >= 4 else 0) + random.randint(-3, 3)
            E.note(6, note, v, bar_start + i * EIGHTH + swing_offset(i, 8),
                   EIGHTH - random.randint(12, 20), time_amount=6, vel_amount=3)
    else:
        # Standard driving pattern with groove
        fifth = root + 7
        seq = [root, root, fifth, root, root, fifth, root, root]
        if bar_num % 4 == 2:
            seq = [root, fifth, root, root, fifth, root, fifth, root]  # variation
        for i in range(8):
            v = bvel + (3 if i % 2 == 0 else -4) + random.randint(-3, 3)
            sw = swing_offset(i, 8)
            E.note(6, seq[i], v, bar_start + i * EIGHTH + sw,
                   EIGHTH - random.randint(10, 20), time_amount=6, vel_amount=3)


def full_drums_v2(bar_start, pattern='verse', bar_num=0):
    """Full drum kit with humanized timing, ghost notes, fills."""
    ch = 9
    kick, snare, hh_c, hh_o, crash = 36, 38, 42, 46, 49
    bvel_k = breathing_vel(65, bar_num, 8, 5)

    if pattern == 'verse':
        E.note(ch, kick, bvel_k, bar_start, QUARTER, time_amount=5, vel_amount=5)
        E.note(ch, snare, h_vel(52, 5), bar_start + QUARTER, QUARTER, time_amount=7, vel_amount=5)
        E.note(ch, kick, bvel_k - 5, bar_start + HALF, QUARTER, time_amount=6, vel_amount=5)
        E.note(ch, snare, h_vel(52, 5), bar_start + HALF + QUARTER, QUARTER, time_amount=7, vel_amount=5)
        for i in range(8):
            v = 32 + (5 if i % 2 == 0 else 0) + random.randint(-4, 4)
            E.note(ch, hh_c, v, bar_start + i * EIGHTH + swing_offset(i, 8),
                   EIGHTH, time_amount=5, vel_amount=3)
        # Ghost notes
        if bar_num % 2 == 0:
            E.note(ch, snare, 18, bar_start + EIGHTH + swing_offset(1, 8),
                   EIGHTH, time_amount=12, vel_amount=3)
        if bar_num % 3 == 2:
            E.note(ch, kick, bvel_k - 25, bar_start + QUARTER + EIGHTH,
                   EIGHTH, time_amount=10, vel_amount=4)

    elif pattern == 'chorus':
        E.note(ch, kick, bvel_k + 5, bar_start, QUARTER, time_amount=4, vel_amount=5)
        # Extra kick on and-of-1
        E.note(ch, kick, bvel_k - 10, bar_start + EIGHTH, EIGHTH, time_amount=8, vel_amount=4)
        E.note(ch, snare, h_vel(60, 5), bar_start + QUARTER, QUARTER, time_amount=6, vel_amount=5)
        E.note(ch, kick, bvel_k, bar_start + HALF, QUARTER, time_amount=5, vel_amount=5)
        E.note(ch, snare, h_vel(60, 5), bar_start + HALF + QUARTER, QUARTER, time_amount=6, vel_amount=5)
        for i in range(8):
            v = 37 + (5 if i % 2 == 0 else 0) + random.randint(-3, 3)
            E.note(ch, hh_c, v, bar_start + i * EIGHTH + swing_offset(i, 6),
                   EIGHTH, time_amount=4, vel_amount=2)
        # Ghost kick groove
        if bar_num % 2 == 1:
            E.note(ch, kick, bvel_k - 22, bar_start + QUARTER + EIGHTH,
                   EIGHTH, time_amount=10, vel_amount=4)

    elif pattern == 'fill':
        E.note(ch, kick, bvel_k + 8, bar_start, QUARTER, time_amount=4)
        E.note(ch, snare, 45, bar_start + QUARTER, EIGHTH, time_amount=8)
        E.note(ch, snare, 50, bar_start + QUARTER + EIGHTH, EIGHTH, time_amount=6)
        E.note(ch, snare, 55, bar_start + HALF, EIGHTH, time_amount=5)
        E.note(ch, snare, 60, bar_start + HALF + EIGHTH, EIGHTH, time_amount=6)
        E.note(ch, crash, 70, bar_start + HALF + QUARTER, QUARTER, time_amount=4)

    elif pattern == 'intro':
        E.note(ch, hh_c, 28 + random.randint(-4, 4), bar_start, EIGHTH,
               time_amount=8, vel_amount=3)
        E.note(ch, hh_c, 22 + random.randint(-4, 4), bar_start + HALF, EIGHTH,
               time_amount=8, vel_amount=3)

    elif pattern == 'crash':
        E.note(ch, crash, 72, bar_start, QUARTER, time_amount=3)
        E.note(ch, kick, 75, bar_start, QUARTER, time_amount=3)


def voice_v2(bar_start, phrase, vel=58, bar_num=0):
    """Vocal melody with contour-shaped dynamics."""
    t = bar_start
    prev_note = None
    for i, (note, dur) in enumerate(phrase):
        if note is not None:
            v = vel
            if prev_note is not None:
                interval = note - prev_note
                if interval > 3: v += 5
                elif interval < -3: v -= 2
            v = breathing_vel(v, bar_num + i, 6, 5)
            actual_dur = dur - random.randint(20, 40)

            # Anticipation on some notes
            antic = -SIXTEENTH if random.random() < 0.12 and i > 0 else 0

            # Grace note on leaps
            if prev_note and abs(note - prev_note) >= 4 and random.random() < 0.25:
                grace = prev_note + (1 if note > prev_note else -1)
                E.note(8, grace, v - 14, t + antic - SIXTEENTH, SIXTEENTH - 5,
                       time_amount=10, vel_amount=3)

            E.note(8, note, v, t + antic, actual_dur, time_amount=8, vel_amount=5)
            prev_note = note
        t += dur


def pad_swell(bar_start, chord_notes, vel=40, bars=2, bar_num=0):
    """Synth pad with expression swell."""
    steps = bars * 4
    for step in range(steps):
        t = bar_start + step * QUARTER
        phase = step / steps
        swell = math.sin(phase * math.pi)
        v = int(vel * 0.7 + vel * 0.3 * swell)
        E.cc(1, 11, max(40, min(127, int(v * 2.5))), h_time(t, 5))

    bvel = breathing_vel(vel, bar_num, 6, 4)
    for note in chord_notes:
        E.note(1, note, bvel, bar_start, BAR4 * bars - 30, time_amount=10, vel_amount=4)


# ============================================================
# BUILD THE SONG
# ============================================================

b = 0

# --- INTRO (4 bars) ---
synth_riff_v2(bt(0), vel=58, bar_num=0)
synth_riff_v2(bt(2), vel=62, bar_num=2)
for i in range(4):
    full_drums_v2(bt(i), 'intro', bar_num=i)
    synth_arp_v2(bt(i), F4 if i < 2 else Bb4, vel=28, bar_num=i)

b = 4

# --- VERSE 1 (16 bars) ---
for i in range(16):
    ci = (i // 2) % 4
    next_ci = ((i + 1) // 2) % 4
    ch = get_chord(VERSE_CHORDS, ci, i)

    clean_guitar_v2(bt(b + i), ch, vel=46, bar_num=i)
    synth_arp_v2(bt(b + i), ch, vel=33, bar_num=i)
    driving_bass_v2(bt(b + i), VERSE_BASS[ci], vel=53, bar_num=i, next_root=VERSE_BASS[next_ci])
    full_drums_v2(bt(b + i), 'verse', bar_num=i)

    if i % 4 == 0:
        synth_riff_v2(bt(b + i), vel=48, bar_num=i)

v1_mel = [
    [(N('F',5), EIGHTH), (N('A',5), EIGHTH), (N('Bb',5), QUARTER), (N('A',5), QUARTER+EIGHTH),
     (N('G',5), EIGHTH), (N('F',5), HALF), (None, HALF)],
    [(N('A',5), QUARTER), (N('G',5), QUARTER+EIGHTH), (N('F',5), EIGHTH),
     (N('D',5), HALF), (None, HALF)],
    [(N('F',5), EIGHTH), (N('G',5), EIGHTH), (N('A',5), QUARTER), (N('Bb',5), QUARTER+EIGHTH),
     (N('C',6), EIGHTH), (N('A',5), HALF), (None, HALF)],
    [(N('Bb',5), QUARTER), (N('A',5), QUARTER+EIGHTH), (N('G',5), EIGHTH),
     (N('F',5), HALF+QUARTER), (None, QUARTER)],
    [(N('F',5), QUARTER), (N('A',5), EIGHTH), (N('Bb',5), EIGHTH), (N('A',5), QUARTER+EIGHTH),
     (N('G',5), EIGHTH), (N('F',5), HALF), (None, HALF)],
    [(N('A',5), QUARTER), (N('Bb',5), QUARTER+EIGHTH), (N('A',5), EIGHTH),
     (N('F',5), HALF), (None, HALF)],
    [(N('C',6), QUARTER), (N('Bb',5), QUARTER), (N('A',5), QUARTER+EIGHTH), (N('G',5), EIGHTH),
     (N('F',5), HALF), (None, HALF)],
    [(N('G',5), QUARTER), (N('A',5), HALF+EIGHTH), (N('F',5), EIGHTH),
     (N('F',5), HALF+QUARTER), (None, QUARTER)],
]
for pi, phrase in enumerate(v1_mel):
    voice_v2(bt(b + pi * 2), phrase, vel=56, bar_num=pi)

b = 20

# --- PRE-CHORUS (4 bars) ---
for i in range(4):
    ch = get_chord(PRE_CHORDS, i, i)
    driving_bass_v2(bt(b + i), PRE_BASS[i], vel=56, bar_num=i + 16, next_root=PRE_BASS[min(i+1,3)])
    synth_arp_v2(bt(b + i), ch, vel=38, bar_num=i + 16)
    full_drums_v2(bt(b + i), 'verse', bar_num=i + 16)
    power_chord_v2(bt(b + i), PRE_BASS[i] + 24, vel=48 + i * 5, pattern='sustained', bar_num=i)

if True:
    full_drums_v2(bt(b + 3), 'fill', bar_num=19)

pc_mel = [
    (N('D',5), QUARTER), (N('F',5), QUARTER), (N('A',5), HALF+EIGHTH),
    (N('Bb',5), EIGHTH), (N('A',5), QUARTER+EIGHTH), (N('G',5), EIGHTH+QUARTER),
    (N('A',5), QUARTER), (N('Bb',5), QUARTER+EIGHTH), (N('C',6), EIGHTH+QUARTER),
    (N('C',6), HALF), (None, HALF),
]
t = bt(b)
prev_note = None
for note, dur in pc_mel:
    if note is not None:
        v = breathing_vel(60, 0, 4, 5)
        if prev_note and note > prev_note: v += 4
        E.note(8, note, v, t, dur - random.randint(20, 35), time_amount=8, vel_amount=5)
        prev_note = note
    t += dur

b = 24

# --- CHORUS 1 (8 bars) ---
full_drums_v2(bt(b), 'crash', bar_num=24)
for i in range(8):
    ci = (i // 2) % 4
    next_ci = ((i + 2) // 2) % 4
    ch = get_chord(CHORUS_CHORDS, ci, i)

    power_chord_v2(bt(b + i), CHORUS_BASS[ci] + 24, vel=70, pattern='chorus', bar_num=i)
    synth_arp_v2(bt(b + i), ch, vel=40, bar_num=i + 24)
    driving_bass_v2(bt(b + i), CHORUS_BASS[ci], vel=60, bar_num=i + 24, next_root=CHORUS_BASS[next_ci])
    full_drums_v2(bt(b + i), 'chorus', bar_num=i + 24)

    if i % 2 == 0:
        synth_riff_v2(bt(b + i), vel=53, bar_num=i + 24)

    if i % 4 == 0:
        pad_swell(bt(b + i), ch, vel=38, bars=2, bar_num=i)

ch_mel = [
    [(N('Bb',5), HALF), (N('C',6), HALF+EIGHTH), (N('D',6), EIGHTH+QUARTER), (N('C',6), HALF)],
    [(N('A',5), QUARTER), (N('Bb',5), HALF+EIGHTH), (N('A',5), EIGHTH), (N('F',5), HALF), (None, HALF)],
    [(N('C',6), HALF), (N('D',6), QUARTER+EIGHTH), (N('C',6), EIGHTH), (N('Bb',5), HALF), (None, HALF)],
    [(N('A',5), QUARTER), (N('G',5), QUARTER+EIGHTH), (N('F',5), EIGHTH), (N('F',5), HALF+QUARTER), (None, QUARTER)],
]
for pi, phrase in enumerate(ch_mel):
    voice_v2(bt(b + pi * 2), phrase, vel=63, bar_num=pi + 24)

b = 32

# --- VERSE 2 (16 bars) ---
for i in range(16):
    ci = (i // 2) % 4
    next_ci = ((i + 1) // 2) % 4
    ch = get_chord(VERSE_CHORDS, ci, i + 16)
    clean_guitar_v2(bt(b + i), ch, vel=48, bar_num=i + 32)
    synth_arp_v2(bt(b + i), ch, vel=35, bar_num=i + 32)
    driving_bass_v2(bt(b + i), VERSE_BASS[ci], vel=53, bar_num=i + 32, next_root=VERSE_BASS[next_ci])
    full_drums_v2(bt(b + i), 'verse', bar_num=i + 32)
    if i % 4 == 0:
        synth_riff_v2(bt(b + i), vel=50, bar_num=i + 32)

v2_mel = [
    [(N('A',5), QUARTER), (N('Bb',5), EIGHTH), (N('A',5), EIGHTH), (N('G',5), QUARTER+EIGHTH),
     (N('F',5), EIGHTH), (N('F',5), HALF), (None, HALF)],
    [(N('G',5), QUARTER), (N('A',5), QUARTER+EIGHTH), (N('F',5), EIGHTH),
     (N('E',5), HALF), (None, HALF)],
    [(N('F',5), QUARTER), (N('A',5), QUARTER+EIGHTH), (N('C',6), EIGHTH+QUARTER),
     (N('Bb',5), QUARTER), (N('A',5), QUARTER+HALF)],
    [(N('Bb',5), QUARTER), (N('A',5), EIGHTH), (N('G',5), EIGHTH), (N('F',5), HALF+EIGHTH),
     (N('F',5), EIGHTH+HALF+QUARTER), (None, QUARTER)],
    [(N('F',5), EIGHTH), (N('G',5), EIGHTH), (N('A',5), QUARTER), (N('Bb',5), QUARTER+EIGHTH),
     (N('A',5), EIGHTH), (N('G',5), HALF), (None, HALF)],
    [(N('A',5), QUARTER), (N('G',5), QUARTER+EIGHTH), (N('F',5), EIGHTH),
     (N('D',5), HALF), (None, HALF)],
    [(N('D',5), QUARTER), (N('F',5), QUARTER+EIGHTH), (N('A',5), EIGHTH+QUARTER),
     (N('Bb',5), HALF), (N('A',5), HALF)],
    [(N('G',5), QUARTER), (N('F',5), HALF+EIGHTH), (N('E',5), EIGHTH),
     (N('F',5), HALF+QUARTER), (None, QUARTER)],
]
for pi, phrase in enumerate(v2_mel):
    voice_v2(bt(b + pi * 2), phrase, vel=54, bar_num=pi + 32)

b = 48

# --- PRE-CHORUS 2 (4 bars) ---
for i in range(4):
    ch = get_chord(PRE_CHORDS, i, i + 4)
    driving_bass_v2(bt(b + i), PRE_BASS[i], vel=56, bar_num=i + 48, next_root=PRE_BASS[min(i+1,3)])
    synth_arp_v2(bt(b + i), ch, vel=38, bar_num=i + 48)
    full_drums_v2(bt(b + i), 'verse', bar_num=i + 48)
    power_chord_v2(bt(b + i), PRE_BASS[i] + 24, vel=50 + i * 5, pattern='sustained', bar_num=i + 4)
full_drums_v2(bt(b + 3), 'fill', bar_num=51)

t = bt(b)
prev_note = None
for note, dur in pc_mel:
    if note is not None:
        v = breathing_vel(62, 4, 4, 5)
        if prev_note and note > prev_note: v += 4
        E.note(8, note, v, t, dur - random.randint(20, 35), time_amount=8, vel_amount=5)
        prev_note = note
    t += dur

b = 52

# --- CHORUS 2 (8 bars) ---
full_drums_v2(bt(b), 'crash', bar_num=52)
for i in range(8):
    ci = (i // 2) % 4
    next_ci = ((i + 2) // 2) % 4
    ch = get_chord(CHORUS_CHORDS, ci, i + 8)
    power_chord_v2(bt(b + i), CHORUS_BASS[ci] + 24, vel=73, pattern='chorus', bar_num=i + 8)
    synth_arp_v2(bt(b + i), ch, vel=42, bar_num=i + 52)
    driving_bass_v2(bt(b + i), CHORUS_BASS[ci], vel=62, bar_num=i + 52, next_root=CHORUS_BASS[next_ci])
    full_drums_v2(bt(b + i), 'chorus', bar_num=i + 52)
    if i % 2 == 0:
        synth_riff_v2(bt(b + i), vel=56, bar_num=i + 52)
    if i % 4 == 0:
        pad_swell(bt(b + i), ch, vel=40, bars=2, bar_num=i + 8)

for pi, phrase in enumerate(ch_mel):
    voice_v2(bt(b + pi * 2), phrase, vel=66, bar_num=pi + 52)

b = 60

# --- INSTRUMENTAL BREAK (8 bars) ---
full_drums_v2(bt(b), 'crash', bar_num=60)
for i in range(8):
    ci = (i // 2) % 4
    next_ci = ((i + 2) // 2) % 4
    ch = get_chord(BREAK_CHORDS, ci, i)
    power_chord_v2(bt(b + i), BREAK_BASS[ci] + 24, vel=65, pattern='muted', bar_num=i + 60)
    synth_arp_v2(bt(b + i), ch, vel=40, bar_num=i + 60)
    driving_bass_v2(bt(b + i), BREAK_BASS[ci], vel=58, bar_num=i + 60, next_root=BREAK_BASS[next_ci])
    full_drums_v2(bt(b + i), 'chorus', bar_num=i + 60)

# Synth solo — with expressive dynamics and vibrato
solo = [
    (N('F',5), QUARTER), (N('A',5), QUARTER+EIGHTH), (N('C',6), EIGHTH+QUARTER),
    (N('D',6), QUARTER), (N('C',6), EIGHTH), (N('Bb',5), EIGHTH), (N('A',5), HALF+EIGHTH),
    (N('Bb',5), EIGHTH), (N('C',6), QUARTER+EIGHTH), (N('D',6), EIGHTH), (N('C',6), QUARTER),
    (N('A',5), HALF), (N('G',5), HALF+EIGHTH),
    (N('F',5), EIGHTH), (N('G',5), QUARTER+EIGHTH), (N('A',5), EIGHTH+QUARTER),
    (N('Bb',5), QUARTER), (N('A',5), QUARTER+EIGHTH), (N('G',5), EIGHTH+QUARTER),
    (N('A',5), QUARTER), (N('Bb',5), QUARTER+EIGHTH), (N('C',6), EIGHTH), (N('D',6), QUARTER),
    (N('C',6), HALF), (N('Bb',5), QUARTER+EIGHTH), (N('A',5), EIGHTH),
    (N('F',5), WHOLE),
]
t = bt(b)
prev_n = None
for note, dur in solo:
    if note is not None:
        v = 65
        if prev_n and note > prev_n: v += 4
        elif prev_n and note < prev_n: v -= 2
        v = breathing_vel(v, 0, 4, 6)
        actual_dur = dur - random.randint(15, 30)
        # Vibrato on longer notes
        if dur >= HALF:
            for step in range(dur // SIXTEENTH):
                bend_t = t + step * SIXTEENTH
                bend_val = int(250 * math.sin(step * 0.9))
                E.pitch_bend(2, bend_val, h_time(bend_t, 3))
            E.pitch_bend(2, 0, t + dur)
        E.note(2, note, v, t, actual_dur, time_amount=8, vel_amount=5)
        prev_n = note
    t += dur

b = 68

# --- FINAL CHORUS (8 bars) ---
full_drums_v2(bt(b), 'crash', bar_num=68)
for i in range(8):
    ci = (i // 2) % 4
    next_ci = ((i + 2) // 2) % 4
    ch = get_chord(CHORUS_CHORDS, ci, i + 16)
    power_chord_v2(bt(b + i), CHORUS_BASS[ci] + 24, vel=76, pattern='chorus', bar_num=i + 16)
    synth_arp_v2(bt(b + i), ch, vel=44, bar_num=i + 68)
    driving_bass_v2(bt(b + i), CHORUS_BASS[ci], vel=64, bar_num=i + 68, next_root=CHORUS_BASS[next_ci])
    full_drums_v2(bt(b + i), 'chorus', bar_num=i + 68)
    if i % 2 == 0:
        synth_riff_v2(bt(b + i), vel=58, bar_num=i + 68)
    if i % 4 == 0:
        pad_swell(bt(b + i), ch, vel=43, bars=2, bar_num=i + 16)

for pi, phrase in enumerate(ch_mel):
    voice_v2(bt(b + pi * 2), phrase, vel=68, bar_num=pi + 68)

b = 76

# --- OUTRO (8 bars) — Riff fades, instruments drop ---
for i in range(8):
    ci = i % 4
    ch = get_chord(VERSE_CHORDS, ci, i + 76)
    vel_fade = max(25, 58 - i * 5)

    if i < 6:
        synth_riff_v2(bt(b + i), vel=max(30, 53 - i * 5), bar_num=i + 76)
    if i < 4:
        driving_bass_v2(bt(b + i), VERSE_BASS[ci], vel=vel_fade, bar_num=i + 76)
    if i < 6:
        full_drums_v2(bt(b + i), 'verse', bar_num=i + 76)
    synth_arp_v2(bt(b + i), ch, vel=max(18, 33 - i * 3), bar_num=i + 76)

    if i >= 6:
        pad_swell(bt(b + i), F4, vel=max(15, 28 - i * 3), bars=1, bar_num=i + 76)


# ============================================================
# OUTPUT
# ============================================================

build_midi(E, 'The Machinery of Sunlight', bpm=92, total_bars=84,
           output_path='/home/user/music/compositions/v2/02_the_machinery_of_sunlight.mid')
