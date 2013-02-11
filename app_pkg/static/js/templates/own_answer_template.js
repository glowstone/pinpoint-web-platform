<div class="row-fluid">

	<div class="span10 offset1 well own-answer">

		<div class="row-fluid own-answer">

			<div class="span2">
				<img class='img-rounded pull-left' src="{{author.profile_img_url}}" height="100" width="100"></img>
			</div>

			<div class="span8">
				<h3 class="pull-left"><a class="visit-profile" href="#">{{author.username}}<a/></h3>
			</div>

			<div class="span2">
				<button class="close answer-delete pull-right" title="Delete?">&times;</button>
			</div>

		</div>

		{{#if photo_url }}
		<div class="row-fluid user-image-div">
			<div class="span12">
				<img class="img-rounded answer-photo" src="{{photo_url}}"></img>
			</div>
		</div>
		{{/if}}


		<div class="row-fluid user-text-div">
			<div class="span10 offset2">
				<p class="lead">{{text}}<p>
			</div>

		</div>

	</div>

</div>