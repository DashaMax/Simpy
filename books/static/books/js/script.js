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

if(navLink.length > 0){
    for(let i = 0; i < navLink.length; i++){
        if(navLink[i].className == 'nav-link active'){
            navLink[i].className = 'nav-link';
        }
    }

    if(currentURL.includes('bookshelf') && currentURL.includes('user')){
        navLink[1].className = 'nav-link active';
    }
    else if(currentURL.includes('user') && currentURL.includes('blogs')){
        navLink[2].className = 'nav-link active';
    }
    else if(currentURL.includes('user') && currentURL.includes('quotes')){
        navLink[3].className = 'nav-link active';
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
        if(bookLink[i].className == 'book-link active'){
            bookLink[i].className = 'book-link';
        }
    }

    if(currentURL.includes('book/') && currentURL.includes('readers')){
        bookLink[1].className = 'book-link active';
    }
    else if(currentURL.includes('book/') && currentURL.includes('reviews')){
        bookLink[2].className = 'book-link active';
    }
    else if(currentURL.includes('book/') && currentURL.includes('quotes')){
        bookLink[3].className = 'book-link active';
    }
    else if(currentURL.includes('book/')){
        bookLink[0].className = 'book-link active';
    }

}


/* Форма добавления нового отзыва */

let butAdd = document.querySelector('.add');
let addForm = document.querySelector('.block-back');
let blockH2 = document.querySelector('.block-back h2');
let body = document.querySelector('body');

if(butAdd){
    butAdd.onclick = function(){
        addForm.style.display = 'block';
        body.style.overflowY = 'hidden'
    };
}

if(blockH2){
    blockH2.onclick = function(){
        addForm.style.display = 'none';
        body.style.overflowY = 'visible';
    };
}


/* Показать/спрятать комментарий */

let showComments = document.querySelectorAll('main .comments .show');

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


/* Сортировка */

let select = document.querySelector('.filters-select');

if(select){
    select.addEventListener('change', (event) => {
        let option = event.target.options[event.target.selectedIndex];
        let value = option.getAttribute('value');
        let name = option.getAttribute('name');

        if(currentURL.includes('?')){
            let url = currentURL.split('?')[0];

            if(name){
                window.location.href = url + '?' + name + '=' + value;
            }
            else{
                window.location.href = url;
            }
        }
        else{
            window.location.href = document.URL + '?' + name + '=' + value;
        }
    });

    /* Добавление selected */

    for(let i = 0; i < select.options.length; i++){
        if(select.options[i].selected){
            select.options[i].setAttribute('selected', false);
        }
    }

    if(currentURL.includes('?date=up')){
        select.options[1].setAttribute('selected', true);
    }
    else if(currentURL.includes('?date=down')){
        select.options[2].setAttribute('selected', true);
    }
    else if(currentURL.includes('?rating=up')){
        select.options[3].setAttribute('selected', true);
    }
    else if(currentURL.includes('?rating=down')){
        select.options[4].setAttribute('selected', true);
    }
}

/* Scroll */

let div = document.querySelector('.messages .block-messages');

if(div){
    div.scrollTop = div.scrollHeight;
}
