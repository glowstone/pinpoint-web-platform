define([
	'collections/answer_collection',
	'views/answer_map_view',
	],
	function(AnswerCollection, AnswerMapView, BBDebug) {

		debug = false;

		var AnswerCollectionMapView = Backbone.View.extend({
		/*
			Constructs a view for a AnswerCollection (you may pass one in or a
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
		collection: new AnswerCollection(),
		initialize: function(options) {
			_.bindAll(this, 'render', 'append_subview', 'depend_subview', 'reset_handler')
			this.el = options.el;
			this.generate_answer_view = options.generate_answer_view
			this.map_reference = options.map_reference;

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
			var answer_map_view = new AnswerMapView({model: model, map_reference: this.el});
			// Subview knows how to place the marker on the Map
			answer_map_view.render()
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

	return AnswerCollectionMapView

	// End of Module define function closure.
	}
);
