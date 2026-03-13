# Peripheral Glow — Logic Pro Setup Guide

A detailed, track-by-track Logic Pro project setup for recreating "Peripheral Glow" from the Grandaddy-style MIDI compositions. This guide translates every synthesis parameter, effect chain, and mix setting into specific Logic Pro instruments, plugins, and values.

---

## Project Settings

| Setting | Value |
|---------|-------|
| **Tempo** | 70 BPM |
| **Time Signature** | 4/4 |
| **Key** | D minor |
| **Sample Rate** | 48 kHz (or 44.1 kHz) |
| **Bit Depth** | 24-bit |
| **Total Duration** | ~5:08 (90 bars) |

### Song Structure

| Section | Bars | Description |
|---------|------|-------------|
| Ambient Intro | 1–8 | Organ drone + synth arpeggio emerge from silence |
| Verse 1 | 9–24 | Dm–F–C–Gm cycle (4 bars each), synth arpeggio + pad + bass |
| Chorus 1 | 25–32 | Bb–F–A7–Dm, clean guitar + strings enter, drums enter |
| Verse 2 | 33–48 | Piano enters, ghost notes on drums, fuller arrangement |
| Chorus 2 | 49–56 | All instruments present, biggest chorus energy |
| Silence/Drone | 57–58 | Everything drops out except organ drone |
| Extended Instrumental | 59–74 | Descending bass line (Dm–Dm/C–Bb–A), distorted guitar wall, climax |
| Verse 3 (Sparse) | 75–82 | Stripped back, quiet vocal + organ + arpeggio, emotional resolution |
| Outro Fade | 83–90 | Dissolves to organ drone, exponential pitch wobble, final grounded D |

---

## Track List Overview

Create 11 tracks in this order:

| # | Track Name | Logic Instrument | Color | Pan |
|---|-----------|-----------------|-------|-----|
| 1 | Organ Drone | Vintage B3 | Dark Red | -20 (slightly L) |
| 2 | Synth Arpeggio | Retro Synth | Cyan | +25 (slightly R) |
| 3 | Synth Pad | Retro Synth | Blue | +15 (slightly R) |
| 4 | Bass | Retro Synth | Brown | Center |
| 5 | Piano | Studio Grand (Steinway) | Ivory/White | -10 (slightly L) |
| 6 | Vocal Melody | Retro Synth | Gold | Center |
| 7 | Clean Guitar | Studio Horns (FM patch) or Retro Synth FM | Green | -30 (L) |
| 8 | Distorted Guitar | Retro Synth + Pedalboard | Orange | +35 (R) |
| 9 | Strings | Studio Strings | Purple | Center |
| 10 | Synth Lead Motif | Retro Synth | Teal | +10 (slightly R) |
| 11 | Drums | Drum Kit Designer | Gray | Center |

---

## Track 1: Organ Drone

**Role:** Sustained D pedal tone — the harmonic anchor present in every section. This is the hypnotic foundation of the entire song.

### Instrument: Vintage B3

Use Logic's **Vintage B3** organ. This is the centerpiece drone — it should feel alive but steady, like a breathing machine.

**Drawbar Settings (approximating a warm, sustained tone):**

| Drawbar | 16' | 5⅓' | 8' | 4' | 2⅔' | 2' | 1⅗' | 1⅓' | 1' |
|---------|-----|------|-----|-----|------|-----|------|------|-----|
| Value | 8 | 3 | 8 | 4 | 0 | 0 | 0 | 0 | 0 |

Pull the 16' and 8' drawbars full or near-full for a dark, warm fundamental. Keep upper harmonics minimal — this is a drone, not a lead.

**Vintage B3 Settings:**
- **Percussion:** Off
- **Vibrato/Chorus:** C1 or V1 (subtle wobble — this replaces the `detune: 6` and `vibrato frequency: 5, depth: 0.1`)
- **Key Click:** Off or minimal
- **Overdrive:** Off (clean drone)

**Rotor Cabinet:**
- **Speed:** Slow (Chorale) — always slow, never fast Leslie
- **Brake:** Engaged (stopped rotor) for the most static drone sound
- Alternatively, set rotor to Slow for very gentle movement

