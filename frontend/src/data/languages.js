/**
 * HarvestSaarthi AI - Master Multilingual Language Configuration
 * English + 22 Languages of the Eighth Schedule of the Constitution of India.
 * Total: 23 Languages in exact required order.
 */

export const LANGUAGES = [
  { code: 'en', name: 'English', native: 'English', speechLocale: 'en-IN' },
  { code: 'hi', name: 'Hindi', native: 'हिन्दी', speechLocale: 'hi-IN' },
  { code: 'as', name: 'Assamese', native: 'অসমীয়া', speechLocale: 'as-IN' },
  { code: 'bn', name: 'Bengali', native: 'বাংলা', speechLocale: 'bn-IN' },
  { code: 'brx', name: 'Bodo', native: 'बड़ो', speechLocale: 'hi-IN' },
  { code: 'doi', name: 'Dogri', native: 'डोगरी', speechLocale: 'hi-IN' },
  { code: 'gu', name: 'Gujarati', native: 'ગુજરાતી', speechLocale: 'gu-IN' },
  { code: 'kn', name: 'Kannada', native: 'ಕನ್ನಡ', speechLocale: 'kn-IN' },
  { code: 'ks', name: 'Kashmiri', native: 'कश्मीरी', speechLocale: 'ks-IN' },
  { code: 'gom', name: 'Konkani', native: 'कोंकणी', speechLocale: 'gom-IN' },
  { code: 'mai', name: 'Maithili', native: 'मैथिली', speechLocale: 'hi-IN' },
  { code: 'ml', name: 'Malayalam', native: 'മലയാളം', speechLocale: 'ml-IN' },
  { code: 'mni', name: 'Manipuri', native: 'মৈতৈলোন্', speechLocale: 'mni-IN' },
  { code: 'mr', name: 'Marathi', native: 'मराठी', speechLocale: 'mr-IN' },
  { code: 'ne', name: 'Nepali', native: 'नेपाली', speechLocale: 'ne-NP' },
  { code: 'or', name: 'Odia', native: 'ଓଡ଼ିଆ', speechLocale: 'or-IN' },
  { code: 'pa', name: 'Punjabi', native: 'ਪੰਜਾਬੀ', speechLocale: 'pa-IN' },
  { code: 'sa', name: 'Sanskrit', native: 'संस्कृतम्', speechLocale: 'sa-IN' },
  { code: 'sat', name: 'Santali', native: 'ᱥᱟᱱᱛᱟᱲᱤ', speechLocale: 'sat-IN' },
  { code: 'sd', name: 'Sindhi', native: 'سنڌي', speechLocale: 'sd-IN' },
  { code: 'ta', name: 'Tamil', native: 'தமிழ்', speechLocale: 'ta-IN' },
  { code: 'te', name: 'Telugu', native: 'తెలుగు', speechLocale: 'te-IN' },
  { code: 'ur', name: 'Urdu', native: 'اردو', speechLocale: 'ur-IN' },
];

export const DEFAULT_LANGUAGE = LANGUAGES[0]; // English

export function getLanguageByCode(code) {
  if (!code) return DEFAULT_LANGUAGE;
  const found = LANGUAGES.find((l) => l.code.toLowerCase() === code.toLowerCase());
  return found || DEFAULT_LANGUAGE;
}
