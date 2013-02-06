define([
	"communication",
	], 
	function(communication) {
	
		var geopluggin_url = "http://www.geoplugin.net/json.gp?jsoncallback=?";

		// return an object to define the location module
		return {
			//onSuccess - Load geospecific Google map
			//onFailure - Load default NYC Google map
			geoplugin_coordinates: function(after_coordinates_found) {

				var geoplugin_success = function(data) {
					var latitude = data['geoplugin_latitude']
					var longitude = data['geoplugin_longitude']
					after_coordinates_found(latitude, longitude);
				}

				var success_action = function(data) {
					// Check successful result to see if needed data is present
					if (('geoplugin_latitude' in data)  && ('geoplugin_longitude' in data)) {
						geoplugin_success(data);
					} else {
						error_action(data);			
					}
				}

				var error_action = function(data) {
					// Assume default location
					var latitude = 40.715062;
					var longitude = -74.005844;
					console.log("Warning, using the deault location");
					after_coordinates_found(latitude, longitude);
				}

				communication.get_json(geopluggin_url, success_action, error_action);
			},
		}
});