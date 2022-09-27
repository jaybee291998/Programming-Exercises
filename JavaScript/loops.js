// var contacts = [
// 	{
// 		"firstName":"Akira",
// 		"lastName":"Laine",
// 		"number":"0911123",
// 		"likes":["pizza", "coding", "brownie points"]
// 	},

// 	{
// 		"firstName":"harry",
// 		"lastName":"potter",
// 		"number":"1292",
// 		"likes":["ginny", "brooms", "voldemort"]
// 	},

// 	{
// 		"firstName":"hemione",
// 		"lastName":"granger",
// 		"number":"12929",
// 		"likes":["ron", "time travel", "brownie points"]
// 	},

// 	{
// 		"firstName":"ron",
// 		"lastName":"weasley",
// 		"number":"748574",
// 		"likes":["scabbers", "candies", "live peacefully"]
// 	}
// ]

// function lookupProfile(name, prop)
// {
// 	let res = "No such thing is found";
// 	for(let i = 0; i < contacts.length; i++)
// 	{
// 		let con = contacts[i];
// 		if(con.hasOwnProperty(prop) && con.hasOwnProperty("firstName") && con["firstName"] === name)
// 		{
// 			res = con[prop];
// 			break;
// 		}
// 	}
// 	return res;
// }


// function getLowest(array)
// {
// 	let lowest = array[0];
// 	for(let i = 1; i < array.length; i++)
// 	{
// 		if(array[i] < lowest) lowest = array[i];
// 	}
// 	return lowest;
// }


// console.log(lookupProfile("ron", "lastName"));
// var list = [];
// var i = 0;
// while(i<10000)
// {
// 	var num = Math.floor(Math.random()*(100-10))+10;	
// 	list.push(num);
// 	i++;
// }


// console.log(getLowest(list));


str = "A";
num = parseInt(str,16);
console.log(num);
