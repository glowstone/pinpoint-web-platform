define([
	'models/question'
	],
	function(Question) {

		var QuestionCollection =  Backbone.Collection.extend({
			model: Question,
			// Flask Restless server does not accept a trailing slash.
			url: '/api/question',
			parse: function(response) {
				// The backend Flask Restless API provides the object array inside the objects response field.
				return response.objects;
			}
		});

		return QuestionCollection;

	// End of Module define function closure.
	}
);