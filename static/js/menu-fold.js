document.addEventListener('DOMContentLoaded', () => {
  const root = document.querySelector('.book-menu');
  if (!root) return;

  const STORAGE_KEY = 'bookFoldOpen';
  const load = () => {
    try { return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {}; }
    catch { return {}; }
  };
  const save = (state) => localStorage.setItem(STORAGE_KEY, JSON.stringify(state));

  const state = load();
  const detailsList = root.querySelectorAll('details.js-fold[data-fold-key]');

  // 復元（保存があればそれを優先。なければ「現在ページを含むもの」を開く）
  const path = window.location.pathname.replace(/\/+$/, ''); // 末尾スラッシュ調整
  detailsList.forEach(d => {
    const key = d.getAttribute('data-fold-key');
    if (key in state) {
      d.open = !!state[key];
    } else {
      // 初回：中に現在ページへのリンクがあれば開く
      const hasActive = !!d.querySelector(`a[href="${path}"], a[href="${path}/"]`);
      if (hasActive) d.open = true;
    }
  });

  // 開閉で保存
  detailsList.forEach(d => {
    d.addEventListener('toggle', () => {
      const key = d.getAttribute('data-fold-key');
      state[key] = d.open;
      save(state);
    });

    // 内部リンクをクリックしたタイミングでも現状保存（遷移前に確実に反映）
    d.querySelectorAll('a[href]').forEach(a => {
      a.addEventListener('click', () => {
        const key = d.getAttribute('data-fold-key');
        state[key] = d.open;
        save(state);
      });
    });
  });
});
