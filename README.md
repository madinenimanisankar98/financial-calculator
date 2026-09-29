# Financial Calculator PRO

A beginner-friendly financial calculator web app built with Flask, HTML5, CSS3,
JavaScript, and Chart.js. College mini-project.

## Features

- **Savings Calculator** — how long until you reach a savings goal, with a
  target-deadline comparison, a doughnut chart, and a savings timeline.
- **EMI Calculator** — monthly loan payment, total interest, and remaining
  balance after partial repayment, with a principal/interest doughnut and an
  amortization chart.
- **GST Calculator** — add or extract GST at 5/12/18/28% or a custom rate.
- **Percentage Calculator** — quick percentage-of-total calculations with a
  gauge chart.
- **Learn section** — plain-language explanations of every formula, in
  English and Telugu (తెలుగు).
- **Ask Questions assistant** — a chat modal that answers savings/EMI/GST/
  budgeting questions. Works offline out of the box; optionally uses the
  Gemini API if you provide a key.
- **Theme** — deep teal and coral, with softly rotating currency symbols in
  the background.

## Project structure

```text
Financial_Calculator_MiniProject/
├── app.py                      # Flask app & REST routes
├── requirements.txt
├── vercel.json                 # Vercel serverless config
├── .env.example
├── api/
│   └── index.py                # Vercel entrypoint
├── backend/
│   ├── calculations.py         # Financial math engine
│   ├── learn_data.py           # English & Telugu Learn content
│   └── ai_helper.py            # Ask Questions logic (offline + Gemini)
├── templates/
│   └── index.html
├── static/
│   ├── css/style.css
│   └── js/
│       ├── script.js
│       ├── charts.js
│       ├── learn.js
│       ├── chart-colors.js
│       └── symbols.js
└── tests/
    └── test_calculations.py
```

## Running locally

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # optional: add GEMINI_API_KEY
python app.py
```

Then open http://localhost:5000

## Running the tests

```bash
pip install pytest
pytest tests/ -v
```

## Deploying to Vercel

1. Push this project to a GitHub repository.
2. Import the repo in Vercel — `vercel.json` routes all requests to
   `api/index.py`, which loads the Flask app.
3. Add `GEMINI_API_KEY` under Vercel's Environment Variables if you want the
   AI assistant to use Gemini instead of its offline answers.

## Notes

- All money values assume Indian Rupees (₹) and GST slabs.
- The EMI formula handles 0% interest loans as a special case (simple
  division) to avoid division by zero.
- The AI assistant works with no API key configured — it falls back to a
  small built-in knowledge base covering savings, EMI, GST, and percentages.
