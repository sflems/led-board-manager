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

	// AJAX Calls for Footer Cards here
	$('div#profile-card').ready(function () {
		const element = document.getElementById("profile-card");
		fetch(`${element.dataset.url}`)
		.then(response => response.json())
		.then(result => {
			console.log(result);
			$('div#profile-card h5.card-title').text(result.profile.name);
			$('div#profile-card div.card-text').html(`
				<p class="m-0">Favourite Team(s): ${JSON.stringify(result.profile.config.preferences.teams,null," ").replace("[","").replace("]","").replace(/["]+/g,"")}</p>
				<p class="m-0">Live Mode: ${result.profile.config.live_mode}</p>
				<p class="m-0">Debug: ${result.profile.config.debug}</p>
				<p class="m-0">Log Level: ${result.profile.config.loglevel}</p>
				<p class="m-0 status"></p>
			`);
			if (result.scoreboard_status != true) {
				$('p.status').html(`
					Scoreboard Status: Supervisor Process Not Found <img src="/static/scoreboard/x-square-fill.svg" class="x-square-fill" width="24" height="24">
				`);
			} else {
				$('p.status').html(`
					Scoreboard Status: Running <img src="/static/scoreboard/check-square-fill.svg" class="x-square-fill" width="24" height="24">
				`);
			};
		})
		.catch(error => {
			console.log(error);
			$('div#profile-card h5.card-title').text("ERROR");
			$('div#profile-card div.card-text').html(`
				<p class="mt-n2">No active profile returned.</p>
			`);
		});
	});

	$('div#monitor-card').ready(function () {
		sysinfo();
		setInterval(sysinfo, 10000);
	});

	// Auto-collapses json forms for easier viewing on load. The "collapsed" option does not work!
	$(document).ready(function(){
			collapse_forms();
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
						<strong>Error!</strong> <small>Profile activation unsuccessful.</small>
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
						<strong>Error!</strong> <small>File save unsuccessful! Attempted to save file as ${result.path}</small>
						<button type="button" class="close" data-dismiss="alert" aria-label="Close">
							<span aria-hidden="true">&times;</span>
						</button>
					</div>  
				`;
			} else {
				document.querySelector('#message').innerHTML = `
					<div class="alert alert-success alert-dismissible fade show">
						<strong>Success!</strong> <small>File saved to ${result.path}</small>
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
						<strong>Error!</strong> <small>Profile "${result.profile}" deleted <strong>unsuccessfully!</strong></small>
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
					<strong>Success!</strong> <small>Web interface shutdown commencing...</small>
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
						<strong>Error!</strong> <small>Server shutdown unsuccessful.</small>
						<button type="button" class="close" data-dismiss="alert" aria-label="Close">
							<span aria-hidden="true">&times;</span>
						</button>
					</div>  
				`;
			};
		})
	});


	$('button#reboot').click(function () {
		document.querySelector('#message').innerHTML = `
			<div class="alert alert-success alert-dismissible fade show">
				<strong>Success!</strong> <small>Rebooting in 5 seconds...</small>
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
						<strong>Error!</strong> <small>Reboot unsuccessful.</small>
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
						<strong>Success!</strong> <small>Shutdown initiated.</small>
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
						<strong>Error!</strong> <small>Shutdown unsuccessful.</small>
						<button type="button" class="close" data-dismiss="alert" aria-label="Close">
							<span aria-hidden="true">&times;</span>
						</button>
					</div>  
				`;
			};
		});
	});


});

function sysinfo() {
	function handleErrors(response) {
		if (!response.ok) {
			throw Error(response.statusText);
		}
		return response;
	};
	const element = document.getElementById("monitor-card");
	fetch(`${element.dataset.url}`)
	.then(handleErrors)
	.then(response => response.json())
	.then(result => {
		console.log(result);
		$('div#monitor-card div.card-text').html(`
		<div class="col-lg-4">
			<h5>CPU</h5>
			<p class="resource mt-n1">${result.cpu} @ ${result.cputemp.replace("temp=","")}</p>
		</div>
		<div class="col-lg-4">
			<h5>Memory</h5>
			<p class="resource mt-n1">${result.memory}</p>
		</div>
		<div class="col-lg-4">
			<h5>Disk</h5>
			<p class="resource mt-n1 mb-0">${result.disk}</p>
		</div>
		`);
	})
	.catch(error => {
		console.log(error);
		$('div#monitor-card div.card-text').html(`
		<div class="col">
			<h5>ERROR</h5>
			<p class="resource mt-n1">No system info returned.</p>
		</div>
		`);
	});
};

function collapse_forms() {
	const collapse_buttons = document.querySelectorAll('button.json-editor-btn-collapse');
		collapse_buttons.forEach(element => {
			if (element !== collapse_buttons[0] && element !== collapse_buttons[1] && element !== collapse_buttons[2]) {
				element.click();	
			};
		});
};