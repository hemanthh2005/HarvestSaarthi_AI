import React from 'react';
import { CheckCircle2, Cpu } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';

export default function ExecutionTrace({ trace = [] }) {
  const { t } = useLanguage();

  if (!trace.length) return null;

  return (
    <div className="glass-card rounded-2xl p-5 mb-8 border border-slate-800">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-bold text-slate-200 flex items-center space-x-2">
          <Cpu className="w-4 h-4 text-emerald-400" />
          <span>{t('trace.title', 'Agent Workflow Execution Trace (Auditable Activity)')}</span>
        </h3>
        <span className="text-[11px] text-slate-400 bg-slate-900 px-2 py-0.5 rounded border border-slate-800">
          {t('trace.badge', '12-Stage Agentic Pipeline')}
        </span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
        {trace.map((step, idx) => (
          <div
            key={idx}
            className="bg-slate-900/80 p-3 rounded-xl border border-slate-800 hover:border-emerald-500/30 transition-all flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between mb-1.5">
                <span className="text-[10px] font-extrabold uppercase px-1.5 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-900">
                  {step.stage}
                </span>
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
              </div>
              <h4 className="text-xs font-bold text-slate-200 mb-1">{step.title}</h4>
              <p className="text-[11px] text-slate-400 line-clamp-2">{step.details}</p>
            </div>
            <div className="text-[10px] text-slate-500 mt-2 font-mono">{step.timestamp}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
