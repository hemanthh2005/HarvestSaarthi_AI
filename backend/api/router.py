"""
HarvestSaarthi AI - FastAPI API Routers
Implements endpoints: health, crops, markets, analyze, decision, what-if, demo, action-plan, report.
"""

from fastapi import APIRouter, HTTPException, Response, Query
from typing import Dict, Any, List
import copy
from backend.models.schemas import (
    FarmerSituation,
    DecisionResult,
    WhatIfRequest,
    ActionStep,
    NegotiationMessage,
)
from backend.agents.orchestrator import OrchestratorAgent
from backend.data.repository import DataRepository
from backend.reports.pdf_generator import generate_pdf_report
from backend.utils.security import check_prompt_injection, sanitize_string

router = APIRouter(prefix="/api")
repo = DataRepository()
orchestrator = OrchestratorAgent(use_llm_mode=False)

# In-memory store for generated report runs
RUN_CACHE: Dict[str, DecisionResult] = {}


@router.get("/health")
def get_health() -> Dict[str, Any]:
    """Health check endpoint."""
    return {
        "success": True,
        "data": {
            "status": "healthy",
            "service": "HarvestSaarthi AI Agent",
            "version": "1.0.0",
            "execution_mode": "FALLBACK_MODE",
            "data_mode": "DEMO",
        },
        "error": None,
    }


@router.get("/crops")
def get_supported_crops() -> Dict[str, Any]:
    """Returns list of supported crops."""
    return {
        "success": True,
        "data": repo.get_crops(),
        "error": None,
    }


@router.get("/markets")
def get_supported_markets() -> Dict[str, Any]:
    """Returns list of supported mandis."""
    return {
        "success": True,
        "data": repo.get_all_markets(),
        "error": None,
    }


@router.post("/analyze")
def analyze_situation(situation: FarmerSituation) -> Dict[str, Any]:
    """Analyzes farmer situation and checks missing inputs."""
    if situation.raw_input_text and check_prompt_injection(situation.raw_input_text):
        raise HTTPException(status_code=400, detail="Potential security policy violation in input text.")

    situation.crop = sanitize_string(situation.crop, 50)
    situation.farmer_location = sanitize_string(situation.farmer_location, 50)

    result = orchestrator.process_situation(situation)
    RUN_CACHE[result.run_id] = result

    return {
        "success": True,
        "data": {
            "run_id": result.run_id,
            "crop": situation.crop,
            "quantity_kg": situation.quantity_kg,
            "farmer_location": situation.farmer_location,
            "missing_information": result.missing_information,
            "recommendation_title": result.recommendation_title,
            "expected_net_realization": result.expected_net_realization,
            "confidence_score": result.confidence_score,
            "risk_level": result.risk_level,
        },
        "error": None,
    }


@router.post("/decision", response_model=Dict[str, Any])
def compute_decision(situation: FarmerSituation) -> Dict[str, Any]:
    """Main decision endpoint executing the 12-stage agent workflow."""
    if situation.raw_input_text and check_prompt_injection(situation.raw_input_text):
        raise HTTPException(status_code=400, detail="Potential security policy violation in input text.")

    result = orchestrator.process_situation(situation)
    RUN_CACHE[result.run_id] = result

    return {
        "success": True,
        "data": result.model_dump(),
        "error": None,
    }


