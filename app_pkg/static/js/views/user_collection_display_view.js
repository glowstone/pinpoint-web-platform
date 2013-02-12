define([
	'collections/user_collection',
	'views/user_view',
	'library/backbone_debug',
	'text!templates/empty_message_template',
	'handlebars',
	],
	function(UserCollection, UserView, BBDebug, empty_template_src, handlebars) {

		debug = false;
		var empty_template = Handlebars.compile(empty_template_src);


		var UserCollectionDisplayView = Backbone.View.extend({
			/* 
			Constructs a view for a UserCollection (you may pass one in or a
			new collection will be initialized). You must pass the el you wish
			to bind the view to. It auto-fetches collection data, merges with the
			collection, and rerenders.
			No client triggered delegateEvents causing server-side changes (no
			creating, editing, or deleting of User resources).
			*/
			events: {
				// By default, no client triggered delegateEvents on this view.
			},
			// Default collection SHARED by views unless caller provides UserCollection at initialization.
			collection: new UserCollection(),
			initialize: function(options) {
				_.bindAll(this, 'render', 'append_subview', 'depend_subview', 'reset_handler', 'check_empty_status');
				this.el = options.el;         // No el by default. 
				this.fetch_data = options.fetch_data;
				this.generate_user_view = options.generate_user_view;
				this.empty_message_template = empty_template({empty_message: options.empty_message});
			
				// Bind collection events to corresponding view handlers
				this.collection.on('add', this.append_subview);
				this.collection.on('remove', this.depend_subview);
				this.collection.on('reset', this.reset_handler);
			},
			check_empty_status: function() {
				if (this.collection.length === 0) {
					$(this.el).find('ul.view-region').append(this.empty_message_template);
				} else {
					$(this.el).find('ul.view-region div.empty-message').slideUp();
				}
			},
			render: function() {
				$(this.el).append("<ul class='view-region'></ul>");
				var self = this;
				_(this.collection.models).each(function(model) {
					self.append_subview(model);
				}, this);
				this.check_empty_status();

				// Naive, no backoff.
				(function fetch_user_collection() {
					self.collection.fetch({
						update: true,
						data: self.fetch_data,
						success: BBDebug.notify(debug, "Successful UserCollection fetch"),
						error: BBDebug.notify(debug, "Error upon UserCollection fetch"),
					});
					setTimeout(fetch_user_collection, 6000);
				})();				
				return this;
			},
			append_subview: function(model) {
				this.check_empty_status();				
				var user_view = this.generate_user_view({model: model});
				$('ul', this.el).append(user_view.render().el);
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

		return UserCollectionDisplayView

	// End of Module define function closure.
	}
);
