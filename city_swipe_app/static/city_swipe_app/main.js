'use strict';

let userLatitude = 50.907688;
let userLongtitude = 34.796716;

let centerLat = 50.907688;
let centerLong = 34.796716;

function rad(x) {
  return x * Math.PI / 180;
}

function getDistance(p1, p2) {
  let R = 6378137; // Earth’s mean radius in meter
  let dLat = rad(p2.lat - p1.lat);
  let dLong = rad(p2.lng - p1.lng);
  let a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(rad(p1.lat)) * Math.cos(rad(p2.lat)) *
    Math.sin(dLong / 2) * Math.sin(dLong / 2);
  let c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  let d = R * c;
  return d; // returns the distance in meter
}

$(document).ready(function() {
    getUserLocation();
    let buttons = document.getElementsByClassName('answer-btn');
    for (let i = 0; i < buttons.length; i++) {
      buttons[i].addEventListener('click', function(){
        submitAnswer(this);
      });
    }
});

function getUserLocation() {
  $.get("/city_swipe_app/getUser/", {})
    .done(function(data){
      if (data === 404) {
        showLocationForm()
      } else {
        let user = data;
        userLatitude = user.latitude;
        userLongtitude = user.longitude;
        getCard();
      }
    });
}

function submitAnswer(answer) {
  let cardId = document.getElementById('cardImage').dataset.cardid;
  $.post("/city_swipe_app/submitAnswer/", {answer: answer.id, card: cardId});
  getCard();
}

function submitLocation() {
  $.post("/city_swipe_app/setUserLocation/", {latitude: userLatitude, longtitude: userLongtitude});
  document.getElementById('submitLocation').remove();
  getCard();
}

function getCard() {
  let card;
  $.get("/city_swipe_app/getCard/", {latitude: userLatitude, longtitude: userLongtitude})
    .done(function(data) {
      if (data === 404) {
        window.location.replace("/city_swipe_app/endPage");
      }else {
        showCard(data);
      }
  });
  return card;
}

function showLocationForm() {
    document.getElementsByClassName('btn-container')[0].hidden = true;
    let title = document.getElementById('questionTitle');
    let mapElem = document.createElement('div');
    let button = document.createElement('button');
    title.innerHTML = 'Вкажіть ваше місце знаходження, аби ми змогли підібрати для вас місця, де ви найчастіше буваєте';
    mapElem.id = 'map';
    button.id = 'submitLocation';
    button.innerText = 'Підтвердити'

    button.addEventListener('click', function() {
      submitLocation();
    });

    document.getElementById('card').appendChild(mapElem);
    document.getElementById('mainContainer').appendChild(button);

    let mymap = L.map('map').setView([50.907688, 34.796716], 13);

  	L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
  		maxZoom: 18,
  		id: 'mapbox/streets-v11',
  		tileSize: 512,
  		zoomOffset: -1
  	}).addTo(mymap);

    let circle = L.circle([50.907688, 34.796716], {
      color: 'yellow',
      fillColor: 'yellow',
      fillOpacity: 0.08,
      radius: 5000
    }).addTo(mymap);

    let marker = L.marker([50.907688, 34.796716]).addTo(mymap);
    mymap.on('click', function(e){
      let center = {
        lat: centerLat,
        lng: centerLong,
      }
      let point = {
        lat: e.latlng.lat,
        lng: e.latlng.lng,
      }

      userLatitude = e.latlng.lat;
      userLongtitude = e.latlng.lng;

      if(getDistance(center, point) <= 5000) {
        marker.remove()
        marker = L.marker(e.latlng).addTo(mymap);
      }
    });
}

function showCard(card) {
    document.getElementsByClassName('btn-container')[0].hidden = false;
    document.getElementById('card').innerHTML = '';

    document.getElementById('questionTitle').innerText = card.title;
    let photo = document.createElement('img');
    photo.src = card.photo;
    photo.id = 'cardImage'
    photo.dataset.cardid = card.id;

    let aboutCard = document.createElement('aboutCard');
    aboutCard.innerText = card.about;

    document.getElementById('card').appendChild(aboutCard);
    document.getElementById('card').appendChild(photo);
}
