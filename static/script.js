//const BASE_URL = "http://192.168.1.8:5000"
//const BASE_URL = "http://127.0.0.1:5000"
const BASE_URL = "https://flask-hello-world-stb5.onrender.com"

async function APIrequest(apiURL){
  try {
    const response = await fetch(apiURL);
    if (!response.ok) {
      throw new Error('Erreur lors de la récupération des données');
    }
    const data = await response.json();
    return data

  } catch (error) {
    console.error('Erreur:', error);
  }
}

let switchSiteSelected = "Bureau Paris";

let sitesData = null;

async function getSitesId() {
  if (sitesData) {
    // Si les données sont déjà récupérées, les retourner directement
    return sitesData;
  }

  try {
    sitesData = await APIrequest(BASE_URL + "/sites"); // Appel de l'API
    return sitesData;

  } catch (error) {
    console.error('Erreur:', error); // Gestion des erreurs
  }
}

function getRandomColor() {
  // Génère une teinte (Hue) entre 0 et 360 degrés
  const hue = Math.floor(Math.random() * 360);

  // Saturation fixée à 70% pour des couleurs vives
  const saturation = 70; 

  // Luminosité entre 50% et 70% pour éviter des couleurs trop sombres ou trop claires
  const lightness = Math.floor(Math.random() * 20) + 50;

  // Créer la couleur en utilisant le modèle HSL
  return `hsl(${hue}, ${saturation}%, ${lightness}%)`;
}

let workersData = null;

async function getWorkers() {
  if (workersData) {
    // Si les données sont déjà récupérées, les retourner directement
    return workersData;
  }

  try {
    workersData = await APIrequest(BASE_URL + "/workers"); // Appel de l'API

    workersData.forEach((element) => {
      element.color = getRandomColor();
    });

    return workersData;

  } catch (error) {
    console.error('Erreur:', error); // Gestion des erreurs
  }
}


// Animation switch lieux
document.addEventListener('DOMContentLoaded', function() {
  const firstSite = document.querySelector('.sites:nth-child(1)');
  const animation = document.querySelector('.animation');

  // Sélectionner par défaut le premier élément
  firstSite.classList.add('active');
  animation.style.left = firstSite.getAttribute('data-target') + 'px';
  animation.style.width = firstSite.offsetWidth - 6 + 'px'; // Largeur de l'élément sélectionné (enlever les marges)

  // Gérer les clics sur les autres éléments
  document.querySelectorAll('.sites').forEach(site => {
    site.addEventListener('click', function() {
      // Supprimer la classe active de tous les autres éléments
      document.querySelectorAll('.sites').forEach(s => s.classList.remove('active'));

      // Ajouter la classe active à l'élément sélectionné
      this.classList.add('active');

      // Déplacer l'animation
      const targetLeft = this.getAttribute('data-target'); // Valeur "left" à partir de l'attribut data-target
      animation.style.left = targetLeft + 'px';
      animation.style.width = this.offsetWidth - 6 + 'px'; // Largeur de l'élément sélectionné (enlever les marges)

      document.querySelectorAll('.main').forEach(e => e.remove());

      currentWeek = 0;
      dayRectangle = new Date();
      dayRectangle.setDate(dayRectangle.getDate()-7);

      if (switchSiteSelected === "Bureau Paris"){
        switchSiteSelected = "Bureau Lyon";
      }else{
        switchSiteSelected = "Bureau Paris";
      }

      createWeek();
      createWeek();
      createWeek();       
    });
  });
});

const colorGreen = '#8FE2A4';
const colorGray = '#E5E5E5';

let isModiferState = false;

const modifierButton = document.getElementById('modifierButton');


async function deleteReservation(workerId, siteId, date) {
  const url = BASE_URL + "/reservations";
  
  const body = JSON.stringify({
    worker_id: workerId,
    site_id: siteId,
    date: date
  });

  try {
    const response = await fetch(url, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
      body: body
    });

    if (!response.ok) {
      throw new Error(`Erreur: ${response.statusText}`);
    }

    const data = await response.json();
    console.log('Réservation supprimée:', data);
  } catch (error) {
    console.error('Erreur lors de la suppression de la réservation:', error);
  }
}

async function createReservation(workerId, siteId, date) {
  const url = BASE_URL + "/reservations";
  
  const body = JSON.stringify({
    worker_id: workerId,
    site_id: siteId,
    date: date
  });

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: body
    });

    if (!response.ok) {
      throw new Error(`Erreur: ${response.statusText}`);
    }

    const data = await response.json();
    console.log('Réservation créée:', data);
  } catch (error) {
    console.error('Erreur lors de la création de la réservation:', error);
  }
}

