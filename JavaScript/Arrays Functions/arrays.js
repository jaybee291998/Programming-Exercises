var itemList = document.getElementById('items');

var names = ['jayvee', 'irene', 'lerma', 'marina', 'rodel', 'imee'];

const companies= [
  {name: "Company One", category: "Finance", start: 1981, end: 2004},
  {name: "Company Two", category: "Retail", start: 1992, end: 2008},
  {name: "Company Three", category: "Auto", start: 1999, end: 2007},
  {name: "Company Four", category: "Retail", start: 1989, end: 2010},
  {name: "Company Five", category: "Technology", start: 2009, end: 2014},
  {name: "Company Six", category: "Finance", start: 1987, end: 2010},
  {name: "Company Seven", category: "Auto", start: 1986, end: 1996},
  {name: "Company Eight", category: "Technology", start: 2011, end: 2016},
  {name: "Company Nine", category: "Retail", start: 1981, end: 1989}
];

const ages = [33, 12, 20, 16, 5, 54, 21, 44, 61, 13, 15, 45, 25, 64, 32];


// const retailCompanies = companies.filter(company => company.category.toLowerCase() === 'retail').map(company=>`${company.name} [${company.start} - ${company.end}]`);

// const ageSquared = ages.map(age=>age*age);

// const sortedCompanies = companies.sort((a,b)=>(a.start>b.start?1:-1));
// const companiesEndedRecently = companies.sort((a,b)=>(a.end>b.end?-1:1));

// const sortedAges = ages.sort((a,b)=>(a<b?-1:1));

// const totalAge = ages.reduce((total, age)=> total+age, 0);
const reduceTest = companies.reduce((total, company) => total + (company.end - company.start), 0);
console.log(reduceTest);
// displayArrayToBrowser(totalAge);



function displayArrayToBrowser(array)
{
	array.forEach(element =>{
		console.log(element);
		var newItem = document.createElement('li');
		newItem.className = 'list-group-item';

		var textNode = document.createTextNode(element);
		newItem.appendChild(textNode);
		itemList.appendChild(newItem);
	});
}