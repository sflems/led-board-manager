document.addEventListener('DOMContentLoaded', function() {
    // Use buttons to toggle between views
    $('#index').click(function(){
		location.href = '/';
	});

    $('btn#following').click(function(){
		location.href = '/settings'
	});

	$('.game-time p').each(function(){
		this.innerText = new Date(this.dataset.datetime).toLocaleTimeString();
	});

});