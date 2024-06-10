
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
  firebase.initializeApp(firebaseConfig);

// Register Form
const registerForm = document.getElementById('myformSign');
registerForm.addEventListener('submit', function(event) {
  event.preventDefault();
  const email = document.getElementById('your_email').value;
  const password = document.getElementById('password').value;

  // Sign up the user
  firebase.auth().createUserWithEmailAndPassword(email, password)
    .then((userCredential) => {
      // Signed in 
      const user = userCredential.user;
      // Here you can store additional user data in Firebase Realtime Database or Firestore
      // For example:
      firebase.database().ref('users/' + user.uid).set({
        firstName: document.getElementById('first_name').value,
        lastName: document.getElementById('last_name').value,
        // Add other user data here
      }).then(() => {
        console.log('User data stored successfully');
        // Redirect or perform other actions after successful registration
      }).catch((error) => {
        console.error('Error storing user data:', error);
      });
    })
    .catch((error) => {
      const errorCode = error.code;
      const errorMessage = error.message;
      // Handle errors here
      console.error('Registration error:', errorMessage);
    });
});