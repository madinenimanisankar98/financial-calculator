// Chart.js rendering helpers. Each function destroys any previous chart
// instance on the same canvas before drawing, so results can be recalculated
// without leaking chart instances.

const _chartInstances = {};

function _renderChart(canvasId, config) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;
  if (_chartInstances[canvasId]) {
    _chartInstances[canvasId].destroy();
  }
  _chartInstances[canvasId] = new Chart(canvas.getContext("2d"), config);
}

// ---- Savings: expenses vs savings doughnut ----
function renderSavingsDoughnut(expenses, savings) {
  _renderChart("savings-doughnut", {
    type: "doughnut",
    data: {
      labels: ["Expenses", "Available Savings"],
      datasets: [{
        data: [expenses, savings],
        backgroundColor: [THEME_COLORS.expenses, THEME_COLORS.savings],
        borderWidth: 0,
      }],
    },
    options: { plugins: { legend: { position: "bottom" } } },
  });
}

// ---- Savings: accumulation timeline ----
function renderSavingsTimeline(timeline) {
  _renderChart("savings-timeline", {
    type: "line",
    data: {
      labels: timeline.map((_, i) => `M${i + 1}`),
      datasets: [{
        label: "Saved so far (₹)",
        data: timeline,
        borderColor: THEME_COLORS.savings,
        backgroundColor: THEME_COLORS.savings + "33",
        fill: true,
        tension: 0.3,
      }],
    },
    options: {
      plugins: { legend: { display: false } },
      scales: { y: { beginAtZero: true } },
    },
  });
}

// ---- EMI: principal vs interest doughnut ----
function renderEmiDoughnut(principal, interest) {
  _renderChart("emi-doughnut", {
    type: "doughnut",
    data: {
      labels: ["Principal", "Total Interest"],
      datasets: [{
        data: [principal, interest],
        backgroundColor: [THEME_COLORS.principal, THEME_COLORS.interest],
        borderWidth: 0,
      }],
    },
    options: { plugins: { legend: { position: "bottom" } } },
  });
}

// ---- EMI: amortization line ----
function renderEmiAmortization(schedule) {
  _renderChart("emi-amortization", {
    type: "line",
    data: {
      labels: schedule.map((_, i) => `P${i + 1}`),
      datasets: [{
        label: "Remaining balance (₹)",
        data: schedule,
        borderColor: THEME_COLORS.interest,
        backgroundColor: THEME_COLORS.interest + "33",
        fill: true,
        tension: 0.3,
      }],
    },
    options: {
      plugins: { legend: { display: false } },
      scales: { y: { beginAtZero: true } },
    },
  });
}

// ---- GST: base vs tax bar ----
function renderGstBar(basePrice, gstAmount) {
  _renderChart("gst-bar", {
    type: "bar",
    data: {
      labels: ["Base Price", "GST Amount"],
      datasets: [{
        data: [basePrice, gstAmount],
        backgroundColor: [THEME_COLORS.principal, THEME_COLORS.interest],
        borderRadius: 6,
      }],
    },
    options: {
      plugins: { legend: { display: false } },
      scales: { y: { beginAtZero: true } },
    },
  });
}

// ---- Percentage: donut gauge ----
function renderPercentageGauge(percentage) {
  const pct = Math.max(0, Math.min(percentage, 100));
  _renderChart("percentage-gauge", {
    type: "doughnut",
    data: {
      labels: ["Selected", "Remaining"],
      datasets: [{
        data: [pct, 100 - pct],
        backgroundColor: [THEME_COLORS.percent, THEME_COLORS.track],
        borderWidth: 0,
      }],
    },
    options: {
      circumference: 180,
      rotation: 270,
      plugins: { legend: { display: false } },
    },
  });
}
