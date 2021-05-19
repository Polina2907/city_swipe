$(document).ready(function(){
    document.getElementById('resetLoc').addEventListener('click', function(){
        $.get("/city_swipe_app/resetUserLocation/");        
        window.location.replace("/city_swipe_app/mainPage");        
    })
})

let mymap = L.map('map').setView([50.907688, 34.796716], 13);

let greenIcon = L.icon({
    iconUrl: '/static/city_swipe_app/green.png',
    iconSize: [20, 20],
});

let yellowIcon = L.icon({
    iconUrl: '/static/city_swipe_app/yellow.png',
    iconSize: [20, 20],
});

let redIcon = L.icon({
    iconUrl: '/static/city_swipe_app/red.png',
    iconSize: [20, 20],
});

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {    
maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1
}).addTo(mymap);

let markers = L.markerClusterGroup();

$.get("/city_swipe_app/getAllCards/")
.done(function(data) {
    for (let i = 0; i < data.length; i++){
        let marker;
        if (data[i].mark >= 5) {
            marker = L.marker([data[i].latitude, data[i].longitude], {icon: greenIcon, opacity: 0.8})
        }
        else if (data[i].mark < 5 && data[i].mark >= 0) {
            marker = L.marker([data[i].latitude, data[i].longitude], {icon: yellowIcon, opacity: 0.8})
        }
        else if (data[i].mark < 0) {
            marker = L.marker([data[i].latitude, data[i].longitude], {icon: redIcon, opacity: 0.8})
        }
        marker.bindPopup(data[i].about + '<br> оцінка: ' + data[i].mark);
        markers.addLayer(marker);
    }
    mymap.addLayer(markers);
    fillStatistic(data);
});

function fillStatistic(cards){
    cards.sort(function(a, b){
        return b.mark - a.mark;
    })
    let bestCards = [];
    let k = 3;
    for (let i = 0; i < cards.length; i++){
       if (k != 0) {
        bestCards.push(cards[i]);
        k--;
       }
    }

    cards.sort(function(a, b){
        return a.mark - b.mark;
    })
    let worstCards = [];
    k = 3;
    for (let i = 0; i < cards.length; i++){
       if (k != 0) {
        worstCards.push(cards[i]);
        k--;
       }
    }
    showStatistic(bestCards, document.getElementById('bestCards'));
    showStatistic(worstCards, document.getElementById('worstCards'));
}

function showStatistic(Cards, coloumn) {
    for(let i = 0; i < Cards.length; i++){
        let card = document.createElement('div');
        card.classList.add('card');
        
        let title = document.createElement('span');
        title.classList.add('title');
        title.innerText = 'Питання: ' + Cards[i].title;
        
        let about = document.createElement('span');
        about.classList.add('about');
        about.innerText = 'Деталі: ' + Cards[i].about;
        
        let mark = document.createElement('span'); 
        mark.classList.add('mark');
        mark.innerText = 'Рейтинг: ' + Cards[i].mark;

        card.appendChild(title);
        card.appendChild(about);
        card.appendChild(mark);

        coloumn.appendChild(card);
    }    
}