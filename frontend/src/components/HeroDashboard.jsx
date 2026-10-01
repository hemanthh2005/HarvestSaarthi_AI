import React from 'react';
import { ShieldCheck, Download } from 'lucide-react';
import { getReportDownloadUrl } from '../services/api';
import { useLanguage } from '../context/LanguageContext';

export default function HeroDashboard({ result }) {
  const { t, translateRisk, language } = useLanguage();

  if (!result) return null;

  const isLowRisk = result.risk_level === 'LOW';
  const isMedRisk = result.risk_level === 'MEDIUM';

  const translatedRiskLevel = translateRisk(result.risk_level);

  return (
    <div className="glass-card-accent rounded-3xl p-6 sm:p-8 mb-8 relative overflow-hidden shadow-2xl">
      {/* Background Decorative Glow */}
      <div className="absolute top-0 right-0 -mr-16 -mt-16 w-64 h-64 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />

      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6 relative z-10">
        <div className="space-y-3 max-w-2xl">
          <div className="flex items-center space-x-2">
            <span className="px-3 py-1 rounded-full text-xs font-extrabold uppercase tracking-wider bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">
              {t('hero.recommendedMove', 'RECOMMENDED NEXT MOVE')}
            </span>
            <span className={`px-2.5 py-1 rounded-full text-xs font-bold ${
              isLowRisk ? 'bg-emerald-950 text-emerald-400 border border-emerald-800' :
              isMedRisk ? 'bg-amber-950 text-amber-400 border border-amber-800' : 'bg-red-950 text-red-400 border border-red-800'
            }`}>
              {t('hero.riskLabel', 'RISK:')} {translatedRiskLevel}
            </span>
          </div>

          <h1 className="text-2xl sm:text-3xl font-black text-white tracking-tight leading-tight">
            {result.recommendation_title}
          </h1>

          <div className="flex flex-wrap items-center gap-4 pt-1">
            {result.primary_reasons.slice(0, 3).map((reason, idx) => (
              <div key={idx} className="flex items-center space-x-1.5 text-xs text-slate-300">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                <span>{reason}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Expected Net & Actions */}
        <div className="w-full md:w-auto flex flex-col sm:flex-row md:flex-col items-stretch sm:items-center md:items-end justify-between gap-4 border-t md:border-t-0 border-slate-800 pt-4 md:pt-0">
          <div className="text-left md:text-right">
            <span className="text-xs uppercase font-bold tracking-wider text-slate-400 block mb-1">
              {t('hero.expectedNetRealization', 'EXPECTED NET REALIZATION')}
            </span>
            <div className="text-3xl sm:text-4xl font-black text-emerald-400 flex items-center md:justify-end">
              <span className="text-2xl font-normal mr-0.5">₹</span>
              {result.expected_net_realization?.toLocaleString('en-IN') || '0'}
            </div>
            <div className="flex items-center md:justify-end space-x-2 text-xs text-slate-400 mt-1">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              <span>{t('hero.confidence', 'Confidence:')} <strong className="text-emerald-300 font-bold">{result.confidence_score}%</strong></span>
            </div>
          </div>

          <a
            href={`${getReportDownloadUrl(result.run_id)}?lang=${language}`}
            target="_blank"
            rel="noopener noreferrer"
            className="px-4 py-2.5 bg-slate-900 hover:bg-slate-800 border border-emerald-500/40 text-emerald-300 text-xs font-bold rounded-xl transition-all flex items-center justify-center space-x-2 shadow-lg"
          >
            <Download className="w-4 h-4" />
            <span>{t('hero.downloadPdf', 'Download PDF Report')}</span>
          </a>
        </div>
      </div>
    </div>
  );
}
