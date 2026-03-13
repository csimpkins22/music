<script lang="ts">
	import { engineState, play, pause, stop, seek } from '../stores/audio-engine';
	import { formatDuration } from '../engine/midi-analysis';

	const state = $derived($engineState);
	const progress = $derived(state.duration > 0 ? (state.position / state.duration) * 100 : 0);

	function handleSeek(event: Event) {
		const input = event.target as HTMLInputElement;
		const pct = parseFloat(input.value);
		seek((pct / 100) * state.duration);
	}

	async function togglePlay() {
		if (state.playback === 'playing') {
			pause();
		} else {
			await play();
		}
	}
</script>

<div class="player" class:disabled={!state.songName || state.loading}>
	<div class="transport">
		<button class="transport-btn stop-btn" onclick={stop} disabled={state.playback === 'stopped'} title="Stop">
			<svg viewBox="0 0 24 24" width="18" height="18">
				<rect x="6" y="6" width="12" height="12" fill="currentColor" />
			</svg>
		</button>

		<button class="transport-btn play-btn" onclick={togglePlay} disabled={!state.songName || state.loading} title={state.playback === 'playing' ? 'Pause' : 'Play'}>
			{#if state.playback === 'playing'}
				<svg viewBox="0 0 24 24" width="22" height="22">
					<rect x="6" y="5" width="4" height="14" fill="currentColor" />
					<rect x="14" y="5" width="4" height="14" fill="currentColor" />
				</svg>
			{:else}
				<svg viewBox="0 0 24 24" width="22" height="22">
					<polygon points="6,4 20,12 6,20" fill="currentColor" />
				</svg>
			{/if}
		</button>
	</div>

	<div class="position">
		<span class="time">{formatDuration(state.position)}</span>
		<input
			type="range"
			min="0"
			max="100"
			step="0.1"
			value={progress}
			oninput={handleSeek}
			class="seek-bar"
			disabled={!state.songName}
		/>
		<span class="time">{formatDuration(state.duration)}</span>
	</div>

	<div class="song-info">
		{#if state.loading}
			<span class="loading">{state.loadingMessage || 'Loading...'}</span>
		{:else if state.songName}
			<span class="song-name">{state.songName}</span>
			<span class="bpm">{Math.round(state.bpm)} BPM</span>
		{:else}
			<span class="hint">Select a song to begin</span>
		{/if}
	</div>
</div>

<style>
	.player {
		display: flex;
		align-items: center;
		gap: 1.5rem;
		padding: 1rem 1.5rem;
		background: #0d0d1a;
		border: 1px solid #1a1a2e;
		border-radius: 8px;
	}

	.player.disabled {
		opacity: 0.6;
	}

	.transport {
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	.transport-btn {
		background: none;
		border: 1px solid #333;
		color: #ccc;
		cursor: pointer;
		border-radius: 50%;
		display: flex;
		align-items: center;
		justify-content: center;
		transition: all 0.15s;
	}

	.transport-btn:hover:not(:disabled) {
		border-color: #666;
		color: #fff;
	}

	.transport-btn:disabled {
		opacity: 0.3;
		cursor: not-allowed;
	}

	.stop-btn {
		width: 32px;
		height: 32px;
	}

	.play-btn {
		width: 42px;
		height: 42px;
		border-color: #4a4a7a;
	}

	.play-btn:hover:not(:disabled) {
		border-color: #7a7aba;
		background: #1a1a3e;
	}

	.position {
		flex: 1;
		display: flex;
		align-items: center;
		gap: 0.75rem;
	}

	.time {
		font-family: 'SF Mono', 'Fira Code', monospace;
		font-size: 0.8rem;
		color: #888;
		min-width: 3rem;
	}

	.seek-bar {
		flex: 1;
		height: 4px;
		-webkit-appearance: none;
		appearance: none;
		background: #1a1a2e;
		border-radius: 2px;
		outline: none;
		cursor: pointer;
	}

	.seek-bar::-webkit-slider-thumb {
		-webkit-appearance: none;
		width: 12px;
		height: 12px;
		background: #6a6aaa;
		border-radius: 50%;
		cursor: pointer;
	}

	.seek-bar:disabled {
		cursor: not-allowed;
		opacity: 0.3;
	}

	.song-info {
		min-width: 160px;
		text-align: right;
	}

	.song-name {
		color: #ccc;
		font-size: 0.85rem;
	}

	.bpm {
		color: #666;
		font-size: 0.75rem;
		margin-left: 0.5rem;
	}

	.loading {
		color: #6a8adb;
		font-size: 0.8rem;
		animation: pulse 1.5s ease-in-out infinite;
	}

	.hint {
		color: #555;
		font-size: 0.8rem;
	}

	@keyframes pulse {
		0%, 100% { opacity: 1; }
		50% { opacity: 0.5; }
	}
</style>
