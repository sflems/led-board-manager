document.addEventListener('DOMContentLoaded', function() {
    // Use buttons to toggle between views
    $('#index').click(function(){
		location.href = '/';
	});
    
    // Fetches daily game JSON data from NHL.com
    fetch_schedule();
});

// Function to fetch daily game JSON data from NHL.com
function fetch_schedule() {
    // Send a GET request to the URL
    fetch('https://statsapi.web.nhl.com/api/v1/schedule')
    // Put response into json form
    .then(response => response.json())
    .then(data => {
        console.log(data);        
        const dates = data.dates;

        dates.forEach(date => {
            const games = date.games;

            games.forEach(game => {
                document.getElementById('daily-schedule').style.display = "block";
                document.getElementById('daily-schedule').insertAdjacentHTML("beforeend", `
                    <div id="game_${game.gamePk}" class="row justify-content-center">
                        <div class="game-time col-3 text-center">
                            <p class="">${(new Date(game.gameDate).toTimeString())}</p>
                        </div>                
                        <div class="teams col-6 text-center">
                            <p>${game.teams.away.team.name} vs ${game.teams.home.team.name}</p>
                        </div>
                        <div class="status col-3 text-center">
                            <strong>${game.status.detailedState}</strong>
                            <p>${game.teams.away.score} vs ${game.teams.home.score}</p>    
                        </div>
                    </div>
                `);
                
            });
        });
        
	});
}