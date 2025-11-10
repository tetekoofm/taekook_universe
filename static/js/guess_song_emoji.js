let allSongs = [];
let gameSongs = [];
let currentIndex = 0;
let score = 0;
const GAME_NAME = "guess_song_emoji";  // match your Flask route/game key

// Load JSON and pick 10 random songs
fetch('/static/js/guess_song_emoji.json')
  .then(res => res.json())
  .then(data => {
      allSongs = data || [];
      if(allSongs.length === 0){
          console.error("No songs found in JSON!");
          return;
      }
      startGame();
  })  
  .catch(err => console.error("Failed to load JSON:", err));

function startGame() {
    if(!allSongs.length) return;  // safety check
    gameSongs = allSongs.sort(() => 0.5 - Math.random()).slice(0, 10);
    currentIndex = 0;
    score = 0;
    loadNextSong();
}

function loadNextSong() {
    if (!gameSongs || gameSongs.length === 0) return;
    if (currentIndex >= gameSongs.length) {
        showScorePopup();
        return;
    }

    const song = gameSongs[currentIndex];
    // Only show emojis on front initially
    const front = document.getElementById("emoji-display");
    const back = document.getElementById("song-answer");

    front.innerText = song.emojis;
    back.innerText = "";  // CLEAR the back initially
    document.getElementById("guess-input").value = '';
    document.getElementById("emoji-card").classList.remove("flipped");
}

// Check guess
function checkGuess() {
    const guess = document.getElementById("guess-input").value.trim().toLowerCase();
    if(!guess) return;
    const song = gameSongs[currentIndex];
    flipCard();
    if(guess === song.name.toLowerCase()) {
        score++;
        launchConfetti();
    }
    setTimeout(() => {
        currentIndex++;
        loadNextSong();
    }, 1500);
}

// Skip song
function skipSong() {
    flipCard();
    setTimeout(() => {
        currentIndex++;
        loadNextSong();
    }, 1500);
}

// Flip card
function flipCard() {
    const card = document.getElementById("emoji-card");
    const song = gameSongs[currentIndex];

    // Start flip animation
    card.classList.add("flipped");

    // Populate back content slightly after animation starts
    setTimeout(() => {
        document.getElementById("song-answer").innerText = song.name;
    }, 150); // 150ms delay matches flip animation timing
}

// Confetti
function launchConfetti() {
    confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 }
    });
}

// Score popup
function showScorePopup() {
  document.getElementById("final-score").innerText = score;
  const popup = document.getElementById("score-popup");
  popup.style.display = "flex";
  popup.classList.add("active");   // add pointer events
}

async function submitScore() {
    const username = document.getElementById("username-input").value.trim() || "Anonymous";
    const isTop = await saveScore(username, score, GAME_NAME);
    showPostGameMenu(isTop);
}

async function skipUsername() {
    const isTop = await saveScore("Anonymous", score, GAME_NAME);
    showPostGameMenu(isTop);
}

function showPostGameMenu(isTop) {
    document.getElementById("username-input").style.display = 'none';
    document.querySelector("#score-popup button[onclick='submitScore()']").style.display = 'none';
    document.querySelector("#score-popup button[onclick='skipUsername()']").style.display = 'none';

    const menu = document.getElementById("post-game-menu");
    menu.style.display = 'block';

    if (isTop) launchConfetti(500);
}

async function saveScore(username, score, gameName) {
    try {
        const res = await fetch('/submit_score', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ game: gameName, username, score })
        });

        if (!res.ok) {
            const text = await res.text();
            console.error("Server returned error:", text);
            return false;
        }

        const data = await res.json();
        displayLeaderboard(data.leaderboard || []);
        return data.leaderboard[0]?.score === score;
    } catch (err) {
        console.error("Error saving score:", err);
        return false;
    }
}

function closePopup() {
  const popup = document.getElementById("score-popup");
  popup.classList.remove("active"); // hide again
  startGame();
}

function displayLeaderboard(leaderboard) {
    const list = document.getElementById("leaderboard");
    list.innerHTML = "";
    if (!leaderboard.length) {
        list.innerHTML = "<li>No scores yet!</li>";
        return;
    }

    leaderboard.forEach((entry, i) => {
        const li = document.createElement("li");
        li.innerText = `${i + 1}️⃣ ${entry.username} — ${entry.score}`;
        if (i === 0) li.style.border = "2px solid gold";
        else if (i === 1) li.style.border = "2px solid silver";
        else if (i === 2) li.style.border = "2px solid #cd7f32";
        list.appendChild(li);
    });
}

// Post-game menu actions
function goHome(){
    window.location.href = '/';  // adjust as needed
}
function goGames(){
    window.location.href = '/games';  // adjust as needed
}

function playAgain(){
  // Reset popup UI
  const popup = document.getElementById("score-popup");
  popup.style.display = 'none';
  popup.classList.remove("active");

  const usernameInput = document.getElementById("username-input");
  usernameInput.style.display = 'inline-block';
  usernameInput.value = '';

  document.querySelector("#score-popup button[onclick='submitScore()']").style.display = 'inline-block';
  document.querySelector("#score-popup button[onclick='skipUsername()']").style.display = 'inline-block';
  document.getElementById("post-game-menu").style.display = 'none';

  startGame(); // reset the game
}

window.onload = async function() {
    try {
        const res = await fetch(`/leaderboard/${GAME_NAME}`);
        if (!res.ok) {
            console.error("Failed to fetch leaderboard:", await res.text());
            return;
        }
        const data = await res.json();
        displayLeaderboard(data);
    } catch (err) {
        console.error("Failed to load leaderboard:", err);
    }
}