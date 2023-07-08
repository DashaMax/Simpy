let dot = document.querySelector('#dot');
let closeMenu = document.querySelector('.close-menu');
let closeMenuH3 = document.querySelector('.close-menu h3');

let butAdd = document.querySelector('.add-form');
let addForm = document.querySelector('.block-back');
let blockH2 = document.querySelector('.block-back h2');

dot.onclick = function(){
    closeMenu.style.display = 'block';
};

closeMenuH3.onclick = function(){
    closeMenu.style.display = 'none';
};

let bookAdd = document.querySelectorAll('.add');

for(let i=0; i<bookAdd.length; i++){
    bookAdd[i].onclick = function(){
        bookAdd[i].innerHTML = 'Добавлена';
        bookAdd[i].classList.remove('add');
        bookAdd[i].classList.add('add-yet');
    }
};

butAdd.onclick = function(){
    addForm.style.display = 'block';
};

blockH2.onclick = function(){
    addForm.style.display = 'none';
};