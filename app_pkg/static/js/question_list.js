require.config({
	paths: {
		'handlebars': 'library/handlebars',
		'text': 'library/require-plugins/text',
		'async': 'library/async',
		'google_maps_loader': 'library/google_maps_loader',
		'google_maps': 'library/google_maps',
	},
	shim: {
		'handlebars': {
			exports: 'Handlebars',
		},
		'jquery-ui': {
			exports: '$',
		}
	},
	config: {
        text: {
            useXhr: function (url, protocol, hostname, port) {
                //Return true of false. true means "use xhr", false means
                //"fetch the .js version of this resource".
                return true;
            }
        }
    }
});
require([
	'google_maps_loader',
	'google_maps',         // My Google Maps Helper
	'library/location',
	'models/question',
	'models/user',
	'collections/question_collection',
	'views/own_question_view',
	'views/other_question_view',
	'views/question_collection_display_view',
	'views/question_collection_creation_view',
	'views/question_collection_map_view',
	], 
	function(google, GMapsHelper, location, Question, User, QuestionCollection, OwnQuestionView, OtherQuestionView, QuestionCollectionDisplayView, QuestionCollectionCreatorView, QuestionCollectionMapView) {

		var debug = true;
		$("li.questions-tab").addClass("active");

		// Cannot get a reference to the map without being passed along as a callback.
		var ugly = function(map) {
			// Question Components

			// Question View Generator
			var generate_question_view = function(model, options) {
				if (model.attributes.author && model.attributes.author.id == USER_ID) {
					return new OwnQuestionView(options);
				} 
				else if (typeof model.attributes.author == 'undefined'){
					// Should only be undefined if built in client and waiting for data (i.e. authenticated user owns the Question)
					return new OwnQuestionView(options);
				}
				else {
					return new OtherQuestionView(options);
				}
			}

			// User viewing his own Question Listing Page
			///////////////////////////////////////////////////////////////////
			if (YOUR_PAGE) {

				question_collection = new QuestionCollection();
				question_collection_aux = new QuestionCollection();
				question_creator = new QuestionCollectionCreatorView({
					el: $("#question-creator-region"),
					collection: question_collection,
					map_reference: map,
				});
				question_creator.render();

				user_question_display = new QuestionCollectionDisplayView({
					el: $("#user-question-display-region"),
					collection: question_collection,
					fetch_data: {
						q: JSON.stringify({
							"filters": [
								{
									name: "user_id",
									op: "==",
									val: USER_ID,
								},
							]
						}),
					},
					generate_question_view: generate_question_view,
					empty_message: "You haven't created any Questions. Try pinning one on the map now?"
				});
				user_question_display.render();

				global_question_display = new QuestionCollectionDisplayView({
					el: $("#global-question-display-region"),
					collection: question_collection_aux,
					fetch_data: {
						q: JSON.stringify({
							"filters": [
								{
									name: "user_id",
									op: "!=",
									val: USER_ID,
								},
							]
						}),
					},
					generate_question_view: generate_question_view,
					empty_message: "No Questions yet. You could be the first to ask one."
				});
				global_question_display.render()

				question_on_map = new QuestionCollectionMapView({
					el: $(map),
					collection: question_collection,
					map_reference: map,				
				});

				question_on_map_aux = new QuestionCollectionMapView({
					el: $(map),
					collection: question_collection_aux,
					map_reference: map,				
				});

			}
			else {
				question_collection = new QuestionCollection();

				page_owner_question_display = new QuestionCollectionDisplayView({
					el: $("#page-owner-question-display-region"),
					collection: question_collection,
					fetch_data: {
						q: JSON.stringify({
							"filters": [
								{
									name: "user_id",
									op: "==",
									val: PAGE_OWNER_ID,
								},
							]
						}),
					},
					generate_question_view: generate_question_view,
					empty_message: "This user has not yet created any Questions. :("
				});
				page_owner_question_display.render();

				question_on_map_aux = new QuestionCollectionMapView({
					el: $(map),
					collection: question_collection,
					map_reference: map,				
				});


			}

		}

		// Return a function that will build the map and invoke the custom callback after the map is created.
		build_map = GMapsHelper.get_func_to_build_map_at_latlng_and_call($("#map_canvas"), ugly);
		location.geoplugin_coordinates(build_map);


	$(document).ready(function() {

		// Create a User Representation Client-Side to update User latitude and longitude
		user = new User({
			id: USER_ID,
		});
		// Fetch the User and then start saving current latitude/longitude to server.


		user.fetch({
			success: function(model, response, options) {
				var geolocation_put = function(latitude, longitude) {
					model.attributes.latitude = latitude;
					model.attributes.longitude = longitude;
					model.save({},{wait:true});
				};
				// Naive, no backoff.
				(function fire_geolocation_updates() {
					// Pass a function that will be called with the discovered latitude and longitude.
					location.geoplugin_coordinates(geolocation_put);
					setTimeout(fire_geolocation_updates, 60000);
				})();	
			},
			error: function(model, xhr, options) {
				// Network problems?
			}
		});


	// End of Document Ready Closure
	});
// End of requireJS Closure
});