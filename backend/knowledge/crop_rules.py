"""
HarvestSaarthi AI - Crop Knowledge Base
Contains perishability curves, shelf-life factors, and storage rules.
"""

from typing import Dict, Any

CROP_PROPERTIES: Dict[str, Dict[str, Any]] = {
    "Tomato": {
        "shelf_life_ambient_days": 3.0,
        "shelf_life_cold_days": 12.0,
        "base_spoilage_rate_per_day": 0.08,  # 8% per day ambient
        "cold_storage_spoilage_rate_per_day": 0.015,  # 1.5% per day cold
        "perishability_tier": "HIGH",
        "temp_sensitivity": "HIGH",
        "humidity_sensitivity": "HIGH",
        "recommended_storage": "COLD_STORAGE",
        "default_price_per_kg": 28.0,
    },
    "Onion": {
        "shelf_life_ambient_days": 30.0,
        "shelf_life_cold_days": 90.0,
        "base_spoilage_rate_per_day": 0.005,  # 0.5% per day ambient
        "cold_storage_spoilage_rate_per_day": 0.001,
        "perishability_tier": "LOW",
        "temp_sensitivity": "LOW",
        "humidity_sensitivity": "MEDIUM",
        "recommended_storage": "VENTILATED",
        "default_price_per_kg": 24.0,
    },
    "Banana": {
        "shelf_life_ambient_days": 4.0,
        "shelf_life_cold_days": 10.0,
        "base_spoilage_rate_per_day": 0.07,  # 7% per day ambient
        "cold_storage_spoilage_rate_per_day": 0.02,
        "perishability_tier": "HIGH",
        "temp_sensitivity": "HIGH",
        "humidity_sensitivity": "HIGH",
        "recommended_storage": "COLD_STORAGE",
        "default_price_per_kg": 22.0,
    },
    "Potato": {
        "shelf_life_ambient_days": 45.0,
        "shelf_life_cold_days": 120.0,
        "base_spoilage_rate_per_day": 0.003,
        "cold_storage_spoilage_rate_per_day": 0.0005,
        "perishability_tier": "LOW",
        "temp_sensitivity": "LOW",
        "humidity_sensitivity": "MEDIUM",
        "recommended_storage": "VENTILATED",
        "default_price_per_kg": 18.0,
    },
    "Green Chili": {
        "shelf_life_ambient_days": 5.0,
        "shelf_life_cold_days": 15.0,
        "base_spoilage_rate_per_day": 0.05,
        "cold_storage_spoilage_rate_per_day": 0.01,
        "perishability_tier": "MEDIUM",
        "temp_sensitivity": "HIGH",
        "humidity_sensitivity": "HIGH",
        "recommended_storage": "COLD_STORAGE",
        "default_price_per_kg": 45.0,
    },
    "Paddy": {
        "shelf_life_ambient_days": 180.0,
        "shelf_life_cold_days": 365.0,
        "base_spoilage_rate_per_day": 0.0005,
        "cold_storage_spoilage_rate_per_day": 0.0001,
        "perishability_tier": "VERY_LOW",
        "temp_sensitivity": "LOW",
        "humidity_sensitivity": "HIGH",
        "recommended_storage": "DRY_GODOWN",
        "default_price_per_kg": 23.0,
    },
    "Maize": {
        "shelf_life_ambient_days": 120.0,
        "shelf_life_cold_days": 300.0,
        "base_spoilage_rate_per_day": 0.0008,
        "cold_storage_spoilage_rate_per_day": 0.0002,
        "perishability_tier": "VERY_LOW",
        "temp_sensitivity": "LOW",
        "humidity_sensitivity": "HIGH",
        "recommended_storage": "DRY_GODOWN",
        "default_price_per_kg": 21.0,
    },
    "Mango": {
        "shelf_life_ambient_days": 4.0,
        "shelf_life_cold_days": 14.0,
        "base_spoilage_rate_per_day": 0.09,
        "cold_storage_spoilage_rate_per_day": 0.018,
        "perishability_tier": "VERY_HIGH",
        "temp_sensitivity": "VERY_HIGH",
        "humidity_sensitivity": "HIGH",
        "recommended_storage": "COLD_STORAGE",
        "default_price_per_kg": 60.0,
    },
}


def get_crop_info(crop_name: str) -> Dict[str, Any]:
    """Retrieve crop properties or fallback to generic defaults."""
    for key, val in CROP_PROPERTIES.items():
        if key.lower() == crop_name.lower():
            return val
    # Fallback generic crop properties
    return {
        "shelf_life_ambient_days": 7.0,
        "shelf_life_cold_days": 21.0,
        "base_spoilage_rate_per_day": 0.03,
        "cold_storage_spoilage_rate_per_day": 0.005,
        "perishability_tier": "MEDIUM",
        "temp_sensitivity": "MEDIUM",
        "humidity_sensitivity": "MEDIUM",
        "recommended_storage": "AMBIENT",
        "default_price_per_kg": 25.0,
    }
