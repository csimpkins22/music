/**
 * Grandaddy style profile.
 *
 * Models the sonic characteristics of Grandaddy's music:
 * - Roland Juno-60 shimmer pads with chorus
 * - DOD FX55B fuzzy-but-notey distortion through Fender Jazzmaster
 * - Piano arpeggios drenched in reverb ("bottom of a well")
 * - Tape warmth, analog wobble, lo-fi character
 * - Droning organ beds
 * - Sparse drum patterns
 * - Heavy reverb on everything
 * - Dynamic contrasts: quiet hymnal → distorted walls
 */

import type { StyleProfile } from '../engine/types';

export const grandaddyProfile: StyleProfile = {
	name: 'Grandaddy',
	genre: 'Space-Age Slacker Rock / Indie Electronic',
	era: '1997-2024',

	instruments: {
		piano: {
			synthType: 'sampler',
			synthConfig: {
				// Will be loaded with Salamander samples at runtime
				// Fallback: triangle-based PolySynth
				fallback: {
					oscillator: { type: 'triangle' },
					envelope: { attack: 0.005, decay: 1.2, sustain: 0.3, release: 1.5 }
				}
			},
			maxPolyphony: 12,
			insertEffects: [
				{
					type: 'Reverb',
					options: { decay: 3.5, wet: 0.45 } // "bottom of a well"
				}
			],
			sendLevels: { reverb: 0.3, delay: 0.1 },
			volume: -6,
			pan: -0.1,
			velocityCurve: 1.0
		},

		synth_pad: {
			synthType: 'poly',
			synthConfig: {
				oscillator: { type: 'sawtooth' },
				envelope: { attack: 0.4, decay: 0.8, sustain: 0.7, release: 2.0 },
				detune: 8 // slight detune for Juno warmth
			},
			maxPolyphony: 8,
			insertEffects: [
				{
					type: 'Chorus',
					options: { frequency: 0.5, delayTime: 3.5, depth: 0.7, wet: 0.6 }
				},
				{
					type: 'Reverb',
					options: { decay: 2.5, wet: 0.35 }
				}
			],
			sendLevels: { reverb: 0.4, delay: 0.15 },
			volume: -10,
			pan: 0.15,
			velocityCurve: 0.8
		},

		synth_lead: {
			synthType: 'poly',
			synthConfig: {
				oscillator: { type: 'sawtooth' },
				envelope: { attack: 0.02, decay: 0.3, sustain: 0.5, release: 0.8 },
				detune: 4
			},
			maxPolyphony: 6,
			insertEffects: [
				{
					type: 'AutoFilter',
					options: { frequency: 0.3, baseFrequency: 400, octaves: 2.5, wet: 0.3 }
				},
				{
					type: 'PingPongDelay',
					options: { delayTime: '8n', feedback: 0.25, wet: 0.2 }
				}
			],
			sendLevels: { reverb: 0.35, delay: 0.2 },
			volume: -8,
			pan: 0.25,
			velocityCurve: 1.0
		},

		clean_guitar: {
			synthType: 'fm',
			synthConfig: {
				harmonicity: 1.5,
				modulationIndex: 2,
				oscillator: { type: 'triangle' },
				modulation: { type: 'sine' },
				envelope: { attack: 0.01, decay: 0.6, sustain: 0.2, release: 1.2 },
				modulationEnvelope: { attack: 0.01, decay: 0.3, sustain: 0.1, release: 0.5 }
			},
			maxPolyphony: 6,
			insertEffects: [
				{
					type: 'Chorus',
					options: { frequency: 1.2, delayTime: 2.5, depth: 0.3, wet: 0.25 }
				},
				{
					type: 'Reverb',
					options: { decay: 1.8, wet: 0.3 }
				}
			],
			sendLevels: { reverb: 0.25, delay: 0.15 },
			volume: -9,
			pan: -0.3,
			velocityCurve: 1.0
		},

		distorted_guitar: {
			synthType: 'fm',
			synthConfig: {
				harmonicity: 2.5,
				modulationIndex: 8,
				oscillator: { type: 'sawtooth' },
				modulation: { type: 'square' },
				envelope: { attack: 0.01, decay: 0.4, sustain: 0.6, release: 0.8 },
				modulationEnvelope: { attack: 0.01, decay: 0.2, sustain: 0.5, release: 0.4 }
			},
			maxPolyphony: 6,
			insertEffects: [
				{
					type: 'Chebyshev',
					options: { order: 3, wet: 0.7 }
				},
				{
					type: 'EQ3',
					options: { low: -2, mid: 4, high: -3, lowFrequency: 200, highFrequency: 4000 }
				},
				{
					type: 'Reverb',
					options: { decay: 1.2, wet: 0.2 }
				}
			],
			sendLevels: { reverb: 0.15, delay: 0.1 },
			volume: -8,
			pan: 0.35,
			velocityCurve: 1.2
		},

		organ: {
			synthType: 'poly',
			synthConfig: {
				oscillator: { type: 'square' },
				envelope: { attack: 0.01, decay: 0.1, sustain: 0.9, release: 0.3 },
				detune: 6
			},
			maxPolyphony: 6,
			insertEffects: [
				{
					type: 'Vibrato',
					options: { frequency: 5, depth: 0.1, wet: 0.4 }
				},
				{
					type: 'Reverb',
					options: { decay: 2.0, wet: 0.3 }
				}
			],
			sendLevels: { reverb: 0.35, delay: 0.1 },
			volume: -14,
			pan: -0.2,
			velocityCurve: 0.7
		},

		bass: {
			synthType: 'mono',
			synthConfig: {
				oscillator: { type: 'triangle' },
				envelope: { attack: 0.02, decay: 0.3, sustain: 0.6, release: 0.4 },
				filterEnvelope: {
					attack: 0.01,
					decay: 0.2,
					sustain: 0.3,
					release: 0.3,
					baseFrequency: 150,
					octaves: 2.5
				}
			},
			insertEffects: [
				{
					type: 'Compressor',
					options: { threshold: -20, ratio: 4, attack: 0.01, release: 0.1 }
				}
			],
			sendLevels: { reverb: 0.08, delay: 0.0 },
			volume: -6,
			pan: 0,
			velocityCurve: 0.9
		},

		strings: {
			synthType: 'poly',
			synthConfig: {
				oscillator: { type: 'sawtooth' },
				envelope: { attack: 0.8, decay: 0.5, sustain: 0.7, release: 2.0 },
				detune: 5
			},
			maxPolyphony: 8,
			insertEffects: [
				{
					type: 'Chorus',
					options: { frequency: 0.8, delayTime: 3, depth: 0.4, wet: 0.3 }
				},
				{
					type: 'Reverb',
					options: { decay: 3.0, wet: 0.4 }
				}
			],
			sendLevels: { reverb: 0.4, delay: 0.1 },
			volume: -12,
			pan: 0,
			velocityCurve: 0.8
		},

		vocal_melody: {
			synthType: 'poly',
			synthConfig: {
				oscillator: { type: 'sine' },
				envelope: { attack: 0.05, decay: 0.2, sustain: 0.6, release: 0.6 },
				detune: 3
			},
			maxPolyphony: 4,
			insertEffects: [
				{
					type: 'Vibrato',
					options: { frequency: 5, depth: 0.15, wet: 0.35 }
				},
				{
					type: 'Reverb',
					options: { decay: 2.0, wet: 0.35 }
				},
				{
					type: 'PingPongDelay',
					options: { delayTime: '8n.', feedback: 0.2, wet: 0.15 }
				}
			],
			sendLevels: { reverb: 0.3, delay: 0.2 },
			volume: -5,
			pan: 0,
			velocityCurve: 1.0
		},

		drums: {
			synthType: 'drum_kit',
			synthConfig: {
				// Individual drum voices configured in instrument-designer.ts
				kick: { pitchDecay: 0.05, octaves: 6, oscillator: { type: 'sine' }, envelope: { attack: 0.001, decay: 0.3, sustain: 0, release: 0.3 } },
				snare: { noise: { type: 'white' }, envelope: { attack: 0.001, decay: 0.2, sustain: 0, release: 0.2 } },
				hihat: { frequency: 400, envelope: { attack: 0.001, decay: 0.1, sustain: 0, release: 0.1 }, harmonicity: 5.1 }
			},
			insertEffects: [
				{
					type: 'Compressor',
					options: { threshold: -15, ratio: 3, attack: 0.005, release: 0.05 }
				},
				{
					type: 'Reverb',
					options: { decay: 0.6, wet: 0.15 }
				}
			],
			sendLevels: { reverb: 0.12, delay: 0.05 },
			volume: -7,
			pan: 0,
			velocityCurve: 1.0
		}
	},

	effects: {
		reverbBus: {
			type: 'Reverb',
			options: { decay: 2.8, wet: 1.0 } // 100% wet on bus (parallel send)
		},
		delayBus: {
			type: 'FeedbackDelay',
			options: { delayTime: '8n.', feedback: 0.3, wet: 1.0 }
		},
		masterBus: [
			{
				type: 'Compressor',
				options: { threshold: -14, ratio: 2.5, attack: 0.02, release: 0.15 }
			},
			{
				type: 'EQ3',
				options: { low: 1, mid: 0, high: -1, lowFrequency: 250, highFrequency: 5000 }
			}
		]
	},

	production: {
		tapeWarmth: 0.3,
		analogDrift: 0.15,
		lofiAmount: 0.1,
		reverbDrench: 0.6
	},

	humanization: {
		timingLooseness: 0.3,
		velocityVariation: 0.25,
		swingAmount: 0.15
	}
};
