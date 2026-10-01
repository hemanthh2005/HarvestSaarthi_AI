import React from 'react';
import { Database, ShieldAlert, Thermometer, Truck, MapPin } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';

export default function EvidencePanel({ result }) {
  const { t } = useLanguage();

  if (!result) return null;

  return (
    <div className="glass-card rounded-2xl p-6 border border-slate-800">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
            <Database className="w-5 h-5 text-emerald-400" />
            {t('evidence.title', 'Evidence & Data Provenance Panel')}
          </h3>
          <p className="text-xs text-slate-400">{t('evidence.description', 'All recommendation decisions are backed by empirical tool data.')}</p>
        </div>
        <div className="flex items-center space-x-2 text-xs">
          <span className="px-2.5 py-0.5 rounded-full font-bold bg-amber-950 text-amber-300 border border-amber-800 font-mono">
            {t('evidence.dataMode', 'DATA MODE:')} {result.data_mode}
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
        {/* Source 1: Market Dataset */}
        <div className="p-3.5 bg-slate-900/80 rounded-xl border border-slate-800">
          <div className="flex items-center space-x-2 text-xs font-bold text-slate-200 mb-1">
            <MapPin className="w-4 h-4 text-emerald-400" />
            <span>{t('evidence.mandiDataset', 'Mandi Price Dataset')}</span>
          </div>
          <p className="text-xs text-slate-400 mb-2">{t('evidence.mandiDesc', 'Benchmark price feeds across Karnataka & South Indian APMCs.')}</p>
          <div className="text-[11px] text-slate-500 font-mono">{t('evidence.sourceLabel', 'Source:')} HarvestSaarthi Prototype Dataset</div>
        </div>

        {/* Source 2: Logistics Rate Model */}
        <div className="p-3.5 bg-slate-900/80 rounded-xl border border-slate-800">
          <div className="flex items-center space-x-2 text-xs font-bold text-slate-200 mb-1">
            <Truck className="w-4 h-4 text-emerald-400" />
            <span>{t('evidence.logisticsRates', 'Logistics & Route Rates')}</span>
          </div>
          <p className="text-xs text-slate-400 mb-2">{t('evidence.logisticsDesc', 'Distance-matrix calculations for TATA Ace & 6-Wheeler trucks.')}</p>
          <div className="text-[11px] text-slate-500 font-mono">{t('evidence.sourceLabel', 'Source:')} HarvestSaarthi Logistics Engine</div>
        </div>

        {/* Source 3: Perishability & Weather */}
        <div className="p-3.5 bg-slate-900/80 rounded-xl border border-slate-800">
          <div className="flex items-center space-x-2 text-xs font-bold text-slate-200 mb-1">
            <Thermometer className="w-4 h-4 text-emerald-400" />
            <span>{t('evidence.cropDecay', 'Crop Decay & Weather Risk')}</span>
          </div>
          <p className="text-xs text-slate-400 mb-2">{t('evidence.cropDecayDesc', 'Perishability curves and temperature/rainfall delay risks.')}</p>
          <div className="text-[11px] text-slate-500 font-mono">{t('evidence.sourceLabel', 'Source:')} Crop Knowledge & Weather Model</div>
        </div>
      </div>

      <div className="mt-4 p-3 bg-slate-950/80 rounded-xl border border-slate-800/80 text-[11px] text-slate-400 flex items-start space-x-2">
        <ShieldAlert className="w-4 h-4 text-amber-400 flex-shrink-0 mt-0.5" />
        <div>
          <strong className="text-slate-300">{t('evidence.disclaimerLabel', 'Decision Support Disclaimer:')}</strong> {result.disclaimer}
        </div>
      </div>
    </div>
  );
}
