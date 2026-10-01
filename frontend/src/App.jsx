import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import HeroDashboard from './components/HeroDashboard';
import DemoSelector from './components/DemoSelector';
import SituationForm from './components/SituationForm';
import ExecutionTrace from './components/ExecutionTrace';
import OptionsMatrix from './components/OptionsMatrix';
import WhatIfSimulator from './components/WhatIfSimulator';
import ActionPlanner from './components/ActionPlanner';
import EvidencePanel from './components/EvidencePanel';
import { postDecision, fetchDemoScenario, fetchCrops } from './services/api';
import { LanguageProvider, useLanguage } from './context/LanguageContext';

function MainLayout() {
  const { t, language } = useLanguage();
  const [loading, setLoading] = useState(false);
  const [crops, setCrops] = useState(["Tomato", "Onion", "Banana", "Potato", "Green Chili", "Paddy", "Maize", "Mango"]);
  const [situation, setSituation] = useState({
    crop: 'Tomato',
    quantity_kg: 2000,
    farmer_location: 'Hassan',
    crop_grade: 'Grade A',
    has_cold_storage: false,
    has_transport: true,
    preferred_selling_radius_km: 150,
    urgency: 'HIGH',
    language: 'en',
  });
  const [decisionResult, setDecisionResult] = useState(null);

  // Load supported crops and initial default demo on start
  useEffect(() => {
    async function init() {
      const cropsRes = await fetchCrops();
      if (cropsRes.success && cropsRes.data) {
        setCrops(cropsRes.data);
      }
      handleSelectDemo('tomato');
    }
    init();
  }, []);

  const handleRunDecision = async (inputSituation) => {
    setLoading(true);
    setSituation(inputSituation);
    const res = await postDecision(inputSituation);
    if (res.success && res.data) {
      setDecisionResult(res.data);
    } else {
      alert(`Decision computation failed: ${res.error || 'Server error'}`);
    }
    setLoading(false);
  };

  const handleSelectDemo = async (demoId) => {
    setLoading(true);
    const res = await fetchDemoScenario(demoId);
    if (res.success && res.data) {
      setSituation(res.data.situation);
      setDecisionResult(res.data.result);
    } else {
      alert(`Failed to load demo scenario: ${res.error || 'Server error'}`);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <Header mode={decisionResult?.execution_mode || 'FALLBACK_MODE'} />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* 1-Click Judge Demo Scenarios */}
        <DemoSelector onSelectDemo={handleSelectDemo} loading={loading} />

        {/* Hero Recommendation Dashboard */}
        <HeroDashboard result={decisionResult} />

        {/* Farmer Input Situation Form */}
        <SituationForm
          onSubmit={handleRunDecision}
          loading={loading}
          crops={crops}
          defaultValues={situation}
        />

        {/* Dynamic What-If Simulator */}
        {decisionResult && (
          <WhatIfSimulator
            situation={situation}
            onResultUpdate={setDecisionResult}
            loading={loading}
          />
        )}

        {/* Agent Execution Trace */}
        {decisionResult && (
          <ExecutionTrace trace={decisionResult.execution_trace} />
        )}

        {/* Evaluated Options Matrix */}
        {decisionResult && (
          <OptionsMatrix
            options={decisionResult.options}
            recommendedId={decisionResult.recommended_option_id}
          />
        )}

        {/* Action Plan & Negotiation Templates */}
        {decisionResult && (
          <ActionPlanner
            actionPlan={decisionResult.action_plan}
            negotiationMessages={decisionResult.negotiation_messages}
          />
        )}

        {/* Evidence & Provenance Panel */}
        {decisionResult && (
          <EvidencePanel result={decisionResult} />
        )}
      </main>

      <footer className="border-t border-slate-900 bg-slate-950 py-6 text-center text-xs text-slate-500">
        {t('footer', 'HarvestSaarthi AI • Submission Prototype for BHARAT AGENTIC 2026 Powered by aiKart')}
      </footer>
    </div>
  );
}

export default function App() {
  return (
    <LanguageProvider>
      <MainLayout />
    </LanguageProvider>
  );
}
