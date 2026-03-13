# V2 Compositions — Review Findings & Changes

## Overview

Each of the 5 original MIDI compositions was carefully reviewed for mechanical patterns, flat dynamics, and missed opportunities to capture Grandaddy's signature sound. The v2 versions address these issues with a shared humanization library and handcrafted improvements per song.

---

## Review Findings (Common Issues in V1)

### Mechanical Feel
- **100% quantized timing** across all instruments — every note landed exactly on the grid
- **Flat velocity blocks** — entire tracks had identical velocity values (e.g., all piano notes at vel=64)
- **No swing** — 8th-note patterns were perfectly even, lacking the slight shuffle that makes music breathe
- **Repetitive patterns** — arpeggios used the same 1-2 patterns for the entire song (up to 1600+ repeated note sequences)
- **No ghost notes** on drums — fills and snare patterns were all at the same dynamic level
- **No expression controllers** — pads and strings entered at one volume and stayed there

### Missing Grandaddy Character
- **No sustain pedal** on piano — Grandaddy's piano parts live in reverb and sustain
- **No analog wobble** on synths/organ — the Juno-60 and organ should have subtle pitch drift
- **No pedal steel bends** on Song 4 — the "Blu Wav" cosmic country feel requires actual pitch bend events
- **Chord voicings were static** — same voicing every time a chord appeared, where Grandaddy varies between root, add9, sus2, min7
- **No dynamic arc** across sections — verses and choruses at the same intensity level
- **Bass lines too simple** — just root notes, missing the chromatic approach notes and melodic walks

---

## Shared Humanization Library (`humanize.py`)

Created a shared library used by all 5 songs to systematically apply human feel:

- **`h_time(tick, amount)`** — Random timing jitter (±5-12 ticks) on note positions
- **`h_vel(vel, amount)`** — Random velocity variation (±2-6 per note)
- **`swing_offset(eighth_index, amount)`** — Delays odd 8th notes by ~18 ticks for subtle swing
- **`accent_beat(beat_in_bar)`** — Natural beat accenting (beat 1 strongest, beat 3 next)
- **`breathing_vel(base_vel, bar_num)`** — Sinusoidal velocity undulation over 8-bar phrases, simulating a performer "breathing" with the music
- **`crescendo_vel()`** — Exponential curve for natural crescendo/decrescendo
- **`EventList` class** — All notes go through humanization by default; `note_raw()` available for intentionally precise events
- **`build_midi()`** — Handles track naming, GM program assignment, and proper event sorting

---

## Per-Song Changes

### Song 1: "Dial Tone Lullaby" (C major, 72 BPM)

**Discoveries:**
- Piano arpeggios used 2 patterns for 76 bars — hypnotic but monotonous
- Synth pad was a flat velocity block throughout
- Drums had zero ghost notes and no fill variation
- Vocal melody had no dynamic contour

**Changes:**
- Piano: 6 arpeggio pattern variations cycling by bar, sustain pedal (CC64) throughout, occasional grace notes (every ~6 bars), chord voicing rotation (root/add9/sus2/min7)
- Synth pad: CC11 expression swells creating breathing dynamics
- Organ: Subtle pitch bend wobble (±200-300 cents) for analog warmth
- Bass: Chromatic approach notes before chord changes, melodic fills
- Drums: Ghost snare notes on off-beats, varied hi-hat patterns, tom fills at section boundaries
- Vocal melody: Contour-based dynamics (higher notes louder), anticipation notes, grace notes
- Bridge: Increased timing jitter (time_amount=15) for rubato feel

### Song 2: "The Machinery of Sunlight" (F major, 92 BPM)

**Discoveries:**
- Signature synth riff was identical every repetition — needs subtle variation
- Power chords had no per-beat velocity shape
- Bass walked the same pattern every bar
- No drum fills at section transitions

**Changes:**
- Synth riff: Staccato/legato variation between bars, alternate endings on repeat bars, velocity emphasis on melodic peak notes
- 5 arpeggio pattern variations with different contours
- Bass: Chromatic walk fills on bar 7 of each 8-bar cycle, octave jumps for energy
- Power chords: Per-beat velocity variation following natural accent pattern
- Drums: Fills at every section boundary (verse→pre-chorus, pre-chorus→chorus), crash cymbals on section entries
- Synth solo: Pitch bend vibrato on sustained notes during instrumental break

