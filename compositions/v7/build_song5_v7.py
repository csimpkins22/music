#!/usr/bin/env python3
"""
Song 5 v7: "Peripheral Glow"
Key: D minor (relative major F) | Tempo: 70 BPM | 4/4 | ~5:08

Dreamy, atmospheric piece channeling "The Crystal Lake" — built on a pedal tone
with hypnotic motion and drifting texture.

v7 changes (final polish):
1. Outro organ wobble ending: last bar wobble reduced to +/-50 cents (was 400) — signal "returns to earth" before disappearing
2. Bass grounding in outro: quiet bass D2 across final 4 bars (vel=18 fading to 12) — tonic anchor under the wobbling organ
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from humanize import *

E = EventList()

BPM = 70

def bt(bar_num):
    return bar_num * BAR4


# === CHORD VOICINGS ===

# Verse: Dm -> F -> C -> Gm (unchanged — strong foundation)
VERSE_VOICINGS = [
    [make_chord(N('D',4), 'minor'), make_chord(N('D',4), 'min7'), [N('D',4), N('F',4), N('A',4), N('D',5)]],
    [make_chord(N('F',4), 'major'), make_chord(N('F',4), 'add9'), [N('F',4), N('A',4), N('C',5)]],
    [make_chord(N('C',4), 'major'), make_chord(N('C',4), 'sus2'), make_chord(N('C',4), 'add9')],
    [make_chord(N('G',4), 'minor'), make_chord(N('G',4), 'min7'), [N('G',4), N('Bb',4), N('D',5)]],
]

# Chorus: Bb -> F -> A7 -> Dm
# A7 = A C# E (G) — the dominant V of Dm. C# is the raised 7th from harmonic minor.
# This creates a real cadential pull: A7 -> Dm with the leading tone C# resolving to D.
CHORUS_VOICINGS = [
    [make_chord(N('Bb',3), 'major'), make_chord(N('Bb',3), 'add9'), [N('Bb',3), N('D',4), N('F',4)]],
    [make_chord(N('F',4), 'major'), make_chord(N('F',4), 'add9')],
    # A7: A major triad (A C# E) — the dominant chord. The C# against D minor context is electric.
    [make_chord(N('A',3), 'major'), [N('A',3), N('Db',4), N('E',4), N('A',4)]],
    [make_chord(N('D',4), 'minor'), make_chord(N('D',4), 'min7')],
]

# Instrumental: Dm -> Dm/C -> Bb -> Gm/Bb (passing) -> A (extended 2 bars)
# Creates chromatic bass descent: D - C - Bb - Bb - A
INSTR_VOICINGS_5 = [
    # Dm
    [make_chord(N('D',4), 'minor'), [N('D',4), N('F',4), N('A',4), N('D',5)]],
    # Dm/C (C in bass)
    [[N('C',4), N('D',4), N('F',4), N('A',4)], [N('C',4), N('F',4), N('A',4)]],
    # Bb major
    [make_chord(N('Bb',3), 'major'), [N('Bb',3), N('D',4), N('F',4), N('Bb',4)]],
    # Gm/Bb (Bb bass under Gm — passing chord for smooth chromatic descent)
    [[N('Bb',3), N('D',4), N('G',4)], [N('Bb',3), N('G',4), N('Bb',4), N('D',5)]],
    # A major — let it hang for 2 bars. Major chord in minor key context.
    [make_chord(N('A',3), 'major'), [N('A',3), N('Db',4), N('E',4), N('A',4)]],
]

INSTR_BASS_5 = [N('D',2), N('C',2), N('Bb',1), N('Bb',1), N('A',1)]
# The 5-chord cycle maps: bar%6 -> 0:Dm, 1:Dm/C, 2:Bb, 3:Gm/Bb, 4:A, 5:A(extended)

def instr_chord_idx(bar_in_section):
    """Map bar position to the 6-bar instrumental cycle:
    0=Dm, 1=Dm/C, 2=Bb, 3=Gm/Bb, 4=A, 5=A(extended)"""
    return bar_in_section % 6

def get_instr_voicing(bar_in_section, bar_num):
    idx = instr_chord_idx(bar_in_section)
    if idx == 5:
        idx = 4  # second bar of A major uses same voicing
    options = INSTR_VOICINGS_5[idx]
    return options[bar_num % len(options)]

def get_instr_bass(bar_in_section):
    idx = instr_chord_idx(bar_in_section)
    if idx == 5:
        return N('A',1)  # second bar of A
    return INSTR_BASS_5[idx]

VERSE_BASS = [N('D',2), N('F',2), N('C',2), N('G',2)]
CHORUS_BASS = [N('Bb',1), N('F',2), N('A',1), N('D',2)]  # A bass for A7 chord
VERSE3_BASS = VERSE_BASS

def get_voicing(voicings, chord_idx, bar_num):
    options = voicings[chord_idx]
    return options[bar_num % len(options)]


# ============================================================
# SONG STRUCTURE (90 bars total at 70 BPM ~ 5:08)
# ============================================================
# Ambient intro:      bars  0-7   (8 bars)
# Verse 1:            bars  8-23  (16 bars)
# Chorus 1:           bars 24-31  (8 bars)
# Verse 2:            bars 32-47  (16 bars)
# Chorus 2:           bars 48-55  (8 bars)
# Silence (drone):    bars 56-57  (2 bars) — everything drops out except organ
# Extended instr:     bars 58-73  (16 bars)
# Verse 3 sparse:     bars 74-81  (8 bars)
# Outro fade:         bars 82-89  (8 bars)

INTRO = (0, 8)
V1 = (8, 24)
CH1 = (24, 32)
V2 = (32, 48)
CH2 = (48, 56)
SILENCE = (56, 58)
INSTR = (58, 74)
V3 = (74, 82)
OUTRO = (82, 90)


# ============================================================
# ORGAN DRONE (Ch 5) — D pedal with Dm7 tension (C natural)
# ============================================================
def organ_drone():
    """Sustained organ drone — the hypnotic bed of the song.
    v3: adds occasional C natural for Dm7 tension. F# over A major in instrumental.
    Outro: pitch wobble increases to +/-400 cents, last bar barely audible."""

    # Intro: pure D drone, very quiet, building
    for bar in range(INTRO[0], INTRO[1]):
        t = bt(bar)
        vel = 30 + bar * 3
        vel = breathing_vel(vel, bar, cycle_bars=8, depth=3)
        E.note(5, N('D',3), vel, t, BAR4 - EIGHTH, time_amount=5, vel_amount=3)
        if bar >= 4:
            E.note(5, N('A',3), vel - 8, t, BAR4 - EIGHTH, time_amount=5, vel_amount=3)
        # v3: add C natural (Dm7 tension) on bars 6-7 of intro
        if bar >= 6:
            E.note(5, N('C',4), vel - 15, t, BAR4 - EIGHTH, time_amount=5, vel_amount=2)
        for q in range(4):
            bend_val = random.randint(-200, 200)
            E.pitch_bend(5, bend_val, t + q * QUARTER + random.randint(0, 40))

    # Verses: D pedal drone with occasional Dm7 tension
    for section in [V1, V2, V3]:
        for bar in range(section[0], section[1]):
            t = bt(bar)
            vel = 42 if section != V3 else 35
            vel = breathing_vel(vel, bar, cycle_bars=8, depth=4)
            E.note(5, N('D',3), vel, t, BAR4 - EIGHTH, time_amount=5, vel_amount=3)
            E.note(5, N('A',3), vel - 6, t, BAR4 - EIGHTH, time_amount=5, vel_amount=3)
            # v3: occasional C natural for Dm7 color (every 3rd bar)
            if bar % 3 == 2:
                E.note(5, N('C',4), vel - 12, t, BAR4 - EIGHTH, time_amount=5, vel_amount=2)
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

    # SILENCE section: organ drone ONLY on D — complete stillness
    for bar in range(SILENCE[0], SILENCE[1]):
        t = bt(bar)
        vel = 38
        vel = breathing_vel(vel, bar, cycle_bars=4, depth=2)
        E.note(5, N('D',3), vel, t, BAR4 - EIGHTH, time_amount=3, vel_amount=2)
        E.note(5, N('A',3), vel - 10, t, BAR4 - EIGHTH, time_amount=3, vel_amount=2)
        # Very subtle wobble during silence — almost meditative
        for q in range(4):
            bend_val = random.randint(-100, 100)
            E.pitch_bend(5, bend_val, t + q * QUARTER + random.randint(0, 30))

    # Instrumental: follow descending bass, add F# over A major
    for bar in range(INSTR[0], INSTR[1]):
        t = bt(bar)
        bar_in_section = bar - INSTR[0]
        cidx = instr_chord_idx(bar_in_section)
        root_bass = get_instr_bass(bar_in_section)
        vel = 55 + min(15, bar_in_section)
        vel = min(70, vel)
        vel = breathing_vel(vel, bar, cycle_bars=8, depth=4)
        E.note(5, root_bass + 12, vel, t, BAR4 - EIGHTH, time_amount=5, vel_amount=3)
        E.note(5, root_bass + 19, vel - 6, t, BAR4 - EIGHTH, time_amount=5, vel_amount=3)

        # v3: on A major bars (idx 4 or 5), add F# — turns A into a lush complex chord
        if cidx >= 4:
            E.note(5, N('Gb',4), vel - 4, t, BAR4 - EIGHTH, time_amount=5, vel_amount=3)

        # v3: on Dm bars, add C natural for Dm7
        if cidx == 0:
            E.note(5, N('C',4), vel - 10, t, BAR4 - EIGHTH, time_amount=5, vel_amount=2)

        for q in range(4):
            bend_val = random.randint(-300, 300)
            E.pitch_bend(5, bend_val, t + q * QUARTER + random.randint(0, 40))

    # Outro: D drone fading, last 4 bars organ ONLY with increasing wobble
    for bar in range(OUTRO[0], OUTRO[1]):
        t = bt(bar)
        bar_in_outro = bar - OUTRO[0]

        # Last 4 bars: dramatic fade with increasing pitch wobble
        if bar_in_outro >= 4:
            # Exponential fade: each bar much quieter
            vel = max(8, 35 - (bar_in_outro - 4) * 8)
            # Last bar: barely there
            if bar_in_outro == 7:
                vel = 8
            E.note(5, N('D',3), vel, t, BAR4 - EIGHTH, time_amount=5, vel_amount=2)
            # Pitch wobble increases to +/-400 cents
            wobble_depth = 150 + (bar_in_outro - 4) * 70  # ramps up
            if bar_in_outro == 7:
                wobble_depth = 50  # v7: return to earth — calm wobble before disappearing
            for step in range(8):
                phase = step / 8.0 * 2 * 3.14159
                bend = int(wobble_depth * math.sin(phase) * (8192 / 200))
                bend = max(-8192, min(8191, bend))
                E.pitch_bend(5, bend, t + step * EIGHTH + random.randint(0, 20))
        else:
            vel = max(20, 45 - bar_in_outro * 4)
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

    patterns = [
        [0,1,2,3, 2,1,0,3, 0,2,1,3, 2,0,3,1],
        [0,2,1,3, 0,3,1,2, 0,2,3,1, 0,1,3,2],
        [3,2,1,0, 3,1,2,0, 3,2,0,1, 3,0,1,2],
        [0,1,0,2, 0,1,0,3, 0,2,0,3, 0,1,0,2],
        [0,3,1,2, 3,0,2,1, 0,3,2,1, 3,0,1,2],
        [0,1,2,1, 0,2,3,2, 0,1,3,1, 0,2,3,1],
    ]

    def arp_bar(bar, chord_notes, vel_base, pattern_idx):
        t = bt(bar)
        notes = list(chord_notes)
        while len(notes) < 4:
            notes.append(notes[0] + 12)
        notes = [n + 12 for n in notes[:4]]

        pat = patterns[pattern_idx % len(patterns)]
        for i, idx in enumerate(pat):
            note_t = t + i * SIXTEENTH
            beat_pos = i % 4
            vel = vel_base + accent_beat(beat_pos, 'natural')
            vel = breathing_vel(vel, bar, cycle_bars=8, depth=4)
            dur = SIXTEENTH - random.randint(15, 40)
            E.note(2, notes[idx % len(notes)], vel, note_t, dur, time_amount=6, vel_amount=3)

    # Intro: arpeggio fades in on Dm
    dm_notes = make_chord(N('D',4), 'minor')
    for bar in range(INTRO[0] + 2, INTRO[1]):
        vel = 25 + (bar - INTRO[0]) * 4
        arp_bar(bar, dm_notes, vel, bar)

    # Verses
    for section in [V1, V2]:
        for bar in range(section[0], section[1]):
            chord_idx = (bar - section[0]) % 4
            chord = get_voicing(VERSE_VOICINGS, chord_idx, bar)
            arp_bar(bar, chord, 45, bar)

    # Choruses — slightly louder
    for section in [CH1, CH2]:
        for bar in range(section[0], section[1]):
            chord_idx = (bar - section[0]) % 4
            chord = get_voicing(CHORUS_VOICINGS, chord_idx, bar)
            arp_bar(bar, chord, 52, bar + 3)

    # NO arpeggio during SILENCE section (complete stillness except organ)

    # Instrumental — loudest, most intense
    for bar in range(INSTR[0], INSTR[1]):
        bar_in_section = bar - INSTR[0]
        chord = get_instr_voicing(bar_in_section, bar)
        vel = 50 + min(15, bar_in_section)
        arp_bar(bar, chord, vel, bar + 1)

    # Verse 3 sparse — quieter, every other bar has gaps
    for bar in range(V3[0], V3[1]):
        chord_idx = (bar - V3[0]) % 4
        chord = get_voicing(VERSE_VOICINGS, chord_idx, bar)
        if bar % 2 == 0:
            arp_bar(bar, chord, 35, bar)
        else:
            t = bt(bar)
            notes = list(chord)
            while len(notes) < 4:
                notes.append(notes[0] + 12)
            notes = [n + 12 for n in notes[:4]]
            pat = patterns[bar % len(patterns)]
            for i in range(8):
                note_t = t + i * SIXTEENTH
                vel = breathing_vel(30, bar, cycle_bars=8, depth=3)
                dur = SIXTEENTH - random.randint(15, 40)
                E.note(2, notes[pat[i] % len(notes)], vel, note_t, dur, time_amount=6, vel_amount=3)

    # Outro — fading away, stops 2 bars before end (last 4 = organ only)
    for bar in range(OUTRO[0], OUTRO[0] + 4):
        chord = make_chord(N('D',4), 'minor')
        vel = max(20, 40 - (bar - OUTRO[0]) * 5)
        arp_bar(bar, chord, vel, bar)


# ============================================================
# SYNTH PAD (Ch 1) — warm bed with expression swells
# v4 FIX #2: Verse pad vel=42, Chorus pad vel=65 (was 55/58)
# ============================================================
def synth_pad():
    """Warm synth pad with CC11 expression swells.
    v4: chorus pad velocity boosted to 65 for real dynamic contrast."""

    def pad_section(start, end, voicings, vel_base, swell=True, use_instr=False):
        for bar in range(start, end):
            t = bt(bar)
            if use_instr:
                bar_in_section = bar - start
                chord = get_instr_voicing(bar_in_section, bar)
            else:
                chord_idx = (bar - start) % 4
                chord = get_voicing(voicings, chord_idx, bar)
            vel = breathing_vel(vel_base, bar, cycle_bars=8, depth=5)

            for note in chord:
                E.note(1, note, vel, t, BAR4 - EIGHTH, time_amount=5, vel_amount=4)

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

    # v4 FIX #2: verse pad vel=42 (unchanged), chorus pad vel=65 (was 55/58)
    pad_section(V1[0], V1[1], VERSE_VOICINGS, 42)       # verse = 42
    pad_section(CH1[0], CH1[1], CHORUS_VOICINGS, 65)     # v4: chorus = 65 (was 55)
    pad_section(V2[0], V2[1], VERSE_VOICINGS, 42)        # verse = 42 (was 48)
    pad_section(CH2[0], CH2[1], CHORUS_VOICINGS, 65)     # v4: chorus = 65 (was 58)
    # NO pad during SILENCE
    pad_section(INSTR[0], INSTR[1], None, 55, use_instr=True)
    pad_section(V3[0], V3[1], VERSE_VOICINGS, 35, swell=False)

    # Outro pad: D minor fading, stops at bar 4 of outro (last 4 = organ only)
    for bar in range(OUTRO[0], OUTRO[0] + 4):
        t = bt(bar)
        chord = make_chord(N('D',4), 'minor')
        vel = max(18, 40 - (bar - OUTRO[0]) * 5)
        for note in chord:
            E.note(1, note, vel, t, BAR4 - EIGHTH, time_amount=5, vel_amount=3)


# ============================================================
# CLEAN GUITAR (Ch 3) — sparse atmospheric chords
# v4 FIX #6: REMOVED from Verse 1. Guitar enters at Chorus 1 (bar 24).
# Less is more — don't add instruments for the sake of density.
# ============================================================
def clean_guitar():
    """Clean guitar — sparse, ringing chords.
    v4: removed from Verse 1. Enters at Chorus 1 where it can be heard."""

    patterns = [
        [(0, 0, 0), (QUARTER, 2, -5), (HALF, 1, -3), (HALF + QUARTER, 2, -7)],
        [(0, 0, 0), (EIGHTH, 1, -8), (QUARTER, 2, -5), (HALF, 0, -3), (HALF + QUARTER, 1, -6)],
        [(0, 0, 3), (HALF, 2, -5), (HALF + QUARTER, 1, -7)],
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
            dur = QUARTER + EIGHTH + random.randint(-20, 40)
            E.note(3, n, v, t + offset, dur, time_amount=8, vel_amount=4)

    # v4 FIX #6: NO guitar in Verse 1. It was inaudible and served no purpose.
    # Guitar enters fresh at Chorus 1 — where it can actually be heard.

    # Chorus 1 — every bar, slightly fuller (v4: this is now the guitar's ENTRANCE)
    for bar in range(CH1[0], CH1[1]):
        chord_idx = (bar - CH1[0]) % 4
        chord = get_voicing(CHORUS_VOICINGS, chord_idx, bar)
        guitar_bar(bar, chord, 52, bar)

    # Verse 2 — every bar (guitar has established itself by now)
    for bar in range(V2[0], V2[1]):
        chord_idx = (bar - V2[0]) % 4
        chord = get_voicing(VERSE_VOICINGS, chord_idx, bar)
        guitar_bar(bar, chord, 50, bar)

    # Chorus 2
    for bar in range(CH2[0], CH2[1]):
        chord_idx = (bar - CH2[0]) % 4
        chord = get_voicing(CHORUS_VOICINGS, chord_idx, bar)
        guitar_bar(bar, chord, 55, bar)

    # NO guitar during SILENCE

    # Verse 3 sparse — every other bar
    for bar in range(V3[0], V3[1]):
        if bar % 2 == 0:
            chord_idx = (bar - V3[0]) % 4
            chord = get_voicing(VERSE_VOICINGS, chord_idx, bar)
            guitar_bar(bar, chord, 38, bar)


# ============================================================
# DISTORTED GUITAR (Ch 4) — fuzzy Jazzmaster
# v3: bars 9-12 of instrumental play a MELODY (single-note line following
# the vocal hook contour) instead of power chords, then return to power chords.
# ============================================================
def distorted_guitar():
    """Fuzzy distorted guitar — v3: single-note melody bars 9-12 of instrumental."""

    # Instrumental section
    for bar in range(INSTR[0], INSTR[1]):
        t = bt(bar)
        bar_in_section = bar - INSTR[0]
        cidx = instr_chord_idx(bar_in_section)
        root_bass = get_instr_bass(bar_in_section)
        root = root_bass

        intensity = min(1.0, bar_in_section / 12.0)
        vel = int(55 + intensity * 25)
        vel = breathing_vel(vel, bar, cycle_bars=8, depth=5)

        # v3: bars 8-11 of instrumental (0-indexed) = slow fuzzy single-note melody
        # Following the vocal hook contour: Bb-A-G-A-Bb-A-G-F-D
        if 8 <= bar_in_section <= 11:
            melody_bar = bar_in_section - 8
            # 4-bar melody contour inspired by the chorus hook
            melodies = [
                # Bar 0: Bb whole note — big statement
                [(N('Bb',4), 0, WHOLE)],
                # Bar 1: A to G — descending
                [(N('A',4), 0, HALF), (N('G',4), HALF, HALF)],
                # Bar 2: A rising to Bb — reaching
                [(N('A',4), 0, QUARTER), (N('Bb',4), QUARTER, DOTTED_HALF)],
                # Bar 3: G to F to D — settling, resolving
                [(N('G',4), 0, QUARTER), (N('F',4), QUARTER, QUARTER), (N('D',4), HALF, HALF)],
            ]
            for note, offset, dur in melodies[melody_bar]:
                E.note(4, note, vel + 5, t + offset, dur - 30, time_amount=8, vel_amount=5)
        else:
            # Power chords as before
            if bar_in_section % 3 == 0:
                notes = make_chord(root + 24, 'power')
            elif bar_in_section % 3 == 1:
                notes = [root + 24, root + 31]
            else:
                notes = [root + 24, root + 31, root + 36]

            for n in notes:
                E.note(4, n, vel, t, HALF + QUARTER, time_amount=10, vel_amount=6)

            if bar_in_section % 4 >= 2:
                for n in notes:
                    E.note(4, n, vel - 8, t + HALF + QUARTER, QUARTER - 30, time_amount=10, vel_amount=6)

    # Chorus 2 — lighter power chord bed
    for bar in range(CH2[0], CH2[1]):
        t = bt(bar)
        chord_idx = (bar - CH2[0]) % 4
        root = CHORUS_BASS[chord_idx]
        vel = 50
        vel = breathing_vel(vel, bar, cycle_bars=4, depth=4)
        notes = make_chord(root + 24, 'power')
        for n in notes:
            E.note(4, n, vel, t, BAR4 - EIGHTH, time_amount=8, vel_amount=5)


# ============================================================
# BASS (Ch 6) — enters verse 1, chromatic walk in instrumental
# v4 FIX #3: Passing tones — every 2nd bar, add chromatic approach on beat 4
# ============================================================
def bass_line():
    """Bass guitar — supportive, with chromatic approach notes.
    v4: every 2nd bar in verses, add chromatic walk on beats 3-4 toward next root."""

    def bass_bar(bar, root, vel_base, section_start, with_fills=False,
                 next_root=None, add_walk=False):
        """v4: add_walk=True adds chromatic approach notes on beats 3-4."""
        t = bt(bar)
        vel = breathing_vel(vel_base, bar, cycle_bars=8, depth=4)
        bar_in_section = bar - section_start

        if add_walk and next_root is not None:
            # v4 FIX #3: chromatic approach — play root on beats 1-2, then walk on beats 3-4
            # Beat 1: root (half note)
            E.note(6, root, vel + accent_beat(0), t, HALF - EIGHTH, time_amount=6, vel_amount=3)
            # Beats 3-4: walk toward next root
            if next_root > root:
                # Walking UP: root, then chromatic step up (e.g., D→E if heading to F)
                walk_note = root + 1  # chromatic approach from below
                if next_root - root == 1:
                    walk_note = root  # already adjacent, just repeat
                E.note(6, root, vel + accent_beat(2) - 3, t + HALF, QUARTER - 20, time_amount=6, vel_amount=3)
                E.note(6, walk_note, vel + accent_beat(3) - 5, t + HALF + QUARTER, QUARTER - 20, time_amount=6, vel_amount=3)
            elif next_root < root:
                # Walking DOWN or large interval: play root + 5th
                E.note(6, root, vel + accent_beat(2) - 3, t + HALF, QUARTER - 20, time_amount=6, vel_amount=3)
                E.note(6, root + 7, vel + accent_beat(3) - 5, t + HALF + QUARTER, QUARTER - 20, time_amount=6, vel_amount=3)
            else:
                # Same root — just play root + octave
                E.note(6, root, vel + accent_beat(2) - 3, t + HALF, QUARTER - 20, time_amount=6, vel_amount=3)
                E.note(6, root + 12, vel + accent_beat(3) - 5, t + HALF + QUARTER, QUARTER - 20, time_amount=6, vel_amount=3)
        elif bar_in_section % 4 == 0:
            E.note(6, root, vel + accent_beat(0), t, BAR4 - QUARTER, time_amount=6, vel_amount=3)
        elif bar_in_section % 4 == 1:
            E.note(6, root, vel + accent_beat(0), t, HALF - EIGHTH, time_amount=6, vel_amount=3)
            E.note(6, root, vel + accent_beat(2) - 5, t + HALF, HALF - EIGHTH, time_amount=6, vel_amount=3)
        elif bar_in_section % 4 == 2:
            E.note(6, root, vel + accent_beat(0), t, DOTTED_HALF - EIGHTH, time_amount=6, vel_amount=3)
            if with_fills:
                E.note(6, root + random.choice([-1, 1, 2]), vel - 8, t + DOTTED_HALF, QUARTER - 30, time_amount=8, vel_amount=4)
            else:
                E.note(6, root + 7, vel - 6, t + DOTTED_HALF, QUARTER - 30, time_amount=6, vel_amount=3)
        else:
            E.note(6, root, vel + accent_beat(0), t, QUARTER - 20, time_amount=6, vel_amount=3)
            E.note(6, root, vel + accent_beat(1) - 5, t + QUARTER, QUARTER - 20, time_amount=6, vel_amount=3)
            E.note(6, root + 7, vel + accent_beat(2) - 3, t + HALF, QUARTER - 20, time_amount=6, vel_amount=3)
            E.note(6, root, vel + accent_beat(3) - 5, t + HALF + QUARTER, QUARTER - 20, time_amount=6, vel_amount=3)

    def get_verse_next_root(bar, section_start, bass_roots):
        """Get the next bar's root for walking bass."""
        chord_idx = (bar - section_start) % 4
        next_chord_idx = (chord_idx + 1) % 4
        return bass_roots[next_chord_idx]

    # Verse 1 — enters bar 4
    # v4 FIX #3: every 2nd bar (odd bars relative to section), add chromatic walk
    for bar in range(V1[0] + 4, V1[1]):
        chord_idx = (bar - V1[0]) % 4
        bar_in_v1 = bar - V1[0]
        do_walk = (bar_in_v1 % 2 == 1)  # every 2nd bar
        next_root = get_verse_next_root(bar, V1[0], VERSE_BASS)
        bass_bar(bar, VERSE_BASS[chord_idx], 55, V1[0], with_fills=True,
                 next_root=next_root, add_walk=do_walk)

    # Chorus 1
    for bar in range(CH1[0], CH1[1]):
        chord_idx = (bar - CH1[0]) % 4
        bass_bar(bar, CHORUS_BASS[chord_idx], 60, CH1[0], with_fills=True)

    # Verse 2
    # v4 FIX #3: every 2nd bar, add chromatic walk
    for bar in range(V2[0], V2[1]):
        chord_idx = (bar - V2[0]) % 4
        bar_in_v2 = bar - V2[0]
        do_walk = (bar_in_v2 % 2 == 1)
        next_root = get_verse_next_root(bar, V2[0], VERSE_BASS)
        bass_bar(bar, VERSE_BASS[chord_idx], 58, V2[0], with_fills=True,
                 next_root=next_root, add_walk=do_walk)

    # Chorus 2
    for bar in range(CH2[0], CH2[1]):
        chord_idx = (bar - CH2[0]) % 4
        bass_bar(bar, CHORUS_BASS[chord_idx], 62, CH2[0], with_fills=True)

    # NO bass during SILENCE

    # Instrumental: descending bass walk with the new 6-bar cycle
    for bar in range(INSTR[0], INSTR[1]):
        t = bt(bar)
        bar_in_section = bar - INSTR[0]
        root = get_instr_bass(bar_in_section)
        vel = 60 + min(12, bar_in_section)
        vel = breathing_vel(vel, bar, cycle_bars=8, depth=4)

        E.note(6, root, vel, t, QUARTER - 20, time_amount=6, vel_amount=3)
        E.note(6, root, vel - 5, t + QUARTER, QUARTER - 20, time_amount=6, vel_amount=3)
        E.note(6, root + 7, vel - 3, t + HALF, QUARTER - 20, time_amount=6, vel_amount=3)
        # Walk note to next chord
        next_bar = bar_in_section + 1
        next_root = get_instr_bass(next_bar) if next_bar < 16 else N('D',2)
        walk_note = root + (1 if next_root > root else -1)
        E.note(6, walk_note, vel - 8, t + HALF + QUARTER, QUARTER - 30, time_amount=8, vel_amount=4)

    # Verse 3 sparse
    for bar in range(V3[0], V3[1]):
        if bar % 2 == 0:
            chord_idx = (bar - V3[0]) % 4
            E.note(6, VERSE_BASS[chord_idx], 45, bt(bar), BAR4 - QUARTER, time_amount=6, vel_amount=3)

    # Outro — very sparse, fading, stops at bar 4 (last 4 = organ only)
    for bar in range(OUTRO[0], OUTRO[0] + 4):
        vel = max(25, 45 - (bar - OUTRO[0]) * 5)
        E.note(6, N('D',2), vel, bt(bar), BAR4 - QUARTER, time_amount=6, vel_amount=3)

    # v7: Bass grounding — quiet D2 across final 4 bars of outro
    # Gives the wobbling organ a tonic anchor, grounding dissolution in D minor
    for bar in range(OUTRO[0] + 4, OUTRO[1]):
        bar_in_outro = bar - OUTRO[0]
        # vel=18 fading to vel=12 across 4 bars
        vel = 18 - (bar_in_outro - 4) * 2  # 18, 16, 14, 12
        E.note(6, N('D',2), vel, bt(bar), BAR4 - QUARTER, time_amount=6, vel_amount=3)


