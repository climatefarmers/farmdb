const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors';
var osmLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: attribution });

var ocsLayer = L.tileLayer.wms('https://maps.isric.org/mapserv?map=/map/ocs.map', {
    layers: 'ocs_0-30cm_mean',
    opacity: 0.5
});

const fields = JSON.parse(document.getElementById('geojson-data').textContent);
let feature = L.geoJSON(fields);


const map = L.map('map', {
    layers: [osmLayer, ocsLayer, feature]
}
);

var baseMaps = {
    "OSM": osmLayer
};

var overlayMaps = {
    "fields": feature,
    "OCS 30cm": ocsLayer
};

L.control.layers(baseMaps, overlayMaps).addTo(map);

setInterval(function () {
    map.fitBounds(feature.getBounds());
    map.invalidateSize();
 }, 100);




