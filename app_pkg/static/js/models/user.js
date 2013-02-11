define([
	],
	function() {

		var User = Backbone.Model.extend({
			defaults: {},
			urlRoot: '/api/user',
		});

		return User;

	// End of Module define function closure.
	}
);