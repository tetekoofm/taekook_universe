  import { initializeApp } from "https://www.gstatic.com/firebasejs/12.5.0/firebase-app.js";
  import { getAnalytics } from "https://www.gstatic.com/firebasejs/12.5.0/firebase-analytics.js";
  import { getDatabase, ref, set, push, onValue, query, orderByChild, limitToLast } 
  from "https://www.gstatic.com/firebasejs/12.5.0/firebase-database.js";

// Initialize Realtime Database
  const firebaseConfig = {
    apiKey: "AIzaSyDfg5nsb9mx-8RQTQ_yrmDhmAqWnjlIIkU",
    authDomain: "thetku.firebaseapp.com",
    projectId: "thetku",
    storageBucket: "thetku.firebasestorage.app",
    messagingSenderId: "1027898575475",
    appId: "1:1027898575475:web:b6917af30e566ca913f806",
    measurementId: "G-JZNTD1XYGF"
  };

  // Initialize Firebase
  const app = initializeApp(firebaseConfig);
  const analytics = getAnalytics(app);
  const database = getDatabase(app);