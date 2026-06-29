from pathlib import Path

src = Path("docs/viewers/s3_isometric_battle_viewer_v09n12c3.html")
dst = Path("docs/viewers/s3_isometric_battle_viewer_v09n12d_trace_overlay.html")

if not src.exists():
    raise FileNotFoundError(src)

html = src.read_text(encoding="utf-8", errors="replace")

overlay_css = r'''
<style id="luxllm-trace-overlay-style">
  #luxTracePanel {
    position: fixed;
    top: 78px;
    right: 18px;
    width: 360px;
    max-height: calc(100vh - 110px);
    overflow-y: auto;
    z-index: 9999;
    background: rgba(9, 16, 28, 0.94);
    color: #e8f0ff;
    border: 1px solid rgba(120, 170, 255, 0.42);
    border-radius: 14px;
    box-shadow: 0 18px 45px rgba(0, 0, 0, 0.45);
    padding: 14px 14px 12px 14px;
    font-family: Inter, Segoe UI, Arial, sans-serif;
    font-size: 12px;
    line-height: 1.35;
    backdrop-filter: blur(8px);
  }

  #luxTracePanel.hidden {
    display: none;
  }

  #luxTracePanel .trace-title {
    font-size: 14px;
    font-weight: 800;
    letter-spacing: 0.02em;
    margin-bottom: 4px;
    color: #ffffff;
  }

  #luxTracePanel .trace-subtitle {
    font-size: 11px;
    color: #9fb4d6;
    margin-bottom: 10px;
  }

  #luxTracePanel .trace-row {
    display: grid;
    grid-template-columns: 110px 1fr;
    gap: 8px;
    padding: 5px 0;
    border-top: 1px solid rgba(255, 255, 255, 0.07);
  }

  #luxTracePanel .trace-key {
    color: #8fb2ff;
    font-weight: 700;
  }

  #luxTracePanel .trace-value {
    color: #edf3ff;
    word-break: break-word;
  }

  #luxTracePanel .trace-badges {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin: 8px 0 8px 0;
  }

  #luxTracePanel .trace-badge {
    border-radius: 999px;
    padding: 3px 8px;
    font-size: 11px;
    font-weight: 700;
    background: rgba(120, 170, 255, 0.16);
    color: #cfe0ff;
    border: 1px solid rgba(120, 170, 255, 0.25);
  }

  #luxTracePanel .trace-badge.good {
    background: rgba(70, 190, 130, 0.18);
    color: #bff7d7;
    border-color: rgba(70, 190, 130, 0.35);
  }

  #luxTracePanel .trace-badge.warn {
    background: rgba(255, 190, 80, 0.18);
    color: #ffe0a6;
    border-color: rgba(255, 190, 80, 0.35);
  }

  #luxTracePanel .trace-badge.bad {
    background: rgba(255, 95, 95, 0.18);
    color: #ffc2c2;
    border-color: rgba(255, 95, 95, 0.35);
  }

  #luxTracePanel .trace-section-title {
    margin-top: 10px;
    margin-bottom: 4px;
    color: #ffffff;
    font-weight: 800;
    font-size: 12px;
  }

  #luxTracePanel .trace-intent {
    margin-top: 6px;
    padding: 7px 8px;
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.055);
    border: 1px solid rgba(255, 255, 255, 0.075);
  }

  #luxTracePanel .trace-intent strong {
    color: #ffffff;
  }

  #luxTracePanel .trace-footer {
    margin-top: 10px;
    color: #8d9bb6;
    font-size: 11px;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    padding-top: 8px;
  }

  #luxTraceToggleHint {
    position: fixed;
    right: 22px;
    bottom: 16px;
    z-index: 9998;
    background: rgba(9, 16, 28, 0.82);
    color: #dbe8ff;
    border: 1px solid rgba(120, 170, 255, 0.28);
    border-radius: 999px;
    padding: 7px 11px;
    font-family: Inter, Segoe UI, Arial, sans-serif;
    font-size: 11px;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.35);
  }
</style>
'''

