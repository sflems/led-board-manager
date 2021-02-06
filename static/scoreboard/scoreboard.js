document.addEventListener('DOMContentLoaded', function () {

	// Use buttons to toggle between views
	$('#index').click(function () {
		location.href = '/';
	});

	$('#profiles_list').click(function () {
		location.href = `${this.dataset.url}`
	});

	$('#settings_create').click(function () {
		location.href = `${this.dataset.url}`
	});

	$('#admin').click(function () {
		location.href = `${this.dataset.url}`
	});

	$('.game-time').each(function () {
		this.innerText = new Date(this.dataset.datetime).toLocaleTimeString();
	});

	// Auto-collapses json forms for easier viewing on load. The "collapsed" option does not work!
	const collapse_buttons = document.querySelectorAll('button.json-editor-btn-collapse');
	collapse_buttons.forEach(element => {
		if (element !== collapse_buttons[0]) {
			element.click();	
		};
	});


	// Add's JSON config to modal when profile is clicked on Profile Page.
	// TODO: Allow users to edit and save form here. MUST BE VALIDATED!
	$(document).on("click", ".modal-link", function () {
		var data = this.dataset.json
		$("#prettyJSON").text(data);
   	});

	$('button#activate').click(function () {
		const csrftoken = Cookies.get('csrftoken');
		fetch(`${this.dataset.editurl}`, {
			headers: {'X-CSRFToken': csrftoken},
			method: 'PUT',
			body: JSON.stringify({
				"activated": true
			})
		})
		.then(response => response.json())
		.then(result => {
			console.log(result);
			if (result.activated != true) {
				document.querySelector('#message').innerHTML = `
					<div class="alert alert-danger alert-dismissible fade show">
						<strong>Error!</strong> Profile activation unsuccessful.
						<button type="button" class="close" data-dismiss="alert" aria-label="Close">
							<span aria-hidden="true">&times;</span>
						</button>
					</div>  
				`;
			} else {
				location.reload();
			};			
		});
	});

	$('button#backup').click(function () {
		const csrftoken = Cookies.get('csrftoken');
		fetch(`${this.dataset.editurl}`, {
			headers: {'X-CSRFToken': csrftoken},
			method: 'PUT',
			body: JSON.stringify({
				"backup": true
			})
		})
		.then(response => response.json())
		.then(result => {
			console.log(result);
			if (result.backup != true) {
				document.querySelector('#message').innerHTML = `
					<div class="alert alert-danger alert-dismissible fade show">
						<strong>Error!</strong> File save unsuccessful! Attempted to save file as ${result.path}
						<button type="button" class="close" data-dismiss="alert" aria-label="Close">
							<span aria-hidden="true">&times;</span>
						</button>
					</div>  
				`;
			} else {
				document.querySelector('#message').innerHTML = `
					<div class="alert alert-success alert-dismissible fade show">
						<strong>Success!</strong> File saved to ${result.path}
						<button type="button" class="close" data-dismiss="alert" aria-label="Close">
							<span aria-hidden="true">&times;</span>
						</button>
					</div>  
				`;
			};			
		});
	});
	$('button#delete').click(function () {
		const csrftoken = Cookies.get('csrftoken');
		fetch(`${this.dataset.editurl}`, {
			headers: {'X-CSRFToken': csrftoken},
			method: 'PUT',
			body: JSON.stringify({
				"delete": true
			})
		})
		.then(response => response.json())
		.then(result => {
			console.log(result);
			if (result.delete != true) {
				document.querySelector('#message').innerHTML = `
					<div class="alert alert-danger alert-dismissible fade show">
						<strong>Error!</strong> Profile "${result.profile}" deleted <strong>unsuccessfully!</strong>
						<button type="button" class="close" data-dismiss="alert" aria-label="Close">
							<span aria-hidden="true">&times;</span>
						</button>
					</div>  
				`;
			} else {
				location.reload();
			};			
		});
	});

	// Adds profile/id path to data-editurl attribute on modal delete confirmation button.
	$('button#deleteModalbutton').click(function () {
		$('button#delete').attr('data-editurl', this.dataset.editurl)
	});

	$('button#edit').click(function () {
		location.href = `${this.dataset.editurl}`
	});

	$('button#stopserver').click(function () {
		document.querySelector('#message').innerHTML = `
				<div class="alert alert-success alert-dismissible fade show">
					<strong>Success!</strong> Web interface will shutdown in 5 seconds...
					<button type="button" class="close" data-dismiss="alert" aria-label="Close">
						<span aria-hidden="true">&times;</span>
					</button>
				</div>  
		`;
		const csrftoken = Cookies.get('csrftoken');
		fetch(`${this.dataset.url}`, {
			headers: {'X-CSRFToken': csrftoken},
			method: 'PUT',
			body: JSON.stringify({
				"stopserver": true
			})
		})
		.then(response => response.json())
		.then(result => {
			console.log(result);
			if (result.stopserver != true) {
				document.querySelector('#message').innerHTML = `
					<div class="alert alert-danger alert-dismissible fade show">
						<strong>Error!</strong> Server shutdown unsuccessful.
						<button type="button" class="close" data-dismiss="alert" aria-label="Close">
							<span aria-hidden="true">&times;</span>
						</button>
					</div>  
				`;
				// make this the no response. not result.
			};
		})
	});


	$('button#reboot').click(function () {
		document.querySelector('#message').innerHTML = `
			<div class="alert alert-success alert-dismissible fade show">
				<strong>Success!</strong> Rebooting in 5 seconds...
				<button type="button" class="close" data-dismiss="alert" aria-label="Close">
					<span aria-hidden="true">&times;</span>
				</button>
			</div>  
		`;
		const csrftoken = Cookies.get('csrftoken');
		fetch(`${this.dataset.url}`, {
			headers: {'X-CSRFToken': csrftoken},
			method: 'PUT',
			body: JSON.stringify({
				"reboot": true
			})
		})
		.then(response => response.json())
		.then(result => {
			console.log(result);
			if (result.reboot != true) {
				document.querySelector('#message').innerHTML = `
					<div class="alert alert-danger alert-dismissible fade show">
						<strong>Error!</strong> Reboot unsuccessful.
						<button type="button" class="close" data-dismiss="alert" aria-label="Close">
							<span aria-hidden="true">&times;</span>
						</button>
					</div>  
				`;
			};
		});
	});

	$('button#shutdown').click(function () {
		document.querySelector('#message').innerHTML = `
					<div class="alert alert-success alert-dismissible fade show">
						<strong>Success!</strong> Shutdown initiated.
						<button type="button" class="close" data-dismiss="alert" aria-label="Close">
							<span aria-hidden="true">&times;</span>
						</button>
					</div>  
				`;
		const csrftoken = Cookies.get('csrftoken');
		fetch(`${this.dataset.url}`, {
			headers: {'X-CSRFToken': csrftoken},
			method: 'PUT',
			body: JSON.stringify({
				"shutdown": true
			})
		})
		.then(response => response.json())
		.then(result => {
			console.log(result);
			if (result.shutdown != true) {
				document.querySelector('#message').innerHTML = `
					<div class="alert alert-danger alert-dismissible fade show">
						<strong>Error!</strong> Shutdown unsuccessful.
						<button type="button" class="close" data-dismiss="alert" aria-label="Close">
							<span aria-hidden="true">&times;</span>
						</button>
					</div>  
				`;
			};
		});
	});

});