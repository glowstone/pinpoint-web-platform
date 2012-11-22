(function () {
	"use strict";
	// TODO use async worker scripts for this application-wide

	if ("geolocation" in navigator) {
		// Get first-available, coarse position (IP or Wifi location)
		navigator.geolocation.getCurrentPosition(function(position) {
			console.log("We found you!");
			console.log(position);
		}, function(error) {
			console.log(error.message);
		});
		// Async fine position watcher
		var positionObject = {enableHighAccuracy: true, maximumAge: 60000, timeout: 60000};
		var wpid = navigator.geolocation.watchPosition(function(position) {
			console.log("Enhance");
			console.log(position);
		}, function(error) {
			console.log(error.message);
		}, positionObject);
	} else {
		console.log("Lame");
	}

})();