<div class="row-fluid ">

	<div class="span11 well generic-question">

		<div class="row-fluid">

			<div class="span1 visit-author">
				<img class='img-rounded pull-left visit-owner' src="{{author.profile_img_url}}" height="50" width="50"></img>
				<strong><a href="" class='visit-owner'>{{author.username}}</a></strong>
			</div>

			<div class="span7">
				<h3><a class="visit-answers" href="#">{{title}}<a/></h3>
			</div>

		</div>


		<div class="row-fluid">

			<div class="span7">
				<p>{{text}}<p>

			</div>
			<div class="span5 pull-right">
				<div class="row-fluid">
					<div class="span6">
						<span class="badge badge-success"></span>&nbsp; {{pluralize postings_count 'Answer' 'Answers'}}<br>
					</div>
					<div class="span5 offset1">
						<button class="btn btn-primary visit-answers span12">Answers »</button>
					</div>
			</div>

		</div>

	</div>

</div>