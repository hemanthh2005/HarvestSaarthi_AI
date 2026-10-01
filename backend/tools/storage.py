"""
HarvestSaarthi AI - storage_tool
"""

from backend.models.schemas import StorageInfo
from backend.data.repository import DataRepository

repo = DataRepository()


def storage_tool(location: str, crop: str, duration_days: float = 3.0) -> StorageInfo:
    """Checks cold storage & ambient warehouse availability, rates, and capacity."""
    return repo.get_storage_info(location, crop)