overlay_html = r'''
<div id="luxTracePanel">
  <div class="trace-title">LLM Decision Trace Overlay</div>
  <div class="trace-subtitle">Replay-grounded inspection panel. Press <b>H</b> to hide/show.</div>

  <div class="trace-badges" id="traceBadges"></div>

  <div class="trace-row"><div class="trace-key">Frame / Step</div><div class="trace-value" id="traceStep">Loading...</div></div>
  <div class="trace-row"><div class="trace-key">Phase</div><div class="trace-value" id="tracePhase">-</div></div>
  <div class="trace-row"><div class="trace-key">Source</div><div class="trace-value" id="traceSource">-</div></div>
  <div class="trace-row"><div class="trace-key">LLM Model</div><div class="trace-value" id="traceModel">-</div></div>
  <div class="trace-row"><div class="trace-key">Objective</div><div class="trace-value" id="traceObjective">-</div></div>
  <div class="trace-row"><div class="trace-key">Risk Posture</div><div class="trace-value" id="traceRisk">-</div></div>
  <div class="trace-row"><div class="trace-key">Reason</div><div class="trace-value" id="traceReason">-</div></div>
  <div class="trace-row"><div class="trace-key">Fallback</div><div class="trace-value" id="traceFallback">-</div></div>
  <div class="trace-row"><div class="trace-key">Risk Filter</div><div class="trace-value" id="traceRiskFilter">-</div></div>
  <div class="trace-row"><div class="trace-key">Score</div><div class="trace-value" id="traceScore">-</div></div>
  <div class="trace-row"><div class="trace-key">Summary</div><div class="trace-value" id="traceSummary">-</div></div>

  <div class="trace-section-title">Unit Intents</div>
  <div id="traceIntents"></div>

  <div class="trace-footer">
    Data source: <code>data/run008_decision_trace_overlay.json</code>
  </div>
</div>

<div id="luxTraceToggleHint">H: toggle decision trace overlay</div>
'''

