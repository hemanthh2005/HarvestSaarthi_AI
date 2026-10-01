"""
HarvestSaarthi AI - Explainable Confidence Calculator
Computes a transparent, deterministic confidence score (0-100%) based on input completeness,
data freshness, tool evidence completeness, and source quality.
"""

from typing import Dict, Any, Tuple, List
from backend.models.schemas import FarmerSituation


def calculate_confidence_score(
    situation: FarmerSituation,
    market_data_found: bool,
    transport_data_found: bool,
    weather_data_found: bool,
    storage_data_found: bool,
    is_live_data: bool = False
) -> Tuple[float, List[str]]:
    """
    Calculate deterministic confidence score and return score + list of reasons.
    """
    score = 0.0
    reasons = []

    # 1. Mandatory Input Completeness (Max 35 points)
    if situation.crop:
        score += 10.0
        reasons.append("Crop specified")
    if situation.quantity_kg > 0:
        score += 10.0
        reasons.append("Valid quantity provided")
    if situation.farmer_location:
        score += 10.0
        reasons.append("Location verified")
    if situation.crop_grade:
        score += 5.0
        reasons.append(f"Quality grade ({situation.crop_grade}) included")

    # 2. Tool Evidence Completeness (Max 45 points)
    if market_data_found:
        score += 15.0
        reasons.append("Market price data verified")
    else:
        reasons.append("Missing exact market price data")

    if transport_data_found:
        score += 10.0
        reasons.append("Logistics & transport cost estimated")
    else:
        reasons.append("Missing transport route details")

    if weather_data_found:
        score += 10.0
        reasons.append("Weather risk data incorporated")

    if storage_data_found:
        score += 10.0
        reasons.append("Storage facility data verified")

    # 3. Data Source Quality & Freshness (Max 20 points)
    if is_live_data:
        score += 20.0
        reasons.append("Live market API feed active")
    else:
        score += 15.0  # Validated demo dataset
        reasons.append("Validated prototype benchmark dataset used")

    # Cap between 10% and 98%
    final_score = round(min(max(score, 10.0), 98.0), 1)
    return final_score, reasons