function handleClick() {
  if (isModiferState) {
    isReserved = this.querySelector("#Jean_Martin");

    const siteId = sitesData.find(site => site.name === "Bureau Paris").id;

    const worker = workersData.find(worker => worker.firstname === "Jean");
    
    if (isReserved){
      this.style.backgroundColor = colorGray;
      deleteReservation(worker.id, siteId, this.id);
      isReserved.remove();
    }else{
      this.style.backgroundColor = colorGreen;
      createReservation(worker.id, siteId, this.id);
      const circle = document.createElement('div');
      circle.classList.add('circle'); // Ajoute la classe pour le style

      var leftPosition = this.querySelectorAll(".circle").length;

      if(this.className.includes("big_rectangle")){
        leftPosition = leftPosition * 45 + 15;
      }else{
        leftPosition = leftPosition * 20 + 15;
      }

      // Appliquer la position gauche (left) au cercle pour le décaler
      circle.style.left = `${leftPosition}px`;
      circle.textContent = worker.firstname[0] + worker.lastname[0];
      circle.classList.add('circle-inner-border');

      circle.style.backgroundColor = worker.color;
      circle.id = worker.firstname + "_" + worker.lastname;

      circle.style.display = 'none';

      // Ajouter le cercle au rectangle
      this.appendChild(circle);
    }
  }
}

const weekLimit = 52;
let currentWeek = 0;
var dayRectangle = new Date();
dayRectangle.setDate(dayRectangle.getDate()-7);


