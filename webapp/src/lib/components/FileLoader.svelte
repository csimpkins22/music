<script lang="ts">
	import { loadMidiFile, loadMidiFromUrl, engineState } from '../stores/audio-engine';

	const BUNDLED_SONGS = [
		{ name: '01 - Dial Tone Lullaby', file: '/midi/01_dial_tone_lullaby.mid' },
		{ name: '02 - The Machinery of Sunlight', file: '/midi/02_the_machinery_of_sunlight.mid' },
		{ name: '03 - Beautiful Machines', file: '/midi/03_beautiful_machines.mid' },
		{ name: '04 - Last Signal Home', file: '/midi/04_last_signal_home.mid' },
		{ name: '05 - Peripheral Glow', file: '/midi/05_peripheral_glow.mid' }
	];

	let dragOver = false;

	async function handleFileInput(event: Event) {
		const input = event.target as HTMLInputElement;
		const file = input.files?.[0];
		if (!file) return;
		const data = await file.arrayBuffer();
		await loadMidiFile(data);
	}

	async function handleDrop(event: DragEvent) {
		event.preventDefault();
		dragOver = false;
		const file = event.dataTransfer?.files?.[0];
		if (!file || !file.name.endsWith('.mid')) return;
		const data = await file.arrayBuffer();
		await loadMidiFile(data);
	}

	function handleDragOver(event: DragEvent) {
		event.preventDefault();
		dragOver = true;
	}

	function handleDragLeave() {
		dragOver = false;
	}

	async function loadBundled(url: string) {
		await loadMidiFromUrl(url);
	}
</script>

<div class="file-loader">
	<div class="bundled-songs">
		<h3>Compositions</h3>
		<div class="song-list">
			{#each BUNDLED_SONGS as song}
				<button
					class="song-button"
					class:active={$engineState.songName && song.file.includes($engineState.songName.toLowerCase().replace(/ /g, '_'))}
					onclick={() => loadBundled(song.file)}
					disabled={$engineState.loading}
				>
					{song.name}
				</button>
			{/each}
		</div>
	</div>

	<div
		class="drop-zone"
		class:drag-over={dragOver}
		ondrop={handleDrop}
		ondragover={handleDragOver}
		ondragleave={handleDragLeave}
		role="button"
		tabindex="0"
	>
		<p>Drop a MIDI file here</p>
		<label class="file-input-label">
			or browse
			<input type="file" accept=".mid,.midi" onchange={handleFileInput} />
		</label>
	</div>
</div>

<style>
	.file-loader {
		display: flex;
		gap: 1.5rem;
		align-items: stretch;
	}

	.bundled-songs {
		flex: 1;
	}

	h3 {
		margin: 0 0 0.75rem 0;
		font-size: 0.85rem;
		text-transform: uppercase;
		letter-spacing: 0.1em;
		color: #888;
	}

	.song-list {
		display: flex;
		flex-direction: column;
		gap: 0.35rem;
	}

	.song-button {
		background: #1a1a2e;
		border: 1px solid #2a2a4a;
		color: #ccc;
		padding: 0.5rem 0.75rem;
		text-align: left;
		cursor: pointer;
		border-radius: 4px;
		font-size: 0.85rem;
		transition: all 0.15s;
	}

	.song-button:hover:not(:disabled) {
		background: #252545;
		border-color: #4a4a7a;
		color: #fff;
	}

	.song-button.active {
		background: #2a2a5a;
		border-color: #6a6aaa;
		color: #fff;
	}

	.song-button:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}

	.drop-zone {
		flex: 0 0 180px;
		border: 2px dashed #333;
		border-radius: 8px;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding: 1rem;
		transition: all 0.2s;
		text-align: center;
	}

	.drop-zone.drag-over {
		border-color: #6a6aaa;
		background: #1a1a3e;
	}

	.drop-zone p {
		margin: 0 0 0.5rem 0;
		color: #666;
		font-size: 0.8rem;
	}

	.file-input-label {
		color: #6a8adb;
		cursor: pointer;
		font-size: 0.8rem;
	}

	.file-input-label:hover {
		text-decoration: underline;
	}

	.file-input-label input {
		display: none;
	}
</style>
