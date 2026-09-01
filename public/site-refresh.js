(() => {
  "use strict";

  const currentVersion = document.documentElement.dataset.siteVersion;
  if (!currentVersion) return;

  // Keep the current research route readable at first glance. The complete
  // public-note index remains available from its native details control.
  const currentRouteNotes = document.querySelector(
    "article.tree-node.current > details.tree-notes[open]",
  );
  if (currentRouteNotes) currentRouteNotes.open = false;

  let requestInFlight = false;

  async function refreshIfStale() {
    if (requestInFlight || document.visibilityState === "hidden") return;
    requestInFlight = true;
    try {
      const response = await fetch(
        "/site-version.json?check=" + Date.now(),
        { cache: "no-store" },
      );
      if (!response.ok) return;
      const latest = await response.json();
      if (!latest.version || latest.version === currentVersion) return;

      const refreshKey = "research-site-refresh:" + latest.version;
      if (sessionStorage.getItem(refreshKey)) return;
      sessionStorage.setItem(refreshKey, "1");

      const next = new URL(window.location.href);
      next.searchParams.set("site", latest.version);
      window.location.replace(next);
    } catch {
      // Offline viewing remains usable; the next focus event retries.
    } finally {
      requestInFlight = false;
    }
  }

  // Check once as soon as the page is interactive.  Historical cached pages
  // should not sit on a stale release counter for fifteen seconds before the
  // version endpoint is consulted.
  window.setTimeout(refreshIfStale, 0);
  window.setTimeout(refreshIfStale, 15_000);
  window.addEventListener("focus", refreshIfStale);
  document.addEventListener("visibilitychange", refreshIfStale);
})();
