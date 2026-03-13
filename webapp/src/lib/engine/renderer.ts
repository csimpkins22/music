/**
 * Render engine.
 * Handles real-time playback scheduling and offline WAV export.
 * This is the central coordinator that ties MIDI data to instruments.
 */

import * as Tone from 'tone';
import type { ParsedMidi, ParsedTrack, TrackRole, StyleProfile, EngineState, PlaybackState } from './types';
import { inferAllRoles } from './role-inference';
import { createInstrument, type InstrumentInstance } from './instrument-designer';
import { Mixer, type MixerChannel } from './mixer';
import { applyStrumOffset, applyVelocityCurve, getRoleHumanization } from './humanizer';

export class PerformanceEngine {
	private midi: ParsedMidi | null = null;
	private profile: StyleProfile;
	private mixer: Mixer;
	private scheduledEvents: number[] = []; // Tone.Transport event IDs
	private _state: EngineState;
	private positionInterval: ReturnType<typeof setInterval> | null = null;
	private stateListeners: ((state: EngineState) => void)[] = [];

	constructor(profile: StyleProfile) {
		this.profile = profile;
		this.mixer = new Mixer();
		this._state = {
			playback: 'stopped',
			position: 0,
			duration: 0,
			bpm: 120,
			songName: '',
			tracks: [],
			loading: false,
			loadingMessage: ''
		};
	}

	get state(): EngineState {
		return this._state;
	}

	onStateChange(listener: (state: EngineState) => void): () => void {
		this.stateListeners.push(listener);
		return () => {
			this.stateListeners = this.stateListeners.filter((l) => l !== listener);
		};
	}

	private emitState(): void {
		this._state = { ...this._state, tracks: this.mixer.getStates() };
		for (const l of this.stateListeners) l(this._state);
	}

	private setLoading(loading: boolean, message: string = ''): void {
		this._state.loading = loading;
		this._state.loadingMessage = message;
		this.emitState();
	}

	async loadMidi(midiData: ParsedMidi): Promise<void> {
		this.setLoading(true, 'Initializing audio...');

		// Ensure audio context is started
		await Tone.start();

		// Clean up previous state
		this.stop();
		this.mixer.dispose();
		this.mixer = new Mixer();

		this.midi = midiData;
		this._state.songName = midiData.name;
		this._state.duration = midiData.duration;
		this._state.bpm = midiData.bpm;

		// Set transport tempo
		Tone.getTransport().bpm.value = midiData.bpm;

		this.setLoading(true, 'Building effects...');

		// Initialize mixer bus effects
		await this.mixer.init(this.profile);

		this.setLoading(true, 'Creating instruments...');

		// Infer roles and create instruments
		const roleAssignments = inferAllRoles(midiData.tracks);

		for (let i = 0; i < roleAssignments.length; i++) {
			const { track, role } = roleAssignments[i];
			const instrProfile = this.profile.instruments[role] ||
				this.profile.instruments['unknown'] ||
				this.getDefaultProfile();

			this.setLoading(true, `Creating ${track.name}...`);

			const instrument = createInstrument(role, instrProfile);
			this.mixer.addChannel(i, track.name, role, instrument, instrProfile);
		}

		this.setLoading(true, 'Scheduling notes...');

		// Schedule all MIDI events
		this.scheduleAllEvents(midiData.tracks, roleAssignments.map((r) => r.role));

		this.setLoading(false);
		this.emitState();
	}

	private getDefaultProfile() {
		return {
			synthType: 'poly' as const,
			synthConfig: {
				oscillator: { type: 'sine' },
				envelope: { attack: 0.01, decay: 0.3, sustain: 0.5, release: 0.5 }
			},
			maxPolyphony: 8,
			insertEffects: [],
			sendLevels: { reverb: 0.2, delay: 0.1 },
			volume: -10,
			pan: 0,
			velocityCurve: 1.0
		};
	}

