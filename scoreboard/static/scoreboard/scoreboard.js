document.addEventListener('DOMContentLoaded', function () {

	// Use buttons to toggle between views
	$('#index').click(function () {
		location.href = '/';
	});

	$('#settings_list').click(function () {
		location.href = `${this.dataset.url}`
	});

	$('#settings_create').click(function () {
		location.href = `${this.dataset.url}`
	});

	$('.game-time p').each(function () {
		this.innerText = new Date(this.dataset.datetime).toLocaleTimeString();
	});
	
	$('#settingsform > label:nth-child(7)').html("");

});