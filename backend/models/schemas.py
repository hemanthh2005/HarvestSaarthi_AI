"""
HarvestSaarthi AI - Pydantic Schemas & Data Models
Defines all input/output structures for API, agents, decision engine, and tools.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator


class FarmerSituation(BaseModel):
    crop: str = Field(..., description="Crop name e.g., Tomato, Onion, Banana")
    quantity_kg: float = Field(..., gt=0, description="Total harvest quantity in kg")
    farmer_location: str = Field(..., description="Farmer's location/district e.g., Hassan, Kolar")
    harvest_date: str = Field("Today", description="Expected harvest timing")
    crop_grade: str = Field("Grade A", description="Quality grade: Grade A, Grade B, Grade C")
    has_cold_storage: bool = Field(False, description="Whether cold storage is available locally")
    has_transport: bool = Field(True, description="Whether transport can be arranged")
    preferred_selling_radius_km: float = Field(150.0, gt=0, description="Max selling radius in km")
    urgency: str = Field("NORMAL", description="Urgency level: LOW, NORMAL, HIGH, URGENT")
    min_expected_price: Optional[float] = Field(None, ge=0, description="Minimum expected price per kg")
    language: str = Field("en", description="Preferred response language: en, kn, hi")
    raw_input_text: Optional[str] = Field(None, description="Original voice or freeform text input")

    @field_validator("crop")
    @classmethod
    def sanitize_crop(cls, v: str) -> str:
        cleaned = v.strip().title()
        if not cleaned:
            raise ValueError("Crop name cannot be empty")
        return cleaned

    @field_validator("farmer_location")
    @classmethod
    def sanitize_location(cls, v: str) -> str:
        cleaned = v.strip().title()
        if not cleaned:
            raise ValueError("Farmer location cannot be empty")
        return cleaned


class MarketPriceData(BaseModel):
    market_name: str
    crop: str
    price_per_kg: float
    distance_km: float
    market_capacity_kg: float
    source: str = "HarvestSaarthi Prototype Dataset"
    timestamp: str
    data_mode: str = "DEMO"
    price_trend: str = "STABLE"  # RISING, FALLING, STABLE


class RouteDistanceData(BaseModel):
    origin: str
    destination: str
    distance_km: float
    estimated_transport_cost: float
    transport_mode: str = "Small Truck (TATA Ace)"
    source: str = "HarvestSaarthi Prototype Dataset"
    data_mode: str = "DEMO"


class WeatherRiskData(BaseModel):
    location: str
    date_range: str
    rain_risk_percent: float
    temperature_celsius: float
    risk_level: str  # LOW, MEDIUM, HIGH
    delay_risk_score: float  # 0 to 10 scale
    source: str = "HarvestSaarthi Prototype Dataset"
    data_mode: str = "DEMO"


class PerishabilityData(BaseModel):
    crop: str
    storage_type: str  # AMBIENT, COLD_STORAGE, VENTILATED
    duration_hours: float
    spoilage_risk_percent: float
    estimated_loss_percent: float
    shelf_life_days: float
    source: str = "HarvestSaarthi Crop Knowledge Engine"
    data_mode: str = "DEMO"


class StorageInfo(BaseModel):
    location: str
    crop: str
    available: bool
    cost_per_kg_day: float
    capacity_kg: float
    storage_type: str
    distance_km: float = 5.0
    source: str = "HarvestSaarthi Prototype Dataset"
    data_mode: str = "DEMO"


class TransportInfo(BaseModel):
    origin: str
    destination: str
    quantity_kg: float
    available: bool
    estimated_cost: float
    capacity_kg: float
    rate_per_km_ton: float
    source: str = "HarvestSaarthi Logistics Tool"
    data_mode: str = "DEMO"


class EvaluatedOption(BaseModel):
    option_id: str  # OPTION_A, OPTION_B, etc.
    option_type: str  # SELL_NEAREST_TODAY, TRANSPORT_DISTANT_MARKET, STORE_AND_SELL_LATER, SPLIT_MARKET
    title: str
    description: str
    target_market: str
    destination_distance_km: float
    selling_timeframe: str
    gross_revenue: float
    transport_cost: float
    storage_cost: float
    estimated_spoilage_loss: float
    other_costs: float = 0.0
    expected_net_realization: float
    risk_level: str  # LOW, MEDIUM, HIGH
    confidence_score: float
    feasible: bool
    infeasibility_reasons: List[str] = []
    evidence: List[Dict[str, Any]] = []


class ActionStep(BaseModel):
    priority: int
    action: str
    reason: str
    dependency: str
    status: str = "PENDING"


class NegotiationMessage(BaseModel):
    template_type: str  # BUYER_INQUIRY, TRANSPORT_REQUEST, MARKET_CONFIRMATION
    language: str  # en, kn, hi
    title: str
    message_text: str


class DecisionResult(BaseModel):
    run_id: str
    recommendation_title: str
    recommended_option_id: str
    expected_net_realization: float
    confidence_score: float
    risk_level: str
    primary_reasons: List[str]
    options: List[EvaluatedOption]
    action_plan: List[ActionStep]
    negotiation_messages: List[NegotiationMessage]
    execution_trace: List[Dict[str, Any]]
    missing_information: List[str] = []
    execution_mode: str = "FALLBACK_MODE"  # AI_MODE or FALLBACK_MODE
    data_mode: str = "DEMO"
    disclaimer: str = (
        "Disclaimer: AI-generated decision support report. Estimates are based on the HarvestSaarthi "
        "prototype/demo benchmark dataset and are not guarantees of market price, profit, or income. "
        "Verify current market prices, buyer terms, transport availability, and other conditions before taking action."
    )
    timestamp: str


class WhatIfRequest(BaseModel):
    situation: FarmerSituation
    override_quantity_kg: Optional[float] = None
    override_market_price_change_percent: Optional[float] = None
    override_transport_cost_multiplier: Optional[float] = None
    override_cold_storage: Optional[bool] = None
    override_delay_days: Optional[float] = None
