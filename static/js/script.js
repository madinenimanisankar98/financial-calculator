// Navigation between home and calculator views, form submissions, and the
// Ask Questions chat modal.

const views = ["home", "savings", "emi", "gst", "percentage"];

function showView(name) {
  views.forEach((v) => {
    const el = document.getElementById(`${v}-view`);
    if (el) el.hidden = v !== name;
  });
  window.scrollTo({ top: 0, behavior: "smooth" });
}

document.querySelectorAll(".calc-card").forEach((card) => {
  card.addEventListener("click", () => showView(card.dataset.calc));
});
document.querySelectorAll("[data-back]").forEach((btn) => {
  btn.addEventListener("click", () => showView("home"));
});

// ---- language toggle (drives both the Learn modal and future i18n) ----
document.querySelectorAll(".lang-option").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".lang-option").forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    setLearnLanguage(btn.dataset.lang);
  });
});

// ---- modals ----
document.getElementById("learn-btn").addEventListener("click", openLearnModal);
document.getElementById("ask-ai-btn").addEventListener("click", () => {
  document.getElementById("ai-modal").hidden = false;
});
document.querySelectorAll("[data-close-modal]").forEach((btn) => {
  btn.addEventListener("click", (e) => {
    e.target.closest(".modal").hidden = true;
  });
});
document.querySelectorAll(".modal").forEach((modal) => {
  modal.addEventListener("click", (e) => {
    if (e.target === modal) modal.hidden = true;
  });
});

// ---- helpers ----
function formToJson(form) {
  const obj = {};
  new FormData(form).forEach((value, key) => (obj[key] = value));
  return obj;
}

function moneyFmt(n) {
  return "₹" + Number(n).toLocaleString("en-IN", { maximumFractionDigits: 2 });
}

async function postJson(url, payload) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Something went wrong");
  return data;
}

// ---- Savings form ----
document.getElementById("savings-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const box = document.getElementById("savings-result");
  try {
    const payload = formToJson(e.target);
    const r = await postJson("/api/savings", payload);
    if (r.error) throw new Error(r.error);

    let statusHtml = "";
    if (r.target_comparison) {
      const cls = "status-" + r.target_comparison.status.toLowerCase();
      statusHtml = `
        <div class="result-item">
          <span class="label">Target comparison</span>
          <span class="status-badge ${cls}">${r.target_comparison.status}</span>
          <div style="margin-top:6px;font-size:13px;color:var(--ink-soft);">
            Needs ${moneyFmt(r.target_comparison.required_monthly_savings)}/month for a
            ${r.target_comparison.target_months}-month target.
          </div>
        </div>`;
    }

    box.innerHTML = `
      <h3>Results for "${r.goal_name}"</h3>
      <div class="result-grid">
        <div class="result-item"><span class="label">Available Savings/mo</span><span class="value">${moneyFmt(r.available_savings)}</span></div>
        <div class="result-item"><span class="label">Estimated Time</span><span class="value">${r.years}y ${r.remaining_months}m</span></div>
        <div class="result-item"><span class="label">Total Days</span><span class="value">${r.total_days}</span></div>
        ${statusHtml}
      </div>
      <div class="progress-track"><div class="progress-fill" id="savings-progress"></div></div>
      <div class="chart-wrap"><canvas id="savings-doughnut"></canvas></div>
      <div class="chart-wrap"><canvas id="savings-timeline"></canvas></div>
    `;
    box.hidden = false;

    renderSavingsDoughnut(Number(payload.monthly_expenses), r.available_savings);
    renderSavingsTimeline(r.timeline);
    requestAnimationFrame(() => {
      document.getElementById("savings-progress").style.width = "100%";
    });
  } catch (err) {
    box.hidden = false;
    box.innerHTML = `<p style="color:var(--accent)">${err.message}</p>`;
  }
});

