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

	console.log("Got here");
	console.log(SCRIPT_ROOT);
	var params = {};
	ajax_post(SCRIPT_ROOT + '/api/question/list.json', params);

// No code below this line. End of enclosing anon. function.
});

