<script context="module">
export const load = async ({page, fetch}) => {
    const res = await fetch("http://localhost:8000/farms/");

    const farm = await res.json()

    return {
        props: {
            farm,
        },
    };
};
</script>

<script>
    export let farm;
</script>

<div class="container">
    <div class="row">
      <div class="col-sm-5" id="farm-info">
        <h1>{farm.name}</h1>
        <p class="text-muted">Website: {farm.website}</p>
      </div>
      <div class="col-lg-7" id="farm-desc">
        <h3>Description:</h3>
        <p class="card-text">{farm.description}</p>
      </div>
    </div>
    <div class="row">
      <div class="col-sm-3" id="fields-list">
        <h3>Fields:</h3>
        {#if farm.fields}
          {#each farm.fields as field}
            <ul>
              <li>{field.field_name}</li>
            </ul>
          {/each}
        {:else}
          <p>No fields...</p>
        {/if}
      </div>
      <div class="col-lg-9" id="farm-map">
          <div id="map"></div>
      </div>
    </div>  
</div>
  
<style>
    .container {
    margin-left: 0;
    margin-right: 0;
    }
    
    #map {
    position: inherit;
    top:0; 
    bottom:0; 
    right:0; 
    left:0;
    height: 500px; 
    width: 100%;
    }

    #farm-info{
        background-color: #bee9f7;
    }
</style>