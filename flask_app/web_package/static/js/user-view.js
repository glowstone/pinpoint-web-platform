$(document).ready(function() {
	"use strict";
	// All code

	var VERBOSE = true;

	// Send an AJAX POSTing (to host server only, no XSS)    
	var ajax_post = function(address, messageType, messagePayload, successAction) {
	    message = {};
	    message['messageType'] = messageType;       //Add a messageType to every message.
	    message['messageData'] = messagePayload;
	    jsonRequest = JSON.stringify(message);
	    ajax_post_send(address, jsonRequest, successAction);  //Use jQuery to send  
	}

	// Uses jQuery .ajax to send AJAX POST
	var ajax_post = function(address, message) {
	    if (VERBOSE) {console.log("Sending:"); console.log(message);}
	    console.log(address);
	    $.ajax({
		type: 'GET',
		url: address,
		data: message,
		contentType: 'application/json',
		dataType: 'json',
		success: function(response) {                           
		    if (VERBOSE) {console.log("Server responded to AJAX call with: "); console.log(response);}
		    //successAction(response);
		}
	    });
	};

	var get_location = function() {
		return {'user_id': 3,
			'latitude': Math.floor(Math.random()*11),
				'longitude': Math.floor(Math.random()*11)
				}
	}

	console.log("Got here");
	console.log(SCRIPT_ROOT);
	var params = {};

	// Dedicated Web Worker
	// If file exists at URL, spawn worker thread. Async download the file. 
	// Otherwise, fails silently.
	
	/*var worker = new Worker(SCRIPT_ROOT + '/static/js/geo-worker.js');

	// Listen to worker's message events, in case he complains.
	worker.addEventListener('message', function(event) {
		console.log('Worker fired a message event!');
		console.log(event.data);
	}, false);

	// Start worker by firing 'message' event.
	worker.postMessage('Hello World');        // Send data to the worker
	*/
	
	ajax_post(SCRIPT_ROOT + '/api/question/list.json', params);
	ajax_post(SCRIPT_ROOT + '/api/user/set_location.json', get_location())


// No code below this line. End of enclosing anon. function.
});

