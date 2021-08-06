const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
const map = L.map('map')
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: attribution }).addTo(map);
const fields = JSON.parse(document.getElementById('geojson-data').textContent);
let feature = L.geoJSON(fields).addTo(map);

setInterval(function () {
    map.fitBounds(feature.getBounds());
    map.invalidateSize();
 }, 100);

