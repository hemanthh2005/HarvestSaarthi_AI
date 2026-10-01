"""
HarvestSaarthi AI - Deterministic Decision Engine
Performs pure Python arithmetic for option evaluation, revenue calculation,
spoilage loss estimation, transport cost calculation, feasibility filtering, and ranking.
"""

from typing import List, Dict, Any, Optional
from backend.models.schemas import (
    FarmerSituation,
    MarketPriceData,
    RouteDistanceData,
    WeatherRiskData,
    PerishabilityData,
    StorageInfo,
    TransportInfo,
    EvaluatedOption,
)
from backend.knowledge.crop_rules import get_crop_info
from backend.decision.confidence import calculate_confidence_score


class DecisionEngine:
    """Pure Python deterministic engine for evaluating post-harvest options."""

    @staticmethod
    def evaluate_all_options(
        situation: FarmerSituation,
        markets: List[MarketPriceData],
        routes: List[RouteDistanceData],
        weather: WeatherRiskData,
        perishability: PerishabilityData,
        storage: StorageInfo,
        transport: TransportInfo,
    ) -> List[EvaluatedOption]:
        """Generate and evaluate all standard post-harvest options deterministically."""
        options: List[EvaluatedOption] = []
        crop_info = get_crop_info(situation.crop)
        qty = situation.quantity_kg

        # Helper to match route by market name
        def get_route(market_name: str) -> Optional[RouteDistanceData]:
            for r in routes:
                if r.destination.lower() in market_name.lower() or market_name.lower() in r.destination.lower():
                    return r
            return None

        # --- OPTION A: Sell at nearest mandi today ---
        if markets:
            nearest_market = min(markets, key=lambda m: m.distance_km)
            route_a = get_route(nearest_market.market_name)
            dist_a = route_a.distance_km if route_a else nearest_market.distance_km
            t_cost_a = route_a.estimated_transport_cost if route_a else (dist_a * (qty / 1000.0) * 12.0)

            # Spoilage for 1 day / immediate dispatch
            spoilage_pct_a = min(perishability.spoilage_risk_percent * 0.25, 2.0)
            spoilage_loss_a = qty * (spoilage_pct_a / 100.0) * nearest_market.price_per_kg
            gross_a = qty * nearest_market.price_per_kg
            net_a = gross_a - t_cost_a - 0.0 - spoilage_loss_a

            feasible_a = True
            infeasible_reasons_a = []
            if dist_a > situation.preferred_selling_radius_km:
                feasible_a = False
                infeasible_reasons_a.append(f"Exceeds preferred radius ({dist_a:.1f} km > {situation.preferred_selling_radius_km} km)")

            options.append(
                EvaluatedOption(
                    option_id="OPTION_A",
                    option_type="SELL_NEAREST_TODAY",
                    title=f"Sell Today at Nearest Market ({nearest_market.market_name})",
                    description=f"Immediate dispatch to local mandi ({dist_a:.1f} km away). Minimizes spoilage and delay risks.",
                    target_market=nearest_market.market_name,
                    destination_distance_km=dist_a,
                    selling_timeframe="Within 24 Hours",
                    gross_revenue=round(gross_a, 2),
                    transport_cost=round(t_cost_a, 2),
                    storage_cost=0.0,
                    estimated_spoilage_loss=round(spoilage_loss_a, 2),
                    other_costs=0.0,
                    expected_net_realization=round(net_a, 2),
                    risk_level="LOW" if weather.risk_level != "HIGH" else "MEDIUM",
                    confidence_score=88.0,
                    feasible=feasible_a,
                    infeasibility_reasons=infeasible_reasons_a,
                    evidence=[
                        {"label": "Market Price", "value": f"₹{nearest_market.price_per_kg}/kg", "source": nearest_market.source},
                        {"label": "Distance", "value": f"{dist_a:.1f} km", "source": "Logistics Engine"},
                        {"label": "Spoilage Risk", "value": f"{spoilage_pct_a:.1f}%", "source": "Crop Knowledge Engine"},
                    ],
                )
            )

        # --- OPTION B: Transport to higher-price distant market ---
        if len(markets) > 1:
            # Pick highest price market that is NOT the nearest
            nearest_m_name = min(markets, key=lambda m: m.distance_km).market_name
            distant_markets = [m for m in markets if m.market_name != nearest_m_name]
            if distant_markets:
                highest_price_market = max(distant_markets, key=lambda m: m.price_per_kg)
                route_b = get_route(highest_price_market.market_name)
                dist_b = route_b.distance_km if route_b else highest_price_market.distance_km
                t_cost_b = route_b.estimated_transport_cost if route_b else (dist_b * (qty / 1000.0) * 14.0)

                # Higher transit time -> slightly higher spoilage during transport
                spoilage_pct_b = min(perishability.spoilage_risk_percent * 0.6, 6.0)
                spoilage_loss_b = qty * (spoilage_pct_b / 100.0) * highest_price_market.price_per_kg
                gross_b = qty * highest_price_market.price_per_kg
                net_b = gross_b - t_cost_b - 0.0 - spoilage_loss_b

                feasible_b = True
                infeasible_reasons_b = []
                if dist_b > situation.preferred_selling_radius_km:
                    feasible_b = False
                    infeasible_reasons_b.append(f"Exceeds preferred radius ({dist_b:.1f} km > {situation.preferred_selling_radius_km} km)")
                if weather.risk_level == "HIGH":
                    infeasible_reasons_b.append("High weather delay risk for long-distance transit")

                options.append(
                    EvaluatedOption(
                        option_id="OPTION_B",
                        option_type="TRANSPORT_DISTANT_MARKET",
                        title=f"Transport to High-Price Market ({highest_price_market.market_name})",
                        description=f"Ship to premium mandi ({dist_b:.1f} km away) offering ₹{highest_price_market.price_per_kg}/kg.",
                        target_market=highest_price_market.market_name,
                        destination_distance_km=dist_b,
                        selling_timeframe="24-48 Hours",
                        gross_revenue=round(gross_b, 2),
                        transport_cost=round(t_cost_b, 2),
                        storage_cost=0.0,
                        estimated_spoilage_loss=round(spoilage_loss_b, 2),
                        other_costs=0.0,
                        expected_net_realization=round(net_b, 2),
                        risk_level="MEDIUM" if weather.risk_level == "LOW" else "HIGH",
                        confidence_score=82.0,
                        feasible=feasible_b,
                        infeasibility_reasons=infeasible_reasons_b,
                        evidence=[
                            {"label": "Market Price", "value": f"₹{highest_price_market.price_per_kg}/kg", "source": highest_price_market.source},
                            {"label": "Distance", "value": f"{dist_b:.1f} km", "source": "Logistics Engine"},
                            {"label": "Transit Spoilage", "value": f"{spoilage_pct_b:.1f}%", "source": "Crop Knowledge Engine"},
                        ],
                    )
                )

        # --- OPTION C: Store temporarily and sell later (2-3 days) ---
        target_m_for_storage = min(markets, key=lambda m: m.distance_km) if markets else None
        if target_m_for_storage:
            price_c = target_m_for_storage.price_per_kg * 1.08  # Projected price uptick (+8%)
            gross_c = qty * price_c
            days_stored = 3.0
            storage_rate = storage.cost_per_kg_day if storage.available else 0.50
            storage_cost_c = qty * storage_rate * days_stored

            # Spoilage depends heavily on cold storage availability
            if storage.available or situation.has_cold_storage:
                spoilage_rate_daily = crop_info.get("cold_storage_spoilage_rate_per_day", 0.015)
            else:
                spoilage_rate_daily = crop_info.get("base_spoilage_rate_per_day", 0.08)

            spoilage_pct_c = min(spoilage_rate_daily * days_stored * 100.0, 30.0)
            spoilage_loss_c = qty * (spoilage_pct_c / 100.0) * price_c

            route_c = get_route(target_m_for_storage.market_name)
            dist_c = route_c.distance_km if route_c else target_m_for_storage.distance_km
            t_cost_c = route_c.estimated_transport_cost if route_c else (dist_c * (qty / 1000.0) * 12.0)
            net_c = gross_c - t_cost_c - storage_cost_c - spoilage_loss_c

            feasible_c = True
            infeasible_reasons_c = []
            if crop_info.get("perishability_tier") == "HIGH" and not (storage.available or situation.has_cold_storage):
                feasible_c = False
                infeasible_reasons_c.append("Crop is highly perishable and no cold storage facility is available")

            options.append(
                EvaluatedOption(
                    option_id="OPTION_C",
                    option_type="STORE_AND_SELL_LATER",
                    title=f"Store Temporarily ({days_stored:.0f} Days) & Sell Later",
                    description=f"Store at local facility and sell at projected higher price (₹{price_c:.1f}/kg).",
                    target_market=target_m_for_storage.market_name,
                    destination_distance_km=dist_c,
                    selling_timeframe=f"After {days_stored:.0f} Days Storage",
                    gross_revenue=round(gross_c, 2),
                    transport_cost=round(t_cost_c, 2),
                    storage_cost=round(storage_cost_c, 2),
                    estimated_spoilage_loss=round(spoilage_loss_c, 2),
                    other_costs=0.0,
                    expected_net_realization=round(net_c, 2),
                    risk_level="MEDIUM" if (storage.available or situation.has_cold_storage) else "HIGH",
                    confidence_score=75.0,
                    feasible=feasible_c,
                    infeasibility_reasons=infeasible_reasons_c,
                    evidence=[
                        {"label": "Projected Price", "value": f"₹{price_c:.1f}/kg (+8%)", "source": "Market Trend Model"},
                        {"label": "Storage Cost", "value": f"₹{storage_cost_c:.2f} ({days_stored:.0f} days)", "source": "Storage Engine"},
                        {"label": "Estimated Spoilage", "value": f"{spoilage_pct_c:.1f}%", "source": "Crop Decay Model"},
                    ],
                )
            )

        # --- OPTION D: Split Harvest (50% local today, 50% distant market) ---
        if len(markets) > 1:
            m_near = min(markets, key=lambda m: m.distance_km)
            m_dist_list = [m for m in markets if m.market_name != m_near.market_name]
            if m_dist_list:
                m_far = max(m_dist_list, key=lambda m: m.price_per_kg)
                qty_half = qty / 2.0

                r_near = get_route(m_near.market_name)
                d_near = r_near.distance_km if r_near else m_near.distance_km
                tc_near = r_near.estimated_transport_cost * 0.55 if r_near else (d_near * (qty_half / 1000.0) * 12.0)

                r_far = get_route(m_far.market_name)
                d_far = r_far.distance_km if r_far else m_far.distance_km
                tc_far = r_far.estimated_transport_cost * 0.55 if r_far else (d_far * (qty_half / 1000.0) * 14.0)

                gross_d = (qty_half * m_near.price_per_kg) + (qty_half * m_far.price_per_kg)
                t_cost_d = tc_near + tc_far

                spoil_near = qty_half * 0.01 * m_near.price_per_kg
                spoil_far = qty_half * 0.04 * m_far.price_per_kg
                spoilage_loss_d = spoil_near + spoil_far

                net_d = gross_d - t_cost_d - 0.0 - spoilage_loss_d

                options.append(
                    EvaluatedOption(
                        option_id="OPTION_D",
                        option_type="SPLIT_MARKET",
                        title=f"Split Harvest (50% {m_near.market_name} + 50% {m_far.market_name})",
                        description=f"Hedge risk by selling 50% locally and shipping 50% to higher-priced {m_far.market_name}.",
                        target_market=f"{m_near.market_name} & {m_far.market_name}",
                        destination_distance_km=round((d_near + d_far) / 2.0, 1),
                        selling_timeframe="24-36 Hours",
                        gross_revenue=round(gross_d, 2),
                        transport_cost=round(t_cost_d, 2),
                        storage_cost=0.0,
                        estimated_spoilage_loss=round(spoilage_loss_d, 2),
                        other_costs=0.0,
                        expected_net_realization=round(net_d, 2),
                        risk_level="LOW",
                        confidence_score=80.0,
                        feasible=True,
                        infeasibility_reasons=[],
                        evidence=[
                            {"label": "Near Price", "value": f"₹{m_near.price_per_kg}/kg", "source": m_near.source},
                            {"label": "Distant Price", "value": f"₹{m_far.price_per_kg}/kg", "source": m_far.source},
                            {"label": "Hedging Strategy", "value": "50/50 Split Risk Reduction", "source": "Risk Engine"},
                        ],
                    )
                )

        return options

    @staticmethod
    def select_best_option(options: List[EvaluatedOption]) -> EvaluatedOption:
        """Filter feasible options and rank by expected net realization."""
        feasible_options = [o for o in options if o.feasible]
        if feasible_options:
            return max(feasible_options, key=lambda o: o.expected_net_realization)
        # Fallback to option with highest net realization if none fully feasible
        return max(options, key=lambda o: o.expected_net_realization)
