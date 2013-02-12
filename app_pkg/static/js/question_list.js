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
	'views/question_collection_display_view',
	'views/question_collection_creation_view',
	], 
	function(google, GMapsHelper, location, Question, User, QuestionCollection, OwnQuestionView, QuestionCollectionDisplayView, QuestionCollectionCreatorView) {

		var debug = true;
		$("li.questions-tab").addClass("active");

		// Cannot get a reference to the map without being passed along as a callback.
		var ugly = function(map) {
			// Question Components

			// Question View Generator
			var generate_question_view = function(model, options) {
				return new OwnQuestionView(options);
				// if (model.attributes.author_id == USER_ID) {
				// 	return new OwnPostingView(options);
				// } 
				// else {
				// 	return new OtherPostingView(options);
				// }
			}

			question_collection = new QuestionCollection()

			question_creator = new QuestionCollectionCreatorView({
				el: $("#question-creator-region"),
				collection: question_collection,
				map_reference: map,
			});
			question_creator.render();

			question_display = new QuestionCollectionDisplayView({
				el: $("#question-display-region"),
				collection: question_collection,
				fetch_data: {
				},
				generate_question_view: generate_question_view,
				empty_message: "No Questions yet. You could be the first to ask one."
			});
			question_display.render()

			// posting_on_map = new PostingCollectionMapView({
			// 	el: $(map),
			// 	collection: posting_collection,
			// 	//map_reference: map,				
			// });
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
					setTimeout(fire_geolocation_updates, 2000);
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