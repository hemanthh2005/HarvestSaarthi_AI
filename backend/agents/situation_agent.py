"""
HarvestSaarthi AI - Situation Understanding Agent
Normalizes user input, interprets natural language/voice text, and detects missing information.
"""

from typing import Tuple, List
import re
from backend.models.schemas import FarmerSituation


class SituationUnderstandingAgent:
    """Agent responsible for understanding and normalizing harvest situations."""

    @staticmethod
    def analyze_situation(situation: FarmerSituation) -> Tuple[FarmerSituation, List[str], List[str]]:
        """
        Processes situation inputs, normalizes values, and returns:
        (Normalized FarmerSituation, missing_information_list, understanding_notes)
        """
        missing: List[str] = []
        notes: List[str] = []

        # If raw text input is provided (e.g. from speech-to-text or freeform input)
        if situation.raw_input_text:
            text = situation.raw_input_text.lower()
            # Simple entity extraction heuristic if user entered text
            if "tomato" in text:
                situation.crop = "Tomato"
            elif "onion" in text:
                situation.crop = "Onion"
            elif "banana" in text:
                situation.crop = "Banana"
            elif "potato" in text:
                situation.crop = "Potato"
            elif "chili" in text or "chilli" in text:
                situation.crop = "Green Chili"
            elif "paddy" in text or "rice" in text:
                situation.crop = "Paddy"

            # Quantity extraction e.g. "2000 kg", "2 ton", "50 bags"
            match_qty = re.search(r"(\d+)\s*(kg|ton|tonne|quintal)", text)
            if match_qty:
                val = float(match_qty.group(1))
                unit = match_qty.group(2)
                if unit in ["ton", "tonne"]:
                    situation.quantity_kg = val * 1000.0
                elif unit == "quintal":
                    situation.quantity_kg = val * 100.0
                else:
                    situation.quantity_kg = val

            # Storage detection
            if "cold storage" in text or "coldhouse" in text:
                situation.has_cold_storage = True
            elif "no storage" in text:
                situation.has_cold_storage = False

        # Validate mandatory fields
        if not situation.crop:
            missing.append("Crop type not specified")
        else:
            notes.append(f"Identified crop: {situation.crop}")

        if situation.quantity_kg <= 0:
            missing.append("Quantity in kg is missing or non-positive")
        else:
            notes.append(f"Harvest volume: {situation.quantity_kg:,.0f} kg")

        if not situation.farmer_location:
            missing.append("Farmer location/district is missing")
        else:
            notes.append(f"Origin location: {situation.farmer_location}")

        notes.append(f"Quality grade: {situation.crop_grade}")
        notes.append(f"Cold storage available: {'Yes' if situation.has_cold_storage else 'No'}")
        notes.append(f"Transport available: {'Yes' if situation.has_transport else 'No'}")

        return situation, missing, notes
