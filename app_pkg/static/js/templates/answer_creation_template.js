
<div class="row-fluid">

	<div class="span8">
		<form id='answer-creation-form' action='/should_not_be_submitted'>
			<textarea id='answer-create-text' class="span12" type='text' name='text' placeholder="Contribute your answer here." rows="3"></textarea><br>	
		</form>
	</div>

	<div class="span4">
		<button id="location-chooser" class="btn btn-info">Location (required)</button>
		<strong>Latitude:</strong><span id="latitude-indicator">None</span>
		<strong>Longitude:</strong><span id="longitude-indicator">None</span>
	</div>

</div>

<div class="row-fluid answer-bar">
	<button id="submit-answer" class='btn btn-success span12'>Post</button>
</div>
