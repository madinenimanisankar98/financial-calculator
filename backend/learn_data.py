"""
Educational content for the Learn section, in English and simple Telugu.
Structure: LEARN_CONTENT[lang][calculator_key] = {title, formula, terms, example, tip}
"""

LEARN_CONTENT = {
    "en": {
        "savings": {
            "title": "Savings Calculator",
            "formula": "Available Savings = Monthly Income − Monthly Expenses\n"
                       "Estimated Months = Goal Price ÷ Available Savings",
            "terms": [
                ("Available Savings", "The money left over each month after expenses."),
                ("Goal Price", "The total amount you need to reach your goal."),
                ("Target Comparison", "Checks if your current savings rate meets a deadline you set."),
            ],
            "example": "If you earn ₹30,000 and spend ₹22,000 a month, you save ₹8,000/month. "
                       "A ₹96,000 goal would take about 12 months.",
            "tip": "Small, consistent savings beat large, irregular ones. Automate a fixed "
                   "transfer right after payday.",
        },
        "emi": {
            "title": "EMI Calculator",
            "formula": "EMI = P × [r × (1+r)^n] ÷ [(1+r)^n − 1]\n"
                       "r = (Annual Rate ÷ 12) ÷ 100, n = total number of months",
            "terms": [
                ("Principal (P)", "The amount you borrow."),
                ("Rate (r)", "The interest rate charged per month."),
                ("Tenure (n)", "The total number of months to repay the loan."),
                ("Remaining Balance", "How much principal is still owed after some EMIs are paid."),
            ],
            "example": "A ₹5,00,000 loan at 10% annual interest over 5 years works out to "
                       "roughly ₹10,624 per month.",
            "tip": "A shorter tenure means a higher EMI but far less total interest paid "
                   "over the life of the loan.",
        },
        "gst": {
            "title": "GST Calculator",
            "formula": "Exclusive: GST = Price × Rate ÷ 100, Final = Price + GST\n"
                       "Inclusive: Base = Price ÷ (1 + Rate/100), GST = Price − Base",
            "terms": [
                ("Exclusive tax", "GST is added on top of the listed price."),
                ("Inclusive tax", "The listed price already includes GST."),
                ("GST slabs", "Common Indian rates are 5%, 12%, 18%, and 28%."),
            ],
            "example": "A ₹1,000 item at 18% exclusive GST costs ₹1,180 after tax.",
            "tip": "Always check whether a quoted price is GST-inclusive before comparing "
                   "two vendors.",
        },
        "percentage": {
            "title": "Percentage Calculator",
            "formula": "Value = (Total × Percentage) ÷ 100",
            "terms": [
                ("Total", "The whole amount you're taking a percentage of."),
                ("Percentage", "The share you want to calculate, out of 100."),
            ],
            "example": "20% of ₹2,500 is ₹500.",
            "tip": "Percentages are the basis for discounts, interest, and tax — getting "
                   "comfortable with them makes every other calculator easier.",
        },
    },
    "te": {
        "savings": {
            "title": "పొదుపు కాలిక్యులేటర్",
            "formula": "మిగిలిన పొదుపు = నెలవారీ ఆదాయం − నెలవారీ ఖర్చులు\n"
                       "అంచనా నెలలు = లక్ష్య మొత్తం ÷ మిగిలిన పొదుపు",
            "terms": [
                ("మిగిలిన పొదుపు", "ఖర్చుల తర్వాత ప్రతి నెలా మిగిలే డబ్బు."),
                ("లక్ష్య మొత్తం", "మీ లక్ష్యానికి అవసరమైన మొత్తం డబ్బు."),
                ("లక్ష్య పోలిక", "మీరు పెట్టుకున్న గడువుకు మీ పొదుపు సరిపోతుందో లేదో చూపిస్తుంది."),
            ],
            "example": "మీరు ₹30,000 సంపాదించి ₹22,000 ఖర్చు చేస్తే, నెలకు ₹8,000 పొదుపు చేస్తారు. "
                       "₹96,000 లక్ష్యానికి సుమారు 12 నెలలు పడతాయి.",
            "tip": "చిన్న, క్రమమైన పొదుపు పెద్ద, అస్థిరమైన పొదుపు కంటే మేలు. జీతం వచ్చిన వెంటనే "
                   "నిర్ణీత మొత్తాన్ని పొదుపు ఖాతాకు మార్చండి.",
        },
        "emi": {
            "title": "EMI కాలిక్యులేటర్",
            "formula": "EMI = P × [r × (1+r)^n] ÷ [(1+r)^n − 1]\n"
                       "r = (వార్షిక వడ్డీ ÷ 12) ÷ 100, n = మొత్తం నెలలు",
            "terms": [
                ("అసలు మొత్తం (P)", "మీరు తీసుకున్న రుణం."),
                ("వడ్డీ రేటు (r)", "నెలవారీ వసూలు చేసే వడ్డీ."),
                ("కాలవ్యవధి (n)", "రుణం తీర్చడానికి మొత్తం నెలలు."),
                ("మిగిలిన బ్యాలెన్స్", "కొన్ని EMIలు చెల్లించిన తర్వాత ఇంకా బాకీ ఉన్న మొత్తం."),
            ],
            "example": "₹5,00,000 రుణం 10% వార్షిక వడ్డీతో 5 సంవత్సరాలకు తీసుకుంటే, నెలకు "
                       "సుమారు ₹10,624 చెల్లించాలి.",
            "tip": "తక్కువ కాలవ్యవధి అంటే ఎక్కువ EMI, కానీ మొత్తం వడ్డీ చాలా తక్కువగా ఉంటుంది.",
        },
        "gst": {
            "title": "GST కాలిక్యులేటర్",
            "formula": "ఎక్స్‌క్లూజివ్: GST = ధర × రేటు ÷ 100, తుది ధర = ధర + GST\n"
                       "ఇన్‌క్లూజివ్: మూల ధర = ధర ÷ (1 + రేటు/100), GST = ధర − మూల ధర",
            "terms": [
                ("ఎక్స్‌క్లూజివ్ పన్ను", "జాబితా ధరకు అదనంగా GST కలుపుతారు."),
                ("ఇన్‌క్లూజివ్ పన్ను", "జాబితా ధరలో GST ఇప్పటికే కలిసి ఉంటుంది."),
                ("GST స్లాబ్‌లు", "సాధారణ భారత రేట్లు 5%, 12%, 18%, 28%."),
            ],
            "example": "₹1,000 వస్తువుపై 18% ఎక్స్‌క్లూజివ్ GST తో తుది ధర ₹1,180.",
            "tip": "రెండు అమ్మకందారులను పోల్చే ముందు ధరలో GST కలిపారో లేదో ఎప్పుడూ చూడండి.",
        },
        "percentage": {
            "title": "శాతం కాలిక్యులేటర్",
            "formula": "విలువ = (మొత్తం × శాతం) ÷ 100",
            "terms": [
                ("మొత్తం", "మీరు శాతం లెక్కించే మొత్తం విలువ."),
                ("శాతం", "100లో మీరు లెక్కించాలనుకునే భాగం."),
            ],
            "example": "₹2,500లో 20% అంటే ₹500.",
            "tip": "డిస్కౌంట్లు, వడ్డీ, పన్నులకు శాతాలే ఆధారం — వీటిని అర్థం చేసుకుంటే మిగతావన్నీ సులభం.",
        },
    },
}


def get_learn_content(lang="en"):
    """Return the full learn content dict for a language, falling back to English."""
    return LEARN_CONTENT.get(lang, LEARN_CONTENT["en"])
