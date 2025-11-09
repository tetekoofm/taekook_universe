document.addEventListener("DOMContentLoaded", () => {
  const startBtn = document.getElementById("startHuntBtn");
  const popup = document.getElementById("ghostyPopupOverlay");
  const audio = document.getElementById("halloweenAudio");

  // ---------------------- CONFIG ----------------------
  const totalIconsAvailable = 14;
  const totalToFind = 10;
  const redirectUrl = "/halloween-special";
  const gamesPage = "/games";
  const pages = [
    "/", "/memories", "/upcoming", "/highlights", "/recap", "/inthenews", "/vibe",
    "/projects", "/guide", "/fanletters", "/pride", "/meet-tae",
    "/meet-koo", "/termsandconditions", "/streaming", "/buying",
    "/voting", "/radio", "/shazam", "/shazamstats", "/spotifystats",
    "/youtubestats", "/brandreputation", "/events", "/reporting",
    "/donating", "/fanbases", "/games"
  ];

  const currentPath = window.location.pathname;

  // ---------------------- STATE ----------------------
  let foundIcons = JSON.parse(localStorage.getItem("foundIcons")) || [];
  let chosenIcons = JSON.parse(localStorage.getItem("chosenIcons"));
  let gameActive = JSON.parse(localStorage.getItem("gameActive")) ?? false;

  if (!chosenIcons) {
    const allIcons = Array.from({ length: totalIconsAvailable }, (_, i) => i + 1);
    chosenIcons = [];
    while (chosenIcons.length < totalToFind) {
      const random = allIcons.splice(Math.floor(Math.random() * allIcons.length), 1)[0];
      chosenIcons.push(random);
    }
    localStorage.setItem("chosenIcons", JSON.stringify(chosenIcons));
  }

  // ---------------------- COUNTER ----------------------
  function updateCounter() {
    const counterText = document.querySelector(".counter-text");
    if (counterText) counterText.textContent = `🎃 Found: ${foundIcons.length} / ${totalToFind}`;
  }

  const fontLink = document.createElement('link');
  fontLink.href = "https://fonts.googleapis.com/css2?family=Creepster&display=swap";
  fontLink.rel = "stylesheet";
  document.head.appendChild(fontLink);

  function createCounter() {
    if (!document.querySelector(".halloween-counter")) {
      const counter = document.createElement("div");
      counter.className = "halloween-counter";
      counter.style.cssText = `
        position: fixed; bottom: 20px; right: 20px;
        background: rgba(0,0,0,0.75); color: #fff;
        padding: 12px 18px; border-radius: 14px;
        display: flex; align-items: center; justify-content: center; gap: 12px;
        z-index: 9999; font-size: 18px; box-shadow: 0 0 15px #ff6600;
      `;
      counter.innerHTML = `<span class="counter-text">🎃 Found: ${foundIcons.length} / ${totalToFind}</span>`;

      const restartBtn = document.createElement("button");
      restartBtn.textContent = "↻ Restart";
      restartBtn.style.cssText = `
        background:rgb(60, 171, 79); color: white; border: none;
        padding: 6px 14px; border-radius: 8px; cursor: pointer;
        width: 140px; line-height: 1.5; vertical-align: middle;
        font-size: 16px; font-family: 'Creepster', cursive;
      `;
      restartBtn.onclick = () => {
        if (confirm("Restart the Hunt?")) {
          foundIcons = [];
          localStorage.setItem("foundIcons", JSON.stringify(foundIcons));
          localStorage.setItem("gameActive", true);
          spawnIcons();
          updateCounter();
        }
      };

      const exitBtn = document.createElement("button");
      exitBtn.textContent = "⛔ Exit";
      exitBtn.style.cssText = `
        background:rgb(57, 166, 224); color: white; border: none;
        padding: 6px 14px; border-radius: 8px; cursor: pointer;
        font-family: 'Creepster', cursive;
      `;
      exitBtn.onclick = () => {
        if (confirm("Exit the Halloween Hunt?")) {
          document.querySelectorAll(".halloween-icon").forEach(i => i.remove());
          counter.remove();
          if (audio) {
            audio.pause();
            audio.currentTime = 0;
          }
          localStorage.removeItem("foundIcons");
          localStorage.removeItem("chosenIcons");
          localStorage.setItem("gameActive", false);
          sessionStorage.clear();
          popup.style.display = "flex";
        }
      };

      const backBtn = document.createElement("button");
      backBtn.textContent = "👾 Back to Games";
      backBtn.style.cssText = `
        background: #9b5de5; color: white; border: none;
        padding: 6px 14px; border-radius: 8px; cursor: pointer;
        width: 140px; line-height: 1.5; vertical-align: middle;
        font-size: 16px; font-family: 'Creepster', cursive;
      `;
      backBtn.onclick = () => window.location.href = gamesPage;

      counter.appendChild(restartBtn);
      counter.appendChild(exitBtn);
      counter.appendChild(backBtn);
      document.body.appendChild(counter);
    }
  }

  // ---------------------- ICONS ----------------------
  function spawnIcons() {
    if (!pages.includes(currentPath)) return;

    const availableIcons = chosenIcons.filter(i => !foundIcons.includes(i));
    if (!availableIcons.length) return;

    const iconsToShow = Math.min(availableIcons.length, Math.floor(Math.random() * 2) + 1);

    for (let i = 0; i < iconsToShow; i++) {
      const iconNum = availableIcons.splice(Math.floor(Math.random() * availableIcons.length), 1)[0];
      const img = document.createElement("img");
      img.src = `/static/images/halloween/${iconNum}.png`;
      img.className = "halloween-icon";
      img.style.position = "fixed";
      img.style.top = `${Math.random() * (window.innerHeight - 100)}px`;
      img.style.left = `${Math.random() * (window.innerWidth - 100)}px`;
      img.style.width = "70px";
      img.style.height = "70px";
      img.style.cursor = "pointer";
      img.style.zIndex = "9000";
      document.body.appendChild(img);

      img.addEventListener("click", (e) => {
        const chime = new Audio("/static/audio/spooky-chimes.mp3");
        chime.play();

        // Sparkles
        for (let s = 0; s < 10; s++) {
          const sparkle = document.createElement("div");
          sparkle.className = "sparkle";
          sparkle.style.setProperty("--tx", `${Math.random() * 200 - 100}px`);
          sparkle.style.setProperty("--ty", `${Math.random() * -200}px`);
          sparkle.style.top = e.pageY + "px";
          sparkle.style.left = e.pageX + "px";
          sparkle.style.animation = `sparkleFly ${0.8 + Math.random()}s ease-out forwards`;
          document.body.appendChild(sparkle);
          setTimeout(() => sparkle.remove(), 1000);
        }

        foundIcons.push(iconNum);
        localStorage.setItem("foundIcons", JSON.stringify(foundIcons));
        updateCounter();
        img.remove();

        if (foundIcons.length >= totalToFind) {
          alert(`🎉 You found all ${totalToFind}! Ghosty’s secret awaits...`);
        
          // Stop the game
          document.querySelectorAll(".halloween-icon").forEach(i => i.remove());
          const counter = document.querySelector(".halloween-counter");
          if (counter) counter.remove();
        
          if (audio) {
            audio.pause();
            audio.currentTime = 0;
          }
        
          // Delay redirect slightly
          setTimeout(() => {
            // Clear storage
            localStorage.removeItem("foundIcons");
            localStorage.removeItem("chosenIcons");
            localStorage.setItem("gameActive", false);
            sessionStorage.clear();
        
            // Redirect
            window.location.href = redirectUrl;
          }, 50); // 50ms is enough
        }
      });
    }
  }

  // ---------------------- INSTRUCTIONS ----------------------
  function showInstructions() {
    if (document.querySelector(".welcome-overlay")) return;

    const overlay = document.createElement("div");
    overlay.className = "welcome-overlay";
    overlay.style.cssText = `
      position: fixed; top: 0; left: 0; width: 100%; height: 100%;
      background: rgba(0, 0, 0, 0.75); color: #fff;
      display: flex; flex-direction: column; justify-content: center; align-items: center;
      text-align: center; z-index: 9998; padding: 40px;
      backdrop-filter: blur(6px);
    `;

    const title = document.createElement("h1");
    title.textContent = "🎃 How the Hunt Works 🎃";
    title.style.marginBottom = "15px";

    const description = document.createElement("p");
    description.innerHTML = `
      👻 Ghosty has hidden spooky icons across Taekook Universe pages!<br>
      🎃 Explore every corner, she loves sneaky spots!<br>
      🕵️‍♀️ Click the icons when you spot them to add to your collection.<br>
      🎯 Find at least 10 icons.<br>
      💫 Each icon you catch gets you closer to Ghosty’s secret surprise!<br><br>
      Keep your eyes sharp, she’s watching from the shadows. 👀
    `;
    description.style.cssText = `
      font-size: 22px; color: rgb(70, 206, 93);
      line-height: 1.6; letter-spacing: 1px; text-shadow: 1px 1px 4px #000;
      max-width: 650px; text-align: center; font-family: 'Creepster', cursive; margin: 0 auto;
    `;

    overlay.appendChild(title);
    overlay.appendChild(description);
    document.body.appendChild(overlay);
  }

  // ---------------------- START THE HUNT ----------------------
  if (startBtn) {
    startBtn.addEventListener("click", () => {
      popup.style.display = "none";
      if (audio) audio.play();

      // Reset game state
      foundIcons = [];
      localStorage.setItem("foundIcons", JSON.stringify(foundIcons));
      localStorage.setItem("gameActive", true);
      localStorage.setItem("foundAll", false);

      showInstructions();
      createCounter();
      spawnIcons();
    });
  }

  // ---------------------- RESTORE STATE ON PAGE RELOAD ----------------------
  if (gameActive) {
    createCounter();
    spawnIcons();
  }
});

  // ---------------------- MOBILE STYLES ----------------------
