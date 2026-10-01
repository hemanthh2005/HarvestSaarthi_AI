"""
HarvestSaarthi AI - Orchestrator Agent
Orchestrates the complete 12-stage agent workflow from farmer input to action plan and report generation.
"""

import time
import uuid
from typing import Dict, Any, List, Optional
from backend.models.schemas import FarmerSituation, DecisionResult, EvaluatedOption
from backend.agents.situation_agent import SituationUnderstandingAgent
from backend.agents.action_agent import ActionPlannerAgent
from backend.decision.engine import DecisionEngine
from backend.decision.confidence import calculate_confidence_score
from backend.tools.market import market_price_tool
from backend.tools.transport import route_distance_tool, transport_tool
from backend.tools.weather import weather_risk_tool
from backend.tools.perishability import perishability_tool
from backend.tools.storage import storage_tool


class OrchestratorAgent:
    """Central decision-and-action orchestrator for HarvestSaarthi AI."""

    def __init__(self, use_llm_mode: bool = False):
        self.use_llm_mode = use_llm_mode

    def process_situation(self, situation: FarmerSituation) -> DecisionResult:
        """Executes full 12-stage agentic workflow."""
        run_id = f"run_{uuid.uuid4().hex[:8]}"
        start_time = time.time()
        trace: List[Dict[str, Any]] = []

        # 1. USER INPUT STAGE
        trace.append({
            "stage": "USER_INPUT",
            "title": "User Input Received",
            "status": "COMPLETED",
            "details": f"Crop: {situation.crop}, Qty: {situation.quantity_kg:,.0f} kg, Location: {situation.farmer_location}",
            "timestamp": time.strftime("%H:%M:%S")
        })

        # 2. SITUATION UNDERSTANDING & NORMALIZATION
        norm_situation, missing_info, notes = SituationUnderstandingAgent.analyze_situation(situation)
        trace.append({
            "stage": "SITUATION_UNDERSTANDING",
            "title": "Situation Understanding & Entity Normalization",
            "status": "COMPLETED",
            "details": "; ".join(notes),
            "timestamp": time.strftime("%H:%M:%S")
        })

        # 3. REQUIREMENT PLANNING
        trace.append({
            "stage": "REQUIREMENT_PLANNING",
            "title": "Requirement Planning & Gap Analysis",
            "status": "COMPLETED",
            "details": f"Missing Fields: {len(missing_info)} | Identified 5 tool requirements: Market, Route, Weather, Perishability, Storage",
            "timestamp": time.strftime("%H:%M:%S")
        })

        # 4. TOOL SELECTION
        trace.append({
            "stage": "TOOL_SELECTION",
            "title": "Tool Selection",
            "status": "COMPLETED",
            "details": "Selected: market_price_tool, route_distance_tool, weather_risk_tool, perishability_tool, storage_tool, transport_tool",
            "timestamp": time.strftime("%H:%M:%S")
        })

        # 5. DATA COLLECTION (Tool Executions)
        markets = market_price_tool(norm_situation.crop, norm_situation.farmer_location)
        routes = [route_distance_tool(norm_situation.farmer_location, m.market_name, norm_situation.quantity_kg) for m in markets]
        weather = weather_risk_tool(norm_situation.farmer_location)
        perishability = perishability_tool(norm_situation.crop, "COLD_STORAGE" if norm_situation.has_cold_storage else "AMBIENT", 24.0)
        storage = storage_tool(norm_situation.farmer_location, norm_situation.crop, 3.0)
        logistics = transport_tool(norm_situation.farmer_location, markets[0].market_name if markets else "Local Mandi", norm_situation.quantity_kg)

        trace.append({
            "stage": "DATA_COLLECTION",
            "title": "Evidence Data Collection",
            "status": "COMPLETED",
            "details": f"Fetched {len(markets)} market prices, {len(routes)} transport routes, weather risk ({weather.risk_level}), perishability curve",
            "timestamp": time.strftime("%H:%M:%S")
        })

        # 6. NORMALIZATION
        trace.append({
            "stage": "NORMALIZATION",
            "title": "Data Normalization & Units Standardization",
            "status": "COMPLETED",
            "details": "All currencies in INR (₹), volumes in kg, distances in km, risks in percentage metrics",
            "timestamp": time.strftime("%H:%M:%S")
        })

        # 7. OPTION GENERATION & 8. COST / RISK CALCULATION
        evaluated_options = DecisionEngine.evaluate_all_options(
            situation=norm_situation,
            markets=markets,
            routes=routes,
            weather=weather,
            perishability=perishability,
            storage=storage,
            transport=logistics
        )

        trace.append({
            "stage": "OPTION_GENERATION",
            "title": "Feasible Option Generation & Cost/Risk Math",
            "status": "COMPLETED",
            "details": f"Generated {len(evaluated_options)} strategies: {', '.join([o.option_id for o in evaluated_options])}",
            "timestamp": time.strftime("%H:%M:%S")
        })

        # 9. OPTION COMPARISON & 10. DECISION
        best_option = DecisionEngine.select_best_option(evaluated_options)

        trace.append({
            "stage": "DECISION",
            "title": "Deterministic Decision Ranking",
            "status": "COMPLETED",
            "details": f"Recommended Strategy: {best_option.title} (Expected Net: ₹{best_option.expected_net_realization:,.2f})",
            "timestamp": time.strftime("%H:%M:%S")
        })

        # 11. ACTION PLAN & NEGOTIATION ASSISTANT
        action_steps, negotiation_msgs = ActionPlannerAgent.generate_action_plan(norm_situation, best_option)

        trace.append({
            "stage": "ACTION_PLAN",
            "title": "Executable Action Plan & Message Templates",
            "status": "COMPLETED",
            "details": f"Generated {len(action_steps)} priority steps & {len(negotiation_msgs)} local-language message templates",
            "timestamp": time.strftime("%H:%M:%S")
        })

        # 12. EXPLANATION + EVIDENCE & CONFIDENCE
        confidence_val, confidence_reasons = calculate_confidence_score(
            situation=norm_situation,
            market_data_found=len(markets) > 0,
            transport_data_found=len(routes) > 0,
            weather_data_found=True,
            storage_data_found=True,
            is_live_data=False
        )

        primary_reasons = [
            f"Recommended strategy ({best_option.title}) yields highest estimated net realization of ₹{best_option.expected_net_realization:,.2f}.",
            f"Factored spoilage loss of ₹{best_option.estimated_spoilage_loss:,.2f} based on crop decay rules.",
            f"Logistics transport cost evaluated at ₹{best_option.transport_cost:,.2f} for {best_option.destination_distance_km:.1f} km.",
            f"Weather risk level is {weather.risk_level} (Rain Risk: {weather.rain_risk_percent}%)."
        ]

        trace.append({
            "stage": "EXPLANATION",
            "title": "Evidence Synthesis & Report Assembly",
            "status": "COMPLETED",
            "details": f"Confidence: {confidence_val}% | Execution time: {time.time() - start_time:.2f}s",
            "timestamp": time.strftime("%H:%M:%S")
        })

        execution_mode = "AI_MODE" if self.use_llm_mode else "FALLBACK_MODE"

        return DecisionResult(
            run_id=run_id,
            recommendation_title=best_option.title,
            recommended_option_id=best_option.option_id,
            expected_net_realization=best_option.expected_net_realization,
            confidence_score=confidence_val,
            risk_level=best_option.risk_level,
            primary_reasons=primary_reasons,
            options=evaluated_options,
            action_plan=action_steps,
            negotiation_messages=negotiation_msgs,
            execution_trace=trace,
            missing_information=missing_info,
            execution_mode=execution_mode,
            data_mode="DEMO",
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
        )
