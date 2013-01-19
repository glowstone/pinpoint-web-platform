
require(['location'], function(location) {



	var Question = Backbone.Model.extend({
		defaults: {
			title: "Default Title",
			text: "Default Text",
			answer_count: 0,
		},
		get_answer_count: function() {
			return this.answer_count;
		},
		initialize: function() {
			this.on('click', function() {
				alert('Clicked ' + this.count);
			})
		}
	});


	var QuestionList = Backbone.Collection.extend({
		model: Question,
		initialize: function() {
		},
	});


	var QuestionListView = Backbone.View.extend({
		el: $('#play'),
		//Source of events to delegateEvents
		events: {
			'click button#add': 'addItem'
		},
		initialize: function() {
			_.bindAll(this, 'render', 'addItem', 'appendItem')
			this.collection = new QuestionList();
			// Bind collection's add event to the views appendItem method
			this.collection.on('add', this.appendItem);
			//_.bindAll(this, 'render');

			this.counter = 0;
			//Self-rendering view
			this.render()
		},
		render: function() {
			var self = this;
			$(this.el).append("<button id='add'>Add a Question</button><button>Download Questions</button>");
			$(this.el).append("<ul></ul>");
			_(this.collection.models).each(function(item) {
				self.appendItem(item);
			}, this);
			return this;
		},
		addItem: function() {
			console.log('addItem was called');
			this.counter++;
			var question = new Question();
			question.set({
				title: 'Title',
				count: this.counter,
			});
			this.collection.add(question);   //add question to collection. View is updated via event 'add'.
		},
		appendItem: function(item) {
			$('ul', this.el).append("<li>" + item.get('title') + ":" + item.get('text') + item.get('count') + "</li>");
		}
	});

	//window.question = new Question({title: "my title!!", special: "my special attribute"});
	var body = new QuestionListView();

	// console.log(question.get('title'));
	// console.log(question.attributes);
	// console.log(question.get('id'));
	// console.log(question.get('cid'));
	// console.log('Reached the end');
	// console.log(question.toJSON());


	// sidebar.on('change:color', function(model, color) {
	//   $('#sidebar').css({background: color});
	// });

	// sidebar.set({color: 'white'});

	// sidebar.promptColor();


	// var google_static_maps_url = "http://maps.googleapis.com/maps/api/staticmap"
	// var key = GOOGLE_API_KEY

	
	// var success_action = function(latitude, longitude) {
	// 	var img = new Image();
	// 	var source = google_static_maps_url + "?center=" + latitude + "," + longitude  + "&zoom=13&size=940x400&sensor=true&scale=1" + "&key=" + key
	// 	img.src = source;
	// 	//img.height=400;
	// 	//img.width=950;
	// 	$(img).addClass("span12");
	// 	img.class="span4"
	// 	$("#map_region").prepend(img);
		
	// 	console.log(source);
	// 	console.log(latitude);
	// 	console.log(longitude);
	// 	console.log("Success");
	// }
	
	// // No error_action, because default coordinates will be used if errors occur.
	// location.geoplugin_coordinates(success_action);
	

	$(document).ready(function() {

		$("#signup_btn").click(function() {
			window.location = "/signup";
		});

		$("#login_btn").click(function() {
			window.location = "/login";
		});

	

	// End of Document Ready Closure
	});
// End of requireJS Closure
});