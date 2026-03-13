/**
 * Effects chain builder.
 * Creates per-track insert effects, bus sends, and master bus processing
 * based on the style profile.
 */

import * as Tone from 'tone';
import type { EffectConfig } from './types';

export interface EffectChain {
	nodes: Tone.ToneAudioNode[];
	input: Tone.ToneAudioNode;
	output: Tone.ToneAudioNode;
	dispose: () => void;
}

export interface BusEffects {
	reverbBus: Tone.Reverb;
	reverbGain: Tone.Gain;
	delayBus: Tone.FeedbackDelay;
	delayGain: Tone.Gain;
	masterChain: Tone.ToneAudioNode[];
	masterGain: Tone.Gain;
	dispose: () => void;
}

function createEffect(config: EffectConfig): Tone.ToneAudioNode {
	const opts = config.options as Record<string, unknown>;

	switch (config.type) {
		case 'Reverb':
			return new Tone.Reverb({
				decay: (opts.decay as number) || 2,
				wet: (opts.wet as number) ?? 0.3
			});
		case 'Chorus':
			return new Tone.Chorus({
				frequency: (opts.frequency as number) || 1,
				delayTime: (opts.delayTime as number) || 3.5,
				depth: (opts.depth as number) || 0.5,
				wet: (opts.wet as number) ?? 0.5
			}).start();
		case 'Vibrato':
			return new Tone.Vibrato({
				frequency: (opts.frequency as number) || 5,
				depth: (opts.depth as number) || 0.1,
				wet: (opts.wet as number) ?? 0.3
			});
		case 'PingPongDelay':
			return new Tone.PingPongDelay({
				delayTime: (opts.delayTime as Tone.Unit.Time) || '8n',
				feedback: (opts.feedback as number) || 0.2,
				wet: (opts.wet as number) ?? 0.2
			});
		case 'FeedbackDelay':
			return new Tone.FeedbackDelay({
				delayTime: (opts.delayTime as Tone.Unit.Time) || '8n.',
				feedback: (opts.feedback as number) || 0.3,
				wet: (opts.wet as number) ?? 0.3
			});
		case 'Chebyshev':
			return new Tone.Chebyshev({
				order: (opts.order as number) || 3,
				wet: (opts.wet as number) ?? 0.5
			});
		case 'Compressor':
			return new Tone.Compressor({
				threshold: (opts.threshold as number) || -20,
				ratio: (opts.ratio as number) || 4,
				attack: (opts.attack as number) || 0.01,
				release: (opts.release as number) || 0.1
			});
		case 'EQ3':
			return new Tone.EQ3({
				low: (opts.low as number) || 0,
				mid: (opts.mid as number) || 0,
				high: (opts.high as number) || 0,
				lowFrequency: (opts.lowFrequency as number) || 250,
				highFrequency: (opts.highFrequency as number) || 5000
			});
		case 'AutoFilter':
			return new Tone.AutoFilter({
				frequency: (opts.frequency as number) || 0.3,
				baseFrequency: (opts.baseFrequency as number) || 400,
				octaves: (opts.octaves as number) || 2.5,
				wet: (opts.wet as number) ?? 0.3
			}).start();
		case 'Distortion':
			return new Tone.Distortion({
				distortion: (opts.distortion as number) || 0.5,
				wet: (opts.wet as number) ?? 0.5
			});
		default:
			// Pass-through gain node for unknown effects
			console.warn(`Unknown effect type: ${config.type}`);
			return new Tone.Gain(1);
	}
}

export function buildInsertChain(effectConfigs: EffectConfig[]): EffectChain {
	if (effectConfigs.length === 0) {
		const gain = new Tone.Gain(1);
		return { nodes: [gain], input: gain, output: gain, dispose: () => gain.dispose() };
	}

	const nodes = effectConfigs.map(createEffect);

	// Chain them together
	for (let i = 0; i < nodes.length - 1; i++) {
		nodes[i].connect(nodes[i + 1]);
	}

	return {
		nodes,
		input: nodes[0],
		output: nodes[nodes.length - 1],
		dispose: () => nodes.forEach((n) => n.dispose())
	};
}

export async function buildBusEffects(
	reverbConfig: EffectConfig,
	delayConfig: EffectConfig,
	masterConfigs: EffectConfig[]
): Promise<BusEffects> {
	// Reverb bus
	const reverbBus = new Tone.Reverb({
		decay: (reverbConfig.options.decay as number) || 2.8,
		wet: 1.0 // 100% wet on send bus
	});
	await reverbBus.generate(); // Pre-generate reverb IR
	const reverbGain = new Tone.Gain(0.5);
	reverbGain.connect(reverbBus);
	reverbBus.toDestination();

	// Delay bus
	const delayBus = new Tone.FeedbackDelay({
		delayTime: (delayConfig.options.delayTime as Tone.Unit.Time) || '8n.',
		feedback: (delayConfig.options.feedback as number) || 0.3,
		wet: 1.0
	});
	const delayGain = new Tone.Gain(0.3);
	delayGain.connect(delayBus);
	delayBus.toDestination();

	// Master bus chain
	const masterGain = new Tone.Gain(1);
	const masterChain = masterConfigs.map(createEffect);

	if (masterChain.length > 0) {
		masterGain.connect(masterChain[0]);
		for (let i = 0; i < masterChain.length - 1; i++) {
			masterChain[i].connect(masterChain[i + 1]);
		}
		masterChain[masterChain.length - 1].toDestination();
	} else {
		masterGain.toDestination();
	}

	return {
		reverbBus,
		reverbGain,
		delayBus,
		delayGain,
		masterChain,
		masterGain,
		dispose: () => {
			reverbBus.dispose();
			reverbGain.dispose();
			delayBus.dispose();
			delayGain.dispose();
			masterChain.forEach((n) => n.dispose());
			masterGain.dispose();
		}
	};
}
