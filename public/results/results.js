(() => {
  'use strict';
  const key='navier-stokes-language-v1';
  const url=new URL(location.href);
  let lang=url.searchParams.get('lang');
  if(!['zh','en'].includes(lang)) { try { lang=localStorage.getItem(key); } catch {} }
  if(!['zh','en'].includes(lang)) lang=navigator.language.toLowerCase().startsWith('zh')?'zh':'en';
  document.documentElement.dataset.language=lang;
  document.documentElement.lang=lang==='zh'?'zh-CN':'en';
  try { localStorage.setItem(key,lang); } catch {}
  const active=document.querySelector(`main[data-language="${lang}"]`);
  document.title=active?.dataset.title||document.title;
  for(const a of active?.querySelectorAll('a[href]')||[]) {
    const target=new URL(a.href,location.href);
    if(target.origin===location.origin && !a.getAttribute('href').startsWith('#') && (target.pathname.endsWith('.html')||target.pathname.endsWith('/'))) { target.searchParams.set('lang',lang);a.href=target.href; }
  }
  const button=document.createElement('button');
  button.type='button';button.className='language-switcher';
  button.textContent=lang==='zh'?'English':'中文';button.setAttribute('aria-label',lang==='zh'?'切换为 English':'Switch to Chinese');
  button.addEventListener('click',()=> { const next=lang==='zh'?'en':'zh';const nextUrl=new URL(location.href);nextUrl.searchParams.set('lang',next);nextUrl.hash=nextUrl.hash.replace(/^#(?:zh|en)-/,'#'+next+'-');location.assign(nextUrl); });
  document.body.append(button);
  if(url.hash && /^#(?:zh|en)-/.test(url.hash) && !url.hash.startsWith('#'+lang+'-')) { url.hash=url.hash.replace(/^#(?:zh|en)-/,'#'+lang+'-');history.replaceState(null,'',url); }
  const target=document.getElementById(decodeURIComponent(location.hash.slice(1)));
  if(target) target.scrollIntoView();
  window.addEventListener('load',async()=>{if(window.MathJax?.startup?.promise)await window.MathJax.startup.promise;const anchor=document.getElementById(decodeURIComponent(location.hash.slice(1)));if(anchor)anchor.scrollIntoView();},{once:true});
})();
