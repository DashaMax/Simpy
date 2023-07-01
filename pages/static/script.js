let dot = document.querySelector('#dot');
let closeMenu = document.querySelector('.close-menu');
let closeMenuH3 = document.querySelector('.close-menu h3');

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