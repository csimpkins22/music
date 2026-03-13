/**
 * Performance interpretation layer.
 * Adds role-aware humanization on top of existing MIDI humanization.
 */

import type { NoteEvent, TrackRole, StyleProfile } from './types';

/**
 * Apply guitar strum offset to simultaneous notes.
 * For chord-like note clusters on guitar tracks, offset notes
 * by a small amount (low to high) to simulate strumming.
 */
export function applyStrumOffset(notes: NoteEvent[], strumTimeMs: number = 12): NoteEvent[] {
	const result: NoteEvent[] = [];
	const tolerance = 0.01; // 10ms window for "simultaneous" notes

	let i = 0;
	while (i < notes.length) {
		// Find cluster of simultaneous notes
		const cluster: NoteEvent[] = [notes[i]];
		let j = i + 1;
		while (j < notes.length && Math.abs(notes[j].time - notes[i].time) < tolerance) {
			cluster.push(notes[j]);
			j++;
		}

		if (cluster.length > 1) {
			// Sort by pitch (low to high) and offset
			cluster.sort((a, b) => a.midi - b.midi);
			const strumTime = strumTimeMs / 1000; // convert to seconds
			for (let k = 0; k < cluster.length; k++) {
				result.push({
					...cluster[k],
					time: cluster[k].time + k * strumTime
				});
			}
		} else {
			result.push(cluster[0]);
		}
		i = j;
	}

	return result;
}

/**
 * Apply velocity curve transformation.
 * velocityCurve < 1: softer response (compress dynamics)
 * velocityCurve = 1: linear (no change)
 * velocityCurve > 1: harder response (expand dynamics)
 */
export function applyVelocityCurve(velocity: number, curve: number): number {
	return Math.pow(velocity, curve);
}

/**
 * Get humanization parameters for a given role.
 */
export function getRoleHumanization(role: TrackRole, profile: StyleProfile): {
	applyStrum: boolean;
	velocityCurve: number;
} {
	const instrProfile = profile.instruments[role];
	return {
		applyStrum: role === 'clean_guitar' || role === 'distorted_guitar',
		velocityCurve: instrProfile?.velocityCurve ?? 1.0
	};
}
