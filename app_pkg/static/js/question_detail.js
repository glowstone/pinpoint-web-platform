require.config({
	paths: {
		'handlebars': 'library/handlebars',
		'text': 'library/require-plugins/text',
		'jquery-ui': 'library/jquery-ui-1.10.0.custom.min',
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
	'communication', 
	'google_maps_loader',
	'google_maps',           // My Google Maps Helper
	'models/user',
	'models/question',
	'models/answer',
	'collections/user_collection',
	'collections/answer_collection',
	'views/own_answer_view',
	'views/other_answer_view',
	'views/user_view',
	//'views/user_adventure_page_view',
	//'views/generic_adventure_view',
	'views/answer_collection_display_view',
	'views/answer_collection_creation_view',
	'views/answer_collection_map_view',
	'views/answer_map_view',
	//'views/user_collection_display_view',
	'library/backbone_debug',
	], 
	function(communication, google, GMapsHelper, User, Question, Answer, UserCollection, AnswerCollection, OwnAnswerView, OtherAnswerView, UserView, AnswerCollectionDisplayView, AnswerCollectionCreatorView, AnswerCollectionMapView, AnswerMapView, BBDebug) {

		var debug = true;

		// Cannot get a reference to the map without being passed along as a callback.
		var ugly = function(map) {
			// Posting Components

			// Posting View Generator
			var generate_answer_view = function(model, options) {
				if (model.attributes.author && model.attributes.author.id == USER_ID) {
					return new OwnAnswerView(options);
				}
				else if (typeof model.attributes.author == 'undefined'){
					// Should only be undefined if built in client and waiting for data (i.e. authenticated user owns the Answer)
					return new OwnAnswerView(options);
				}
				else {
					return new OtherAnswerView(options);
				}
			}

			answer_collection = new AnswerCollection()

			answer_creator = new AnswerCollectionCreatorView({
				el: $("#answer-creator-region"),
				collection: answer_collection,
				map_reference: map,
			});
			answer_creator.render();

			answer_display = new AnswerCollectionDisplayView({
				el: $("#answer-display-region"),
				collection: answer_collection,
				fetch_data: {
					q: JSON.stringify({
						"filters": [
							{
								name: "question_id",
								op: "==",
								val: QUESTION_ID,
							},
						]
					}),
				},
				generate_answer_view: generate_answer_view,
				empty_message: "No posts yet."
			});
			answer_display.render()

			answer_on_map = new AnswerCollectionMapView({
				el: $(map),
				collection: answer_collection,			
			});

		// End of ugly
		}

		// Create Question Representation Client-Side
		question = new Question({
			id: QUESTION_ID,
		});

		// Return a function that will build the map and invoke the custom callback after the map is created.
		build_map = GMapsHelper.get_func_to_build_map_and_call(ugly);

		question.fetch({
			success: function(model, response, options) {
				var address = model.attributes.location;
				geocoder = new google.maps.Geocoder();
				geocoder.geocode({address: address}, build_map);
			},
			error: function(model, xhr, options) {
				buildmap(null, null);             // Will build default map and call ugly.
			}
		});

		// question_stats = new GenericAdventureView({
		// 	el: $("#adventure-stats-region"),
		// 	model: adventure,
		// });
		// adventure_stats.render();


	$(document).ready(function() {

		// Technically, the map loading can fail since it depends on $("#map_canvas") being
		// loaded in DOM, but lets face it, Google Maps and Geocoder take a few ms.
		// Making everything wait until the DOM is ready is waasteful. Would be nice if there
		// were a way to make that one step wait on the DOM and hold things up only if
		// neccessary.

		//User View Generators
		// var generate_user_view = function(options) {
		// 	return new UserAdventurePageView(options);
		// };

		// adventure_companions_view = new UserCollectionDisplayView({
		// 	el: $("#companions-region").get(0),
		// 	collection: new UserCollection(),
		// 	fetch_data: {
		// 		filter_mode: 'adventure_companions',
		// 		adventure_id: ADVENTURE_ID,
		// 	},
		// 	generate_user_view: generate_user_view,
		// });
		// adventure_companions_view.render();

		

	// End of Document Ready Closure
	});
// End of requireJS Closure
});