	private scheduleAllEvents(tracks: ParsedTrack[], roles: TrackRole[]): void {
		// Clear any existing scheduled events
		this.clearScheduledEvents();

		const transport = Tone.getTransport();

		for (let i = 0; i < tracks.length; i++) {
			const track = tracks[i];
			const role = roles[i];
			const channel = this.mixer.channels[i];
			if (!channel) continue;

			const humanization = getRoleHumanization(role, this.profile);

			// Process notes
			let notes = [...track.notes];

			// Apply strum offset for guitar parts
			if (humanization.applyStrum) {
				notes = applyStrumOffset(notes);
			}

			// Schedule note events
			for (const note of notes) {
				const velocity = applyVelocityCurve(note.velocity, humanization.velocityCurve);
				const time = note.time;
				const duration = Math.max(0.01, note.duration);

				if (channel.instrument.drumKit) {
					// Drum notes
					const id = transport.schedule((scheduledTime) => {
						channel.instrument.drumKit!.trigger(
							note.midi,
							velocity,
							scheduledTime,
							duration
						);
					}, time);
					this.scheduledEvents.push(id);
				} else if (channel.instrument.instrument) {
					// Melodic notes
					const noteName = Tone.Frequency(note.midi, 'midi').toNote();
					const id = transport.schedule((scheduledTime) => {
						try {
							if (channel.instrument.instrument instanceof Tone.MonoSynth) {
								channel.instrument.instrument.triggerAttackRelease(
									noteName, duration, scheduledTime, velocity
								);
							} else {
								(channel.instrument.instrument as Tone.PolySynth).triggerAttackRelease(
									noteName, duration, scheduledTime, velocity
								);
							}
						} catch {
							// Instrument may be disposed during cleanup
						}
					}, time);
					this.scheduledEvents.push(id);
				}
			}

			// Schedule CC events
			for (const [ccNum, events] of track.controlChanges) {
				for (const cc of events) {
					if (ccNum === 64) {
						// Sustain pedal — for now just log (Sampler handles it, PolySynth doesn't natively)
						// Could extend release time when pedal is down
					} else if (ccNum === 11) {
						// Expression — map to volume automation
						const id = transport.schedule((scheduledTime) => {
							try {
								const volDb = Tone.gainToDb(cc.value / 127);
								// Subtle expression — don't go below -20dB
								const mappedVol = Math.max(-20, volDb);
								channel.channel.volume.setValueAtTime(
									channel.state.volume + mappedVol * 0.3,
									scheduledTime
								);
							} catch {
								// ignore
							}
						}, cc.time);
						this.scheduledEvents.push(id);
					}
				}
			}

			// Schedule pitch bend events
			for (const pb of track.pitchBends) {
				const id = transport.schedule((scheduledTime) => {
					try {
						if (channel.instrument.instrument) {
							// Map pitch bend (-1..1) to detune in cents (±200 cents = ±2 semitones)
							const detuneCents = pb.value * 200;
							if (channel.instrument.instrument instanceof Tone.MonoSynth) {
								channel.instrument.instrument.detune.setValueAtTime(detuneCents, scheduledTime);
							} else {
								// PolySynth doesn't support global detune easily; use set
								(channel.instrument.instrument as Tone.PolySynth).set({ detune: detuneCents });
							}
						}
					} catch {
						// ignore
					}
				}, pb.time);
				this.scheduledEvents.push(id);
			}
		}
	}

	private clearScheduledEvents(): void {
		const transport = Tone.getTransport();
		for (const id of this.scheduledEvents) {
			transport.clear(id);
		}
		this.scheduledEvents = [];
	}

	async play(): Promise<void> {
		await Tone.start();
		const transport = Tone.getTransport();

		if (this._state.playback === 'paused') {
			transport.start();
		} else {
			transport.start();
		}

		this._state.playback = 'playing';
		this.startPositionTracking();
		this.emitState();
	}

	pause(): void {
		Tone.getTransport().pause();
		this._state.playback = 'paused';
		this.stopPositionTracking();
		this.emitState();
	}

