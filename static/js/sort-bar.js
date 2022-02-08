var category = document.getElementsByClassName('custom-product-active');
var sorting = document.getElementsByClassName('shared-property');

var active = category[0];
var copyOfCategory="";
categories = active.getAttribute("href");

console.log(active.getAttribute("href"))
console.log(categories.indexOf('=', 0))
console.log(sorting[0])

for (let i = 20; i < categories.length; i++) {
    copyOfCategory = copyOfCategory + categories[i];
    console.log(copyOfCategory);
}

sorting[0].href='/products/?category='+(copyOfCategory)+('&sort=price&direction=desc');


