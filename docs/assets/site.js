// Same-origin public release metadata; no analytics or third-party requests.
(() => {
  if (!document.querySelector('[data-mac-status]')) return;
  fetch('release.json', {cache: 'no-cache'})
    .then(response => { if (!response.ok) throw new Error('metadata unavailable'); return response.json(); })
    .then(release => {
      const mac = release.mac;
      const assetRoot = 'https://github.com/xvshiting/mussito-public/releases/download/';
      if (mac?.status === 'published' && mac.signed === true && mac.notarized === true &&
          typeof mac.download_url === 'string' && mac.download_url.startsWith(assetRoot) && mac.download_url.endsWith('.dmg')) {
        document.querySelector('[data-mac-status]').textContent = `正式版 ${mac.version}`;
        const link = document.querySelector('[data-mac-download]');
        link.href = mac.download_url; link.textContent = '下载 Mac 安装包 ↗';
        document.querySelector('[data-mac-note]').textContent = `SHA-256：${mac.sha256}`;
        document.querySelector('[data-mac-note]').classList.add('checksum');
      }
      const ios = release.iphone;
      if (ios?.status === 'published' && typeof ios.app_store_url === 'string' && /^https:\/\/apps\.apple\.com\/[a-z]{2}\/app\/.+\/id\d+$/.test(ios.app_store_url)) {
        document.querySelector('[data-ios-status]').textContent = '已在 App Store 上架';
        const link = document.querySelector('[data-ios-download]');
        link.href = ios.app_store_url; link.textContent = '前往 App Store ↗';
        link.nextElementSibling.textContent = '价格与可用地区以 App Store 显示为准。';
      }
    })
    .catch(() => { /* Keep accurate static availability and working links. */ });
})();
