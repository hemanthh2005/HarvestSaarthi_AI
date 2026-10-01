"""
HarvestSaarthi AI - Official aiKart Runner Contract Entrypoint
Reads buyer input from /aikart/input.json or AIKART_INPUT environment variable,
invokes the deterministic HarvestSaarthi Orchestrator Agent,
and outputs /aikart/output.json with exact format {"format": "markdown", "response": "..."}.
"""

import json
import os
import sys
from typing import Dict, Any

from backend.models.schemas import FarmerSituation
from backend.agents.orchestrator import OrchestratorAgent

INPUT_FILE_PATH = "/aikart/input.json"
OUTPUT_FILE_PATH = "/aikart/output.json"


def read_aikart_input() -> Dict[str, Any]:
    """Reads input JSON from /aikart/input.json or AIKART_INPUT environment variable."""
    if os.path.exists(INPUT_FILE_PATH):
        with open(INPUT_FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    elif "AIKART_INPUT" in os.environ and os.environ["AIKART_INPUT"].strip():
        raw_env = os.environ["AIKART_INPUT"].strip()
        try:
            return json.loads(raw_env)
        except json.JSONDecodeError:
            return {"crop": "Tomato", "quantity_kg": 2000, "location": "Hassan", "raw_text": raw_env}
    else:
        # Fallback default input if executed without arguments
        return {
            "crop": "Tomato",
            "quantity_kg": 2000,
            "location": "Hassan",
            "harvest_timing": "Tomorrow Morning",
            "storage_available": False,
            "transport_available": True,
            "preferred_language": "English",
        }


def format_markdown_response(result) -> str:
    """Formats decision result into clean, professional, farmer-facing Markdown."""
    reasons_list = "\n".join([f"- {r}" for r in result.primary_reasons])

    options_list = []
    for opt in result.options:
        status_str = "FEASIBLE" if opt.feasible else "INFEASIBLE"
        options_list.append(
            f"| **{opt.option_id}** | {opt.title} | {opt.target_market} | Rs. {opt.gross_revenue:,.0f} | "
            f"Rs. {opt.transport_cost:,.0f} | Rs. {opt.estimated_spoilage_loss:,.0f} | **Rs. {opt.expected_net_realization:,.0f}** | {opt.risk_level} ({status_str}) |"
        )
    options_table = "\n".join(options_list)

    action_list = []
    for act in result.action_plan:
        action_list.append(f"{act.priority}. **{act.action}** — *{act.reason}* (Dependency: {act.dependency})")
    action_plan_str = "\n".join(action_list)

    md = f"""# HARVESTSAARTHI AI — POST-HARVEST DECISION REPORT
> *"From Harvest Uncertainty to the Right Next Move."*

---

### 🎯 RECOMMENDED NEXT MOVE
**{result.recommendation_title}**

- **Expected Net Realization:** Rs. {result.expected_net_realization:,.2f}
- **Confidence Score:** {result.confidence_score}%
- **Risk Level:** {result.risk_level}
- **Execution Mode:** {result.execution_mode}
- **Data Mode:** {result.data_mode} BENCHMARK

---

### 💡 WHY THIS RECOMMENDATION?
{reasons_list}

---

### 📊 EVALUATED SELLING & STORAGE STRATEGIES
| Option ID | Strategy Title | Target Market | Gross Rev | Transport | Spoilage Loss | Expected Net | Risk & Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
{options_table}

---

### 📋 EXECUTABLE ACTION PLAN
{action_plan_str}

---

### 🛡️ DISCLAIMER
{result.disclaimer}
"""
    return md


def main():
    try:
        data = read_aikart_input()

        # Parse inputs into FarmerSituation
        crop = str(data.get("crop") or "Tomato")
        qty = float(data.get("quantity_kg") or data.get("quantity") or 2000.0)
        location = str(data.get("location") or data.get("farmer_location") or "Hassan")
        timing = str(data.get("harvest_timing") or "Tomorrow Morning")
        storage_avail = bool(data.get("storage_available") or data.get("has_cold_storage") or False)
        transport_avail = bool(data.get("transport_available") or data.get("has_transport") or True)
        lang = str(data.get("preferred_language") or "en").lower()
        if lang.startswith("kan"):
            lang = "kn"
        elif lang.startswith("hin"):
            lang = "hi"
        else:
            lang = "en"

        situation = FarmerSituation(
            crop=crop,
            quantity_kg=qty,
            farmer_location=location,
            harvest_date=timing,
            has_cold_storage=storage_avail,
            has_transport=transport_avail,
            language=lang,
        )

        # Run Orchestrator Agent Workflow
        orchestrator = OrchestratorAgent(use_llm_mode=False)
        result = orchestrator.process_situation(situation)

        # Format Markdown Output
        markdown_str = format_markdown_response(result)

        output_payload = {
            "format": "markdown",
            "response": markdown_str
        }

        # Determine output location (/aikart/output.json or local fallback)
        out_path = OUTPUT_FILE_PATH
        out_dir = os.path.dirname(out_path)
        if out_dir and not os.path.exists(out_dir):
            try:
                os.makedirs(out_dir, exist_ok=True)
            except Exception:
                out_path = "output.json"

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(output_payload, f, indent=2, ensure_ascii=False)

        print(f"[aiKart Runner] Output successfully written to {out_path}")
        sys.exit(0)

    except Exception as e:
        print(f"[aiKart Runner ERROR] Execution failed: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
