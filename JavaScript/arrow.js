const anon = (array, exponent, f) =>
{
	for(i = 0; i < array.length; i++)
	{
		array[i] = f(array[i], exponent);
	}
	return array;
}

const exp = (num, exp) =>
{
	let ans = 1;
	for(let i = 0; i < exp; i++)
	{
		ans *= num;
	}
	return ans;

}

let array = [12,13,4,15,16,11];
console.log(array);
console.log(anon(array, 2, exp));