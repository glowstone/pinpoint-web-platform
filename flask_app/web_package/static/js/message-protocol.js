(function () {
	"use strict";

	// Constants
	var VERBOSE = false;

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
	    if (verbose) {console.log("Sending:"); console.log(message);}
	    $.ajax({
		type: 'POST',
		url: address,
		data: message,
		contentType: 'application/json',
		dataType: 'json',
		success: function(response) {                           
		    if (verbose) {console.log("Server responded to AJAX call with: "); console.log(response);}
		    //successAction(response);
		}
	    });
	};

	if (VERBOSE) {console.log("message-protocol.js loaded");}

// No code below this line. End of enclosing anon. function.
})();

   



