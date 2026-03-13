/**
 * Shared TypeScript types for the MIDI performance engine.
 */

// ============================================================
// MIDI ANALYSIS TYPES
// ============================================================

export interface NoteEvent {
	midi: number;
	name: string;
	velocity: number;
	duration: number; // seconds
	time: number; // seconds (absolute start time)
	ticks: number;
	durationTicks: number;
}

export interface CCEvent {
	number: number;
	value: number;
	time: number; // seconds
	ticks: number;
}

export interface PitchBendEvent {
	value: number; // -1 to 1 (normalized from -8192..8191)
	time: number; // seconds
	ticks: number;
}

export interface ParsedTrack {
	name: string;
	channel: number;
	program: number | null;
	notes: NoteEvent[];
	controlChanges: Map<number, CCEvent[]>;
	pitchBends: PitchBendEvent[];
	// Analysis
	noteRange: { min: number; max: number };
	avgVelocity: number;
	noteDensity: number; // notes per second
	maxPolyphony: number;
	isPercussion: boolean;
	noteCount: number;
}

export interface ParsedMidi {
	name: string;
	bpm: number;
	timeSignature: { numerator: number; denominator: number };
	duration: number; // seconds
	tracks: ParsedTrack[];
}

// ============================================================
// ROLE INFERENCE
// ============================================================

export type TrackRole =
	| 'piano'
	| 'synth_pad'
	| 'synth_lead'
	| 'clean_guitar'
	| 'distorted_guitar'
	| 'organ'
	| 'bass'
	| 'strings'
	| 'vocal_melody'
	| 'drums'
	| 'unknown';

export interface RoleAssignment {
	track: ParsedTrack;
	role: TrackRole;
	confidence: number; // 0-1
}

// ============================================================
// STYLE PROFILE
// ============================================================

export interface EffectConfig {
	type: string; // Tone.js effect class name
	options: Record<string, unknown>;
}

export interface InstrumentProfile {
	synthType: 'poly' | 'fm' | 'mono' | 'sampler' | 'drum_kit';
	synthConfig: Record<string, unknown>;
	maxPolyphony?: number;
	insertEffects: EffectConfig[];
	sendLevels: { reverb: number; delay: number };
	volume: number; // dB
	pan: number; // -1 to 1
	velocityCurve: number; // 0.5=soft, 1=linear, 2=hard
}

export interface StyleProfile {
	name: string;
	genre: string;
	era: string;

	instruments: Partial<Record<TrackRole, InstrumentProfile>>;

	effects: {
		reverbBus: EffectConfig;
		delayBus: EffectConfig;
		masterBus: EffectConfig[];
	};

	production: {
		tapeWarmth: number;
		analogDrift: number;
		lofiAmount: number;
		reverbDrench: number;
	};

	humanization: {
		timingLooseness: number;
		velocityVariation: number;
		swingAmount: number;
	};
}

// ============================================================
// MIXER
// ============================================================

export interface MixerChannelState {
	trackIndex: number;
	role: TrackRole;
	name: string;
	volume: number; // dB
	pan: number; // -1 to 1
	solo: boolean;
	mute: boolean;
	reverbSend: number; // 0-1
	delaySend: number; // 0-1
}

// ============================================================
// PLAYBACK
// ============================================================

export type PlaybackState = 'stopped' | 'playing' | 'paused';

export interface EngineState {
	playback: PlaybackState;
	position: number; // seconds
	duration: number; // seconds
	bpm: number;
	songName: string;
	tracks: MixerChannelState[];
	loading: boolean;
	loadingMessage: string;
}