const mobileStyles = `
@media (max-width: 1024px) {
  #ghostyPopupOverlay, .welcome-overlay {
    top: 50% !important;
    left: 50% !important;
    transform: translate(-50%, -50%) !important;
    width: 80% !important;
    max-width: 700px !important;
    padding: 25px !important;
    overflow-y: auto !important;
  }

  .popup-content, .welcome-overlay {
    padding: 25px !important;
  }

  .ghosty-avatar {
    width: 180px !important;
    height: 180px !important;
    margin-bottom: 20px !important;
  }

  .ghosty-gifs img {
    width: 140px !important;
    height: 140px !important;
    gap: 10px !important;
  }

  #ghostyPopupOverlay h1, .welcome-overlay h1 {
    font-size: 2em !important;
    margin-bottom: 15px !important;
  }

  #ghostyPopupOverlay p, .welcome-overlay p {
    font-size: 1.2em !important;
    line-height: 1.4em !important;
    margin-bottom: 20px !important;
  }

  #startHuntBtn {
    font-size: 1em !important;
    padding: 10px 20px !important;
    margin-top: 12px !important;
  }

  .halloween-counter button {
    font-size: 15px !important;
  }
}

@media (max-width: 768px) {
  #ghostyPopupOverlay, .welcome-overlay {
    top: 50% !important;
    left: 50% !important;
    transform: translate(-50%, -50%) !important; /* center vertically and horizontally */
    width: 90% !important;
    max-width: 320px !important;
    padding: 15px !important;
    overflow-y: auto !important; /* allow scrolling if content is tall */
  }
  
    .popup-content, .welcome-overlay {
    padding: 15px !important;
  }

  .ghosty-avatar {
    width: 120px !important;
    height: 120px !important;
    margin-bottom: 15px !important;
  }

  .ghosty-gifs img {
    width: 100px !important;
    height: 100px !important;
  }

  #ghostyPopupOverlay h1, .welcome-overlay h1 {
    font-size: 1.5em !important;
    margin-bottom: 10px !important;
  }

  #ghostyPopupOverlay p, .welcome-overlay p {
    font-size: 0.95em !important;
    line-height: 1.3em !important;
    margin-bottom: 15px !important;
  }

  #startHuntBtn {
    font-size: 0.9em !important;
    padding: 8px 14px !important;
    margin-top: 10px !important;
  }

  .halloween-counter {
    bottom: 10px !important;
    right: 10px !important;
    padding: 8px 10px !important;
    font-size: 14px !important;
    flex-direction: column !important;
    gap: 6px !important;
    width: auto !important;
  }

  .halloween-counter button {
    width: 80% !important;
    font-size: 10px !important;
    padding: 6px 0 !important;
  }

  .halloween-icon {
    width: 50px !important;
    height: 50px !important;
  }

  .sparkle {
    width: 6px !important;
    height: 6px !important;
  }

  .welcome-overlay h1 {
    font-size: 1.5em !important;
    margin-bottom: 10px !important;
  }

  .welcome-overlay p {
    font-size: 0.9em !important;
    line-height: 1.4em !important;
  }

  #startHuntBtn {
    font-size: 0.9em !important;
    padding: 8px 14px !important;
    margin-top: 10px !important;
  }
}
`;

// Inject into the document head
const styleTag = document.createElement("style");
styleTag.innerHTML = mobileStyles;
document.head.appendChild(styleTag);