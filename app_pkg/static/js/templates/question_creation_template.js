
<div class="row-fluid">

	<div class="span8">
		<form id='question-creation-form' action='/should_not_be_submitted'>
			<input id='question-create-title' class='span12' type='text' name='title' placeholder="What is your question?"><br>
			<textarea id='question-create-text' class="span12" type='text' name='text' placeholder="Type your question text here." rows="3"></textarea><br>	
		</form>
	</div>

	<div class="span4">
		<button id="location-chooser" class="btn btn-info">Location (required)</button>
		<strong>Latitude:</strong><span id="latitude-indicator">None</span>
		<strong>Longitude:</strong><span id="longitude-indicator">None</span>
	</div>

</div>

<div class="row-fluid posting-bar">
	<button id="submit-posting" class='btn btn-success span12'>Post</button>
</div>
