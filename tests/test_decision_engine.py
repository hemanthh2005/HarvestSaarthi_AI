"""
HarvestSaarthi AI - Decision Engine Unit Tests
Tests math logic for gross revenue, transport cost, spoilage loss, expected net realization, and confidence.
"""

import pytest
from backend.models.schemas import (
    FarmerSituation,
    MarketPriceData,
    RouteDistanceData,
    WeatherRiskData,
    PerishabilityData,
    StorageInfo,
    TransportInfo,
)
from backend.decision.engine import DecisionEngine
from backend.decision.confidence import calculate_confidence_score


def test_decision_engine_evaluation():
    situation = FarmerSituation(
        crop="Tomato",
        quantity_kg=2000.0,
        farmer_location="Hassan",
        has_cold_storage=False,
        has_transport=True,
    )

    markets = [
        MarketPriceData(
            market_name="Hassan APMC Mandi",
            crop="Tomato",
            price_per_kg=26.50,
            distance_km=8.0,
            market_capacity_kg=50000,
            source="Test Dataset",
            timestamp="2026-10-01",
        ),
        MarketPriceData(
            market_name="Bangalore Yeshwanthpur APMC",
            crop="Tomato",
            price_per_kg=34.00,
            distance_km=180.0,
            market_capacity_kg=250000,
            source="Test Dataset",
            timestamp="2026-10-01",
        ),
    ]

    routes = [
        RouteDistanceData(origin="Hassan", destination="Hassan APMC Mandi", distance_km=8.0, estimated_transport_cost=692.0),
        RouteDistanceData(origin="Hassan", destination="Bangalore Yeshwanthpur APMC", distance_km=180.0, estimated_transport_cost=4820.0),
    ]

    weather = WeatherRiskData(location="Hassan", date_range="48H", rain_risk_percent=10.0, temperature_celsius=26.0, risk_level="LOW", delay_risk_score=1.0)
    perishability = PerishabilityData(crop="Tomato", storage_type="AMBIENT", duration_hours=24.0, spoilage_risk_percent=8.0, estimated_loss_percent=8.0, shelf_life_days=3.0)
    storage = StorageInfo(location="Hassan", crop="Tomato", available=False, cost_per_kg_day=0.6, capacity_kg=20000, storage_type="AMBIENT")
    transport = TransportInfo(origin="Hassan", destination="Hassan APMC Mandi", quantity_kg=2000.0, available=True, estimated_cost=692.0, capacity_kg=3000, rate_per_km_ton=12.0)

    options = DecisionEngine.evaluate_all_options(
        situation=situation,
        markets=markets,
        routes=routes,
        weather=weather,
        perishability=perishability,
        storage=storage,
        transport=transport,
    )

    assert len(options) >= 2
    option_a = [o for o in options if o.option_id == "OPTION_A"][0]

    # Verify deterministic math
    expected_gross = 2000.0 * 26.50  # 53,000
    assert option_a.gross_revenue == expected_gross
    assert option_a.transport_cost == 692.0
    assert option_a.expected_net_realization < expected_gross

    best_option = DecisionEngine.select_best_option(options)
    assert best_option is not None


def test_confidence_score_calculation():
    situation = FarmerSituation(
        crop="Tomato",
        quantity_kg=2000.0,
        farmer_location="Hassan",
        crop_grade="Grade A",
    )

    score, reasons = calculate_confidence_score(
        situation=situation,
        market_data_found=True,
        transport_data_found=True,
        weather_data_found=True,
        storage_data_found=True,
        is_live_data=False,
    )

    assert score >= 70.0
    assert len(reasons) > 0
