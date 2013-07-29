google.load("maps", "2");

$(document).unload(function(){
    GUnload();
});
function formatDecimal(myNumber) {
    
    return myNumber.toFixed(6);
}
$(document).ready(function(){

    var lat = -34.893169;
    var lng = -56.165543;
    
    var center = new GLatLng(lat,lng);

    var map = new google.maps.Map2(document.getElementById("map"));
    map.addControl(new GSmallMapControl());
    map.setCenter(center, 7);

    this.onMapClick = function(overlay, point) {
        $('#id_latitud').val(formatDecimal(point.lat()));
        $('#id_longitud').val(formatDecimal(point.lng()));
        if (this.marker == null) {
            this.marker = new GMarker(point);
            this.map.addOverlay(this.marker);
        } else {
            this.marker.setPoint(point);
        }
    }

    this.marker = new GMarker(center);
    map.addOverlay(this.marker);

    GEvent.bind(map, "click", this, this.onMapClick);
    
    
});