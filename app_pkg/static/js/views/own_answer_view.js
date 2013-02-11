define([
	'text!templates/own_answer_template',
	'handlebars',
	],
	function(template_source) {

		var debug = false;

		var template = Handlebars.compile(template_source);
		Handlebars.registerHelper('pluralize', function(number, single, plural) {
  			if (number === 1) { return single; }
  			else { return plural; }
		});


		var OwnAnswerView = Backbone.View.extend({
			/*
			Constructs a templated view of an individual Answer that is owned
			by the current user. The client may trigger delegateEvents causing 
			server side changes (editing or deleting individual answers by the 
			author of the answers is allowed). To other Users in the same adventure
			the answers will not be writable.
			*/
			tagName: 'div',
			events: {
				'click a.visit-profile': 'visit_profile_handler',
				'click button.answer-delete': 'delete_handler',
			},
			// Default model is null because one must be provided upon initialization.
			model: null,
			initialize: function() {
				_.bindAll(this, 'render', 'unrender', 'edit_handler', 'delete_handler', 'scroll_to', 'visit_profile_handler');
			
				// Bind model events to corresponding view handlers
				this.model.bind('scroll_to', this.scroll_to);
				this.model.bind('change', this.render);
				this.model.bind('remove', this.unrender);
			},
			render: function() {	
				var rendered_content = template(this.model.attributes);
				$(this.el).html(rendered_content);
				return this;
			},
			unrender: function() {
				$(this.el).slideUp();
			},
			scroll_to: function() {
				var self = this;
				$('html,body').animate({
					scrollTop: $(this.el).offset().top
				}, 1500);
				$(".own-answer", this.el).animate(
					{borderColor: "#42ACE9"}, 750,
					function() {
						$(".own-answer", self.el).animate({borderColor: "#E3E3E3"}, 1750);
					}
				);	
			},
			visit_profile_handler: function(event) {
				event.preventDefault();
				user_username = this.model.attributes.author.username
				window.location.href = WEB_USER_URL + user_username;
			},
			edit_handler: function() {
				console.log("edit handler called");
			},
			delete_handler: function() {				
				var self = this;
				this.model.destroy({
					wait: false,
					error: function(model, xhr, options) {
						if (options.xhr.status === 204) {
  							self.unrender();     // Backbone considers 204 NO CONTENT an error, though it is valid
  						} else {
  							// Failed to delete. Network problems?
  						}
					}
				});
			}
		});

		return OwnAnswerView;

		// End of Module define function closure.
	}
);