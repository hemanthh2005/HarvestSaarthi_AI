import React, { useState } from 'react';
import { Mic, MicOff, Send, Sliders, AlertCircle } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';

export default function SituationForm({ onSubmit, loading, crops = [], defaultValues = {} }) {
  const { t, translateCrop, currentLanguageObject } = useLanguage();
  const [crop, setCrop] = useState(defaultValues.crop || 'Tomato');
  const [quantityKg, setQuantityKg] = useState(defaultValues.quantity_kg || 2000);
  const [location, setLocation] = useState(defaultValues.farmer_location || 'Hassan');
  const [cropGrade, setCropGrade] = useState(defaultValues.crop_grade || 'Grade A');
  const [hasColdStorage, setHasColdStorage] = useState(defaultValues.has_cold_storage || false);
  const [hasTransport, setHasTransport] = useState(defaultValues.has_transport ?? true);
  const [radiusKm, setRadiusKm] = useState(defaultValues.preferred_selling_radius_km || 150);
  const [urgency, setUrgency] = useState(defaultValues.urgency || 'NORMAL');
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [voiceNotice, setVoiceNotice] = useState(null);

  const currentLang = currentLanguageObject;

  // Browser Speech-to-Text Recognition Handler
  const toggleVoiceInput = () => {
    setVoiceNotice(null);

    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      setVoiceNotice(t('form.voiceNotice', 'Voice input is not available for this language in the current browser. Please use text input.'));
      return;
    }

    if (isListening) {
      setIsListening(false);
      return;
    }

    try {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      const recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = true;
      recognition.lang = currentLang.speechLocale || 'en-IN';

      recognition.onstart = () => {
        setIsListening(true);
        setVoiceNotice(null);
      };

      recognition.onresult = (event) => {
        const text = Array.from(event.results).map(r => r[0].transcript).join('');
        setTranscript(text);
      };

      recognition.onerror = (event) => {
        setIsListening(false);
        if (event.error === 'language-not-supported' || event.error === 'not-allowed' || event.error === 'no-speech') {
          setVoiceNotice(t('form.voiceNotice', 'Voice input is not available for this language in the current browser. Please use text input.'));
        }
      };

      recognition.onend = () => setIsListening(false);
      recognition.start();
    } catch (err) {
      setIsListening(false);
      setVoiceNotice(t('form.voiceNotice', 'Voice input is not available for this language in the current browser. Please use text input.'));
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({
      crop,
      quantity_kg: parseFloat(quantityKg),
      farmer_location: location,
      crop_grade: cropGrade,
      has_cold_storage: hasColdStorage,
      has_transport: hasTransport,
      preferred_selling_radius_km: parseFloat(radiusKm),
      urgency,
      language: currentLang.code,
      raw_input_text: transcript || null,
    });
  };

  return (
    <div className="glass-card rounded-2xl p-6 mb-8 border border-slate-800">
      <div className="flex flex-wrap items-center justify-between gap-3 mb-5">
        <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
          <Sliders className="w-5 h-5 text-emerald-400" />
          {t('form.title', 'Farmer Harvest Situation Input')}
        </h2>

        {/* Voice Input Button */}
        <button
          type="button"
          onClick={toggleVoiceInput}
          className={`flex items-center gap-2 px-3 py-1.5 rounded-xl text-xs font-semibold border transition-all ${
            isListening
              ? 'bg-red-500/20 border-red-500 text-red-300 animate-pulse'
              : 'bg-emerald-950/60 border-emerald-500/40 text-emerald-300 hover:bg-emerald-900/50'
          }`}
        >
          {isListening ? <MicOff className="w-4 h-4 text-red-400" /> : <Mic className="w-4 h-4 text-emerald-400" />}
          <span>{isListening ? t('form.voiceListening', 'Listening (Speak Now)...') : `${t('form.voiceButton', 'Voice Input')} (${currentLang.name} — ${currentLang.native})`}</span>
        </button>
      </div>

      {/* Voice Fallback / Unsupported Notice */}
      {voiceNotice && (
        <div className="mb-4 p-3 bg-amber-950/40 border border-amber-500/40 rounded-xl text-xs text-amber-300 flex items-start gap-2">
          <AlertCircle className="w-4 h-4 text-amber-400 flex-shrink-0 mt-0.5" />
          <span>{voiceNotice}</span>
        </div>
      )}

      {transcript && (
        <div className="mb-4 p-3 bg-emerald-950/40 border border-emerald-800/50 rounded-xl text-xs text-emerald-300">
          🗣️ <strong>{t('form.recognizedSpeech', 'Recognized Speech')} ({currentLang.name}):</strong> "{transcript}"
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
          {/* Crop */}
          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">{t('form.cropType', 'Crop Type')}</label>
            <select
              value={crop}
              onChange={(e) => setCrop(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-100 focus:ring-2 focus:ring-emerald-500"
            >
              {crops.map((c) => (
                <option key={c} value={c}>{translateCrop(c)} ({c})</option>
              ))}
            </select>
          </div>

          {/* Quantity */}
          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">{t('form.quantityKg', 'Harvest Quantity (kg)')}</label>
            <input
              type="number"
              min="10"
              step="50"
              value={quantityKg}
              onChange={(e) => setQuantityKg(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-100 focus:ring-2 focus:ring-emerald-500"
              required
            />
          </div>

          {/* Location */}
          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">{t('form.location', 'Farmer District/Location')}</label>
            <input
              type="text"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-100 focus:ring-2 focus:ring-emerald-500"
              required
            />
          </div>

          {/* Quality Grade */}
          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">{t('form.qualityGrade', 'Crop Quality Grade')}</label>
            <select
              value={cropGrade}
              onChange={(e) => setCropGrade(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-100 focus:ring-2 focus:ring-emerald-500"
            >
              <option value="Grade A">{t('form.gradeA', 'Grade A (Premium)')}</option>
              <option value="Grade B">{t('form.gradeB', 'Grade B (Standard)')}</option>
              <option value="Grade C">{t('form.gradeC', 'Grade C (Commercial)')}</option>
            </select>
          </div>
        </div>

        {/* Toggles & Sliders */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-2">
          {/* Cold Storage Toggle */}
          <div className="flex items-center justify-between p-3 bg-slate-900/60 rounded-xl border border-slate-800">
            <span className="text-xs font-medium text-slate-300">{t('form.coldStorageAvailable', 'Local Cold Storage Available?')}</span>
            <input
              type="checkbox"
              checked={hasColdStorage}
              onChange={(e) => setHasColdStorage(e.target.checked)}
              className="w-4 h-4 accent-emerald-500 rounded cursor-pointer"
            />
          </div>

          {/* Transport Availability */}
          <div className="flex items-center justify-between p-3 bg-slate-900/60 rounded-xl border border-slate-800">
            <span className="text-xs font-medium text-slate-300">{t('form.transportAvailable', 'Transport Truck Available?')}</span>
            <input
              type="checkbox"
              checked={hasTransport}
              onChange={(e) => setHasTransport(e.target.checked)}
              className="w-4 h-4 accent-emerald-500 rounded cursor-pointer"
            />
          </div>

          {/* Selling Radius */}
          <div className="p-3 bg-slate-900/60 rounded-xl border border-slate-800">
            <div className="flex justify-between text-xs font-medium text-slate-300 mb-1">
              <span>{t('form.maxSellingRadius', 'Max Selling Radius:')}</span>
              <strong className="text-emerald-400">{radiusKm} km</strong>
            </div>
            <input
              type="range"
              min="20"
              max="400"
              step="10"
              value={radiusKm}
              onChange={(e) => setRadiusKm(e.target.value)}
              className="w-full accent-emerald-500 cursor-pointer"
            />
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full py-3 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold rounded-xl shadow-lg shadow-emerald-900/40 transition-all flex items-center justify-center space-x-2"
        >
          <Send className="w-4 h-4" />
          <span>{loading ? t('form.submittingButton', 'Agent Computing Optimal Decision Plan...') : `${t('form.submitButton', 'Run HarvestSaarthi Decision Agent')} (${currentLang.native})`}</span>
        </button>
      </form>
    </div>
  );
}