# ============================================================
# DRUMS (Ch 9) — enters at chorus, sparse and atmospheric
# v4 FIX #2: Verse drums vel=50, Chorus drums vel=75
# v5 FIX #2: Verse 2 ghost notes — ALTERNATING pattern:
#   Even bars (34,36,38...): ghost KICK on &2 (vel=25)
#   Odd bars (35,37,39...): ghost SNARE on &4 (vel=20)
# ============================================================
def drums():
    """Drums — sparse, enter at chorus.
    v4: chorus vel boosted to 75.
    v5: Verse 2 ghost notes alternate — kick on &2 (even bars), snare on &4 (odd bars)."""
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

        E.note(9, KICK, vel + accent_beat(0), t, QUARTER, time_amount=6, vel_amount=4)
        if bar_in_section % 4 != 3:
            E.note(9, KICK, vel + accent_beat(2) - 3, t + HALF, QUARTER, time_amount=6, vel_amount=4)

        E.note(9, SNARE, vel + accent_beat(1) + 3, t + QUARTER, QUARTER, time_amount=6, vel_amount=5)
        E.note(9, SNARE, vel + accent_beat(3), t + HALF + QUARTER, QUARTER, time_amount=6, vel_amount=5)

        for i in range(8):
            hh_t = t + i * EIGHTH
            hh_vel = vel - 15 + swing_offset(i, amount=12)
            if i == 4 and bar_in_section % 3 == 0:
                E.note(9, HH_OPEN, hh_vel + 5, hh_t, EIGHTH, time_amount=5, vel_amount=3)
            else:
                E.note(9, HH_CLOSED, hh_vel, hh_t, EIGHTH // 2, time_amount=5, vel_amount=3)

        if bar_in_section % 2 == 1:
            ghost_pos = random.choice([EIGHTH, HALF + EIGHTH, HALF + QUARTER + EIGHTH])
            E.note(9, SNARE, vel - 25, t + ghost_pos, EIGHTH, time_amount=8, vel_amount=3)

    def verse2_pattern(bar, vel_base, section_start):
        """v5 FIX #2: alternating ghost notes for intentional pocket.
        Even bars (34,36,38...): ghost KICK on &2 (vel=25)
        Odd bars (35,37,39...): ghost SNARE on &4 (vel=20)"""
        t = bt(bar)
        vel = breathing_vel(vel_base, bar, cycle_bars=8, depth=3)

        for q in range(4):
            ride_vel = vel - 12 + accent_beat(q)
            E.note(9, RIDE, ride_vel, t + q * QUARTER, QUARTER, time_amount=6, vel_amount=3)

        E.note(9, KICK, vel - 5, t, QUARTER, time_amount=6, vel_amount=4)

        bar_in_section = bar - section_start
        if bar_in_section % 2 == 0:
            E.note(9, RIMSHOT, vel - 10, t + HALF, QUARTER, time_amount=6, vel_amount=4)

        # v5 FIX #2: alternating ghost notes — creates intentional pocket
        # Use absolute bar numbers for even/odd check to get bars 34,36,38 vs 35,37,39
        if bar % 2 == 0:
            # Even bars (34, 36, 38, etc.): ghost KICK on the "and" of 2 (vel=25)
            E.note(9, KICK, 25, t + QUARTER + EIGHTH, EIGHTH, time_amount=8, vel_amount=2)
        else:
            # Odd bars (35, 37, 39, etc.): ghost SNARE on the "and" of 4 (vel=20)
            E.note(9, SNARE, 20, t + HALF + QUARTER + EIGHTH, EIGHTH, time_amount=8, vel_amount=2)

    def fill(bar, vel_base):
        t = bt(bar)
        vel = vel_base
        E.note(9, TOM_MID, vel, t + HALF, EIGHTH, time_amount=5, vel_amount=4)
        E.note(9, TOM_MID, vel - 3, t + HALF + EIGHTH, EIGHTH, time_amount=5, vel_amount=4)
        E.note(9, TOM_LOW, vel + 2, t + HALF + QUARTER, EIGHTH, time_amount=5, vel_amount=4)
        E.note(9, TOM_LOW, vel - 2, t + HALF + QUARTER + EIGHTH, EIGHTH, time_amount=5, vel_amount=4)

    # Chorus 1 — v4 FIX #2: vel=75 (was 65)
    E.note(9, CRASH, 75, bt(CH1[0]), HALF, time_amount=5, vel_amount=4)
    for bar in range(CH1[0], CH1[1]):
        chorus_pattern(bar, 75, CH1[0])    # v4: was 65, now 75
        if bar == CH1[1] - 1:
            fill(bar, 60)

    # Verse 2 — sparse ride pattern, v4 FIX #2: vel=50 (unchanged)
    for bar in range(V2[0] + 4, V2[1]):
        verse2_pattern(bar, 50, V2[0])

    # Chorus 2 — v4 FIX #2: vel=75 (was 68)
    E.note(9, CRASH, 78, bt(CH2[0]), HALF, time_amount=5, vel_amount=4)
    for bar in range(CH2[0], CH2[1]):
        chorus_pattern(bar, 75, CH2[0])    # v4: was 68, now 75
        if bar == CH2[1] - 1:
            fill(bar, 62)

    # NO drums during SILENCE

    # Instrumental — crashes in after the silence. Big contrast.
    E.note(9, CRASH, 85, bt(INSTR[0]), HALF, time_amount=5, vel_amount=4)
    for bar in range(INSTR[0], INSTR[1]):
        intensity = min(1.0, (bar - INSTR[0]) / 12.0)
        vel = int(60 + intensity * 20)
        chorus_pattern(bar, vel, INSTR[0])
        if (bar - INSTR[0]) % 4 == 0 and bar > INSTR[0]:
            E.note(9, CRASH, vel + 5, bt(bar), HALF, time_amount=5, vel_amount=4)
        if bar == INSTR[1] - 1:
            fill(bar, 70)


# ============================================================
# PIANO (Ch 0) — enters at verse 2
# ============================================================
def piano():
    """Piano — enters at verse 2, warm chords with sustain pedal."""

    def piano_chords(bar, chord_notes, vel_base, section_start, style='pads'):
        t = bt(bar)
        vel = breathing_vel(vel_base, bar, cycle_bars=8, depth=5)

        if style == 'pads':
            E.cc(0, 64, 127, t + 5)
            for note in chord_notes:
                E.note(0, note, vel, t, BAR4 - QUARTER, time_amount=6, vel_amount=4)
            E.cc(0, 64, 0, t + BAR4 - EIGHTH)
        elif style == 'arpeggio':
            notes = list(chord_notes) + [chord_notes[0] + 12]
            E.cc(0, 64, 127, t + 5)
            arp_patterns = [
                [0, 1, 2, 3, 2, 1, 0, 3],
                [0, 2, 1, 3, 0, 2, 3, 1],
                [3, 2, 1, 0, 1, 2, 3, 0],
            ]
            pat = arp_patterns[bar % len(arp_patterns)]
            for i, idx in enumerate(pat):
                note_t = t + i * EIGHTH
                n = notes[idx % len(notes)]
                v = vel - 5 + accent_beat(i % 4)
                E.note(0, n, v, note_t, QUARTER, time_amount=8, vel_amount=4)
            E.cc(0, 64, 0, t + BAR4 - EIGHTH)

    # Verse 2
    for bar in range(V2[0], V2[1]):
        chord_idx = (bar - V2[0]) % 4
        chord = get_voicing(VERSE_VOICINGS, chord_idx, bar)
        piano_chords(bar, chord, 48, V2[0], style='pads')

    # Chorus 2
    for bar in range(CH2[0], CH2[1]):
        chord_idx = (bar - CH2[0]) % 4
        chord = get_voicing(CHORUS_VOICINGS, chord_idx, bar)
        piano_chords(bar, chord, 55, CH2[0], style='pads')

    # NO piano during SILENCE

    # Instrumental — arpeggiated piano emerges
    for bar in range(INSTR[0] + 4, INSTR[1]):
        bar_in_section = bar - INSTR[0]
        chord = get_instr_voicing(bar_in_section, bar)
        vel = 45 + min(15, bar_in_section - 4)
        piano_chords(bar, chord, vel, INSTR[0], style='arpeggio')

    # Verse 3 — gentle arpeggios
    for bar in range(V3[0], V3[1]):
        chord_idx = (bar - V3[0]) % 4
        chord = get_voicing(VERSE_VOICINGS, chord_idx, bar)
        piano_chords(bar, chord, 38, V3[0], style='arpeggio')

    # Outro — quiet piano pads, stops at bar 4 (last 4 = organ only)
    for bar in range(OUTRO[0], OUTRO[0] + 4):
        t = bt(bar)
        chord = make_chord(N('D',4), 'minor')
        vel = max(20, 38 - (bar - OUTRO[0]) * 4)
        E.cc(0, 64, 127, t + 5)
        for note in chord:
            E.note(0, note, vel, t, BAR4 - QUARTER, time_amount=6, vel_amount=3)
        E.cc(0, 64, 0, t + BAR4 - EIGHTH)


# ============================================================
# STRINGS (Ch 7) — orchestral swells
# ============================================================
def strings():
    """String ensemble — swells in choruses, grandeur in instrumental."""

    def string_swell(bar, chord_notes, vel_base, swell_bars=2, phase=0):
        t = bt(bar)
        vel = vel_base
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

    # Chorus 1
    for bar in range(CH1[0], CH1[1]):
        chord_idx = (bar - CH1[0]) % 4
        chord = get_voicing(CHORUS_VOICINGS, chord_idx, bar)
        high_chord = [n + 12 for n in chord[:3]]
        string_swell(bar, high_chord, 42, swell_bars=2, phase=(bar - CH1[0]) % 4)

    # Chorus 2
    for bar in range(CH2[0], CH2[1]):
        chord_idx = (bar - CH2[0]) % 4
        chord = get_voicing(CHORUS_VOICINGS, chord_idx, bar)
        high_chord = [n + 12 for n in chord[:3]]
        string_swell(bar, high_chord, 50, swell_bars=2, phase=(bar - CH2[0]) % 4)

    # NO strings during SILENCE

    # Instrumental — biggest string presence
    for bar in range(INSTR[0] + 4, INSTR[1]):
        bar_in_section = bar - INSTR[0]
        chord = get_instr_voicing(bar_in_section, bar)
        high_chord = [n + 12 for n in chord[:3]]
        intensity = min(1.0, bar_in_section / 12.0)
        vel = int(45 + intensity * 25)
        string_swell(bar, high_chord, vel, swell_bars=2, phase=bar_in_section % 4)


# ============================================================
# VOCAL MELODY (Ch 8) — dreamy, floating melody
# v4 FIX #1: Verse 1 opens with Bb->D falling 6th IMMEDIATELY (the hook IS the opening)
# v4 FIX #5: Verse 3 is a "fall and recovery" arc — D5 down to D4, silence, back to D5
# v5 FIX #4: Verse 3 recovery uses chromatic approach C#5->D5 instead of direct D5
# ============================================================
def vocal_melody():
    """Vocal melody — v4: immediate Bb->D hook, fall-and-recovery V3 arc.
    v5: chromatic C#5->D5 approach on V3 recovery."""

    scale = [N('D',5), N('E',5), N('F',5), N('G',5), N('A',5), N('Bb',5), N('C',6), N('D',6)]

    def phrase(bar_start, notes_data, vel_base):
        t = bt(bar_start)
        for i, nd in enumerate(notes_data):
            if len(nd) == 3:
                scale_idx, beat_offset, dur = nd
                note = scale[scale_idx % len(scale)]
            elif len(nd) == 4:
                # (midi_note_direct, beat_offset, dur, 'raw') — for chromatic notes like C#
                note, beat_offset, dur, _ = nd

            tick = t + beat_offset
            if len(nd) == 3:
                vel = vel_base + (scale_idx - 3) * 2
            else:
                vel = vel_base + 3  # chromatic notes get slight emphasis
            vel = breathing_vel(vel, bar_start, cycle_bars=8, depth=4)

            # Grace note occasionally
            if i % 5 == 3 and i > 0 and len(nd) == 3:
                grace = scale[(scale_idx - 1) % len(scale)]
                E.note(8, grace, vel - 15, tick - SIXTEENTH, SIXTEENTH - 10, time_amount=6, vel_amount=3)

            # Anticipation
            if i % 7 == 4:
                tick -= SIXTEENTH
                dur += SIXTEENTH

            E.note(8, note, vel, tick, dur, time_amount=8, vel_amount=4)

    # === VERSE 1 ===
    # v4 FIX #1: IMMEDIATE HOOK — the Bb->D falling 6th IS the opening.
    # Bar 0 (bar 8): Bb5 quarter note, then D5 dotted half — the hook announces itself.
    # Bar 1 (bar 9): silence — let the hook ring.
    # Bar 2 (bar 10): F5->A5 rising 3rd — answering the fall.
    phrase(8, [
        (5, 0, QUARTER),                     # Bb5 — the hook STARTS here
        (0, QUARTER, DOTTED_HALF),            # D5 — falling 6th, held. Identity established.
        # Bar 1: SILENCE. The hook breathes.
        # Bar 2: F->A rising 3rd — the answer
        (2, BAR4 * 2, HALF),                  # F5 — rising...
        (4, BAR4 * 2 + HALF, HALF),           # A5 — ...the answer to the fall
        # Bar 3: settle
        (3, BAR4 * 3, HALF),                  # G — settling
        (2, BAR4 * 3 + HALF, HALF),           # F — home territory
    ], 55)

    # Phrase 2: bars 12-15 — reaching higher
    phrase(12, [
        (4, 0, QUARTER),
        (5, QUARTER, HALF),               # Bb — reaching
        (4, HALF + QUARTER, QUARTER),
        (3, BAR4, HALF),
        (2, BAR4 + HALF, QUARTER),
        (4, BAR4 * 2, DOTTED_HALF),       # A — peak
        (3, BAR4 * 2 + DOTTED_HALF, QUARTER),
        (2, BAR4 * 3, HALF),
        (0, BAR4 * 3 + HALF, HALF),       # D — rest
    ], 58)

    # Phrase 3: bars 16-19
    phrase(16, [
        (0, 0, HALF),
        (2, HALF, QUARTER),
        (3, HALF + QUARTER, QUARTER),
        (4, BAR4, HALF + QUARTER),
        (3, BAR4 + HALF + QUARTER, QUARTER),
        (2, BAR4 * 2, HALF),
        (3, BAR4 * 2 + HALF, HALF),
        (2, BAR4 * 3, DOTTED_HALF),
        (0, BAR4 * 3 + DOTTED_HALF, QUARTER),
    ], 55)

    # Phrase 4: bars 20-23
    phrase(20, [
        (4, 0, HALF),
        (3, HALF, QUARTER),
        (2, HALF + QUARTER, QUARTER),
        (0, BAR4, WHOLE),
        (6, BAR4 * 2, HALF),              # C — surprise
        (5, BAR4 * 2 + HALF, QUARTER),
        (4, BAR4 * 2 + HALF + QUARTER, QUARTER),
        (3, BAR4 * 3, HALF),
        (2, BAR4 * 3 + HALF, HALF),
    ], 55)

    # === CHORUS 1 ===
    # v3: On the A7 chord (3rd chord, bars 26-27 relative), vocal sings C#5
    # resolving to D5 on the Dm chord. C#->D is the most satisfying resolution.
    phrase(24, [
        (5, 0, DOTTED_HALF),              # Bb — big opening (over Bb chord)
        (4, DOTTED_HALF, QUARTER),         # A
        (3, BAR4, HALF),                   # G (over F chord)
        (4, BAR4 + HALF, HALF),            # A
        # A7 chord — THE moment. C# is the raised 7th.
        (N('Db',5), BAR4 * 2, DOTTED_HALF, 'raw'),  # C#5 — electric against D minor
        (N('Db',5), BAR4 * 2 + DOTTED_HALF, QUARTER, 'raw'),  # C# held...
        # Resolution: C# -> D on the Dm chord
        (0, BAR4 * 3, HALF),              # D — HOME. The resolution.
        (2, BAR4 * 3 + HALF, HALF),       # F — settling into Dm
    ], 62)

    phrase(28, [
        (7, 0, DOTTED_HALF),              # D (high) — peak
        (6, DOTTED_HALF, QUARTER),         # C
        (5, BAR4, HALF),                   # Bb
        (4, BAR4 + HALF, HALF),            # A
        # A7 chord again — C# again
        (N('Db',5), BAR4 * 2, WHOLE, 'raw'),  # C#5 — sustained yearning
        # Resolve to D
        (0, BAR4 * 3, HALF),              # D — resolution
        (0, BAR4 * 3 + HALF, HALF),       # D — final rest
    ], 65)

    # === VERSE 2 ===
    phrase(32, [
        (0, 0, QUARTER),
        (2, QUARTER, HALF),
        (3, HALF + QUARTER, QUARTER),
        (4, BAR4, HALF),
        (3, BAR4 + HALF, QUARTER),
        (2, BAR4 + HALF + QUARTER, QUARTER),
        (3, BAR4 * 2, DOTTED_HALF),
        (4, BAR4 * 3, HALF),
        (5, BAR4 * 3 + HALF, HALF),
    ], 55)

    phrase(36, [
        (4, 0, HALF),
        (3, HALF, QUARTER),
        (4, HALF + QUARTER, QUARTER),
        (5, BAR4, DOTTED_HALF),
        (4, BAR4 + DOTTED_HALF, QUARTER),
        (3, BAR4 * 2, HALF),
        (2, BAR4 * 2 + HALF, HALF),
        (0, BAR4 * 3, WHOLE),
    ], 58)

    phrase(40, [
        (2, 0, HALF),
        (3, HALF, QUARTER),
        (4, HALF + QUARTER, QUARTER),
        (5, BAR4, HALF + QUARTER),
        (4, BAR4 + HALF + QUARTER, QUARTER),
        (3, BAR4 * 2, DOTTED_HALF),
        (2, BAR4 * 2 + DOTTED_HALF, QUARTER),
        (0, BAR4 * 3, WHOLE),
    ], 58)

    phrase(44, [
        (3, 0, HALF),
        (4, HALF, HALF),
        (5, BAR4, QUARTER),
        (4, BAR4 + QUARTER, QUARTER),
        (3, BAR4 + HALF, HALF),
        (4, BAR4 * 2, DOTTED_HALF),
        (5, BAR4 * 2 + DOTTED_HALF, QUARTER),
        (4, BAR4 * 3, HALF),
        (3, BAR4 * 3 + HALF, HALF),
    ], 56)

    # === CHORUS 2 === (same C# treatment, slightly more intense)
    phrase(48, [
        (5, 0, DOTTED_HALF),              # Bb
        (4, DOTTED_HALF, QUARTER),         # A
        (3, BAR4, HALF),                   # G
        (4, BAR4 + HALF, HALF),            # A
        # A7 — C# again, louder this time
        (N('Db',5), BAR4 * 2, DOTTED_HALF, 'raw'),  # C#5
        (N('Db',5), BAR4 * 2 + DOTTED_HALF, QUARTER, 'raw'),
        # Resolve
        (0, BAR4 * 3, HALF),              # D
        (2, BAR4 * 3 + HALF, HALF),       # F
    ], 65)

    phrase(52, [
        (7, 0, WHOLE),                    # D (high) — peak held longer
        (6, BAR4, HALF),                   # C
        (5, BAR4 + HALF, HALF),            # Bb
        # A7 — one last C#
        (N('Db',5), BAR4 * 2, DOTTED_HALF, 'raw'),  # C#5
        (N('E',5), BAR4 * 2 + DOTTED_HALF, QUARTER, 'raw'),  # E — the 5th of A7, adding color
        # Final resolution
        (0, BAR4 * 3, HALF),              # D
        (0, BAR4 * 3 + HALF, HALF),       # D — home
    ], 68)

    # === VERSE 3 — v4 FIX #5: "FALL AND RECOVERY" ARC ===
    # v5 FIX #4: Recovery uses chromatic approach C#5 (eighth) -> D5 (held)
    # 7 notes that tell a story. D5 falls to D4 (bars 1-4), silence at bottom,
    # then rises back through chromatic C#5->D5. A complete emotional arc.
    v3_start = V3[0]

    # Bar 1: D5 whole note — HOME. Starting point.
    t = bt(v3_start)
    E.note(8, N('D',5), 40, t, WHOLE, time_amount=6, vel_amount=3)

    # Bar 2: A4 whole note — descent begins
    t = bt(v3_start + 1)
    E.note(8, N('A',4), 38, t, WHOLE, time_amount=6, vel_amount=3)

    # Bar 3: F4 half, then D4 half — still falling, hitting bottom
    t = bt(v3_start + 2)
    E.note(8, N('F',4), 36, t, HALF, time_amount=6, vel_amount=3)
    E.note(8, N('D',4), 33, t + HALF, HALF, time_amount=6, vel_amount=3)

    # Bar 4: SILENCE — the bottom. Nothing. Let it sit.

    # Bars 5-6: D4 to A4 — rising. The recovery begins.
    t = bt(v3_start + 4)
    E.note(8, N('D',4), 33, t, WHOLE, time_amount=6, vel_amount=3)
    t = bt(v3_start + 5)
    E.note(8, N('A',4), 36, t, WHOLE, time_amount=6, vel_amount=3)

    # Bar 7: A4 whole — building toward home
    t = bt(v3_start + 6)
    E.note(8, N('A',4), 38, t, WHOLE, time_amount=5, vel_amount=2)

    # Bar 8: v5 FIX #4 — chromatic approach: C#5 (eighth) then D5 (held)
    # Instead of jumping straight to D5, the chromatic passing tone C#5
    # makes the homecoming ACTIVE — you hear the effort of returning.
    t = bt(v3_start + 7)
    E.note(8, N('Db',5), 32, t, EIGHTH, time_amount=6, vel_amount=3)  # C#5 — chromatic approach
    E.note(8, N('D',5), 30, t + EIGHTH, WHOLE - EIGHTH, time_amount=5, vel_amount=2)  # D5 — home, held


# ============================================================
# SYNTH LEAD — D-F-A RISING MOTIF (Ch 10) — the "glow"
# v4 FIX #4: OCTAVE CLIMBING — only 4 appearances, each one octave higher.
# v5 FIX #3: 2nd and 4th appearances INVERTED (A->F->D descending).
# Creates call-and-response pattern, not just transposition.
# ============================================================
def synth_lead_rising_motif():
    """The 'glow' — D-F-A rising 3-note figure.
    v4: 4 appearances only, each one octave higher (D3->D6). Rarity = power.
    v5: 2nd and 4th appearances inverted (A->F->D) for call-and-response."""

    # v5 FIX #3: 4 appearances with alternating direction
    # 1st (bar 58): D3-F3-A3 — ascending (call)
    # 2nd (bar 62): A4-F4-D4 — DESCENDING/inverted (response)
    # 3rd (bar 66): D5-F5-A5 — ascending (call)
    # 4th (bar 70): A6-F6-D6 — DESCENDING/inverted (response)

    appearances = [
        (58, 3, 30, False),   # bar 58: octave 3, vel 30, ascending (call)
        (62, 4, 50, True),    # bar 62: octave 4, vel 50, INVERTED (response)
        (66, 5, 75, False),   # bar 66: octave 5, vel 75, ascending (call)
        (70, 6, 100, True),   # bar 70: octave 6, vel 100, INVERTED (response)
    ]

    for bar, octave, vel_base, inverted in appearances:
        t = bt(bar)
        if inverted:
            # v5 FIX #3: inverted shape — A->F->D (descending)
            motif_notes = [N('A', octave), N('F', octave), N('D', octave)]
        else:
            # Original ascending shape — D->F->A
            motif_notes = [N('D', octave), N('F', octave), N('A', octave)]
        vel = breathing_vel(vel_base, bar, cycle_bars=4, depth=3)

        # Just 3 notes. Each on a triplet subdivision within a quarter note.
        for i, note in enumerate(motif_notes):
            note_t = t + i * (QUARTER // 3)
            dur = QUARTER // 3 - 15
            # Slight accent on the last note (the peak/nadir of the glow)
            v = vel + (4 if i == 2 else 0)
            E.note(10, note, v, note_t, dur, time_amount=6, vel_amount=3)

    # Let the motif ring into the first bar of V3 at diminished volume
    t = bt(V3[0])
    # Use the highest octave (6) for the trailing echo — a fading memory
    for i, note in enumerate([N('D',6), N('F',6), N('A',6)]):
        E.note(10, note, 20, t + i * (QUARTER // 3), QUARTER, time_amount=6, vel_amount=3)


# ============================================================
# v5 FIX #1: SYNTH COUNTER-MELODY (Ch 10) — Verse 1 bars 10-11
# After the vocal Bb->D falling 6th (bars 8-9), synth responds with
# E5->G5 rising minor 3rd (contrary motion). Bar 11: synth rests too.
# Creates call-and-response symmetry with the vocal hook.
# ============================================================
def synth_counter_melody():
    """v5 FIX #1: Synth counter-melody in Verse 1 bars 10-11.
    After the vocal falls (Bb->D), synth rises (E5->G5) — contrary motion.
    Bar 11: synth rests (mirroring vocal silence in bar 9)."""

    # Bar 10 (absolute): synth responds to the vocal's Bb->D fall with E5->G5 rise
    # The vocal has F5->A5 in bar 10, so the synth counter-melody sits below it
    # E5->G5 is a rising minor 3rd — contrary motion to the falling 6th
    t = bt(10)
    E.note(10, N('E',5), 45, t, HALF, time_amount=8, vel_amount=4)       # E5 — start of response
    E.note(10, N('G',5), 48, t + HALF, HALF, time_amount=8, vel_amount=4) # G5 — rising minor 3rd

    # Bar 11: SILENCE — synth rests, mirroring the vocal's silence in bar 9.
    # Call-and-response symmetry: vocal calls (8-9), synth responds (10), both rest (9/11).


# ============================================================
# SYNTH LEAD EXPRESSION (Ch 2) — pitch bend during instrumental
# ============================================================
def synth_lead_expression():
    """Pitch bend vibrato on synth arpeggio during instrumental."""
    for bar in range(INSTR[0], INSTR[1]):
        t = bt(bar)
        intensity = min(1.0, (bar - INSTR[0]) / 12.0)
        bend_depth = int(200 + intensity * 600)

        for step in range(16):
            phase = step / 16.0 * 2 * 3.14159
            bend = int(bend_depth * math.sin(phase))
            E.pitch_bend(2, bend, t + step * SIXTEENTH)

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
synth_lead_rising_motif()
synth_counter_melody()       # v5 FIX #1: counter-melody in Verse 1 bars 10-11
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
    total_bars=90,
    channel_names={
        0: 'Piano',
        1: 'Synth Pad (Juno Warm)',
        2: 'Synth Arpeggio',
        3: 'Clean Guitar',
        4: 'Distorted Guitar (Jazzmaster Fuzz)',
        5: 'Organ Drone',
        6: 'Bass Guitar',
        7: 'String Ensemble',
        8: 'Vocal Melody',
        9: 'Drums',
        10: 'Synth Lead (Rising Motif)',
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
        10: 80,  # Lead 1 (Square) — for the rising motif
    },
    output_path=output_path,
)
