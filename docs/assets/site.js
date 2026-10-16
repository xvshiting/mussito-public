// Language lives in the URL; no cookies, analytics, or third-party requests.
(() => {
  const switcher = document.querySelector('[data-language-switch]');
  if (switcher) {
    const target = new URL(switcher.getAttribute('href'), document.baseURI);
    const syncFragment = () => {
      target.hash = window.location.hash;
      switcher.href = target.href;
    };
    syncFragment();
    window.addEventListener('hashchange', syncFragment);
  }
  if (!document.querySelector('[data-mac-status]')) return;
  const english = document.documentElement.lang === 'en';
  const siteRoot = document.documentElement.dataset.siteRoot || '.';
  fetch(new URL(`${siteRoot}/release.json`, document.baseURI), {cache: 'no-cache'})
    .then(response => { if (!response.ok) throw new Error('metadata unavailable'); return response.json(); })
    .then(release => {
      const mac = release.mac;
      const assetRoot = 'https://github.com/xvshiting/mussito-public/releases/download/';
      if (mac?.status === 'published' && mac.signed === true && mac.notarized === true &&
          typeof mac.download_url === 'string' && mac.download_url.startsWith(assetRoot) && mac.download_url.endsWith('.dmg')) {
        document.querySelector('[data-mac-status]').textContent = english ? `Release ${mac.version}` : `正式版 ${mac.version}`;
        const link = document.querySelector('[data-mac-download]');
        link.href = mac.download_url;
        link.textContent = english ? 'Download for Mac ↗' : '下载 Mac 安装包 ↗';
        document.querySelector('[data-mac-note]').textContent = `SHA-256: ${mac.sha256}`;
        document.querySelector('[data-mac-note]').classList.add('checksum');
      }
      const ios = release.iphone;
      if (ios?.status === 'published' && typeof ios.app_store_url === 'string' && /^https:\/\/apps\.apple\.com\/[a-z]{2}\/app\/.+\/id\d+$/.test(ios.app_store_url)) {
        document.querySelector('[data-ios-status]').textContent = english ? 'Available on the App Store' : '已在 App Store 上架';
        const link = document.querySelector('[data-ios-download]');
        link.href = ios.app_store_url;
        link.textContent = english ? 'View on the App Store ↗' : '前往 App Store ↗';
        link.nextElementSibling.textContent = english ? 'See the App Store for pricing and regional availability.' : '价格与可用地区以 App Store 显示为准。';
      }
    })
    .catch(() => { /* Keep accurate static availability and working links. */ });
})();
