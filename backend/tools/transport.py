"""
HarvestSaarthi AI - route_distance_tool & transport_tool
"""

from backend.models.schemas import RouteDistanceData, TransportInfo
from backend.data.repository import DataRepository

repo = DataRepository()


def route_distance_tool(origin: str, destination: str, quantity_kg: float = 1000.0) -> RouteDistanceData:
    """Calculates route distance and estimated transport cost."""
    return repo.get_route_distance(origin, destination, quantity_kg)


def transport_tool(origin: str, destination: str, quantity_kg: float) -> TransportInfo:
    """Checks vehicle availability and calculates logistics rates."""
    route = route_distance_tool(origin, destination, quantity_kg)
    return TransportInfo(
        origin=origin,
        destination=destination,
        quantity_kg=quantity_kg,
        available=True,
        estimated_cost=route.estimated_transport_cost,
        capacity_kg=3000.0 if quantity_kg <= 2500 else 10000.0,
        rate_per_km_ton=12.0 if quantity_kg <= 2500 else 8.5,
        source="HarvestSaarthi Logistics Engine",
        data_mode="DEMO",
    )
