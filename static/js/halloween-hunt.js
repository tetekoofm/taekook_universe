document.addEventListener("DOMContentLoaded", () => {
  const totalIcons = 14;
  const redirectUrl = "/halloween-special";

  // List of all pages where icons can appear
  const pages = [
    // "/",
    "/memories",
    "/highlights",
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
    "/brandreputation",
    "/events",
    "/reporting"
]
  // Load found icons from localStorage
  const foundIcons = JSON.parse(localStorage.getItem("foundIcons")) || [];

  // 🌫️ Dynamic purple multi-layer fog
  const fog = document.createElement("div");
  fog.id = "fog-overlay";

  for (let i = 1; i <= 3; i++) {
      const layer = document.createElement("div");
      layer.className = "fog-layer layer" + i;

      // Assign unique animation and duration randomly
      const animName = `floatFog${i}`;
      const duration = 120 + Math.random() * 60; // 120-180s
      layer.style.animation = `${animName} ${duration}s linear infinite`;
      layer.style.opacity = 0.12 + Math.random() * 0.08; // 0.12 - 0.2

      // Slightly randomize background color for variation
      const r = 150 + Math.floor(Math.random()*80);
      const g = 0 + Math.floor(Math.random()*30);
      const b = 100 + Math.floor(Math.random()*80);
      layer.style.background = `radial-gradient(circle, rgba(${r},${g},${b},0.06) 0%, rgba(${r/2},0,${b/2},0.03) 100%)`;

      fog.appendChild(layer);
  }

  // ✅ Append fog to body so it becomes visible
  document.body.appendChild(fog);

  // Counter
  const counter = document.createElement("div");
  counter.className = "halloween-counter";
  counter.innerText = `🎃 ${foundIcons.length} / ${totalIcons} found`;
  document.body.appendChild(counter);

  // Randomly decide if this page gets an icon
  const pageHasIcon = Math.random() < 0.5; // 50% chance to place an icon here
  const remainingIcons = [];
  for (let i = 1; i <= totalIcons; i++) {
      if (!foundIcons.includes(i)) remainingIcons.push(i);
  }

  if (pageHasIcon && remainingIcons.length > 0) {
      const iconNum = remainingIcons[Math.floor(Math.random() * remainingIcons.length)];

      const img = document.createElement("img");
      img.src = `/static/images/halloween/${iconNum}.png`;
      img.className = "halloween-icon";
      img.style.top = (10 + Math.random() * 70) + "%";
      img.style.left = (10 + Math.random() * 70) + "%";
      img.style.position = "fixed";
      img.style.width = "200px";
      img.style.height = "200px";
      img.style.cursor = "pointer";
      img.style.zIndex = 9999;
      img.style.filter = "invert(1)"; // ✅ add reverse colors
      document.body.appendChild(img);
      

      const chime = new Audio("/static/audio/spooky-chimes.mp3");

      img.addEventListener("click", (e) => {
          chime.currentTime = 0;
          chime.play();

          // Sparkle effect
          for (let s = 0; s < 8; s++) {
              const sparkle = document.createElement("div");
              sparkle.className = "sparkle";
              sparkle.style.top = e.pageY + "px";
              sparkle.style.left = e.pageX + "px";
              document.body.appendChild(sparkle);
              setTimeout(() => sparkle.remove(), 800);
          }

          img.remove();
          foundIcons.push(iconNum);
          localStorage.setItem("foundIcons", JSON.stringify(foundIcons));
          counter.innerText = `🎃 ${foundIcons.length} / ${totalIcons} found`;

          if (foundIcons.length >= 10) {
            // Unlock via Flask route
            fetch("/unlock_halloween", { method: "POST" })
              .then(() => {
                alert("🎃 You found all 10! Ghosty’s secret awaits...");
                window.location.href = "/halloween-special";
              });
          }
      });
  }
});
