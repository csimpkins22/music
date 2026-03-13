/**
 * Audio engine singleton store.
 * Manages the PerformanceEngine instance and exposes reactive state.
 */

import { writable, derived } from 'svelte/store';
import { PerformanceEngine } from '../engine/renderer';
import { parseMidiFile } from '../engine/midi-analysis';
import { grandaddyProfile } from '../profiles/grandaddy';
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

let engine: PerformanceEngine | null = null;

function getEngine(): PerformanceEngine {
	if (!engine) {
		engine = new PerformanceEngine(grandaddyProfile);
		engine.onStateChange((state) => {
			engineState.set(state);
		});
	}
	return engine;
}

export async function loadMidiFile(data: ArrayBuffer): Promise<void> {
	const midi = parseMidiFile(data);
	parsedMidi.set(midi);
	const eng = getEngine();
	await eng.loadMidi(midi);
}

export async function loadMidiFromUrl(url: string): Promise<void> {
	engineState.update((s) => ({ ...s, loading: true, loadingMessage: 'Loading MIDI file...' }));
	const response = await fetch(url);
	const data = await response.arrayBuffer();
	await loadMidiFile(data);
}

export async function play(): Promise<void> {
	await getEngine().play();
}

export function pause(): void {
	getEngine().pause();
}

export function stop(): void {
	getEngine().stop();
}

export function seek(seconds: number): void {
	getEngine().seek(seconds);
}

export function setVolume(trackIndex: number, volume: number): void {
	getEngine().setVolume(trackIndex, volume);
}

export function setPan(trackIndex: number, pan: number): void {
	getEngine().setPan(trackIndex, pan);
}

export function toggleSolo(trackIndex: number): void {
	getEngine().toggleSolo(trackIndex);
}

export function toggleMute(trackIndex: number): void {
	getEngine().toggleMute(trackIndex);
}

export const isPlaying = derived(engineState, ($s) => $s.playback === 'playing');
export const isPaused = derived(engineState, ($s) => $s.playback === 'paused');
export const isLoading = derived(engineState, ($s) => $s.loading);
