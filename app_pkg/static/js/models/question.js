define([
	],
	function() {

		var Question = Backbone.Model.extend({
			defaults: {
			},
			urlRoot: '/api/question',
		});

		return Question;

	// End of Module define function closure.
	}
);
