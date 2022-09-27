const posts = [
	{title: 'Post one', body: 'This is post one'},
	{title: 'Post two', body: 'This is post two'}
];

function getPost() 
{
	setTimeout(() => {
		let output = '';
		posts.forEach(post => {
			output += `<li>${post.title}</li>`;
		});
		document.body.innerHTML = output;
	}, 1000);
}

function createPost(post)
{
	return new Promise((resolve, reject) => {
		setTimeout(() => {
			posts.push(post);

			let error = false;

			if(!error) resolve();
			else reject('Something went wrong');
		}, 2000);
	});

}

async function getTodos()
{
	const response = await fetch('https://jsonplaceholder.typicode.com/todos');

	const data = await response.json();

	console.log(data);
}

getTodos();
console.log('i like turles');
// fetch('https://jsonplaceholder.typicode.com/todos')
//  .then(res => res.json())
//  .then(data => console.log(data));

// createPost({ title: 'Post 3', body: 'This is post 3' })
//  .then(getPost)
//  .catch(error => console.log(error));

// async function init()
// {
// 	await createPost({ title: 'Post 3', body: 'This is post 3' });

// 	getPost();
// }

// init();

// console.log(setTimeout((message) => { console.log(message) }, 2000, "This is my return value"));

// const promise1 = new Promise((resolve, reject) => {
// 	resolve({ title: 'I hate  Pots', body: 'posts'});
// 	return 'I do return';
// });


// promise1.then((message) => console.log(message));


