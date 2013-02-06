require([
	'library/location',
	'library/google_static_maps',
	], 
	function(location, static_map) {

		console.log("Loaded index.js");

		var width = $(window).width(),
			height = Math.round($(window).height()*0.45);
			

		var builder = static_map.map_builder($("#map_region"), width, height);
		// Callback passed in will always be called, either with user coords or with default coords.
		location.geoplugin_coordinates(builder);
		

		$(document).ready(function() {

			$("#signup_btn").click(function() {

				$("#signup-div").animate({
					right: '-20px',
				});
				$("#login-div").animate({
					right: '-330px',
				});
			});

			$("#login_btn").click(function() {
				$("#signup-div").animate({
					right: '-330px',
				});
				$("#login-div").animate({
					right: '-20px',
				});
			});

			if (REDIRECTION) {
				// Flip out the login panel since user was redirected to login.
				$("#signup-div").animate({
					right: '-330px',
				});
				$("#login-div").animate({
					right: '-20px',
				});
			} else {
				$("#signup-div").animate({
					right: '-20px',
				});
			}

			$("#learn-more-scroll").click(function() {
				$('html,body').animate({
					scrollTop: $("#scroll-landing").offset().top
				}, 1500);

			});

		

		// End of Document Ready Closure
		});

	// End of requireJS Closure
	}
);