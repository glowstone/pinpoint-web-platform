define([
	],
	function() {

		var debug = false;

		var AnswerMapView = Backbone.View.extend({
			/*
			Constructs a templated view of an individual Answer that is owned
			by the current user. The client may trigger delegateEvents causing 
			server side changes (editing or deleting individual postings by the 
			author of the postings is allowed). To other Users in the same adventure
			the postings will not be writable.
			*/
			tagName: 'div',
			events: {
				//'click button.posting-delete': 'delete_handler',
			},
			// Default model is null because one must be provided upon initialization.
			model: null,
			initialize: function(options) {
				_.bindAll(this, 'render', 'unrender');
				this.map_reference = options.map_reference
			
				// Bind model events to corresponding view handlers
				// Preventing from dynamically responding to changes since location is not
				// editable by user. This prevents phantom animations placing multiple times.
				//this.model.bind('change', this.render);
				this.model.bind('remove', this.unrender);
			},
			render: function() {
				var self = this;
				var attributes = this.model.attributes
				// Create Marker
				var marker = new google.maps.Marker({
					position: new google.maps.LatLng(attributes.latitude, attributes.longitude),
					map: this.map_reference[0],   //Unwrap from jQuery
					title: this.model.attributes.text.substring(0,100) + "...",
					animation: google.maps.Animation.DROP,
				})
				this.marker = marker;
				// Tie in our listener method with the Google Maps Library
				google.maps.event.addListener(marker, 'click', function() {
					self.model.trigger("scroll_to");
				});
				return marker;
			},
			unrender: function() {
				this.marker.setMap(null);
			},
		});

		return AnswerMapView;

		// End of Module define function closure.
	}
);