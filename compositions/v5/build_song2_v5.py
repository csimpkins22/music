#!/usr/bin/env python3
"""
Song 2 v5: "The Machinery of Sunlight"
Key: F major (modulates to Gb for final chorus) | Tempo: 92 BPM | 4/4 | ~3:50

v5 songwriter notes:
Building on v4 with four targeted improvements:

FIX 1: VERSE 1 MELODY bars 6-7 — syncopated descent between 5th leaps.
  D6 (eighth) rest (eighth) C6 (quarter+eighth) Bb5 (eighth). Rhythmic bite.

FIX 2: BAR 23 PRE-CHORUS — extend beat-4 silence. Synth arp drops out entirely
  on beat 4 of bar 23. Bass A→Bb→B walk only takes beats 1-3. Beat 4 = pure silence.

FIX 3: VERSE 2 bars 34-35 — synth counter-melody. While vocal echoes, synth lead
  plays D5→F5 (ascending) against vocal's descending line. Contrary motion.

FIX 4: VERSE 1 bars 12-15 — quiet muted distorted guitar (vel=28, eighth-note
  muted pattern) as texture buildup toward pre-chorus. Smoother entry into chorus.
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from humanize import *

E = EventList()

def bt(bar_num):
    return bar_num * BAR4

# ============================================================
# CHORDS — F major, with modulation to Gb
# ============================================================

F4 = make_chord(N('F',4), 'major')
Am4 = make_chord(N('A',4), 'minor')
Bb4 = make_chord(N('Bb',4), 'major')
C4m = make_chord(N('C',4), 'major')
Dm4 = make_chord(N('D',4), 'minor')
Gm4 = make_chord(N('G',4), 'minor')  # vi chord for verse reharmonization
F4_add9 = make_chord(N('F',4), 'add9')
Bb4_add9 = [N('Bb',4), N('D',5), N('F',5), N('C',6)]
C4_sus4 = make_chord(N('C',4), 'sus4')
Db4 = make_chord(N('Db',4), 'major')  # borrowed from F minor — the surprise
Db4_7 = make_chord(N('Db',4), '7')    # V7 of Gb for modulation prep

# Gb major key chords (for final chorus modulation)
Gb4 = make_chord(N('Gb',4), 'major')
Bbm4 = make_chord(N('Bb',4), 'minor')
Cb4 = make_chord(N('B',3), 'major')  # Cb = B enharmonic
Db4_ch = make_chord(N('Db',4), 'major')
Ebm4 = make_chord(N('Eb',4), 'minor')

VERSE_CHORDS = [
    [F4, F4_add9], [Am4, Am4], [Bb4, Bb4_add9], [C4m, C4_sus4]
]
# Reharmonized version: bar 3 (index 2) is Gm instead of Bb
VERSE_CHORDS_REHARMED = [
    [F4, F4_add9], [Am4, Am4], [Gm4, Gm4], [C4m, C4_sus4]
]
VERSE_BASS = [N('F',2), N('A',2), N('Bb',2), N('C',3)]
VERSE_BASS_REHARMED = [N('F',2), N('A',2), N('G',2), N('C',3)]  # Gm root

CHORUS_CHORDS = [
    [Bb4, Bb4_add9], [F4, F4_add9], [C4m, C4_sus4], [Dm4, Dm4]
]
CHORUS_BASS = [N('Bb',2), N('F',2), N('C',3), N('D',3)]

PRE_CHORDS = [
    [Dm4, Dm4], [Bb4, Bb4], [C4m, C4_sus4], [C4m, C4m]
]
PRE_BASS = [N('D',2), N('Bb',2), N('C',3), N('E',2)]  # C/E in bar 4 — bass walks up to F

BREAK_CHORDS = [
    [F4, F4_add9], [Dm4, Dm4], [Bb4, Bb4_add9], [C4m, C4_sus4]
]
BREAK_BASS = [N('F',2), N('D',2), N('Bb',2), N('C',3)]

# Gb major final chorus
FINAL_CHORDS = [
    [Cb4, Cb4], [Gb4, Gb4], [Db4_ch, Db4_ch], [Ebm4, Ebm4]
]
FINAL_BASS = [N('B',1), N('Gb',2), N('Db',3), N('Eb',3)]

def gc(chords, ci, bar):
    return chords[ci][bar % len(chords[ci])]


# ============================================================
# Helper: is this bar in the 2nd 8-bar cycle of a verse?
# ============================================================
def is_reharmed_bar(bar_in_verse):
    """Returns True if this bar falls in the 2nd 8-bar cycle (bars 8-15)."""
    return 8 <= bar_in_verse < 16


def get_verse_chord_and_bass(bar_in_verse, ci):
    """Return the appropriate chord/bass for this verse bar, with reharmonization."""
    if is_reharmed_bar(bar_in_verse):
        ch = gc(VERSE_CHORDS_REHARMED, ci, bar_in_verse)
        bass = VERSE_BASS_REHARMED[ci]
    else:
        ch = gc(VERSE_CHORDS, ci, bar_in_verse)
        bass = VERSE_BASS[ci]
    return ch, bass


# ============================================================
# INSTRUMENT FUNCTIONS
# ============================================================

def synth_riff(bar_start, vel=62, bar_num=0, key='F'):
    """The catchy synth riff — develops across the song."""
    if key == 'F':
        f, a, bb, c, d = N('F',5), N('A',5), N('Bb',5), N('C',6), N('D',5)
    else:  # Gb
        f, a, bb, c, d = N('Gb',5), N('Bb',5), N('B',5), N('Db',6), N('Eb',5)

    riff1 = [
        (f, EIGHTH, 0), (None, EIGHTH, 0),
        (a, EIGHTH, -3), (bb, EIGHTH + (20 if bar_num % 3 == 0 else 0), 2),
        (a, QUARTER, 0), (f, QUARTER, -2),
        (d, EIGHTH, -4), (f, EIGHTH + QUARTER, 3),
    ]
    t = bar_start
    for i, (note, dur, vel_mod) in enumerate(riff1):
        if note is not None:
            v = breathing_vel(vel + vel_mod, bar_num, 4, 4)
            actual_dur = dur - (random.randint(30, 50) if dur <= EIGHTH else random.randint(15, 25))
            E.note(2, note, v, t + swing_offset(i, 10), actual_dur, time_amount=6, vel_amount=4)
        t += dur if note is not None else dur

    if bar_num % 4 < 2:
        riff2 = [
            (a, EIGHTH, -2), (bb, EIGHTH, 0), (c, QUARTER, 4),
            (bb, EIGHTH, 0), (a, EIGHTH, -2),
            (f, QUARTER, -3), (None, QUARTER, 0), (f, QUARTER, 2),
        ]
    else:
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


def synth_arp(bar_start, chord_notes, vel=40, bar_num=0, stop_at_beat=None):
    """16th-note arpeggio with varied patterns.
    stop_at_beat: if set, only play up to (but not including) this beat (0-indexed).
    Used to create silence on specific beats (e.g., beat 4 of bar 23)."""
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

    max_sixteenths = 16
    if stop_at_beat is not None:
        max_sixteenths = stop_at_beat * 4  # 4 sixteenths per beat

    for i in range(max_sixteenths):
        note = get_note(i, notes)
        t = bar_start + i * SIXTEENTH
        v = bvel + accent_beat(i // 4) + (3 if i % 4 == 0 else -2)
        E.note(1, note, v, t, SIXTEENTH - random.randint(8, 15), time_amount=5, vel_amount=3)


def power_chord(bar_start, root, vel=70, pattern='chorus', bar_num=0):
    """Distorted guitar power chords."""
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


def clean_guitar(bar_start, chord_notes, vel=48, bar_num=0):
    """Clean guitar arpeggios with varied patterns."""
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
        if i == 4 and bar_num % 3 == 1:
            E.note(3, notes[idx] - 2, v - 12, t - SIXTEENTH, SIXTEENTH - 5, time_amount=8)
        E.note(3, notes[idx], v, t, dur, time_amount=6, vel_amount=3)


def driving_bass(bar_start, root, vel=58, bar_num=0, next_root=None, chromatic_walk_beat4=False):
    """Driving 8th-note bass with groove and chromatic walks.
    chromatic_walk_beat4: if True, beat 4 walks chromatically toward next_root."""
    bvel = breathing_vel(vel, bar_num, 8, 4)

    if bar_num % 8 == 7 and next_root is not None:
        walk_notes = []
        step = 1 if next_root > root else -1
        count = min(4, abs(next_root - root))
        for j in range(8):
            if j < 8 - count:
                walk_notes.append(root)
            else:
                walk_notes.append(root + (j - (8 - count) + 1) * step)
        for i, note in enumerate(walk_notes):
            v = bvel - 5 + (5 if i >= 4 else 0) + random.randint(-3, 3)
            E.note(6, note, v, bar_start + i * EIGHTH + swing_offset(i, 8),
                   EIGHTH - random.randint(12, 20), time_amount=6, vel_amount=3)
    elif chromatic_walk_beat4 and next_root is not None:
        fifth = root + 7
        seq = [root, root, fifth, root, root, fifth]  # beats 1-3 normal
        step = 1 if next_root > root else -1
        walk_start = root + step
        walk_end = walk_start + step
        seq.append(walk_start)
        seq.append(walk_end)
        for i in range(8):
            v = bvel + (3 if i % 2 == 0 else -4) + random.randint(-3, 3)
            E.note(6, seq[i], v, bar_start + i * EIGHTH + swing_offset(i, 8),
                   EIGHTH - random.randint(10, 20), time_amount=6, vel_amount=3)
    else:
        fifth = root + 7
        seq = [root, root, fifth, root, root, fifth, root, root]
        if bar_num % 4 == 2:
            seq = [root, fifth, root, root, fifth, root, fifth, root]
        for i in range(8):
            v = bvel + (3 if i % 2 == 0 else -4) + random.randint(-3, 3)
            E.note(6, seq[i], v, bar_start + i * EIGHTH + swing_offset(i, 8),
                   EIGHTH - random.randint(10, 20), time_amount=6, vel_amount=3)


def chromatic_bass_walk(bar_start, notes_sequence, vel=58, bar_num=0, beats=4):
    """Play a chromatic bass walk: one note per beat across a bar.
    notes_sequence: list of MIDI notes, one per beat.
    beats: number of beats to play (default 4). Use 3 to leave beat 4 silent."""
    bvel = breathing_vel(vel, bar_num, 8, 4)
    for i, note in enumerate(notes_sequence[:beats]):
        v = bvel + (4 if i == 0 else 0) + random.randint(-3, 3)
        E.note(6, note, v, bar_start + i * QUARTER, QUARTER - random.randint(10, 20),
               time_amount=6, vel_amount=3)


def whole_bass(bar_start, root, vel=50, bar_num=0):
    """Simple whole-note bass for quieter moments."""
    bvel = breathing_vel(vel, bar_num, 8, 4)
    E.note(6, root, bvel, bar_start, BAR4 - 30, time_amount=8, vel_amount=4)


def full_drums(bar_start, pattern='verse', bar_num=0, verse_build_phase=None):
    """Full drum kit.
    verse_build_phase: 0-3 for progressive verse build.
      0 = kick on 1 only
      1 = add snare ghost notes on beat 2+
      2 = add hi-hat 8ths
      3 = full verse pattern (same as original 'verse')
    """
    ch = 9
    kick, snare, hh_c, hh_o, crash = 36, 38, 42, 46, 49
    bvel_k = breathing_vel(65, bar_num, 8, 5)

    if pattern == 'verse' and verse_build_phase is not None:
        if verse_build_phase == 0:
            E.note(ch, kick, bvel_k, bar_start, QUARTER, time_amount=5, vel_amount=5)

        elif verse_build_phase == 1:
            E.note(ch, kick, bvel_k, bar_start, QUARTER, time_amount=5, vel_amount=5)
            E.note(ch, snare, 25, bar_start + QUARTER + swing_offset(1, 8), EIGHTH, time_amount=10, vel_amount=3)
            E.note(ch, snare, 22, bar_start + HALF + EIGHTH + swing_offset(1, 8), EIGHTH, time_amount=12, vel_amount=3)
            E.note(ch, snare, 28, bar_start + HALF + QUARTER + swing_offset(1, 8), EIGHTH, time_amount=10, vel_amount=3)

        elif verse_build_phase == 2:
            E.note(ch, kick, bvel_k, bar_start, QUARTER, time_amount=5, vel_amount=5)
            E.note(ch, snare, 25, bar_start + QUARTER + swing_offset(1, 8), EIGHTH, time_amount=10, vel_amount=3)
            E.note(ch, snare, 22, bar_start + HALF + EIGHTH + swing_offset(1, 8), EIGHTH, time_amount=12, vel_amount=3)
            E.note(ch, snare, 28, bar_start + HALF + QUARTER + swing_offset(1, 8), EIGHTH, time_amount=10, vel_amount=3)
            for i in range(8):
                v = 32 + (5 if i % 2 == 0 else 0) + random.randint(-4, 4)
                E.note(ch, hh_c, v, bar_start + i * EIGHTH + swing_offset(i, 8), EIGHTH, time_amount=5)

        else:
            E.note(ch, kick, bvel_k, bar_start, QUARTER, time_amount=5, vel_amount=5)
            E.note(ch, snare, h_vel(52, 5), bar_start + QUARTER, QUARTER, time_amount=7, vel_amount=5)
            E.note(ch, kick, bvel_k - 5, bar_start + HALF, QUARTER, time_amount=6, vel_amount=5)
            E.note(ch, snare, h_vel(52, 5), bar_start + HALF + QUARTER, QUARTER, time_amount=7, vel_amount=5)
            for i in range(8):
                v = 32 + (5 if i % 2 == 0 else 0) + random.randint(-4, 4)
                E.note(ch, hh_c, v, bar_start + i * EIGHTH + swing_offset(i, 8), EIGHTH, time_amount=5)
            if bar_num % 2 == 0:
                E.note(ch, snare, 18, bar_start + EIGHTH + swing_offset(1, 8), EIGHTH, time_amount=12)

    elif pattern == 'verse':
        E.note(ch, kick, bvel_k, bar_start, QUARTER, time_amount=5, vel_amount=5)
        E.note(ch, snare, h_vel(52, 5), bar_start + QUARTER, QUARTER, time_amount=7, vel_amount=5)
        E.note(ch, kick, bvel_k - 5, bar_start + HALF, QUARTER, time_amount=6, vel_amount=5)
        E.note(ch, snare, h_vel(52, 5), bar_start + HALF + QUARTER, QUARTER, time_amount=7, vel_amount=5)
        for i in range(8):
            v = 32 + (5 if i % 2 == 0 else 0) + random.randint(-4, 4)
            E.note(ch, hh_c, v, bar_start + i * EIGHTH + swing_offset(i, 8), EIGHTH, time_amount=5)
        if bar_num % 2 == 0:
            E.note(ch, snare, 18, bar_start + EIGHTH + swing_offset(1, 8), EIGHTH, time_amount=12)

    elif pattern == 'chorus':
        E.note(ch, kick, bvel_k + 5, bar_start, QUARTER, time_amount=4, vel_amount=5)
        E.note(ch, kick, bvel_k - 10, bar_start + EIGHTH, EIGHTH, time_amount=8, vel_amount=4)
        E.note(ch, snare, h_vel(60, 5), bar_start + QUARTER, QUARTER, time_amount=6, vel_amount=5)
        E.note(ch, kick, bvel_k, bar_start + HALF, QUARTER, time_amount=5, vel_amount=5)
        E.note(ch, snare, h_vel(60, 5), bar_start + HALF + QUARTER, QUARTER, time_amount=6, vel_amount=5)
        for i in range(8):
            v = 37 + (5 if i % 2 == 0 else 0) + random.randint(-3, 3)
            E.note(ch, hh_c, v, bar_start + i * EIGHTH + swing_offset(i, 6), EIGHTH, time_amount=4)
        if bar_num % 2 == 1:
            E.note(ch, kick, bvel_k - 22, bar_start + QUARTER + EIGHTH, EIGHTH, time_amount=10)

    elif pattern == 'fill':
        E.note(ch, kick, bvel_k + 8, bar_start, QUARTER, time_amount=4)
        E.note(ch, snare, 45, bar_start + QUARTER, EIGHTH, time_amount=8)
        E.note(ch, snare, 50, bar_start + QUARTER + EIGHTH, EIGHTH, time_amount=6)
        E.note(ch, snare, 55, bar_start + HALF, EIGHTH, time_amount=5)
        E.note(ch, snare, 60, bar_start + HALF + EIGHTH, EIGHTH, time_amount=6)
        E.note(ch, crash, 70, bar_start + HALF + QUARTER, QUARTER, time_amount=4)

    elif pattern == 'fill_beat3':
        # Fill that stops after beat 3 — leaves beat 4 silent for the breath
        E.note(ch, kick, bvel_k + 8, bar_start, QUARTER, time_amount=4)
        E.note(ch, snare, 45, bar_start + QUARTER, EIGHTH, time_amount=8)
        E.note(ch, snare, 50, bar_start + QUARTER + EIGHTH, EIGHTH, time_amount=6)
        E.note(ch, snare, 55, bar_start + HALF, EIGHTH, time_amount=5)
        E.note(ch, snare, 60, bar_start + HALF + EIGHTH, EIGHTH, time_amount=6)
        # NO crash on beat 4 — silence

    elif pattern == 'intro':
        E.note(ch, hh_c, 28 + random.randint(-4, 4), bar_start, EIGHTH, time_amount=8)
        E.note(ch, hh_c, 22 + random.randint(-4, 4), bar_start + HALF, EIGHTH, time_amount=8)

    elif pattern == 'crash':
        E.note(ch, crash, 72, bar_start, QUARTER, time_amount=3)
        E.note(ch, kick, 75, bar_start, QUARTER, time_amount=3)


def pad_swell(bar_start, chord_notes, vel=40, bars=2, bar_num=0):
    """Synth pad with expression swell."""
    steps = bars * 4
    for step in range(steps):
        t = bar_start + step * QUARTER
        swell = math.sin((step / steps) * math.pi)
        v = int(vel * 0.7 + vel * 0.3 * swell)
        E.cc(1, 11, max(40, min(127, int(v * 2.5))), h_time(t, 5))
    bvel = breathing_vel(vel, bar_num, 6, 4)
    for note in chord_notes:
        E.note(1, note, bvel, bar_start, BAR4 * bars - 30, time_amount=10, vel_amount=4)


def voice(bar_start, phrase, vel=58, bar_num=0):
    """Vocal melody with contour dynamics."""
    t = bar_start
    prev = None
    for i, (note, dur) in enumerate(phrase):
        if note is not None:
            v = vel
            if prev is not None:
                if note > prev + 3: v += 5
                elif note < prev - 3: v -= 2
            v = breathing_vel(v, bar_num + i, 6, 5)
            antic = -SIXTEENTH if random.random() < 0.12 and i > 0 else 0
            if prev and abs(note - prev) >= 4 and random.random() < 0.25:
                grace = prev + (1 if note > prev else -1)
                E.note(8, grace, v - 14, t + antic - SIXTEENTH, SIXTEENTH - 5, time_amount=10)
            E.note(8, note, v, t + antic, dur - random.randint(20, 40), time_amount=8, vel_amount=5)
            prev = note
        t += dur


# ============================================================
# BUILD THE SONG
# ============================================================

b = 0

# --- INTRO (4 bars) ---
synth_riff(bt(0), vel=58, bar_num=0)
synth_riff(bt(2), vel=62, bar_num=2)
for i in range(4):
    full_drums(bt(i), 'intro', bar_num=i)
    synth_arp(bt(i), F4 if i < 2 else Bb4, vel=28, bar_num=i)

b = 4

# --- VERSE 1 (16 bars) ---
# Progressive drum build over 4x4-bar blocks
for i in range(16):
    ci = (i // 2) % 4
    next_ci = ((i + 1) // 2) % 4

    # Reharmonize 2nd 8-bar cycle (bars 8-15 within verse)
    ch, bass_root = get_verse_chord_and_bass(i, ci)
    next_ch, next_bass = get_verse_chord_and_bass(i + 1 if i < 15 else 0, next_ci)

    clean_guitar(bt(b + i), ch, vel=46, bar_num=i)
    synth_arp(bt(b + i), ch, vel=33, bar_num=i)

    # Every 4th verse bar, chromatic bass walk on beat 4
    use_chromatic = (i % 4 == 3)
    driving_bass(bt(b + i), bass_root, vel=53, bar_num=i,
                 next_root=next_bass, chromatic_walk_beat4=use_chromatic)

    # Determine drum build phase (0-3) based on 4-bar block
    verse_build = i // 4  # 0, 1, 2, 3
    full_drums(bt(b + i), 'verse', bar_num=i, verse_build_phase=verse_build)

    if i % 4 == 0:
        synth_riff(bt(b + i), vel=48, bar_num=i)

    # v5 FIX 4: Bars 12-15 (last 4 bars of verse 1) — quiet muted distorted guitar
    # vel=28, eighth-note muted pattern as texture buildup toward pre-chorus
    if 12 <= i <= 15:
        power_chord(bt(b + i), bass_root + 24, vel=28, pattern='muted', bar_num=i)

# v5 FIX 1: Verse 1 melody with syncopated descent in bars 6-7 (phrase 4, 0-indexed phrase 3)
# Between the 5th leaps: D6 (eighth) rest (eighth) C6 (quarter+eighth) Bb5 (eighth)
v1_mel = [
    # Phrase 1: F5 LEAPS to C6 (5th!), falls to Bb5, rest, A5 drops to D5 (5th!)
    [(N('F',5), QUARTER), (N('C',6), HALF), (N('Bb',5), QUARTER),
     (None, QUARTER), (N('A',5), QUARTER), (N('D',5), HALF)],
    # Phrase 2: echo the 5th — G5 up to D6, settle back
    [(N('G',5), QUARTER), (N('D',6), QUARTER+EIGHTH), (N('C',6), EIGHTH),
     (N('Bb',5), HALF), (None, HALF)],
    # Phrase 3: another 5th leap — F5 to C6, then stepwise descent
    [(N('F',5), EIGHTH), (N('C',6), QUARTER+EIGHTH), (N('Bb',5), QUARTER),
     (N('A',5), QUARTER), (N('G',5), HALF), (None, HALF)],
    # Phrase 4 (bars 6-7): v5 FIX 1 — syncopated descent between 5th hooks
    # D6 (eighth) rest (eighth) C6 (quarter+eighth) Bb5 (eighth) — rhythmic bite
    [(N('A',5), QUARTER), (N('D',6), EIGHTH), (None, EIGHTH),
     (N('C',6), QUARTER+EIGHTH), (N('Bb',5), EIGHTH),
     (N('F',5), HALF+QUARTER), (None, QUARTER)],
    # Phrase 5: restart with the hook leap
    [(N('F',5), QUARTER), (N('C',6), HALF), (N('Bb',5), QUARTER+EIGHTH),
     (N('A',5), EIGHTH), (N('G',5), HALF)],
    # Phrase 6: invert the 5th — C6 down to F5
    [(N('C',6), QUARTER), (N('F',5), HALF+EIGHTH), (N('G',5), EIGHTH),
     (N('A',5), HALF), (None, HALF)],
    # Phrase 7: build tension with ascending 5ths
    [(N('D',5), QUARTER), (N('A',5), QUARTER), (N('C',6), QUARTER+EIGHTH), (N('Bb',5), EIGHTH),
     (N('A',5), HALF), (None, HALF)],
    # Phrase 8: resolve downward with final 5th drop
    [(N('A',5), QUARTER), (N('D',5), HALF+EIGHTH), (N('F',5), EIGHTH),
     (N('F',5), HALF+QUARTER), (None, QUARTER)],
]
for pi, phrase in enumerate(v1_mel):
    voice(bt(b + pi * 2), phrase, vel=56, bar_num=pi)

b = 20

# --- PRE-CHORUS (4 bars) — Building, bass walks C→E in bar 4 ---
for i in range(4):
    ch = gc(PRE_CHORDS, i, i)

    if i < 3:
        synth_arp(bt(b + i), ch, vel=38, bar_num=i + 16)
        power_chord(bt(b + i), PRE_BASS[i] + 24, vel=48 + i * 5, pattern='sustained', bar_num=i)
        full_drums(bt(b + i), 'verse', bar_num=i + 16)
        driving_bass(bt(b + i), PRE_BASS[i], vel=56, bar_num=i + 16, next_root=PRE_BASS[min(i+1,3)])
    else:
        # v5 FIX 2: Bar 23 — synth arp drops out entirely on beat 4
        # Bass A→Bb→B walk only takes beats 1-3. Beat 4 is pure silence.
        synth_arp(bt(b + i), ch, vel=38, bar_num=i + 16, stop_at_beat=3)
        power_chord(bt(b + i), PRE_BASS[i] + 24, vel=48 + i * 5, pattern='sustained', bar_num=i)
        full_drums(bt(b + i), 'fill_beat3', bar_num=19)
        # Bass walk A→Bb→B only on beats 1-3 (3 notes, not 4)
        chromatic_bass_walk(bt(b + i), [N('A',2), N('Bb',2), N('B',2)],
                           vel=56, bar_num=19, beats=3)

# Pre-chorus melody — RISING chromatic line builds tension
pc_mel = [
    (N('D',5), QUARTER), (N('F',5), QUARTER), (N('A',5), HALF+EIGHTH),
    (N('Bb',5), EIGHTH), (N('A',5), QUARTER+EIGHTH), (N('G',5), EIGHTH+QUARTER),
    # Here's the rising chromatic: A→Bb→B→C
    (N('A',5), QUARTER), (N('Bb',5), QUARTER+EIGHTH), (N('B',5), EIGHTH+QUARTER),
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
full_drums(bt(b), 'crash', bar_num=24)
for i in range(8):
    ci = (i // 2) % 4
    next_ci = ((i + 2) // 2) % 4
    ch = gc(CHORUS_CHORDS, ci, i)
    power_chord(bt(b + i), CHORUS_BASS[ci] + 24, vel=70, pattern='chorus', bar_num=i)
    synth_arp(bt(b + i), ch, vel=40, bar_num=i + 24)
    driving_bass(bt(b + i), CHORUS_BASS[ci], vel=60, bar_num=i + 24, next_root=CHORUS_BASS[next_ci])
    full_drums(bt(b + i), 'chorus', bar_num=i + 24)
    if i % 2 == 0:
        synth_riff(bt(b + i), vel=53, bar_num=i + 24)
    if i % 4 == 0:
        pad_swell(bt(b + i), ch, vel=38, bars=2, bar_num=i)

# Chorus melody — HELD NOTE approach
ch_mel = [
    [(N('C',6), WHOLE),
     (N('Bb',5), HALF), (N('A',5), SIXTEENTH), (N('Bb',5), SIXTEENTH),
     (N('A',5), SIXTEENTH), (N('G',5), SIXTEENTH), (N('A',5), QUARTER+EIGHTH), (N('F',5), EIGHTH)],
    [(N('Bb',5), HALF+QUARTER), (N('A',5), QUARTER),
     (N('F',5), HALF), (None, HALF)],
    [(N('C',6), WHOLE),
     (N('D',6), QUARTER), (N('C',6), SIXTEENTH), (N('Bb',5), SIXTEENTH),
     (N('A',5), SIXTEENTH), (N('G',5), SIXTEENTH), (N('A',5), HALF)],
    [(N('Bb',5), QUARTER), (N('A',5), QUARTER+EIGHTH), (N('G',5), EIGHTH),
     (N('F',5), HALF+QUARTER), (None, QUARTER)],
]
for pi, phrase in enumerate(ch_mel):
    voice(bt(b + pi * 2), phrase, vel=63, bar_num=pi + 24)

b = 32

# --- VERSE 2 (16 bars) — Bass drops out bars 5-8 for breathing room ---
for i in range(16):
    ci = (i // 2) % 4
    next_ci = ((i + 1) // 2) % 4

    # Reharmonize 2nd 8-bar cycle
    ch, bass_root = get_verse_chord_and_bass(i, ci)
    next_ch, next_bass = get_verse_chord_and_bass(i + 1 if i < 15 else 0, next_ci)

    clean_guitar(bt(b + i), ch, vel=48, bar_num=i + 32)
    synth_arp(bt(b + i), ch, vel=35, bar_num=i + 32)

    # Progressive drum build for verse 2 as well
    verse_build = i // 4
    full_drums(bt(b + i), 'verse', bar_num=i + 32, verse_build_phase=verse_build)

    if i % 4 == 0:
        synth_riff(bt(b + i), vel=50, bar_num=i + 32)

    # BASS DROPS OUT bars 4-7 — creates a pocket of space (kept from v3)
    if i < 4 or i >= 8:
        use_chromatic = (i % 4 == 3)
        driving_bass(bt(b + i), bass_root, vel=53, bar_num=i + 32,
                     next_root=next_bass, chromatic_walk_beat4=use_chromatic)
    elif i == 4:
        whole_bass(bt(b + i), bass_root, vel=35, bar_num=i + 32)

# Verse 2 melody — same intervallic 5th identity but resolves UP (foreshadows modulation)
v2_mel = [
    [(N('F',5), QUARTER), (N('C',6), HALF), (N('Bb',5), QUARTER),
     (None, QUARTER), (N('A',5), QUARTER), (N('D',5), HALF)],
    [(N('G',5), QUARTER), (N('A',5), QUARTER+EIGHTH), (N('F',5), EIGHTH),
     (N('E',5), HALF), (None, HALF)],
    [(N('F',5), QUARTER), (N('C',6), QUARTER+EIGHTH), (N('Bb',5), EIGHTH+QUARTER),
     (N('A',5), QUARTER), (N('G',5), QUARTER+HALF)],
    [(N('A',5), QUARTER), (N('D',5), EIGHTH), (N('E',5), EIGHTH), (N('F',5), HALF+EIGHTH),
     (N('F',5), EIGHTH+HALF+QUARTER), (None, QUARTER)],
    [(N('F',5), EIGHTH), (N('C',6), QUARTER+EIGHTH), (N('Bb',5), QUARTER+EIGHTH),
     (N('A',5), EIGHTH), (N('G',5), HALF), (None, HALF)],
    [(N('C',6), QUARTER), (N('F',5), QUARTER+EIGHTH), (N('G',5), EIGHTH),
     (N('A',5), HALF), (None, HALF)],
    # Verse 2 diverges — RISES with 5ths pointing upward
    [(N('D',5), QUARTER), (N('A',5), QUARTER+EIGHTH), (N('C',6), EIGHTH+QUARTER),
     (N('Bb',5), HALF), (N('C',6), HALF)],
    # Resolves on C6 (not F5 like v1) — pointing UP, toward the modulation later
    [(N('C',6), QUARTER), (N('Bb',5), HALF+EIGHTH), (N('A',5), EIGHTH),
     (N('Bb',5), HALF+QUARTER), (None, QUARTER)],
]
for pi, phrase in enumerate(v2_mel):
    voice(bt(b + pi * 2), phrase, vel=54, bar_num=pi + 32)

# v5 FIX 3: Verse 2 bars 34-35 (i=2,3 within verse, phrase index 1) —
# Synth counter-melody: D5→F5 ascending against vocal's descending line.
# Bars 34-35 are absolute bars, = verse 2 bars 2-3 (b+2 and b+3).
# Vocal phrase 2 (pi=1) covers bars 34-35: G5→A5→F5→E5 (descending trend).
# Synth lead plays contrary ascending D5→F5 across those two bars.
counter_mel_v2 = [
    (N('D',5), QUARTER), (N('D',5), QUARTER+EIGHTH), (N('E',5), EIGHTH),
    (N('F',5), HALF),
    (N('F',5), QUARTER), (N('E',5), QUARTER), (N('F',5), HALF),
]
t_counter = bt(b + 2)
for note, dur in counter_mel_v2:
    v = breathing_vel(45, 34, 4, 4)
    E.note(2, note, v, t_counter, dur - random.randint(15, 30), time_amount=8, vel_amount=4)
    t_counter += dur

b = 48

# --- PRE-CHORUS 2 (4 bars) ---
for i in range(4):
    ch = gc(PRE_CHORDS, i, i + 4)

    if i < 3:
        synth_arp(bt(b + i), ch, vel=38, bar_num=i + 48)
        power_chord(bt(b + i), PRE_BASS[i] + 24, vel=50 + i * 5, pattern='sustained', bar_num=i + 4)
        driving_bass(bt(b + i), PRE_BASS[i], vel=56, bar_num=i + 48, next_root=PRE_BASS[min(i+1,3)])
        full_drums(bt(b + i), 'verse', bar_num=i + 48)
    else:
        # v5 FIX 2: Beat 4 silence before chorus 2 (same treatment as bar 23)
        synth_arp(bt(b + i), ch, vel=38, bar_num=i + 48, stop_at_beat=3)
        power_chord(bt(b + i), PRE_BASS[i] + 24, vel=50 + i * 5, pattern='sustained', bar_num=i + 4)
        full_drums(bt(b + i), 'fill_beat3', bar_num=51)
        chromatic_bass_walk(bt(b + i), [N('A',2), N('Bb',2), N('B',2)],
                           vel=56, bar_num=51, beats=3)

# Re-use pre-chorus melody
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

# --- CHORUS 2 (8 bars) — With Db surprise chord in bar 7 ---
full_drums(bt(b), 'crash', bar_num=52)
for i in range(8):
    ci = (i // 2) % 4
    next_ci = ((i + 2) // 2) % 4

    # Bar 6-7: Db major instead of Dm — borrowed from F minor, creates yearning
    if i >= 6:
        ch = Db4
        bass_root = N('Db',3)
    else:
        ch = gc(CHORUS_CHORDS, ci, i + 8)
        bass_root = CHORUS_BASS[ci]

    power_chord(bt(b + i), bass_root + 24 if i < 6 else N('Db',3) + 24, vel=73,
                pattern='chorus', bar_num=i + 8)
    synth_arp(bt(b + i), ch if isinstance(ch, list) and isinstance(ch[0], int) else gc(CHORUS_CHORDS, ci, i+8),
              vel=42, bar_num=i + 52)
    driving_bass(bt(b + i), bass_root, vel=62, bar_num=i + 52,
                 next_root=CHORUS_BASS[next_ci] if i < 6 else N('F',2))
    full_drums(bt(b + i), 'chorus', bar_num=i + 52)
    if i % 2 == 0:
        synth_riff(bt(b + i), vel=56, bar_num=i + 52)
    if i % 4 == 0:
        pad_swell(bt(b + i), gc(CHORUS_CHORDS, ci, i+8), vel=40, bars=2, bar_num=i + 8)

# Chorus 2 melody — same held-note approach
for pi, phrase in enumerate(ch_mel):
    voice(bt(b + pi * 2), phrase, vel=66, bar_num=pi + 52)

b = 60

# --- INSTRUMENTAL BREAK (8 bars) — Call and response, then silence ---
full_drums(bt(b), 'crash', bar_num=60)
for i in range(8):
    ci = (i // 2) % 4
    next_ci = ((i + 2) // 2) % 4
    ch = gc(BREAK_CHORDS, ci, i)

    # Guitar and synth alternate: odd bars = muted guitar, even bars = synth riff
    if i % 2 == 0:
        synth_riff(bt(b + i), vel=60, bar_num=i + 60)
    power_chord(bt(b + i), BREAK_BASS[ci] + 24, vel=65,
                pattern='muted' if i % 2 == 1 else 'chorus', bar_num=i + 60)

    synth_arp(bt(b + i), ch, vel=40, bar_num=i + 60)
    driving_bass(bt(b + i), BREAK_BASS[ci], vel=58, bar_num=i + 60, next_root=BREAK_BASS[next_ci])
    full_drums(bt(b + i), 'chorus', bar_num=i + 60)

# Solo with vibrato
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
        if dur >= HALF:
            for step in range(dur // SIXTEENTH):
                bend_val = int(250 * math.sin(step * 0.9))
                E.pitch_bend(2, bend_val, h_time(t + step * SIXTEENTH, 3))
            E.pitch_bend(2, 0, t + dur)
        E.note(2, note, v, t, dur - random.randint(15, 30), time_amount=8, vel_amount=5)
        prev_n = note
    t += dur

b = 68

# --- ONE BAR OF SILENCE + MODULATION PREP ---
# Piano plays Db7 (V7 of Gb) — the dominant 7th that resolves to Gb
for note in Db4_7:
    E.note(0, note, 55, bt(b), BAR4 - 60, time_amount=8, vel_amount=4)
# Also a higher voicing for fullness
for note in Db4_7:
    E.note(0, note + 12, 45, bt(b), BAR4 - 60, time_amount=10, vel_amount=4)

b = 69

# --- FINAL CHORUS (8 bars) — MODULATED TO Gb MAJOR ---
full_drums(bt(b), 'crash', bar_num=69)
for i in range(8):
    ci = (i // 2) % 4
    next_ci = ((i + 2) // 2) % 4
    ch = gc(FINAL_CHORDS, ci, i)

    # Power chords in Gb now
    power_chord(bt(b + i), FINAL_BASS[ci] + 24, vel=78, pattern='chorus', bar_num=i + 16)

    # Synth riff transposed to Gb!
    if i % 2 == 0:
        synth_riff(bt(b + i), vel=60, bar_num=i + 69, key='Gb')

    synth_arp(bt(b + i), ch, vel=44, bar_num=i + 69)
    driving_bass(bt(b + i), FINAL_BASS[ci], vel=66, bar_num=i + 69, next_root=FINAL_BASS[next_ci])
    full_drums(bt(b + i), 'chorus', bar_num=i + 69)
    if i % 4 == 0:
        pad_swell(bt(b + i), ch, vel=45, bars=2, bar_num=i + 16)

# Chorus melody — now in Gb (everything up a half step), held-note approach transposed
ch_mel_gb = [
    [(N('Db',6), WHOLE),
     (N('B',5), HALF), (N('Bb',5), SIXTEENTH), (N('B',5), SIXTEENTH),
     (N('Bb',5), SIXTEENTH), (N('Ab',5), SIXTEENTH), (N('Bb',5), QUARTER+EIGHTH), (N('Gb',5), EIGHTH)],
    [(N('B',5), HALF+QUARTER), (N('Bb',5), QUARTER),
     (N('Gb',5), HALF), (None, HALF)],
    [(N('Db',6), WHOLE),
     (N('Eb',6), QUARTER), (N('Db',6), SIXTEENTH), (N('B',5), SIXTEENTH),
     (N('Bb',5), SIXTEENTH), (N('Ab',5), SIXTEENTH), (N('Bb',5), HALF)],
    [(N('B',5), QUARTER), (N('Bb',5), QUARTER+EIGHTH), (N('Ab',5), EIGHTH),
     (N('Gb',5), HALF+QUARTER), (None, QUARTER)],
]
for pi, phrase in enumerate(ch_mel_gb):
    voice(bt(b + pi * 2), phrase, vel=70, bar_num=pi + 69)

b = 77

# --- OUTRO (8 bars) — Gb major riff fading ---
for i in range(8):
    vel_fade = max(25, 58 - i * 5)
    if i < 6:
        synth_riff(bt(b + i), vel=max(30, 53 - i * 5), bar_num=i + 77, key='Gb')
    if i < 4:
        driving_bass(bt(b + i), FINAL_BASS[i % 4], vel=vel_fade, bar_num=i + 77)
    if i < 6:
        full_drums(bt(b + i), 'verse', bar_num=i + 77)
    synth_arp(bt(b + i), gc(FINAL_CHORDS, i % 4, i), vel=max(18, 33 - i * 3), bar_num=i + 77)

    if i >= 6:
        pad_swell(bt(b + i), Gb4, vel=max(15, 28 - i * 3), bars=1, bar_num=i + 77)


# ============================================================
# OUTPUT
# ============================================================

build_midi(E, 'The Machinery of Sunlight', bpm=92, total_bars=85,
           channel_names={
               0: 'Piano', 1: 'Synth Pad', 2: 'Synth Lead', 3: 'Clean Guitar',
               4: 'Distorted Guitar', 5: 'Organ', 6: 'Bass', 7: 'Strings',
               8: 'Vocal Melody', 9: 'Drums',
           },
           output_path='/home/user/music/compositions/v5/02_the_machinery_of_sunlight.mid')
