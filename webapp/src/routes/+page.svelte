<script lang="ts">
	import FileLoader from '$lib/components/FileLoader.svelte';
	import Player from '$lib/components/Player.svelte';
	import TrackMixer from '$lib/components/TrackMixer.svelte';
	import { engineState, audioInitialized, initAudio } from '$lib/stores/audio-engine';

	const state = $derived($engineState);
	const audioReady = $derived($audioInitialized);

	async function handleEnableAudio() {
		await initAudio();
	}
</script>

{#if !audioReady}
	<div class="audio-gate">
		<div class="gate-content">
			<h1>Grandaddy MIDI Engine</h1>
			<p>Style-aware MIDI performance engine</p>
			<button class="enable-audio-btn" onclick={handleEnableAudio}>
				<svg viewBox="0 0 24 24" width="28" height="28">
					<polygon points="6,4 20,12 6,20" fill="currentColor" />
				</svg>
				Tap to Enable Audio
			</button>
			<p class="gate-hint">Required for mobile playback</p>
		</div>
	</div>
{/if}

<div class="page" class:hidden={!audioReady}>
	<header>
		<h1>Grandaddy MIDI Engine</h1>
		<p class="subtitle">Style-aware MIDI performance engine</p>
	</header>

	<section class="loader-section">
		<FileLoader />
	</section>

	<section class="player-section">
		<Player />
	</section>

	{#if state.tracks.length > 0}
		<section class="mixer-section">
			<TrackMixer />
		</section>
	{/if}
</div>

<style>
	.audio-gate {
		position: fixed;
		inset: 0;
		background: #0a0a14;
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 1000;
	}

	.gate-content {
		text-align: center;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 1rem;
	}

	.gate-content h1 {
		margin: 0;
		font-size: 1.8rem;
		color: #ddd;
		font-weight: 400;
		letter-spacing: 0.05em;
	}

	.gate-content p {
		margin: 0;
		color: #666;
		font-size: 0.9rem;
	}

	.enable-audio-btn {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		background: #1a1a3e;
		border: 2px solid #4a4a7a;
		color: #ccc;
		padding: 1rem 2rem;
		border-radius: 12px;
		font-size: 1.1rem;
		cursor: pointer;
		transition: all 0.2s;
		margin-top: 1rem;
		-webkit-tap-highlight-color: transparent;
	}

	.enable-audio-btn:hover, .enable-audio-btn:active {
		background: #252560;
		border-color: #7a7aba;
		color: #fff;
		transform: scale(1.02);
	}

	.gate-hint {
		color: #444 !important;
		font-size: 0.75rem !important;
	}

	.page {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.page.hidden {
		display: none;
	}

	header {
		border-bottom: 1px solid #1a1a2e;
		padding-bottom: 1rem;
	}

	h1 {
		margin: 0;
		font-size: 1.5rem;
		color: #ddd;
		font-weight: 400;
		letter-spacing: 0.05em;
	}

	.subtitle {
		margin: 0.25rem 0 0 0;
		color: #555;
		font-size: 0.8rem;
	}

	section {
		width: 100%;
	}
</style>
