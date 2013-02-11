define([
	'models/answer'
	],
	function(Answer) {

		var AnswerCollection =  Backbone.Collection.extend({
			model: Answer,
			// Flask Restless server does not accept a trailing slash.
			url: '/api/answer',
			parse: function(response) {
				// The backend Flask Restless API provides the object array inside the objects response field.
				return response.objects;
			},
		});

		return AnswerCollection;

	// End of Module define function closure.
	}
);