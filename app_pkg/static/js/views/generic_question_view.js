define([
	'text!templates/generic_question_template',
	'handlebars',
	'library/backbone_debug',
	],
	function(template_source, handlebars, BBDebug) {

		var debug = true;

		var template = Handlebars.compile(template_source);
		Handlebars.registerHelper('pluralize', function(number, single, plural) {
  			if (number === 1) { return single; }
  			else { return plural; }
		});


		var GenericQuestionView = Backbone.View.extend({
			/*
			Constructs a templated view of an individual Question model. 
			This view is used for questions viewed by the owner and non-owners
			alike on the question detail page. It should primarily just display
			information about the question and its counts.
			*/
			tagName: 'div',
			events: {
				'click .visit-author': 'visit_author_handler',
			},
			// Default model is null because one must be provided upon initialization.
			model: null,
			initialize: function() {
				_.bindAll(this, 'render', 'unrender', 'visit_author_handler');
			
				// Bind model events to corresponding view handlers
				this.model.bind('change', this.render);
				this.model.bind('remove', this.unrender);
			},
			render: function() {
				var self = this;
				var rendered_content = template(this.model.attributes);
				$(this.el).html(rendered_content).slideDown();

				(function fetch_question_collection() {
					self.model.fetch({
						update: true,
						data: self.fetch_data,
						success: BBDebug.notify(debug, "Successful Question fetch"),
						error: BBDebug.notify(debug, "Error upon Question fetch"),
					});
					setTimeout(fetch_question_collection, 8000);
				})();
				return this;
			},
			unrender: function() {
				$(this.el).fadeOut();
			},
			visit_author_handler: function(event) {
				event.preventDefault();
				user_username = this.model.attributes.author.username
				window.location.href = WEB_USER_URL + user_username;
			},
		});

		return GenericQuestionView;

		// End of Module define function closure.
	}
);