**Insert Effects (on the channel strip):**
1. **Tremolo** (Modulation → Tremolo) — Rate: 5 Hz, Depth: 10%, to simulate the vibrato `wet: 0.4`. Use symmetrical mode for even amplitude wobble.
2. **ChromaVerb** — Decay: 2.0s, Wet: 30%, Dark preset. Warm hall reverb.

**Volume:** -14 dB (pushed back in the mix — this is felt, not heard prominently)

**Performance Notes:**
- Notes played: Sustained D2–D3 range (pedal tones), occasional C3/A3 movement
- The organ is present in ALL sections — even during the "silence" at bars 57–58
- Pitch bend automation: ±200 cents in verses, ±300 cents in instrumental, ±400 cents in outro bars 86–88, settling to ±50 cents in final bar
- In Logic: Use **Pitch Bend** automation lane. Set pitch bend range to ±2 semitones (200 cents). For wider bends in the instrumental/outro, automate gradually

### Pitch Bend Automation Guide

Draw pitch bend automation as slow, random sine-wave-like curves:
- **Intro/Verses/Choruses:** Gentle, ±1 semitone wandering (random, slow)
- **Silence section (bars 57–58):** Tighter, ±0.5 semitone (meditative stillness)
- **Instrumental (bars 59–74):** Wider, ±1.5 semitones (increased energy)
- **Outro bars 83–86:** ±0.75 semitone (fading)
- **Outro bars 87–89:** Dramatic, ±2 semitones (climactic dissolution)
- **Bar 90 (final):** ±0.25 semitone, settling to center (returns to earth)

---

## Track 2: Synth Arpeggio

**Role:** Hypnotic 16th-note arpeggio pattern — the constant motion that drives the song forward. Think "The Crystal Lake" shimmering motion.

### Instrument: Retro Synth (Analog mode)

**Oscillator:**
- **Wave:** Sawtooth
- **Detune:** +4 cents (use Fine Tune in Retro Synth, or a second oscillator slightly detuned)

If using dual oscillators:
- OSC 1: Sawtooth, 0 cents
- OSC 2: Sawtooth, +4 cents
- Mix: 50/50

**Amplitude Envelope:**
- Attack: 0.02s (20ms — snappy for arpeggiated notes)
- Decay: 0.3s
- Sustain: 50%
- Release: 0.8s

**Filter:**
- Type: Low Pass 24dB
- Cutoff: ~60% (let it breathe but not be too bright)
- Resonance: 10–15%

**Insert Effects Chain:**
1. **AutoFilter** (Filter → AutoFilter):
   - Rate: 0.3 Hz
   - Frequency: 400 Hz
   - Range: 2.5 octaves
   - Mix: 30%
   - Use LFO modulation with sine wave shape for smooth sweeping
2. **Delay Designer** or **Stereo Delay** (Ping Pong mode):
   - Delay Time: 1/8 note (synced to tempo)
   - Feedback: 25%
   - Wet: 20%

**Send Levels:**
- Bus 1 (Reverb): 35%
- Bus 2 (Delay): 20%

**Volume:** -8 dB
**Pan:** +25 (right of center)

**Performance Notes:**
- Note range: D5–D6 (high register, airy)
- Plays continuous 16th notes throughout — the rhythmic engine
- Velocity: Starts quiet (vel 25) in intro, builds to 45 in verses, 52 in choruses, 65+ in instrumental
- **Pitch bend in instrumental section:** Sine wave oscillation, depth ramps from ±1 to ±4 semitones across the 16-bar instrumental. Draw this as automation increasing in amplitude over bars 59–74, then reset at bar 75.

---

## Track 3: Synth Pad

**Role:** Warm harmonic bed — the Juno-60 shimmer. Sustained chords that swell and breathe underneath everything.

### Instrument: Retro Synth (Analog mode)

**Oscillator:**
- **Wave:** Sawtooth
- **Detune:** +8 cents (the Juno shimmer — key to this sound!)

Dual oscillator approach:
- OSC 1: Sawtooth, 0 cents
- OSC 2: Sawtooth, +8 cents
- Mix: 50/50

