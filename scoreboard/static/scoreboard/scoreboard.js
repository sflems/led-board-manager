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

	$('.game-time p').each(function () {
		this.innerText = new Date(this.dataset.datetime).toLocaleTimeString();
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
				document.querySelector('#message').innerHTML = `
					<div class="alert alert-success alert-dismissible fade show">
						<strong>Success!</strong> Profile "${result.profile}" deleted. (Backup files may remain).
						<button type="button" class="close" data-dismiss="alert" aria-label="Close">
							<span aria-hidden="true">&times;</span>
						</button>
					</div>  
				`;
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

	$('button#reboot').click(function () {
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
						<strong>Error!</strong> Reboot unsuccessful!</strong>
						<button type="button" class="close" data-dismiss="alert" aria-label="Close">
							<span aria-hidden="true">&times;</span>
						</button>
					</div>  
				`;
			} else {
				document.querySelector('#message').innerHTML = `
					<div class="alert alert-success alert-dismissible fade show">
						<strong>Success!</strong> Raspberry Pi is rebooting...
						<button type="button" class="close" data-dismiss="alert" aria-label="Close">
							<span aria-hidden="true">&times;</span>
						</button>
					</div>  
				`;
			};
		});
	});
});