<script>
	import { onMount } from "svelte";
	import Farm from "./Farm.svelte";
	let farms;
	onMount(async () => {
		await fetch(`http://localhost:8000/farms/`)
			.then(r => r.json())
			.then(data => {
				farms = data;
			});
	})
</script>

<style>
	.loading {
		opacity: 0;
		animation: 0.4s 0.8s forwards fade-in;
	}
	@keyframes fade-in {
		from { opacity: 0; }
		to { opacity: 1; }
	}
	li {
		list-style-type: georgian;
	}
</style>

{#if farms}
	{#each farms as farm }
		<ul>
			<li>		
				<h3>{farm.name}</h3>
                <p><a href={farm.website}>{farm.website}</a></p>
                <p><a href={`/farms/${farm.id}`}>Details</a></p>
			</li>
		</ul>
	{/each}

{:else}
	<p class="loading">loading...</p>
{/if}