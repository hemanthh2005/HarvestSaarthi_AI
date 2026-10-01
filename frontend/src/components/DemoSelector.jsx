import React from 'react';
import { Play, Sparkles } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';

export default function DemoSelector({ onSelectDemo, loading }) {
  const { t, translateCrop } = useLanguage();

  const demos = [
    {
      id: 'tomato',
      crop: 'Tomato',
      translatedCrop: translateCrop('Tomato'),
      title: t('demo.demos.tomato.title', 'DEMO 1: Tomato Farmer (Hassan)'),
      description: t('demo.demos.tomato.description', '2,000 kg harvest • High perishability • No cold storage available'),
      expected: t('demo.demos.tomato.expected', 'Sell quickly at nearby Hassan Mandi (Minimizes spoilage loss)'),
    },
    {
      id: 'onion',
      crop: 'Onion',
      translatedCrop: translateCrop('Onion'),
      title: t('demo.demos.onion.title', 'DEMO 2: Onion Farmer (Kolar)'),
      description: t('demo.demos.onion.description', '10,000 kg harvest • Low perishability • Storage available'),
      expected: t('demo.demos.onion.expected', 'Store 3 days for higher price premium (Storage option feasible)'),
    },
    {
      id: 'banana',
      crop: 'Banana',
      translatedCrop: translateCrop('Banana'),
      title: t('demo.demos.banana.title', 'DEMO 3: Banana Farmer (Mysuru)'),
      description: t('demo.demos.banana.description', '3,000 kg harvest • Rain risk 65% • Imminent harvest'),
      expected: t('demo.demos.banana.expected', 'Urgent transport dispatch to Bangalore Yeshwanthpur'),
    }
  ];

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 mb-8">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <Sparkles className="w-5 h-5 text-emerald-400" />
          <h2 className="text-base font-bold text-slate-100">
            {t('demo.title', '1-Click Judge Demo Scenarios')}
          </h2>
        </div>
        <span className="text-xs text-slate-400 bg-slate-800 px-2.5 py-1 rounded-full border border-slate-700">
          {t('demo.badge', 'Deterministic Test Cases')}
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {demos.map(demo => (
          <button
            key={demo.id}
            onClick={() => onSelectDemo(demo.id)}
            disabled={loading}
            className="text-left p-4 rounded-xl glass-card hover:border-emerald-500/50 hover:bg-slate-800/80 transition-all group relative overflow-hidden"
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-bold px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800">
                {demo.translatedCrop}
              </span>
              <div className="w-7 h-7 rounded-full bg-emerald-900/50 flex items-center justify-center group-hover:bg-emerald-600 transition-all">
                <Play className="w-3.5 h-3.5 text-emerald-300 group-hover:text-white fill-current ml-0.5" />
              </div>
            </div>
            <h3 className="font-bold text-sm text-slate-200 group-hover:text-emerald-300 mb-1">
              {demo.title}
            </h3>
            <p className="text-xs text-slate-400 mb-2">{demo.description}</p>
            <div className="text-[11px] text-emerald-400/90 bg-emerald-950/40 p-2 rounded border border-emerald-900/40">
              💡 <strong>{t('demo.expectedOutcomeLabel', 'Expected Outcome:')}</strong> {demo.expected}
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
