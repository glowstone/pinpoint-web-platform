define([
	'text!templates/own_question_template',
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


		var OwnQuestionView = Backbone.View.extend({
			/*
			Constructs a templated view of an individual Question model
			owned by the current authenticated User. 
			The client may trigger delegateEvents causing server side 
			changes (editing or deleting). Deleting individual Questions
			is allowed and handled.
			*/
			tagName: 'div',
			events: {
				'click .visit-author': 'visit_user_handler',
				'click a.visit-question': 'visit_question_handler',
				'click button.visit-question': 'visit_question_handler',
				'click a.delete-question': 'delete_handler',
			},
			// Default model is null because one must be provided upon initialization.
			model: null,
			initialize: function() {
				_.bindAll(this, 'render', 'unrender', 'scroll_to', 'visit_user_handler', 'visit_question_handler', 'delete_handler');
			
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
				$(".own-posting", this.el).animate(
					{borderColor: "#42ACE9"}, 750,
					function() {
						$(".own-posting", self.el).animate({borderColor: "#E3E3E3"}, 1750);
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
			delete_handler: function() {
				var self = this;
				this.delete_question_answers();
				this.model.destroy({
					wait: true,
					error: function(model, xhr, options) {
						if (options.xhr.status === 204) {
  							self.unrender();     // Backbone considers 204 NO CONTENT an error, though it is valid
  						} else {
  							// Failed to delete. Network problems?
  						}
					}
				});
			},
			delete_question_answers: function() {
				// Flask Restless API does not remove Answers when deleting a Question
				// To get Question deletion to succeed, must delete all questions
				_(this.model.attributes.answers).each(function(id_obj) {
					an_answer = new Answer({
						id: id_obj.id
					});
					an_answer.destroy();
				});
			},

		});

		return OwnQuestionView;

		// End of Module define function closure.
	}
);