// Scatters slowly spinning currency symbols behind the page (teal + coral theme).
(function () {
  const SYMBOLS = ["₹", "$", "€", "£", "¥"];
  const COLORS = ["#FB7185", "#FBBF24", "#5EEAD4", "#FDBA74", "#A7F3D0"];
  const COUNT = 40;

  const layer = document.getElementById("symbol-bg");
  if (!layer) return;

  let seed = 24;
  function rand() {
    seed = (seed * 9301 + 49297) % 233280;
    return seed / 233280;
  }

  for (let i = 0; i < COUNT; i++) {
    const s = document.createElement("span");
    s.className = "sym";
    s.textContent = SYMBOLS[i % SYMBOLS.length];
    s.style.left = rand() * 97 + "%";
    s.style.top = rand() * 95 + "%";
    s.style.fontSize = 10 + Math.round(rand() * 6) + "px";
    s.style.color = COLORS[Math.floor(rand() * COLORS.length)];
    s.style.animationDuration = 6 + Math.round(rand() * 12) + "s";
    s.style.animationDirection = rand() > 0.5 ? "reverse" : "normal";
    layer.appendChild(s);
  }
})();
