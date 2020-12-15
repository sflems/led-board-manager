document.addEventListener('DOMContentLoaded', function() {
  // Use buttons to toggle between views
  document.querySelector('#index').addEventListener('click', () => load_views('all_posts'));
  
  // By default all posts
  load_posts('all_posts');
});

function load_views(view) {
  
  // Show the posts view and hide other views
  document.querySelector('#posts-view').style.display = 'block';
  document.querySelector('#profile-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#posts-view').prepend = `
	<h3>Network Posts</h3>
	<div class="posts-list"></div>
  `;
  
  // Get all posts and load them
  if (view == 'all_posts') {
		
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
	if (posts.length != 0) {
		posts.forEach(post => {
			
			const element = document.createElement('div');
			element.innerHTML = `
				<div class="col-3-sm">${post.title}</div>
				<div class="col-6-sm">${post.content}</div>
				<div class="col-3-sm">${post.author}</div>
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