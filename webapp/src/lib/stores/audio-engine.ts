/**
 * Audio engine singleton store.
 * Manages the PerformanceEngine instance and exposes reactive state.
 * All Tone.js imports are lazy to avoid SSR crashes.
 */

import { writable, derived } from 'svelte/store';
import { browser } from '$app/environment';
import type { EngineState, ParsedMidi } from '../engine/types';

const defaultState: EngineState = {
	playback: 'stopped',
	position: 0,
	duration: 0,
	bpm: 120,
	songName: '',
	tracks: [],
	loading: false,
	loadingMessage: ''
};

export const engineState = writable<EngineState>(defaultState);
export const parsedMidi = writable<ParsedMidi | null>(null);

// Lazy imports to avoid SSR crash (Tone.js requires browser)
let engine: import('../engine/renderer').PerformanceEngine | null = null;

async function getEngine() {
	if (!engine) {
		const { PerformanceEngine } = await import('../engine/renderer');
		const { grandaddyProfile } = await import('../profiles/grandaddy');
		engine = new PerformanceEngine(grandaddyProfile);
		engine.onStateChange((state) => {
			engineState.set(state);
		});
	}
	return engine;
}

export async function loadMidiFile(data: ArrayBuffer): Promise<void> {
	if (!browser) return;
	const { parseMidiFile } = await import('../engine/midi-analysis');
	const midi = parseMidiFile(data);
	parsedMidi.set(midi);
	const eng = await getEngine();
	await eng.loadMidi(midi);
}

export async function loadMidiFromUrl(url: string): Promise<void> {
	if (!browser) return;
	engineState.update((s) => ({ ...s, loading: true, loadingMessage: 'Loading MIDI file...' }));
	const response = await fetch(url);
	const data = await response.arrayBuffer();
	await loadMidiFile(data);
}

export async function play(): Promise<void> {
	if (!browser) return;
	const eng = await getEngine();
	await eng.play();
}

export function pause(): void {
	engine?.pause();
}

export function stop(): void {
	engine?.stop();
}

export function seek(seconds: number): void {
	engine?.seek(seconds);
}

export function setVolume(trackIndex: number, volume: number): void {
	engine?.setVolume(trackIndex, volume);
}

export function setPan(trackIndex: number, pan: number): void {
	engine?.setPan(trackIndex, pan);
}

export function toggleSolo(trackIndex: number): void {
	engine?.toggleSolo(trackIndex);
}

export function toggleMute(trackIndex: number): void {
	engine?.toggleMute(trackIndex);
}

export const isPlaying = derived(engineState, ($s) => $s.playback === 'playing');
export const isPaused = derived(engineState, ($s) => $s.playback === 'paused');
export const isLoading = derived(engineState, ($s) => $s.loading);
