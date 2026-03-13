#!/usr/bin/env python3
"""
Song 1 v5: "Dial Tone Lullaby"
Key: C major | Tempo: 72 BPM | 4/4 | ~4:30

v5 songwriter notes:
Building on v4's arrangement. This version addresses four targeted issues:

1. VERSE 1 MELODY bars 12-13: The falling 6th G->B was a direct drop.
   Now adds passing tone: G->D->B (step then skip) for intervallic interest.
2. CHORUS DRUMS bars 26,28,30: Ghost snare vel=15 on "and" of beat 2
   in those bars for syncopated rhythmic tension.
3. BRIDGE BASS bars 56-63: Chromatic passing tones on beat 4 of each bar.
   Dm bar: D->Db walkdown. Bb bar: Bb->A walkdown. Ab bar: Ab->G walkdown.
   Earns each borrowed chord transition.
4. VERSE 2 bars 36-39: Drop synth pad entirely in bars 38-39.
   Let drums/bass carry alone. Return pad bar 40 with sudden swell (vel jump +15).
   Creates textural breathing room.
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from humanize import *

E = EventList()

def bt(bar_num):
    return bar_num * BAR4


# ============================================================
# CHORD VOICINGS — richer and more varied than v2
# ============================================================

# Verse: C - Am - F - G  (primary)
# Verse alt (bars 5-8 of each 8-bar block): C - Am - Dm - G
VERSE_CHORDS_A = [
    [make_chord(N('C',4), 'major'), make_chord(N('C',4), 'add9'), make_chord(N('C',4), 'sus2')],
    [make_chord(N('A',3), 'minor'), make_chord(N('A',3), 'min7'), [N('A',3), N('C',4), N('E',4), N('G',4)]],
    [make_chord(N('F',3), 'major'), make_chord(N('F',3), 'add9'), [N('F',3), N('A',3), N('C',4)]],
    [make_chord(N('G',3), 'major'), make_chord(N('G',3), 'sus4'), make_chord(N('G',3), 'add9')],
]
VERSE_CHORDS_B = [
    [make_chord(N('C',4), 'major'), make_chord(N('C',4), 'sus2')],
    [make_chord(N('A',3), 'minor'), [N('A',3), N('E',4), N('A',4)]],  # open Am voicing
    [make_chord(N('D',4), 'minor'), make_chord(N('D',4), 'min7')],     # Dm instead of F
    [make_chord(N('G',3), 'major'), make_chord(N('G',3), 'sus4')],
]
VERSE_BASS_A = [N('C',2), N('A',1), N('F',2), N('G',2)]
VERSE_BASS_B = [N('C',2), N('A',1), N('D',2), N('G',2)]

# Chorus: Am - F - C - G, but bar 7 substitutes Ab for the "Grandaddy surprise"
CHORUS_CHORDS = [
    [make_chord(N('A',3), 'minor'), make_chord(N('A',3), 'min7')],
    [make_chord(N('F',3), 'major'), make_chord(N('F',3), 'add9')],
    [make_chord(N('C',4), 'major'), make_chord(N('C',4), 'add9')],
    [make_chord(N('G',3), 'major'), make_chord(N('G',3), 'sus4')],
]
CHORUS_BASS = [N('A',1), N('F',2), N('C',2), N('G',2)]

# PAD INVERSIONS for chorus (fix #4) — first inversions, voiced higher
CHORUS_PAD_INVERSIONS = [
    # Am root = A-C-E -> first inversion C-E-A (voiced higher)
    [[N('C',4), N('E',4), N('A',4)], [N('C',4), N('E',4), N('G',4), N('A',4)]],
    # F root = F-A-C -> first inversion A-C-F
    [[N('A',3), N('C',4), N('F',4)], [N('A',3), N('C',4), N('F',4), N('G',4)]],
    # C root = C-E-G -> first inversion E-G-C
    [[N('E',4), N('G',4), N('C',5)], [N('E',4), N('G',4), N('B',4), N('C',5)]],
    # G root = G-B-D -> first inversion B-D-G
    [[N('B',3), N('D',4), N('G',4)], [N('B',3), N('D',4), N('F#',4), N('G',4)]],
]

# The surprise chord — Ab major, borrowed from C minor
AB_CHORD = [[make_chord(N('Ab',3), 'major'), [N('Ab',3), N('C',4), N('Eb',4)]]]
# Ab pad inversion: C-Eb-Ab
AB_PAD_INV = [[N('C',4), N('Eb',4), N('Ab',4)]]

# Bridge: Dm - Bb - Ab - G  (two borrowed chords!)
BRIDGE_CHORDS = [
    [make_chord(N('D',4), 'minor'), make_chord(N('D',4), 'min7')],
    [make_chord(N('Bb',3), 'major'), [N('Bb',3), N('D',4), N('F',4)]],   # borrowed from C minor
    [make_chord(N('Ab',3), 'major'), [N('Ab',3), N('C',4), N('Eb',4)]],   # borrowed from C minor
    [make_chord(N('G',3), 'major'), make_chord(N('G',3), 'sus4')],
]
BRIDGE_BASS = [N('D',2), N('Bb',1), N('Ab',1), N('G',2)]

# Outro uses verse chords but ends on Cmaj7
CMAJ7 = [N('C',4), N('E',4), N('G',4), N('B',4)]


def gv(voicings, ci, bar):
    opts = voicings[ci]
    return opts[bar % len(opts)]


# ============================================================
# INSTRUMENT FUNCTIONS
# ============================================================

def piano_arpeggio(bar_start, chord_notes, vel=50, bar_num=0):
    """Piano arpeggios with sustain pedal, varied patterns, grace notes."""
    notes = list(chord_notes) + [chord_notes[0] + 12]
    patterns = [
        [0,1,2,3,2,1,0,3],    # wave
        [0,2,1,3,0,2,3,1],    # skip
        [3,2,1,0,1,2,3,2],    # descending wave
        [0,1,0,2,1,2,3,2],    # tentative
        [0,3,1,2,0,3,2,1],    # wide
        [0,1,2,1,0,2,3,2],    # gentle sway
    ]
    pat = patterns[bar_num % len(patterns)]

    E.cc(0, 64, 100, h_time(bar_start, 3))
    E.cc(0, 64, 0, h_time(bar_start + BAR4 - 30, 3))

    bvel = breathing_vel(vel, bar_num, cycle_bars=8, depth=5)

    for i in range(8):
        idx = pat[i] % len(notes)
        note = notes[idx]
        t = bar_start + i * EIGHTH + swing_offset(i, 12)
        beat = i // 2
        v = bvel + accent_beat(beat)
        v = v if i % 2 == 0 else v - 7

        # Grace note every ~6 bars on beat 1
        if i == 0 and bar_num % 6 == 3:
            grace = note - 2 if note - 2 >= 48 else note + 2
            E.note(0, grace, v - 15, t - SIXTEENTH, SIXTEENTH - 5, time_amount=5)

        E.note(0, note, v, t, EIGHTH - random.randint(15, 30), time_amount=6, vel_amount=3)


def piano_whole_chord(bar_start, chord_notes, vel=42):
    """Sustained whole chord with pedal — for moments of stillness."""
    E.cc(0, 64, 110, h_time(bar_start, 3))
    for n in chord_notes:
        E.note(0, n, vel + random.randint(-3, 3), bar_start, BAR4 - 30,
               time_amount=12, vel_amount=5)
    E.cc(0, 64, 0, h_time(bar_start + BAR4 - 30, 3))


def piano_bridge_chromatic(bar_start, chord_notes, chromatic_top_from, chromatic_top_to, vel=43, bar_num=0):
    """Bridge piano with flowing eighth-note arpeggios and chromatic
    voice-leading in the top note. On beat 4 the top note walks chromatically
    toward the next chord's top note."""
    notes = list(chord_notes) + [chord_notes[0] + 12]
    E.cc(0, 64, 110, h_time(bar_start, 3))

    # Eighth-note arpeggio pattern: flowing up and back
    # 8 eighths per bar, pattern indexes into notes[]
    pattern = [0, 1, 2, 3, 2, 1, 0, 2]

    for j in range(8):
        t = bar_start + j * EIGHTH + swing_offset(j, 10)
        beat = j // 2
        v = breathing_vel(vel, bar_num + j, 4, 5)
        v = v + accent_beat(beat) + (0 if j % 2 == 0 else -6)

        if j < 6:
            # Normal arpeggio notes
            idx = pattern[j] % len(notes)
            note = notes[idx]
        elif j == 6:
            # Beat 4 first eighth: still the original top note
            note = chromatic_top_from
        else:
            # Beat 4 second eighth: chromatic approach to next chord's top
            note = chromatic_top_to

        E.note(0, note, v, t, EIGHTH - 20, time_amount=12, vel_amount=5)

    E.cc(0, 64, 0, h_time(bar_start + BAR4 - 30, 3))


