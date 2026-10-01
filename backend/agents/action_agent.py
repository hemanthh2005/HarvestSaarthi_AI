"""
HarvestSaarthi AI - Action Planning & Negotiation Agent
Generates prioritized executable action steps and multilingual buyer/logistics message templates.
"""

from typing import List, Tuple
from backend.models.schemas import FarmerSituation, EvaluatedOption, ActionStep, NegotiationMessage


class ActionPlannerAgent:
    """Agent that converts decisions into concrete actions and communication templates."""

    @staticmethod
    def generate_action_plan(
        situation: FarmerSituation,
        selected_option: EvaluatedOption
    ) -> Tuple[List[ActionStep], List[NegotiationMessage]]:
        """Produces prioritized action steps and multilingual message templates."""
        steps: List[ActionStep] = []

        # Step 1: Quality & Volume Confirmation
        steps.append(
            ActionStep(
                priority=1,
                action=f"Confirm exact harvest quantity ({situation.quantity_kg:,.0f} kg) and grade ({situation.crop_grade}).",
                reason="Prevents mismatch during mandi weighing and price grading.",
                dependency="Harvest Inspection",
                status="PENDING",
            )
        )

        # Step 2: Mandi / Buyer Confirmation
        steps.append(
            ActionStep(
                priority=2,
                action=f"Contact buyer/trader at {selected_option.target_market} to confirm active purchase rates.",
                reason="Mandi prices fluctuate daily; recheck before loading produce.",
                dependency="Mandi Price Verification",
                status="PENDING",
            )
        )

        # Step 3: Transport / Storage Booking
        if "STORE" in selected_option.option_type:
            steps.append(
                ActionStep(
                    priority=3,
                    action=f"Reserve storage slot at local facility in {situation.farmer_location}.",
                    reason=f"Secures storage space at estimated ₹{selected_option.storage_cost:,.2f} total cost.",
                    dependency="Storage Availability Check",
                    status="PENDING",
                )
            )
        else:
            steps.append(
                ActionStep(
                    priority=3,
                    action=f"Book transport vehicle for dispatch to {selected_option.target_market} ({selected_option.destination_distance_km:.1f} km).",
                    reason=f"Secures logistics truck at estimated cost of ₹{selected_option.transport_cost:,.2f}.",
                    dependency="Transport Booking",
                    status="PENDING",
                )
            )

        # Step 4: Dispatch & Timing
        steps.append(
            ActionStep(
                priority=4,
                action=f"Dispatch produce within recommended window ({selected_option.selling_timeframe}).",
                reason="Minimizes post-harvest spoilage loss and delay risks.",
                dependency="Logistics Loading",
                status="PENDING",
            )
        )

        # Step 5: Final Settlement Verification
        steps.append(
            ActionStep(
                priority=5,
                action="Verify weighment slip and immediate bank/cash settlement at market.",
                reason="Ensures full expected net realization without unverified deductions.",
                dependency="Produce Delivery",
                status="PENDING",
            )
        )

        # Multilingual Negotiation & Inquiry Messages
        messages: List[NegotiationMessage] = []
        crop = situation.crop
        qty = situation.quantity_kg
        grade = situation.crop_grade
        market = selected_option.target_market
        lang = situation.language.lower()

        # English Templates
        msg_en_buyer = (
            f"Namaskara, I have approximately {qty:,.0f} kg of {grade} {crop} ready for dispatch. "
            f"Please confirm today's purchase price and available buying quota at {market}."
        )
        msg_en_transport = (
            f"Hello, I need transport for {qty:,.0f} kg of {crop} from {situation.farmer_location} to {market} "
            f"({selected_option.destination_distance_km:.1f} km). Please confirm vehicle availability and rate quote."
        )

        # Kannada Templates (Kannada script + transliteration for accessibility)
        msg_kn_buyer = (
            f"ನಮಸ್ಕಾರ, ನನ್ನ ಬಳಿ ಸುಮಾರು {qty:,.0f} kg {grade} {crop} ಬೆಳೆ ಸಿದ್ಧವಾಗಿದೆ. "
            f"{market} ಮಾರುಕಟ್ಟೆಯಲ್ಲಿ ಇಂದಿನ ಖರೀದಿ ಬೆಲೆ ಮತ್ತು ಲಭ್ಯತೆಯನ್ನು ದಯವಿಟ್ಟು ಖಚಿತಪಡಿಸಿ.\n"
            f"(Namaskara, nanna bali sumaru {qty:,.0f} kg {crop} ready ide. {market} mandi price confirm maadi.)"
        )
        msg_kn_transport = (
            f"ನಮಸ್ಕಾರ, {situation.farmer_location} ನಿಂದ {market} ಗೆ {qty:,.0f} kg {crop} ಸಾಗಿಸಲು ವಾಹನ ಬೇಕಾಗಿದೆ. "
            f"ದಯವಿಟ್ಟು ಬಾಡಿಗೆ ದರ ತಿಳಿಸಿ.\n"
            f"(Namaskara, {situation.farmer_location} ninda {market} ge transport vehicle beku. Rate maahiti kodi.)"
        )

        # Hindi Templates
        msg_hi_buyer = (
            f"नमस्कार, मेरे पास लगभग {qty:,.0f} kg {grade} {crop} उपज तैयार है। "
            f"कृपया {market} मंडी में आज का खरीद भाव और लोड क्षमता कन्फर्म करें।"
        )
        msg_hi_transport = (
            f"नमस्कार, {situation.farmer_location} से {market} के लिए {qty:,.0f} kg {crop} परिवहन हेतु ट्रक चाहिए। "
            f"कृपया भाड़ा दर और उपलब्धता बताएं।"
        )

        # Append messages based on target language or default trio
        if lang == "kn":
            messages.append(NegotiationMessage(template_type="BUYER_INQUIRY", language="kn", title="ಖರೀದಿದಾರರ ವಿಚಾರಣೆ (Buyer Inquiry - Kannada)", message_text=msg_kn_buyer))
            messages.append(NegotiationMessage(template_type="TRANSPORT_REQUEST", language="kn", title="ಸಾರಿಗೆ ವಿನಂತಿ (Transport Request - Kannada)", message_text=msg_kn_transport))
        elif lang == "hi":
            messages.append(NegotiationMessage(template_type="BUYER_INQUIRY", language="hi", title="खरीदार पूछताछ (Buyer Inquiry - Hindi)", message_text=msg_hi_buyer))
            messages.append(NegotiationMessage(template_type="TRANSPORT_REQUEST", language="hi", title="परिवहन अनुरोध (Transport Request - Hindi)", message_text=msg_hi_transport))
        elif lang == "en":
            messages.append(NegotiationMessage(template_type="BUYER_INQUIRY", language="en", title="Buyer Price Verification (English)", message_text=msg_en_buyer))
            messages.append(NegotiationMessage(template_type="TRANSPORT_REQUEST", language="en", title="Logistics & Truck Booking (English)", message_text=msg_en_transport))
        else:
            messages.append(NegotiationMessage(template_type="BUYER_INQUIRY", language="en", title=f"Buyer Verification ({lang.upper()} Default: English)", message_text=msg_en_buyer))
            messages.append(NegotiationMessage(template_type="BUYER_INQUIRY", language="kn", title="ಖರೀದಿದಾರರ ವಿಚಾರಣೆ (Kannada)", message_text=msg_kn_buyer))
            messages.append(NegotiationMessage(template_type="BUYER_INQUIRY", language="hi", title="खरीदार पूछताछ (Hindi)", message_text=msg_hi_buyer))
            messages.append(NegotiationMessage(
                template_type="NOTICE",
                language=lang,
                title=f"Language Support Note ({lang.upper()})",
                message_text=f"Direct WhatsApp negotiation templates for {lang.upper()} are currently defaulting to English/Hindi. All decision math and recommendations remain 100% active."
            ))

        return steps, messages
