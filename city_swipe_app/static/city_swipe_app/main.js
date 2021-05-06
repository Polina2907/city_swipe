'use strict';

let card;
window.addEventListener('load', function() {

    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
          if (this.responseText === '404'){
              //перенаправить юзера на страницу конца
          }
          else{
            card = JSON.parse(this.responseText);
            showCard();
          }
        }
    };
    xhttp.open('GET', '/city_swipe_app/getCard/', true);
    xhttp.send();
});

function showCard() {
    document.getElementById('image').src = card.photo;
    document.getElementById('title').innerHTML = card.name;
}