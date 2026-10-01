import React, { useState } from 'react';
import { RefreshCw, SlidersHorizontal } from 'lucide-react';
import { postWhatIf } from '../services/api';
import { useLanguage } from '../context/LanguageContext';

export default function WhatIfSimulator({ situation, onResultUpdate, loading }) {
  const { t } = useLanguage();
  const [overrideQty, setOverrideQty] = useState(situation?.quantity_kg || 2000);
  const [overridePriceChange, setOverridePriceChange] = useState(0);
  const [overrideColdStorage, setOverrideColdStorage] = useState(situation?.has_cold_storage || false);

  const handleSimulate = async () => {
    const payload = {
      situation,
      override_quantity_kg: parseFloat(overrideQty),
      override_market_price_change_percent: parseFloat(overridePriceChange),
      override_cold_storage: overrideColdStorage,
    };
    const res = await postWhatIf(payload);
    if (res.success && res.data) {
      onResultUpdate(res.data);
    }
  };

  return (
    <div className="glass-card rounded-2xl p-6 mb-8 border border-emerald-500/30 bg-gradient-to-br from-slate-900 to-emerald-950/20">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
            <SlidersHorizontal className="w-5 h-5 text-emerald-400" />
            {t('simulator.title', 'Interactive "What-If?" Scenario Simulator')}
          </h2>
          <p className="text-xs text-slate-400">{t('simulator.description', 'Change parameters below to watch the decision agent recalculate in real time.')}</p>
        </div>
        <span className="text-xs font-bold text-emerald-300 bg-emerald-950 px-2.5 py-1 rounded-full border border-emerald-800">
          {t('simulator.badge', 'Dynamic Reasoning Test')}
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-5 mb-5">
        {/* Quantity Override */}
        <div className="p-4 bg-slate-900/80 rounded-xl border border-slate-800">
          <div className="flex justify-between text-xs font-medium text-slate-300 mb-2">
            <span>{t('simulator.simulateHarvestQty', 'Simulate Harvest Quantity:')}</span>
            <strong className="text-emerald-400 font-mono">{overrideQty} kg</strong>
          </div>
          <input
            type="range"
            min="500"
            max="25000"
            step="500"
            value={overrideQty}
            onChange={(e) => setOverrideQty(e.target.value)}
            className="w-full accent-emerald-500 cursor-pointer"
          />
        </div>

        {/* Price Trend Override */}
        <div className="p-4 bg-slate-900/80 rounded-xl border border-slate-800">
          <div className="flex justify-between text-xs font-medium text-slate-300 mb-2">
            <span>{t('simulator.simulatePriceChange', 'Simulate Market Price Change:')}</span>
            <strong className={`font-mono ${overridePriceChange >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>
              {overridePriceChange > 0 ? `+${overridePriceChange}%` : `${overridePriceChange}%`}
            </strong>
          </div>
          <input
            type="range"
            min="-30"
            max="40"
            step="5"
            value={overridePriceChange}
            onChange={(e) => setOverridePriceChange(e.target.value)}
            className="w-full accent-emerald-500 cursor-pointer"
          />
        </div>

        {/* Storage Availability Override */}
        <div className="p-4 bg-slate-900/80 rounded-xl border border-slate-800 flex items-center justify-between">
          <div>
            <span className="text-xs font-medium text-slate-200 block">{t('simulator.coldStorageAvailable', 'Cold Storage Available?')}</span>
            <span className="text-[11px] text-slate-400">{t('simulator.toggleDesc', 'Toggle to unlock storage strategies')}</span>
          </div>
          <button
            type="button"
            onClick={() => setOverrideColdStorage(!overrideColdStorage)}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all border ${
              overrideColdStorage
                ? 'bg-emerald-600 text-white border-emerald-400'
                : 'bg-slate-800 text-slate-400 border-slate-700'
            }`}
          >
            {overrideColdStorage ? t('simulator.toggleAvailable', '✓ AVAILABLE') : t('simulator.toggleUnavailable', '✕ UNAVAILABLE')}
          </button>
        </div>
      </div>

      <button
        onClick={handleSimulate}
        disabled={loading}
        className="w-full py-2.5 bg-slate-800 hover:bg-slate-700 border border-emerald-500/40 text-emerald-300 text-xs font-bold rounded-xl transition-all flex items-center justify-center space-x-2"
      >
        <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
        <span>{t('simulator.recalculateButton', 'Re-calculate & Evaluate What-If Strategy')}</span>
      </button>
    </div>
  );
}