// ---- EMI form ----
document.getElementById("emi-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const box = document.getElementById("emi-result");
  try {
    const payload = formToJson(e.target);
    const r = await postJson("/api/emi", payload);
    if (r.error) throw new Error(r.error);

    box.innerHTML = `
      <h3>EMI Breakdown</h3>
      <div class="result-grid">
        <div class="result-item"><span class="label">Monthly EMI</span><span class="value">${moneyFmt(r.emi)}</span></div>
        <div class="result-item"><span class="label">Total Payable</span><span class="value">${moneyFmt(r.total_payable)}</span></div>
        <div class="result-item"><span class="label">Total Interest</span><span class="value">${moneyFmt(r.total_interest)}</span></div>
        ${r.remaining_balance !== null ? `<div class="result-item"><span class="label">Remaining Balance</span><span class="value">${moneyFmt(r.remaining_balance)}</span></div>` : ""}
      </div>
      <div class="chart-wrap"><canvas id="emi-doughnut"></canvas></div>
      <div class="chart-wrap"><canvas id="emi-amortization"></canvas></div>
    `;
    box.hidden = false;

    renderEmiDoughnut(Number(payload.principal), r.total_interest);
    renderEmiAmortization(r.amortization);
  } catch (err) {
    box.hidden = false;
    box.innerHTML = `<p style="color:var(--accent)">${err.message}</p>`;
  }
});

// ---- GST form ----
document.querySelectorAll(".chip[data-gst]").forEach((chip) => {
  chip.addEventListener("click", () => {
    document.querySelectorAll(".chip[data-gst]").forEach((c) => c.classList.remove("active"));
    chip.classList.add("active");
    document.querySelector('#gst-form input[name="gst_percent"]').value = chip.dataset.gst;
  });
});

document.getElementById("gst-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const box = document.getElementById("gst-result");
  try {
    const payload = formToJson(e.target);
    if (payload.gst_percent_custom) {
      payload.gst_percent = payload.gst_percent_custom;
    }
    delete payload.gst_percent_custom;
    const r = await postJson("/api/gst", payload);
    if (r.error) throw new Error(r.error);

    box.innerHTML = `
      <h3>${r.product_name ? r.product_name : "GST"} Breakdown</h3>
      <div class="result-grid">
        <div class="result-item"><span class="label">Base Price</span><span class="value">${moneyFmt(r.base_price)}</span></div>
        <div class="result-item"><span class="label">GST (${r.gst_percent}%)</span><span class="value">${moneyFmt(r.gst_amount)}</span></div>
        <div class="result-item"><span class="label">Final Price</span><span class="value">${moneyFmt(r.final_price)}</span></div>
      </div>
      <div class="chart-wrap"><canvas id="gst-bar"></canvas></div>
    `;
    box.hidden = false;
    renderGstBar(r.base_price, r.gst_amount);
  } catch (err) {
    box.hidden = false;
    box.innerHTML = `<p style="color:var(--accent)">${err.message}</p>`;
  }
});

// ---- Percentage form ----
document.getElementById("percentage-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const box = document.getElementById("percentage-result");
  try {
    const payload = formToJson(e.target);
    const r = await postJson("/api/percentage", payload);
    if (r.error) throw new Error(r.error);

    box.innerHTML = `
      <div class="result-grid">
        <div class="result-item"><span class="label">${r.percentage}% of ${moneyFmt(r.total)}</span><span class="value">${moneyFmt(r.value)}</span></div>
        <div class="result-item"><span class="label">Remainder</span><span class="value">${moneyFmt(r.remainder)}</span></div>
      </div>
      <div class="chart-wrap"><canvas id="percentage-gauge"></canvas></div>
    `;
    box.hidden = false;
    renderPercentageGauge(r.percentage);
  } catch (err) {
    box.hidden = false;
    box.innerHTML = `<p style="color:var(--accent)">${err.message}</p>`;
  }
});

// ---- Ask AI chat ----
document.getElementById("ai-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const input = document.getElementById("ai-question");
  const log = document.getElementById("ai-chat-log");
  const question = input.value.trim();
  if (!question) return;

  log.insertAdjacentHTML("beforeend", `<div class="ai-msg user">${question}</div>`);
  input.value = "";
  log.scrollTop = log.scrollHeight;

  try {
    const res = await fetch("/api/ask-ai", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });
    const data = await res.json();
    log.insertAdjacentHTML("beforeend", `<div class="ai-msg bot">${data.answer}</div>`);
  } catch {
    log.insertAdjacentHTML("beforeend", `<div class="ai-msg bot">Sorry, something went wrong. Please try again.</div>`);
  }
  log.scrollTop = log.scrollHeight;
});
