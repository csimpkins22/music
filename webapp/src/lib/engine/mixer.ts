/**
 * Mix engine.
 * Manages per-track channels (volume, pan, solo, mute),
 * bus routing (reverb/delay sends), and master output.
 */

import * as Tone from 'tone';
import type { TrackRole, InstrumentProfile, MixerChannelState, StyleProfile } from './types';
import type { InstrumentInstance } from './instrument-designer';
import { buildInsertChain, buildBusEffects, type BusEffects, type EffectChain } from './fx-chain-builder';

export interface MixerChannel {
	state: MixerChannelState;
	instrument: InstrumentInstance;
	channel: Tone.Channel;
	insertChain: EffectChain;
	reverbSendGain: Tone.Gain;
	delaySendGain: Tone.Gain;
}

export class Mixer {
	channels: MixerChannel[] = [];
	busEffects: BusEffects | null = null;
	private soloActive = false;

	async init(profile: StyleProfile): Promise<void> {
		// Build bus effects from profile
		this.busEffects = await buildBusEffects(
			profile.effects.reverbBus,
			profile.effects.delayBus,
			profile.effects.masterBus
		);
	}

	addChannel(
		trackIndex: number,
		name: string,
		role: TrackRole,
		instrument: InstrumentInstance,
		profile: InstrumentProfile
	): MixerChannel {
		// Create channel strip (volume + pan)
		const channel = new Tone.Channel({
			volume: profile.volume,
			pan: profile.pan
		});

		// Insert effects chain
		const insertChain = buildInsertChain(profile.insertEffects);

		// Connect: instrument output → insert chain → channel → master bus
		const instrumentOutput = instrument.drumKit
			? instrument.drumKit.output
			: instrument.instrument;

		if (instrumentOutput) {
			instrumentOutput.connect(insertChain.input);
		}
		insertChain.output.connect(channel);

		// Connect channel to master bus
		if (this.busEffects) {
			channel.connect(this.busEffects.masterGain);
		} else {
			channel.toDestination();
		}

		// Reverb send
		const reverbSendGain = new Tone.Gain(profile.sendLevels.reverb);
		channel.connect(reverbSendGain);
		if (this.busEffects) {
			reverbSendGain.connect(this.busEffects.reverbGain);
		}

		// Delay send
		const delaySendGain = new Tone.Gain(profile.sendLevels.delay);
		channel.connect(delaySendGain);
		if (this.busEffects) {
			delaySendGain.connect(this.busEffects.delayGain);
		}

		const state: MixerChannelState = {
			trackIndex,
			role,
			name,
			volume: profile.volume,
			pan: profile.pan,
			solo: false,
			mute: false,
			reverbSend: profile.sendLevels.reverb,
			delaySend: profile.sendLevels.delay
		};

		const mixerChannel: MixerChannel = {
			state,
			instrument,
			channel,
			insertChain,
			reverbSendGain,
			delaySendGain
		};

		this.channels.push(mixerChannel);
		return mixerChannel;
	}

	setVolume(trackIndex: number, volume: number): void {
		const ch = this.channels.find((c) => c.state.trackIndex === trackIndex);
		if (ch) {
			ch.state.volume = volume;
			ch.channel.volume.value = volume;
		}
	}

	setPan(trackIndex: number, pan: number): void {
		const ch = this.channels.find((c) => c.state.trackIndex === trackIndex);
		if (ch) {
			ch.state.pan = pan;
			ch.channel.pan.value = pan;
		}
	}

	toggleSolo(trackIndex: number): void {
		const ch = this.channels.find((c) => c.state.trackIndex === trackIndex);
		if (!ch) return;
		ch.state.solo = !ch.state.solo;
		this.updateSoloMuteState();
	}

	toggleMute(trackIndex: number): void {
		const ch = this.channels.find((c) => c.state.trackIndex === trackIndex);
		if (!ch) return;
		ch.state.mute = !ch.state.mute;
		this.updateSoloMuteState();
	}

	private updateSoloMuteState(): void {
		this.soloActive = this.channels.some((c) => c.state.solo);

		for (const ch of this.channels) {
			if (this.soloActive) {
				// If any track is soloed, mute all non-soloed tracks
				ch.channel.mute = ch.state.mute || !ch.state.solo;
			} else {
				ch.channel.mute = ch.state.mute;
			}
		}
	}

	setReverbSend(trackIndex: number, level: number): void {
		const ch = this.channels.find((c) => c.state.trackIndex === trackIndex);
		if (ch) {
			ch.state.reverbSend = level;
			ch.reverbSendGain.gain.value = level;
		}
	}

	setDelaySend(trackIndex: number, level: number): void {
		const ch = this.channels.find((c) => c.state.trackIndex === trackIndex);
		if (ch) {
			ch.state.delaySend = level;
			ch.delaySendGain.gain.value = level;
		}
	}

	getStates(): MixerChannelState[] {
		return this.channels.map((c) => ({ ...c.state }));
	}

	dispose(): void {
		for (const ch of this.channels) {
			ch.instrument.dispose();
			ch.channel.dispose();
			ch.insertChain.dispose();
			ch.reverbSendGain.dispose();
			ch.delaySendGain.dispose();
		}
		this.channels = [];
		this.busEffects?.dispose();
		this.busEffects = null;
	}
}
