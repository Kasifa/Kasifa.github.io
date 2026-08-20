(() => {
  "use strict";

  const storageKey = "navier-stokes-language-v1";
  const translations = globalThis.NS_EN_TRANSLATIONS ?? {};
  const chinesePattern = /[\u3400-\u9fff\uf900-\ufaff]/u;
  const translatedAttributes = ["alt", "aria-label", "content", "placeholder", "title"];
  const skippedTags = new Set(["SCRIPT", "STYLE", "NOSCRIPT"]);

  function normalize(value) {
    return value.replace(/\s+/g, " ").trim();
  }

  function selectedLanguage() {
    const requested = new URLSearchParams(location.search).get("lang");
    if (requested === "zh" || requested === "en") {
      try { localStorage.setItem(storageKey, requested); } catch {}
      return requested;
    }

    try {
      const saved = localStorage.getItem(storageKey);
      if (saved === "zh" || saved === "en") return saved;
    } catch {}

    return navigator.language.toLowerCase().startsWith("zh") ? "zh" : "en";
  }

  function translateTextNodes() {
    const walker = document.createTreeWalker(
      document.documentElement,
      NodeFilter.SHOW_TEXT,
      {
        acceptNode(node) {
          if (!node.parentElement || skippedTags.has(node.parentElement.tagName)) {
            return NodeFilter.FILTER_REJECT;
          }
          const key = normalize(node.nodeValue ?? "");
          return chinesePattern.test(key) && translations[key]
            ? NodeFilter.FILTER_ACCEPT
            : NodeFilter.FILTER_REJECT;
        },
      },
    );

    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    for (const node of nodes) {
      const source = node.nodeValue ?? "";
      const key = normalize(source);
      const leading = source.match(/^\s*/)?.[0] ?? "";
      const trailing = source.match(/\s*$/)?.[0] ?? "";
      node.nodeValue = `${leading}${translations[key]}${trailing}`;
    }
  }

  function translateAttributes() {
    for (const element of document.querySelectorAll("*")) {
      for (const attribute of translatedAttributes) {
        if (!element.hasAttribute(attribute)) continue;
        if (attribute === "content" && element.tagName !== "META") continue;
        const source = element.getAttribute(attribute) ?? "";
        const translation = translations[normalize(source)];
        if (translation) element.setAttribute(attribute, translation);
      }
    }
  }

  function addSwitcher(language) {
    const target = language === "zh" ? "en" : "zh";
    const button = document.createElement("button");
    button.type = "button";
    button.className = "language-switcher";
    button.lang = target === "en" ? "en" : "zh-CN";
    button.textContent = target === "en" ? "English" : "中文";
    button.setAttribute(
      "aria-label",
      target === "en" ? "切换为 English" : "Switch to Chinese",
    );
    button.addEventListener("click", () => {
      try { localStorage.setItem(storageKey, target); } catch {}
      const url = new URL(location.href);
      url.searchParams.set("lang", target);
      location.replace(url.href);
    });
    document.body.append(button);
  }

  function labelChinesePdfDownloads() {
    for (const link of document.querySelectorAll('a[href$=".pdf"]')) {
      const url = new URL(link.href, location.href);
      if (url.origin !== location.origin || !url.pathname.startsWith("/notes/")) {
        continue;
      }
      const label = document.createElement("span");
      label.className = "pdf-language-label";
      label.textContent = " (Chinese PDF)";
      link.append(label);
      link.title = "This download is the Chinese PDF. Use Print / PDF for an English copy.";
    }
  }

  const language = selectedLanguage();
  document.documentElement.lang = language === "en" ? "en" : "zh-CN";
  document.documentElement.dataset.language = language;
  if (language === "en") {
    translateTextNodes();
    translateAttributes();
    labelChinesePdfDownloads();
  }
  if (window.parent !== window) {
    try {
      const parentTitle =
        language === "en"
          ? "The 3D Navier–Stokes Global Regularity Problem"
          : "三维 Navier–Stokes 全局正则性问题";
      window.parent.document.title = parentTitle;
      window.parent.document.documentElement.lang =
        language === "en" ? "en" : "zh-CN";
      if (window.frameElement) window.frameElement.title = parentTitle;
    } catch {}
  }
  addSwitcher(language);
})();
