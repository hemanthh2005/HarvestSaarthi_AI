"""
HarvestSaarthi AI - Tools Unit Tests
"""

from backend.tools.market import market_price_tool
from backend.tools.transport import route_distance_tool, transport_tool
from backend.tools.weather import weather_risk_tool
from backend.tools.perishability import perishability_tool
from backend.tools.storage import storage_tool


def test_market_price_tool():
    prices = market_price_tool("Tomato", "Hassan")
    assert len(prices) > 0
    assert prices[0].crop == "Tomato"
    assert prices[0].price_per_kg > 0
    assert prices[0].data_mode == "DEMO"


def test_route_distance_tool():
    route = route_distance_tool("Hassan", "Bangalore Yeshwanthpur APMC", 2000.0)
    assert route.distance_km > 0
    assert route.estimated_transport_cost > 0


def test_weather_risk_tool():
    weather = weather_risk_tool("Hassan")
    assert weather.risk_level in ["LOW", "MEDIUM", "HIGH"]


def test_perishability_tool():
    p = perishability_tool("Tomato", "AMBIENT", 24.0)
    assert p.spoilage_risk_percent > 0
    assert p.shelf_life_days > 0


def test_storage_tool():
    s = storage_tool("Kolar", "Onion")
    assert s.location == "Kolar"
