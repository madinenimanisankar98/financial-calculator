"""
Financial math engine for Financial Calculator PRO.
Pure functions only — no Flask imports here, so this module is easy to unit test.
"""


def calculate_savings(monthly_income, monthly_expenses, goal_name, goal_price,
                       target_value=None, target_unit=None):
    """
    Savings Calculator.

    monthly_income, monthly_expenses, goal_price: numbers (₹)
    goal_name: string (required, just passed through for display)
    target_value: optional number, paired with target_unit ("months" | "years")
    """
    available_savings = monthly_income - monthly_expenses

    if available_savings <= 0:
        return {
            "goal_name": goal_name,
            "available_savings": available_savings,
            "error": "Monthly expenses meet or exceed income, so this goal "
                     "cannot be reached through savings alone.",
        }

    estimated_months = goal_price / available_savings
    years = int(estimated_months // 12)
    remaining_months = round(estimated_months - years * 12, 1)
    total_days = round(estimated_months * 30)

    result = {
        "goal_name": goal_name,
        "goal_price": goal_price,
        "available_savings": round(available_savings, 2),
        "estimated_months": round(estimated_months, 2),
        "years": years,
        "remaining_months": remaining_months,
        "total_days": total_days,
        "timeline": _savings_timeline(available_savings, goal_price),
    }

    if target_value and target_unit:
        target_months = target_value * 12 if target_unit == "years" else target_value
        if target_months <= 0:
            result["target_comparison"] = None
        else:
            required_monthly = goal_price / target_months
            if available_savings >= required_monthly:
                status = "Sufficient"
            elif available_savings >= required_monthly * 0.85:
                status = "Close"
            else:
                status = "Insufficient"
            result["target_comparison"] = {
                "target_months": target_months,
                "required_monthly_savings": round(required_monthly, 2),
                "status": status,
            }

    return result


def _savings_timeline(available_savings, goal_price, max_points=24):
    """Month-by-month cumulative savings, capped at max_points for chart readability."""
    if available_savings <= 0:
        return []
    total_months = min(int(goal_price / available_savings) + 1, max_points)
    return [round(min(available_savings * m, goal_price), 2) for m in range(1, total_months + 1)]


def calculate_emi(principal, annual_rate, tenure_value, tenure_unit, emis_paid=0):
    """
    EMI Calculator.

    principal: loan amount (₹)
    annual_rate: annual interest rate (%)
    tenure_value + tenure_unit ("years" | "months")
    emis_paid: number of EMIs already paid, for the remaining-balance figure
    """
    n = tenure_value * 12 if tenure_unit == "years" else tenure_value
    n = int(n)
    r = (annual_rate / 12) / 100

    if r == 0:
        emi = principal / n
    else:
        factor = (1 + r) ** n
        emi = principal * r * factor / (factor - 1)

    total_payable = emi * n
    total_interest = total_payable - principal

    remaining_balance = None
    if 0 < emis_paid < n:
        k = emis_paid
        if r == 0:
            remaining_balance = principal - emi * k
        else:
            factor_n = (1 + r) ** n
            factor_k = (1 + r) ** k
            remaining_balance = principal * (factor_n - factor_k) / (factor_n - 1)

    return {
        "emi": round(emi, 2),
        "total_months": n,
        "total_payable": round(total_payable, 2),
        "total_interest": round(total_interest, 2),
        "remaining_balance": round(remaining_balance, 2) if remaining_balance is not None else None,
        "amortization": _amortization_schedule(principal, r, n),
    }


def _amortization_schedule(principal, r, n, max_points=24):
    """Remaining balance after each period, downsampled to max_points for the chart."""
    if n <= 0:
        return []
    step = max(1, n // max_points)
    schedule = []
    if r == 0:
        emi = principal / n
        for k in range(0, n + 1, step):
            schedule.append(round(max(principal - emi * k, 0), 2))
    else:
        factor_n = (1 + r) ** n
        for k in range(0, n + 1, step):
            factor_k = (1 + r) ** k
            balance = principal * (factor_n - factor_k) / (factor_n - 1)
            schedule.append(round(max(balance, 0), 2))
    return schedule


def calculate_gst(price, gst_percent, tax_mode="exclusive", product_name=None):
    """
    GST Calculator.

    tax_mode: "exclusive" -> price is before tax, GST added on top
              "inclusive" -> price already includes GST, GST is extracted
    """
    if tax_mode == "inclusive":
        base_price = price / (1 + gst_percent / 100)
        gst_amount = price - base_price
        final_price = price
    else:
        base_price = price
        gst_amount = price * gst_percent / 100
        final_price = base_price + gst_amount

    return {
        "product_name": product_name,
        "tax_mode": tax_mode,
        "gst_percent": gst_percent,
        "base_price": round(base_price, 2),
        "gst_amount": round(gst_amount, 2),
        "final_price": round(final_price, 2),
    }


def calculate_percentage(total, percentage):
    """Percentage Calculator: value = (total * percentage) / 100."""
    value = total * percentage / 100
    return {
        "total": total,
        "percentage": percentage,
        "value": round(value, 2),
        "remainder": round(total - value, 2),
    }
