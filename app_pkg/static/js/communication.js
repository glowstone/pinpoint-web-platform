define(function() {

	return {
		send_message: function(message) {
			console.log("Sending message " + message);
			return 6;
		},
		get_json: function(url, success_action, error_action) {
			$.ajax({
				dataType: "json",
				url: url,
				success: success_action,
				error: error_action
			});
		}
	}
});