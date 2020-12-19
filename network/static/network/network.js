document.addEventListener('DOMContentLoaded', function() {
  // Use buttons to toggle between views
  document.querySelector('#index').addEventListener('click', () => load_views('all_posts'));
  document.querySelector('#following').addEventListener('click', () => load_views('following'));
  document.querySelector('#compose-form').onsubmit = compose_post;
  
  let posts_list = document.querySelectorAll('#post');
  posts_list.forEach(post => {
	  post.addEventListener('click', function() {
		  post.querySelector('#post-content').classList.toggle("truncate");
	  });
  });

  // By default load all posts view
  // load_views('all_posts');
});

function load_views(view) {
  
  // Show the posts view and hide other views
  document.querySelector('#posts-view').style.display = 'block';
  document.querySelector('#profile-view').style.display = 'none';


  
  // Get all posts and load them
  if (view == 'all_posts') {
	  
		// Show the view name
		document.querySelector('#posts-view').innerHTML = `
			<div class="posts-list"></div>
		`;
		
		fetch('/views/all_posts')
		.then(response => response.json())
		.then(posts => {
			// Print posts
			console.log(posts);
			
			// Load all posts
			load_posts(posts);
		});
  };
  
  // Get posts from all followed users and load them
  if (view == 'following') {
	  
		// Show the view name
		document.querySelector('#posts-view').innerHTML = `
			<div class="posts-list"></div>
		`;
		
		fetch('/views/following')
		.then(response => response.json())
		.then(posts => {
			// If error thrown(response status is not in the range 200-299 inclusive), display error
			if (Response.ok !== true) {
				console.log(posts.error);
				const element = document.createElement('div');
				element.innerHTML = `
					<div class="col">${posts.error}</div>
				`;
				element.classList.add("row","posts");
				document.querySelector('.posts-list').append(element);
			// Otherwise load the posts
			} else {
				// Print posts
				console.log(posts);
				
				// Load all posts
				load_posts(posts);
			}
		});
  };

  // TODO: Implement Profiles View

}

// Loads all posts
function load_posts(posts) {
	if (posts.length > 0) {
		posts.forEach(post => {
			const element = document.createElement('div');
			element.innerHTML = `
				<div id="post" class="col">
					<p id="post-content" class="mb-2 lead truncate">${ post.content.replace(/\n/g, "<br >") }</p>
					<h4 class="mb-2 font-weight-light text-right">- ${ post.author }</h4>
					<p class="mb-0 text-muted text-right">${ post.timestamp }</p>
				</div>
			`;
			element.classList.add("row", "no-gutters", "border", "rounded", "overflow-hidden", "mb-4", "p-4", "shadow-sm", "max-h-250", "position-relative",);
			element.addEventListener('click', function() {
				element.querySelector('#post-content').classList.toggle("truncate");
	  });
			document.querySelector('.posts-list').append(element);		
		});
	} else {
		const element = document.createElement('div');
		element.innerHTML = `
			<div class="col">No posts to display.</div>
		`;
		element.classList.add("row","no-gutters", "border", "rounded", "overflow-hidden", "mb-4", "p-4", "shadow-sm", "h-250", "position-relative",);
		document.querySelector('.posts-list').append(element);
	}
}

	//Submits new post form
function compose_post() {
	// Get form data
	let content = document.querySelector('#compose-content').value;
			
	//Send Post request to emails URL with new email JSON data
	fetch('/posts/create', {
		method: 'POST',
		body: JSON.stringify({
			content: content,
		})
	})
	.then(response => response.json())
	.then(result => {
		// Print result
		console.log(result);
		load_views('all_posts');
	});
	
	return false;	
}