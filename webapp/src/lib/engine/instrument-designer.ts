/**
 * Instrument designer.
 * Creates and configures Tone.js instruments based on track role and style profile.
 */

import * as Tone from 'tone';
import type { TrackRole, InstrumentProfile } from './types';

// Standard GM drum map
const DRUM_MAP: Record<number, string> = {
	35: 'kick', 36: 'kick',
	37: 'rimshot', 38: 'snare', 40: 'snare',
	39: 'clap',
	41: 'tom_low', 43: 'tom_low', 45: 'tom_low',
	47: 'tom_mid', 48: 'tom_mid',
	42: 'hihat_closed', 44: 'hihat_closed',
	46: 'hihat_open',
	49: 'crash', 57: 'crash',
	51: 'ride', 53: 'ride', 59: 'ride'
};

export interface InstrumentInstance {
	instrument: Tone.PolySynth | Tone.MonoSynth | Tone.Sampler | null;
	drumKit: DrumKit | null;
	role: TrackRole;
	dispose: () => void;
}

interface DrumVoice {
	synth: Tone.MembraneSynth | Tone.NoiseSynth | Tone.MetalSynth;
}

export interface DrumKit {
	voices: Map<string, DrumVoice>;
	trigger: (note: number, velocity: number, time: number, duration: number) => void;
	output: Tone.Gain;
	dispose: () => void;
}

function createDrumKit(): DrumKit {
	const output = new Tone.Gain(1);
	const voices = new Map<string, DrumVoice>();

	const kick = new Tone.MembraneSynth({
		pitchDecay: 0.05, octaves: 6,
		oscillator: { type: 'sine' },
		envelope: { attack: 0.001, decay: 0.3, sustain: 0, release: 0.3 }
	}).connect(output);
	voices.set('kick', { synth: kick });

	const snare = new Tone.NoiseSynth({
		noise: { type: 'white' },
		envelope: { attack: 0.001, decay: 0.2, sustain: 0, release: 0.15 }
	}).connect(output);
	voices.set('snare', { synth: snare });

	const rimshot = new Tone.NoiseSynth({
		noise: { type: 'pink' },
		envelope: { attack: 0.001, decay: 0.08, sustain: 0, release: 0.05 }
	}).connect(output);
	voices.set('rimshot', { synth: rimshot });

	const clap = new Tone.NoiseSynth({
		noise: { type: 'white' },
		envelope: { attack: 0.001, decay: 0.15, sustain: 0, release: 0.1 }
	}).connect(output);
	voices.set('clap', { synth: clap });

	const hhClosed = new Tone.MetalSynth({
		envelope: { attack: 0.001, decay: 0.08, release: 0.05 },
		harmonicity: 5.1, modulationIndex: 20, resonance: 4000, octaves: 1.5
	}).connect(output);
	voices.set('hihat_closed', { synth: hhClosed });

	const hhOpen = new Tone.MetalSynth({
		envelope: { attack: 0.001, decay: 0.3, release: 0.2 },
		harmonicity: 5.1, modulationIndex: 20, resonance: 4000, octaves: 1.5
	}).connect(output);
	voices.set('hihat_open', { synth: hhOpen });

	const crash = new Tone.MetalSynth({
		envelope: { attack: 0.001, decay: 1.0, release: 0.8 },
		harmonicity: 5.1, modulationIndex: 30, resonance: 3500, octaves: 1.5
	}).connect(output);
	voices.set('crash', { synth: crash });

	const ride = new Tone.MetalSynth({
		envelope: { attack: 0.001, decay: 0.5, release: 0.3 },
		harmonicity: 5.1, modulationIndex: 15, resonance: 5000, octaves: 1.5
	}).connect(output);
	voices.set('ride', { synth: ride });

	const tomLow = new Tone.MembraneSynth({
		pitchDecay: 0.03, octaves: 4,
		oscillator: { type: 'sine' },
		envelope: { attack: 0.001, decay: 0.25, sustain: 0, release: 0.2 }
	}).connect(output);
	voices.set('tom_low', { synth: tomLow });

	const tomMid = new Tone.MembraneSynth({
		pitchDecay: 0.03, octaves: 4,
		oscillator: { type: 'sine' },
		envelope: { attack: 0.001, decay: 0.2, sustain: 0, release: 0.15 }
	}).connect(output);
	voices.set('tom_mid', { synth: tomMid });

	function trigger(note: number, velocity: number, time: number, duration: number) {
		const voiceName = DRUM_MAP[note];
		if (!voiceName) return;
		const voice = voices.get(voiceName);
		if (!voice) return;

		const vel = Math.max(0.01, Math.min(1, velocity));

		if (voice.synth instanceof Tone.MembraneSynth) {
			const pitchMap: Record<string, string> = { kick: 'C1', tom_low: 'A1', tom_mid: 'D2' };
			voice.synth.triggerAttackRelease(pitchMap[voiceName] || 'C1', Math.min(duration, 0.5), time, vel);
		} else if (voice.synth instanceof Tone.NoiseSynth) {
			voice.synth.triggerAttackRelease(Math.min(duration, 0.3), time, vel);
		} else if (voice.synth instanceof Tone.MetalSynth) {
			voice.synth.triggerAttackRelease(Math.min(duration, 0.5), time, vel * 0.3);
		}
	}

	return {
		voices, trigger, output,
		dispose: () => { voices.forEach((v) => v.synth.dispose()); output.dispose(); }
	};
}

