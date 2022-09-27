// function displayTime()
// {
// 	let date = new Date();
// 	let time = date.toLocaleTimeString();
// 	document.getElementById('output').textContent =Date.now();
// }

// const createClock = setInterval(displayTime, 1000);


let startTime = Date.now();
let currentTime = 0;
let endTime = 0;

let running = false;

const output = document.getElementById('output');

const startBtn = document.getElementById('start');
const pauseBtn = document.getElementById('pause');
const resetBtn = document.getElementById('reset');


startBtn.addEventListener('click', start);
pauseBtn.addEventListener('click', pause);
resetBtn.addEventListener('click', reset);

function updateDisplay()
{
	if(running)
	{
		updateCurrentTime();		
	}
	output.textContent = convertToStopwatchFormat(currentTime);

	// console.log(Date.now() - startTime);
}

function convertToStopwatchFormat(time)
{
	let hour = 0;
	let minute = 0;
	let second = 0;
	let millisecond = 0;

	let rem = 0;

	let timeConvertedToSec = Math.floor(time / 1000);
	hour = Math.floor(timeConvertedToSec / 3600);
	rem = timeConvertedToSec % 3600;
	minute = Math.floor(rem / 60);
	rem = rem % 60;
	second = rem;




	return `${convert(hour)} : ${convert(minute)} : ${convert(second)}`;

}

function convert(num)
{
	if(num < 10) return '0'+num;
	else return num;
}

function start()
{
	if(!running)
	{
		startTime = Date.now() - currentTime;
		running = true;
	}
}

function pause()
{
	if(running)
	{
		endTime = Date.now();
		running = false;
		updateCurrentTime();
	}
	
}

function reset()
{
	if(running)
	{
		startTime = Date.now();
		running = false;
		updateCurrentTime();
	}
}

function updateCurrentTime()
{
	currentTime = Date.now() - startTime;
}




const createStopwatch = setInterval(updateDisplay, 1000);