### Song 3: "Beautiful Machines" (Eb major, 84 BPM)

**Discoveries:**
- The "big build" had no smooth intensity curve — instruments entered at full volume
- Crescendo section was supposed to be the climax but had flat dynamics
- Piano used only 2 patterns across 120+ bars
- String section had no expression movement

**Changes:**
- Smooth intensity ramp: Linear interpolation over 16-bar crescendo section, each bar slightly louder/more active than the last
- Strings: CC11 expression swells creating orchestral breathing
- 6 piano arpeggio patterns cycling for variety
- Drum fills at every section transition, varied fill patterns
- Organ: Pitch bend wobble for analog character
- Distorted guitar: Varied voicings (power, root+fifth, full) cycling per bar
- Soaring synth lead: Pitch bend vibrato on notes longer than a quarter note
- Decay section: Individual instrument fadeouts in reverse order of entry (guitar first, then organ, drums, synth, bass, pad, piano last)

### Song 4: "Last Signal Home" (G major, 58 BPM, 3/4 waltz)

**Discoveries:**
- No pitch bend events for pedal steel simulation — the core "cosmic country" element was missing
- Fingerpicking used one pattern for the entire song
- Waltz accent pattern wasn't applied (beat 1 emphasis missing)
- Brush drum pattern was identical every bar

**Changes:**
- Pedal steel (synth lead): Actual pitch bend events — bends up from a semitone below the target note, vibrato on sustained notes, bend-and-release gestures
- 4 fingerpicking pattern variations with hammer-on simulation (quick grace notes)
- Waltz-specific accent patterns (beat 1: +8, beat 2: -4, beat 3: -2) applied to all instruments
- Brush drums: Varied patterns bar-to-bar, cross-stick on beat 3 alternatives, waltz fill patterns
- Bridge: Rubato timing (time_amount=15) for expressive stretching
- 5-chord cycle in bridge with chromatic bass approach notes
- Strings: CC11 expression swells for orchestral warmth
- Piano: Enters at bridge with sustained chords under pedal

### Song 5: "Peripheral Glow" (D minor, 70 BPM)

**Discoveries:**
- Organ drone was static — no analog character
- Synth arpeggio used 2 patterns, making it hypnotic but monotonous over 5 minutes
- No dynamic arc between sections — verse and chorus at same intensity
- Bass line too simple for the descending chromatic section
- Drums entered too early, reducing impact

**Changes:**
- Organ drone: Pitch bend wobble throughout for analog warmth, volume ramp in intro, D pedal tone throughout verses
- 6 synth arpeggio patterns cycling, with velocity contouring on beat positions and staccato articulation
- Clean guitar: 4 fingerpicking patterns with varied density, ringing sustain
- Distorted guitar: Enters only at instrumental and chorus 2 — Jazzmaster fuzz power chords with intensity ramp
- Bass: Descending chromatic walk in instrumental section with approach notes, sparse in verse 3/outro
- Drums: Enter only at chorus 1 (not verse), ghost snare notes, ride cymbal pattern in verse 2, crash cymbals at section entries
- Piano: Enters at verse 2 with sustained chords under sustain pedal, arpeggiated during instrumental
- Strings: CC11 expression swells in choruses and instrumental
- Synth lead expression: Pitch bend vibrato during instrumental with increasing depth (building intensity)
- Verse 3: Deliberately sparse — instruments play every other bar, creating space
- Outro: All instruments fade independently

---

## Technical Notes

- All songs use **480 ticks per beat** (standard MIDI resolution)
- Humanization seed is fixed (`random.seed(42)`) for reproducibility
- Every note passes through timing jitter and velocity variation by default
- Track names are descriptive (e.g., "Synth Pad (Juno Warm)", "Distorted Guitar (Jazzmaster Fuzz)") to inform arrangement/mixing
- General MIDI program numbers are consistent across all songs for album cohesion
