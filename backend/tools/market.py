"""
HarvestSaarthi AI - market_price_tool
"""

from typing import List
from backend.models.schemas import MarketPriceData
from backend.data.repository import DataRepository

repo = DataRepository()


def market_price_tool(crop: str, location: str, date: str = "Today") -> List[MarketPriceData]:
    """
    Fetches market prices for a given crop across nearby mandis.
    Returns structured MarketPriceData objects.
    """
    prices = repo.get_market_prices_for_crop(crop, location)
    if not prices:
        # Generic fallback price if crop not in dataset
        prices.append(
            MarketPriceData(
                market_name=f"{location} District Mandi",
                crop=crop,
                price_per_kg=25.0,
                distance_km=10.0,
                market_capacity_kg=30000.0,
                source="HarvestSaarthi Prototype Dataset",
                timestamp="2026-10-01T16:00:00Z",
                data_mode="DEMO",
            )
        )
    return prices
