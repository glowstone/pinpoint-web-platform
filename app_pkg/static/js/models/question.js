define([
	],
	function() {

		var Question = Backbone.Model.extend({
			defaults: {
			},
			/* Backbone uses this route during saving models and  Trailing slash required since dealing
			with individual models and Backbone just appends the model.id.*/
			urlRoot: '/api/question',
		});

		return Question;

	// End of Module define function closure.
	}
);
