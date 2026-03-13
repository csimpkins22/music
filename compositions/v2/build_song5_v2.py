#!/usr/bin/env python3
"""
Song 5 v2: "Peripheral Glow"
Key: D minor (relative major F) | Tempo: 70 BPM | 4/4 | ~5:00

Dreamy, atmospheric piece channeling "The Crystal Lake" — built on a pedal tone
with hypnotic motion and drifting texture.

v2 improvements:
- Organ drone with subtle pitch bend wobble for analog warmth
- 16th-note synth arpeggio with pattern variation (6 patterns) and velocity contouring
- Clean guitar with varied voicings (sus2, add9, min7 alternatives)
- Bass with descending chromatic walk in instrumental section
- Drums enter only at chorus with ghost notes and varied patterns
- Distorted guitar with fuzzy power chords in instrumental, Jazzmaster-style
- Vocal melody with grace notes, anticipations, and contour-based dynamics
- Expression swells (CC11) on synth pad
- Sustain pedal (CC64) on piano
- Bridge/instrumental: augmented climb feel with pitch bend on lead
- Breathing velocity undulation across all instruments
- Ambient intro with pure organ drone + filtered synth arpeggio
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from humanize import *

E = EventList()

BPM = 70

def bt(bar_num):
    return bar_num * BAR4

# === CHORD VOICINGS ===
# Verse: Dm → F → C → Gm (with pedal D implied)
VERSE_VOICINGS = [
    [make_chord(N('D',4), 'minor'), make_chord(N('D',4), 'min7'), [N('D',4), N('F',4), N('A',4), N('D',5)]],
    [make_chord(N('F',4), 'major'), make_chord(N('F',4), 'add9'), [N('F',4), N('A',4), N('C',5)]],
    [make_chord(N('C',4), 'major'), make_chord(N('C',4), 'sus2'), make_chord(N('C',4), 'add9')],
    [make_chord(N('G',4), 'minor'), make_chord(N('G',4), 'min7'), [N('G',4), N('Bb',4), N('D',5)]],
]

# Chorus: Bb → F → C → Dm
CHORUS_VOICINGS = [
    [make_chord(N('Bb',3), 'major'), make_chord(N('Bb',3), 'add9'), [N('Bb',3), N('D',4), N('F',4)]],
    [make_chord(N('F',4), 'major'), make_chord(N('F',4), 'add9')],
    [make_chord(N('C',4), 'major'), make_chord(N('C',4), 'sus4'), make_chord(N('C',4), 'add9')],
    [make_chord(N('D',4), 'minor'), make_chord(N('D',4), 'min7')],
]

# Instrumental: Dm → Dm/C → Bb → A (descending bass, augmented climb feeling)
INSTR_VOICINGS = [
    [make_chord(N('D',4), 'minor'), [N('D',4), N('F',4), N('A',4), N('D',5)]],
    [[N('C',4), N('D',4), N('F',4), N('A',4)], [N('C',4), N('F',4), N('A',4)]],  # Dm/C
    [make_chord(N('Bb',3), 'major'), [N('Bb',3), N('D',4), N('F',4), N('Bb',4)]],
    [make_chord(N('A',3), 'major'), [N('A',3), N('Db',4), N('E',4), N('A',4)]],  # A major (borrowed, creates tension)
]

VERSE_BASS = [N('D',2), N('F',2), N('C',2), N('G',2)]
CHORUS_BASS = [N('Bb',1), N('F',2), N('C',2), N('D',2)]
INSTR_BASS = [N('D',2), N('C',2), N('Bb',1), N('A',1)]  # descending

# Verse 3 sparse: same as verse
VERSE3_BASS = VERSE_BASS

def get_voicing(voicings, chord_idx, bar_num):
    options = voicings[chord_idx]
    return options[bar_num % len(options)]


# ============================================================
# SONG STRUCTURE (88 bars total at 70 BPM ≈ 5:02)
# ============================================================
# Ambient intro: bars 0-7 (8 bars)
# Verse 1: bars 8-23 (16 bars)
# Chorus 1: bars 24-31 (8 bars)
# Verse 2: bars 32-47 (16 bars)
# Chorus 2: bars 48-55 (8 bars)
# Extended instrumental: bars 56-71 (16 bars)
# Verse 3 sparse: bars 72-79 (8 bars)
# Outro fade: bars 80-87 (8 bars)

INTRO = (0, 8)
V1 = (8, 24)
CH1 = (24, 32)
V2 = (32, 48)
CH2 = (48, 56)
INSTR = (56, 72)
V3 = (72, 80)
OUTRO = (80, 88)


# ============================================================
# ORGAN DRONE (Ch 5) — D pedal throughout verses, chord root elsewhere
# ============================================================
def organ_drone():
    """Sustained organ drone — the hypnotic bed of the song."""
    # Intro: pure D drone, very quiet, building
    for bar in range(INTRO[0], INTRO[1]):
        t = bt(bar)
        vel = 30 + bar * 3  # slowly getting louder
        vel = breathing_vel(vel, bar, cycle_bars=8, depth=3)
        E.note(5, N('D',3), vel, t, BAR4 - EIGHTH, time_amount=5, vel_amount=3)
        # Add fifth for richness after bar 4
        if bar >= 4:
            E.note(5, N('A',3), vel - 8, t, BAR4 - EIGHTH, time_amount=5, vel_amount=3)
        # Subtle pitch bend wobble for analog feel
        for q in range(4):
            bend_val = random.randint(-200, 200)
            E.pitch_bend(5, bend_val, t + q * QUARTER + random.randint(0, 40))

    # Verses: D pedal drone
    for section in [V1, V2, V3]:
        for bar in range(section[0], section[1]):
            t = bt(bar)
            vel = 42 if section != V3 else 35
            vel = breathing_vel(vel, bar, cycle_bars=8, depth=4)
            E.note(5, N('D',3), vel, t, BAR4 - EIGHTH, time_amount=5, vel_amount=3)
            E.note(5, N('A',3), vel - 6, t, BAR4 - EIGHTH, time_amount=5, vel_amount=3)
            # Pitch bend wobble
            for q in range(4):
                bend_val = random.randint(-250, 250)
                E.pitch_bend(5, bend_val, t + q * QUARTER + random.randint(0, 50))

    # Choruses: follow chord root
    for section in [CH1, CH2]:
        for bar in range(section[0], section[1]):
            t = bt(bar)
            chord_idx = (bar - section[0]) % 4
            root = CHORUS_BASS[chord_idx]
            vel = 50
            vel = breathing_vel(vel, bar, cycle_bars=8, depth=4)
            E.note(5, root + 12, vel, t, BAR4 - EIGHTH, time_amount=5, vel_amount=3)
            E.note(5, root + 19, vel - 6, t, BAR4 - EIGHTH, time_amount=5, vel_amount=3)
            for q in range(4):
                bend_val = random.randint(-200, 200)
                E.pitch_bend(5, bend_val, t + q * QUARTER + random.randint(0, 40))

    # Instrumental: follow descending bass
    for bar in range(INSTR[0], INSTR[1]):
        t = bt(bar)
        chord_idx = (bar - INSTR[0]) % 4
        root = INSTR_BASS[chord_idx]
        vel = 55 + (bar - INSTR[0])  # gradually louder
        vel = min(70, vel)
        vel = breathing_vel(vel, bar, cycle_bars=8, depth=4)
        E.note(5, root + 12, vel, t, BAR4 - EIGHTH, time_amount=5, vel_amount=3)
        E.note(5, root + 19, vel - 6, t, BAR4 - EIGHTH, time_amount=5, vel_amount=3)
        for q in range(4):
            bend_val = random.randint(-300, 300)
            E.pitch_bend(5, bend_val, t + q * QUARTER + random.randint(0, 40))

    # Outro: D drone fading
    for bar in range(OUTRO[0], OUTRO[1]):
        t = bt(bar)
        vel = max(20, 45 - (bar - OUTRO[0]) * 3)
        E.note(5, N('D',3), vel, t, BAR4 - EIGHTH, time_amount=5, vel_amount=3)
        E.note(5, N('A',3), vel - 8, t, BAR4 - EIGHTH, time_amount=5, vel_amount=3)
        for q in range(4):
            bend_val = random.randint(-150, 150)
            E.pitch_bend(5, bend_val, t + q * QUARTER + random.randint(0, 40))


# ============================================================
# SYNTH ARPEGGIO (Ch 2) — 16th note hypnotic motion
# ============================================================
def synth_arpeggio():
    """Hypnotic 16th-note synth arpeggio — the signature texture."""

    # 6 different 16th-note patterns (indices into chord tones + octave)
    patterns = [
        [0,1,2,3, 2,1,0,3, 0,2,1,3, 2,0,3,1],    # wave-like
        [0,2,1,3, 0,3,1,2, 0,2,3,1, 0,1,3,2],    # skippy
        [3,2,1,0, 3,1,2,0, 3,2,0,1, 3,0,1,2],    # descending focus
        [0,1,0,2, 0,1,0,3, 0,2,0,3, 0,1,0,2],    # pedal tone pattern
        [0,3,1,2, 3,0,2,1, 0,3,2,1, 3,0,1,2],    # wide jumps
        [0,1,2,1, 0,2,3,2, 0,1,3,1, 0,2,3,1],    # gentle undulation
    ]

    def arp_bar(bar, chord_notes, vel_base, pattern_idx):
        t = bt(bar)
        notes = list(chord_notes)
        # Extend to 4 notes if needed
        while len(notes) < 4:
            notes.append(notes[0] + 12)
        # Transpose up an octave for shimmer
        notes = [n + 12 for n in notes[:4]]

        pat = patterns[pattern_idx % len(patterns)]
        for i, idx in enumerate(pat):
            note_t = t + i * SIXTEENTH
            # Velocity contouring: subtle accents on beat positions
            beat_pos = i % 4
            vel = vel_base + accent_beat(beat_pos // 1, 'natural')
            vel = breathing_vel(vel, bar, cycle_bars=8, depth=4)
            # Staccato 16ths
            dur = SIXTEENTH - random.randint(15, 40)
            E.note(2, notes[idx % len(notes)], vel, note_t, dur, time_amount=6, vel_amount=3)

    # Intro: arpeggio fades in on Dm
    dm_notes = make_chord(N('D',4), 'minor')
    for bar in range(INTRO[0] + 2, INTRO[1]):  # starts bar 2
        vel = 25 + (bar - INTRO[0]) * 4
        arp_bar(bar, dm_notes, vel, bar)

    # Verses
    for section in [V1, V2]:
        for bar in range(section[0], section[1]):
            chord_idx = (bar - section[0]) % 4
            chord = get_voicing(VERSE_VOICINGS, chord_idx, bar)
            vel = 45
            arp_bar(bar, chord, vel, bar)

    # Choruses — slightly louder, different pattern emphasis
    for section in [CH1, CH2]:
        for bar in range(section[0], section[1]):
            chord_idx = (bar - section[0]) % 4
            chord = get_voicing(CHORUS_VOICINGS, chord_idx, bar)
            vel = 52
            arp_bar(bar, chord, vel, bar + 3)  # offset pattern selection

    # Instrumental — loudest, most intense
    for bar in range(INSTR[0], INSTR[1]):
        chord_idx = (bar - INSTR[0]) % 4
        chord = get_voicing(INSTR_VOICINGS, chord_idx, bar)
        vel = 50 + min(15, (bar - INSTR[0]))
        arp_bar(bar, chord, vel, bar + 1)

    # Verse 3 sparse — quieter, every other bar has gaps
    for bar in range(V3[0], V3[1]):
        chord_idx = (bar - V3[0]) % 4
        chord = get_voicing(VERSE_VOICINGS, chord_idx, bar)
        if bar % 2 == 0:
            arp_bar(bar, chord, 35, bar)
        else:
            # Only first half of bar
            t = bt(bar)
            notes = list(chord)
            while len(notes) < 4:
                notes.append(notes[0] + 12)
            notes = [n + 12 for n in notes[:4]]
            pat = patterns[bar % len(patterns)]
            for i in range(8):  # only first 8 sixteenths
                note_t = t + i * SIXTEENTH
                vel = breathing_vel(30, bar, cycle_bars=8, depth=3)
                dur = SIXTEENTH - random.randint(15, 40)
                E.note(2, notes[pat[i] % len(notes)], vel, note_t, dur, time_amount=6, vel_amount=3)

    # Outro — fading away
    for bar in range(OUTRO[0], OUTRO[1]):
        chord = make_chord(N('D',4), 'minor')
        vel = max(20, 40 - (bar - OUTRO[0]) * 3)
        if bar < OUTRO[1] - 2:  # stops 2 bars before end
            arp_bar(bar, chord, vel, bar)


# ============================================================
# SYNTH PAD (Ch 1) — warm bed with expression swells
# ============================================================
def synth_pad():
    """Warm synth pad — Juno-60 style sustained chords with CC11 expression swells."""

    def pad_section(start, end, voicings, vel_base, swell=True):
        for bar in range(start, end):
            t = bt(bar)
            chord_idx = (bar - start) % 4
            chord = get_voicing(voicings, chord_idx, bar)
            vel = breathing_vel(vel_base, bar, cycle_bars=8, depth=5)

            for note in chord:
                E.note(1, note, vel, t, BAR4 - EIGHTH, time_amount=5, vel_amount=4)

            # Expression swells (CC11) — crescendo over 2-bar phrases
            if swell:
                phase_in_phrase = (bar - start) % 4
                for q in range(4):
                    expr_tick = t + q * QUARTER
                    if phase_in_phrase < 2:
                        expr_val = 70 + phase_in_phrase * 15 + q * 4
                    else:
                        expr_val = 100 - (phase_in_phrase - 2) * 15 - q * 4
                    expr_val = max(60, min(120, expr_val))
                    E.cc(1, 11, expr_val, expr_tick)

    # Intro: very quiet pad from bar 4
    for bar in range(INTRO[0] + 4, INTRO[1]):
        t = bt(bar)
        chord = make_chord(N('D',4), 'minor')
        vel = 25 + (bar - INTRO[0] - 4) * 5
        for note in chord:
            E.note(1, note, vel, t, BAR4 - EIGHTH, time_amount=5, vel_amount=3)

    pad_section(V1[0], V1[1], VERSE_VOICINGS, 45)
    pad_section(CH1[0], CH1[1], CHORUS_VOICINGS, 55)
    pad_section(V2[0], V2[1], VERSE_VOICINGS, 48)
    pad_section(CH2[0], CH2[1], CHORUS_VOICINGS, 58)
    pad_section(INSTR[0], INSTR[1], INSTR_VOICINGS, 55)
    pad_section(V3[0], V3[1], VERSE_VOICINGS, 35, swell=False)

    # Outro pad: D minor fading
    for bar in range(OUTRO[0], OUTRO[1]):
        t = bt(bar)
        chord = make_chord(N('D',4), 'minor')
        vel = max(18, 40 - (bar - OUTRO[0]) * 3)
        for note in chord:
            E.note(1, note, vel, t, BAR4 - EIGHTH, time_amount=5, vel_amount=3)


# ============================================================
# CLEAN GUITAR (Ch 3) — sparse atmospheric chords
# ============================================================
def clean_guitar():
    """Clean guitar playing sparse, ringing chords — enters at verse 1."""

    # Fingerpicking patterns (beat positions within a bar)
    patterns = [
        # pattern: list of (beat_offset, chord_tone_index, vel_offset)
        [(0, 0, 0), (QUARTER, 2, -5), (HALF, 1, -3), (HALF + QUARTER, 2, -7)],
        [(0, 0, 0), (EIGHTH, 1, -8), (QUARTER, 2, -5), (HALF, 0, -3), (HALF + QUARTER, 1, -6)],
        [(0, 0, 3), (HALF, 2, -5), (HALF + QUARTER, 1, -7)],  # sparser
        [(0, 0, 0), (DOTTED_QUARTER, 1, -5), (HALF, 2, -3), (DOTTED_QUARTER + HALF, 0, -6)],
    ]

    def guitar_bar(bar, chord_notes, vel_base, pattern_idx):
        t = bt(bar)
        pat = patterns[pattern_idx % len(patterns)]
        notes = list(chord_notes)
        while len(notes) < 3:
            notes.append(notes[0] + 12)

        vel = breathing_vel(vel_base, bar, cycle_bars=8, depth=4)
        for offset, tone_idx, vel_off in pat:
            n = notes[tone_idx % len(notes)]
            v = vel + vel_off + accent_beat((offset // QUARTER) % 4)
            # Longer sustain for clean guitar — let it ring
            dur = QUARTER + EIGHTH + random.randint(-20, 40)
            E.note(3, n, v, t + offset, dur, time_amount=8, vel_amount=4)

    # Verse 1 — sparse fingerpicking
    for bar in range(V1[0], V1[1]):
        chord_idx = (bar - V1[0]) % 4
        chord = get_voicing(VERSE_VOICINGS, chord_idx, bar)
        guitar_bar(bar, chord, 48, bar)

    # Chorus 1 — slightly fuller
    for bar in range(CH1[0], CH1[1]):
        chord_idx = (bar - CH1[0]) % 4
        chord = get_voicing(CHORUS_VOICINGS, chord_idx, bar)
        guitar_bar(bar, chord, 52, bar)

    # Verse 2
    for bar in range(V2[0], V2[1]):
        chord_idx = (bar - V2[0]) % 4
        chord = get_voicing(VERSE_VOICINGS, chord_idx, bar)
        guitar_bar(bar, chord, 50, bar)

    # Chorus 2
    for bar in range(CH2[0], CH2[1]):
        chord_idx = (bar - CH2[0]) % 4
        chord = get_voicing(CHORUS_VOICINGS, chord_idx, bar)
        guitar_bar(bar, chord, 55, bar)

    # Verse 3 sparse — every other bar
    for bar in range(V3[0], V3[1]):
        if bar % 2 == 0:
            chord_idx = (bar - V3[0]) % 4
            chord = get_voicing(VERSE_VOICINGS, chord_idx, bar)
            guitar_bar(bar, chord, 38, bar)


# ============================================================
# DISTORTED GUITAR (Ch 4) — fuzzy Jazzmaster, instrumental section
# ============================================================
def distorted_guitar():
    """Fuzzy distorted guitar — enters at instrumental section for the big moment."""

    # Instrumental section: power chords with Grandaddy's fuzzy-but-notey distortion
    for bar in range(INSTR[0], INSTR[1]):
        t = bt(bar)
        chord_idx = (bar - INSTR[0]) % 4
        root = INSTR_BASS[chord_idx]

        # Intensity ramps up over the 16 bars
        intensity = min(1.0, (bar - INSTR[0]) / 12.0)
        vel = int(55 + intensity * 25)
        vel = breathing_vel(vel, bar, cycle_bars=8, depth=5)

        # Power chord voicings vary
        if bar % 3 == 0:
            notes = make_chord(root + 24, 'power')
        elif bar % 3 == 1:
            notes = [root + 24, root + 31]  # root + fifth only
        else:
            notes = [root + 24, root + 31, root + 36]  # root + fifth + octave

        # First half of bar: sustained chord
        for n in notes:
            E.note(4, n, vel, t, HALF + QUARTER, time_amount=10, vel_amount=6)

        # Some bars: add a rhythmic hit on beat 4
        if bar % 4 >= 2:
            for n in notes:
                E.note(4, n, vel - 8, t + HALF + QUARTER, QUARTER - 30, time_amount=10, vel_amount=6)

    # Also enters for chorus 2 — lighter
    for bar in range(CH2[0], CH2[1]):
        t = bt(bar)
        chord_idx = (bar - CH2[0]) % 4
        root = CHORUS_BASS[chord_idx]
        vel = 50
        vel = breathing_vel(vel, bar, cycle_bars=4, depth=4)
        notes = make_chord(root + 24, 'power')
        # Whole notes — pad-like distortion bed
        for n in notes:
            E.note(4, n, vel, t, BAR4 - EIGHTH, time_amount=8, vel_amount=5)


# ============================================================
# BASS (Ch 6) — enters verse 1, descending walk in instrumental
# ============================================================
def bass_line():
    """Bass guitar — supportive, with chromatic approach notes and melodic fills."""

    def bass_bar(bar, root, vel_base, section_start, with_fills=False):
        t = bt(bar)
        vel = breathing_vel(vel_base, bar, cycle_bars=8, depth=4)
        bar_in_section = bar - section_start

        # Main note patterns vary
        if bar_in_section % 4 == 0:
            # Whole note
            E.note(6, root, vel + accent_beat(0), t, BAR4 - QUARTER, time_amount=6, vel_amount=3)
        elif bar_in_section % 4 == 1:
            # Half + half
            E.note(6, root, vel + accent_beat(0), t, HALF - EIGHTH, time_amount=6, vel_amount=3)
            E.note(6, root, vel + accent_beat(2) - 5, t + HALF, HALF - EIGHTH, time_amount=6, vel_amount=3)
        elif bar_in_section % 4 == 2:
            # Dotted half + quarter
            E.note(6, root, vel + accent_beat(0), t, DOTTED_HALF - EIGHTH, time_amount=6, vel_amount=3)
            # Chromatic approach to next chord root
            if with_fills:
                next_chord_idx = ((bar - section_start) // 1 + 1) % 4
                # approach note: semitone below next root
                E.note(6, root + random.choice([-1, 1, 2]), vel - 8, t + DOTTED_HALF, QUARTER - 30, time_amount=8, vel_amount=4)
            else:
                E.note(6, root + 7, vel - 6, t + DOTTED_HALF, QUARTER - 30, time_amount=6, vel_amount=3)
        else:
            # Quarter note pattern
            E.note(6, root, vel + accent_beat(0), t, QUARTER - 20, time_amount=6, vel_amount=3)
            E.note(6, root, vel + accent_beat(1) - 5, t + QUARTER, QUARTER - 20, time_amount=6, vel_amount=3)
            E.note(6, root + 7, vel + accent_beat(2) - 3, t + HALF, QUARTER - 20, time_amount=6, vel_amount=3)
            E.note(6, root, vel + accent_beat(3) - 5, t + HALF + QUARTER, QUARTER - 20, time_amount=6, vel_amount=3)

    # Verse 1 — enters bar 4 (not from the start)
    for bar in range(V1[0] + 4, V1[1]):
        chord_idx = (bar - V1[0]) % 4
        bass_bar(bar, VERSE_BASS[chord_idx], 55, V1[0], with_fills=True)

    # Chorus 1
    for bar in range(CH1[0], CH1[1]):
        chord_idx = (bar - CH1[0]) % 4
        bass_bar(bar, CHORUS_BASS[chord_idx], 60, CH1[0], with_fills=True)

    # Verse 2
    for bar in range(V2[0], V2[1]):
        chord_idx = (bar - V2[0]) % 4
        bass_bar(bar, VERSE_BASS[chord_idx], 58, V2[0], with_fills=True)

    # Chorus 2
    for bar in range(CH2[0], CH2[1]):
        chord_idx = (bar - CH2[0]) % 4
        bass_bar(bar, CHORUS_BASS[chord_idx], 62, CH2[0], with_fills=True)

    # Instrumental: descending bass walk — the key moment
    for bar in range(INSTR[0], INSTR[1]):
        t = bt(bar)
        chord_idx = (bar - INSTR[0]) % 4
        root = INSTR_BASS[chord_idx]
        vel = 60 + min(12, (bar - INSTR[0]))
        vel = breathing_vel(vel, bar, cycle_bars=8, depth=4)

        # More active bass in instrumental
        E.note(6, root, vel, t, QUARTER - 20, time_amount=6, vel_amount=3)
        E.note(6, root, vel - 5, t + QUARTER, QUARTER - 20, time_amount=6, vel_amount=3)
        E.note(6, root + 7, vel - 3, t + HALF, QUARTER - 20, time_amount=6, vel_amount=3)
        # Walk note to next chord
        next_root = INSTR_BASS[(chord_idx + 1) % 4]
        walk_note = root + (1 if next_root > root else -1)
        E.note(6, walk_note, vel - 8, t + HALF + QUARTER, QUARTER - 30, time_amount=8, vel_amount=4)

    # Verse 3 sparse
    for bar in range(V3[0], V3[1]):
        if bar % 2 == 0:
            chord_idx = (bar - V3[0]) % 4
            E.note(6, VERSE_BASS[chord_idx], 45, bt(bar), BAR4 - QUARTER, time_amount=6, vel_amount=3)

    # Outro — very sparse, fading
    for bar in range(OUTRO[0], OUTRO[0] + 4):
        vel = max(25, 45 - (bar - OUTRO[0]) * 5)
        E.note(6, N('D',2), vel, bt(bar), BAR4 - QUARTER, time_amount=6, vel_amount=3)


# ============================================================
# DRUMS (Ch 9) — enters at chorus, sparse and atmospheric
# ============================================================
def drums():
    """Drums — very sparse, enter only at chorus. Ghost notes and varied patterns."""
    KICK = 36
    SNARE = 38
    HH_CLOSED = 42
    HH_OPEN = 46
    RIDE = 51
    CRASH = 49
    RIMSHOT = 37
    TOM_LOW = 45
    TOM_MID = 47

    def chorus_pattern(bar, vel_base, section_start):
        t = bt(bar)
        bar_in_section = bar - section_start
        vel = breathing_vel(vel_base, bar, cycle_bars=8, depth=4)

        # Kick: beat 1 and 3, with variation
        E.note(9, KICK, vel + accent_beat(0), t, QUARTER, time_amount=6, vel_amount=4)
        if bar_in_section % 4 != 3:  # skip kick on beat 3 every 4th bar
            E.note(9, KICK, vel + accent_beat(2) - 3, t + HALF, QUARTER, time_amount=6, vel_amount=4)

        # Snare: beat 2 and 4
        E.note(9, SNARE, vel + accent_beat(1) + 3, t + QUARTER, QUARTER, time_amount=6, vel_amount=5)
        E.note(9, SNARE, vel + accent_beat(3), t + HALF + QUARTER, QUARTER, time_amount=6, vel_amount=5)

        # Hi-hat: 8th notes with variation
        for i in range(8):
            hh_t = t + i * EIGHTH
            hh_vel = vel - 15 + swing_offset(i, amount=12)
            # Occasional open hi-hat
            if i == 4 and bar_in_section % 3 == 0:
                E.note(9, HH_OPEN, hh_vel + 5, hh_t, EIGHTH, time_amount=5, vel_amount=3)
            else:
                E.note(9, HH_CLOSED, hh_vel, hh_t, EIGHTH // 2, time_amount=5, vel_amount=3)

        # Ghost notes on snare
        if bar_in_section % 2 == 1:
            ghost_pos = random.choice([EIGHTH, HALF + EIGHTH, HALF + QUARTER + EIGHTH])
            E.note(9, SNARE, vel - 25, t + ghost_pos, EIGHTH, time_amount=8, vel_amount=3)

    def verse2_pattern(bar, vel_base, section_start):
        """Very sparse verse drums — just ride and occasional kick."""
        t = bt(bar)
        bar_in_section = bar - section_start
        vel = breathing_vel(vel_base, bar, cycle_bars=8, depth=3)

        # Ride on quarters
        for q in range(4):
            ride_vel = vel - 12 + accent_beat(q)
            E.note(9, RIDE, ride_vel, t + q * QUARTER, QUARTER, time_amount=6, vel_amount=3)

        # Kick only on beat 1
        E.note(9, KICK, vel - 5, t, QUARTER, time_amount=6, vel_amount=4)

        # Rimshot on beat 3 (instead of snare — more atmospheric)
        if bar_in_section % 2 == 0:
            E.note(9, RIMSHOT, vel - 10, t + HALF, QUARTER, time_amount=6, vel_amount=4)

    def fill(bar, vel_base):
        """Drum fill at section boundary."""
        t = bt(bar)
        vel = vel_base
        # Simple tom fill
        E.note(9, TOM_MID, vel, t + HALF, EIGHTH, time_amount=5, vel_amount=4)
        E.note(9, TOM_MID, vel - 3, t + HALF + EIGHTH, EIGHTH, time_amount=5, vel_amount=4)
        E.note(9, TOM_LOW, vel + 2, t + HALF + QUARTER, EIGHTH, time_amount=5, vel_amount=4)
        E.note(9, TOM_LOW, vel - 2, t + HALF + QUARTER + EIGHTH, EIGHTH, time_amount=5, vel_amount=4)

    # Chorus 1 — crash on entry
    E.note(9, CRASH, 75, bt(CH1[0]), HALF, time_amount=5, vel_amount=4)
    for bar in range(CH1[0], CH1[1]):
        chorus_pattern(bar, 65, CH1[0])
        if bar == CH1[1] - 1:
            fill(bar, 60)

    # Verse 2 — sparse ride pattern (drums don't fully drop out)
    for bar in range(V2[0] + 4, V2[1]):  # enters 4 bars in
        verse2_pattern(bar, 50, V2[0])

    # Chorus 2 — crash on entry
    E.note(9, CRASH, 78, bt(CH2[0]), HALF, time_amount=5, vel_amount=4)
    for bar in range(CH2[0], CH2[1]):
        chorus_pattern(bar, 68, CH2[0])
        if bar == CH2[1] - 1:
            fill(bar, 62)

    # Instrumental — builds to biggest drum moment
    E.note(9, CRASH, 80, bt(INSTR[0]), HALF, time_amount=5, vel_amount=4)
    for bar in range(INSTR[0], INSTR[1]):
        intensity = min(1.0, (bar - INSTR[0]) / 12.0)
        vel = int(60 + intensity * 20)
        chorus_pattern(bar, vel, INSTR[0])
        # Extra crash every 4 bars during build
        if (bar - INSTR[0]) % 4 == 0 and bar > INSTR[0]:
            E.note(9, CRASH, vel + 5, bt(bar), HALF, time_amount=5, vel_amount=4)
        if bar == INSTR[1] - 1:
            fill(bar, 70)


# ============================================================
# PIANO (Ch 0) — enters at verse 2, provides harmonic support
# ============================================================
def piano():
    """Piano — enters at verse 2, warm chords with sustain pedal."""

    def piano_chords(bar, chord_notes, vel_base, section_start, style='pads'):
        t = bt(bar)
        vel = breathing_vel(vel_base, bar, cycle_bars=8, depth=5)

        if style == 'pads':
            # Sustained chords, like piano pads
            # Sustain pedal on
            E.cc(0, 64, 127, t + 5)
            for note in chord_notes:
                E.note(0, note, vel, t, BAR4 - QUARTER, time_amount=6, vel_amount=4)
            # Pedal release at end of bar, re-engage next bar
            E.cc(0, 64, 0, t + BAR4 - EIGHTH)
        elif style == 'arpeggio':
            # Gentle arpeggio
            notes = list(chord_notes) + [chord_notes[0] + 12]
            E.cc(0, 64, 127, t + 5)
            patterns = [
                [0, 1, 2, 3, 2, 1, 0, 3],
                [0, 2, 1, 3, 0, 2, 3, 1],
                [3, 2, 1, 0, 1, 2, 3, 0],
            ]
            pat = patterns[bar % len(patterns)]
            for i, idx in enumerate(pat):
                note_t = t + i * EIGHTH
                n = notes[idx % len(notes)]
                v = vel - 5 + accent_beat(i % 4)
                E.note(0, n, v, note_t, QUARTER, time_amount=8, vel_amount=4)
            E.cc(0, 64, 0, t + BAR4 - EIGHTH)

    # Verse 2 — warm piano pads
    for bar in range(V2[0], V2[1]):
        chord_idx = (bar - V2[0]) % 4
        chord = get_voicing(VERSE_VOICINGS, chord_idx, bar)
        piano_chords(bar, chord, 48, V2[0], style='pads')

    # Chorus 2
    for bar in range(CH2[0], CH2[1]):
        chord_idx = (bar - CH2[0]) % 4
        chord = get_voicing(CHORUS_VOICINGS, chord_idx, bar)
        piano_chords(bar, chord, 55, CH2[0], style='pads')

    # Instrumental — arpeggiated piano emerges
    for bar in range(INSTR[0] + 4, INSTR[1]):
        chord_idx = (bar - INSTR[0]) % 4
        chord = get_voicing(INSTR_VOICINGS, chord_idx, bar)
        vel = 45 + min(15, (bar - INSTR[0] - 4))
        piano_chords(bar, chord, vel, INSTR[0], style='arpeggio')

    # Verse 3 — gentle arpeggios
    for bar in range(V3[0], V3[1]):
        chord_idx = (bar - V3[0]) % 4
        chord = get_voicing(VERSE_VOICINGS, chord_idx, bar)
        piano_chords(bar, chord, 38, V3[0], style='arpeggio')

    # Outro — very quiet piano pads, last sound along with organ
    for bar in range(OUTRO[0], OUTRO[1]):
        t = bt(bar)
        chord = make_chord(N('D',4), 'minor')
        vel = max(20, 38 - (bar - OUTRO[0]) * 2)
        E.cc(0, 64, 127, t + 5)
        for note in chord:
            E.note(0, note, vel, t, BAR4 - QUARTER, time_amount=6, vel_amount=3)
        E.cc(0, 64, 0, t + BAR4 - EIGHTH)


# ============================================================
# STRINGS (Ch 7) — orchestral swells in choruses and instrumental
# ============================================================
def strings():
    """String ensemble — swells in choruses, adds grandeur to instrumental."""

    def string_swell(bar, chord_notes, vel_base, swell_bars=2, phase=0):
        t = bt(bar)
        vel = vel_base
        # Expression swell over the chord
        for q in range(4):
            expr_tick = t + q * QUARTER
            swell_phase = (phase + q) / (swell_bars * 4)
            if swell_phase < 0.5:
                expr_val = int(60 + 50 * (swell_phase * 2))
            else:
                expr_val = int(110 - 50 * ((swell_phase - 0.5) * 2))
            expr_val = max(50, min(120, expr_val))
            E.cc(7, 11, expr_val, expr_tick)

        vel = breathing_vel(vel, bar, cycle_bars=8, depth=4)
        for note in chord_notes:
            E.note(7, note, vel, t, BAR4 - EIGHTH, time_amount=5, vel_amount=4)

    # Chorus 1 — gentle strings
    for bar in range(CH1[0], CH1[1]):
        chord_idx = (bar - CH1[0]) % 4
        chord = get_voicing(CHORUS_VOICINGS, chord_idx, bar)
        # Transpose up for brightness
        high_chord = [n + 12 for n in chord[:3]]
        string_swell(bar, high_chord, 42, swell_bars=2, phase=(bar - CH1[0]) % 4)

    # Chorus 2 — fuller
    for bar in range(CH2[0], CH2[1]):
        chord_idx = (bar - CH2[0]) % 4
        chord = get_voicing(CHORUS_VOICINGS, chord_idx, bar)
        high_chord = [n + 12 for n in chord[:3]]
        string_swell(bar, high_chord, 50, swell_bars=2, phase=(bar - CH2[0]) % 4)

    # Instrumental — biggest string presence
    for bar in range(INSTR[0] + 4, INSTR[1]):
        chord_idx = (bar - INSTR[0]) % 4
        chord = get_voicing(INSTR_VOICINGS, chord_idx, bar)
        high_chord = [n + 12 for n in chord[:3]]
        intensity = min(1.0, (bar - INSTR[0]) / 12.0)
        vel = int(45 + intensity * 25)
        string_swell(bar, high_chord, vel, swell_bars=2, phase=(bar - INSTR[0]) % 4)


# ============================================================
# VOCAL MELODY (Ch 8) — dreamy, floating melody
# ============================================================
def vocal_melody():
    """Vocal melody — dreamy, modal, floating above the texture."""

    # D natural minor scale: D E F G A Bb C D
    scale = [N('D',5), N('E',5), N('F',5), N('G',5), N('A',5), N('Bb',5), N('C',6), N('D',6)]

    def phrase(bar_start, notes_data, vel_base):
        """Play a melodic phrase. notes_data: list of (scale_idx, beat_offset, duration)."""
        t = bt(bar_start)
        for i, (scale_idx, beat_offset, dur) in enumerate(notes_data):
            note = scale[scale_idx % len(scale)]
            tick = t + beat_offset
            # Contour-based dynamics: higher notes louder
            vel = vel_base + (scale_idx - 3) * 2
            vel = breathing_vel(vel, bar_start, cycle_bars=8, depth=4)

            # Grace note occasionally (every ~5th note)
            if i % 5 == 3 and i > 0:
                grace = scale[(scale_idx - 1) % len(scale)]
                E.note(8, grace, vel - 15, tick - SIXTEENTH, SIXTEENTH - 10, time_amount=6, vel_amount=3)

            # Anticipation: occasionally start a sixteenth early
            if i % 7 == 4:
                tick -= SIXTEENTH
                dur += SIXTEENTH

            E.note(8, note, vel, tick, dur, time_amount=8, vel_amount=4)

    # Verse 1 phrases (4 phrases of 4 bars each)
    # Phrase 1: bars 8-11 — ascending opening
    phrase(8, [
        (0, 0, HALF),              # D - whole bar start
        (2, HALF + QUARTER, QUARTER),  # F
        (3, BAR4, HALF),           # G
        (4, BAR4 + HALF, QUARTER), # A
        (3, BAR4 * 2, DOTTED_HALF),# G — lingering
        (2, BAR4 * 3, HALF),       # F
        (0, BAR4 * 3 + HALF, HALF),# D — resolution
    ], 55)

    # Phrase 2: bars 12-15 — reaching higher
    phrase(12, [
        (4, 0, QUARTER),           # A
        (5, QUARTER, HALF),        # Bb — reaching
        (4, HALF + QUARTER, QUARTER),# A
        (3, BAR4, HALF),           # G
        (2, BAR4 + HALF, QUARTER), # F
        (4, BAR4 * 2, DOTTED_HALF),# A — peak
        (3, BAR4 * 2 + DOTTED_HALF, QUARTER),# G
        (2, BAR4 * 3, HALF),       # F
        (0, BAR4 * 3 + HALF, HALF),# D — rest
    ], 58)

    # Phrase 3: bars 16-19 — repeat-ish of phrase 1 with variation
    phrase(16, [
        (0, 0, HALF),              # D
        (2, HALF, QUARTER),        # F
        (3, HALF + QUARTER, QUARTER),# G
        (4, BAR4, HALF + QUARTER), # A — held longer
        (3, BAR4 + HALF + QUARTER, QUARTER),# G
        (2, BAR4 * 2, HALF),       # F
        (3, BAR4 * 2 + HALF, HALF),# G — different ending
        (2, BAR4 * 3, DOTTED_HALF),# F
        (0, BAR4 * 3 + DOTTED_HALF, QUARTER),# D
    ], 55)

    # Phrase 4: bars 20-23 — descending to resolution
    phrase(20, [
        (4, 0, HALF),              # A
        (3, HALF, QUARTER),        # G
        (2, HALF + QUARTER, QUARTER),# F
        (0, BAR4, WHOLE),          # D — long resolution
        (6, BAR4 * 2, HALF),       # C (upper) — surprise
        (5, BAR4 * 2 + HALF, QUARTER),# Bb
        (4, BAR4 * 2 + HALF + QUARTER, QUARTER),# A
        (3, BAR4 * 3, HALF),       # G — settle
        (2, BAR4 * 3 + HALF, HALF),# F
    ], 55)

    # Chorus 1: bars 24-31 — more sustained, emotional
    phrase(24, [
        (5, 0, DOTTED_HALF),       # Bb — big opening
        (4, DOTTED_HALF, QUARTER), # A
        (3, BAR4, HALF),           # G
        (4, BAR4 + HALF, HALF),    # A
        (5, BAR4 * 2, WHOLE),      # Bb — soaring
        (4, BAR4 * 3, HALF),       # A
        (3, BAR4 * 3 + HALF, HALF),# G
    ], 62)

    phrase(28, [
        (7, 0, DOTTED_HALF),       # D (high) — peak
        (6, DOTTED_HALF, QUARTER), # C
        (5, BAR4, HALF),           # Bb
        (4, BAR4 + HALF, HALF),    # A
        (3, BAR4 * 2, WHOLE),      # G — descent
        (2, BAR4 * 3, HALF),       # F
        (0, BAR4 * 3 + HALF, HALF),# D — home
    ], 65)

    # Verse 2: similar melodic material, slightly different contour
    phrase(32, [
        (0, 0, QUARTER),           # D — pickup
        (2, QUARTER, HALF),        # F
        (3, HALF + QUARTER, QUARTER),# G
        (4, BAR4, HALF),           # A
        (3, BAR4 + HALF, QUARTER), # G
        (2, BAR4 + HALF + QUARTER, QUARTER),# F
        (3, BAR4 * 2, DOTTED_HALF),# G
        (4, BAR4 * 3, HALF),       # A — different ending
        (5, BAR4 * 3 + HALF, HALF),# Bb
    ], 55)

    phrase(36, [
        (4, 0, HALF),              # A
        (3, HALF, QUARTER),        # G
        (4, HALF + QUARTER, QUARTER),# A
        (5, BAR4, DOTTED_HALF),    # Bb
        (4, BAR4 + DOTTED_HALF, QUARTER),# A
        (3, BAR4 * 2, HALF),       # G
        (2, BAR4 * 2 + HALF, HALF),# F
        (0, BAR4 * 3, WHOLE),      # D — rest
    ], 58)

    phrase(40, [
        (2, 0, HALF),              # F
        (3, HALF, QUARTER),        # G
        (4, HALF + QUARTER, QUARTER),# A
        (5, BAR4, HALF + QUARTER), # Bb — climax of verse
        (4, BAR4 + HALF + QUARTER, QUARTER),# A
        (3, BAR4 * 2, DOTTED_HALF),# G
        (2, BAR4 * 2 + DOTTED_HALF, QUARTER),# F
        (0, BAR4 * 3, WHOLE),      # D
    ], 58)

    phrase(44, [
        (3, 0, HALF),              # G — building to chorus
        (4, HALF, HALF),           # A
        (5, BAR4, QUARTER),        # Bb
        (4, BAR4 + QUARTER, QUARTER),# A
        (3, BAR4 + HALF, HALF),    # G
        (4, BAR4 * 2, DOTTED_HALF),# A — anticipation
        (5, BAR4 * 2 + DOTTED_HALF, QUARTER),# Bb
        (4, BAR4 * 3, HALF),       # A
        (3, BAR4 * 3 + HALF, HALF),# G
    ], 56)

    # Chorus 2: same as chorus 1 but slightly more intense
    phrase(48, [
        (5, 0, DOTTED_HALF),       # Bb
        (4, DOTTED_HALF, QUARTER), # A
        (3, BAR4, HALF),           # G
        (4, BAR4 + HALF, HALF),    # A
        (5, BAR4 * 2, WHOLE),      # Bb
        (4, BAR4 * 3, HALF),       # A
        (3, BAR4 * 3 + HALF, HALF),# G
    ], 65)

    phrase(52, [
        (7, 0, WHOLE),             # D (high) — peak held longer
        (6, BAR4, HALF),           # C
        (5, BAR4 + HALF, HALF),    # Bb
        (4, BAR4 * 2, DOTTED_HALF),# A
        (3, BAR4 * 2 + DOTTED_HALF, QUARTER),# G
        (2, BAR4 * 3, HALF),       # F
        (0, BAR4 * 3 + HALF, HALF),# D
    ], 68)

    # Verse 3 sparse: bars 72-79 — just fragments
    phrase(72, [
        (0, 0, WHOLE),             # D — alone
        (2, BAR4 * 2, HALF),       # F
        (3, BAR4 * 2 + HALF, HALF),# G
        (0, BAR4 * 3, WHOLE),      # D
    ], 42)

    phrase(76, [
        (4, 0, WHOLE),             # A — one last reach
        (3, BAR4, HALF),           # G
        (2, BAR4 + HALF, HALF),    # F
        (0, BAR4 * 2, WHOLE + HALF),# D — long final note
    ], 40)


# ============================================================
# SYNTH LEAD (Ch 2 — shares with arpeggio but higher register)
# uses a separate lead function on same channel during instrumental
# Actually, let's use a different approach: lead melody during
# instrumental on Ch 2 by pausing arpeggio — but arpeggio continues.
# Instead, use pitch bend for soaring quality.
# ============================================================
# The synth lead is already handled via the arpeggio.
# For the instrumental, we add pitch bend expression on Ch 2.
def synth_lead_expression():
    """Add pitch bend vibrato/expression to synth during instrumental."""
    for bar in range(INSTR[0], INSTR[1]):
        t = bt(bar)
        intensity = min(1.0, (bar - INSTR[0]) / 12.0)
        bend_depth = int(200 + intensity * 600)  # increasing vibrato depth

        # Vibrato: sinusoidal pitch bend
        for step in range(16):
            phase = step / 16.0 * 2 * 3.14159
            bend = int(bend_depth * math.sin(phase))
            E.pitch_bend(2, bend, t + step * SIXTEENTH)

    # Reset pitch bend after instrumental
    E.pitch_bend(2, 0, bt(INSTR[1]))


# ============================================================
# BUILD ALL PARTS
# ============================================================
organ_drone()
synth_arpeggio()
synth_pad()
clean_guitar()
distorted_guitar()
bass_line()
drums()
piano()
strings()
vocal_melody()
synth_lead_expression()

# ============================================================
# EXPORT MIDI
# ============================================================
import math

output_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(output_dir, '05_peripheral_glow.mid')

build_midi(
    E, 'Peripheral Glow', BPM,
    time_sig_num=4, time_sig_den=4,
    total_bars=88,
    channel_names={
        0: 'Piano',
        1: 'Synth Pad (Juno Warm)',
        2: 'Synth Arpeggio / Lead',
        3: 'Clean Guitar',
        4: 'Distorted Guitar (Jazzmaster Fuzz)',
        5: 'Organ Drone',
        6: 'Bass Guitar',
        7: 'String Ensemble',
        8: 'Vocal Melody',
        9: 'Drums',
    },
    channel_programs={
        0: 0,    # Acoustic Grand Piano
        1: 89,   # Pad 2 (Warm)
        2: 81,   # Lead 2 (Sawtooth)
        3: 27,   # Electric Guitar (Clean)
        4: 30,   # Overdriven Guitar
        5: 19,   # Church Organ
        6: 33,   # Electric Bass (Finger)
        7: 49,   # String Ensemble 1
        8: 85,   # Lead 6 (Voice)
    },
    output_path=output_path,
)
