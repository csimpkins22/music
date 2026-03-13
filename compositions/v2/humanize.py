"""
Shared humanization and MIDI utility library for v2 compositions.

Provides timing jitter, velocity variation, swing, dynamic expression,
and the event-to-MIDI conversion pipeline.
"""

import mido
import random
import math

TICKS = 480
BAR4 = TICKS * 4    # bar in 4/4
BAR3 = TICKS * 3    # bar in 3/4
HALF = TICKS * 2
QUARTER = TICKS
EIGHTH = TICKS // 2
SIXTEENTH = TICKS // 4
DOTTED_HALF = QUARTER * 3
DOTTED_QUARTER = QUARTER + EIGHTH
WHOLE = QUARTER * 4

# Seed for reproducibility
random.seed(42)

def N(name, octave=4):
    """Note name to MIDI number. E.g. N('Eb',4) = 63."""
    notes = {'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}
    base = name[0]
    mod = 0
    if len(name) > 1:
        if name[1] == 'b': mod = -1
        elif name[1] == '#': mod = 1
    return 12 * (octave + 1) + notes[base] + mod

def make_chord(root, quality='major'):
    if quality == 'major': return [root, root+4, root+7]
    elif quality == 'minor': return [root, root+3, root+7]
    elif quality == 'power': return [root, root+7, root+12]
    elif quality == 'sus2': return [root, root+2, root+7]
    elif quality == 'sus4': return [root, root+5, root+7]
    elif quality == 'add9': return [root, root+4, root+7, root+14]
    elif quality == 'min7': return [root, root+3, root+7, root+10]
    elif quality == 'maj7': return [root, root+4, root+7, root+11]
    elif quality == '7': return [root, root+4, root+7, root+10]
    elif quality == 'dim': return [root, root+3, root+6]
    elif quality == '6': return [root, root+4, root+7, root+9]
    return [root, root+4, root+7]


# ============================================================
# HUMANIZATION ENGINE
# ============================================================

def h_time(tick, amount=8):
    """Humanize a tick position with random jitter.
    amount: max offset in ticks (±). Default ±8 ticks ≈ ±10ms at 120bpm."""
    return max(0, tick + random.randint(-amount, amount))

def h_vel(vel, amount=5):
    """Humanize velocity with random variation."""
    return max(1, min(127, vel + random.randint(-amount, amount)))

def swing_offset(eighth_index, amount=18):
    """Add swing to 8th notes. Even 8ths stay, odd 8ths push late.
    amount: ticks to delay odd 8ths. 18 ticks ≈ light swing."""
    if eighth_index % 2 == 1:
        return random.randint(amount - 4, amount + 4)
    return 0

def accent_beat(beat_in_bar, style='natural'):
    """Return velocity boost for a given beat position.
    beat_in_bar: 0-based beat number.
    Simulates natural accenting patterns."""
    if style == 'natural':
        # Beat 1 strongest, beat 3 next, 2 and 4 lighter
        accents = {0: 6, 1: -3, 2: 3, 3: -2}
        return accents.get(beat_in_bar, 0)
    elif style == 'waltz':
        accents = {0: 8, 1: -4, 2: -2}
        return accents.get(beat_in_bar, 0)
    return 0

def crescendo_vel(base_vel, position, total, target_vel):
    """Compute velocity along a crescendo/decrescendo curve.
    Uses a slight exponential curve for natural feel."""
    ratio = position / max(1, total - 1)
    # Slight exponential curve
    curved = ratio ** 1.3
    return int(base_vel + (target_vel - base_vel) * curved)

def breathing_vel(base_vel, bar_num, cycle_bars=8, depth=6):
    """Subtle velocity undulation over multi-bar phrases.
    Simulates a performer 'breathing' with the music."""
    phase = (bar_num % cycle_bars) / cycle_bars * 2 * math.pi
    offset = int(depth * math.sin(phase))
    return max(1, min(127, base_vel + offset))


# ============================================================
# EVENT SYSTEM
# ============================================================

class EventList:
    """Collects note events with humanization applied."""

    def __init__(self):
        self.events = []

    def note(self, ch, note, vel, start, dur, humanize_time=True, humanize_vel=True,
             time_amount=8, vel_amount=5):
        """Add a humanized note."""
        if humanize_time:
            start = h_time(start, time_amount)
        if humanize_vel:
            vel = h_vel(vel, vel_amount)
        vel = max(1, min(127, vel))
        dur = max(10, dur)
        self.events.append(('on', start, ch, note, vel))
        self.events.append(('off', start + dur, ch, note, 0))

    def note_raw(self, ch, note, vel, start, dur):
        """Add a note with no humanization."""
        vel = max(1, min(127, vel))
        self.events.append(('on', start, ch, note, vel))
        self.events.append(('off', start + dur, ch, note, 0))

    def cc(self, ch, control, value, tick):
        """Add a control change event."""
        self.events.append(('cc', tick, ch, control, value))

    def pitch_bend(self, ch, value, tick):
        """Add a pitch bend event. value: -8192 to 8191."""
        self.events.append(('pb', tick, ch, value, 0))


def build_midi(events_obj, song_name, bpm, time_sig_num=4, time_sig_den=4,
               total_bars=80, channel_names=None, channel_programs=None,
               output_path=None):
    """Convert EventList to a MIDI file."""

    if channel_names is None:
        channel_names = {
            0: 'Piano', 1: 'Synth Pad', 2: 'Synth Lead', 3: 'Clean Guitar',
            4: 'Distorted Guitar', 5: 'Organ', 6: 'Bass', 7: 'Strings',
            8: 'Vocal Melody', 9: 'Drums',
        }
    if channel_programs is None:
        channel_programs = {
            0: 0, 1: 89, 2: 81, 3: 27, 4: 30, 5: 19, 6: 33, 7: 49, 8: 85,
        }

    bar_ticks = TICKS * time_sig_num

    mid = mido.MidiFile(ticks_per_beat=TICKS)

    # Track 0: tempo/time sig
    tempo_track = mido.MidiTrack()
    mid.tracks.append(tempo_track)
    tempo_track.append(mido.MetaMessage('track_name', name=song_name, time=0))
    tempo_track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(bpm), time=0))
    tempo_track.append(mido.MetaMessage('time_signature', numerator=time_sig_num,
                                         denominator=time_sig_den, time=0))
    tempo_track.append(mido.MetaMessage('end_of_track', time=total_bars * bar_ticks))

    # Organize events by channel
    channels = {}
    for ev in events_obj.events:
        ev_type = ev[0]
        ch = ev[2]
        if ch not in channels:
            channels[ch] = []
        channels[ch].append(ev)

    for ch in sorted(channels.keys()):
        track = mido.MidiTrack()
        mid.tracks.append(track)
        name = channel_names.get(ch, f'Channel {ch}')
        track.append(mido.MetaMessage('track_name', name=name, time=0))

        if ch in channel_programs:
            track.append(mido.Message('program_change', channel=ch,
                                       program=channel_programs[ch], time=0))

        # Sort: by tick, then offs before ons, then CCs
        def sort_key(e):
            type_order = {'off': 0, 'cc': 1, 'pb': 1, 'on': 2}
            return (e[1], type_order.get(e[0], 1))

        sorted_events = sorted(channels[ch], key=sort_key)

        current_tick = 0
        for ev in sorted_events:
            ev_type = ev[0]
            tick = ev[1]
            delta = max(0, tick - current_tick)

            if ev_type == 'on':
                _, _, ch_num, note, vel = ev
                track.append(mido.Message('note_on', channel=ch_num, note=note,
                                           velocity=vel, time=delta))
            elif ev_type == 'off':
                _, _, ch_num, note, _ = ev
                track.append(mido.Message('note_off', channel=ch_num, note=note,
                                           velocity=0, time=delta))
            elif ev_type == 'cc':
                _, _, ch_num, control, value = ev
                track.append(mido.Message('control_change', channel=ch_num,
                                           control=control, value=value, time=delta))
            elif ev_type == 'pb':
                _, _, ch_num, value, _ = ev
                track.append(mido.Message('pitchwheel', channel=ch_num,
                                           pitch=value, time=delta))

            current_tick = tick

        track.append(mido.MetaMessage('end_of_track', time=QUARTER))

    mid.save(output_path)
    print(f"Saved: {output_path}")
    print(f"  Tracks: {len(mid.tracks)}, Duration: {mid.length:.1f}s ({mid.length/60:.1f} min)")
    return mid