export function createInstrument(role: TrackRole, profile: InstrumentProfile): InstrumentInstance {
	if (role === 'drums' || profile.synthType === 'drum_kit') {
		const kit = createDrumKit();
		return { instrument: null, drumKit: kit, role, dispose: () => kit.dispose() };
	}

	// Use 'any' for config to avoid Tone.js strict type gymnastics
	// eslint-disable-next-line @typescript-eslint/no-explicit-any
	const config = profile.synthConfig as any;
	let instrument: Tone.PolySynth | Tone.MonoSynth;

	if (profile.synthType === 'mono') {
		instrument = new Tone.MonoSynth({
			oscillator: config.oscillator || { type: 'triangle' },
			envelope: config.envelope || { attack: 0.01, decay: 0.3, sustain: 0.5, release: 0.5 },
			filterEnvelope: config.filterEnvelope || undefined
		});
	} else if (profile.synthType === 'fm') {
		const synth = new Tone.PolySynth(Tone.FMSynth);
		synth.maxPolyphony = profile.maxPolyphony || 6;
		synth.set({
			harmonicity: config.harmonicity || 1,
			modulationIndex: config.modulationIndex || 3,
		} as any); // eslint-disable-line @typescript-eslint/no-explicit-any
		instrument = synth;
	} else if (profile.synthType === 'sampler') {
		const fallback = config.fallback || {};
		const synth = new Tone.PolySynth(Tone.Synth);
		synth.maxPolyphony = profile.maxPolyphony || 12;
		synth.set({
			oscillator: fallback.oscillator || { type: 'triangle' },
			envelope: fallback.envelope || { attack: 0.01, decay: 0.5, sustain: 0.3, release: 1.0 }
		} as any); // eslint-disable-line @typescript-eslint/no-explicit-any
		instrument = synth;
	} else {
		const synth = new Tone.PolySynth(Tone.Synth);
		synth.maxPolyphony = profile.maxPolyphony || 8;
		synth.set({
			oscillator: config.oscillator || { type: 'sawtooth' },
			envelope: config.envelope || { attack: 0.01, decay: 0.3, sustain: 0.5, release: 0.5 }
		} as any); // eslint-disable-line @typescript-eslint/no-explicit-any
		if (config.detune) {
			synth.set({ detune: config.detune } as any); // eslint-disable-line @typescript-eslint/no-explicit-any
		}
		instrument = synth;
	}

	return { instrument, drumKit: null, role, dispose: () => instrument.dispose() };
}
