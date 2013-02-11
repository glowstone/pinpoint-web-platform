define([
	'handlebars',
	'text!templates/user_view_template',
	],
	function(handlebars, template_source) {

		var debug = false;

		var template = Handlebars.compile(template_source);
		Handlebars.registerHelper('pluralize', function(number, single, plural) {
  			if (number === 1) { return single; }
  			else { return plural; }
		});

		var UserView = Backbone.View.extend({
			/*
			Constructs a templated view of an individual User model.
			No client triggered delegateEvents causing server-side changes (no
			creating, editing, or deleting User resources).
			Client may trigger an event by cicking on the UserView div to cause
			a redirect to that user's adventure_list profile. 
			*/
			tagName: 'div',
			events: {
				'click .visit-profile': 'visit_profile_handler',
				'click a.visit-profile-link': 'visit_profile_handler',
			},
			// Default model is null because one must be provided upon initialization.
			model: null,
			initialize: function() {
				_.bindAll(this, 'render', 'unrender', 'visit_profile_handler');
			
				// Bind model events to corresponding view handlers
				this.model.bind('change', this.render);
				this.model.bind('remove', this.unrender);
			},
			render: function() {		
				var rendered_content = template(this.model.attributes);
				$(this.el).html(rendered_content);
				return this;
			},
			unrender: function() {
				$(this.el).remove();
			},
			visit_profile_handler: function(event) {
				event.preventDefault();
				user_username = this.model.attributes.username
				window.location.href = WEB_USER_URL + user_username;
			}
		});

		return UserView;

		// End of Module define function closure.
	}
);