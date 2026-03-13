<script lang="ts">
	let { children } = $props();
</script>

<svelte:head>
	<title>Grandaddy MIDI Engine</title>
</svelte:head>

<div class="app">
	{@render children()}
</div>

<style>
	:global(body) {
		margin: 0;
		padding: 0;
		background: #0a0a14;
		color: #ccc;
		font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
		-webkit-font-smoothing: antialiased;
	}

	:global(*) {
		box-sizing: border-box;
	}

	.app {
		max-width: 900px;
		margin: 0 auto;
		padding: 2rem 1.5rem;
	}
</style>
