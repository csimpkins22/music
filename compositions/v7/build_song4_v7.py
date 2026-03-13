#!/usr/bin/env python3
"""
Song 4 v6: "Last Signal Home"
Key: G major | Tempo: 58 BPM | 3/4 | ~4:27

v6 changes — production-level improvements:
1. Bridge silence texture (bars 56-59): Guitar velocity FLAT vel=22 (no breathing_vel)
   during no-drum bars. The void is truly calm — no dynamic pushes.
2. Final chorus vocal leap framing (bars 72-73): Synth pad DROPS OUT on bar 72
   when vocal leaps E6->G6. Pad returns bar 73. The climax breathes in clear space.
3. Bass 3/4 alignment: bass_counter_riff enforces max 3 notes per bar.
   waltz_bass chromatic approach note on beat 3 only on last bar before chord change.

Kept from v5: rest+chromatic Bb5 in verse 1, bass counter-riffs in Ch1,
clean sustained pedal steel in bridge, E6 leap approach to G6 peak.
Kept from v4: waltz leaps, passing tones in Ch2, chromatic bass, drum fills,
E major surprise, F major borrowed chord, pedal steel turns, organ wobble timing,
Picardy third, "home" G ending.
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

# Bridge: Am - Em - F - C - D with F major borrowed from mixolydian
BRIDGE_V = [
    [make_chord(N('A',3),'minor'), make_chord(N('A',3),'min7')],
    [make_chord(N('E',4),'minor'), [N('E',4),N('G',4),N('B',4)]],
    [make_chord(N('F',4),'major'), make_chord(N('F',4),'add9')],   # F major — the drift
    [make_chord(N('C',4),'major'), make_chord(N('C',4),'add9')],
    [make_chord(N('D',4),'major'), make_chord(N('D',4),'sus4')],
]
BRIDGE_BASS = [N('A',1), N('E',2), N('F',2), N('C',2), N('D',2)]  # F in bass too

# E MAJOR chord for the final chorus surprise (parallel major of Em)
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


def waltz_bass(bar_start, root, vel=48, bar_num=0, next_root=None, chromatic_bar=False):
    """Waltz bass: 3 notes per bar in 3/4 time (root, 5th, approach/5th).
    v6 FIX 3: chromatic approach on beat 3 ONLY when chromatic_bar=True
    (last bar before a chord change). Otherwise beat 3 repeats the 5th.
    This prevents 4-note walking patterns that misalign with 3/4 time."""
    bvel = breathing_vel(vel, bar_num, 8, 4)
    v1 = bvel + accent_beat(0, 'waltz') + random.randint(-3, 3)
    v2 = bvel + accent_beat(1, 'waltz') + random.randint(-3, 3)

    # Beat 1: root
    E.note(6, root, v1, bar_start, QUARTER - 15, time_amount=8, vel_amount=4)
    # Beat 2: 5th
    E.note(6, root + 7, v2, bar_start + QUARTER, QUARTER - 15, time_amount=10, vel_amount=3)

    # Beat 3: chromatic approach ONLY on last bar before chord change
    if chromatic_bar and next_root is not None:
        # Chromatic approach: half-step below the next root
        approach = next_root - 1
        E.note(6, approach, v2 - 3, bar_start + HALF, QUARTER - 15, time_amount=10, vel_amount=3)
    else:
        # Default: repeat 5th (no walking 4th note that would misalign)
        E.note(6, root + 7, v2 - 3, bar_start + HALF, QUARTER - 15, time_amount=8, vel_amount=3)


# --- v5 FIX 2: Bass counter-riff for chorus bars ---
# v6 FIX 3: Enforce max 3 notes to stay aligned with 3/4 time
def bass_counter_riff(bar_start, notes, vel=46, bar_num=0):
    """Bass plays a quarter-note pattern of exactly 3 notes in 3/4 time.
    v6: truncates to 3 notes if more are passed — prevents 4th note
    hitting beat 1 of the next bar."""
    notes = notes[:3]  # v6 FIX 3: hard limit to 3 notes for 3/4 alignment
    bvel = breathing_vel(vel, bar_num, 8, 4)
    for beat, note in enumerate(notes):
        v = bvel + accent_beat(beat, 'waltz') + random.randint(-3, 3)
        E.note(6, note, v, bar_start + beat * QUARTER, QUARTER - 15,
               time_amount=8, vel_amount=4)


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


def pedal_steel_with_turns(bar_start, phrase, vel=45, bar_num=0):
    """Pedal steel that adds a melodic turn (2 quick eighth notes) at end of every other bar."""
    t = bar_start
    for i, (note, dur) in enumerate(phrase):
        if note is not None:
            v = breathing_vel(vel, bar_num + i, 4, 5)
            bend_dur = min(dur // 4, EIGHTH)
            E.pitch_bend(2, -2048, h_time(t - 5, 2))

            if i % 2 == 1 and dur >= DOTTED_HALF:
                # Every other bar: hold note shorter, then play 2 eighth-note turn
                hold_dur = dur - 2 * EIGHTH
                E.note(2, note, v, t, hold_dur - 20, time_amount=8, vel_amount=4)
                # Melodic turn: step up then step down
                turn_start = t + hold_dur
                step_up = note + 2    # whole step up
                step_down = note      # back to original
                E.note(2, step_up, v - 5, turn_start, EIGHTH - 15, time_amount=6, vel_amount=3)
                E.note(2, step_down, v - 8, turn_start + EIGHTH, EIGHTH - 15, time_amount=6, vel_amount=3)
            else:
                E.note(2, note, v, t, dur - 20, time_amount=8, vel_amount=4)

            steps = max(1, bend_dur // SIXTEENTH)
            for step in range(steps + 1):
                bend_val = int(-2048 + 2048 * (step / steps))
                E.pitch_bend(2, bend_val, h_time(t + step * SIXTEENTH, 3))
            if dur >= HALF:
                vib_start = t + bend_dur
                # Vibrato only for the held portion
                vib_dur = dur - bend_dur if i % 2 == 0 else (dur - 2 * EIGHTH - bend_dur)
                for step in range(max(0, vib_dur // SIXTEENTH)):
                    vib = int(150 * math.sin(step * 0.6))
                    E.pitch_bend(2, vib, h_time(vib_start + step * SIXTEENTH, 3))
            E.pitch_bend(2, 0, t + dur)
        t += dur


def pedal_steel_sustained(bar_start, note, dur, vel=45, bar_num=0):
    """Pedal steel playing a single long sustained note — no bend-up, just vibrato."""
    v = breathing_vel(vel, bar_num, 4, 5)
    E.pitch_bend(2, 0, h_time(bar_start - 5, 2))
    E.note(2, note, v, bar_start, dur - 20, time_amount=6, vel_amount=4)
    for step in range(dur // SIXTEENTH):
        vib = int(200 * math.sin(step * 0.4))
        E.pitch_bend(2, vib, h_time(bar_start + step * SIXTEENTH, 3))
    E.pitch_bend(2, 0, bar_start + dur)


# --- v5 FIX 3: Clean pedal steel sustained — no bends, no vibrato ---
def pedal_steel_clean_sustained(bar_start, note, dur, vel=28, bar_num=0):
    """Pedal steel playing a clean sustained note — no bend, no vibrato. Just tone."""
    v = breathing_vel(vel, bar_num, 4, 3)
    E.pitch_bend(2, 0, h_time(bar_start - 5, 2))
    E.note(2, note, v, bar_start, dur - 20, time_amount=6, vel_amount=3)
    E.pitch_bend(2, 0, bar_start + dur)


def waltz_drums(bar_start, pattern='basic', bar_num=0):
    ch = 9
    kick, snare, hh_c, hh_o, ride, crash, rim = 36, 38, 42, 46, 51, 49, 37
    tom_hi, tom_lo = 50, 45  # High tom, low tom for fills
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

    elif pattern == 'fill':
        # Beat 1: kick
        E.note(ch, kick, bvel + accent_beat(0,'waltz'), bar_start, QUARTER,
               time_amount=4, vel_amount=3)
        # Beat 2: two eighth-note toms (high->low)
        E.note(ch, tom_hi, bvel + 3, bar_start + QUARTER, EIGHTH,
               time_amount=5, vel_amount=3)
        E.note(ch, tom_lo, bvel, bar_start + QUARTER + EIGHTH, EIGHTH,
               time_amount=5, vel_amount=3)
        # Beat 3: snare roll (three triplets)
        triplet = QUARTER // 3
        for t in range(3):
            v = bvel + 5 - t * 2 + random.randint(-2, 2)
            E.note(ch, snare, v, bar_start + HALF + t * triplet, triplet - 10,
                   time_amount=4, vel_amount=3)


def piano_waltz(bar_start, chord_notes, vel=43, bar_num=0):
    bvel = breathing_vel(vel, bar_num, 6, 4)
    E.cc(0, 64, 100, h_time(bar_start, 3))
    for i, n in enumerate(chord_notes):
        v = bvel + accent_beat(i, 'waltz') + random.randint(-3, 3)
        E.note(0, n, v, bar_start + i * QUARTER, QUARTER - random.randint(12, 20),
               time_amount=8, vel_amount=3)
    E.cc(0, 64, 0, h_time(bar_start + BAR3 - 30, 3))


def organ_clean(bar_start, chord_notes, vel=30, bars=4, bar_num=0):
    """Clean organ — no pitch wobble. For chorus 1 and 2."""
    bvel = breathing_vel(vel, bar_num, 6, 3)
    for n in chord_notes:
        E.note(5, n, bvel, bar_start, BAR3 * bars - 30, time_amount=12, vel_amount=4)
    # No pitch bend — clean


def organ(bar_start, chord_notes, vel=30, bars=4, bar_num=0, wobble_cents=60):
    """Organ with configurable pitch wobble. For final chorus only in v4."""
    bvel = breathing_vel(vel, bar_num, 6, 3)
    for n in chord_notes:
        E.note(5, n, bvel, bar_start, BAR3 * bars - 30, time_amount=12, vel_amount=4)
    for step in range(bars * 6):
        t = bar_start + step * EIGHTH
        bend = int(wobble_cents * math.sin(step * 0.3))
        E.pitch_bend(5, bend, h_time(t, 3))
    E.pitch_bend(5, 0, bar_start + BAR3 * bars)


def organ_fading(bar_start, chord_notes, vel=30, bars=8, bar_num=0):
    """Outro organ: pitch wobble drifts from +/-60 to +/-200 cents."""
    bvel = breathing_vel(vel, bar_num, 6, 3)
    for n in chord_notes:
        E.note(5, n, bvel, bar_start, BAR3 * bars - 30, time_amount=12, vel_amount=4)
    total_steps = bars * 6
    for step in range(total_steps):
        t = bar_start + step * EIGHTH
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
    """Strings that crescendo over many bars — for the final chorus."""
    steps = bars * 6
    for step in range(steps):
        t = bar_start + step * EIGHTH
        progress = (step / max(1, steps - 1)) ** 1.2
        expr = int(40 + 87 * progress)
        E.cc(7, 11, min(127, expr), h_time(t, 3))
    for n in [nn + 12 for nn in chord_notes[:3]]:
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
for i in range(16):
    ci = (i // 2) % 4
    nci = ((i+1) // 2) % 4
    fingerpick(bt(b+i), gv(VERSE_V, ci, i), vel=44, bar_num=i+8)
    if i >= 4:
        is_chromatic = (i % 4 == 3)
        waltz_bass(bt(b+i), VERSE_BASS[ci], vel=40, bar_num=i,
                   next_root=VERSE_BASS[nci], chromatic_bar=is_chromatic)
    if i >= 8:
        if i == 15:
            waltz_drums(bt(b+i), 'fill', bar_num=i+8)
        else:
            waltz_drums(bt(b+i), 'verse', bar_num=i+8)
    if i % 4 == 0:
        pad_swell(bt(b+i), gv(VERSE_V, ci, i+1), vel=28, bars=4, bar_num=i)

# v5 FIX 1: Verse 1 melody — waltz LEAPS
# Phrase 2 (bars 10-11): Break stepwise C6->B5 with rest + chromatic Bb5 passing tone
v1 = [
    # Phrase 1: G5 LEAPS to D6 (5th!), hold D6 for a full bar, then fall
    [(N('G',5), QUARTER), (N('D',6), HALF),
     (N('D',6), DOTTED_HALF)],
    # Phrase 2 (bars 10-11): REST (half note), then chromatic Bb5 (eighth), B5 (eighth)
    # v5 FIX 1: Breaks the ladder descent with rest and chromatic passing tone
    [(None, HALF), (N('Bb',5), EIGHTH), (N('B',5), EIGHTH),
     (N('B',5), DOTTED_HALF)],
    # Phrase 3: E5 lifts to G5, holds, A5 reaches up
    [(N('E',5), DOTTED_HALF),
     (N('G',5), HALF), (N('A',5), QUARTER)],
    # Phrase 4: resolve back — A sinks to G, then F# settles to G
    [(N('A',5), HALF), (N('G',5), QUARTER),
     (N('G',5), DOTTED_HALF)],
    # Phrase 5: second half — G5 LEAPS up to D6, C6 pulls back
    [(N('G',5), QUARTER), (N('D',6), HALF),
     (N('D',6), HALF), (N('C',6), QUARTER)],
    # Phrase 6: B5 holds, sinks to A — weight on downbeats
    [(N('B',5), DOTTED_HALF),
     (N('A',5), DOTTED_HALF)],
    # Phrase 7: E5 holds, steps up to G5
    [(N('E',5), DOTTED_HALF),
     (N('G',5), HALF), (None, QUARTER)],
    # Phrase 8: final phrase — G5 to F# resolve to D5, all sustained
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

    # v5 FIX 2: Bass counter-riff on bars 26 and 30 (i=2 and i=6)
    if i == 2:
        # Em bar counter-riff: E->G->A (quarter-note pattern in 3/4)
        bass_counter_riff(bt(b+i), [N('E',2), N('G',2), N('A',2)], vel=46, bar_num=i+8)
    elif i == 6:
        # G bar counter-riff: G->B->D (quarter-note pattern in 3/4)
        bass_counter_riff(bt(b+i), [N('G',2), N('B',2), N('D',3)], vel=46, bar_num=i+8)
    else:
        is_chromatic = (i % 4 == 3)
        waltz_bass(bt(b+i), CHORUS_BASS[ci], vel=46, bar_num=i+8,
                   next_root=CHORUS_BASS[nci], chromatic_bar=is_chromatic)

    if i == 7:
        waltz_drums(bt(b+i), 'fill', bar_num=i+24)
    else:
        waltz_drums(bt(b+i), 'chorus', bar_num=i+24)
    if i % 2 == 0:
        pad_swell(bt(b+i), gv(CHORUS_V, ci, i+1), vel=36, bars=2, bar_num=i+8)
    piano_waltz(bt(b+i), gv(CHORUS_V, ci, i+2), vel=40, bar_num=i+24)

# Chorus 1 melody (original)
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

# Pedal steel counter-melody for chorus 1
pedal_steel(bt(b), [(n, d) for n, d in zip(
    [N('G',5),N('F#',5),N('E',5),N('D',5),N('E',5),N('G',5),N('F#',5),N('D',5)],
    [DOTTED_HALF]*8)], vel=36, bar_num=24)

# Chorus 1 gets CLEAN organ (no wobble)
for i in range(0, 8, 4):
    ci = (i // 2) % 4
    organ_clean(bt(b+i), gv(CHORUS_V, ci, i+3), vel=26, bars=4, bar_num=i+24)

b = 32

# === VERSE 2 (16 bars) ===
for i in range(16):
    ci = (i // 2) % 4
    nci = ((i+1) // 2) % 4
    fingerpick(bt(b+i), gv(VERSE_V, ci, i+16), vel=46, bar_num=i+32)
    is_chromatic = (i % 4 == 3)
    waltz_bass(bt(b+i), VERSE_BASS[ci], vel=42, bar_num=i+16,
               next_root=VERSE_BASS[nci], chromatic_bar=is_chromatic)
    if i >= 4:
        if i == 15:
            waltz_drums(bt(b+i), 'fill', bar_num=i+32)
        else:
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

# Pedal steel with melodic turns for verse 2
pedal_steel_with_turns(bt(b), [(n, d) for n, d in zip(
    [N('G',5),N('F#',5),N('E',5),N('D',5),N('E',5),N('G',5),N('F#',5),N('D',5),
     N('E',5),N('G',5),N('A',5),N('G',5),N('F#',5),N('E',5),N('D',5),N('E',5)],
    [DOTTED_HALF]*16)], vel=38, bar_num=32)

b = 48

# === CHORUS 2 (8 bars) — clean organ (no wobble) ===
waltz_drums(bt(b), 'crash', bar_num=48)
for i in range(8):
    ci = (i // 2) % 4
    nci = ((i+2) // 2) % 4
    fingerpick(bt(b+i), gv(CHORUS_V, ci, i+8), vel=50, bar_num=i+48)
    is_chromatic = (i % 4 == 3)
    waltz_bass(bt(b+i), CHORUS_BASS[ci], vel=48, bar_num=i+24,
               next_root=CHORUS_BASS[nci], chromatic_bar=is_chromatic)
    if i == 7:
        waltz_drums(bt(b+i), 'fill', bar_num=i+48)
    else:
        waltz_drums(bt(b+i), 'chorus', bar_num=i+48)
    piano_waltz(bt(b+i), gv(CHORUS_V, ci, i+4), vel=43, bar_num=i+48)
    if i % 2 == 0:
        pad_swell(bt(b+i), gv(CHORUS_V, ci, i+5), vel=38, bars=2, bar_num=i+24)
    if i % 4 == 0:
        organ_clean(bt(b+i), gv(CHORUS_V, ci, i+3), vel=26, bars=4, bar_num=i+24)

# Chorus 2 melody — DECORATED with passing tones
ch_mel_2 = [
    [(N('B',5),QUARTER+EIGHTH),(N('C',6),EIGHTH),(N('D',6),EIGHTH),(N('E',6),EIGHTH),
     (N('E',6),QUARTER+EIGHTH),(N('D',6),EIGHTH),(N('C',6),EIGHTH),(N('D',6),EIGHTH)],
    [(N('C',6),EIGHTH),(N('B',5),EIGHTH),(N('A',5),EIGHTH),(N('B',5),EIGHTH+QUARTER),
     (N('A',5),QUARTER),(N('G',5),EIGHTH),(N('A',5),EIGHTH)],
    [(N('G',5),EIGHTH),(N('A',5),EIGHTH),(N('B',5),EIGHTH),(N('C',6),EIGHTH),(N('D',6),EIGHTH),(N('C',6),EIGHTH),
     (N('C',6),QUARTER+EIGHTH),(N('B',5),EIGHTH),(N('A',5),EIGHTH),(N('B',5),EIGHTH)],
    [(N('A',5),EIGHTH),(N('G',5),EIGHTH),(N('F#',5),EIGHTH),(N('G',5),EIGHTH+QUARTER),
     (N('G',5),HALF),(None,QUARTER)],
]
for pi, phrase in enumerate(ch_mel_2):
    voice(bt(b + pi*2), phrase, vel=56, bar_num=pi+48)

b = 56

# === BRIDGE (12 bars) — Am-Em-F-C-D with F major borrowed chord ===
# Bridge drums — NO drums for first 4 bars, brush enters for remaining 8
bridge_seq = [0,1,2,3,4, 0,1,2,3,4, 0,1]
for i in range(12):
    ci = bridge_seq[i]
    piano_waltz(bt(b+i), gv(BRIDGE_V, ci, i), vel=50, bar_num=i+56)
    waltz_bass(bt(b+i), BRIDGE_BASS[ci], vel=46, bar_num=i+32,
               next_root=BRIDGE_BASS[bridge_seq[min(i+1,11)]])
    # Silence for first 4 bars, then brush
    if i >= 4:
        waltz_drums(bt(b+i), 'brush', bar_num=i+56)
    if i % 2 == 0:
        pad_swell(bt(b+i), gv(BRIDGE_V, ci, i+1), vel=33, bars=2, bar_num=i+32)

    # v6 FIX 1: Bridge bars 56-59 (first 4 bars, no drums) — guitar vel FLAT 22
    # No breathing_vel — the void should be truly calm, no dynamic pushes
    if i < 4:
        # FLAT velocity, no breathing_vel modulation
        for n in gv(BRIDGE_V, ci, i+2):
            E.note(3, n - 12, 22, bt(b+i), BAR3 - 25,
                   time_amount=15, vel_amount=5)
    else:
        # Normal breathing_vel guitar for bars 60+ (drums are back)
        for n in gv(BRIDGE_V, ci, i+2):
            E.note(3, n - 12, breathing_vel(36, i, 6, 4), bt(b+i), BAR3 - 25,
                   time_amount=15, vel_amount=5)

# v5 FIX 3: Bridge bars 56-59 (first 4 bars, no drums) — clean sustained pedal steel D5
# Fills the percussion void with a clean tone, no bends, no movement
pedal_steel_clean_sustained(bt(b), N('D',5), BAR3 * 4, vel=28, bar_num=56)

# Bridge melody: E6 (highest note) appears on the F chord
br = [
    # Am: start low, yearning
    [(N('E',5),QUARTER),(N('G',5),QUARTER+EIGHTH),(N('A',5),EIGHTH),
     (N('B',5),HALF),(N('A',5),QUARTER)],
    # Em: settle
    [(N('G',5),DOTTED_HALF),
     (N('E',5),DOTTED_HALF)],
    # F MAJOR: the peak — E6 on the wrongest chord
    [(N('C',6),QUARTER),(N('E',6),HALF),
     (N('E',6),DOTTED_HALF)],
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

# Pedal steel — bridge counter-melody (starts after the clean sustained D5 ends at bar 60)
pedal_steel(bt(b+4), [(n, d) for n, d in zip(
    [N('E',5),N('G',5),N('A',5),N('B',5),N('D',6),N('B',5),N('A',5),N('G',5)],
    [DOTTED_HALF]*8)], vel=40, bar_num=60)

b = 68

# === FINAL CHORUS (10 bars) — 8 normal + 2 bars E MAJOR surprise ===
# Strings enter for ALL 10 bars, crescendo through E major.

waltz_drums(bt(b), 'crash', bar_num=68)

# --- First 8 bars: normal Em-C-G-D chorus ---
for i in range(8):
    ci = (i // 2) % 4
    nci = ((i+2) // 2) % 4
    fingerpick(bt(b+i), gv(CHORUS_V, ci, i+16), vel=53, bar_num=i+68)
    is_chromatic = (i % 4 == 3)
    waltz_bass(bt(b+i), CHORUS_BASS[ci], vel=50, bar_num=i+40,
               next_root=CHORUS_BASS[nci], chromatic_bar=is_chromatic)
    waltz_drums(bt(b+i), 'chorus', bar_num=i+68)
    piano_waltz(bt(b+i), gv(CHORUS_V, ci, i+6), vel=48, bar_num=i+68)

    # v6 FIX 2: Pad DROPS OUT on bar 72 (i=4) to frame vocal leap E6->G6
    # Pad returns on bar 73 (i=5). The climax breathes in clear space.
    if i == 4:
        # Bar 72: NO pad_swell — let the vocal leap breathe
        pass
    elif i % 2 == 0:
        pad_swell(bt(b+i), gv(CHORUS_V, ci, i+7), vel=40, bars=2, bar_num=i+40)

# Final chorus gets wobble organ
for i in range(0, 8, 4):
    ci = (i // 2) % 4
    organ(bt(b+i), gv(CHORUS_V, ci, i+5), vel=30, bars=4, bar_num=i+40, wobble_cents=60)

# Strings enter — all 10 bars of the final chorus, crescendo through E major
strings_crescendo(bt(b), gv(CHORUS_V, 0, 0), vel_start=20, vel_end=55, bars=10, bar_num=68)

# v5 FIX 4: Final chorus melody — rewritten approach to G6 peak
# Bars 72-74: leap from rest directly to E6, earning the climax by surprise
ch_mel_final = [
    [(N('B',5),HALF+EIGHTH),(N('D',6),EIGHTH),
     (N('E',6),HALF),(N('D',6),QUARTER)],
    [(N('C',6),QUARTER),(N('B',5),HALF),
     (N('A',5),DOTTED_HALF)],
    # v5 FIX 4: G5 (half) rest (quarter) E6 (quarter) G6 (dotted half)
    # The leap from rest directly to E6 is unexpected — earns the climax by surprise
    # v6 FIX 2: Pad drops out this bar — vocal leap breathes in clear space
    [(N('G',5), HALF), (None, QUARTER),
     (N('E',6), QUARTER), (N('G',6), DOTTED_HALF)],
    [(N('D',6),QUARTER),(N('B',5),HALF),
     (N('G',5),DOTTED_HALF)],
]
for pi, phrase in enumerate(ch_mel_final):
    voice(bt(b + pi*2), phrase, vel=60, bar_num=pi+68)

# Pedal steel counter for normal chorus bars
pedal_steel(bt(b), [(n, d) for n, d in zip(
    [N('G',5),N('F#',5),N('E',5),N('D',5),N('E',5),N('G',5),N('F#',5),N('D',5)],
    [DOTTED_HALF]*8)], vel=38, bar_num=68)

# --- THE E MAJOR SURPRISE: bars 8-9 of the final chorus (2 extra bars) ---
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

# E major bars also get wobble organ (part of final chorus)
organ(bt(e_bar), E_MAJOR_CHORD, vel=32, bars=2, bar_num=76, wobble_cents=60)

# Pedal steel plays G# — THE note that changes
pedal_steel_sustained(bt(e_bar), N('G#',5), BAR3 * 2, vel=48, bar_num=76)

# Vocal sustains G5 (clash!) over E major (G vs G# = old key fighting new key)
# Then resolves: last 2 beats shift from G5 to G#5 (acceptance, surrender)
g5_dur = BAR3 + QUARTER  # bar 1 full + beat 1 of bar 2
E.note(8, N('G',5), 58, bt(e_bar), g5_dur - 30, time_amount=6, vel_amount=4)
# Resolution: G#5 for last 2 beats of bar 2
E.note(8, N('G#',5), 55, bt(e_bar + 1) + QUARTER, HALF - 30, time_amount=6, vel_amount=4)

# Additional strings voicing for the E major bars specifically (E-G#-B an octave up)
for n in [N('E',5), N('G#',5), N('B',5)]:
    E.note(7, n + 12, 45, bt(e_bar), BAR3 * 2 - 30, time_amount=10, vel_amount=5)

b = 78  # 68 + 10

# === OUTRO (8 bars) ===
# organ_fading with wobble +/-60 -> +/-200 cents (only now does full wobble appear)
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

# Organ with fading signal — pitch wobble drifts from +/-60 to +/-200 cents
organ_fading(bt(b), gv(VERSE_V, 0, 0), vel=24, bars=8, bar_num=78)

# Pedal steel final bend
pedal_steel(bt(b+4), [(N('D',5), DOTTED_HALF*4)], vel=33, bar_num=82)

# Final piano chord — G add9
E.cc(0, 64, 110, h_time(bt(b+5), 3))
for n in make_chord(N('G',4), 'major'):
    E.note(0, n, 35, bt(b+5), BAR3 * 2 - 30, time_amount=12, vel_amount=4)
E.cc(0, 64, 0, h_time(bt(b+7) - 30, 3))

# THE LAST SOUND — a single fingerpicked G, completely alone. The tonic. Home.
last_bar = b + 7
E.note_raw(3, N('G',4), 40, bt(last_bar) + HALF, DOTTED_HALF + BAR3)


# ============================================================
# OUTPUT
# ============================================================

build_midi(E, 'Last Signal Home', bpm=58, time_sig_num=3, total_bars=88,
           channel_names={
               0: 'Piano', 1: 'Synth Pad', 2: 'Pedal Steel Synth', 3: 'Clean Guitar',
               4: 'Distorted Guitar', 5: 'Organ', 6: 'Bass', 7: 'Strings',
               8: 'Vocal Melody', 9: 'Drums',
           },
           output_path='/home/user/music/compositions/v7/04_last_signal_home.mid')
