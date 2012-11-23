
self.addEventListener('message', function(e) {
	self.postMessage('Hello?');
}, false);



var perform_request = function(data) {
	var that = this;

	// Create Standard XMLHttpRequest
	var xreq = new XMLHttpRequest();
	xreq.responseType = "json";

	// Prepare request to PUT geolocation data asynchronously.
	xreq.open('PUT', '/api/user/set_location.json', true);   // async = true 

	xreq.addEventListener('readystatechange', function(e) {
		that.postMessage(xreq.readyState);
		if (xreq.readyState === 4) {
			if (xreq.status === 200) {
				that.postMessage(xreq.response);
				that.postMessage(xreq.responseType);
				var result = JSON.parse(xreq.response);
				that.postMessage(result);
				that.postMessage(result.success);
				that.postMessage('Got here');
			} else {
				that.postMessage("Failure");

			}
		} 
	}, false)

	// Fire the request
	self.postMessage(data);
	xreq.send(data);
}

var get_location = function() {
	return {'lat': Math.floor(Math.random()*11),
			   'long': Math.floor(Math.random()*11)
			   }
}

// Notify Backend of Current Location
var exponential_XMLHttpRequest = function(next_message, perform_request) {
	var min_interval = 1000;
	var max_interval = 5000;
	perform_request(next_message());
}

exponential_XMLHttpRequest(get_location, perform_request);

