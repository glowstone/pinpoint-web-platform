define([
	'collections/answer_collection',
	'library/backbone_debug',
	'text!templates/empty_message_template',
	'handlebars',
	],
	function(AnswerCollection, BBDebug, empty_template_src, handlebars) {

		debug = false;
		var empty_template = Handlebars.compile(empty_template_src);

		var AnswerCollectionDisplayView = Backbone.View.extend({
		/*
			Constructs a view for an AnswerCollection (you may pass one in or a
			new collection will be initialized). You must pass the el you wish to
			bind the view to. It auto-fetches collection data, merges with the 
			collection, and rerenders.
			No client triggered delegateEvents causing server-side changes (no 
			creating adventures, although subviews can allow editing/deletion).
			Arguments: el, collection(optional), fetch_data, subview_type 
			*/
		events: {
			// By default, no client triggered delegateEvents on this view.
			},
		// Default collection SHARED by views unless caller provides AdventureCollection at initialization.
		collection: new AnswerCollection(),
		initialize: function(options) {
			_.bindAll(this, 'render', 'append_subview', 'depend_subview', 'reset_handler', 'check_empty_status')
			this.el = options.el;
			this.fetch_data = options.fetch_data;
			this.generate_answer_view = options.generate_answer_view
			this.empty_message_template = empty_template({empty_message: options.empty_message});


			// Bind collection events to corresponding view handlers
			this.collection.on('add', this.append_subview);
			this.collection.on('change', this.check_empty_status)
			this.collection.on('remove', this.depend_subview);
			this.collection.on('reset', this.reset_handler);
		},
		check_empty_status: function() {
			if (this.collection.length === 0) {
				$(this.el).find('div.view-region').append(this.empty_message_template);
			} else {
				$(this.el).find('div.view-region div.empty-message').slideUp();
			}
		},
		render: function() {
			$(this.el).append("<div class='view-region'></div>");
			var self = this;
			_(this.collection.models).each(function(item) {
				self.append_subview(item);
			}, this);
			this.check_empty_status();

			// Naive, no backoff.
			(function fetch_user_collection() {
				self.collection.fetch({
					update: true,
					data: self.fetch_data,
					success: BBDebug.notify(debug, "Successful AnswerCollection fetch"),
					error: BBDebug.notify(debug, "Error upon AnswerCollection fetch"),
				});
				setTimeout(fetch_user_collection, 8000);
			})();
			return this;
		},
		append_subview: function(model) {
			var answer_view = this.generate_answer_view(model, {model: model});
			$(answer_view.render().el).hide().prependTo($(this.el).find('div.view-region')).slideDown("slow");
			this.check_empty_status();
		},
		depend_subview: function(model) {
			this.check_empty_status();
			model.trigger('remove');
		}, 
		reset_handler: function(collection, options) {
			/* If reset were manually called on the collection (passed in from outside)
			or fetched without the update option, new models are already installed in the
			collection. Our job now is to clean up old model views and rerender with 
			new models.
			*/
			var self = this;
			_(options.previousModels).each(function(model) {
				self.depend_subview(model);
			})
			self.render();
		},
	});

	return AnswerCollectionDisplayView

	// End of Module define function closure.
	}
);
