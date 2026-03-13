/**
 * Track role inference.
 * Maps MIDI tracks to musical roles using track names, channels, GM programs, and heuristics.
 */

import type { ParsedTrack, TrackRole, RoleAssignment } from './types';

// Name patterns for each role (checked in order)
const NAME_PATTERNS: [RegExp, TrackRole][] = [
	[/drum/i, 'drums'],
	[/percussion/i, 'drums'],
	[/kick|snare|hi.?hat|cymbal/i, 'drums'],
	[/bass\b/i, 'bass'],
	[/piano|grand|keys/i, 'piano'],
	[/organ|drone/i, 'organ'],
	[/pad|warm|juno/i, 'synth_pad'],
	[/lead|arpeggio|synth.*lead/i, 'synth_lead'],
	[/synth/i, 'synth_lead'], // generic synth → lead
	[/distort|fuzz|overdriv|jazzmaster/i, 'distorted_guitar'],
	[/clean.*guitar|guitar.*clean|electric.*guitar/i, 'clean_guitar'],
	[/guitar/i, 'clean_guitar'],
	[/string|ensemble|orchestr/i, 'strings'],
	[/vocal|voice|melody.*voice|voice.*melody/i, 'vocal_melody'],
	[/vocal.*melody|melody/i, 'vocal_melody'],
];

// GM program number ranges to roles
const PROGRAM_ROLES: [number, number, TrackRole][] = [
	[0, 7, 'piano'],         // Piano family
	[16, 23, 'organ'],       // Organ family
	[24, 31, 'clean_guitar'],// Guitar family
	[32, 39, 'bass'],        // Bass family
	[40, 47, 'strings'],     // Strings
	[48, 55, 'strings'],     // Ensemble
	[80, 87, 'synth_lead'],  // Synth Lead
	[88, 95, 'synth_pad'],   // Synth Pad
];

function roleFromName(name: string): TrackRole | null {
	for (const [pattern, role] of NAME_PATTERNS) {
		if (pattern.test(name)) return role;
	}
	return null;
}

function roleFromProgram(program: number | null): TrackRole | null {
	if (program === null) return null;
	for (const [lo, hi, role] of PROGRAM_ROLES) {
		if (program >= lo && program <= hi) return role;
	}
	// Distorted guitar (program 29-31)
	if (program >= 29 && program <= 31) return 'distorted_guitar';
	return null;
}

function roleFromHeuristics(track: ParsedTrack): TrackRole {
	const { noteRange, maxPolyphony, noteDensity } = track;
	const midpoint = (noteRange.min + noteRange.max) / 2;

	// Very low register → bass
	if (noteRange.max < 60 && midpoint < 48) return 'bass';

	// Channel 9 → drums (already handled but safety)
	if (track.isPercussion) return 'drums';

	// High density, moderate poly → arpeggio/lead
	if (noteDensity > 4 && maxPolyphony <= 2) return 'synth_lead';

	// Low density, high poly → pad
	if (noteDensity < 1 && maxPolyphony >= 3) return 'synth_pad';

	// Moderate everything → could be many things
	if (maxPolyphony >= 3 && midpoint > 55 && midpoint < 75) return 'piano';

	// High register monophonic → vocal/lead
	if (maxPolyphony <= 2 && midpoint > 70) return 'vocal_melody';

	return 'unknown';
}

export function inferRole(track: ParsedTrack): RoleAssignment {
	// 1. Percussion channel
	if (track.isPercussion || track.channel === 9) {
		return { track, role: 'drums', confidence: 1.0 };
	}

	// 2. Track name matching (highest confidence)
	const nameRole = roleFromName(track.name);
	if (nameRole) {
		return { track, role: nameRole, confidence: 0.95 };
	}

	// 3. GM program matching
	const programRole = roleFromProgram(track.program);
	if (programRole) {
		return { track, role: programRole, confidence: 0.8 };
	}

	// 4. Heuristic analysis
	const heuristicRole = roleFromHeuristics(track);
	return {
		track,
		role: heuristicRole,
		confidence: heuristicRole === 'unknown' ? 0.1 : 0.5
	};
}

export function inferAllRoles(tracks: ParsedTrack[]): RoleAssignment[] {
	return tracks.map(inferRole);
}

export const ROLE_LABELS: Record<TrackRole, string> = {
	piano: 'Piano',
	synth_pad: 'Synth Pad',
	synth_lead: 'Synth Lead',
	clean_guitar: 'Clean Guitar',
	distorted_guitar: 'Distorted Guitar',
	organ: 'Organ',
	bass: 'Bass',
	strings: 'Strings',
	vocal_melody: 'Vocal Melody',
	drums: 'Drums',
	unknown: 'Unknown'
};

export const ROLE_COLORS: Record<TrackRole, string> = {
	piano: '#e8d5b7',
	synth_pad: '#7eb8da',
	synth_lead: '#f0a050',
	clean_guitar: '#98d898',
	distorted_guitar: '#e06060',
	organ: '#c4a0d8',
	bass: '#6088c0',
	strings: '#d4b870',
	vocal_melody: '#f0c0d0',
	drums: '#a0a0a0',
	unknown: '#808080'
};
