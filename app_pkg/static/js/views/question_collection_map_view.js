define([
	'collections/question_collection',
	'views/question_map_view',
	],
	function(QuestionCollection, QuestionMapView, BBDebug) {

		debug = false;

		var QuestionCollectionMapView = Backbone.View.extend({
		/*
			Constructs a view for a QuestionCollection (you may pass one in or a
			new collection will be initialized). You must pass the el you wish to
			bind the view to. 
			No client triggered delegateEvents causing server-side changes (no 
			creating adventures, although subviews can allow editing/deletion).
			Arguments: el, collection(optional), fetch_data, subview_type 
			*/
		events: {
			// By default, no client triggered delegateEvents on this view.
		},
		// Default collection SHARED by views unless caller provides AdventureCollection at initialization.
		collection: new QuestionCollection(),
		initialize: function(options) {
			_.bindAll(this, 'render', 'append_subview', 'depend_subview', 'reset_handler')
			this.el = options.el;
			this.generate_question_view = options.generate_question_view

			// Bind collection events to corresponding view handlers
			this.collection.on('add', this.append_subview);
			this.collection.on('remove', this.depend_subview);
			this.collection.on('reset', this.reset_handler);
		},
		render: function() {
			var self = this;
			_(this.collection.models).each(function(model) {
				self.append_subview(model);
			}, this);
			return this;
		},
		append_subview: function(model) {
			var question_map_view = new QuestionMapView({model: model, map_reference: this.el});
			// Subview knows how to place the marker on the Map
			question_map_view.render()
		},
		depend_subview: function(model) {
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

	return QuestionCollectionMapView

	// End of Module define function closure.
	}
);
