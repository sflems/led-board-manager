document.addEventListener('DOMContentLoaded', function() {
  // Use buttons to toggle between views
  document.querySelector('#index').addEventListener('click', () => load_views('all_posts'));
  document.querySelector('#following').addEventListener('click', () => load_views('following'));
  
  // By default load all posts view
  load_views('all_posts');
});

function load_views(view) {
  
  // Show the posts view and hide other views
  document.querySelector('#posts-view').style.display = 'block';
  document.querySelector('#profile-view').style.display = 'none';


  
  // Get all posts and load them
  if (view == 'all_posts') {
	  
		// Show the view name
		document.querySelector('#posts-view').innerHTML = `
			<h3>Network - Posts</h3>
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
			<h3>Following List - Recent Posts</h3>
			<div class="posts-list"></div>
		`;
		
		fetch('/views/following')
		.then(response => response.json())
		.then(posts => {
			// Print posts
			console.log(posts);
			
			// Load all posts
			load_posts(posts);
		});
  };
}

// Loads all posts
function load_posts(posts) {
	if (posts.length > 0) {
		posts.forEach(post => {
			const element = document.createElement('div');
			element.innerHTML = `
				<div class="col-3">${post.title}</div>
				<div class="col-6">${post.content}</div>
				<div class="col-3">${post.author}</div>
			`;
			element.classList.add("row","posts");
			document.querySelector('.posts-list').append(element);		
		});
	} else {
		const element = document.createElement('div');
		element.innerHTML = `
			<div class="col">No posts to display.</div>
		`;
		element.classList.add("row","posts");
		document.querySelector('.posts-list').append(element);
	}
}