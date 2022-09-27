const allConstruct = (target, wordBank) =>
{
	if(target === '') return [[]];

	for(let str of wordBank)
	{
		if(target.indexOf(str) === 0) //checks if str is a suffix of the target
		{
			const newTarget = target.slice(str.length);
			console.log(newTarget);
			const com = allConstruct(newTarget, wordBank);
		}	
	}

	return null;
}

let wordBank = ["ja", "yv", "ee"];
let target = "jayvee";

allConstruct(target, wordBank);
