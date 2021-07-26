<script>
	export let name;
	import { onMount } from "svelte";
	import Farms from "../Farms.svelte";
	import Farm from "../Farm.svelte";
	let farms;
	let farm;
</script>

<main>
	<h1>Hello {name}!</h1>
	<Farms {farms} />
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>