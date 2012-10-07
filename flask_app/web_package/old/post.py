

class Post(object):
	def __init__(self, create_time, ttl_time, delete_time, user_id, abstract_location_id):
		self.create_time = create_time
		self.ttl_time = ttl_time
		self.delete_time = delete_time
		self.user_id = user_id
		self.abstract_location_id = abstract_location_id

class Query(Post):
	def __init__(self, title, text):
		self.title = title
		self.text = text


class Event(Post):
	def __init__(self, title, text, start_time, end_time):
		self.title = title
		self.text = text
		self.start_time = start_time
		self.end_time = end_time

class Challenge(Post):
	def __init__(self, title, challenge_text):
		self.title = title


class Alert(Post):
	def __init__(self, alert_msg);
		self.alert_msg = alert_msg