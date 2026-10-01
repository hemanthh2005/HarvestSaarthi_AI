/**
 * HarvestSaarthi AI - Centralized Translation Dictionary
 * Includes complete UI translations for English and Kannada (ಕನ್ನಡ)
 * with robust fallback to English.
 */

export const TRANSLATIONS = {
  en: {
    header: {
      title: "HARVESTSAARTHI AI",
      tagline: '"From Harvest Uncertainty to the Right Next Move."',
      mode: "MODE:",
      data: "DATA:",
      demoBenchmark: "DEMO BENCHMARK",
      farmerLanguage: "Farmer Language",
      searchPlaceholder: "Search (e.g. Kannada, ಕನ್ನಡ, Hindi)...",
      noLanguageFound: "No matching language found.",
      languagesCount: "23 Languages",
      selectionHeader: "Farmer Language Selection",
    },
    demo: {
      title: "1-Click Judge Demo Scenarios",
      badge: "Deterministic Test Cases",
      expectedOutcomeLabel: "Expected Outcome:",
      demos: {
        tomato: {
          title: "DEMO 1: Tomato Farmer (Hassan)",
          description: "2,000 kg harvest • High perishability • No cold storage available",
          expected: "Sell quickly at nearby Hassan Mandi (Minimizes spoilage loss)",
        },
        onion: {
          title: "DEMO 2: Onion Farmer (Kolar)",
          description: "10,000 kg harvest • Low perishability • Storage available",
          expected: "Store 3 days for higher price premium (Storage option feasible)",
        },
        banana: {
          title: "DEMO 3: Banana Farmer (Mysuru)",
          description: "3,000 kg harvest • Rain risk 65% • Imminent harvest",
          expected: "Urgent transport dispatch to Bangalore Yeshwanthpur",
        },
      },
    },
    hero: {
      recommendedMove: "RECOMMENDED NEXT MOVE",
      riskLabel: "RISK:",
      expectedNetRealization: "EXPECTED NET REALIZATION",
      confidence: "Confidence:",
      downloadPdf: "Download PDF Report",
    },
    form: {
      title: "Farmer Harvest Situation Input",
      voiceButton: "Voice Input",
      voiceListening: "Listening (Speak Now)...",
      cropType: "Crop Type",
      quantityKg: "Harvest Quantity (kg)",
      location: "Farmer District/Location",
      qualityGrade: "Crop Quality Grade",
      gradeA: "Grade A (Premium)",
      gradeB: "Grade B (Standard)",
      gradeC: "Grade C (Commercial)",
      coldStorageAvailable: "Local Cold Storage Available?",
      transportAvailable: "Transport Truck Available?",
      maxSellingRadius: "Max Selling Radius:",
      submitButton: "Run HarvestSaarthi Decision Agent",
      submittingButton: "Agent Computing Optimal Decision Plan...",
      voiceNotice: "Voice input is not available for this language in the current browser. Please use text input.",
      recognizedSpeech: "Recognized Speech",
    },
    simulator: {
      title: 'Interactive "What-If?" Scenario Simulator',
      description: "Change parameters below to watch the decision agent recalculate in real time.",
      badge: "Dynamic Reasoning Test",
      simulateHarvestQty: "Simulate Harvest Quantity:",
      simulatePriceChange: "Simulate Market Price Change:",
      coldStorageAvailable: "Cold Storage Available?",
      toggleAvailable: "✓ AVAILABLE",
      toggleUnavailable: "✕ UNAVAILABLE",
      toggleDesc: "Toggle to unlock storage strategies",
      recalculateButton: "Re-calculate & Evaluate What-If Strategy",
    },
    trace: {
      title: "Agent Workflow Execution Trace (Auditable Activity)",
      badge: "12-Stage Agentic Pipeline",
    },
    options: {
      title: "Evaluated Selling & Storage Options",
      description: "Calculated after applying transport, storage, and crop spoilage math.",
      strategiesEvaluated: "Strategies Evaluated",
      recommendedBadge: "RECOMMENDED",
      feasible: "FEASIBLE",
      infeasible: "INFEASIBLE",
      grossRevenue: "Gross Revenue:",
      transportCost: "Transport Cost:",
      storageCost: "Storage Cost:",
      spoilageLoss: "Spoilage Loss:",
      expectedNet: "Expected Net:",
      infeasibilityReason: "Infeasibility Reason:",
      timeframe: "Timeframe:",
      risk: "Risk:",
    },
    action: {
      title: "Executable Action Plan",
      sequenceBadge: "Prioritized Sequence",
      dependency: "Dependency:",
      status: "STATUS:",
      templatesTitle: "Local-Language Communication Templates",
      readyBadge: "WhatsApp / SMS Ready",
      copyText: "Copy Text",
      copied: "Copied!",
    },
    evidence: {
      title: "Evidence & Data Provenance Panel",
      description: "All recommendation decisions are backed by empirical tool data.",
      dataMode: "DATA MODE:",
      mandiDataset: "Mandi Price Dataset",
      mandiDesc: "Benchmark price feeds across Karnataka & South Indian APMCs.",
      logisticsRates: "Logistics & Route Rates",
      logisticsDesc: "Distance-matrix calculations for TATA Ace & 6-Wheeler trucks.",
      cropDecay: "Crop Decay & Weather Risk",
      cropDecayDesc: "Perishability curves and temperature/rainfall delay risks.",
      sourceLabel: "Source:",
      disclaimerLabel: "Decision Support Disclaimer:",
    },
    crops: {
      Tomato: "Tomato",
      Onion: "Onion",
      Banana: "Banana",
      Potato: "Potato",
      "Green Chili": "Green Chili",
      Paddy: "Paddy",
      Maize: "Maize",
      Mango: "Mango",
    },
    riskLevels: {
      LOW: "LOW",
      MEDIUM: "MEDIUM",
      HIGH: "HIGH",
    },
    footer: "HarvestSaarthi AI • Submission Prototype for BHARAT AGENTIC 2026 Powered by aiKart",
  },
  kn: {
    header: {
      title: "ಹಾರ್ವೆಸ್ಟ್ ಸಾರಥಿ AI",
      tagline: '"ಕೊಯ್ಲಿನ ಅನಿಶ್ಚಿತತೆಯಿಂದ ಸರಿಯಾದ ಮುಂದಿನ ಕ್ರಮದವರೆಗೆ."',
      mode: "ವಿಧಾನ:",
      data: "ಮಾಹಿತಿ:",
      demoBenchmark: "ಡೆಮೊ ಮಾನದಂಡ",
      farmerLanguage: "ರೈತರ ಭಾಷೆ",
      searchPlaceholder: "ಹುಡುಕಿ (ಉದಾ. ಕನ್ನಡ, Hindi, English)...",
      noLanguageFound: "ಯಾವುದೇ ಭಾಷೆ ಕಂಡುಬಂದಿಲ್ಲ.",
      languagesCount: "23 ಭಾಷೆಗಳು",
      selectionHeader: "ರೈತರ ಭಾಷೆಯ ಆಯ್ಕೆ",
    },
    demo: {
      title: "1-ಕ್ಲಿಕ್ ನ್ಯಾಯಾಧೀಶರ ಡೆಮೊ ಸನ್ನಿವೇಶಗಳು",
      badge: "ನಿರ್ದಿಷ್ಟ ಪರೀಕ್ಷಾ ಪ್ರಕರಣಗಳು",
      expectedOutcomeLabel: "ನಿರೀಕ್ಷಿತ ಫಲಿತಾಂಶ:",
      demos: {
        tomato: {
          title: "ಡೆಮೊ 1: ಟೊಮ್ಯಾಟೊ ಬೆಳೆಗಾರ (ಹಾಸನ)",
          description: "2,000 ಕೆಜಿ ಕೊಯ್ಲು • ಹೆಚ್ಚಿನ ಹಾಳಾಗುವಿಕೆ • ಶೀತಲ ಸಂಗ್ರಹಣೆ ಲಭ್ಯವಿಲ್ಲ",
          expected: "ಸಮೀಪದ ಹಾಸನ ಮಂಡಿಯಲ್ಲಿ ತ್ವರಿತವಾಗಿ ಮಾರಾಟ ಮಾಡಿ (ಹಾಳಾಗುವ ನಷ್ಟವನ್ನು ಕಡಿಮೆ ಮಾಡುತ್ತದೆ)",
        },
        onion: {
          title: "ಡೆಮೊ 2: ಈರುಳ್ಳಿ ಬೆಳೆಗಾರ (ಕೋಲಾರ)",
          description: "10,000 ಕೆಜಿ ಕೊಯ್ಲು • ಕಡಿಮೆ ಹಾಳಾಗುವಿಕೆ • ಸಂಗ್ರಹಣೆ ಲಭ್ಯವಿದೆ",
          expected: "ಹೆಚ್ಚಿನ ಬೆಲೆಗಾಗಿ 3 ದಿನ ಸಂಗ್ರಹಿಸಿ (ಸಂಗ್ರಹಣಾ ಆಯ್ಕೆ ಸಾಧ್ಯವಿದೆ)",
        },
        banana: {
          title: "ಡೆಮೊ 3: ಬಾಳೆ ಬೆಳೆಗಾರ (ಮೈಸೂರು)",
          description: "3,000 ಕೆಜಿ ಕೊಯ್ಲು • ಮಳೆಯ ಅಪಾಯ 65% • ತಕ್ಷಣದ ಕೊಯ್ಲು",
          expected: "ಬೆಂಗಳೂರು ಯಶವಂತಪುರಕ್ಕೆ ತುರ್ತು ಸಾರಿಗೆ ರವಾನೆ",
        },
      },
    },
    hero: {
      recommendedMove: "ಶಿಫಾರಸು ಮಾಡಲಾದ ಮುಂದಿನ ಕ್ರಮ",
      riskLabel: "ಅಪಾಯ:",
      expectedNetRealization: "ನಿರೀಕ್ಷಿತ ನಿವ್ವಳ ಆದಾಯ",
      confidence: "ವಿಶ್ವಾಸಾರ್ಹತೆ:",
      downloadPdf: "PDF ವರದಿ ಡೌನ್ಲೋಡ್ ಮಾಡಿ",
    },
    form: {
      title: "ರೈತರ ಕೊಯ್ಲಿನ ಸನ್ನಿವೇಶದ ವಿವರಗಳು",
      voiceButton: "ಧ್ವನಿ ನಮೂದು",
      voiceListening: "ಆಲಿಸಲಾಗುತ್ತಿದೆ (ಈಗ ಮಾತನಾಡಿ)...",
      cropType: "ಬೆಳೆಯ ಪ್ರಕಾರ",
      quantityKg: "ಕೊಯ್ಲಿನ ಪ್ರಮಾಣ (ಕೆಜಿ)",
      location: "ರೈತರ ಜಿಲ್ಲೆ/ಸ್ಥಳ",
      qualityGrade: "ಬೆಳೆಯ ಗುಣಮಟ್ಟದ ದರ್ಜೆ",
      gradeA: "ದರ್ಜೆ ಎ (ಉತ್ತಮ ಶ್ರೇಷ್ಠ)",
      gradeB: "ದರ್ಜೆ ಬಿ (ಸಾಮಾನ್ಯ)",
      gradeC: "ದರ್ಜೆ ಸಿ (ವಾಣಿಜ್ಯ)",
      coldStorageAvailable: "ಸ್ಥಳೀಯ ಶೀತಲ ಸಂಗ್ರಹಣೆ ಲಭ್ಯವಿದೆಯೇ?",
      transportAvailable: "ಸಾರಿಗೆ ಟ್ರಕ್ ಲಭ್ಯವಿದೆಯೇ?",
      maxSellingRadius: "ಗರಿಷ್ಠ ಮಾರಾಟ ವ್ಯಾಪ್ತಿ:",
      submitButton: "ಹಾರ್ವೆಸ್ಟ್ ಸಾರಥಿ ನಿರ್ಧಾರ ಏಜೆಂಟ್ ಚಾಲನೆ ಮಾಡಿ",
      submittingButton: "ಏಜೆಂಟ್ ಸೂಕ್ತ ನಿರ್ಧಾರ ಯೋಜನೆಯನ್ನು ಲೆಕ್ಕಾಚಾರ ಮಾಡುತ್ತಿದೆ...",
      voiceNotice: "ಪ್ರಸ್ತುತ ಬ್ರೌಸರ್‌ನಲ್ಲಿ ಈ ಭಾಷೆಗೆ ಧ್ವನಿ ನಮೂದು ಲಭ್ಯವಿಲ್ಲ. ದಯವಿಟ್ಟು ಪಠ್ಯ ನಮೂದನ್ನು ಬಳಸಿ.",
      recognizedSpeech: "ಗುರುತಿಸಿದ ಧ್ವನಿ",
    },
    simulator: {
      title: 'ಸಂವಾದಾತ್ಮಕ "ಏನಾಗಬಹುದು?" ಸನ್ನಿವೇಶದ ಸಿಮ್ಯುಲೇಟರ್',
      description: "ನೈಜ ಸಮಯದಲ್ಲಿ ನಿರ್ಧಾರ ಏಜೆಂಟ್ ಮರುಲೆಕ್ಕಾಚಾರ ಮಾಡುವುದನ್ನು ವೀಕ್ಷಿಸಲು ಕೆಳಗಿನ ನಿಯತಾಂಕಗಳನ್ನು ಬದಲಾಯಿಸಿ.",
      badge: "ಕ್ರಿಯಾತ್ಮಕ ತರ್ಕ ಪರೀಕ್ಷೆ",
      simulateHarvestQty: "ಕೊಯ್ಲಿನ ಪ್ರಮಾಣವನ್ನು ಸಿಮ್ಯುಲೇಟ್ ಮಾಡಿ:",
      simulatePriceChange: "ಮಾರುಕಟ್ಟೆ ಬೆಲೆಯ ಬದಲಾವಣೆಯನ್ನು ಸಿಮ್ಯುಲೇಟ್ ಮಾಡಿ:",
      coldStorageAvailable: "ಶೀತಲ ಸಂಗ್ರಹಣೆ ಲಭ್ಯವಿದೆಯೇ?",
      toggleAvailable: "✓ ಲಭ್ಯವಿದೆ",
      toggleUnavailable: "✕ ಲಭ್ಯವಿಲ್ಲ",
      toggleDesc: "ಸಂಗ್ರಹಣಾ ತಂತ್ರಗಳನ್ನು ಅನ್‌ಲಾಕ್ ಮಾಡಲು ಟಾಗಲ್ ಮಾಡಿ",
      recalculateButton: "ಮರುಲೆಕ್ಕಾಚಾರ ಮಾಡಿ ಮತ್ತು ಸನ್ನಿವೇಶವನ್ನು ಮೌಲ್ಯಮಾಪನ ಮಾಡಿ",
    },
    trace: {
      title: "ಏಜೆಂಟ್ ವರ್ಕ್‌ಫ್ಲೋ ಮೌಲ್ಯಮಾಪನ ಟ್ರೇಸ್ (ಆಡಿಟ್ ಮಾಡಬಹುದಾದ ಚಟುವಟಿಕೆ)",
      badge: "12-ಹಂತದ ಏಜೆಂಟ್ ಪೈಪ್‌ಲೈನ್",
    },
    options: {
      title: "ಮೌಲ್ಯಮಾಪನ ಮಾಡಿದ ಮಾರಾಟ ಮತ್ತು ಸಂಗ್ರಹಣಾ ಆಯ್ಕೆಗಳು",
      description: "ಸಾರಿಗೆ, ಸಂಗ್ರಹಣೆ ಮತ್ತು ಬೆಳೆ ಹಾಳಾಗುವಿಕೆಯ ಲೆಕ್ಕಾಚಾರದ ನಂತರ ಲೆಕ್ಕಹಾಕಲಾಗಿದೆ.",
      strategiesEvaluated: "ಮೌಲ್ಯಮಾಪನ ಮಾಡಿದ ತಂತ್ರಗಳು",
      recommendedBadge: "ಶಿಫಾರಸು ಮಾಡಲಾಗಿದೆ",
      feasible: "ಸಾಧ್ಯವಿದೆ",
      infeasible: "ಸಾಧ್ಯವಿಲ್ಲ",
      grossRevenue: "ಒಟ್ಟು ಆದಾಯ:",
      transportCost: "ಸಾರಿಗೆ ವೆಚ್ಚ:",
      storageCost: "ಸಂಗ್ರಹಣಾ ವೆಚ್ಚ:",
      spoilageLoss: "ಹಾಳಾಗುವಿಕೆಯ ನಷ್ಟ:",
      expectedNet: "ನಿರೀಕ್ಷಿತ ನಿವ್ವಳ:",
      infeasibilityReason: "ಸಾಧ್ಯವಿಲ್ಲದಿರಲು ಕಾರಣ:",
      timeframe: "ಸಮಯದ ಮಿತಿ:",
      risk: "ಅಪಾಯ:",
    },
    action: {
      title: "ಕಾರ್ಯಗತಗೊಳಿಸಬಹುದಾದ ಕಾರ್ಯಯೋಜನೆ",
      sequenceBadge: "ಆದ್ಯತೆಯ ಅನುಕ್ರಮ",
      dependency: "ಅವಲಂಬನೆ:",
      status: "ಸ್ಥಿತಿ:",
      templatesTitle: "ಸ್ಥಳೀಯ ಭಾಷೆಯ ಸಂವಹನ ಟೆಂಪ್ಲೇಟ್‌ಗಳು",
      readyBadge: "WhatsApp / SMS ಸಿದ್ಧವಾಗಿದೆ",
      copyText: "ಪಠ್ಯ ನಕಲಿಸಿ",
      copied: "ನಕಲಿಸಲಾಗಿದೆ!",
    },
    evidence: {
      title: "ಸಾಕ್ಷ್ಯ ಮತ್ತು ಮಾಹಿತಿ ಮೂಲ ಫಲಕ",
      description: "ಎಲ್ಲಾ ಶಿಫಾರಸು ನಿರ್ಧಾರಗಳು ಪ್ರಾಯೋಗಿಕ ಉಪಕರಣಗಳ ಮಾಹಿತಿಯಿಂದ ಬೆಂಬಲಿತವಾಗಿವೆ.",
      dataMode: "ಮಾಹಿತಿ ವಿಧಾನ:",
      mandiDataset: "ಮಂಡಿ ಬೆಲೆ ಮಾಹಿತಿ ಮೂಲ",
      mandiDesc: "ಕರ್ನಾಟಕ ಮತ್ತು ದಕ್ಷಿಣ ಭಾರತದ ಎಪಿಎಂಸಿ ಮಾರುಕಟ್ಟೆಗಳ ಬೆಲೆ ಲೈವ್ ಬಂಚ್‌ಮಾರ್ಕ್.",
      logisticsRates: "ಲಾಜಿಸ್ಟಿಕ್ಸ್ ಮತ್ತು ಮಾರ್ಗದ ದರಗಳು",
      logisticsDesc: "ಟಾಟಾ ಏಸ್ ಮತ್ತು 6-ಚಕ್ರದ ಟ್ರಕ್‌ಗಳ ದೂರದ ವೆಚ್ಚದ ಲೆಕ್ಕಾಚಾರಗಳು.",
      cropDecay: "ಬೆಳೆ ಹಾಳಾಗುವಿಕೆ ಮತ್ತು ಹವಾಮಾನ ಅಪಾಯ",
      cropDecayDesc: "ಹಾಳಾಗುವಿಕೆಯ ಪ್ರಮಾಣ ಮತ್ತು ತಾಪಮಾನ/ಮಳೆಯ ವಿಳಂಬದ ಅಪಾಯಗಳು.",
      sourceLabel: "ಮೂಲ:",
      disclaimerLabel: "ನಿರ್ಧಾರ ಬೆಂಬಲ ಹಕ್ಕುತ್ಯಾಗ:",
    },
    crops: {
      Tomato: "ಟೊಮ್ಯಾಟೊ",
      Onion: "ಈರುಳ್ಳಿ",
      Banana: "ಬಾಳೆಹಣ್ಣು",
      Potato: "ಆಲೂಗಡ್ಡೆ",
      "Green Chili": "ಹಸಿಮೆಣಸಿನಕಾಯಿ",
      Paddy: "ಭತ್ತ",
      Maize: "ಮೆಕ್ಕೆಜೋಳ",
      Mango: "ಮಾವಿನಹಣ್ಣು",
    },
    riskLevels: {
      LOW: "ಕಡಿಮೆ",
      MEDIUM: "ಮಧ್ಯಮ",
      HIGH: "ಹೆಚ್ಚು",
    },
    footer: "ಹಾರ್ವೆಸ್ಟ್ ಸಾರಥಿ AI • BHARAT AGENTIC 2026 Powered by aiKart",
  },
};

/**
 * Resolves nested translation keys (e.g. 'hero.recommendedMove') for current language,
 * falling back to English if the key or language is not defined.
 */
export function getTranslation(langCode, keyPath, fallback = '') {
  const lang = (langCode || 'en').toLowerCase();
  const dict = TRANSLATIONS[lang] || TRANSLATIONS.en;
  
  const keys = keyPath.split('.');
  let current = dict;
  
  for (const k of keys) {
    if (current && typeof current === 'object' && k in current) {
      current = current[k];
    } else {
      current = undefined;
      break;
    }
  }

  if (typeof current === 'string') {
    return current;
  }

  // Fallback to English if current language missing key
  if (lang !== 'en') {
    let enCurrent = TRANSLATIONS.en;
    for (const k of keys) {
      if (enCurrent && typeof enCurrent === 'object' && k in enCurrent) {
        enCurrent = enCurrent[k];
      } else {
        enCurrent = undefined;
        break;
      }
    }
    if (typeof enCurrent === 'string') {
      return enCurrent;
    }
  }

  return fallback || keyPath;
}
