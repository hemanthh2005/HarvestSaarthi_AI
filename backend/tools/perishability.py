"""
HarvestSaarthi AI - perishability_tool
"""

from backend.models.schemas import PerishabilityData
from backend.knowledge.crop_rules import get_crop_info


def perishability_tool(crop: str, storage_type: str = "AMBIENT", duration_hours: float = 24.0) -> PerishabilityData:
    """Calculates spoilage risk percentage and shelf life for a given crop and storage setup."""
    info = get_crop_info(crop)
    days = max(duration_hours / 24.0, 0.5)

    if storage_type == "COLD_STORAGE":
        rate = info.get("cold_storage_spoilage_rate_per_day", 0.015)
        shelf_life = info.get("shelf_life_cold_days", 14.0)
    else:
        rate = info.get("base_spoilage_rate_per_day", 0.08)
        shelf_life = info.get("shelf_life_ambient_days", 3.0)

    spoilage_pct = min(rate * days * 100.0, 95.0)

    return PerishabilityData(
        crop=crop,
        storage_type=storage_type,
        duration_hours=duration_hours,
        spoilage_risk_percent=round(spoilage_pct, 2),
        estimated_loss_percent=round(spoilage_pct, 2),
        shelf_life_days=shelf_life,
        source="HarvestSaarthi Crop Decay Model",
        data_mode="DEMO",
    )
