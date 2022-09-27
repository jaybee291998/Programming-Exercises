var count = 0;

function cc(card)
{
	switch(card)
	{
		
		case 2: 
		case 3:
		case 4:
		case 5:
		case 6:
			count++;
			break;

		case 10:
		case "J": 
		case "Q":
		case "K":
		case "A":
			count--;
			break;
	}

	var bet = "hold";
	if(count > 0) bet = "bet";

	return "Current count: " + count + "\nMove: " + bet;
}

cc("A"); cc(3); cc(7); cc(5);
console.log(cc(2));