**Amplitude Envelope:**
- Attack: 0.4s (slow swell-in)
- Decay: 0.8s
- Sustain: 70%
- Release: 2.0s (long tail)

**Filter:**
- Type: Low Pass 12dB or 24dB
- Cutoff: ~55% (warm, not too bright)
- Resonance: 5–10%

**Insert Effects Chain:**
1. **Ensemble** (Logic's Chorus, or use Retro Synth's built-in chorus):
   - Rate: 0.5 Hz
   - Delay Time: 3.5 ms
   - Depth: 70%
   - Mix: 60%
   - This is the defining Juno-60 chorus effect — don't skip this
2. **ChromaVerb:**
   - Decay: 2.5s
   - Wet: 35%
   - Use "Blooming" or "Hall" algorithm

**Send Levels:**
- Bus 1 (Reverb): 40%
- Bus 2 (Delay): 15%

**Volume:** -10 dB
**Pan:** +15 (slightly right)

**Expression Automation (CC11):**
- Draw a slow breathing curve on the Expression automation lane
- 4-bar phrases: rises over bars 1–2, falls over bars 3–4
- Range: 60–120 (MIDI CC value)
- In Logic, use the **Modulation** or **Expression** automation lane

**Performance Notes:**
- Note range: D4–Bb5 (warm mid-range pads)
- Chord voicings: open triads and add9 chords following the progression
- Velocity: 42 (verses), 65 (choruses), increases through instrumental

---

## Track 4: Bass

**Role:** Warm, supportive bass with chromatic walk-ups in verses and the crucial descending bass line in the instrumental section.

### Instrument: Retro Synth (Analog mode, Mono)

**Oscillator:**
- **Wave:** Triangle (warm, round bass tone)
- **Mono Mode:** On (single voice, for classic bass behavior)
- **Glide:** Off (or very short, 5ms, for the chromatic walk-ups)

**Amplitude Envelope:**
- Attack: 0.02s (20ms — slight pluck)
- Decay: 0.3s
- Sustain: 60%
- Release: 0.4s

**Filter:**
- Type: Low Pass 24dB
- Cutoff: ~40% (dark and warm)
- Resonance: 0%
- **Filter Envelope:**
  - Attack: 0.01s
  - Decay: 0.2s
  - Sustain: 30%
  - Release: 0.3s
  - Envelope Amount: +2.5 octaves (creates that subtle "bwow" on note attack)

**Insert Effects:**
1. **Compressor:**
   - Threshold: -20 dB
   - Ratio: 4:1
   - Attack: 10ms
   - Release: 100ms
   - This keeps the bass level and controlled

**Send Levels:**
- Bus 1 (Reverb): 8% (very dry — bass stays tight)
- Bus 2 (Delay): 0% (no delay on bass)

**Volume:** -6 dB
**Pan:** Center

