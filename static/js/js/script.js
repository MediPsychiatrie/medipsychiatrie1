// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.11.1/firebase-app.js";
import { getDatabase, ref, set, get, child } from "https://www.gstatic.com/firebasejs/10.11.1/firebase-database.js";


// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyCipLSrzVTCM8rmtPu9VlxM3Pz4OVHTVVw",
  authDomain: "medipsychiatre-d9468.firebaseapp.com",
  databaseURL: "https://medipsychiatre-d9468-default-rtdb.firebaseio.com",
  projectId: "medipsychiatre-d9468",
  storageBucket: "medipsychiatre-d9468.appspot.com",
  messagingSenderId: "603264205444",
  appId: "1:603264205444:web:afadb2a9e27d732ce178d1"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// get ref to database services

const db = getDatabase(app);

document.getElementById("register").addEventListener('click', function(e){
set(ref(db, 'user/' + document.getElementById("first_name").value),{

    first_name : document.getElementById("first_name").value,
    last_name : document.getElementById("last_name").value,
    Genre : document.getElementById("Genre").value,
    date : document.getElementById("date").value,
    Situation_Familiale : document.getElementById("SF").value,
    poids : document.getElementById("poids").value,
    taille : document.getElementById("taille").value,
    email : document.getElementById("your_email").value,
    password : document.getElementById("password").value,
    phone : document.getElementById("phone").value,
    place : document.getElementById("place").value,
    Country : document.getElementById("Country").value

});
alert("Connexion réussie !");

})