<script lang="ts">
	import { engineState } from '../stores/audio-engine';
	import TrackStrip from './TrackStrip.svelte';

	const tracks = $derived($engineState.tracks);
</script>

<div class="track-mixer">
	{#if tracks.length > 0}
		<h3>Tracks</h3>
		<div class="tracks">
			{#each tracks as track (track.trackIndex)}
				<TrackStrip {track} />
			{/each}
		</div>
	{/if}
</div>

<style>
	.track-mixer {
		margin-top: 1rem;
	}

	h3 {
		margin: 0 0 0.75rem 0;
		font-size: 0.85rem;
		text-transform: uppercase;
		letter-spacing: 0.1em;
		color: #888;
	}

	.tracks {
		display: flex;
		flex-direction: column;
		gap: 0.35rem;
	}
</style>
