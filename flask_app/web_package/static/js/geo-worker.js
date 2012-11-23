
self.addEventListener('message', function(e) {
	self.postMessage('Hello?');
}, false);

var xhr = new XMLHttpRequest();
xhr.open('GET', '/api/user/set_location.json', true);
	xhr.send({'lat': 234,
			  'long': 345
			  });
	
	
