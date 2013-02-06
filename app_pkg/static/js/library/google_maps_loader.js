//Google Maps (HTTP) API v3 Asynchronous Loader
// Depends on requirejs async plugin

define([
	'async!http://maps.googleapis.com/maps/api/js?key=' + GOOGLE_API_KEY + '&sensor=true&languge=en',
	],
	function() {
		// Returns google.maps object, which defines the module.
		return window.google
	
	// End of Module define function closure
	}
);