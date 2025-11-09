document.addEventListener("DOMContentLoaded", () => {
  const startBtn = document.getElementById("startHuntBtn");
  const popup = document.getElementById("ghostyPopupOverlay");
  const audio = document.getElementById("halloweenAudio");

  // ---------------------- CONFIG ----------------------
  const totalIconsAvailable = 14;
  const totalToFind = 10;
  const redirectUrl = "/halloween-special";
  const gamesPage = "/games";
  const huntPages = [
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

  // ---------------------- INITIALIZE ICONS ----------------------
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
    if (counterText)
      counterText.textContent = `🎃 Found: ${foundIcons.length} / ${totalToFind}`;
  }

  function createCounter() {
    if (document.querySelector(".halloween-counter")) return;

    const counter = document.createElement("div");
    counter.className = "halloween-counter";
    counter.style.cssText = `
      position: fixed; bottom: 20px; right: 20px;
      background: rgba(0,0,0,0.8); color: #fff;
      padding: 12px 18px; border-radius: 14px;
      display: flex; align-items: center; justify-content: center; gap: 10px;
      z-index: 9999; font-size: 18px; box-shadow: 0 0 15px #ff6600;
    `;
    counter.innerHTML = `<span class="counter-text">🎃 Found: ${foundIcons.length} / ${totalToFind}</span>`;

    const restartBtn = document.createElement("button");
    restartBtn.textContent = "↻ Restart";
    restartBtn.style.cssText = `
      background:rgb(60, 171, 79); color: white; border: none;
      padding: 6px 14px; border-radius: 8px; cursor: pointer;
      font-size: 16px; font-family: 'Creepster', cursive;
    `;
    restartBtn.onclick = () => {
      if (confirm("Restart the Hunt?")) {
        localStorage.clear();
        sessionStorage.clear();
        window.location.reload();
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
        localStorage.setItem("gameActive", false);
        localStorage.removeItem("foundIcons");
        localStorage.removeItem("chosenIcons");
        sessionStorage.clear();
        popup.style.display = "flex";
        window.location.href = "/"; 
      }
    };

    const backBtn = document.createElement("button");
    backBtn.textContent = "👾 Back to Games";
    backBtn.style.cssText = `
      background: #9b5de5; color: white; border: none;
      padding: 6px 14px; border-radius: 8px; cursor: pointer;
      font-size: 16px; font-family: 'Creepster', cursive;
    `;
    backBtn.onclick = () => (window.location.href = gamesPage);

    counter.appendChild(restartBtn);
    counter.appendChild(exitBtn);
    counter.appendChild(backBtn);
    document.body.appendChild(counter);
  }

  // ---------------------- SPAWN ICONS ----------------------
  function spawnIcons() {
    if (!huntPages.includes(currentPath)) return;

    const availableIcons = chosenIcons.filter(i => !foundIcons.includes(i));
    if (!availableIcons.length) return;

    const iconsToShow = Math.min(availableIcons.length, 1);

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

      img.addEventListener("click", () => {
        const chime = new Audio("/static/audio/spooky-chimes.mp3");
        chime.play();

        foundIcons.push(iconNum);
        localStorage.setItem("foundIcons", JSON.stringify(foundIcons));
        updateCounter();
        img.remove();

        if (foundIcons.length >= totalToFind) {
          alert(`🎉 You found all ${totalToFind}! Ghosty’s secret awaits...`);
          localStorage.setItem("gameActive", false);
          window.location.href = redirectUrl;
        }
      });

      document.body.appendChild(img);
    }
  }

  // ---------------------- INSTRUCTIONS ----------------------
  function showInstructions() {
    if (document.querySelector(".welcome-overlay")) return;

    const overlay = document.createElement("div");
    overlay.className = "welcome-overlay";
    overlay.style.cssText = `
      position: fixed; top: 0; left: 0; width: 100%; height: 100%;
      background: rgba(0, 0, 0, 0.85);
      color: #fff; display: flex;
      flex-direction: column; justify-content: center; align-items: center;
      text-align: center; z-index: 9998; padding: 40px;
      backdrop-filter: blur(6px);
    `;

    const title = document.createElement("h1");
    title.textContent = "🎃 How the Hunt Works 🎃";
    title.style.cssText = `
      font-size: 48px; margin-bottom: 20px;
      color: #ff6600; font-family: 'Creepster', cursive;
      text-shadow: 2px 2px 6px #000;
    `;

    const description = document.createElement("p");
    description.innerHTML = `
      👻 Ghosty has hidden spooky icons across Taekook Universe pages!<br>
      🎯 Find at least 10 icons to unlock the secret.<br>
      🕵️‍♀️ Click the icons when you spot them to add to your collection.<br>
      💫 Explore different pages — each click counts!<br><br>
      Keep your eyes sharp!
    `;
    description.style.cssText = `
      font-size: 22px; color: #46ce5d; line-height: 1.6;
      max-width: 700px; font-family: 'Creepster', cursive;
      text-shadow: 1px 1px 4px #000; margin: 0 auto;
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
      localStorage.setItem("gameActive", true);
      createCounter();
      showInstructions();
      spawnIcons();
    });
  }

  // ---------------------- RESTORE ON RELOAD ----------------------
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