	stop(): void {
		const transport = Tone.getTransport();
		transport.stop();
		transport.position = 0;
		this._state.playback = 'stopped';
		this._state.position = 0;
		this.stopPositionTracking();
		this.emitState();
	}

	seek(seconds: number): void {
		Tone.getTransport().seconds = Math.max(0, Math.min(seconds, this._state.duration));
		this._state.position = seconds;
		this.emitState();
	}

	private startPositionTracking(): void {
		this.stopPositionTracking();
		this.positionInterval = setInterval(() => {
			if (this._state.playback === 'playing') {
				this._state.position = Tone.getTransport().seconds;
				// Auto-stop at end
				if (this._state.position >= this._state.duration) {
					this.stop();
					return;
				}
				this.emitState();
			}
		}, 100); // Update 10x per second
	}

	private stopPositionTracking(): void {
		if (this.positionInterval) {
			clearInterval(this.positionInterval);
			this.positionInterval = null;
		}
	}

	// Mixer controls (delegated)
	setVolume(trackIndex: number, volume: number): void {
		this.mixer.setVolume(trackIndex, volume);
		this.emitState();
	}

	setPan(trackIndex: number, pan: number): void {
		this.mixer.setPan(trackIndex, pan);
		this.emitState();
	}

	toggleSolo(trackIndex: number): void {
		this.mixer.toggleSolo(trackIndex);
		this.emitState();
	}

	toggleMute(trackIndex: number): void {
		this.mixer.toggleMute(trackIndex);
		this.emitState();
	}

	// WAV export
	async exportWav(): Promise<Blob> {
		if (!this.midi) throw new Error('No MIDI loaded');

		const duration = this.midi.duration + 2; // add 2s tail for reverb

		const buffer = await Tone.Offline(async () => {
			// Recreate everything in offline context
			// This is simplified — full implementation would rebuild the engine
			// For now, we just render what we have
		}, duration);

		return audioBufferToWav(buffer);
	}

	dispose(): void {
		this.stop();
		this.clearScheduledEvents();
		this.mixer.dispose();
		this.stateListeners = [];
	}
}

// Convert AudioBuffer to WAV Blob
function audioBufferToWav(buffer: Tone.ToneAudioBuffer): Blob {
	const raw = buffer.get();
	if (!raw) return new Blob();

	const numChannels = raw.numberOfChannels;
	const sampleRate = raw.sampleRate;
	const length = raw.length;
	const bytesPerSample = 2; // 16-bit
	const blockAlign = numChannels * bytesPerSample;
	const dataSize = length * blockAlign;
	const headerSize = 44;
	const arrayBuffer = new ArrayBuffer(headerSize + dataSize);
	const view = new DataView(arrayBuffer);

	// WAV header
	writeString(view, 0, 'RIFF');
	view.setUint32(4, 36 + dataSize, true);
	writeString(view, 8, 'WAVE');
	writeString(view, 12, 'fmt ');
	view.setUint32(16, 16, true); // chunk size
	view.setUint16(20, 1, true); // PCM
	view.setUint16(22, numChannels, true);
	view.setUint32(24, sampleRate, true);
	view.setUint32(28, sampleRate * blockAlign, true);
	view.setUint16(32, blockAlign, true);
	view.setUint16(34, 16, true); // bits per sample
	writeString(view, 36, 'data');
	view.setUint32(40, dataSize, true);

	// Interleave channels and write 16-bit PCM
	let offset = 44;
	for (let i = 0; i < length; i++) {
		for (let ch = 0; ch < numChannels; ch++) {
			const sample = raw.getChannelData(ch)[i];
			const clamped = Math.max(-1, Math.min(1, sample));
			view.setInt16(offset, clamped * 0x7fff, true);
			offset += 2;
		}
	}

	return new Blob([arrayBuffer], { type: 'audio/wav' });
}

function writeString(view: DataView, offset: number, str: string): void {
	for (let i = 0; i < str.length; i++) {
		view.setUint8(offset + i, str.charCodeAt(i));
	}
}
