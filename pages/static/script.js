let dot = document.querySelector('#dot');
let closeMenu = document.querySelector('.close-menu');
let closeMenuH3 = document.querySelector('.close-menu h3');

let butAdd = document.querySelector('.add-form');
let addForm = document.querySelector('.block-back');
let blockH2 = document.querySelector('.block-back h2');

let showComments = document.querySelectorAll('main .comments .show');

dot.onclick = function(){
    closeMenu.style.display = 'block';
    dot.style.display = 'none';
};

closeMenuH3.onclick = function(){
    closeMenu.style.display = 'none';
    dot.style.display = 'block';
};

let bookAdd = document.querySelectorAll('.add');

for(let i=0; i<bookAdd.length; i++){
    bookAdd[i].onclick = function(){
        bookAdd[i].innerHTML = 'Добавлена';
        bookAdd[i].classList.remove('add');
        bookAdd[i].classList.add('add-yet');
    }
};

if(butAdd){
    butAdd.onclick = function(){
        addForm.style.display = 'block';
    };
}

if (blockH2){
    blockH2.onclick = function(){
        addForm.style.display = 'none';
    };
}

showComments.forEach(item => {
    item.addEventListener('click', function(){
        let NOW = item.parentNode.parentNode;
        let commentBack = NOW.querySelectorAll('.back');

        for(let i=0; i<commentBack.length; i++){
            commentBack[i].style.display = 'flex';
        };

        item.style.display = 'none';
    })
})