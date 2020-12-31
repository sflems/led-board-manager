document.addEventListener('DOMContentLoaded', function() {
    // Use buttons to toggle between views
	$('#profile').click(function(){
		location.href = '/profile/' + $("#profile strong").text()
	});
    $('#index').click(function(){
		location.href = '/'
	});
    $('#following').click(function(){
		location.href = '/following'
	});
    $('#compose-form').submit(function(){
		compose_post();
		return false;
	});  
  
    let posts_list = document.querySelectorAll('.post');
    posts_list.forEach(post => {
	    post.querySelector('#post-content').addEventListener('click', function() {
		    post.querySelector('#post-content').classList.toggle("truncate");
	    });
	    post.querySelector('#like-form').onsubmit = () => {
	    	like_post(`${post.id}`);
			return false;
	    };
		if (post.querySelector('button.follow') != null) {
			post.querySelector('button.follow').addEventListener('click', function() {
				follow_user(this.dataset.user);
				return false;
			});
		};
		if (post.querySelector('small#edit-post') != null) {
			post.querySelector('small#edit-post').addEventListener('click', function() {
				edit_post(`${post.id}`);
				this.style.display = "none";
			});
		};
    });
})

function load_views(view) {
  
    if (view == 'all_posts') {  
		// Show the posts view and hide other views
		document.querySelector('#posts-view').style.display = 'block';
		document.querySelector('#compose-view').style.display = 'block';
		document.querySelector('#profile-view').style.display = 'none';
	// Get posts from all followed users and load them
	} else if (view == 'following') {  
		// Show the posts view and hide other views
		document.querySelector('#posts-view').style.display = 'block';
		document.querySelector('#compose-view').style.display = 'block';
		document.querySelector('#profile-view').style.display = 'none';
	} else if (view == 'profile') {  
		// Show the posts view and hide other views
		document.querySelector('#posts-view').style.display = 'none';
		document.querySelector('#compose-view').style.display = 'none';
		document.querySelector('#profile-view').style.display = 'block';
	}
}


function compose_post() {
	// Get form data
	content = document.querySelector('#compose-content').value;
	const csrftoken = Cookies.get('csrftoken');
			
	//Send Post request to postss URL with new post JSON data
	fetch('/posts/create', {
		headers: {'X-CSRFToken': csrftoken},
		method: 'POST',		
		body: JSON.stringify({
			content: content,
		}),
	})
	.then(response => response.json())
	.then(response => {
		// Print result
		console.log(response);
		if (response.error) {
			alert(response.error);
		} else if (window.location.href.indexOf("following") > -1) {
			document.querySelector('#message').innerHTML = `
				<div class="alert alert-success alert-dismissible fade show">
					<strong>Success!</strong> Post created.
					<button type="button" class="close" data-dismiss="alert" aria-label="Close">
						<span aria-hidden="true">&times;</span>
					</button>
				</div>  
			`;
		} else {
			document.querySelector('#compose-form').reset();
			document.querySelector('#posts-view').insertAdjacentHTML("afterbegin", response.html);
			document.querySelector('#message').innerHTML = `
				<div class="alert alert-success alert-dismissible fade show">
					<strong>Success!</strong> Post created.
					<button type="button" class="close" data-dismiss="alert" aria-label="Close">
						<span aria-hidden="true">&times;</span>
					</button>
				</div> 
			`;
			document.querySelector('#like-form').onsubmit = () => {
				like_post(response.post);
				return false;
			};			
		};
	});
}

// Likes a post
function like_post(post_id) {
	const csrftoken = Cookies.get('csrftoken');
	fetch(`/posts/${post_id}`, {
		headers: {'X-CSRFToken': csrftoken},
		method: 'PUT',
		body: JSON.stringify({
			like: true
		})
	})
	.then(response => response.json())
	.then(result => {
		// Print result
		console.log(result);
		//if liked not tru then make button = unlike
		if (result.liked != true) {
			$("#" + result.post_id).find("#like-post").text("Like Post");
			$("#" + result.post_id).find("#like-post").removeClass("btn-danger ml-n2");
			$("#" + result.post_id).find("#like-post").addClass("btn-primary");
			if (result.likes == 1) {
				$("#" + result.post_id).find(".like-count").text("1 Like");
			} else {
				$("#" + result.post_id).find(".like-count").text(result.likes + " Likes");
			};
			
			
		//else button = like
		} else {
			$("#" + result.post_id).find("#like-post").text("Unlike Post");
			$("#" + result.post_id).find("#like-post").removeClass("btn-primary");
			$("#" + result.post_id).find("#like-post").addClass("btn-danger ml-n2");
			if (result.likes == 1) {
				$("#" + result.post_id).find(".like-count").text("1 Like");
			} else {
				$("#" + result.post_id).find(".like-count").text(result.likes + " Likes");
			};
		};
	});
}

// Creates Text Area to edit a post
function edit_post(post_id) {
	post = document.getElementById(post_id);
	old_content = post.querySelector('#post-content').innerText;
	post.querySelector('.post p').outerHTML = `
		<form method="PUT" id="edit-form">
			<div class="form-group">
				<textarea id="compose-content" class="form-control mb-4" rows="5" cols="200">${old_content}</textarea>
			</div>
			<button id="submit" class="btn btn-sml btn-primary float-right">Submit Changes</button>
		</form>
	`;
	$('#edit-form').submit(function(){
		save_post(post_id);
		return false;
	});
}

// Saves an edited a post
function save_post(post_id) {
	content = document.getElementById(post_id).querySelector('#compose-content').value;
	const csrftoken = Cookies.get('csrftoken');
	
	fetch(`/posts/${post_id}`, {
		headers: {'X-CSRFToken': csrftoken},
		method: 'PUT',
		body: JSON.stringify({
			edit: true,
			content: content,
		})
	})
	.then(response => response.json())
	.then(result => {
		// Print result
		// TODO: Update post (or not), once response recieved.
		console.log(result);
		
		if (result.changed == true) {
			document.getElementById(post_id).querySelector('#edit-form').outerHTML = `
				<p id="post-content" class="col mb-2 lead truncate">${content}</p>
			`;
			document.getElementById(post_id).querySelector('small').style.display = "block";
			document.querySelector('#message').innerHTML = `
				<div class="alert alert-success alert-dismissible fade show">
					<strong>Success!</strong> ${result.message}.
					<button type="button" class="close" data-dismiss="alert" aria-label="Close">
						<span aria-hidden="true">&times;</span>
					</button>
				</div>  
			`;
		};
		
	});
}

// Follows a post
function follow_user(username) {
	const csrftoken = Cookies.get('csrftoken');
	fetch(`/profile/${username}`, {
		headers: {'X-CSRFToken': csrftoken},
		method: 'PUT',
		body: JSON.stringify({
			follow: true
		})
	})
	.then(response => response.json())
	.then(result => {
		// Print result
		console.log(result);
		buttons = document.querySelectorAll(`button[data-user="${username}"]`);
		//if followed not true then make button = unfollow
		if (result.followed != true) {
			buttons.forEach(button => {
				button.innerHTML = "Follow";
			});
			
		//else button = follow
		} else {
			buttons.forEach(button => {
				button.innerHTML = "Unfollow";
			});
		};
	});
}