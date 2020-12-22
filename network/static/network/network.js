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
    document.querySelector('#compose-form').onsubmit = () => {
		compose_post();
		return false;
	};  
  
    let posts_list = document.querySelectorAll('.post');
    posts_list.forEach(post => {
	    post.querySelector('#post-content').addEventListener('click', function() {
		    post.querySelector('#post-content').classList.toggle("truncate");
	    });
	    post.querySelector('#like-form').onsubmit = () => {
	    	like_post(`${post.id}`);
			return false;
	    };
    });

  // TODO: Implement Profiles View

  // By default load all posts view
  // load_views('all_posts');
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
				<div class="alert alert-success">
					<strong>Success!</strong> Post successfully created.
				</div> 
			`;
		} else {
			document.querySelector('#compose-form').reset();
			document.querySelector('#posts-view').insertAdjacentHTML("afterbegin", response.html);
			document.querySelector('#message').innerHTML = `
				<div class="alert alert-success">
					<strong>Success!</strong> Post successfully created.
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
			changed: true
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