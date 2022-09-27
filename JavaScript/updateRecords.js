var collection = {
	"2548":{
		"album":"slippery when wet",
		"artist": "Bon Jovi",
		"tracks": [
			"let it rock",
			"you five love a bad name"
		]
	},
	"2468":{
		"album": "1999",
		"artist": "prince",
		"tracks": [
			"1999",
			"little red corvette"
		]
	},
	"1245": {
		"artist": "robert palmer",
		"tracks": []
	},
	"5439": {
		"album": "ABBA Gold"
	}
};

var collectionCopy = JSON.parse(JSON.stringify(collection));

function updateRecords(id, prop, value)
{
	if(collection.hasOwnProperty(id))
	{
		if(collection[id].hasOwnProperty(prop))
		{
			if(value !== "")
			{
				if(value === "tracks")
				{
					collection[id][prop].push(value);
				}
				else
				{
					collection[id][prop] = value;
				}
			}
			else
			{
				delete collection[id][prop];
			}
		}
		else
		{
			if(value !== "")
			{
				if(prop === "tracks")
				{
					collection[id][prop] = [];
					collection[id][prop].push(value);
				}
				else
				{
					collection[id][prop] = value;
				}
			}
		}
	}	
	else
	{
		collection[id] = {};
		if(value !== "")
		{
			if(prop === "tracks")
			{
				collection[id][prop] = [];
				collection[id][prop].push(value);
			}
			else
			{
				collection[id][prop] = value;
			}		
		}

	}
	return collection;
}

console.log(updateRecords("2468", "tracks", ""));