@router.post("/what-if")
def compute_what_if(req: WhatIfRequest) -> Dict[str, Any]:
    """Re-runs decision engine with dynamic parameter overrides."""
    situation = copy.deepcopy(req.situation)

    # Apply overrides
    if req.override_quantity_kg is not None and req.override_quantity_kg > 0:
        situation.quantity_kg = req.override_quantity_kg
    if req.override_cold_storage is not None:
        situation.has_cold_storage = req.override_cold_storage

    result = orchestrator.process_situation(situation)

    # If price change override specified, adjust options expected net realization
    if req.override_market_price_change_percent is not None:
        factor = 1.0 + (req.override_market_price_change_percent / 100.0)
        for opt in result.options:
            opt.gross_revenue = round(opt.gross_revenue * factor, 2)
            opt.expected_net_realization = round(opt.gross_revenue - opt.transport_cost - opt.storage_cost - opt.estimated_spoilage_loss, 2)

        # Re-sort best option
        best = max([o for o in result.options if o.feasible] or result.options, key=lambda o: o.expected_net_realization)
        result.recommendation_title = best.title
        result.recommended_option_id = best.option_id
        result.expected_net_realization = best.expected_net_realization

    RUN_CACHE[result.run_id] = result
    return {
        "success": True,
        "data": result.model_dump(),
        "error": None,
    }


@router.get("/demo/{demo_id}")
def get_demo_scenario(demo_id: str) -> Dict[str, Any]:
    """
    Preconfigured judge demo scenarios:
    1. tomato -> Hassan, 2000 kg, no cold storage -> Sell quickly nearby
    2. onion -> Kolar, 10000 kg, storage available -> Storage alternative feasible
    3. banana -> Mysuru, 3000 kg, urgent harvest -> High perishability dispatch plan
    """
    clean_id = demo_id.lower().strip()

    if "tomato" in clean_id or clean_id == "1":
        sit = FarmerSituation(
            crop="Tomato",
            quantity_kg=2000.0,
            farmer_location="Hassan",
            harvest_date="Tomorrow Morning",
            crop_grade="Grade A",
            has_cold_storage=False,
            has_transport=True,
            preferred_selling_radius_km=150.0,
            urgency="HIGH",
            language="en",
        )
    elif "onion" in clean_id or clean_id == "2":
        sit = FarmerSituation(
            crop="Onion",
            quantity_kg=10000.0,
            farmer_location="Kolar",
            harvest_date="Today",
            crop_grade="Grade A",
            has_cold_storage=True,
            has_transport=True,
            preferred_selling_radius_km=250.0,
            urgency="NORMAL",
            language="en",
        )
    elif "banana" in clean_id or clean_id == "3":
        sit = FarmerSituation(
            crop="Banana",
            quantity_kg=3000.0,
            farmer_location="Mysuru",
            harvest_date="Today",
            crop_grade="Grade A",
            has_cold_storage=False,
            has_transport=True,
            preferred_selling_radius_km=180.0,
            urgency="URGENT",
            language="en",
        )
    else:
        raise HTTPException(status_code=404, detail="Demo scenario not found. Choose: tomato, onion, banana.")

    result = orchestrator.process_situation(sit)
    RUN_CACHE[result.run_id] = result

    return {
        "success": True,
        "data": {
            "demo_id": clean_id,
            "situation": sit.model_dump(),
            "result": result.model_dump(),
        },
        "error": None,
    }


@router.post("/action-plan")
def get_action_plan(situation: FarmerSituation) -> Dict[str, Any]:
    """Returns executable action steps and negotiation templates."""
    result = orchestrator.process_situation(situation)
    return {
        "success": True,
        "data": {
            "recommendation": result.recommendation_title,
            "action_plan": [a.model_dump() for a in result.action_plan],
            "negotiation_messages": [n.model_dump() for n in result.negotiation_messages],
        },
        "error": None,
    }


@router.get("/report/{run_id}")
def download_pdf_report(run_id: str):
    """Generates and downloads PDF decision report for run_id."""
    result = RUN_CACHE.get(run_id)
    if not result:
        # Generate default demo result if run_id not in cache
        demo_sit = FarmerSituation(crop="Tomato", quantity_kg=2000.0, farmer_location="Hassan")
        result = orchestrator.process_situation(demo_sit)

    pdf_bytes = generate_pdf_report(result)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=HarvestSaarthi_Decision_Report_{run_id}.pdf"},
    )