overlay_js = r'''
<script id="luxllm-trace-overlay-script">
(function () {
  const TRACE_URL = "../../data/run008_decision_trace_overlay.json";
  let traceOverlayData = null;
  let traceItems = [];
  let tracePanelVisible = true;

  function byId(id) {
    return document.getElementById(id);
  }

  function text(id, value) {
    const el = byId(id);
    if (!el) return;
    if (value === undefined || value === null || value === "") {
      el.textContent = "-";
    } else {
      el.textContent = String(value);
    }
  }

  function badge(label, cls) {
    return `<span class="trace-badge ${cls || ""}">${escapeHtml(label)}</span>`;
  }

  function escapeHtml(value) {
    return String(value ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  function getCurrentFrameIndex() {
    const candidates = [
      "currentFrameIndex",
      "currentFrame",
      "frameIndex",
      "currentStep",
      "step",
      "t",
    ];

    for (const name of candidates) {
      try {
        if (typeof window[name] === "number" && Number.isFinite(window[name])) {
          return Math.max(0, Math.floor(window[name]));
        }
      } catch (e) {}
    }

    const sliderCandidates = [
      "frameSlider",
      "timelineSlider",
      "stepSlider",
      "replaySlider",
      "turnSlider",
    ];

    for (const id of sliderCandidates) {
      const el = document.getElementById(id);
      if (el && el.value !== undefined) {
        const v = Number(el.value);
        if (Number.isFinite(v)) return Math.max(0, Math.floor(v));
      }
    }

    const range = document.querySelector('input[type="range"]');
    if (range && range.value !== undefined) {
      const v = Number(range.value);
      if (Number.isFinite(v)) return Math.max(0, Math.floor(v));
    }

    return 0;
  }

  function getTraceItem() {
    if (!traceItems.length) return null;

    const idx = getCurrentFrameIndex();
    if (idx >= 0 && idx < traceItems.length) {
      return traceItems[idx];
    }

    return traceItems[Math.min(traceItems.length - 1, Math.max(0, idx))];
  }

  function renderBadges(item) {
    const badges = [];

    if (item.has_exact_llm_decision) {
      badges.push(badge("fresh LLM step", "good"));
    } else if (item.has_recent_llm_decision) {
      badges.push(badge("cached/recent plan", "good"));
    } else {
      badges.push(badge("no LLM plan", "warn"));
    }

    if (item.fallback_used) {
      badges.push(badge("fallback", "warn"));
    }

    if (item.timed_out || item.llm_error) {
      badges.push(badge("LLM issue", "bad"));
    } else {
      badges.push(badge("LLM errors: 0", "good"));
    }

    if (item.risk_filter_changed) {
      badges.push(badge("risk filter changed", "warn"));
    }

    const el = byId("traceBadges");
    if (el) el.innerHTML = badges.join("");
  }

  function renderIntents(item) {
    const el = byId("traceIntents");
    if (!el) return;

    const intents = Array.isArray(item.intents) ? item.intents : [];
    if (!intents.length) {
      el.innerHTML = `<div class="trace-intent">No unit intent recorded for this frame.</div>`;
      return;
    }

    el.innerHTML = intents.map((it) => {
      const target = Array.isArray(it.target) ? `[${it.target.join(", ")}]` : "-";
      return `
        <div class="trace-intent">
          <div><strong>Unit ${escapeHtml(it.unit_id)}</strong>: ${escapeHtml(it.intent || "-")}</div>
          <div>priority=${escapeHtml(it.priority ?? "-")} | risk=${escapeHtml(it.risk || "-")} | target=${escapeHtml(target)}</div>
          <div>${escapeHtml(it.reason || "")}</div>
        </div>
      `;
    }).join("");
  }

  function renderTracePanel() {
    if (!traceItems.length) return;

    const item = getTraceItem();
    if (!item) return;

    const plan = item.global_plan || {};

    renderBadges(item);

    text("traceStep", `${item.frame_index} / ${item.step}`);
    text("tracePhase", item.phase || plan.phase);
    text("traceSource", `${item.decision_source || "-"} (${item.llm_mode || "mode unknown"})`);
    text("traceModel", item.llm_model || "-");
    text("traceObjective", plan.main_objective || "-");
    text("traceRisk", plan.risk_posture || "-");
    text("traceReason", plan.reason || "-");

    const fallbackText = item.fallback_used
      ? `Yes${item.fallback_reason ? ": " + item.fallback_reason : ""}`
      : "No";
    text("traceFallback", fallbackText);

    const riskFilterText = item.risk_filter_enabled
      ? `enabled, changed=${Boolean(item.risk_filter_changed)}, targets=${item.risk_filter_changed_targets ?? 0}`
      : "disabled";
    text("traceRiskFilter", riskFilterText);

    text("traceScore", `P0 ${item.score_player_0 ?? 0} : P1 ${item.score_player_1 ?? 0}`);
    text("traceSummary", item.overlay_summary || "-");

    renderIntents(item);
  }

  async function loadTraceOverlay() {
    try {
      const res = await fetch(TRACE_URL, { cache: "no-store" });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      traceOverlayData = await res.json();
      traceItems = Array.isArray(traceOverlayData.items) ? traceOverlayData.items : [];
      console.log("[LuxLLM Trace Overlay] loaded", {
        frames: traceOverlayData.num_frames,
        traceRows: traceOverlayData.num_trace_rows,
        llmRows: traceOverlayData.num_llm_decision_rows,
        matchedTrace: traceOverlayData.matched_step_trace_frames,
      });
      renderTracePanel();
    } catch (err) {
      console.error("[LuxLLM Trace Overlay] failed to load", err);
      text("traceSummary", "Failed to load data/run008_decision_trace_overlay.json. Start the viewer through python -m http.server from the project root.");
    }
  }

  document.addEventListener("keydown", function (event) {
    if (event.key && event.key.toLowerCase() === "h") {
      tracePanelVisible = !tracePanelVisible;
      const panel = byId("luxTracePanel");
      if (panel) panel.classList.toggle("hidden", !tracePanelVisible);
    }
  });

  window.luxllmRenderTracePanel = renderTracePanel;
  window.luxllmTraceOverlay = {
    reload: loadTraceOverlay,
    render: renderTracePanel,
    getCurrentFrameIndex,
  };

  loadTraceOverlay();
  setInterval(renderTracePanel, 250);
})();
</script>
'''

if "luxllm-trace-overlay-script" in html:
    raise RuntimeError("Trace overlay script already exists in source HTML. Use the original v09n12c3 source.")

# Insert CSS before </head>, or before </body> if no head.
if "</head>" in html:
    html = html.replace("</head>", overlay_css + "\n</head>", 1)
else:
    html = html.replace("</body>", overlay_css + "\n</body>", 1)

# Insert panel and JS before </body>.
if "</body>" in html:
    html = html.replace("</body>", overlay_html + "\n" + overlay_js + "\n</body>", 1)
else:
    html += "\n" + overlay_css + "\n" + overlay_html + "\n" + overlay_js

dst.write_text(html, encoding="utf-8")
print(f"Wrote {dst}")
print("Open this viewer through http://localhost:8000/docs/viewers/s3_isometric_battle_viewer_v09n12d_trace_overlay.html")
