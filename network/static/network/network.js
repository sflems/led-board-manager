document.addEventListener('DOMContentLoaded', function() {
    // Use buttons to toggle between views
    document.querySelector('#index').addEventListener('click', () => location.href='/');
    document.querySelector('#following').addEventListener('click', () => location.href='/views/following');
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
	let content = document.querySelector('#compose-content').value;
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
		} else {
			document.querySelector('#compose-form').reset();
			document.querySelector('#posts-view').insertAdjacentHTML("afterbegin", response.html);
			document.querySelector('#like-form').onsubmit = () => {
				like_post(response.post);
				return false;
			};
		};
	})
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
		location.reload();
	});
}