import React, { useState } from 'react';
import { ListOrdered, MessageSquare, Copy, Check } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';

export default function ActionPlanner({ actionPlan = [], negotiationMessages = [] }) {
  const { t } = useLanguage();
  const [copiedIdx, setCopiedIdx] = useState(null);

  const copyToClipboard = (text, idx) => {
    navigator.clipboard.writeText(text);
    setCopiedIdx(idx);
    setTimeout(() => setCopiedIdx(null), 2000);
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
      {/* Executable Action Steps */}
      <div className="glass-card rounded-2xl p-6 border border-slate-800">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
            <ListOrdered className="w-5 h-5 text-emerald-400" />
            {t('action.title', 'Executable Action Plan')}
          </h3>
          <span className="text-xs text-slate-400 font-mono">{t('action.sequenceBadge', 'Prioritized Sequence')}</span>
        </div>

        <div className="space-y-3">
          {actionPlan.map((act) => (
            <div key={act.priority} className="p-3 bg-slate-900/80 rounded-xl border border-slate-800 flex items-start gap-3">
              <span className="flex-shrink-0 w-6 h-6 rounded-full bg-emerald-950 border border-emerald-500/40 text-emerald-400 text-xs font-bold flex items-center justify-center">
                {act.priority}
              </span>
              <div className="flex-1 min-w-0">
                <h4 className="text-xs font-bold text-slate-200 mb-0.5">{act.action}</h4>
                <p className="text-[11px] text-slate-400 mb-1">{act.reason}</p>
                <div className="flex items-center space-x-2 text-[10px] text-slate-500">
                  <span>{t('action.dependency', 'Dependency:')} <strong>{act.dependency}</strong></span>
                  <span>•</span>
                  <span className="text-emerald-400 font-mono">{t('action.status', 'STATUS:')} {act.status}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Multilingual Negotiation / Inquiry Templates */}
      <div className="glass-card rounded-2xl p-6 border border-slate-800">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
            <MessageSquare className="w-5 h-5 text-emerald-400" />
            {t('action.templatesTitle', 'Local-Language Communication Templates')}
          </h3>
          <span className="text-xs text-emerald-400 bg-emerald-950 px-2 py-0.5 rounded border border-emerald-900">
            {t('action.readyBadge', 'WhatsApp / SMS Ready')}
          </span>
        </div>

        <div className="space-y-3">
          {negotiationMessages.map((msg, idx) => (
            <div key={idx} className="p-3 bg-slate-900/80 rounded-xl border border-slate-800">
              <div className="flex items-center justify-between mb-1.5">
                <span className="text-xs font-bold text-emerald-300">{msg.title}</span>
                <button
                  onClick={() => copyToClipboard(msg.message_text, idx)}
                  className="flex items-center space-x-1 text-[11px] px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 transition-all border border-slate-700"
                >
                  {copiedIdx === idx ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                  <span>{copiedIdx === idx ? t('action.copied', 'Copied!') : t('action.copyText', 'Copy Text')}</span>
                </button>
              </div>
              <p className="text-xs text-slate-300 whitespace-pre-line font-sans leading-relaxed bg-slate-950/60 p-2.5 rounded-lg border border-slate-800/80">
                {msg.message_text}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
