define([
	],
	function() {

		var URL_BASE = "http://maps.googleapis.com/maps/api/staticmap"
		var KEY = GOOGLE_API_KEY

		return {
			map_builder: function(el, width, height) {
				/* Returns a function which takes the latitude and longitude
				the map should be centered at and prepends it inside the given
				el element. Will download a map of the desired width and height.
				*/
				var free_size = 640,
					aspect_ratio = width/height,
					image_width,
					image_height;

				// Set size of div for image wrapping
				el.css('width', width);
				el.css('height', height);
				
				if (aspect_ratio > 1.0) {
					// Wider than it is tall.
					image_width = free_size;                 
					image_height = Math.round(free_size/aspect_ratio);
				} else {
					// Taller than it is wide.
					image_height = free_size;
					image_width = Math.round(free_size/aspect_ratio);
				}


				return function(latitude, longitude) {
					var img = new Image();
					var source = URL_BASE + "?center=" + latitude + "," + longitude  + "&zoom=13&size=" + image_width + "x" + image_height + "&sensor=true&scale=2" + "&key=" + KEY
					
					img.src = source;
					el.css('width', width);
					el.css('height', height);
					
					$("#map_region").append(img);

				}
			},
		}

	// End of Module define function closure
	}
);