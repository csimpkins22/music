#!/usr/bin/env python3
"""
Song 1 v2: "Dial Tone Lullaby"
Key: C major | Tempo: 72 BPM | 4/4 | ~4:15

v2 improvements:
- Humanized timing on ALL instruments (±5-12 tick jitter)
- Velocity breathing/undulation across phrases
- Piano arpeggios: more varied patterns, neighbor tones, occasional sus/add9 voicings
- Synth lead: complete rewrite with expressive dynamics and counter-melody
- Vocal melody: grace notes, subtle anticipations, wider dynamic arc
- Drums: varied patterns bar-to-bar, ghost notes, hi-hat variation
- Bass: chromatic approach notes, melodic fills between chord changes
- Added sustain pedal (CC64) for piano warmth
- Synth pad: velocity swells, not flat blocks
- Organ: subtle pitch bend wobble for analog feel
- Bridge: rubato-like timing stretches
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from humanize import *

E = EventList()

def bt(bar_num):
    return bar_num * BAR4

# Scale: C major — C D E F G A B
# Chord voicings with more variety (inversions, extensions)
VERSE_VOICINGS = [
    # C major — vary between root, add9, sus2
    [make_chord(N('C',4), 'major'), make_chord(N('C',4), 'add9'), make_chord(N('C',4), 'sus2')],
    # Em — vary between root and min7
    [make_chord(N('E',4), 'minor'), make_chord(N('E',4), 'min7'), [N('E',4), N('G',4), N('B',4)]],
    # F major — root and add9
    [make_chord(N('F',4), 'major'), make_chord(N('F',4), 'add9'), [N('F',4), N('A',4), N('C',5)]],
    # G — root and sus4
    [make_chord(N('G',4), 'major'), make_chord(N('G',4), 'sus4'), [N('G',4), N('B',4), N('D',5)]],
]

CHORUS_VOICINGS = [
    [make_chord(N('A',4), 'minor'), make_chord(N('A',4), 'min7')],
    [make_chord(N('F',4), 'major'), make_chord(N('F',4), 'add9')],
    [make_chord(N('C',4), 'major'), make_chord(N('C',4), 'add9')],
    [make_chord(N('G',4), 'major'), make_chord(N('G',4), 'sus4')],
]

BRIDGE_VOICINGS = [
    [make_chord(N('D',4), 'minor'), make_chord(N('D',4), 'min7')],
    [make_chord(N('A',4), 'minor'), [N('A',4), N('C',5), N('E',5)]],
    [make_chord(N('F',4), 'major'), [N('F',4), N('A',4), N('C',5)]],
    [make_chord(N('C',4), 'major'), make_chord(N('C',4), 'sus2')],
]

VERSE_BASS = [N('C',2), N('E',2), N('F',2), N('G',2)]
CHORUS_BASS = [N('A',1), N('F',2), N('C',2), N('G',2)]
BRIDGE_BASS = [N('D',2), N('A',1), N('F',2), N('C',2)]


def get_voicing(voicings, chord_idx, bar_num):
    """Pick a voicing based on bar number for variety."""
    options = voicings[chord_idx]
    return options[bar_num % len(options)]


def piano_arpeggio_v2(bar_start, chord_notes, vel=50, bar_num=0):
    """Humanized piano arpeggio with varied patterns, accents, and occasional grace notes."""
    notes = list(chord_notes) + [chord_notes[0] + 12]
    if len(chord_notes) > 3:
        notes = list(chord_notes) + [chord_notes[0] + 12]

    # 6 different patterns to cycle through
    patterns = [
        [0,1,2,3,2,1,0,3],    # wave
        [0,2,1,3,0,2,3,1],    # skip
        [3,2,1,0,1,2,3,2],    # descending wave
        [0,1,0,2,1,2,3,2],    # tentative
        [0,3,1,2,0,3,2,1],    # wide
        [0,1,2,1,0,2,3,2],    # gentle sway
    ]
    pat = patterns[bar_num % len(patterns)]

    # Add sustain pedal
    E.cc(0, 64, 100, h_time(bar_start, 3))  # pedal down
    E.cc(0, 64, 0, h_time(bar_start + BAR4 - 30, 3))  # pedal up

    # Breathing velocity
    base_vel = breathing_vel(vel, bar_num, cycle_bars=8, depth=5)

    for i in range(8):
        idx = pat[i] % len(notes)
        note = notes[idx]
        t = bar_start + i * EIGHTH + swing_offset(i, 12)

        # Natural accenting: beat 1 and 3 stronger
        beat = i // 2
        v = base_vel + accent_beat(beat)
        v = v if i % 2 == 0 else v - 7

        # Occasional grace note (every ~6 bars, on beat 1)
        if i == 0 and bar_num % 6 == 3:
            grace = note - 2 if note - 2 >= 48 else note + 2
            E.note(0, grace, v - 15, t - SIXTEENTH, SIXTEENTH - 5, time_amount=5)

        E.note(0, note, v, t, EIGHTH - random.randint(15, 30), time_amount=6, vel_amount=3)


def synth_pad_v2(bar_start, chord_notes, vel=40, bars=2, bar_num=0):
    """Synth pad with velocity swell — not a flat block."""
    # Swell: start soft, peak at 60% through, ease back
    steps = bars * 4  # control points per bar
    for step in range(steps):
        t = bar_start + step * QUARTER
        phase = step / steps
        # Bell curve swell
        swell = math.sin(phase * math.pi)
        v = int(vel * 0.7 + vel * 0.3 * swell)
        # Express via CC11 (expression) instead of re-triggering notes
        E.cc(1, 11, max(40, min(127, int(v * 2.5))), h_time(t, 5))

    # The actual notes — with subtle humanization
    bvel = breathing_vel(vel, bar_num, 6, 4)
    for note in chord_notes:
        E.note(1, note, bvel, bar_start, BAR4 * bars - 30, time_amount=10, vel_amount=4)


def synth_lead_v2(bar_start, phrase, vel=55, bar_num=0):
    """Expressive synth lead with dynamics shaped by melodic contour."""
    t = bar_start
    prev_note = None
    for i, (note, dur) in enumerate(phrase):
        if note is not None:
            # Shape velocity by pitch height — higher = louder (natural expression)
            pitch_boost = max(0, (note - 60) // 4)
            v = breathing_vel(vel + pitch_boost, bar_num + i, 4, 6)

            # Legato overlap from previous note
            actual_dur = dur - random.randint(20, 40)

            # Add subtle vibrato via pitch bend on longer notes
            if dur >= HALF:
                # Start straight, add wobble
                for step in range(0, dur // SIXTEENTH, 2):
                    bend_t = t + step * SIXTEENTH
                    bend_val = int(200 * math.sin(step * 0.8))
                    E.pitch_bend(2, bend_val, h_time(bend_t, 3))
                E.pitch_bend(2, 0, t + dur)  # reset

            E.note(2, note, v, t, actual_dur, time_amount=8, vel_amount=4)
            prev_note = note
        t += dur


def bass_v2(bar_start, root, vel=48, bar_num=0, pattern='whole', next_root=None):
    """Bass with chromatic approaches, fills, and humanized timing."""
    bvel = breathing_vel(vel, bar_num, 8, 4)

    if pattern == 'whole':
        E.note(6, root, bvel, bar_start, BAR4 - 40, time_amount=10, vel_amount=4)
        # Chromatic approach to next chord on last beat
        if next_root is not None and bar_num % 3 == 2:
            approach = next_root - 1 if next_root > root else next_root + 1
            E.note(6, approach, bvel - 8, bar_start + HALF + QUARTER, QUARTER - 20,
                   time_amount=8, vel_amount=3)
    elif pattern == 'half':
        E.note(6, root, bvel, bar_start, HALF - 30, time_amount=8, vel_amount=4)
        fifth = root + 7
        E.note(6, fifth, bvel - 5, bar_start + HALF, HALF - 30, time_amount=10, vel_amount=3)
        # Occasional walking fill
        if bar_num % 4 == 3 and next_root is not None:
            E.note(6, next_root - 2, bvel - 10, bar_start + HALF + QUARTER, QUARTER - 20,
                   time_amount=6, vel_amount=3)
    elif pattern == 'melodic':
        # More melodic bass — root, 3rd, 5th, approach
        E.note(6, root, bvel, bar_start, QUARTER - 20, time_amount=8)
        E.note(6, root + 4, bvel - 5, bar_start + QUARTER, QUARTER - 20, time_amount=10)
        E.note(6, root + 7, bvel - 3, bar_start + HALF, QUARTER - 20, time_amount=8)
        target = next_root if next_root else root
        approach = target - 1 if random.random() > 0.5 else target + 2
        E.note(6, approach, bvel - 8, bar_start + HALF + QUARTER, QUARTER - 20, time_amount=10)


def drums_v2(bar_start, pattern='minimal', bar_num=0):
    """Drums with per-bar variation, ghost notes, and humanized timing."""
    ch = 9
    kick, snare, hh_c, hh_o, rim = 36, 38, 42, 46, 37
    bvel_k = breathing_vel(48, bar_num, 8, 4)

    if pattern == 'minimal':
        E.note(ch, kick, bvel_k, bar_start, QUARTER, time_amount=6, vel_amount=4)
        # Vary hi-hat pattern
        for i in range(4):
            t = bar_start + i * QUARTER
            v = 22 + accent_beat(i) + random.randint(-3, 3)
            if i == 0: continue  # skip beat 1 (kick is there)
            E.note(ch, hh_c, v, t, EIGHTH, time_amount=8, vel_amount=3)
        # Ghost note on occasional bars
        if bar_num % 3 == 1:
            E.note(ch, snare, 15, bar_start + QUARTER + EIGHTH, EIGHTH, time_amount=12)

    elif pattern == 'verse':
        E.note(ch, kick, bvel_k, bar_start, QUARTER, time_amount=5, vel_amount=4)
        E.note(ch, snare, h_vel(28, 4), bar_start + QUARTER, QUARTER, time_amount=8, vel_amount=5)
        E.note(ch, kick, bvel_k - 5, bar_start + HALF, QUARTER, time_amount=6, vel_amount=4)
        E.note(ch, snare, h_vel(28, 4), bar_start + HALF + QUARTER, QUARTER, time_amount=8, vel_amount=5)
        # Hi-hat with swing
        for i in range(8):
            t = bar_start + i * EIGHTH + swing_offset(i, 10)
            v = 20 + (4 if i % 2 == 0 else 0) + random.randint(-3, 3)
            E.note(ch, hh_c, v, t, EIGHTH, time_amount=6, vel_amount=2)
        # Ghost notes between snares (random)
        if bar_num % 2 == 0:
            E.note(ch, snare, 12, bar_start + QUARTER + EIGHTH + swing_offset(1, 10),
                   EIGHTH, time_amount=12, vel_amount=3)
        # Occasional open hi-hat variation
        if bar_num % 4 == 3:
            E.note(ch, hh_o, 25, bar_start + HALF + QUARTER, EIGHTH, time_amount=8)

    elif pattern == 'chorus':
        E.note(ch, kick, bvel_k + 5, bar_start, QUARTER, time_amount=5, vel_amount=4)
        E.note(ch, snare, h_vel(35, 5), bar_start + QUARTER, QUARTER, time_amount=7, vel_amount=5)
        E.note(ch, kick, bvel_k, bar_start + HALF, QUARTER, time_amount=6, vel_amount=4)
        E.note(ch, snare, h_vel(35, 5), bar_start + HALF + QUARTER, QUARTER, time_amount=7, vel_amount=5)
        for i in range(8):
            t = bar_start + i * EIGHTH + swing_offset(i, 8)
            v = 26 + (5 if i % 2 == 0 else 0) + random.randint(-3, 3)
            E.note(ch, hh_c, v, t, EIGHTH, time_amount=5, vel_amount=2)
        # Ghost kicks for groove
        if bar_num % 2 == 1:
            E.note(ch, kick, bvel_k - 20, bar_start + QUARTER + EIGHTH, EIGHTH, time_amount=10)

    elif pattern == 'fill':
        E.note(ch, kick, bvel_k + 8, bar_start, QUARTER, time_amount=4)
        E.note(ch, snare, 30, bar_start + QUARTER, EIGHTH, time_amount=8)
        E.note(ch, snare, 35, bar_start + QUARTER + EIGHTH, EIGHTH, time_amount=10)
        E.note(ch, snare, 40, bar_start + HALF, EIGHTH, time_amount=8)
        E.note(ch, snare, 45, bar_start + HALF + EIGHTH, EIGHTH, time_amount=6)
        E.note(ch, hh_o, 50, bar_start + HALF + QUARTER, QUARTER, time_amount=5)


def voice_v2(bar_start, phrase, vel=52, bar_num=0):
    """Vocal melody with expressive dynamics, anticipations, and grace notes."""
    t = bar_start
    prev_note = None
    for i, (note, dur) in enumerate(phrase):
        if note is not None:
            v = vel
            # Shape by melodic contour
            if prev_note is not None:
                interval = note - prev_note
                if interval > 3: v += 4   # leaps get louder
                elif interval < -3: v -= 2  # descents get softer

            v = breathing_vel(v, bar_num + i, 6, 5)

            # Occasional anticipation (play 16th note early)
            anticipation = 0
            if i > 0 and random.random() < 0.15 and dur <= HALF:
                anticipation = -SIXTEENTH

            # Grace note on larger leaps
            if prev_note is not None and abs(note - prev_note) >= 4 and random.random() < 0.3:
                grace = prev_note + (1 if note > prev_note else -1)
                E.note(8, grace, v - 12, t + anticipation - SIXTEENTH, SIXTEENTH - 5,
                       time_amount=10, vel_amount=3)

            actual_dur = dur - random.randint(25, 45)
            E.note(8, note, v, t + anticipation, actual_dur, time_amount=10, vel_amount=5)
            prev_note = note
        t += dur


def organ_v2(bar_start, chord_notes, vel=32, bars=4, bar_num=0):
    """Organ with subtle pitch bend wobble for analog feel."""
    bvel = breathing_vel(vel, bar_num, 6, 3)
    for note in chord_notes:
        E.note(5, note, bvel, bar_start, BAR4 * bars - 30, time_amount=12, vel_amount=4)
    # Subtle LFO-like pitch wobble
    for step in range(bars * 8):
        t = bar_start + step * EIGHTH
        bend = int(80 * math.sin(step * 0.3))
        E.pitch_bend(5, bend, h_time(t, 3))
    E.pitch_bend(5, 0, bar_start + BAR4 * bars)


# ============================================================
# BUILD THE SONG
# ============================================================

b = 0

# --- INTRO (8 bars) — Solo piano, building gently ---
for i in range(8):
    ci = i % 4
    voicing = get_voicing(VERSE_VOICINGS, ci, i)
    vel = 38 + i * 2  # gentle crescendo into verse
    piano_arpeggio_v2(bt(i), voicing, vel=vel, bar_num=i)

b = 8

# --- VERSE 1 (16 bars) ---
for i in range(16):
    ci = (i // 2) % 4
    next_ci = ((i + 1) // 2) % 4
    voicing = get_voicing(VERSE_VOICINGS, ci, i)

    piano_arpeggio_v2(bt(b + i), voicing, vel=50, bar_num=i)

    # Synth pad enters bar 4 with swell
    if i >= 4 and i % 2 == 0:
        synth_pad_v2(bt(b + i), get_voicing(VERSE_VOICINGS, ci, i + 1), vel=32 + i, bars=2, bar_num=i)

    # Bass enters bar 8 — whole notes with chromatic approaches
    if i >= 8:
        next_bass = VERSE_BASS[next_ci] if i < 15 else VERSE_BASS[0]
        pattern = 'melodic' if i >= 12 else 'whole'
        bass_v2(bt(b + i), VERSE_BASS[ci], vel=38, bar_num=i, pattern=pattern, next_root=next_bass)

    # Drums — very sparse at first, verse pattern later
    if i >= 12:
        if i == 15:
            drums_v2(bt(b + i), 'fill', bar_num=i)
        else:
            drums_v2(bt(b + i), 'minimal', bar_num=i)

# Verse 1 melody — descending phrases with ornaments
v1_phrases = [
    [(72, QUARTER), (71, QUARTER), (69, HALF), (67, HALF), (None, HALF)],
    [(69, QUARTER), (67, QUARTER), (65, HALF), (64, HALF+EIGHTH), (None, QUARTER+EIGHTH)],
    [(65, QUARTER), (67, HALF), (69, QUARTER), (72, HALF), (None, HALF)],
    [(71, QUARTER), (69, EIGHTH), (67, EIGHTH), (67, HALF), (65, WHOLE)],
    [(72, QUARTER), (72, QUARTER+EIGHTH), (69, EIGHTH), (67, HALF), (None, HALF)],
    [(69, EIGHTH), (67, EIGHTH), (65, QUARTER), (64, HALF), (65, HALF+EIGHTH), (None, QUARTER+EIGHTH)],
    [(67, QUARTER), (69, QUARTER), (72, HALF), (74, HALF), (72, HALF)],
    [(71, QUARTER), (69, HALF+EIGHTH), (67, EIGHTH), (65, HALF+QUARTER), (None, QUARTER)],
]
for pi, phrase in enumerate(v1_phrases):
    voice_v2(bt(b + pi * 2), phrase, vel=48 + pi, bar_num=pi)

b = 24

# --- CHORUS 1 (8 bars) ---
for i in range(8):
    ci = (i // 2) % 4
    next_ci = ((i + 2) // 2) % 4
    voicing = get_voicing(CHORUS_VOICINGS, ci, i)

    piano_arpeggio_v2(bt(b + i), voicing, vel=56, bar_num=i + 8)

    if i % 2 == 0:
        synth_pad_v2(bt(b + i), get_voicing(CHORUS_VOICINGS, ci, i + 1), vel=48, bars=2, bar_num=i)

    bass_v2(bt(b + i), CHORUS_BASS[ci], vel=46, bar_num=i,
            pattern='half', next_root=CHORUS_BASS[next_ci])
    drums_v2(bt(b + i), 'chorus', bar_num=i)

# Chorus melody — more open, leaping intervals
chorus_phrases = [
    [(69, QUARTER), (72, HALF+EIGHTH), (76, EIGHTH), (74, HALF), (None, HALF)],
    [(74, QUARTER), (72, QUARTER+EIGHTH), (69, EIGHTH), (67, HALF), (None, HALF)],
    [(72, QUARTER), (74, HALF), (76, QUARTER), (77, HALF), (76, HALF)],
    [(74, QUARTER), (72, HALF+EIGHTH), (69, EIGHTH), (67, HALF+QUARTER), (None, QUARTER)],
]
for pi, phrase in enumerate(chorus_phrases):
    voice_v2(bt(b + pi * 2), phrase, vel=56, bar_num=pi + 16)

# Synth lead counter-melody — rewritten with more expression
lead_phrases = [
    [(76, HALF), (77, HALF+EIGHTH), (79, EIGHTH+QUARTER), (None, QUARTER)],
    [(77, QUARTER), (76, QUARTER+EIGHTH), (74, EIGHTH), (None, BAR4)],
    [(79, HALF), (77, HALF+EIGHTH), (76, EIGHTH), (None, HALF)],
    [(77, QUARTER), (76, QUARTER+EIGHTH), (74, EIGHTH), (72, WHOLE)],
]
for pi, phrase in enumerate(lead_phrases):
    synth_lead_v2(bt(b + pi * 2), phrase, vel=42, bar_num=pi)

b = 32

# --- VERSE 2 (16 bars) — Fuller from start ---
for i in range(16):
    ci = (i // 2) % 4
    next_ci = ((i + 1) // 2) % 4
    voicing = get_voicing(VERSE_VOICINGS, ci, i + 16)

    piano_arpeggio_v2(bt(b + i), voicing, vel=53, bar_num=i + 16)

    if i % 2 == 0:
        synth_pad_v2(bt(b + i), get_voicing(VERSE_VOICINGS, ci, i + 3), vel=40, bars=2, bar_num=i)

    pattern = 'half' if i >= 8 else 'whole'
    bass_v2(bt(b + i), VERSE_BASS[ci], vel=43, bar_num=i, pattern=pattern,
            next_root=VERSE_BASS[next_ci])
    drums_v2(bt(b + i), 'verse', bar_num=i + 16)

v2_phrases = [
    [(72, HALF), (69, QUARTER+EIGHTH), (67, EIGHTH), (65, HALF), (None, HALF)],
    [(67, QUARTER), (69, HALF+EIGHTH), (67, EIGHTH), (64, HALF), (None, HALF)],
    [(65, QUARTER), (67, QUARTER), (69, HALF), (72, QUARTER), (74, QUARTER+HALF)],
    [(72, QUARTER), (69, HALF+EIGHTH), (67, EIGHTH), (65, HALF+QUARTER), (None, QUARTER)],
    [(74, QUARTER), (72, QUARTER+EIGHTH), (69, EIGHTH), (67, HALF), (None, HALF)],
    [(69, QUARTER), (67, EIGHTH), (65, EIGHTH), (64, HALF), (65, HALF+EIGHTH), (None, QUARTER+EIGHTH)],
    [(67, QUARTER), (69, HALF), (72, QUARTER), (74, HALF), (76, HALF)],
    [(74, QUARTER), (72, HALF+EIGHTH), (69, EIGHTH), (67, HALF+QUARTER), (None, QUARTER)],
]
for pi, phrase in enumerate(v2_phrases):
    voice_v2(bt(b + pi * 2), phrase, vel=51 + pi, bar_num=pi + 24)

b = 48

# --- CHORUS 2 (8 bars) — With organ added ---
for i in range(8):
    ci = (i // 2) % 4
    next_ci = ((i + 2) // 2) % 4
    voicing = get_voicing(CHORUS_VOICINGS, ci, i + 8)

    piano_arpeggio_v2(bt(b + i), voicing, vel=58, bar_num=i + 32)

    if i % 2 == 0:
        synth_pad_v2(bt(b + i), get_voicing(CHORUS_VOICINGS, ci, i + 5), vel=50, bars=2, bar_num=i)

    # Organ added
    if i % 4 == 0:
        organ_v2(bt(b + i), get_voicing(CHORUS_VOICINGS, ci, i), vel=32, bars=4, bar_num=i)

    bass_v2(bt(b + i), CHORUS_BASS[ci], vel=48, bar_num=i + 8,
            pattern='melodic', next_root=CHORUS_BASS[next_ci])
    drums_v2(bt(b + i), 'chorus', bar_num=i + 8)

for pi, phrase in enumerate(chorus_phrases):
    voice_v2(bt(b + pi * 2), phrase, vel=58, bar_num=pi + 32)
for pi, phrase in enumerate(lead_phrases):
    synth_lead_v2(bt(b + pi * 2), phrase, vel=45, bar_num=pi + 8)

b = 56

# --- BRIDGE (8 bars) — Stripped back, piano + pad, rubato feel ---
for i in range(8):
    ci = (i // 2) % 4
    voicing = get_voicing(BRIDGE_VOICINGS, ci, i)

    # Slower arpeggios — quarter notes with more timing freedom
    notes = voicing + [voicing[0] + 12]
    E.cc(0, 64, 110, h_time(bt(b + i), 3))  # sustain pedal
    for j in range(4):
        note = notes[j % len(notes)]
        t = bt(b + i) + j * QUARTER
        v = breathing_vel(43, i + j, 4, 5)
        v = v if j in [0, 2] else v - 6
        # More timing freedom in bridge (rubato)
        E.note(0, note, v, t, QUARTER - 25, time_amount=15, vel_amount=5)
    E.cc(0, 64, 0, h_time(bt(b + i) + BAR4 - 30, 3))

    if i % 2 == 0:
        synth_pad_v2(bt(b + i), voicing, vel=35, bars=2, bar_num=i + 40)

# Bridge melody — the most vulnerable
bridge_melody = [
    [(74, HALF), (76, HALF+EIGHTH), (77, EIGHTH+QUARTER), (None, QUARTER)],
    [(76, QUARTER), (74, HALF+EIGHTH), (72, EIGHTH), (69, HALF+QUARTER), (None, QUARTER)],
    [(72, HALF), (74, HALF), (76, HALF+QUARTER), (None, QUARTER)],
    [(74, QUARTER), (72, HALF+EIGHTH), (69, EIGHTH), (67, HALF+QUARTER), (None, QUARTER)],
]
for pi, phrase in enumerate(bridge_melody):
    voice_v2(bt(b + pi * 2), phrase, vel=45, bar_num=pi + 40)

b = 64

# --- OUTRO (12 bars) — Gradual dissolution ---
for i in range(12):
    ci = i % 4
    voicing = get_voicing(VERSE_VOICINGS, ci, i + 50)
    vel = max(25, 48 - i * 2)

    if i < 8:
        piano_arpeggio_v2(bt(b + i), voicing, vel=vel, bar_num=i + 50)
    else:
        # Last 4 bars: whole chords dying away
        E.cc(0, 64, 100, h_time(bt(b + i), 3))
        for n in voicing:
            E.note(0, n, vel - 5, bt(b + i), BAR4 - 30, time_amount=12, vel_amount=5)
        E.cc(0, 64, 0, h_time(bt(b + i) + BAR4 - 30, 3))

    if i < 6 and i % 2 == 0:
        synth_pad_v2(bt(b + i), voicing, vel=max(20, 33 - i * 3), bars=2, bar_num=i + 50)

    if i < 4:
        bass_v2(bt(b + i), VERSE_BASS[ci], vel=max(25, 38 - i * 5), bar_num=i + 50, pattern='whole')

# Final shimmer
E.note(1, N('G',5), 22, bt(b + 8), BAR4 * 4 - 20, time_amount=15, vel_amount=3)


# ============================================================
# OUTPUT
# ============================================================

build_midi(E, 'Dial Tone Lullaby', bpm=72, total_bars=76,
           output_path='/home/user/music/compositions/v2/01_dial_tone_lullaby.mid')
