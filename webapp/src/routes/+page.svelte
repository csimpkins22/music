<script lang="ts">
	import FileLoader from '$lib/components/FileLoader.svelte';
	import Player from '$lib/components/Player.svelte';
	import TrackMixer from '$lib/components/TrackMixer.svelte';
	import { engineState } from '$lib/stores/audio-engine';
	import { get } from 'svelte/store';

	const state = $derived($engineState);
</script>

<div class="page">
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
	.page {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
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
