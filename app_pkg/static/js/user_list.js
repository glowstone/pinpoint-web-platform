require.config({
	paths: {
		'handlebars': 'library/handlebars',
		'text': 'library/require-plugins/text',
	},
	shim: {
		'handlebars': {
			exports: 'Handlebars',
		}
	},
	config: {
        text: {
            useXhr: function (url, protocol, hostname, port) {
                return true;
            }
        }
    }
});
require([
	'communication', 
	'models/user', 
	'views/user_view',
	'collections/user_collection',
	'views/user_collection_display_view',
	], 
	function(communication, User, UserView, UserCollection, UserCollectionDisplayView) {
		
		$(document).ready(function() {

			$("li.users-tab").addClass("active");

			// User View Generators
			var generate_user_view = function(options) {
				return new UserView(options);
			};

			all_users_view = new UserCollectionDisplayView({
				el: $("#all-users-pane").get(0),
				collection: new UserCollection(),
				generate_user_view: generate_user_view,
				empty_message: ""       // Don't show a message about there being no other users. 
			});
			all_users_view.render();
			

		// End of Document Ready Closure
		});

	// End of requireJS function Closure
	}
);