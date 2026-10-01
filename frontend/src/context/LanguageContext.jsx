import React, { createContext, useContext, useState, useEffect } from 'react';
import { getTranslation, TRANSLATIONS } from '../i18n/translations';
import { getLanguageByCode } from '../data/languages';

const LanguageContext = createContext();

export const STORAGE_KEY = 'harvestsaarthi_language';

export function LanguageProvider({ children }) {
  const [language, setLanguageState] = useState(() => {
    return localStorage.getItem(STORAGE_KEY) || 'en';
  });

  const setLanguage = (newLangCode) => {
    setLanguageState(newLangCode);
    localStorage.setItem(STORAGE_KEY, newLangCode);
  };

  const t = (keyPath, fallback = '') => {
    return getTranslation(language, keyPath, fallback);
  };

  const translateCrop = (cropName) => {
    if (!cropName) return '';
    return t(`crops.${cropName}`, cropName);
  };

  const translateRisk = (riskLevel) => {
    if (!riskLevel) return '';
    return t(`riskLevels.${riskLevel}`, riskLevel);
  };

  const currentLanguageObject = getLanguageByCode(language);

  return (
    <LanguageContext.Provider value={{
      language,
      setLanguage,
      t,
      translateCrop,
      translateRisk,
      currentLanguageObject,
    }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
}
