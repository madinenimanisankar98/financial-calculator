// Handles the Learn modal: fetches bilingual content and renders it.

let currentLang = "en";
let learnCache = {};

async function loadLearnContent(lang) {
  if (learnCache[lang]) return learnCache[lang];
  const res = await fetch(`/api/learn?lang=${lang}`);
  const data = await res.json();
  learnCache[lang] = data;
  return data;
}

function renderLearnContent(data) {
  const body = document.getElementById("learn-body");
  const order = ["savings", "emi", "gst", "percentage"];
  body.innerHTML = order
    .map((key) => {
      const topic = data[key];
      if (!topic) return "";
      const terms = topic.terms
        .map(([term, def]) => `<li><strong>${term}:</strong> ${def}</li>`)
        .join("");
      return `
        <div class="learn-topic">
          <h3>${topic.title}</h3>
          <div class="formula">${topic.formula}</div>
          <ul>${terms}</ul>
          <p class="example">${topic.example}</p>
          <p class="tip">💡 ${topic.tip}</p>
        </div>`;
    })
    .join("");
}

async function openLearnModal() {
  const data = await loadLearnContent(currentLang);
  renderLearnContent(data);
  document.getElementById("learn-modal").hidden = false;
}

function setLearnLanguage(lang) {
  currentLang = lang;
  if (!document.getElementById("learn-modal").hidden) {
    loadLearnContent(lang).then(renderLearnContent);
  }
}
