define([
	],
	function() {

		var Question = Backbone.Model.extend({
			defaults: {
			},
			/* Backbone does not seem to pay any attention to the collection url 
			while saving individual models. Trailing slash required since dealing
			with individual models and Backbone just appends the model.id.*/
			urlRoot: '/api/question/',
		});

		return Question;

	// End of Module define function closure.
	}
);
