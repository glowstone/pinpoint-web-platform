define([
	'text!templates/other_question_template',
	'models/answer',
	'handlebars',
	],
	function(template_source, Answer) {

		var debug = false;

		var template = Handlebars.compile(template_source);
		Handlebars.registerHelper('pluralize', function(number, single, plural) {
  			if (number === 1) { return single; }
  			else { return plural; }
		});


		var OtherQuestionView = Backbone.View.extend({
			/*
			Constructs a templated view of an individual Question model
			that is not owned by the current authenticated User. 
			The client may not trigger delegateEvents causing server side 
			changes (no editing or deleting).
			*/
			tagName: 'div',
			events: {
				'click .visit-author': 'visit_user_handler',
				'click a.visit-question': 'visit_question_handler',
				'click button.visit-question': 'visit_question_handler',
			},
			// Default model is null because one must be provided upon initialization.
			model: null,
			initialize: function() {
				_.bindAll(this, 'render', 'unrender', 'scroll_to', 'visit_user_handler', 'visit_question_handler');
			
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
				$(".other-question", this.el).animate(
					{borderColor: "#42ACE9"}, 750,
					function() {
						$(".other-question", self.el).animate({borderColor: "#E3E3E3"}, 1750);
					}
				);	
			},
			visit_user_handler: function(event) {
				event.preventDefault();
				user_username = this.model.attributes.author.username
				console.log(user_username);
				window.location.href = WEB_USER_URL + user_username;
			},
			visit_question_handler: function() {
				event.preventDefault()
				question_id = this.model.attributes.id
				window.location.href = WEB_QUESTION_URL + question_id;
			},

		});

		return OtherQuestionView;

		// End of Module define function closure.
	}
);