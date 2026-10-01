"""
HarvestSaarthi AI - Data Repository & Adapter
Loads local benchmark JSON dataset and provides fallback query methods.
"""

import json
import os
from typing import Dict, Any, List, Optional
from backend.models.schemas import (
    MarketPriceData,
    RouteDistanceData,
    WeatherRiskData,
    StorageInfo,
    TransportInfo,
)

DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), "dataset.json")


class DataRepository:
    """Repository for querying deterministic local agricultural dataset."""

    def __init__(self, data_path: str = DATA_FILE_PATH):
        self.data_path = data_path
        self._load_data()

    def _load_data(self):
        with open(self.data_path, "r", encoding="utf-8") as f:
            self.dataset = json.load(f)

    def get_crops(self) -> List[str]:
        return self.dataset.get("crops", [])

    def get_all_markets(self) -> List[Dict[str, Any]]:
        return self.dataset.get("markets", [])

    def get_market_prices_for_crop(self, crop: str, farmer_location: str) -> List[MarketPriceData]:
        results: List[MarketPriceData] = []
        loc_key = f"distance_from_{farmer_location.lower()}_km"

        for m in self.dataset.get("markets", []):
            prices = m.get("prices", {})
            if crop in prices:
                price = prices[crop]
                dist = m.get(loc_key, m.get("distance_from_hassan_km", 50.0))
                results.append(
                    MarketPriceData(
                        market_name=m["market_name"],
                        crop=crop,
                        price_per_kg=price,
                        distance_km=float(dist),
                        market_capacity_kg=float(m.get("market_capacity_kg", 50000)),
                        source="HarvestSaarthi Prototype Dataset",
                        timestamp="2026-10-01T16:00:00Z",
                        data_mode="DEMO",
                        price_trend=m.get("price_trend", "STABLE"),
                    )
                )
        return results

    def get_route_distance(self, origin: str, destination: str, quantity_kg: float = 1000.0) -> RouteDistanceData:
        # Distance heuristic based on dataset
        dist_km = 50.0
        for m in self.dataset.get("markets", []):
            if m["market_name"].lower() in destination.lower() or destination.lower() in m["market_name"].lower():
                loc_key = f"distance_from_{origin.lower()}_km"
                dist_km = float(m.get(loc_key, m.get("distance_from_hassan_km", 80.0)))
                break

        # Calculate estimated transport cost: rate * dist * tons + base fee
        tons = max(quantity_kg / 1000.0, 0.5)
        rate = 12.0 if tons <= 2.5 else 8.5
        est_cost = (dist_km * rate * tons) + 500.0

        return RouteDistanceData(
            origin=origin,
            destination=destination,
            distance_km=dist_km,
            estimated_transport_cost=round(est_cost, 2),
            transport_mode="Small Truck (TATA Ace)" if tons <= 2.5 else "Medium Truck (Eicher)",
            source="HarvestSaarthi Prototype Dataset",
            data_mode="DEMO",
        )

    def get_weather_risk(self, location: str) -> WeatherRiskData:
        risks = self.dataset.get("weather_risks", {})
        for loc, info in risks.items():
            if loc.lower() in location.lower() or location.lower() in loc.lower():
                return WeatherRiskData(
                    location=location,
                    date_range="Next 48 Hours",
                    rain_risk_percent=info["rain_risk_percent"],
                    temperature_celsius=info["temperature_celsius"],
                    risk_level=info["risk_level"],
                    delay_risk_score=info["delay_risk_score"],
                    source="HarvestSaarthi Prototype Dataset",
                    data_mode="DEMO",
                )

        # Fallback default weather risk
        return WeatherRiskData(
            location=location,
            date_range="Next 48 Hours",
            rain_risk_percent=10.0,
            temperature_celsius=27.0,
            risk_level="LOW",
            delay_risk_score=1.0,
            source="HarvestSaarthi Prototype Dataset",
            data_mode="DEMO",
        )

    def get_storage_info(self, location: str, crop: str) -> StorageInfo:
        facilities = self.dataset.get("storage_facilities", [])
        for f in facilities:
            if f["location"].lower() in location.lower() or location.lower() in f["location"].lower():
                return StorageInfo(
                    location=location,
                    crop=crop,
                    available=f["cold_storage_available"] or f["ambient_warehouse_available"],
                    cost_per_kg_day=f["cold_storage_cost_per_kg_day"] if f["cold_storage_available"] else f["ambient_storage_cost_per_kg_day"],
                    capacity_kg=float(f["capacity_kg"]),
                    storage_type="COLD_STORAGE" if f["cold_storage_available"] else "AMBIENT",
                    source="HarvestSaarthi Prototype Dataset",
                    data_mode="DEMO",
                )

        return StorageInfo(
            location=location,
            crop=crop,
            available=False,
            cost_per_kg_day=0.50,
            capacity_kg=0.0,
            storage_type="UNAVAILABLE",
            source="HarvestSaarthi Prototype Dataset",
            data_mode="DEMO",
        )
