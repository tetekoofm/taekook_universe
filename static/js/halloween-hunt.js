document.addEventListener("DOMContentLoaded", () => {
  const totalIconsAvailable = 14; // total images
  const totalToFind = 10; // icons to find per hunt
  const redirectUrl = "/halloween-special";

  // Pages where icons can appear
  const pages = [
    "/",
    "/memories",
    "/highlights",
    "/inthenews",
    "/vibe",
    "/projects",
    "/guide",
    "/fanletters",
    "/pride",
    "/meet-tae",
    "/meet-koo",
    "/termsandconditions",
    "/streaming",
    "/buying",
    "/voting",
    "/radio",
    "/shazam",
    "/shazamstats",
    "/spotifystats",
    "/youtubestats",
    "/brandreputation",
    "/events",
    "/reporting",
    "/donating",
    "/fanbases"
  ];

  const currentPath = window.location.pathname;
  if (!pages.includes(currentPath)) return;

  let foundIcons = JSON.parse(localStorage.getItem("foundIcons")) || [];
  let chosenIcons = JSON.parse(localStorage.getItem("chosenIcons"));

  if (!chosenIcons) {
    const allIcons = Array.from({ length: totalIconsAvailable }, (_, i) => i + 1);
    chosenIcons = [];
    while (chosenIcons.length < totalToFind) {
      const random = allIcons.splice(Math.floor(Math.random() * allIcons.length), 1)[0];
      chosenIcons.push(random);
    }
    localStorage.setItem("chosenIcons", JSON.stringify(chosenIcons));
  }

  // --- Floating Counter ---
  const counter = document.createElement("div");
  counter.className = "halloween-counter";
  counter.style.cssText = `
    position: fixed; bottom: 20px; right: 20px;
    background: rgba(0,0,0,0.6); color: #ff6fff;
    padding: 10px 15px; border-radius: 10px; font-size: 18px;
    z-index: 9999; font-family: 'Creepster', cursive;
    display: flex; gap: 8px; align-items: center;
  `;

  const counterText = document.createElement("span");
  counterText.textContent = `🎃 ${foundIcons.length} / ${totalToFind} found`;

  const restartBtn = document.createElement("button");
  restartBtn.textContent = "↻ Restart";
  restartBtn.style.cssText = `
    background: transparent; color: #ff6fff; border: 1px solid #ff6fff;
    border-radius: 6px; cursor: pointer; font-size: 14px; padding: 3px 8px;
  `;
  restartBtn.addEventListener("click", () => {
    if (confirm("Restart the Halloween Hunt?")) {
      localStorage.removeItem("foundIcons");
      localStorage.removeItem("chosenIcons");
      sessionStorage.removeItem("halloweenPopupShown"); // reset popup
      location.reload();
    }
  });

  const skipBtn = document.createElement("button");
  skipBtn.textContent = "🎃 Already Hunted";
  skipBtn.style.cssText = `
    background: #ff6fff; color: #000; border: none; border-radius: 6px;
    cursor: pointer; font-size: 14px; padding: 3px 8px;
  `;
  skipBtn.addEventListener("click", () => window.location.href = redirectUrl);

  counter.appendChild(counterText);
  counter.appendChild(restartBtn);
  counter.appendChild(skipBtn);
  document.body.appendChild(counter);

  // --- Sparkle Animation ---
  const style = document.createElement("style");
  style.textContent = `
    @keyframes sparkleFly {
      0% { transform: scale(1) translate(0,0); opacity:1; }
      100% { transform: scale(0.5) translate(${Math.random()*200-100}px, ${Math.random()*-200}px); opacity:0; }
    }
    .sparkle { position: absolute; width: 8px; height: 8px; border-radius: 50%; background: #ff6fff; z-index: 10000; }
  `;
  document.head.appendChild(style);

  // --- Spawn Icons Function ---
  function spawnIcons() {
    if (foundIcons.length >= totalToFind) return;

    const availableIcons = chosenIcons.filter(i => !foundIcons.includes(i));
    if (availableIcons.length === 0) return;

    const iconNum = availableIcons[Math.floor(Math.random() * availableIcons.length)];
    const img = document.createElement("img");
    img.src = `/static/images/halloween/${iconNum}.png`;
    img.className = "halloween-icon";
    img.style.cssText = `
      position: absolute; width: 100px; height: 100px; cursor: pointer; z-index: 9999;
      filter: invert(1); transition: transform 0.3s ease;
      top: ${Math.random() * (document.body.scrollHeight - 300)}px;
      left: ${Math.random() * (window.innerWidth - 120)}px;
    `;
    img.addEventListener("mouseenter", () => img.style.transform = "scale(1.2)");
    img.addEventListener("mouseleave", () => img.style.transform = "scale(1)");
    document.body.appendChild(img);

    const chime = new Audio("/static/audio/spooky-chimes.mp3");
    img.addEventListener("click", (e) => {
      chime.currentTime = 0;
      chime.play();

      for (let s = 0; s < 10; s++) {
        const sparkle = document.createElement("div");
        sparkle.className = "sparkle";
        sparkle.style.cssText = `
          position: absolute; width: 8px; height: 8px; border-radius: 50%;
          background: #ff6fff; top: ${e.pageY}px; left: ${e.pageX}px;
          opacity: 0.8; z-index: 10000;
          animation: sparkleFly ${0.8 + Math.random()}s ease-out forwards;
        `;
        document.body.appendChild(sparkle);
        setTimeout(() => sparkle.remove(), 1000);
      }

      img.remove();
      foundIcons.push(iconNum);
      localStorage.setItem("foundIcons", JSON.stringify(foundIcons));
      counterText.textContent = `🎃 ${foundIcons.length} / ${totalToFind} found`;

      if (foundIcons.length >= totalToFind) {
        fetch("/unlock_halloween", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ completed: true })
        })
        .then(r => r.ok ? r.json() : Promise.reject("Failed to unlock"))
        .then(() => {
          alert(`🎃 You found all ${totalToFind}! Ghosty’s secret awaits...`);
          window.location.href = redirectUrl;
        })
        .catch(err => console.error("Failed to unlock", err));
      }
    });
  }

  // --- Popup Overlay (Once per session) ---
  if (!sessionStorage.getItem("halloweenPopupShown")) {
    sessionStorage.setItem("halloweenPopupShown", "true"); // mark as shown

    const halloweenAudio = new Audio("/static/audio/halloween.mp3");
    const homepageMusic = window.homepageMusic || null;

    const popup = document.createElement("div");
    popup.id = "ghostyPopupOverlay";
    popup.style.cssText = `
      position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
      background: rgba(0,0,0,0.85); display: flex; justify-content: center;
      align-items: center; z-index: 10000; flex-direction: column;
      color: #7CFC00; font-family: 'Creepster', cursive; text-align: center;
      padding: 20px;
    `;

    const title = document.createElement("h1");
    title.textContent = "🎃 Welcome to Ghosty's Halloween Hunt! 🎃";
    title.style.marginBottom = "15px";

    const description = document.createElement("p");
    description.innerHTML = `
      Find Our Ghosty! 👻<br>
      Oh no! Ghosty, our mischievous admin, is missing on her birthday!<br>
      She left behind clues and emojis, floating away with her magical friends<br>
      <strong>Ms. Catty 🐱</strong> and <strong>Mr. Batty 🦇</strong>.<br>
      Can you find her before the Halloween party begins? Your trick-or-treating adventure starts now!
    `;
    description.style.cssText = `
      font-size: 25px; line-height: 2; letter-spacing: 1px;
      text-shadow: 1px 1px 4px #000; margin-bottom: 25px;
    `;

    const startBtn = document.createElement("button");
    startBtn.textContent = "Start Hunt";
    startBtn.style.cssText = `
      padding: 12px 24px; font-size: 18px;
      background: #ff6fff; color: #000; border: none; border-radius: 10px;
      cursor: pointer;
    `;

    popup.appendChild(title);
    popup.appendChild(description);
    popup.appendChild(startBtn);
    document.body.appendChild(popup);

    // Pause homepage music
    if (homepageMusic && !homepageMusic.paused) homepageMusic.pause();

    // Play Halloween music
    halloweenAudio.play().catch(() => {});

    startBtn.addEventListener("click", () => {
      popup.style.display = "none";
      halloweenAudio.pause();
      halloweenAudio.currentTime = 0;
      if (homepageMusic) homepageMusic.play();

      spawnIcons();
    });
  } else {
    // Popup already shown, spawn icons immediately
    spawnIcons();
  }
});
document.addEventListener("DOMContentLoaded", () => {
  const totalIconsAvailable = 14; // total images
  const totalToFind = 10; // icons to find per hunt
  const redirectUrl = "/halloween-special";

  // Pages where icons can appear
  const pages = [
    "/",
    "/memories",
    "/highlights",
    "/inthenews",
    "/vibe",
    "/projects",
    "/guide",
    "/fanletters",
    "/pride",
    "/meet-tae",
    "/meet-koo",
    "/termsandconditions",
    "/streaming",
    "/buying",
    "/voting",
    "/radio",
    "/shazam",
    "/shazamstats",
    "/spotifystats",
    "/youtubestats",
    "/brandreputation",
    "/events",
    "/reporting",
    "/donating",
    "/fanbases"
  ];

  const currentPath = window.location.pathname;
  if (!pages.includes(currentPath)) return;

  let foundIcons = JSON.parse(localStorage.getItem("foundIcons")) || [];
  let chosenIcons = JSON.parse(localStorage.getItem("chosenIcons"));

  if (!chosenIcons) {
    const allIcons = Array.from({ length: totalIconsAvailable }, (_, i) => i + 1);
    chosenIcons = [];
    while (chosenIcons.length < totalToFind) {
      const random = allIcons.splice(Math.floor(Math.random() * allIcons.length), 1)[0];
      chosenIcons.push(random);
    }
    localStorage.setItem("chosenIcons", JSON.stringify(chosenIcons));
  }

  // --- Floating Counter ---
  const counter = document.createElement("div");
  counter.className = "halloween-counter";
  counter.style.cssText = `
    position: fixed; bottom: 20px; right: 20px;
    background: rgba(0,0,0,0.6); color: #ff6fff;
    padding: 10px 15px; border-radius: 10px; font-size: 18px;
    z-index: 9999; font-family: 'Creepster', cursive;
    display: flex; gap: 8px; align-items: center;
  `;

  const counterText = document.createElement("span");
  counterText.textContent = `🎃 ${foundIcons.length} / ${totalToFind} found`;

  const restartBtn = document.createElement("button");
  restartBtn.textContent = "↻ Restart";
  restartBtn.style.cssText = `
    background: transparent; color: #ff6fff; border: 1px solid #ff6fff;
    border-radius: 6px; cursor: pointer; font-size: 14px; padding: 3px 8px;
  `;
  restartBtn.addEventListener("click", () => {
    if (confirm("Restart the Halloween Hunt?")) {
      localStorage.removeItem("foundIcons");
      localStorage.removeItem("chosenIcons");
      sessionStorage.removeItem("halloweenPopupShown"); // reset popup
      location.reload();
    }
  });

  const skipBtn = document.createElement("button");
  skipBtn.textContent = "🎃 Already Hunted";
  skipBtn.style.cssText = `
    background: #ff6fff; color: #000; border: none; border-radius: 6px;
    cursor: pointer; font-size: 14px; padding: 3px 8px;
  `;
  skipBtn.addEventListener("click", () => window.location.href = redirectUrl);

  counter.appendChild(counterText);
  counter.appendChild(restartBtn);
  counter.appendChild(skipBtn);
  document.body.appendChild(counter);

  // --- Sparkle Animation ---
  const style = document.createElement("style");
  style.textContent = `
    @keyframes sparkleFly {
      0% { transform: scale(1) translate(0,0); opacity:1; }
      100% { transform: scale(0.5) translate(${Math.random()*200-100}px, ${Math.random()*-200}px); opacity:0; }
    }
    .sparkle { position: absolute; width: 8px; height: 8px; border-radius: 50%; background: #ff6fff; z-index: 10000; }
  `;
  document.head.appendChild(style);

  // --- Spawn Icons Function ---
  function spawnIcons() {
    if (foundIcons.length >= totalToFind) return;

    const availableIcons = chosenIcons.filter(i => !foundIcons.includes(i));
    if (availableIcons.length === 0) return;

    const iconNum = availableIcons[Math.floor(Math.random() * availableIcons.length)];
    const img = document.createElement("img");
    img.src = `/static/images/halloween/${iconNum}.png`;
    img.className = "halloween-icon";
    img.style.cssText = `
      position: absolute; width: 100px; height: 100px; cursor: pointer; z-index: 9999;
      filter: invert(1); transition: transform 0.3s ease;
      top: ${Math.random() * (document.body.scrollHeight - 300)}px;
      left: ${Math.random() * (window.innerWidth - 120)}px;
    `;
    img.addEventListener("mouseenter", () => img.style.transform = "scale(1.2)");
    img.addEventListener("mouseleave", () => img.style.transform = "scale(1)");
    document.body.appendChild(img);

    const chime = new Audio("/static/audio/spooky-chimes.mp3");
    img.addEventListener("click", (e) => {
      chime.currentTime = 0;
      chime.play();

      for (let s = 0; s < 10; s++) {
        const sparkle = document.createElement("div");
        sparkle.className = "sparkle";
        sparkle.style.cssText = `
          position: absolute; width: 8px; height: 8px; border-radius: 50%;
          background: #ff6fff; top: ${e.pageY}px; left: ${e.pageX}px;
          opacity: 0.8; z-index: 10000;
          animation: sparkleFly ${0.8 + Math.random()}s ease-out forwards;
        `;
        document.body.appendChild(sparkle);
        setTimeout(() => sparkle.remove(), 1000);
      }

      img.remove();
      foundIcons.push(iconNum);
      localStorage.setItem("foundIcons", JSON.stringify(foundIcons));
      counterText.textContent = `🎃 ${foundIcons.length} / ${totalToFind} found`;

      if (foundIcons.length >= totalToFind) {
        fetch("/unlock_halloween", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ completed: true })
        })
        .then(r => r.ok ? r.json() : Promise.reject("Failed to unlock"))
        .then(() => {
          alert(`🎃 You found all ${totalToFind}! Ghosty’s secret awaits...`);
          window.location.href = redirectUrl;
        })
        .catch(err => console.error("Failed to unlock", err));
      }
    });
  }

  // --- Popup Overlay (Once per session) ---
  if (!sessionStorage.getItem("halloweenPopupShown")) {
    sessionStorage.setItem("halloweenPopupShown", "true"); // mark as shown

    const halloweenAudio = new Audio("/static/audio/halloween.mp3");
    const homepageMusic = window.homepageMusic || null;

    const popup = document.createElement("div");
    popup.id = "ghostyPopupOverlay";
    popup.style.cssText = `
      position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
      background: rgba(0,0,0,0.85); display: flex; justify-content: center;
      align-items: center; z-index: 10000; flex-direction: column;
      font-family: 'Creepster', cursive; text-align: center;
      padding: 20px;
    `;

    const title = document.createElement("h1");
    title.textContent = "🎃 Welcome to Ghosty's Halloween Hunt! 🎃";
    title.style.marginBottom = "15px";

    const description = document.createElement("p");
    description.innerHTML = `
      Find Our Ghosty! 👻<br>
      Oh no! Ghosty, our mischievous admin, is missing on her birthday!<br>
      She left behind clues and emojis, floating away with her magical friends<br>
      <strong>Ms. Catty 🐱</strong> and <strong>Mr. Batty 🦇</strong>.<br>
      Can you find her before the Halloween party begins? Your trick-or-treating adventure starts now!
    `;
    description.style.cssText = `
      font-size: 25px;
      line-height: 2;
      letter-spacing: 1px;
      color: #7CFC00 !important;  /* force green */
      text-shadow: 1px 1px 4px #000;
      font-family: 'Creepster', cursive !important;
      margin-bottom: 25px;
    `;
  
    const startBtn = document.createElement("button");
    startBtn.textContent = "Start Hunt";
    startBtn.style.cssText = `
      padding: 12px 24px; font-size: 18px;
      background: #ff6fff; color: #000; border: none; border-radius: 10px;
      cursor: pointer; font-family: 'Creepster', cursive;
    `;

    popup.appendChild(title);
    popup.appendChild(description);
    popup.appendChild(startBtn);
    document.body.appendChild(popup);

    // Pause homepage music
    if (homepageMusic && !homepageMusic.paused) homepageMusic.pause();

    // Play Halloween music
    halloweenAudio.play().catch(() => {});

    startBtn.addEventListener("click", () => {
      popup.style.display = "none";
      halloweenAudio.pause();
      halloweenAudio.currentTime = 0;
      if (homepageMusic) homepageMusic.play();

      spawnIcons();
    });
  } else {
    // Popup already shown, spawn icons immediately
    spawnIcons();
  }
});
