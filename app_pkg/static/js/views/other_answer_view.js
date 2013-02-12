define([
	'text!templates/other_answer_template',
	'handlebars',
	],
	function(template_source) {

		var debug = false;

		var template = Handlebars.compile(template_source);
		Handlebars.registerHelper('pluralize', function(number, single, plural) {
  			if (number === 1) { return single; }
  			else { return plural; }
		});


		var OtherAnswerView = Backbone.View.extend({
			/*
			Constructs a templated view of an individual Answer that is not 
			owned by the person viewing it. The client may not trigger delegateEvents 
			causing server side changes
			*/
			tagName: 'div',
			events: {
				'click a.visit-profile': 'visit_profile_handler',
			},
			// Default model is null because one must be provided upon initialization.
			model: null,
			initialize: function() {
				_.bindAll(this, 'render', 'unrender', 'scroll_to', 'visit_profile_handler');
			
				// Bind model events to corresponding view handlers
				this.model.bind('scroll_to', this.scroll_to)
				this.model.bind('change', this.render);
				this.model.bind('remove', this.unrender);
			},
			scroll_to: function() {
				var self = this;
				$('html,body').animate({
					scrollTop: $(this.el).offset().top
				}, 1500);
				$(".other-answer", this.el).animate(
					{borderColor: "#42ACE9"}, 750, 
					function() {
						$(".other-answer", self.el).animate({borderColor: "#E3E3E3"}, 1750);
					}
				);	
			},
			visit_profile_handler: function(event) {
				event.preventDefault();
				user_username = this.model.attributes.author.username
				window.location.href = WEB_USER_URL + user_username;
			},
			render: function() {	
				var rendered_content = template(this.model.attributes);
				$(this.el).html(rendered_content);
				return this;
			},
			unrender: function() {
				$(this.el).slideUp();
			},
		});

		return OtherAnswerView;

		// End of Module define function closure.
	}
);