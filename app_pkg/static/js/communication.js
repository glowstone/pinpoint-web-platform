define(function() {

	var ajax_post_send = function(address, message, successAction) {
	    $.ajax({
			type: 'POST',
			url: address,
			data: message,
			contentType: 'application/json',
			dataType: 'json',
			success: successAction,
		});
	};

	return {
		
		get_json: function(url, success_action, error_action) {
			$.ajax({
				dataType: "json",
				url: url,
				success: success_action,
				error: error_action
			});
		},

		ajax_post: function(address, messageType, messagePayload, successAction) {
		    message = {};
		    message['messageType'] = messageType;
		    message['messageData'] = messagePayload;
		    jsonRequest = JSON.stringify(message);
		    ajax_post_send(address, message, successAction); 
		},	

	}
});