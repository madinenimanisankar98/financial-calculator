import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.calculations import (
    calculate_savings,
    calculate_emi,
    calculate_gst,
    calculate_percentage,
)


def test_savings_basic():
    r = calculate_savings(30000, 22000, "Laptop", 96000)
    assert r["available_savings"] == 8000
    assert r["estimated_months"] == 12.0
    assert r["years"] == 1
    assert r["remaining_months"] == 0


def test_savings_with_target_sufficient():
    r = calculate_savings(30000, 22000, "Laptop", 96000, target_value=1, target_unit="years")
    assert r["target_comparison"]["status"] == "Sufficient"


def test_savings_expenses_exceed_income():
    r = calculate_savings(20000, 25000, "Phone", 50000)
    assert "error" in r


def test_emi_standard_loan():
    r = calculate_emi(500000, 10, 5, "years")
    # Known approximate EMI for this input
    assert 10600 <= r["emi"] <= 10650
    assert r["total_months"] == 60
    assert r["total_payable"] > 500000
    assert r["total_interest"] == round(r["total_payable"] - 500000, 2)


def test_emi_zero_interest():
    r = calculate_emi(120000, 0, 12, "months")
    assert r["emi"] == 10000.0
    assert r["total_interest"] == 0.0


def test_emi_remaining_balance_decreases():
    r_full = calculate_emi(500000, 10, 5, "years", emis_paid=0)
    r_partial = calculate_emi(500000, 10, 5, "years", emis_paid=24)
    assert r_full["remaining_balance"] is None  # emis_paid=0 means no partial calc
    assert r_partial["remaining_balance"] < 500000
    assert r_partial["remaining_balance"] > 0


def test_gst_exclusive():
    r = calculate_gst(1000, 18, tax_mode="exclusive")
    assert r["base_price"] == 1000
    assert r["gst_amount"] == 180
    assert r["final_price"] == 1180


def test_gst_inclusive():
    r = calculate_gst(1180, 18, tax_mode="inclusive")
    assert round(r["base_price"], 2) == 1000.0
    assert round(r["gst_amount"], 2) == 180.0


def test_percentage_basic():
    r = calculate_percentage(2500, 20)
    assert r["value"] == 500
    assert r["remainder"] == 2000


def test_percentage_over_100():
    r = calculate_percentage(800, 150)
    assert r["value"] == 1200
    assert r["remainder"] == -400
