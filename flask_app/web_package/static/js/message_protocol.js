
// Constants
var verbose = false;

// Send an AJAX POSTing (to host server only, no XSS)    
var ajax_post = function(address, messageType, messagePayload, successAction) {
    message = {};
    message['messageType'] = messageType;       //Add a messageType to every message.
    message['messageData'] = messagePayload;
    jsonRequest = JSON.stringify(message);
    ajax_post_send(address, jsonRequest, successAction);  //Use jQuery to send  
}

// Send a Cross Site Get Request
var xss_get = function(address, messageType, messagePayload, successAction) {
    if (verbose) {
	console.log("Sending (to " + address + ")");
    }
    message = {};
    message['messageType'] = messageType;         //Add a messageType to every message
    message['messageData'] = messagePayload;
    xss_get_send(address, message, successAction);      //Use jQuery to send.
}
   
// Uses jQuery .ajax to send AJAX POST
var ajax_post_send = function(address, message, successAction) {
    if (verbose) {console.log("Sending:"); console.log(message);}
    $.ajax({
	type: 'POST',
	url: address,
	data: message,
	contentType: 'application/json',
	dataType: 'json',
	success: function(response) {                           
	    if (verbose) {console.log("Server responded to AJAX call with: "); console.log(response);}
	    successAction(response);
	}
    });
};

// Uses jQuery .ajax to send XSS GET
var xss_get_send = function(address, message, successAction) {
    if (verbose) {
	console.log(message);
    }
    $.ajax({
	type: 'GET',
	url: address,
	data: message,
	dataType: 'jsonp',
	success: function(response) {                           
	    if (verbose) {console.log("Server responded to AJAX call with: "); console.log(response);}
	    successAction(response);
	}
    });
};

if (verbose) {console.log("message_protocol.js loaded");}

