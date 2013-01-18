
require(['location'], function(location) {

	// var google_static_maps_url = "http://maps.googleapis.com/maps/api/staticmap"
	// var key = GOOGLE_API_KEY

	
	// var success_action = function(latitude, longitude) {
	// 	var img = new Image();
	// 	var source = google_static_maps_url + "?center=" + latitude + "," + longitude  + "&zoom=13&size=940x400&sensor=true&scale=1" + "&key=" + key
	// 	img.src = source;
	// 	//img.height=400;
	// 	//img.width=950;
	// 	$(img).addClass("span12");
	// 	img.class="span4"
	// 	$("#map_region").prepend(img);
		
	// 	console.log(source);
	// 	console.log(latitude);
	// 	console.log(longitude);
	// 	console.log("Success");
	// }
	
	// // No error_action, because default coordinates will be used if errors occur.
	// location.geoplugin_coordinates(success_action);
	

	$(document).ready(function() {

		$("#signup_btn").click(function() {
			window.location = "/signup";
		});

		$("#login_btn").click(function() {
			window.location = "/login";
		});

	

	// End of Document Ready Closure
	});
// End of requireJS Closure
});