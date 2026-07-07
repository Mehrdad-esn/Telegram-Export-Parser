import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'

import faCommon from '../public/locales/fa/common.json'
import enCommon from '../public/locales/en/common.json'

const resources = {
  fa: { common: faCommon },
  en: { common: enCommon },
}

i18n.use(initReactI18next).init({
  resources,
  lng: 'fa',
  fallbackLng: 'fa',
  ns: ['common'],
  defaultNS: 'common',
  interpolation: { escapeValue: false },
  returnObjects: true,
})

export function changeLanguage(language: string) {
  i18n.changeLanguage(language)
}

export default i18n
