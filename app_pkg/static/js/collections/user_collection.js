define([
	'models/user'
	],
	function(User) {

		var UserCollection =  Backbone.Collection.extend({
			model: User,
			// Flask Restless server does not accept a trailing slash.
			url: '/api/user',
			parse: function(response) {
				// The backend Flask Restless API provides the object array inside the objects response field.
				return response.objects;
			},
		});

		return UserCollection;

	// End of Module define function closure.
	}
);