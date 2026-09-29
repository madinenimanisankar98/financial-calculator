// Chart colors for the Deep Teal + Coral theme.
// Charts sit inside dark teal cards, so these are light/bright colors that read well on #0B3F4A.
const THEME_COLORS = {
  savings: "#5EEAD4",
  expenses: "#FB7185",
  principal: "#5EEAD4",
  interest: "#FB7185",
  percent: "#FDBA74",
  track: "#164C56",
  grid: "#164C56",
  text: "#E6FBF8",
};

if (window.Chart) {
  Chart.defaults.color = THEME_COLORS.text;
  Chart.defaults.borderColor = THEME_COLORS.grid;
  Chart.defaults.font.family = '"Inter", system-ui, sans-serif';
}
