define([
	'models/question',
	'collections/question_collection',
	'library/backbone_debug',
	'text!templates/question_creation_template',
	'handlebars',
	],
	function(Question, QuestionCollection, BBDebug, template_source, hb) {


		debug = false;
		var template = Handlebars.compile(template_source);

		var QuestionCollectionCreationView = Backbone.View.extend({
				/*
				Constructs a view that is used to create Questions, but it does
				NOT display the questions. To do that, pass both the 
				QuestionCollectionDisplayView and this QuestionCollectionCreationView
				the same Question collection at initialization so they internally
				share a data structure. 
				Client may trigger delegateEvents to create a new Question. The hooked
				up display view then has rendering responsibility for the question in
				the shared collection.
				Required: pass collection instance in options hash.
				*/
				events: {
					// Client may trigger Adventure creation.
					'click button#location-chooser': 'choose_location',
					'click button#submit-question': 'question_creation_handler',
				},
				model: Question,
				// Default collection SHARED by views unless caller provides QuestionCollection at initialization.
				collection: null,
				initialize: function(options) {
					_.bindAll(this, 'render', 'question_creation_handler', 'choose_location')
					this.el = options.el;
					this.map_reference = options.map_reference;
					this.last_photo_url = null;
					this.last_latitude = null;
					this.last_longitude = null;
					this.map_chooser_state = false;   // Not currently choosing.
					this.last_marker = null;
				},
				render: function() {
					// Render the adventure creation panel.
					var rendered_content = template({});
					$(this.el).append(rendered_content);
					return this;
				},
				question_creation_handler: function(event) {
					var values = {};
					var inputs = $('#question-creation-form :input');
					_(inputs).each(function(input) {
						values[input.name] = $(input).val();
					});
					values['latitude'] = this.last_latitude;
					values['longitude'] = this.last_longitude;

					if (this.last_latitude == null || this.last_longitude == null) {
						//Don't submit the data. Flash the button to choose a location.
						this.missing_location_notification();			
					}
					else if (values.title == "" || values.text == ""){
						if (values.title == "") {
							this.missing_title_notification();
						} else {
							this.missing_text_notification();
						}
					}
					else {
						// Valid attempt to create a Question
						// Creates a Question with the values, saves model to server, and adds model to the collection
						var self = this;
						this.collection.create(values, {
							wait: true,
							success: function(model, response, options) {
								// server response only returns question id, which is merged into client side model.
								// fetch model immediately to retrieve additional information.
								model.fetch({
									update: true,
								})
								self.reset_creation_form()
							},
							error: function(model, xhr, options) {
								console.log(xhr);
							}
						});
					}				
				},
				choose_location: function() {
					var self = this;
					if (this.map_chooser_state) {
						$("#location-chooser").text("Location (required)");
						this.map_reference.setOptions({draggableCursor: null});
						google.maps.event.removeListener(this.listen_handle);
						// No longer choosing location
						this.map_chooser_state = false;
					}
					else {
						var update_chosen_location = function(e) {
							if (self.last_marker) {
								self.last_marker.setMap(null);    //Clear last marker
							}
							var position = e.latLng;
							self.last_latitude = position.lat();
							self.last_longitude = position.lng();
							$("#latitude-indicator").text((self.last_latitude).toFixed(2))   // toFixed safe for presentation only.
							$("#longitude-indicator").text((self.last_longitude).toFixed(2))
							var marker = new google.maps.Marker({
								position: new google.maps.LatLng(self.last_latitude, self.last_longitude),
								map: self.map_reference,
								animation: google.maps.Animation.BOUNCE,
							});
							self.last_marker = marker
						}
						// Setup click listener on the map
						$("#location-chooser").text("Stop Choosing");
						this.map_reference.setOptions({draggableCursor: 'crosshair'});
						this.listen_handle = google.maps.event.addListener(this.map_reference, 'click', update_chosen_location);	
						this.map_chooser_state = true;
					}
				},
				reset_creation_form: function() {
					$("#question-creation-form")[0].reset();
					this.last_longitude = null;
					this.last_latitude = null;
					if (this.last_marker) {
						this.last_marker.setMap(null);    //Clear last marker
					}
					if (this.map_chooser_state) {
						//Stops listening, changes button back, sets map_chooser state to false
						this.choose_location();   
					}
					$("#latitude-indicator").text("None");
					$("#longitude-indicator").text("None");
				},
				missing_location_notification: function() {
					$("#location-chooser").animate({opacity: .3}, 200, function() {
						$("#location-chooser").animate({opacity: 1}, 200, function() {
							$("#location-chooser").animate({opacity: .3}, 200, function() {
								$("#location-chooser").animate({opacity: 1}, 200);
							});
						});
					});		
				},
				missing_title_notification: function() {
					console.log("Missing title");
					var self = this;
					console.log($("#questioncreate-title"));
					$("#question-create-title", this.el).animate(
						{backgroundColor: "#42ACE9"}, 750,
						function() {
							$("#question-create-title", self.el).animate({borderColor: "#E3E3E3"}, 1750);
						}
					);	
				}, 
				missing_text_notification: function() {
					console.log("Missing text");
					$("question-create-text", this.el).animate(
						{borderColor: "#42ACE9"}, 750,
						function() {
							$("question-create-text", self.el).animate({borderColor: "#E3E3E3"}, 1750);
						}
					);	
				}
				// Additional creation view handlers go here

			});

		return QuestionCollectionCreationView

	// End of Module define function closure
	}
);