function initMap() {
    var latlng = new google.maps.LatLng(40.7411583, -73.60908);

    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 14,
        center: latlng,
        disableDefaultUI: true
    });

    google.maps.event.addDomListenerOnce(map, 'idle', function () {
        google.maps.event.addDomListener(window, 'resize', function () {
            map.setCenter(latlng);
        });
    });

    var geocoder = new google.maps.Geocoder();
    var address = 'Learner-Centered Initiatives, Ltd';

    geocodeAddress(geocoder, map, address);
}

function geocodeAddress(geocoder, resultsMap, address) {
    geocoder.geocode({'address': address}, function (results, status) {
        if (status === 'OK') {
            resultsMap.setCenter(results[0].geometry.location);
            var marker = new google.maps.Marker({
                map: resultsMap,
                position: results[0].geometry.location,
                draggable: true,
                animation: google.maps.Animation.DROP
            });

            var infowindow = new google.maps.InfoWindow({
                content: '<b>' + address + '</b>'
                //size: new google.maps.Size(150, 50)
            });

            marker.addListener('click', function () {
                if (marker.getAnimation() !== null) {
                    marker.setAnimation(null);
                } else {
                    marker.setAnimation(google.maps.Animation.BOUNCE);
                }

                infowindow.open(resultsMap, marker);

            });

            return marker;
        } else {
            alert('Geocode was not successful for the following reason: ' + status);
        }
    });

    return false;
}