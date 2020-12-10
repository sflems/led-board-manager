document.addEventListener('DOMContentLoaded', function() {
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  
  // By default load the inbox
  load_mailbox('inbox');
});


function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  document.querySelector('#compose-form').onsubmit = send_email;
}

function reply(email) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = `${email.sender}`;
  
  // Check if subject already contains Re:
  if (email.subject.toLowerCase().startsWith("re:") != true) {
	  document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
  } else {
	  document.querySelector('#compose-subject').value = `${email.subject}`; 
  }
  
  document.querySelector('#compose-body').value = '\n' + `\"On ${email.timestamp}, ${email.sender} wrote:\n\n ${email.body}\"` + '\n';
  
  document.querySelector('#compose-form').onsubmit = send_email;
}

function send_email() {
	// Get form data
	let recipients = document.querySelector('#compose-recipients').value;
	let subject = document.querySelector('#compose-subject').value;
	let body = document.querySelector('#compose-body').value;
			
	//Send Post request to emails URL with new email JSON data
	fetch('/emails', {
		method: 'POST',
		body: JSON.stringify({
			recipients: recipients,
			subject: subject,
			body: body,
		})
	})
	.then(response => response.json())
	.then(result => {
		// Print result
		console.log(result);
	});

	load_mailbox('inbox');
	return false;
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `
	<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>
	<div class="emails-list"></div>
  `;
  
  // Inbox mail
  if (mailbox == 'inbox') {
		
		fetch('/emails/inbox')
		.then(response => response.json())
		.then(emails => {
			// Print emails
			console.log(emails);
			
			// Load all emails
			load_mail(emails);
		});
  };
  
  // Sent mail
  if (mailbox == 'sent') {
		
		fetch('/emails/sent')
		.then(response => response.json())
		.then(emails => {
			// Print emails
			console.log(emails);
			
			// ... do something else with emails ...
			if (emails.length != 0) {
				emails.forEach(email => {
					const element = document.createElement('div');
					element.innerHTML = `
						<div id="sender" class="col-3">${email.recipients}</div>
						<div class="col-6">${email.subject}</div>
						<div class="col-3">${email.timestamp}</div>
					`;
					element.classList.add("row","emails");
					element.addEventListener('click', function() {
						//Open individual emails
						load_email(email);
					});

					document.querySelector('.emails-list').append(element);		
				});
			} else {
				const element = document.createElement('div');
				element.innerHTML = `
					<div class="col">No mail to display.</div>
				`;
				element.classList.add("row","emails");
				document.querySelector('.emails-list').append(element);
			}
		});
		
  };
  
  // Archived mail
  if (mailbox == 'archive') {
		
		fetch('/emails/archive')
		.then(response => response.json())
		.then(emails => {
			// Print emails
			console.log(emails);
			
			// Load archived emails if they exist, else return empty
			load_mail(emails);		
		});
		
  };
}

// Loads all emails
function load_mail(emails) {
	if (emails.length != 0) {
		emails.forEach(email => {
			const element = document.createElement('div');
			element.innerHTML = `
				<div id="sender" class="col-3">${email.sender}</div>
				<div class="col-6">${email.subject}</div>
				<div class="col-3">${email.timestamp}</div>
			`;
			element.classList.add("row","emails");
			if (email.read === false) {element.classList.add("read-mail")};
			element.addEventListener('click', function() {
				//Open individual emails and mark them as read
				mark_read(email);
				load_email(email);
			});
			if (email.read === true) {
				//Change style for Read email here
				element.classList.add("read-email");
			};
			document.querySelector('.emails-list').append(element);		
		});
	} else {
		const element = document.createElement('div');
		element.innerHTML = `
			<div class="col">No mail to display.</div>
		`;
		element.classList.add("row","emails");
		document.querySelector('.emails-list').append(element);
	}
}

// Loads a single email
function load_email(email) {
	fetch(`/emails/${email.id}`)
	.then(response => response.json())
	.then(email => {
		// Print email
		console.log(email);

		// ... do something else with email ...
		const element = document.createElement('div');
		if (email.archived != true) {
			element.innerHTML = `<button class="btn btn-sm btn-outline-primary" id="archive-mail">Archive</button>`;
			document.querySelector('#emails-view').innerHTML = element.innerHTML;
			document.querySelector('#archive-mail').addEventListener('click', () => archive(email));
		} else {
			element.innerHTML = `<button class="btn btn-sm btn-outline-primary" id="archive-remove">Unarchive</button>`;
			document.querySelector('#emails-view').innerHTML = element.innerHTML;
			document.querySelector('#archive-remove').addEventListener('click', () => remove_archive(email));
		};
		
		var display_body = email.body.replace(/\n/g, "<br >");
		
		document.querySelector('#emails-view').insertAdjacentHTML('beforeend', `
			<button class="btn btn-sm btn-outline-primary" id="reply">Reply</button>
			<div class="row"><div class="col from">From: ${email.sender}</div></div>
			<div class="row"><div class="col to">To: ${email.recipients}</div></div>
			<div class="row"><div class="col subject">Subject: ${email.subject}</div></div>
			<div class="row"><div class="col from">Date: ${email.timestamp}</div></div>
			<div class="row"><div class="col message">Message:<br><br>${display_body}</div></div>
		`);
		document.querySelector('#reply').addEventListener('click', () => reply(email));
	});
}

// Marks email by id as read
function mark_read(email) {
	if (email.read != true) {
		fetch(`/emails/${email.id}`, {
			method: 'PUT',
			body: JSON.stringify({
				read: true
			})
		})
	};
}

// Marks email by id as unread
function mark_unread(email) {
	if (email.read == true) {
		fetch(`/emails/${email.id}`, {
			method: 'PUT',
			body: JSON.stringify({
				read: false
			})
		})
	};
}

// Archives email by id
function archive(email) {
	if (email.archived != true) {
		fetch(`/emails/${email.id}`, {
			method: 'PUT',
			body: JSON.stringify({
				archived: true
			})
		})
		// Then load the inbox
		load_mailbox('inbox');
	};
}

// Archives email by id
function remove_archive(email) {
	if (email.archived == true) {
		fetch(`/emails/${email.id}`, {
			method: 'PUT',
			body: JSON.stringify({
				archived: false
			})
		})
		// Then load the inbox
		load_mailbox('inbox');
	};
}