const weekContainer = document.getElementById("weekSelector");
const createWeek = () => {

  currentWeek += 1;

  dayRectangle.setDate((dayRectangle.getDate() - (dayRectangle.getDay() + 6) % 7)+7);

  var formattedDate = dayRectangle.getFullYear() + '-' +
    String(dayRectangle.getMonth() + 1).padStart(2, '0') + '-' +
    String(dayRectangle.getDate()).padStart(2, '0');

  // Créer l'élément principal contenant la semaine et les rectangles
  const mainDiv = document.createElement("div");
  mainDiv.classList.add("main");

  // Créer l'élément p pour la semaine
  const weekElement = document.createElement("p");
  weekElement.classList.add("week");
  weekElement.textContent = `Semaine du ${dayRectangle.toLocaleString('fr-Fr',{month: "numeric", day: "numeric"})}`;

  // Créer le conteneur principal des jours
  const daysDiv = document.createElement("div");
  daysDiv.classList.add("days");

  // Créer le grand rectangle
  const bigRectangle = document.createElement("div");
  bigRectangle.classList.add("big_rectangle");
  if (currentWeek == 1){bigRectangle.classList.add("activeWeek");}
  if (isModiferState){
    bigRectangle.style.backgroundColor = colorGray;
  }

  // Créer le jour de la semaine
  const lundi = document.createElement("p");
  lundi.classList.add("dayOfTheWeek");
  lundi.textContent = "Lundi";

  bigRectangle.appendChild(lundi);

  // Créer la date
  const lundiNum = document.createElement("p");
  lundiNum.classList.add("dayNum");
  lundiNum.textContent = `${dayRectangle.toLocaleString('fr-Fr',{month: "numeric", day: "numeric"})}`;

  formattedDate = dayRectangle.getFullYear() + '-' +
    String(dayRectangle.getMonth() + 1).padStart(2, '0') + '-' +
    String(dayRectangle.getDate()).padStart(2, '0');

  bigRectangle.id = formattedDate;
  bigRectangle.appendChild(lundiNum);

  // Créer le conteneur pour les petits rectangles
  const smallDaysDiv = document.createElement("div");
  smallDaysDiv.classList.add("days", "small");

  // Conteneur pour la ligne du haut des petits rectangles
  const topSmallDaysDiv = document.createElement("div");
  topSmallDaysDiv.classList.add("days", "small", "top");

  // Petits rectangles dans la ligne du haut
  const smallRectangle1 = document.createElement("div");
  smallRectangle1.classList.add("small_rectangle");
  if (currentWeek == 1){smallRectangle1.classList.add("activeWeek");}
  if (isModiferState){
    smallRectangle1.style.backgroundColor = colorGray;
  }

  // Créer le jour de la semaine
  const mardi = document.createElement("p");
  mardi.classList.add("dayOfTheWeek");
  mardi.textContent = "Mardi";

  smallRectangle1.appendChild(mardi);

  // Créer la date
  const mardiNum = document.createElement("p");
  mardiNum.classList.add("dayNum");
  dayRectangle.setDate(dayRectangle.getDate()+1);
  mardiNum.textContent = `${dayRectangle.toLocaleString('fr-Fr',{month: "numeric", day: "numeric"})}`;

  formattedDate = dayRectangle.getFullYear() + '-' +
    String(dayRectangle.getMonth() + 1).padStart(2, '0') + '-' +
    String(dayRectangle.getDate()).padStart(2, '0');

  smallRectangle1.id = formattedDate;
  smallRectangle1.appendChild(mardiNum);

  const smallRectangle2 = document.createElement("div");
  smallRectangle2.classList.add("small_rectangle");
  if (currentWeek == 1){smallRectangle2.classList.add("activeWeek");}
  if (isModiferState){
    smallRectangle2.style.backgroundColor = colorGray;
  }
  
  // Créer le jour de la semaine
  const mercredi = document.createElement("p");
  mercredi.classList.add("dayOfTheWeek");
  mercredi.textContent = "Mercredi";

  smallRectangle2.appendChild(mercredi);

  // Créer la date
  const mercrediNum = document.createElement("p");
  mercrediNum.classList.add("dayNum");
  dayRectangle.setDate(dayRectangle.getDate()+1);
  mercrediNum.textContent = `${dayRectangle.toLocaleString('fr-Fr',{month: "numeric", day: "numeric"})}`;

  formattedDate = dayRectangle.getFullYear() + '-' +
    String(dayRectangle.getMonth() + 1).padStart(2, '0') + '-' +
    String(dayRectangle.getDate()).padStart(2, '0');

  smallRectangle2.id = formattedDate;
  smallRectangle2.appendChild(mercrediNum);

  // Ajouter les petits rectangles à la ligne du haut
  topSmallDaysDiv.appendChild(smallRectangle1);
  topSmallDaysDiv.appendChild(smallRectangle2);

  // Conteneur pour la ligne du bas des petits rectangles
  const bottomSmallDaysDiv = document.createElement("div");
  bottomSmallDaysDiv.classList.add("days", "small", "bottom");

  // Petits rectangles dans la ligne du bas
  const smallRectangle3 = document.createElement("div");
  smallRectangle3.classList.add("small_rectangle");
  if (currentWeek == 1){smallRectangle3.classList.add("activeWeek");}
  if (isModiferState){
    smallRectangle3.style.backgroundColor = colorGray;
  }
    
  // Créer le jour de la semaine
  const jeudi = document.createElement("p");
  jeudi.classList.add("dayOfTheWeek");
  jeudi.textContent = "Jeudi";

  smallRectangle3.appendChild(jeudi);

  // Créer la date
  const jeudiNum = document.createElement("p");
  jeudiNum.classList.add("dayNum");
  dayRectangle.setDate(dayRectangle.getDate()+1);
  jeudiNum.textContent = `${dayRectangle.toLocaleString('fr-Fr',{month: "numeric", day: "numeric"})}`;

  formattedDate = dayRectangle.getFullYear() + '-' +
    String(dayRectangle.getMonth() + 1).padStart(2, '0') + '-' +
    String(dayRectangle.getDate()).padStart(2, '0');

  smallRectangle3.id = formattedDate;
  smallRectangle3.appendChild(jeudiNum);

  const smallRectangle4 = document.createElement("div");
  smallRectangle4.classList.add("small_rectangle");
  if (currentWeek == 1){smallRectangle4.classList.add("activeWeek");}
  if (isModiferState){
    smallRectangle4.style.backgroundColor = colorGray;
  }
    
  // Créer le jour de la semaine
  const vendredi = document.createElement("p");
  vendredi.classList.add("dayOfTheWeek");
  vendredi.textContent = "Vendredi";

  smallRectangle4.appendChild(vendredi);

  // Créer la date
  const vendrediNum = document.createElement("p");
  vendrediNum.classList.add("dayNum");
  dayRectangle.setDate(dayRectangle.getDate()+1);
  vendrediNum.textContent = `${dayRectangle.toLocaleString('fr-Fr',{month: "numeric", day: "numeric"})}`;

  formattedDate = dayRectangle.getFullYear() + '-' +
    String(dayRectangle.getMonth() + 1).padStart(2, '0') + '-' +
    String(dayRectangle.getDate()).padStart(2, '0');

  smallRectangle4.id = formattedDate;
  smallRectangle4.appendChild(vendrediNum);

  // Ajouter les petits rectangles à la ligne du bas
  bottomSmallDaysDiv.appendChild(smallRectangle3);
  bottomSmallDaysDiv.appendChild(smallRectangle4);

  // Ajouter la ligne du haut et du bas dans le conteneur des petits jours
  smallDaysDiv.appendChild(topSmallDaysDiv);
  smallDaysDiv.appendChild(bottomSmallDaysDiv);

  // Ajouter le grand rectangle et le conteneur des petits jours dans le conteneur des jours
  daysDiv.appendChild(bigRectangle);
  daysDiv.appendChild(smallDaysDiv);

  // Ajouter la semaine et les jours dans l'élément principal
  mainDiv.appendChild(weekElement);
  mainDiv.appendChild(daysDiv);

  // Ajouter l'élément principal dans le container (par exemple `body`)
  weekContainer.appendChild(mainDiv);

  const rectangles = document.querySelectorAll(".big_rectangle, .small_rectangle");

  modifierButton.onclick = function() {

    const circles = document.querySelectorAll('.circle');

    circles.forEach(circle => {
      if (circle.style.display === 'none') {
        circle.style.display = 'flex';
      } else {
        circle.style.display = 'none';
      }
    });

    if (!isModiferState) {
      rectangles.forEach((element) => {
        if(element.querySelector("#Jean_Martin")){
          element.style.backgroundColor = colorGreen;
        }else{
          element.style.backgroundColor = colorGray;
        }
      });
      this.innerText = 'Sauvegarder'
    }else {
      rectangles.forEach((element) => {
        if (element.classList.contains('activeWeek')){
          element.style.backgroundColor = '#93DDFF';
        }else{
          element.style.backgroundColor = '#FFE371';
        }
      });
      this.innerText = "M'enregistrer"
    }
    isModiferState = !isModiferState;
  };

  rectangles.forEach(rect => {
    rect.removeEventListener('click', handleClick);
    rect.addEventListener('click', handleClick);
  });



  async function fetchReservationsForParis() {
    try {

      var weekRectangle = new Date();
      var dayOfWeek = weekRectangle.getDay(); // 0 = Dimanche, 1 = Lundi, etc.
      var diffToMonday = (dayOfWeek + 6) % 7; // Trouver le décalage pour revenir à Lundi (si on est Dimanche, ce sera 6)
      weekRectangle.setDate(weekRectangle.getDate() - diffToMonday); // Revenir au lundi

      // Ajouter les semaines en fonction de `currentWeek`
      weekRectangle.setDate(weekRectangle.getDate() + 7 * (currentWeek-1));
      weekRectangle = weekRectangle.getFullYear() + '-' +
      String(weekRectangle.getMonth() + 1).padStart(2, '0') + '-' +
      String(weekRectangle.getDate()).padStart(2, '0');

      // Récupérer l'ID du site pour "Bureau Paris"

      const sitesId = await getSitesId();
      const siteId = sitesId.find(site => site.name === switchSiteSelected).id;

      const reservationParis = await APIrequest(BASE_URL + "/reservations/site/" + siteId + "/week?start_date=" + weekRectangle);

      const workers = await getWorkers();
                  
      const circleCountByDate = {};

      reservationParis.forEach(reservation => {
        rectangles.forEach(rectangle => {
          if (reservation.date === rectangle.id) {

            // Créer un div pour le cercle
            const circle = document.createElement('div');
            circle.classList.add('circle'); // Ajoute la classe pour le style

            if (!circleCountByDate[reservation.date]) {
              circleCountByDate[reservation.date] = 0; // Initialiser à 0 si pas encore de cercles
            }
      
            var leftPosition = null;

            if(rectangle.className.includes("big_rectangle")){
              leftPosition = circleCountByDate[reservation.date] * 45 + 15;
            }else{
              leftPosition = circleCountByDate[reservation.date] * 20 + 15;
            }

            // Appliquer la position gauche (left) au cercle pour le décaler
            circle.style.left = `${leftPosition}px`;
            const worker = workers.find(worker => worker.id === reservation.worker_id);
            circle.textContent = worker.firstname[0] + worker.lastname[0];

            if (worker.firstname === "Jean" && worker.lastname === "Martin") {
              circle.classList.add('circle-inner-border');
              if (isModiferState){
                rectangle.style.backgroundColor = colorGreen;
              }
            }

            circle.style.backgroundColor = worker.color;

            circle.id = worker.firstname + "_" + worker.lastname;

            if (isModiferState) {
              circle.style.display = 'none';
            }

            // Incrémenter le compteur de cercles pour cette date
            circleCountByDate[reservation.date] += 1;

            // Ajouter le cercle au rectangle
            rectangle.appendChild(circle);
          }
        });
      });
      
    } catch (error) {
      console.error('Erreur:', error); // Gestion des erreurs
    }
  }


  fetchReservationsForParis();

};


const handleInfiniteScroll = () => {
  const endOfScroll =
  weekContainer.scrollLeft + 2 * weekContainer.clientWidth >= weekContainer.scrollWidth - 5; // Détecte la fin du scroll

  if (endOfScroll && currentWeek < weekLimit) {
    createWeek();
  }

  if (currentWeek === weekLimit) {
    removeInfiniteScroll();
  }
};
weekContainer.addEventListener("scroll", handleInfiniteScroll);

const removeInfiniteScroll = () => {
  window.removeEventListener("scroll", handleInfiniteScroll);
};

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

window.onload = function () {
  createWeek();
  sleep(5000).then(() => {
    createWeek();
    createWeek(); 
  });
};
