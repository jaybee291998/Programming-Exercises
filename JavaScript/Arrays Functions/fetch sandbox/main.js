const output = document.getElementById('output');

const getUsersBtn = document.getElementById('getUser');
const getPostsBtn = document.getElementById('getPost');
const form = document.getElementById('addPost');


getUsersBtn.addEventListener('click', getUsers);
getPostsBtn.addEventListener('click', getPosts);
form.addEventListener('submit', addPost);

function getUsers()
{
	fetch('https://jsonplaceholder.typicode.com/users')
	.then(res => res.json())
	.then(users => {
		console.log(users);
		let outputText = '<h2 class="mb-4">Users</h2>';
		users.forEach(user =>{
			outputText += `<ul class='list-group mb-3'>
				<li class='list-group-item'>ID:${user.id}</li>
				<li class='list-group-item'>Username:${user.username}</li>
				<li class='list-group-item'>Email:${user.email}</li>
			</ul>`;
		});
		output.innerHTML = outputText;
	});
}


function getPosts()
{
	fetch('http://127.0.0.1:8000/api/task-list/')
	.then(res => res.json())
	.then(posts => {
		console.log(posts);
		let outputText = '<h2 class="mb-4">Post</h2>';
		posts.forEach(post =>{
			outputText += `
				<div class ='card card-body mb-3'>
					<h3>${post.title}</h3>
					<p>${post.is_complete}</p>
				</div
			`;
		});
		output.innerHTML = outputText;
	});

}
// function getPosts()
// {
// 	fetch('https://jsonplaceholder.typicode.com/posts')
// 	.then(res => res.json())
// 	.then(posts => {
// 		console.log(posts);
// 		let outputText = '<h2 class="mb-4">Post</h2>';
// 		posts.forEach(post =>{
// 			outputText += `
// 				<div class ='card card-body mb-3'>
// 					<h3>${post.title}</h3>
// 					<p>${post.body}</p>
// 				</div
// 			`;
// 		});
// 		output.innerHTML = outputText;
// 	});

// }

function addPost(e)
{
	e.preventDefault();

	let title = document.getElementById('title').value;
	let body = document.getElementById('body').value;

	fetch('https://jsonplaceholder.typicode.com/posts',{
		method: 'POST',
		headers: {
			'Accept': 'application/json, text/plain, */*',
			'Content-type': 'application/json'
		},
		body: JSON.stringify({title:title, body:body})
	})
	.then(res => res.json())
	.then(data => console.log(data));
	console.log('asynchronous rules!!!!');
}

// function addTask(e)
// {
// 	e.preventDefault();

// 	let title = document.getElementById('title').value;
// 	let body = document.getElementById('body').value;

// 	fetch('http://127.0.0.1:8000/api/task-create/',{
// 		method: 'POST',
// 		headers: {
// 			'Accept': 'application/json, text/plain, */*',
// 			'Content-type': 'application/json'
// 		},
// 		body: JSON.stringify({title:title})
// 	})
// 	.then(res => res.json())
// 	.then(data => console.log(data))
// 	.catch("Error: Something went wrong");
// 	console.log('asynchronous rules!!!!');
// }

// function displayUserData(users)
// {

// }