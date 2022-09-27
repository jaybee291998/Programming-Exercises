var player = {
	'name' 		: 'Ainz Ooal Gown',
	'level' 	: 100,
	'race' 		: 'Undead',
	'classes' 	: {'necromancer':10, 'master of death':10, 'eclipse':5, 'etc':35},
	'stats'		: {'hp':60, 'mp':101, 'physAtk':35, 'physDef':70, 'agl':40, 'magAtk':90, 'magDef':95, 'resist':95, 'sp':100}
};

var player2 = {
	'name' 		: 'Ainz Ooal Gown',
	'level' 	: 100,
	'race' 		: 'Undead',
	'classes' 	: {'necromancer':10, 'master of death':10, 'eclipse':5, 'etc':35},
	'stats'		: {'hp':60, 'mp':101, 'physAtk':35, 'physDef':70, 'agl':40, 'magAtk':90, 'magDef':95, 'resist':95, 'sp':100}
};


var players = []

//console.log(player);
//player['name'] = 'Momonga';
player['WCI'] = ["momonga's red orb", "depiction of nature and country", "billion blades", "avvarice of generosity", "ginungagap"];


var stats = player['stats'];
console.log(stats);


var newClass = 'emperor of death';
player['classes'][newClass] = 10;
player['classes']['etc']-=player['classes'][newClass];
console.log(player);

var cls = 'emperor of death';
if(player['classes'].hasOwnProperty(cls)) console.log("The player " + player['name'] + " has a class in " + cls + " with " + player['classes'][cls] + " levels");
else console.log("No such class '" + cls +"' is found for the player " + player["name"]);