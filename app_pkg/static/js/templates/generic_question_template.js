<div class="row-fluid span11">

	<div class="span12 well question-stats">

		<div class="row-fluid">
			<div class="span12">
				<h3>{{title}}</h3>
			</div>
		</div>

		<div class="row-fluid">
			<div class="span12">
				<p class="small">{{text}}<p>
			</div>
			
		</div>

		<div class="row-fluid">
			<div class="span6">
				<span><strong>Author: </strong></span><a class="visit-author" href="">{{author.username}}</a><br>
				<span class="badge badge-success">{{answers.length}}</span>&nbsp; {{pluralize answers.length 'Answer' 'Answers'}}<br>
			</div>

			<div class="span6 pull-right">
				<strong class="pull-right">{{location}}</strong><br>
			</div>
		</div>

	</div>

</div>
