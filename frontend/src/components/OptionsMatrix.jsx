import React from 'react';
import { TrendingUp } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';

export default function OptionsMatrix({ options = [], recommendedId }) {
  const { t, translateRisk } = useLanguage();

  if (!options.length) return null;

  return (
    <div className="glass-card rounded-2xl p-6 mb-8 border border-slate-800">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-emerald-400" />
            {t('options.title', 'Evaluated Selling & Storage Options')}
          </h2>
          <p className="text-xs text-slate-400">{t('options.description', 'Calculated after applying transport, storage, and crop spoilage math.')}</p>
        </div>
        <span className="text-xs font-semibold text-slate-400 bg-slate-900 px-3 py-1 rounded-full border border-slate-800">
          {options.length} {t('options.strategiesEvaluated', 'Strategies Evaluated')}
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {options.map((opt) => {
          const isRecommended = opt.option_id === recommendedId;

          return (
            <div
              key={opt.option_id}
              className={`rounded-2xl p-5 border flex flex-col justify-between transition-all relative ${
                isRecommended
                  ? 'bg-gradient-to-b from-emerald-950/80 to-slate-900 border-emerald-500/60 shadow-xl shadow-emerald-950/50'
                  : 'bg-slate-900/60 border-slate-800 hover:border-slate-700'
              }`}
            >
              {isRecommended && (
                <div className="absolute -top-3 left-4 bg-emerald-500 text-slate-950 text-[10px] font-black uppercase px-2.5 py-0.5 rounded-full shadow">
                  {t('options.recommendedBadge', 'RECOMMENDED')}
                </div>
              )}

              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-mono font-bold text-slate-400">{opt.option_id}</span>
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded ${
                    opt.feasible
                      ? 'bg-emerald-950 text-emerald-400 border border-emerald-800'
                      : 'bg-red-950 text-red-400 border border-red-800'
                  }`}>
                    {opt.feasible ? t('options.feasible', 'FEASIBLE') : t('options.infeasible', 'INFEASIBLE')}
                  </span>
                </div>

                <h3 className="font-bold text-sm text-slate-100 mb-1 leading-snug">{opt.title}</h3>
                <p className="text-xs text-slate-400 mb-3">{opt.description}</p>

                {/* Arithmetic Breakdown */}
                <div className="space-y-1.5 text-xs bg-slate-950/60 p-3 rounded-xl border border-slate-800/80 mb-3 font-mono">
                  <div className="flex justify-between text-slate-400">
                    <span>{t('options.grossRevenue', 'Gross Revenue:')}</span>
                    <span className="text-slate-200">₹{opt.gross_revenue?.toLocaleString('en-IN')}</span>
                  </div>
                  <div className="flex justify-between text-slate-400">
                    <span>{t('options.transportCost', 'Transport Cost:')}</span>
                    <span className="text-red-400">-₹{opt.transport_cost?.toLocaleString('en-IN')}</span>
                  </div>
                  <div className="flex justify-between text-slate-400">
                    <span>{t('options.storageCost', 'Storage Cost:')}</span>
                    <span className="text-amber-400">-₹{opt.storage_cost?.toLocaleString('en-IN')}</span>
                  </div>
                  <div className="flex justify-between text-slate-400">
                    <span>{t('options.spoilageLoss', 'Spoilage Loss:')}</span>
                    <span className="text-red-400">-₹{opt.estimated_spoilage_loss?.toLocaleString('en-IN')}</span>
                  </div>
                  <div className="flex justify-between text-slate-200 font-bold border-t border-slate-800 pt-1 text-sm">
                    <span>{t('options.expectedNet', 'Expected Net:')}</span>
                    <span className="text-emerald-400">₹{opt.expected_net_realization?.toLocaleString('en-IN')}</span>
                  </div>
                </div>

                {!opt.feasible && opt.infeasibility_reasons?.length > 0 && (
                  <div className="p-2 bg-red-950/40 border border-red-900/50 rounded-lg text-[11px] text-red-300 space-y-1 mb-2">
                    <span className="font-bold block">{t('options.infeasibilityReason', 'Infeasibility Reason:')}</span>
                    {opt.infeasibility_reasons.map((r, i) => (
                      <p key={i}>• {r}</p>
                    ))}
                  </div>
                )}
              </div>

              <div className="text-[11px] text-slate-400 flex items-center justify-between border-t border-slate-800/80 pt-2.5">
                <span>{t('options.timeframe', 'Timeframe:')} <strong>{opt.selling_timeframe}</strong></span>
                <span>{t('options.risk', 'Risk:')} <strong className="text-slate-200">{translateRisk(opt.risk_level)}</strong></span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
