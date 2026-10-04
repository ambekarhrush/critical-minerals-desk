import pytest
from fastapi.testclient import TestClient
from app.main import app, Scenario, calculate

client = TestClient(app)


def test_units_and_zero_discount():
    r = calculate(Scenario(price=80, cost=45, tonnes=4000, capex=1000, years=20, discount=0))
    assert r["annual_musd"] == 140
    assert r["npv_musd"] == 1800
    assert r["breakeven_usd_kg"] == 57.5


def test_delay_reduces_positive_cashflows():
    assert calculate(Scenario(delay=4))["npv_musd"] < calculate(Scenario(delay=0))["npv_musd"]


def test_break_even():
    base = Scenario()
    price = calculate(base)["breakeven_usd_kg"]
    assert abs(calculate(base.model_copy(update={"price": price}))["npv_musd"]) < .1


@pytest.mark.parametrize("data", [{"tonnes": 0}, {"delay": -1}, {"years": 2.5}, {"price": "NaN"}])
def test_invalid_inputs(data):
    assert client.post("/api/scenario", json=data).status_code == 422


def test_sources_and_unknowns():
    records = client.get("/api/projects").json()["projects"]
    assert all(r["source"].startswith("https://") for r in records)
    assert records[2]["volume"] is None
    assert records[0]["basis"] != records[1]["basis"]