def synth_pad(bar_start, chord_notes, vel=40, bars=2, bar_num=0):
    """Synth pad with CC11 expression swell."""
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


def synth_lead(bar_start, phrase, vel=55, bar_num=0):
    """Synth lead with contour dynamics and vibrato on long notes."""
    t = bar_start
    for i, (note, dur) in enumerate(phrase):
        if note is not None:
            pitch_boost = max(0, (note - 60) // 4)
            v = breathing_vel(vel + pitch_boost, bar_num + i, 4, 6)
            actual_dur = dur - random.randint(20, 40)
            if dur >= HALF:
                for step in range(0, dur // SIXTEENTH, 2):
                    bend_t = t + step * SIXTEENTH
                    bend_val = int(200 * math.sin(step * 0.8))
                    E.pitch_bend(2, bend_val, h_time(bend_t, 3))
                E.pitch_bend(2, 0, t + dur)
            E.note(2, note, v, t, actual_dur, time_amount=8, vel_amount=4)
        t += dur


def organ(bar_start, chord_notes, vel=32, bars=4, bar_num=0):
    """Organ with analog pitch wobble."""
    bvel = breathing_vel(vel, bar_num, 6, 3)
    for note in chord_notes:
        E.note(5, note, bvel, bar_start, BAR4 * bars - 30, time_amount=12, vel_amount=4)
    for step in range(bars * 8):
        t = bar_start + step * EIGHTH
        bend = int(80 * math.sin(step * 0.3))
        E.pitch_bend(5, bend, h_time(t, 3))
    E.pitch_bend(5, 0, bar_start + BAR4 * bars)


def strings_swell(bar_start, chord_notes, vel=30, bars=4, bar_num=0):
    """Strings with expression swell — saved for the big moments."""
    steps = bars * 8
    for step in range(steps):
        t = bar_start + step * EIGHTH
        swell = math.sin((step / steps) * math.pi) ** 0.8
        v = max(30, min(120, int(40 + 80 * swell)))
        E.cc(7, 11, v, h_time(t, 3))
    bvel = breathing_vel(vel, bar_num, 8, 5)
    for n in [nn + 12 for nn in chord_notes]:
        E.note(7, n, bvel, bar_start, BAR4 * bars - 30, time_amount=12, vel_amount=5)


def bass(bar_start, root, vel=48, bar_num=0, pattern='whole', next_root=None):
    """Bass with chromatic approaches and varied patterns."""
    bvel = breathing_vel(vel, bar_num, 8, 4)
    if pattern == 'whole':
        E.note(6, root, bvel, bar_start, BAR4 - 40, time_amount=10, vel_amount=4)
        if next_root is not None and bar_num % 3 == 2:
            approach = next_root - 1 if next_root > root else next_root + 1
            E.note(6, approach, bvel - 8, bar_start + HALF + QUARTER, QUARTER - 20,
                   time_amount=8, vel_amount=3)
    elif pattern == 'half':
        E.note(6, root, bvel, bar_start, HALF - 30, time_amount=8, vel_amount=4)
        fifth = root + 7
        E.note(6, fifth, bvel - 5, bar_start + HALF, HALF - 30, time_amount=10, vel_amount=3)
        if bar_num % 4 == 3 and next_root is not None:
            E.note(6, next_root - 2, bvel - 10, bar_start + HALF + QUARTER, QUARTER - 20,
                   time_amount=6, vel_amount=3)
    elif pattern == 'melodic':
        E.note(6, root, bvel, bar_start, QUARTER - 20, time_amount=8)
        E.note(6, root + 4, bvel - 5, bar_start + QUARTER, QUARTER - 20, time_amount=10)
        E.note(6, root + 7, bvel - 3, bar_start + HALF, QUARTER - 20, time_amount=8)
        target = next_root if next_root else root
        approach = target - 1 if random.random() > 0.5 else target + 2
        E.note(6, approach, bvel - 8, bar_start + HALF + QUARTER, QUARTER - 20, time_amount=10)
    elif pattern == 'chromatic_walk':
        E.note(6, root, bvel, bar_start, BAR4 - 40, time_amount=10, vel_amount=4)


def bass_chromatic_walk(bar_start, walk_notes, vel=38, bar_num=0):
    """Bass plays explicit quarter-note chromatic walk pattern."""
    bvel = breathing_vel(vel, bar_num, 8, 4)
    for i, note in enumerate(walk_notes):
        t = bar_start + i * QUARTER
        v = bvel + accent_beat(i)
        E.note(6, note, v, t, QUARTER - 30, time_amount=8, vel_amount=4)


def bass_with_chromatic_passing(bar_start, root, passing_tone, vel=38, bar_num=0, next_root=None):
    """FIX #3 (v5): Bass whole note with chromatic passing tone on beat 4.
    Plays root for beats 1-3, then passing_tone on beat 4 as a walkdown."""
    bvel = breathing_vel(vel, bar_num, 8, 4)
    # Root note for beats 1-3
    E.note(6, root, bvel, bar_start, HALF + QUARTER - 30, time_amount=10, vel_amount=4)
    # Chromatic passing tone on beat 4
    E.note(6, passing_tone, bvel - 5, bar_start + HALF + QUARTER, QUARTER - 30,
           time_amount=8, vel_amount=3)


def drums(bar_start, pattern='minimal', bar_num=0):
    """Drums with per-bar variation and ghost notes."""
    ch = 9
    kick, snare, hh_c, hh_o, rim, crash = 36, 38, 42, 46, 37, 49
    bvel_k = breathing_vel(48, bar_num, 8, 4)

    if pattern == 'minimal':
        E.note(ch, kick, bvel_k, bar_start, QUARTER, time_amount=6, vel_amount=4)
        for i in range(4):
            t = bar_start + i * QUARTER
            v = 22 + accent_beat(i) + random.randint(-3, 3)
            if i == 0: continue
            E.note(ch, hh_c, v, t, EIGHTH, time_amount=8, vel_amount=3)
        if bar_num % 3 == 1:
            E.note(ch, snare, 15, bar_start + QUARTER + EIGHTH, EIGHTH, time_amount=12)

    elif pattern == 'verse':
        E.note(ch, kick, bvel_k, bar_start, QUARTER, time_amount=5, vel_amount=4)
        E.note(ch, snare, h_vel(28, 4), bar_start + QUARTER, QUARTER, time_amount=8, vel_amount=5)
        E.note(ch, kick, bvel_k - 5, bar_start + HALF, QUARTER, time_amount=6, vel_amount=4)
        E.note(ch, snare, h_vel(28, 4), bar_start + HALF + QUARTER, QUARTER, time_amount=8, vel_amount=5)
        for i in range(8):
            t = bar_start + i * EIGHTH + swing_offset(i, 10)
            v = 20 + (4 if i % 2 == 0 else 0) + random.randint(-3, 3)
            E.note(ch, hh_c, v, t, EIGHTH, time_amount=6, vel_amount=2)
        if bar_num % 2 == 0:
            E.note(ch, snare, 12, bar_start + QUARTER + EIGHTH + swing_offset(1, 10),
                   EIGHTH, time_amount=12, vel_amount=3)
        if bar_num % 4 == 3:
            E.note(ch, hh_o, 25, bar_start + HALF + QUARTER, EIGHTH, time_amount=8)

    elif pattern == 'verse_energetic':
        E.note(ch, kick, bvel_k, bar_start, QUARTER, time_amount=5, vel_amount=4)
        E.note(ch, snare, h_vel(28, 4), bar_start + QUARTER, QUARTER, time_amount=8, vel_amount=5)
        E.note(ch, kick, bvel_k - 5, bar_start + HALF, QUARTER, time_amount=6, vel_amount=4)
        E.note(ch, snare, h_vel(28, 4), bar_start + HALF + QUARTER, QUARTER, time_amount=8, vel_amount=5)
        # Added snare on "and" of 3 (beat 2.5 = half + eighth)
        E.note(ch, snare, h_vel(22, 3), bar_start + HALF + EIGHTH + swing_offset(1, 10),
               EIGHTH, time_amount=8, vel_amount=4)
        for i in range(8):
            t = bar_start + i * EIGHTH + swing_offset(i, 10)
            v = 22 + (5 if i % 2 == 0 else 0) + random.randint(-3, 3)
            E.note(ch, hh_c, v, t, EIGHTH, time_amount=6, vel_amount=2)
        if bar_num % 2 == 0:
            E.note(ch, snare, 12, bar_start + QUARTER + EIGHTH + swing_offset(1, 10),
                   EIGHTH, time_amount=12, vel_amount=3)

    elif pattern == 'chorus':
        E.note(ch, kick, bvel_k + 5, bar_start, QUARTER, time_amount=5, vel_amount=4)
        E.note(ch, snare, h_vel(35, 5), bar_start + QUARTER, QUARTER, time_amount=7, vel_amount=5)
        E.note(ch, kick, bvel_k, bar_start + HALF, QUARTER, time_amount=6, vel_amount=4)
        E.note(ch, snare, h_vel(35, 5), bar_start + HALF + QUARTER, QUARTER, time_amount=7, vel_amount=5)
        for i in range(8):
            t = bar_start + i * EIGHTH + swing_offset(i, 8)
            v = 26 + (5 if i % 2 == 0 else 0) + random.randint(-3, 3)
            E.note(ch, hh_c, v, t, EIGHTH, time_amount=5, vel_amount=2)
        if bar_num % 2 == 1:
            E.note(ch, kick, bvel_k - 20, bar_start + QUARTER + EIGHTH, EIGHTH, time_amount=10)

    elif pattern == 'fill':
        E.note(ch, kick, bvel_k + 8, bar_start, QUARTER, time_amount=4)
        E.note(ch, snare, 30, bar_start + QUARTER, EIGHTH, time_amount=8)
        E.note(ch, snare, 35, bar_start + QUARTER + EIGHTH, EIGHTH, time_amount=10)
        E.note(ch, snare, 40, bar_start + HALF, EIGHTH, time_amount=8)
        E.note(ch, snare, 45, bar_start + HALF + EIGHTH, EIGHTH, time_amount=6)
        E.note(ch, hh_o, 50, bar_start + HALF + QUARTER, QUARTER, time_amount=5)

    elif pattern == 'crash':
        E.note(ch, crash, 65, bar_start, QUARTER, time_amount=3)
        E.note(ch, kick, 60, bar_start, QUARTER, time_amount=3)


def drums_chorus_with_ghost(bar_start, bar_num=0):
    """FIX #2 (v5): Chorus drums with ghost snare vel=15 on 'and' of beat 2.
    Used on specific bars for syncopated rhythmic tension."""
    ch = 9
    kick, snare, hh_c = 36, 38, 42
    bvel_k = breathing_vel(48, bar_num, 8, 4)

    # Standard chorus pattern
    E.note(ch, kick, bvel_k + 5, bar_start, QUARTER, time_amount=5, vel_amount=4)
    E.note(ch, snare, h_vel(35, 5), bar_start + QUARTER, QUARTER, time_amount=7, vel_amount=5)
    E.note(ch, kick, bvel_k, bar_start + HALF, QUARTER, time_amount=6, vel_amount=4)
    E.note(ch, snare, h_vel(35, 5), bar_start + HALF + QUARTER, QUARTER, time_amount=7, vel_amount=5)
    for i in range(8):
        t = bar_start + i * EIGHTH + swing_offset(i, 8)
        v = 26 + (5 if i % 2 == 0 else 0) + random.randint(-3, 3)
        E.note(ch, hh_c, v, t, EIGHTH, time_amount=5, vel_amount=2)
    if bar_num % 2 == 1:
        E.note(ch, kick, bvel_k - 20, bar_start + QUARTER + EIGHTH, EIGHTH, time_amount=10)

    # FIX #2: Ghost snare on "and" of beat 2 (= beat 2 + eighth = QUARTER + EIGHTH)
    # "and" of beat 2 in 0-indexed eighths is position 3
    E.note(ch, snare, 15, bar_start + QUARTER + EIGHTH + swing_offset(3, 8),
           EIGHTH, time_amount=12, vel_amount=2)


def voice(bar_start, phrase, vel=52, bar_num=0):
    """Vocal melody with contour dynamics, grace notes, anticipations."""
    t = bar_start
    prev_note = None
    for i, (note, dur) in enumerate(phrase):
        if note is not None:
            v = vel
            if prev_note is not None:
                interval = note - prev_note
                if interval > 3: v += 4
                elif interval < -3: v -= 2
            v = breathing_vel(v, bar_num + i, 6, 5)

            anticipation = 0
            if i > 0 and random.random() < 0.15 and dur <= HALF:
                anticipation = -SIXTEENTH

            if prev_note is not None and abs(note - prev_note) >= 4 and random.random() < 0.3:
                grace = prev_note + (1 if note > prev_note else -1)
                E.note(8, grace, v - 12, t + anticipation - SIXTEENTH, SIXTEENTH - 5,
                       time_amount=10, vel_amount=3)

            actual_dur = dur - random.randint(25, 45)
            E.note(8, note, v, t + anticipation, actual_dur, time_amount=10, vel_amount=5)
            prev_note = note
        t += dur


# ============================================================
# BUILD THE SONG
# ============================================================

b = 0

# === INTRO (8 bars) — Solo piano, C-Am-F-G ===
# Start quieter than v2. Let the piano find its footing.
for i in range(8):
    ci = (i // 2) % 4
    vel = 35 + i * 2  # very gentle crescendo
    piano_arpeggio(bt(i), gv(VERSE_CHORDS_A, ci, i), vel=vel, bar_num=i)

b = 8

# === VERSE 1 (16 bars) ===
# First 8 bars: C-Am-F-G (the safe progression, establishing home)
# Second 8 bars: C-Am-Dm-G (introduce Dm — first hint of shadow)
for i in range(16):
    is_second_half = i >= 8
    chords = VERSE_CHORDS_B if is_second_half else VERSE_CHORDS_A
    bass_notes = VERSE_BASS_B if is_second_half else VERSE_BASS_A
    ci = (i // 2) % 4
    next_ci = ((i + 1) // 2) % 4
    voicing = gv(chords, ci, i)

    piano_arpeggio(bt(b + i), voicing, vel=48, bar_num=i)

    # Pad enters bar 4 (as before, but with Am voicings now)
    if i >= 4 and i % 2 == 0:
        synth_pad(bt(b + i), gv(chords, ci, i + 1), vel=30 + i, bars=2, bar_num=i)

    # Bass enters bar 8
    # Bars 8-11 get chromatic walking bass instead of whole notes
    if i >= 8:
        if i == 8:
            # Bar 8 (C chord): C whole note
            bass(bt(b + i), bass_notes[ci], vel=38, bar_num=i, pattern='whole')
        elif i == 9:
            # Bar 9 (Am chord): chromatic walk C-B-A (quarters)
            bass_chromatic_walk(bt(b + i), [N('C',2), N('B',1), N('A',1), N('A',1)],
                                vel=38, bar_num=i)
        elif i == 10:
            # Bar 10 (F/Dm chord): chromatic walk A-G-F (quarters)
            bass_chromatic_walk(bt(b + i), [N('A',1), N('G',2), N('F',2), N('F',2)],
                                vel=38, bar_num=i)
        elif i == 11:
            # Bar 11 (G chord): chromatic walk F-F#-G (quarters)
            bass_chromatic_walk(bt(b + i), [N('F',2), N('F#',2), N('G',2), N('G',2)],
                                vel=38, bar_num=i)
        else:
            # Bars 12+: melodic pattern as in v3
            next_bass = bass_notes[next_ci] if i < 15 else VERSE_BASS_A[0]
            pattern = 'melodic' if i >= 12 else 'whole'
            bass(bt(b + i), bass_notes[ci], vel=38, bar_num=i, pattern=pattern, next_root=next_bass)

    # Drums — sparse at first
    if i >= 12:
        if i == 15:
            drums(bt(b + i), 'fill', bar_num=i)
        else:
            drums(bt(b + i), 'minimal', bar_num=i)

# FIX #1 (v5): VERSE 1 MELODY — bars 12-13 hook now G->D->B (passing tone)
# instead of direct G->B falling 6th. Step (G->D) then skip (D->B) for
# intervallic interest in the hook itself.
v1_phrases = [
    # Phrase 1 (bars 8-9): G5 then dramatic DROP to C4, climb to E4
    [(N('G',5), QUARTER), (N('C',4), HALF+EIGHTH), (N('E',4), EIGHTH), (N('G',4), HALF), (None, HALF)],
    # Phrase 2 (bars 10-11): Steps up from the landed position, reaches for A
    [(64, QUARTER), (65, HALF), (67, QUARTER), (69, HALF), (67, HALF)],
    # Phrase 3 (bars 12-13): THE HOOK — G steps to D (passing tone) then skips to B, resolves to C
    # v4 was: G(67) -> B(59) direct. v5: G(67) -> D(62) -> B(59) -> C(60)
    [(67, QUARTER), (62, QUARTER), (59, HALF+EIGHTH), (60, EIGHTH+HALF), (None, HALF)],
    # Phrase 4 (bars 14-15): Settling phrase, ends on E (3rd — unresolved)
    [(65, QUARTER), (64, QUARTER+EIGHTH), (62, EIGHTH), (60, HALF), (64, HALF)],
    # Phrase 5 (bars 16-17): Restates opening leap but smaller — G5 to E4
    [(N('G',5), QUARTER), (N('E',4), HALF+EIGHTH), (N('F',4), EIGHTH), (N('D',4), HALF), (None, HALF)],
    # Phrase 6 (bars 18-19): Over the Dm chord now — note how it darkens
    [(65, QUARTER), (62, QUARTER), (60, HALF), (62, HALF), (None, HALF)],
    # Phrase 7 (bars 20-21): Building back to G
    [(64, QUARTER), (65, QUARTER), (67, HALF), (72, HALF), (None, HALF)],
    # Phrase 8 (bars 22-23): The falling 6th again — C down to E (same interval)
    [(72, HALF), (64, HALF+EIGHTH), (65, EIGHTH+HALF+QUARTER), (None, QUARTER)],
]
for pi, phrase in enumerate(v1_phrases):
    voice(bt(b + pi * 2), phrase, vel=47 + pi, bar_num=pi)

b = 24

# === CHORUS 1 (8 bars) — Am-F-C-G, with Ab surprise in bar 7 ===
# FIX #2 (v5): Ghost snare on "and" of beat 2 in bars 26, 28, 30
# Absolute bars 26,28,30 = chorus bars i=2,4,6 (b=24, so i = abs_bar - 24)
GHOST_SNARE_CHORUS_BARS = {2, 4, 6}  # relative to chorus start (bar 24)

for i in range(8):
    ci = (i // 2) % 4
    next_ci = ((i + 2) // 2) % 4

    # Bar 6-7: substitute Ab for G (the borrowed chord surprise)
    if i >= 6:
        voicing = gv(AB_CHORD, 0, i)
        bass_root = N('Ab',1)
        pad_voicing = AB_PAD_INV[0]
    else:
        voicing = gv(CHORUS_CHORDS, ci, i)
        bass_root = CHORUS_BASS[ci]
        pad_voicing = gv(CHORUS_PAD_INVERSIONS, ci, i)

    piano_arpeggio(bt(b + i), voicing, vel=55, bar_num=i + 8)

    # Pad plays INVERSIONS, not same voicing as piano
    if i % 2 == 0:
        synth_pad(bt(b + i), pad_voicing, vel=45, bars=2, bar_num=i)

    next_bass = CHORUS_BASS[next_ci] if i < 6 else N('Ab',1)
    bass(bt(b + i), bass_root, vel=45, bar_num=i, pattern='half', next_root=next_bass)

    # FIX #2: Use ghost snare variant on bars 26,28,30 (i=2,4,6)
    if i in GHOST_SNARE_CHORUS_BARS:
        drums_chorus_with_ghost(bt(b + i), bar_num=i)
    else:
        drums(bt(b + i), 'chorus', bar_num=i)

# CHORUS 1 MELODY — the falling 6th IS the hook, right at the top
chorus_phrases = [
    # Phrase 1 (bars 24-25): THE HOOK front and center — C drops to E
    [(72, QUARTER), (64, HALF+EIGHTH), (65, EIGHTH), (67, HALF), (None, HALF)],
    # Phrase 2 (bars 26-27): Climbs hopefully, reaches for A
    [(67, QUARTER), (69, HALF), (72, QUARTER), (69, HALF), (None, HALF)],
    # Phrase 3 (bars 28-29): The falling 6th again, higher
    [(72, HALF), (74, HALF+EIGHTH), (76, EIGHTH+QUARTER), (None, QUARTER)],
    # Phrase 4 (bars 30-31): Over the Ab chord — this note (G) against Ab is magical
    [(76, QUARTER), (74, QUARTER), (72, HALF+EIGHTH), (67, EIGHTH+HALF+QUARTER), (None, QUARTER)],
]
for pi, phrase in enumerate(chorus_phrases):
    voice(bt(b + pi * 2), phrase, vel=55, bar_num=pi + 16)

# TRUE counter-melody in chorus 1 — contrary motion counterpoint
lead_ch1 = [
    # Phrase 1: Vocal descends C->E (falling 6th). Synth RISES E4->G4->B4->C5 (contrary!)
    [(N('E',4), QUARTER), (N('G',4), QUARTER), (N('B',4), QUARTER), (N('C',5), QUARTER),
     (N('B',4), SIXTEENTH), (N('C',5), SIXTEENTH), (N('D',5), SIXTEENTH), (N('C',5), SIXTEENTH),
     (N('B',4), SIXTEENTH), (N('A',4), SIXTEENTH), (N('G',4), SIXTEENTH), (N('A',4), SIXTEENTH),
     (None, HALF)],
    # Phrase 2: Vocal climbs G->A. Synth descends D5->C5->B4->A4 (contrary)
    [(N('D',5), QUARTER), (N('C',5), QUARTER+EIGHTH), (N('B',4), EIGHTH),
     (N('A',4), QUARTER),
     (N('G',4), SIXTEENTH), (N('A',4), SIXTEENTH), (N('B',4), SIXTEENTH), (N('A',4), SIXTEENTH),
     (None, HALF)],
    # Phrase 3: Vocal rises C->D->E. Synth DESCENDS from G5->F5->E5 (contrary)
    [(N('G',5), QUARTER), (N('F',5), QUARTER+EIGHTH), (N('E',5), EIGHTH),
     (N('D',5), QUARTER), (None, QUARTER+HALF)],
    # Phrase 4: Vocal descends E->G4. Synth rises G4->A4->B4->C5 under the Ab chord
    [(N('G',4), QUARTER), (N('A',4), QUARTER), (N('B',4), HALF+EIGHTH),
     (N('C',5), EIGHTH),
     (N('B',4), SIXTEENTH), (N('C',5), SIXTEENTH), (N('B',4), SIXTEENTH), (N('A',4), SIXTEENTH),
     (None, QUARTER)],
]
for pi, phrase in enumerate(lead_ch1):
    synth_lead(bt(b + pi * 2), phrase, vel=38, bar_num=pi)

b = 32

# === VERSE 2 (16 bars) — Fuller, with organ entering bar 8 ===
# FIX #4 (v5): Drop synth pad in bars 38-39 (i=6,7 relative to verse 2 start).
#   Let drums/bass carry alone. Return pad bar 40 (i=8) with vel jump +15.
# Drums build through verse 2 instead of identical 'verse' pattern.
V2_PAD_DROP_BARS = {6, 7}  # relative bars where pad is dropped (absolute 38-39)
V2_PAD_SWELL_BAR = 8       # relative bar where pad returns with swell (absolute 40)

for i in range(16):
    is_second_half = i >= 8
    chords = VERSE_CHORDS_B if is_second_half else VERSE_CHORDS_A
    bass_notes = VERSE_BASS_B if is_second_half else VERSE_BASS_A
    ci = (i // 2) % 4
    next_ci = ((i + 1) // 2) % 4
    voicing = gv(chords, ci, i + 16)

    piano_arpeggio(bt(b + i), voicing, vel=52, bar_num=i + 16)

    # FIX #4 (v5): Pad logic — skip bars 6-7 (abs 38-39), swell on bar 8 (abs 40)
    if i % 2 == 0:
        if i not in V2_PAD_DROP_BARS:
            pad_vel = 38
            if i == V2_PAD_SWELL_BAR:
                pad_vel = 38 + 15  # sudden swell: vel jump +15
            synth_pad(bt(b + i), gv(chords, ci, i + 3), vel=pad_vel, bars=2, bar_num=i)

    pattern = 'half' if i >= 8 else 'whole'
    bass(bt(b + i), bass_notes[ci], vel=42, bar_num=i, pattern=pattern,
         next_root=bass_notes[next_ci])

    # Drums build across verse 2
    # Bars 0-7 (absolute 32-39): 'minimal'
    # Bars 8-11 (absolute 40-43): 'verse'
    # Bars 12-14 (absolute 44-46): 'verse_energetic'
    # Bar 15 (absolute 47): 'fill' to launch into chorus 2
    if i < 8:
        drums(bt(b + i), 'minimal', bar_num=i + 16)
    elif i < 12:
        drums(bt(b + i), 'verse', bar_num=i + 16)
    elif i < 15:
        drums(bt(b + i), 'verse_energetic', bar_num=i + 16)
    else:
        drums(bt(b + i), 'fill', bar_num=i + 16)

    # ORGAN ENTERS bar 8 of verse 2
    if i >= 8 and i % 4 == 0:
        organ(bt(b + i), gv(chords, ci, i), vel=25, bars=4, bar_num=i)

# Verse 2 melody — ASCENDING where verse 1 descended
v2_phrases = [
    # Phrase 1 (bars 32-33): Start on C5, CLIMB to E5->G5 (opposite of v1's descent)
    [(N('C',5), QUARTER), (N('E',5), QUARTER+EIGHTH), (N('G',5), EIGHTH),
     (N('A',5), HALF), (None, HALF)],
    # Phrase 2 (bars 34-35): Continue high, gently stepping down from the peak
    [(N('G',5), QUARTER), (N('E',5), HALF+EIGHTH), (N('D',5), EIGHTH),
     (N('C',5), HALF), (None, HALF)],
    # Phrase 3 (bars 36-37): THE DARK HOOK — A5 drops to C#4 (minor 6th)
    [(N('A',5), HALF), (N('C#',4), HALF+EIGHTH), (N('D',4), EIGHTH+HALF),
     (None, HALF)],
    # Phrase 4 (bars 38-39): Recovery from the dark drop, climbing again
    [(N('E',4), QUARTER), (N('G',4), QUARTER+EIGHTH), (N('A',4), EIGHTH),
     (N('C',5), HALF), (N('B',4), HALF)],
    # Phrase 5 (bars 40-41): Ascending again — C5 to E5 (echoing phrase 1 shape)
    [(N('C',5), QUARTER), (N('D',5), QUARTER+EIGHTH), (N('E',5), EIGHTH),
     (N('G',5), HALF), (None, HALF)],
    # Phrase 6 (bars 42-43): Over Dm — the ascent turns minor, pulls back
    [(N('F',5), QUARTER), (N('E',5), EIGHTH), (N('D',5), EIGHTH),
     (N('A',4), HALF), (N('B',4), HALF+EIGHTH), (None, QUARTER+EIGHTH)],
    # Phrase 7 (bars 44-45): Building to climax — highest sustained note
    [(N('C',5), QUARTER), (N('E',5), QUARTER), (N('G',5), HALF),
     (N('A',5), HALF), (None, HALF)],
    # Phrase 8 (bars 46-47): The minor 6th hook one more time — A5 to C#4, then resolve up to D
    [(N('A',5), QUARTER), (N('C#',4), HALF+EIGHTH), (N('D',4), EIGHTH),
     (N('E',4), HALF+QUARTER), (None, QUARTER)],
]
for pi, phrase in enumerate(v2_phrases):
    voice(bt(b + pi * 2), phrase, vel=50 + pi, bar_num=pi + 24)

b = 48

# === CHORUS 2 (8 bars) — With organ, new synth counter-melody, Ab surprise again ===
drums(bt(b), 'crash', bar_num=48)
for i in range(8):
    ci = (i // 2) % 4

    if i >= 6:
        voicing = gv(AB_CHORD, 0, i)
        bass_root = N('Ab',1)
        pad_voicing = AB_PAD_INV[0]
    else:
        voicing = gv(CHORUS_CHORDS, ci, i + 8)
        bass_root = CHORUS_BASS[ci]
        pad_voicing = gv(CHORUS_PAD_INVERSIONS, ci, i)

    piano_arpeggio(bt(b + i), voicing, vel=57, bar_num=i + 32)

    # Pad plays inversions
    if i % 2 == 0:
        synth_pad(bt(b + i), pad_voicing, vel=48, bars=2, bar_num=i)

    if i % 4 == 0:
        organ(bt(b + i), voicing, vel=30, bars=4, bar_num=i)

    bass(bt(b + i), bass_root, vel=47, bar_num=i + 8,
         pattern='melodic', next_root=CHORUS_BASS[((i+2)//2) % 4] if i < 6 else N('G',2))

    # FIX #2: Ghost snare on bars 26,28,30 pattern also applies to chorus 2
    # Chorus 2 bars: absolute 48-55, same relative positions i=2,4,6
    if i in GHOST_SNARE_CHORUS_BARS:
        drums_chorus_with_ghost(bt(b + i), bar_num=i + 8)
    else:
        drums(bt(b + i), 'chorus', bar_num=i + 8)

# Same vocal melody as chorus 1 but slightly louder
for pi, phrase in enumerate(chorus_phrases):
    voice(bt(b + pi * 2), phrase, vel=58, bar_num=pi + 32)

# Counter-melody in chorus 2 — more melodic, echoes the falling 6th motif
lead_ch2 = [
    [(76, QUARTER), (74, HALF), (72, QUARTER+EIGHTH), (69, EIGHTH+HALF), (None, HALF)],
    [(72, HALF), (74, QUARTER+EIGHTH), (76, EIGHTH+QUARTER), (74, QUARTER), (72, HALF)],
    [(79, HALF), (77, QUARTER+EIGHTH), (76, EIGHTH), (74, HALF), (None, HALF)],
    [(76, QUARTER), (74, HALF+EIGHTH), (72, EIGHTH), (72, WHOLE)],
]
for pi, phrase in enumerate(lead_ch2):
    synth_lead(bt(b + pi * 2), phrase, vel=44, bar_num=pi + 8)

b = 56

# === BRIDGE (8 bars) — Dm-Bb-Ab-G, the borrowed chords create magic ===
# Piano uses flowing eighth-note patterns with chromatic voice-leading
# FIX #3 (v5): Bass adds chromatic passing tones on beat 4 of each bar:
#   Dm bar: D->Db walkdown
#   Bb bar: Bb->A walkdown
#   Ab bar: Ab->G walkdown
#   G bar: resolves naturally (no chromatic passing tone needed)

for i in range(8):
    ci = (i // 2) % 4
    voicing = gv(BRIDGE_CHORDS, ci, i)

    # Determine chromatic top-note walk for piano
    if ci == 0:  # Dm: top note A4, walks to Ab4
        piano_bridge_chromatic(bt(b + i), voicing, N('A',4), N('Ab',4),
                                vel=43, bar_num=i)
    elif ci == 1:  # Bb: top note F4, walks D to Db
        piano_bridge_chromatic(bt(b + i), voicing, N('D',5), N('Db',5),
                                vel=43, bar_num=i)
    elif ci == 2:  # Ab: top note Eb4, walks Eb5->D5 (approaching G chord)
        piano_bridge_chromatic(bt(b + i), voicing, N('Eb',5), N('D',5),
                                vel=43, bar_num=i)
    else:  # G: resolves naturally, no chromatic walk needed
        piano_bridge_chromatic(bt(b + i), voicing, N('D',4), N('D',4),
                                vel=43, bar_num=i)

    if i % 2 == 0:
        synth_pad(bt(b + i), voicing, vel=34, bars=2, bar_num=i + 40)

    # FIX #3 (v5): Bass with chromatic passing tones on beat 4
    bridge_bass_root = BRIDGE_BASS[(i // 2) % 4]
    if ci == 0:
        # Dm bar: D->Db walkdown on beat 4
        bass_with_chromatic_passing(bt(b + i), bridge_bass_root, bridge_bass_root - 1,
                                     vel=38, bar_num=i + 40)
    elif ci == 1:
        # Bb bar: Bb->A walkdown on beat 4
        bass_with_chromatic_passing(bt(b + i), bridge_bass_root, bridge_bass_root - 1,
                                     vel=38, bar_num=i + 40)
    elif ci == 2:
        # Ab bar: Ab->G walkdown on beat 4
        bass_with_chromatic_passing(bt(b + i), bridge_bass_root, bridge_bass_root - 1,
                                     vel=38, bar_num=i + 40)
    else:
        # G bar: no chromatic passing tone, just whole note
        bass(bt(b + i), bridge_bass_root, vel=38, bar_num=i + 40,
             pattern='whole', next_root=BRIDGE_BASS[((i + 2) // 2) % 4])

# BRIDGE MELODY — climbs to A5 (the highest note) on the Ab chord
bridge_melody = [
    # Over Dm: starts low, contemplative
    [(62, HALF), (65, HALF+EIGHTH), (67, EIGHTH+QUARTER), (None, QUARTER)],
    # Over Bb: starting to rise, the Bb chord lifts it
    [(67, QUARTER), (69, HALF+EIGHTH), (72, EIGHTH), (74, HALF+QUARTER), (None, QUARTER)],
    # Over Ab: THE PEAK — A5 (69) against Ab (68) chord root. That semitone tension is devastating.
    [(76, HALF), (77, HALF), (69, HALF+QUARTER), (None, QUARTER)],
    # Over G: the release, falling back to earth
    [(67, QUARTER), (65, HALF+EIGHTH), (64, EIGHTH), (60, HALF+QUARTER), (None, QUARTER)],
]
for pi, phrase in enumerate(bridge_melody):
    voice(bt(b + pi * 2), phrase, vel=48, bar_num=pi + 40)

b = 64

# === SILENCE (2 bars) — just piano sustain ringing out ===
piano_whole_chord(bt(b), make_chord(N('G',3), 'sus4'), vel=30)
piano_whole_chord(bt(b + 1), make_chord(N('G',3), 'major'), vel=25)

b = 66

# === FINAL CHORUS (8 bars) — Everything comes together ===
drums(bt(b), 'crash', bar_num=66)
for i in range(8):
    ci = (i // 2) % 4

    if i >= 6:
        voicing = gv(AB_CHORD, 0, i)
        bass_root = N('Ab',1)
        pad_voicing = AB_PAD_INV[0]
    else:
        voicing = gv(CHORUS_CHORDS, ci, i + 16)
        bass_root = CHORUS_BASS[ci]
        pad_voicing = gv(CHORUS_PAD_INVERSIONS, ci, i)

    piano_arpeggio(bt(b + i), voicing, vel=60, bar_num=i + 50)

    # Pad plays inversions
    if i % 2 == 0:
        synth_pad(bt(b + i), pad_voicing, vel=52, bars=2, bar_num=i)

    if i % 4 == 0:
        organ(bt(b + i), voicing, vel=34, bars=4, bar_num=i)

    bass(bt(b + i), bass_root, vel=50, bar_num=i + 16,
         pattern='melodic' if i < 6 else 'whole',
         next_root=CHORUS_BASS[((i+2)//2) % 4] if i < 6 else N('G',2))

    # FIX #2: Ghost snare on same relative positions in final chorus
    if i in GHOST_SNARE_CHORUS_BARS:
        drums_chorus_with_ghost(bt(b + i), bar_num=i + 16)
    else:
        drums(bt(b + i), 'chorus', bar_num=i + 16)

    # STRINGS enter in the last 4 bars — the big emotional payoff
    if i == 4:
        strings_swell(bt(b + 4), gv(CHORUS_CHORDS, 2, 0), vel=30, bars=4, bar_num=50)

# Same chorus melody but at its loudest
for pi, phrase in enumerate(chorus_phrases):
    voice(bt(b + pi * 2), phrase, vel=62, bar_num=pi + 50)

# Use the more melodic ch2 counter-melody
for pi, phrase in enumerate(lead_ch2):
    synth_lead(bt(b + pi * 2), phrase, vel=48, bar_num=pi + 16)

b = 74

# === OUTRO (12 bars) — Dissolving, ending on Cmaj7 ===
for i in range(12):
    ci = i % 4
    fade_vel = max(25, 48 - i * 2)

    if i < 4:
        voicing = gv(VERSE_CHORDS_A, ci, i + 60)
        piano_arpeggio(bt(b + i), voicing, vel=fade_vel, bar_num=i + 60)
    elif i < 8:
        voicing = gv(VERSE_CHORDS_A, ci, i + 60)
        piano_whole_chord(bt(b + i), voicing, vel=fade_vel - 5)
    else:
        piano_whole_chord(bt(b + i), CMAJ7, vel=max(20, fade_vel - 8))

    if i < 6 and i % 2 == 0:
        synth_pad(bt(b + i), gv(VERSE_CHORDS_A, ci, i), vel=max(20, 33 - i * 3), bars=2, bar_num=i + 60)

    if i < 4:
        bass(bt(b + i), VERSE_BASS_A[ci], vel=max(25, 38 - i * 5), bar_num=i + 60, pattern='whole')

    if i < 6 and i % 4 == 0:
        organ(bt(b + i), gv(VERSE_CHORDS_A, ci, i), vel=max(18, 28 - i * 2), bars=4, bar_num=i + 60)

# The final moment: a single high E5 on the piano
E.cc(0, 64, 127, bt(b + 10))
E.note(0, N('E',5), 28, bt(b + 10), BAR4 * 2 - 20, time_amount=15, vel_amount=3)
E.cc(0, 64, 0, bt(b + 12) - 30)

# A whisper of synth pad: just the B and E of Cmaj7, very quiet, disappearing
E.note(1, N('B',4), 16, bt(b + 10), BAR4 * 2 - 20, time_amount=15, vel_amount=3)
E.note(1, N('E',5), 14, bt(b + 10), BAR4 * 2 - 20, time_amount=15, vel_amount=3)


# ============================================================
# OUTPUT
# ============================================================

build_midi(E, 'Dial Tone Lullaby', bpm=72, total_bars=86,
           channel_names={
               0: 'Piano', 1: 'Synth Pad', 2: 'Synth Lead', 3: 'Clean Guitar',
               4: 'Distorted Guitar', 5: 'Organ', 6: 'Bass', 7: 'Strings',
               8: 'Vocal Melody', 9: 'Drums',
           },
           output_path='/home/user/music/compositions/v5/01_dial_tone_lullaby.mid')
