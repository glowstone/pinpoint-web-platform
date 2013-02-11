<div class='pull-left span3 visit-profile well'>
	<div class='row-fluid'>

		<div class='span6'>
			<a href="#" class="lead visit-profile-link">{{username}}</a>
			<br>
			<span class="pull-left counter"><span class='badge badge-important'>{{ questions.length }}</span> {{pluralize questions.length 'Question' 'Questions'}}</span>
			<br>
			<span class="pull-left counter"><span class='badge badge-info'>{{ answers.length }}</span> {{pluralize answers.length 'Answer' 'Answers'}}</span>
			<br>
		</div>

		<div class='span5 offset1 visit-profile-img'>
			<img class='img-rounded' src='{{profile_img_url}}' height='50' width='50'></img>
		</div>

	</div>
</div>