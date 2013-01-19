
require(['location'], function(location) {

	// Backbone.sync = function(method, model, success, error){
	// 	success();
	// }

	var Question = Backbone.Model.extend({
		defaults: {
			title: "Default Title",
			text: "Default Text",
			user: {
				fullname: 'Full Name',
				username: 'username',
				email: 'user@sample.com',
			},
			coords: {
				latitude: 42,
				longitude: -70,
			},
			date: 324243242,
		},
		initialize: function() {	
		},
	});

	var QuestionView = Backbone.View.extend({
		name: 'QuestionView',
		tagName: 'li',
		// Source of events to delegateEvents
		events: {
			'click span.swap': 'swap',
			'click span.delete': 'remove',
		},
		initialize: function(question_model) {
			// All QuestionView methods will have 'this' set to the QuestionView.
			_.bindAll(this, 'render', 'unrender', 'swap', 'remove');
			this.model = question_model   // Quesiton model instance provided at initialize.
		
			// Bind model events to corresponding view handlers
			this.model.bind('change', this.render);
			this.model.bind('remove', this.unrender);
			this.bind('all', this.all);
		},
		render: function() {
			$(this.el).html('<span>'+this.model.get('title')+this.model.get('text')+"</span>" + "<span class=swap>Swap</span><span class=delete>Delete</span>");
			return this;
		},
		unrender: function() {
			console.log('unrender');
			$(this.el).remove();
		},
		swap: function() {
			var swapped = {
				title: this.model.get('text'),
				text: this.model.get('title'),
			}
			this.model.set(swapped);
		},
		remove: function() {
			console.log("Calling remove");
			this.model.destroy();
		},
		all: function(event_name) {
			console.log(event_name);
		}
	});


	var QuestionCollection =  Backbone.Collection.extend({
		// A collection of Question model 'items'
		model: Question,
		url: '/api/questions',
		name: 'QuestionCollection',
	});


	var QuestionCollectionView = Backbone.View.extend({
		name: 'QuestionCollectionView',
		el: $('#play'),      // Attaches to existing element
		// Source of events to delegateEvents
		events: {
			'click button#add': 'addItem'
		},
		initialize: function(question_collection) {
			// All QuestionCollectionView methods will have 'this' set to the QuestionView.
			_.bindAll(this, 'render', 'addItem', 'appendItem')

			this.collection = question_collection;    //QuestionCollection instance provided during initialize.

			// Bind collection events to corresponding view handlers
			this.collection.on('add', this.appendItem);
			this.collection.on('remove', this.dependItem);
			this.collection.on('reset', this.reset);

			this.counter = 0;
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
		reset: function(models, options) {

			console.log('Reset was fired!');
			console.log(options);
			console.log(models);
			_(options.previousModels).each(function(item) {
				item.trigger('remove');
			});
			console.log("Here");
			console.log(this);

		},
		addItem: function() {
			console.log('addItem was called');
			this.counter++;
			var question = new Question();
			question.set({
				title: 'Title',
				count: this.counter,
			});
			this.collection.add(question);   // Add question to the question collection.
		},
		appendItem: function(item) {
			console.log("QuestionCollectionView appendItem called.");
			// Delegate rendering of item to the ItemView
			var question_view = new QuestionView(item);
			console.log(question_view);
			$('ul', this.el).append(question_view.render().el);
		},
		dependItem: function(item) {
			console.log("Got to dependItem");
			item.trigger('remove');
		}
	});

	//window.question = new Question({title: "my title!!", special: "my special attribute"});
	var question_collection = new QuestionCollection();
	var question_collection_view = new QuestionCollectionView(question_collection);
	question_collection_view.render();

	var question = new Question();
	console.log(question_collection);
	var question2 = new Question();
	var question3 = new Question();
	var question4 = new Question();
	var question5 = new Question();
	question_collection.add(question);
	question_collection.add(question2);
	question_collection.add(question3);
	question_collection.add(question4);
	question_collection.add(question5);


	var on_success = function(collection, response, options) {
		console.log('success');
		console.log(collection);
		console.log(response);
		console.log(options);
		console.log(question_collection)
	}

	var on_failure = function(collection, xhr, options) {
		console.log('Failure')
		console.log(collection);
		console.log(xhr);
		console.log(options);
	}

	var jqxhr = question_collection.fetch({
		success: on_success, 
		error: on_failure,
	});
	console.log(question_collection);
	console.log(jqxhr);


	


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