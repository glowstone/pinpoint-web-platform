define([
	], 
	function() {


		// return an object to define the google maps helper module
		return {

			get_func_to_build_map_at_latlng_and_call: function(el, callback) {
				/* 
				Accepts the element in which the map should be rendered and a 
				callback that should be invoked after the returned function is
				called. 
				Returns a function to which a latitude and longitude are provided
				and then the map rendering occurs and callback is called, passing
				the map instance.
				*/
				var map_build_and_call = function(latitude, longitude) {
					var mapOptions = {
						zoom: 12,
						center: new google.maps.LatLng(latitude, longitude),
						mapTypeId: google.maps.MapTypeId.ROADMAP,
						scrollwheel: false,
					}
					// Default to NYC as the Google Static Map does.
					// center: new google.maps.LatLng(40.715062, -74.005844),
					var map = new window.google.maps.Map(el[0], mapOptions);
					callback(map);
				}
				return map_build_and_call
			},

			get_func_to_build_map_and_call: function(callback) {

				var map_build_and_call = function(results, status) {
					var elem = document.getElementById("map_canvas");
					if (status == google.maps.GeocoderStatus.OK) {
						var mapOptions = {
							zoom: 12,
							center: results[0].geometry.location,
							mapTypeId: google.maps.MapTypeId.ROADMAP,
							scrollwheel: false,
						}
						var marker = new google.maps.Marker({
				            map: map,
				            position: results[0].geometry.location
				        });
					} 
					else {
						var mapOptions = {
						    zoom: 12,
						    // Default to NYC as the Google Static Map does.
						    center: new google.maps.LatLng(40.715062, -74.005844),
						    mapTypeId: google.maps.MapTypeId.ROADMAP,
						    scrollwheel: false
						}
					}
					var map = new window.google.maps.Map(elem, mapOptions);
					callback(map);
				}
				return map_build_and_call

			},

		}

});