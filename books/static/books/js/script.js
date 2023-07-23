/* Открыть/закрыть меню */

let dot = document.querySelector('#dot');
let closeMenu = document.querySelector('.close-menu');
let closeMenuH3 = document.querySelector('.close-x');

dot.onclick = function(){
    closeMenu.style.display = 'block';
    dot.style.display = 'none';
};

closeMenuH3.onclick = function(){
    closeMenu.style.display = 'none';
    dot.style.display = 'block';
};

/* Добавление класса active в nav-profile */

let currentURL = document.URL;
let navLink = document.querySelectorAll('.nav-profile .nav-link');

if(navLink){
    for(let i = 0; i < navLink.length; i++){
        if(navLink[i].className == 'nav-link active'){
            navLink[i].className = 'nav-link';
        }
    }

    if(currentURL.includes('bookshelf') && currentURL.includes('user')){
        navLink[1].className = 'nav-link active';
    }
    else if(currentURL.includes('user')){
        navLink[0].className = 'nav-link active';
    }
}

/* Добавление класса active в nav-book */

currentURL = document.URL;
let bookLink = document.querySelectorAll('.nav-book .book-link');

if(bookLink){
    for(let i = 0; i < bookLink.length; i++){
        console.log(bookLink[i].className);
        if(bookLink[i].className == 'book-link active'){
            bookLink[i].className = 'book-link';
        }
    }

    if(currentURL.includes('book') && currentURL.includes('readers')){
        bookLink[1].className = 'book-link active';
    }
    else if(currentURL.includes('book')){
        bookLink[0].className = 'book-link active';
    }
}







let butAdd = document.querySelector('.add-form');
let addForm = document.querySelector('.block-back');
let blockH2 = document.querySelector('.block-back h2');

let showComments = document.querySelectorAll('main .comments .show');

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