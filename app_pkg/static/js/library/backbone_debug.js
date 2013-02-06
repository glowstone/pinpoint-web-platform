define([
	],
	function() {

		return {

			// Backbone Debugging Notifier
			notify: function(debug, message) {
				if (debug) {
					return function(collection, response, options) {
						console.log(message);
						console.log(collection);
						console.log(response);
						console.log(options);
					}
				} 
				else {
					return function() {

					}
				}
			}

		}

	// End of Module define function closure.
	}
);