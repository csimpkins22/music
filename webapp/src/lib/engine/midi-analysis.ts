/**
 * MIDI ingestion and analysis.
 * Parses Standard MIDI files and extracts track metadata, notes, CC data, pitch bends.
 */

import { Midi } from '@tonejs/midi';
import type { ParsedMidi, ParsedTrack, NoteEvent, CCEvent, PitchBendEvent } from './types';

export function parseMidiFile(midiData: ArrayBuffer): ParsedMidi {
	const midi = new Midi(midiData);

	const bpm = midi.header.tempos.length > 0 ? midi.header.tempos[0].bpm : 120;

	const timeSig = midi.header.timeSignatures.length > 0
		? midi.header.timeSignatures[0].timeSignature
		: [4, 4];

	const tracks: ParsedTrack[] = [];

	for (const track of midi.tracks) {
		// Skip empty tracks (tempo track, etc.)
		if (track.notes.length === 0 && track.controlChanges === undefined) continue;
		if (track.notes.length === 0) continue;

		const notes: NoteEvent[] = track.notes.map((n) => ({
			midi: n.midi,
			name: n.name,
			velocity: n.velocity,
			duration: n.duration,
			time: n.time,
			ticks: n.ticks,
			durationTicks: n.durationTicks
		}));

		// Control changes
		const controlChanges = new Map<number, CCEvent[]>();
		if (track.controlChanges) {
			for (const [ccNum, events] of Object.entries(track.controlChanges)) {
				controlChanges.set(
					parseInt(ccNum),
					events.map((e) => ({
						number: parseInt(ccNum),
						value: e.value,
						time: e.time,
						ticks: e.ticks
					}))
				);
			}
		}

		// Pitch bends — @tonejs/midi provides {time, ticks, value} where value is -1 to 1
		// eslint-disable-next-line @typescript-eslint/no-explicit-any
		const pitchBends: PitchBendEvent[] = ((track as any).pitchBends || []).map((pb: any) => ({
			value: pb.value ?? 0,
			time: pb.time ?? 0,
			ticks: pb.ticks ?? 0
		}));

		// Analysis
		const midiValues = notes.map((n) => n.midi);
		const noteRange = {
			min: Math.min(...midiValues),
			max: Math.max(...midiValues)
		};
		const avgVelocity =
			notes.reduce((sum, n) => sum + n.velocity, 0) / notes.length;

		const duration = midi.duration || 1;
		const noteDensity = notes.length / duration;

		// Compute max polyphony
		const maxPolyphony = computeMaxPolyphony(notes);

		const channel = track.channel ?? -1;
		const isPercussion = channel === 9;

		tracks.push({
			name: track.name || `Track ${tracks.length + 1}`,
			channel,
			program: track.instrument?.number ?? null,
			notes,
			controlChanges,
			pitchBends,
			noteRange,
			avgVelocity,
			noteDensity,
			maxPolyphony,
			isPercussion,
			noteCount: notes.length
		});
	}

	return {
		name: midi.name || 'Untitled',
		bpm,
		timeSignature: { numerator: timeSig[0], denominator: timeSig[1] },
		duration: midi.duration,
		tracks
	};
}

function computeMaxPolyphony(notes: NoteEvent[]): number {
	if (notes.length === 0) return 0;

	// Create events: +1 for note start, -1 for note end
	const events: { time: number; delta: number }[] = [];
	for (const n of notes) {
		events.push({ time: n.time, delta: 1 });
		events.push({ time: n.time + n.duration, delta: -1 });
	}
	events.sort((a, b) => a.time - b.time || a.delta - b.delta);

	let current = 0;
	let max = 0;
	for (const e of events) {
		current += e.delta;
		if (current > max) max = current;
	}
	return max;
}

export function formatDuration(seconds: number): string {
	const m = Math.floor(seconds / 60);
	const s = Math.floor(seconds % 60);
	return `${m}:${s.toString().padStart(2, '0')}`;
}
