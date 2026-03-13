<script lang="ts">
	import { setVolume, setPan, toggleSolo, toggleMute } from '../stores/audio-engine';
	import { ROLE_LABELS, ROLE_COLORS } from '../engine/role-inference';
	import type { MixerChannelState } from '../engine/types';

	const { track }: { track: MixerChannelState } = $props();

	const roleLabel = $derived(ROLE_LABELS[track.role] || 'Unknown');
	const roleColor = $derived(ROLE_COLORS[track.role] || '#808080');

	function handleVolume(event: Event) {
		const input = event.target as HTMLInputElement;
		setVolume(track.trackIndex, parseFloat(input.value));
	}

	function handlePan(event: Event) {
		const input = event.target as HTMLInputElement;
		setPan(track.trackIndex, parseFloat(input.value));
	}
</script>

<div class="track-strip" class:muted={track.mute} class:soloed={track.solo}>
	<div class="track-header">
		<span class="role-dot" style:background-color={roleColor}></span>
		<div class="track-info">
			<span class="track-name">{track.name}</span>
			<span class="track-role">{roleLabel}</span>
		</div>
	</div>

	<div class="controls">
		<div class="buttons">
			<button
				class="btn solo-btn"
				class:active={track.solo}
				onclick={() => toggleSolo(track.trackIndex)}
				title="Solo"
			>S</button>
			<button
				class="btn mute-btn"
				class:active={track.mute}
				onclick={() => toggleMute(track.trackIndex)}
				title="Mute"
			>M</button>
		</div>

		<div class="slider-group">
			<label class="slider-label">Vol
			<input
				type="range"
				min="-40"
				max="6"
				step="0.5"
				value={track.volume}
				oninput={handleVolume}
				class="volume-slider"
			/></label>
			<span class="slider-value">{Math.round(track.volume)}dB</span>
		</div>

		<div class="slider-group">
			<label class="slider-label">Pan
			<input
				type="range"
				min="-1"
				max="1"
				step="0.05"
				value={track.pan}
				oninput={handlePan}
				class="pan-slider"
			/></label>
			<span class="slider-value">{track.pan > 0 ? `R${Math.round(track.pan * 100)}` : track.pan < 0 ? `L${Math.round(Math.abs(track.pan) * 100)}` : 'C'}</span>
		</div>
	</div>
</div>

<style>
	.track-strip {
		background: #111122;
		border: 1px solid #1a1a2e;
		border-radius: 6px;
		padding: 0.6rem 0.8rem;
		transition: all 0.15s;
	}

	.track-strip.muted {
		opacity: 0.45;
	}

	.track-strip.soloed {
		border-color: #daa520;
	}

	.track-header {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		margin-bottom: 0.5rem;
	}

	.role-dot {
		width: 8px;
		height: 8px;
		border-radius: 50%;
		flex-shrink: 0;
	}

	.track-info {
		display: flex;
		flex-direction: column;
		min-width: 0;
	}

	.track-name {
		color: #ccc;
		font-size: 0.8rem;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}

	.track-role {
		color: #666;
		font-size: 0.65rem;
		text-transform: uppercase;
		letter-spacing: 0.05em;
	}

	.controls {
		display: flex;
		align-items: center;
		gap: 0.75rem;
	}

	.buttons {
		display: flex;
		gap: 0.25rem;
	}

	.btn {
		width: 22px;
		height: 22px;
		border: 1px solid #333;
		background: none;
		color: #666;
		font-size: 0.65rem;
		font-weight: bold;
		cursor: pointer;
		border-radius: 3px;
		display: flex;
		align-items: center;
		justify-content: center;
		transition: all 0.1s;
	}

	.btn:hover {
		border-color: #555;
		color: #aaa;
	}

	.solo-btn.active {
		background: #daa520;
		border-color: #daa520;
		color: #000;
	}

	.mute-btn.active {
		background: #cc4444;
		border-color: #cc4444;
		color: #fff;
	}

	.slider-group {
		display: flex;
		align-items: center;
		gap: 0.3rem;
		flex: 1;
	}

	.slider-label {
		color: #555;
		font-size: 0.6rem;
		text-transform: uppercase;
		min-width: 1.5rem;
	}

	input[type='range'] {
		flex: 1;
		height: 3px;
		-webkit-appearance: none;
		appearance: none;
		background: #1a1a2e;
		border-radius: 2px;
		outline: none;
	}

	input[type='range']::-webkit-slider-thumb {
		-webkit-appearance: none;
		width: 10px;
		height: 10px;
		background: #6a6aaa;
		border-radius: 50%;
		cursor: pointer;
	}

	.slider-value {
		color: #555;
		font-size: 0.6rem;
		font-family: monospace;
		min-width: 2.5rem;
		text-align: right;
	}
</style>
