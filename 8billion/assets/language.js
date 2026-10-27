// The entry URL follows the browser unless a visitor chose a language.
// Language-specific URLs stay shareable and never redirect automatically.
(() => {
  const key = '8billion-lang';
  const supported = ['ko', 'en', 'ja', 'zh-hans', 'zh-hant'];
  const pathFor = lang => '/8billion/' + (lang === 'en' ? '' : lang + '/');
  function resolve(tag) {
    const value = String(tag || '').toLowerCase().replace(/_/g, '-');
    if (supported.includes(value)) return value;
    const parts = value.split('-');
    if (parts[0] === 'zh') {
      if (parts.includes('hant')) return 'zh-hant';
      if (parts.includes('hans')) return 'zh-hans';
      return parts.some(p => ['tw', 'hk', 'mo'].includes(p)) ? 'zh-hant' : 'zh-hans';
    }
    return supported.includes(parts[0]) ? parts[0] : null;
  }

  if (/^\/8billion\/(?:index\.html)?$/.test(location.pathname) &&
      !/bot|crawler|spider|slurp/i.test(navigator.userAgent)) {
    let saved;
    try { saved = localStorage.getItem(key); } catch (_) {}
    const requested = resolve(new URLSearchParams(location.search).get('lang'));
    const preferences = navigator.languages && navigator.languages.length
      ? navigator.languages : [navigator.language];
    const chosen = requested || resolve(saved) || preferences.map(resolve).find(Boolean) || 'en';
    if (chosen !== 'en') location.replace(pathFor(chosen) + location.search + location.hash);
  }

  document.addEventListener('click', event => {
    const link = event.target.closest('.language-menu a[data-lang]');
    if (!link) return;
    const lang = link.dataset.lang;
    try {
      if (lang === 'system') localStorage.removeItem(key);
      else localStorage.setItem(key, lang);
    } catch (_) {
      // English shares the automatic entry URL. Keep it explicitly selectable
      // even in browsers that disallow saving preferences.
      if (lang === 'en') link.href = '/8billion/?lang=en';
    }
  });
})();