**Performance Notes:**
- Note range: A1–F2 (deep, supportive)
- Verse bass: D2, F2, C2, G2 (whole notes, one per 4-bar chord)
- Chorus bass: Bb1, F2, A1, D2
- **Instrumental descending line (the key moment):** D2 → C2 → Bb1 → Bb1 → A1 → A1 (6-bar repeating cycle)
- Chromatic walk-ups connect chord changes in verses (e.g., C#→D or E→F fills)
- Velocity: 55 (verse), 60 (chorus), 60+ (instrumental)
- Final 4 bars (outro): Quiet D2, velocity 18→12, barely audible anchor

---

## Track 5: Piano

**Role:** Emotional anchor — enters in Verse 2, adds pad voicings and arpeggiated figures in the instrumental. Drenched in reverb ("bottom of a well").

### Instrument: Studio Grand (Steinway Grand Piano)

Use Logic's **Studio Piano** or **Steinway Grand** from the built-in library.

**Settings:**
- **Tone:** Warm (roll off high end slightly)
- **Ambience:** Medium (the insert reverb will add more)
- **Dynamics:** Full range

**Insert Effects:**
1. **ChromaVerb** (or Space Designer):
   - **Decay: 3.5s** — this is the signature "bottom of a well" piano reverb
   - **Wet: 45%** — heavily wet, the reverb IS the sound
   - Algorithm: Hall or Chamber (large, diffuse)
   - Pre-delay: 20–30ms
   - High cut: ~6 kHz (darken the reverb tail)

**Send Levels:**
- Bus 1 (Reverb): 30%
- Bus 2 (Delay): 10%

**Volume:** -6 dB
**Pan:** -10 (slightly left)

**Sustain Pedal Automation:**
- CC64 engaged at the start of each bar (value 127)
- Released just before the bar ends (value 0)
- Applied to all piano sections (Verse 2, Chorus 2, Instrumental, Verse 3, Outro)

**Performance Notes:**
- Note range: D4–D6
- Does NOT play in Verse 1 or Chorus 1 — enters at bar 33 (Verse 2)
- Verse 2: Pad voicings (sustained chords)
- Instrumental: Arpeggio patterns, climbing to D6
- Velocity: 48 (Verse 2), 55 (Chorus 2), 45–60 (Instrumental)

---

## Track 6: Vocal Melody

**Role:** The primary melodic hook line. A bright, vocal-like synth tone that sits forward in the mix.

### Instrument: Retro Synth (Analog mode)

**Oscillator:**
- **Wave:** Sine (pure, vocal-like)
- **Detune:** +3 cents (subtle warmth)

**Amplitude Envelope:**
- Attack: 0.05s (50ms — slight softness to entry)
- Decay: 0.2s
- Sustain: 60%
- Release: 0.6s

**Filter:**
- Type: Low Pass 12dB
- Cutoff: ~70% (keep it bright and forward)
- Resonance: 5%

**Insert Effects Chain:**
1. **Scanner Vibrato** (Modulation → Scanner Vibrato):
   - Rate: 5 Hz
   - Depth: 15%
   - Mix: 35%
   - Use a gentle, even vibrato — no chorus component
2. **ChromaVerb:**
   - Decay: 2.0s
   - Wet: 35%
3. **Stereo Delay** (Ping Pong):
   - Delay Time: Dotted 1/8 note
   - Feedback: 20%
   - Wet: 15%

**Send Levels:**
- Bus 1 (Reverb): 30%
- Bus 2 (Delay): 20%

**Volume:** -5 dB (forward in the mix — this is the "voice")
**Pan:** Center

**Performance Notes:**
- Note range: D4–D6 (wide emotional range)
- Verse phrases at velocity 55–58, Chorus 62–68, Verse 3 (sparse) at 30–40
- Grace notes: Occasional phrases play a semitone below before resolving up
- Verse 3 emotional arc: D5→A4→F4→D4 descending, then silence, then C#5→D5 chromatic approach (the "homecoming" moment)
- Anticipation: Some phrases pulled slightly ahead of the beat for urgency

---

## Track 7: Clean Guitar

**Role:** Sparse atmospheric chords — ringing arpeggios that enter at Chorus 1. Think Jazzmaster clean tone with chorus shimmer.

### Instrument: Retro Synth (FM mode) or Alchemy

Using **Retro Synth in FM mode** to emulate clean electric guitar:

**FM Settings:**
- **Harmonicity:** 1.5
- **Modulation Index (FM Amount):** 2 (low — clean, bell-like)
- **Carrier Wave:** Triangle
- **Modulator Wave:** Sine

**Amplitude Envelope:**
- Attack: 0.01s (fast pluck)
- Decay: 0.6s
- Sustain: 20% (notes ring then fade)
- Release: 1.2s (long ring-out)

**Modulation Envelope:**
- Attack: 0.01s
- Decay: 0.3s
- Sustain: 10%
- Release: 0.5s
- (This makes the "pluck" brighter on attack, mellower as it sustains)

**Insert Effects Chain:**
1. **Ensemble** (Chorus):
   - Rate: 1.2 Hz
   - Delay: 2.5ms
   - Depth: 30%
   - Mix: 25%
2. **ChromaVerb:**
   - Decay: 1.8s
   - Wet: 30%

**Send Levels:**
- Bus 1 (Reverb): 25%
- Bus 2 (Delay): 15%

**Volume:** -9 dB
**Pan:** -30 (left)

**Performance Notes:**
- Note range: D4–D5 (ringing midrange chords)
- Does NOT play in Verse 1 — enters at Chorus 1 (bar 25)
- Sparse chords, letting notes ring
- Velocity: 52 (Chorus 1), 50 (Verse 2), 55 (Chorus 2)

---

## Track 8: Distorted Guitar

**Role:** Fuzzy Jazzmaster power chords — only appears in the extended instrumental section (bars 59–74). The "wall of sound" moment. Also plays a single-note melody in bars 67–70.

### Instrument: Retro Synth (FM mode) + Pedalboard

**FM Settings (aggressive):**
- **Harmonicity:** 2.5 (complex harmonics)
- **Modulation Index (FM Amount):** 8 (high — produces distortion-like overtones)
- **Carrier Wave:** Sawtooth
- **Modulator Wave:** Square (harsh, aggressive modulation)

**Amplitude Envelope:**
- Attack: 0.01s (immediate)
- Decay: 0.4s
- Sustain: 60%
- Release: 0.8s

**Modulation Envelope:**
- Attack: 0.01s
- Decay: 0.2s
- Sustain: 50%
- Release: 0.4s

**Insert Effects Chain:**
1. **Distortion** (or Pedalboard → Fuzz/Overdrive):
   - If using Logic's **Distortion** plugin: Drive ~30–40%, Tone ~50%, Output to taste
   - If using **Pedalboard**: Use "Grinder" or "Fuzz Machine" pedal at moderate settings
   - Target: "Fuzzy but notey" — you should still hear chord tones clearly (the DOD FX55B character)
2. **Channel EQ:**
   - Low: -2 dB @ 200 Hz (reduce mud)
   - Mid: +4 dB @ 1–2 kHz (cut through the mix)
   - High: -3 dB @ 4 kHz (tame harshness)
3. **ChromaVerb:**
   - Decay: 1.2s (shorter — don't wash out the distortion)
   - Wet: 20%

**Send Levels:**
- Bus 1 (Reverb): 15%
- Bus 2 (Delay): 10%

**Volume:** -8 dB
**Pan:** +35 (right)

**Performance Notes:**
- Only plays bars 59–74 (Extended Instrumental) — MUTE for all other sections
- Power chords: D4–Bb4 range
- Single-note melody (bars 67–70): Bb→A/G→A/Bb→G/F/D descending contour, velocity +5 emphasis
- Velocity ramps from 55 to 80 over the 16-bar section (intensity builds)
- This is the climactic "wall" moment — it should feel overwhelming when it enters

---

## Track 9: Strings

**Role:** Orchestral swells in choruses and instrumental section. Slow, lush, pad-like strings that add emotional weight.

### Instrument: Studio Strings (or Alchemy "Strings" preset)

Use Logic's **Studio Strings** for realistic ensemble, or **Alchemy** with a Strings preset and these adjustments:

**If using Retro Synth (Analog) as fallback:**

**Oscillator:**
- **Wave:** Sawtooth
- **Detune:** +5 cents

**Amplitude Envelope:**
- Attack: 0.8s (slow, realistic bow attack — essential)
- Decay: 0.5s
- Sustain: 70%
- Release: 2.0s (long fade)

**Insert Effects Chain:**
1. **Ensemble** (Chorus):
   - Rate: 0.8 Hz
   - Delay: 3ms
   - Depth: 40%
   - Mix: 30%
2. **ChromaVerb:**
   - Decay: 3.0s
   - Wet: 40%
   - Use a "Hall" algorithm (large, orchestral)

**Send Levels:**
- Bus 1 (Reverb): 40%
- Bus 2 (Delay): 10%

**Volume:** -12 dB (sits back in the mix, supportive)
**Pan:** Center

**Expression Automation (CC11):**
- Bell-curve swells over 2-bar phrases
- Range: 50–120 (MIDI CC value)
- Attack phase (bar 1): Rise from 60 to 110
- Release phase (bar 2): Fall from 110 back to 60

**Performance Notes:**
- Note range: D5–F6 (high register, ethereal)
- Enters at Chorus 1 (bar 25)
- Velocity: 42 (Chorus 1), 50 (Chorus 2), 45–70 (Instrumental, building)

---

## Track 10: Synth Lead Motif

**Role:** Rising D–F–A motif that appears 4 times with escalating intensity, plus counter-melody. A square-wave lead that cuts through.

### Instrument: Retro Synth (Analog mode)

**Oscillator:**
- **Wave:** Square (characteristic, slightly hollow lead tone)
- **Pulse Width:** ~50% (true square) or experiment with 40% for slight nasal quality

**Amplitude Envelope:**
- Attack: 0.02s
- Decay: 0.3s
- Sustain: 50%
- Release: 0.8s

**Filter:**
- Type: Low Pass 12dB
- Cutoff: ~65%
- Resonance: 15% (slight peak for presence)

**Insert Effects Chain:**
1. **AutoFilter** (Filter → AutoFilter):
   - Rate: 0.3 Hz
   - Depth: 30%
   - Sine LFO shape, gentle sweep for movement without being obvious
2. **Stereo Delay** (Ping Pong):
   - Delay Time: 1/8 note
   - Feedback: 25%
   - Wet: 20%

**Send Levels:**
- Bus 1 (Reverb): 35%
- Bus 2 (Delay): 20%

**Volume:** -8 dB
**Pan:** +10 (slightly right)

**Performance Notes:**
- The rising motif (D–F–A) appears in Verse 1, with each appearance climbing an octave: D3→D4→D5→D6
- Velocity escalates dramatically: 30 → 50 → 75 → 100 (each appearance louder)
- Counter-melody in the E5–G5 range
- Inverted on 2nd and 4th appearances (A–F–D instead of D–F–A)
- Echoes into Verse 3 at lower velocity

---

## Track 11: Drums

**Role:** Sparse, patient rhythm. Enters at Chorus 1 — no drums in Verse 1 or the intro. Ghost notes in Verse 2. Builds through the instrumental.

### Instrument: Drum Kit Designer

**Kit Selection:** Use a vintage/indie kit — avoid anything too polished. Suggestions:
- **SoCal** kit (dry, warm)
- **Brooklyn** kit (indie character)
- **East Bay** kit
- Or any kit, then process with the effects below

**Kit Tuning:**
- Kick: Tune down slightly for warmth
- Snare: Medium tuning, slightly dampened
- Hi-hats: Reduce brightness

**Insert Effects (on the Drum Bus):**
1. **Compressor:**
   - Threshold: -15 dB
   - Ratio: 3:1
   - Attack: 5ms
   - Release: 50ms
   - (Glue compression — holds the kit together)
2. **ChromaVerb:**
   - Decay: 0.6s (short, roomy — not a big hall)
   - Wet: 15%

**Send Levels:**
- Bus 1 (Reverb): 12%
- Bus 2 (Delay): 5%

**Volume:** -7 dB
**Pan:** Center

**Drum Pattern Notes:**
- **No drums bars 1–24** (Verse 1 is drumless — builds tension)
- **Chorus 1 (bars 25–32):** Basic kick + snare pattern, velocity ~75
- **Verse 2 (bars 33–48):** Ghost notes — even bars: ghost kick on the "and" of beat 2 (vel 25), odd bars: ghost snare on the "and" of beat 4 (vel 20)
- **Chorus 2 (bars 49–56):** Full pattern, velocity ~75–85
- **Instrumental (bars 59–74):** Building intensity, velocity 60→80, crash cymbals at section entries
- **Verse 3 (bars 75–82):** Sparse or absent
- **Outro:** Fading out

**MIDI Note Mapping (GM Standard):**
- Kick: C1 (MIDI 36)
- Snare: D1 (MIDI 38)
- Closed Hi-hat: F#1 (MIDI 42)
- Open Hi-hat: A#1 (MIDI 46)
- Ride: D#2 (MIDI 51)
- Crash: C#2 (MIDI 49)

---

## Bus Effects Setup

Create two auxiliary bus sends plus the master bus processing.

### Bus 1: Reverb Bus

**Plugin:** ChromaVerb (or Space Designer)
- **Decay:** 2.8s
- **Wet:** 100% (this is a parallel send — fully wet)
- **Algorithm:** Hall or Blooming
- **Pre-delay:** 15–20ms
- **Damping:** Roll off highs above 6 kHz
- **Character:** Warm, diffuse, enveloping

### Bus 2: Delay Bus

**Plugin:** Stereo Delay or Tape Delay
- **Delay Time:** Dotted 1/8 note (synced to 70 BPM)
- **Feedback:** 30%
- **Wet:** 100% (parallel send — fully wet)
- **High Cut:** ~5 kHz (darken the repeats for lo-fi character)
- **Low Cut:** ~200 Hz (keep repeats from getting muddy)

### Master Bus (Stereo Output)

Apply these in order on the stereo output channel:

1. **Compressor (Glue):**
   - Threshold: -14 dB
   - Ratio: 2.5:1
   - Attack: 20ms
   - Release: 150ms
   - Gentle glue — should barely be compressing (1–3 dB reduction)

2. **Channel EQ:**
   - Low shelf: +1 dB @ 250 Hz (subtle warmth)
   - Mids: Flat
   - High shelf: -1 dB @ 5 kHz (take the edge off — lo-fi ceiling)

---

## Mix Summary — Volume & Pan Reference

| Track | Volume | Pan | Bus 1 (Reverb) | Bus 2 (Delay) |
|-------|--------|-----|-----------------|----------------|
| Organ Drone | -14 dB | -20 | 35% | 10% |
| Synth Arpeggio | -8 dB | +25 | 35% | 20% |
| Synth Pad | -10 dB | +15 | 40% | 15% |
| Bass | -6 dB | 0 | 8% | 0% |
| Piano | -6 dB | -10 | 30% | 10% |
| Vocal Melody | -5 dB | 0 | 30% | 20% |
| Clean Guitar | -9 dB | -30 | 25% | 15% |
| Distorted Guitar | -8 dB | +35 | 15% | 10% |
| Strings | -12 dB | 0 | 40% | 10% |
| Synth Lead Motif | -8 dB | +10 | 35% | 20% |
| Drums | -7 dB | 0 | 12% | 5% |

---

## MIDI Import Notes

Import `05_peripheral_glow.mid` into Logic Pro:

1. **File → Import → MIDI File** (or drag the .mid file into the arrangement)
2. Logic will create tracks for each MIDI channel automatically
3. Reassign each track to the instruments described above based on channel mapping:

| MIDI Channel | Track Assignment |
|-------------|-----------------|
| Ch 0 | Piano |
| Ch 1 | Synth Pad |
| Ch 2 | Synth Arpeggio |
| Ch 3 | Clean Guitar |
| Ch 4 | Distorted Guitar |
| Ch 5 | Organ Drone |
| Ch 6 | Bass |
| Ch 7 | Strings |
| Ch 8 | Vocal Melody |
| Ch 9 | Drums |
| Ch 10 | Synth Lead Motif |

4. After import, the MIDI data already contains:
   - All notes with humanized timing and velocity
   - CC11 (Expression) automation on Synth Pad and Strings
   - CC64 (Sustain Pedal) on Piano
   - Pitch Bend data on Organ Drone and Synth Arpeggio
   - Ghost note velocities on Drums

---

## Production Character Notes

### The Lo-Fi Ceiling
This isn't a pristine modern production. Everything should feel slightly warm and soft:
- Roll off highs above 10–12 kHz on the master
- Don't over-compress — let dynamics breathe
- Embrace the reverb — it's supposed to sound cavernous
- The organ drone should be felt as a constant presence, not listened to directly

### The Build
The song's emotional arc depends on the gradual accumulation of layers:
- Bars 1–8: Just organ + arpeggio (two voices in a vast space)
- Layers add one by one through verses and choruses
- Bars 59–74: Everything at once (the climactic wall)
- Bars 75–90: Reverse dissolution back to just the organ drone
- The last sound should be a single, warm, grounded D

### The Descending Bass Line
The instrumental section's Dm→Dm/C→Bb→A descent is the emotional core of the piece. Make sure the bass is audible and the harmonic movement is clear. This is the "augmented climb" effect from "The Crystal Lake."

### Space and Silence
The 2-bar "silence" at bars 57–58 (where only the organ drone remains) is critical. It creates anticipation before the instrumental explosion. Don't fill it — let the drone breathe alone.
