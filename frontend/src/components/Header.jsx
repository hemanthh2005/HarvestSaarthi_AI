import React, { useState, useRef, useEffect } from 'react';
import { Sprout, ShieldCheck, Database, Globe, ChevronDown, Search, Check } from 'lucide-react';
import { LANGUAGES, getLanguageByCode } from '../data/languages';
import { useLanguage } from '../context/LanguageContext';

export default function Header({ mode = 'FALLBACK_MODE' }) {
  const { language, setLanguage, t } = useLanguage();
  const [isOpen, setIsOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const dropdownRef = useRef(null);

  const selectedLang = getLanguageByCode(language);

  // Close dropdown on outside click
  useEffect(() => {
    function handleClickOutside(event) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Filter languages by search query
  const filteredLanguages = LANGUAGES.filter((lang) => {
    if (!searchQuery.trim()) return true;
    const q = searchQuery.toLowerCase().trim();
    return (
      lang.name.toLowerCase().includes(q) ||
      lang.native.toLowerCase().includes(q) ||
      lang.code.toLowerCase().includes(q)
    );
  });

  const handleSelectLanguage = (lang) => {
    setLanguage(lang.code);
    setIsOpen(false);
    setSearchQuery('');
  };

  return (
    <header className="border-b border-slate-800 bg-slate-950/90 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Logo & Tagline */}
        <div className="flex items-center space-x-3">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-emerald-400 to-emerald-700 flex items-center justify-center shadow-lg shadow-emerald-900/30">
            <Sprout className="h-6 w-6 text-slate-950" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-extrabold text-lg tracking-tight bg-gradient-to-r from-emerald-300 via-emerald-400 to-teal-200 bg-clip-text text-transparent">
                {t('header.title', 'HARVESTSAARTHI AI')}
              </span>
              <span className="text-[10px] uppercase tracking-widest px-2 py-0.5 rounded bg-emerald-950/80 border border-emerald-500/30 text-emerald-300 font-semibold">
                BHARAT AGENTIC 2026
              </span>
            </div>
            <p className="text-xs text-slate-400 font-medium">{t('header.tagline', '"From Harvest Uncertainty to the Right Next Move."')}</p>
          </div>
        </div>

        {/* Status Badges & Controls */}
        <div className="flex items-center space-x-3">
          {/* Mode Badge */}
          <div className="hidden lg:flex items-center space-x-1.5 text-xs px-2.5 py-1 rounded-full bg-slate-900 border border-slate-700 text-slate-300">
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
            <span>{t('header.mode', 'MODE:')} <strong className="text-emerald-400 font-mono">{mode}</strong></span>
          </div>

          {/* Data Mode */}
          <div className="hidden md:flex items-center space-x-1.5 text-xs px-2.5 py-1 rounded-full bg-amber-950/40 border border-amber-500/30 text-amber-300">
            <Database className="w-3.5 h-3.5 text-amber-400" />
            <span>{t('header.data', 'DATA:')} <strong className="font-mono">{t('header.demoBenchmark', 'DEMO BENCHMARK')}</strong></span>
          </div>

          {/* Searchable 23-Language Farmer Language Selector */}
          <div className="relative" ref={dropdownRef}>
            <button
              type="button"
              onClick={() => setIsOpen(!isOpen)}
              className="flex items-center space-x-2 bg-slate-900 hover:bg-slate-850 px-3 py-1.5 rounded-xl border border-slate-700 text-xs font-semibold text-slate-200 shadow-sm transition-all focus:ring-2 focus:ring-emerald-500/50"
              aria-expanded={isOpen}
              aria-haspopup="true"
            >
              <Globe className="w-4 h-4 text-emerald-400" />
              <span className="hidden sm:inline text-slate-400 text-[11px] font-normal">{t('header.farmerLanguage', 'Farmer Language')}:</span>
              <span className="text-emerald-300 font-bold">{selectedLang.name}</span>
              <span className="text-slate-400 font-normal">({selectedLang.native})</span>
              <ChevronDown className={`w-3.5 h-3.5 text-slate-400 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
            </button>

            {/* Dropdown Menu */}
            {isOpen && (
              <div className="absolute right-0 mt-2 w-72 bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl z-50 overflow-hidden glass-card">
                {/* Header & Search */}
                <div className="p-3 border-b border-slate-800 bg-slate-950/60">
                  <div className="flex items-center justify-between text-xs font-bold text-slate-300 mb-2 px-1">
                    <span className="flex items-center gap-1.5">
                      <Globe className="w-3.5 h-3.5 text-emerald-400" />
                      {t('header.selectionHeader', 'Farmer Language Selection')}
                    </span>
                    <span className="text-[10px] text-slate-500 font-mono">{t('header.languagesCount', '23 Languages')}</span>
                  </div>
                  <div className="relative">
                    <Search className="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-2.5" />
                    <input
                      type="text"
                      placeholder={t('header.searchPlaceholder', 'Search (e.g. Kannada, ಕನ್ನಡ, Hindi)...')}
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      className="w-full bg-slate-950 border border-slate-800 rounded-lg pl-8 pr-3 py-1.5 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-emerald-500"
                      autoFocus
                    />
                  </div>
                </div>

                {/* Languages List */}
                <div className="max-h-64 overflow-y-auto p-1.5 space-y-0.5 divide-y divide-slate-800/40">
                  {filteredLanguages.length > 0 ? (
                    filteredLanguages.map((lang) => {
                      const isSelected = selectedLang.code === lang.code;
                      return (
                        <button
                          key={lang.code}
                          onClick={() => handleSelectLanguage(lang)}
                          className={`w-full text-left px-3 py-2 rounded-xl text-xs flex items-center justify-between transition-all ${
                            isSelected
                              ? 'bg-emerald-950/80 border border-emerald-500/40 text-emerald-300 font-bold'
                              : 'text-slate-300 hover:bg-slate-800/80 hover:text-slate-100'
                          }`}
                        >
                          <div className="flex items-center space-x-2">
                            <span>{lang.name}</span>
                            <span className="text-slate-500">—</span>
                            <span className="text-emerald-400/90 font-medium">{lang.native}</span>
                          </div>
                          {isSelected && <Check className="w-3.5 h-3.5 text-emerald-400" />}
                        </button>
                      );
                    })
                  ) : (
                    <div className="p-4 text-center text-xs text-slate-500">
                      {t('header.noLanguageFound', 'No matching language found.')}
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}
