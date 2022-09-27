 var arr = [];

 function addItem(item)
 {
 	arr.push(item);
 }

 function removeItem()
 {
 	return arr.shift();
 }

addItem(1);
addItem(2);
addItem(3);

console.log(JSON.stringify(arr));
console.log(removeItem());
console.log(JSON.stringify(arr));