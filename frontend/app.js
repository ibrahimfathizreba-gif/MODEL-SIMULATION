/* ══════════════════════════════════════════════════════════
   app.js — Shared API layer + Chart helpers + KPI updater
   ══════════════════════════════════════════════════════════ */

const API_BASE = 'http://localhost:8000';

/* ── Global state ─────────────────────────────────────────── */
window.SIM = {
  scenario:       'moderate',
  horizon:        20,
  adoptionSpeed:  1.0,
  automationRate: 5,      // display-only %
  data:           null,   // last simulation result
};

/* ── Utility helpers ──────────────────────────────────────── */
const fmt = {
  pct:  (v) => (v == null ? '—' : `${Number(v).toFixed(2)}%`),
  gdp:  (v) => (v == null ? '—' : `$${Number(v).toFixed(2)}T`),
  jobs: (v) => (v == null ? '—' : `${(Number(v)/1e6).toFixed(2)}M`),
  num:  (v, d=2) => (v == null ? '—' : Number(v).toFixed(d)),
};

/* ── API fetch wrapper ────────────────────────────────────── */
async function apiFetch(path, options = {}) {
  const res = await fetch(API_BASE + path, options);
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }
  return res.json();
}

/* ── Loading overlay ─────────────────────────────────────── */
function showLoading(msg = 'Running simulation…') {
  const el = document.getElementById('loading-overlay');
  if (el) {
    el.querySelector('.loading-text').textContent = msg;
    el.classList.add('show');
  }
}
function hideLoading() {
  const el = document.getElementById('loading-overlay');
  if (el) el.classList.remove('show');
}

/* ── Toast notifications ──────────────────────────────────── */
function toast(msg, type = 'info') {
  const icons = { success: '✓', error: '✕', info: 'ℹ' };
  const container = document.getElementById('toast-container');
  if (!container) return;
  const el = document.createElement('div');
  el.className = `toast ${type}`;
  el.innerHTML = `<span>${icons[type]||'ℹ'}</span><span>${msg}</span>`;
  container.appendChild(el);
  setTimeout(() => el.remove(), 4000);
}

/* ── KPI card updater ─────────────────────────────────────── */
function updateKPIs(data) {
  const last = (arr) => arr && arr.length ? arr[arr.length - 1] : null;

  const kpis = {
    'kpi-jobs':     fmt.jobs(last(data.total_jobs)),
    'kpi-unem':     fmt.pct(last(data.unemployment)),
    'kpi-gdp':      fmt.gdp(last(data.gdp)),
    'kpi-ai':       fmt.pct(last(data.ai_adoption)),
    'kpi-accuracy': data.ml_forecast ? fmt.pct(data.ml_forecast.model_accuracy) : '—',
  };

  for (const [id, val] of Object.entries(kpis)) {
    const el = document.getElementById(id);
    if (el) {
      el.textContent = val;
      el.classList.add('fade-in');
    }
  }
}

/* ── ApexCharts default palette ───────────────────────────── */
const COLORS = {
  cyan:   '#00d4ff',
  gold:   '#ffd700',
  green:  '#00e676',
  red:    '#ff4d6a',
  purple: '#a855f7',
  orange: '#ff7c3a',
};

const CHART_DEFAULTS = {
  background: 'transparent',
  foreColor:  '#8fa3bf',
  fontFamily: "'Inter', sans-serif",
  toolbar:    { show: false },
};

function lineChart(id, series, categories, title, yFormatter = (v) => v) {
  const el = document.getElementById(id);
  if (!el) return;
  const options = {
    chart:   { ...CHART_DEFAULTS, type: 'line', height: 260,
               animations: { enabled: true, speed: 600 } },
    series,
    xaxis:   { categories, labels: { style: { colors: '#8fa3bf', fontSize: '11px' } } },
    yaxis:   { labels: { formatter: yFormatter, style: { colors: '#8fa3bf' } } },
    stroke:  { width: 2.5, curve: 'smooth' },
    markers: { size: 0 },
    colors:  [COLORS.cyan, COLORS.gold, COLORS.green, COLORS.red],
    grid:    { borderColor: '#1e2d45', strokeDashArray: 3 },
    tooltip: { theme: 'dark' },
    title:   { text: title, style: { color: '#e8f0fe', fontSize: '13px', fontWeight: 700 } },
    legend:  { labels: { colors: '#8fa3bf' } },
  };
  const chart = new ApexCharts(el, options);
  chart.render();
  return chart;
}

function areaChart(id, series, categories, title) {
  const el = document.getElementById(id);
  if (!el) return;
  const options = {
    chart:   { ...CHART_DEFAULTS, type: 'area', height: 280,
               animations: { enabled: true, speed: 700 } },
    series,
    fill:    { type: 'gradient', gradient: { opacityFrom: 0.35, opacityTo: 0.05 } },
    xaxis:   { categories, labels: { style: { colors: '#8fa3bf', fontSize: '11px' } } },
    yaxis:   { labels: { style: { colors: '#8fa3bf' } } },
    stroke:  { width: 2, curve: 'smooth' },
    colors:  [COLORS.cyan, COLORS.purple, COLORS.gold],
    grid:    { borderColor: '#1e2d45', strokeDashArray: 3 },
    tooltip: { theme: 'dark' },
    title:   { text: title, style: { color: '#e8f0fe', fontSize: '13px', fontWeight: 700 } },
    legend:  { labels: { colors: '#8fa3bf' } },
  };
  const chart = new ApexCharts(el, options);
  chart.render();
  return chart;
}

function barChart(id, series, categories, title) {
  const el = document.getElementById(id);
  if (!el) return;
  const options = {
    chart:    { ...CHART_DEFAULTS, type: 'bar', height: 280,
                animations: { enabled: true, speed: 600 } },
    series,
    plotOptions:{ bar: { borderRadius: 4, columnWidth: '60%' } },
    xaxis:    { categories, labels: { style: { colors: '#8fa3bf', fontSize: '11px' } } },
    yaxis:    { labels: { style: { colors: '#8fa3bf' } } },
    colors:   [COLORS.cyan, COLORS.gold, COLORS.green, COLORS.orange],
    grid:     { borderColor: '#1e2d45', strokeDashArray: 3 },
    tooltip:  { theme: 'dark' },
    title:    { text: title, style: { color: '#e8f0fe', fontSize: '13px', fontWeight: 700 } },
    legend:   { labels: { colors: '#8fa3bf' } },
    dataLabels:{ enabled: false },
  };
  const chart = new ApexCharts(el, options);
  chart.render();
  return chart;
}

function donutChart(id, series, labels, title, colors) {
  const el = document.getElementById(id);
  if (!el) return;
  const options = {
    chart:   { ...CHART_DEFAULTS, type: 'donut', height: 220 },
    series,
    labels,
    colors:  colors || [COLORS.cyan, COLORS.gold, COLORS.green, COLORS.purple, COLORS.orange],
    legend:  { position: 'bottom', labels: { colors: '#8fa3bf' }, fontSize: '11px' },
    tooltip: { theme: 'dark' },
    title:   { text: title, style: { color: '#e8f0fe', fontSize: '13px', fontWeight: 700 } },
    plotOptions: { pie: { donut: { size: '62%',
      labels: { show: true, total: {
        show: true, label: 'Total', color: '#8fa3bf',
        formatter: (w) => {
          const s = w.globals.seriesTotals.reduce((a, b) => a + b, 0);
          return (s / 1e6).toFixed(1) + 'M';
        }
      } } } } },
    dataLabels: { enabled: false },
  };
  const chart = new ApexCharts(el, options);
  chart.render();
  return chart;
}

function rangeAreaChart(id, years, lower, mean, upper, title) {
  const el = document.getElementById(id);
  if (!el) return;
  const options = {
    chart:  { ...CHART_DEFAULTS, type: 'rangeArea', height: 300,
              animations: { enabled: true, speed: 700 } },
    series: [
      { name: '95% CI',  type: 'rangeArea',
        data: years.map((y, i) => ({ x: y, y: [lower[i], upper[i]] })) },
      { name: 'Mean',    type: 'line',
        data: years.map((y, i) => ({ x: y, y: mean[i] })) },
    ],
    fill:   { opacity: [0.18, 1] },
    stroke: { curve: 'smooth', width: [0, 2.5] },
    colors: [COLORS.cyan, COLORS.gold],
    xaxis:  { type: 'numeric', labels: { style: { colors: '#8fa3bf', fontSize: '11px' } } },
    yaxis:  { labels: { style: { colors: '#8fa3bf' } } },
    grid:   { borderColor: '#1e2d45', strokeDashArray: 3 },
    tooltip:{ theme: 'dark' },
    title:  { text: title, style: { color: '#e8f0fe', fontSize: '13px', fontWeight: 700 } },
    legend: { labels: { colors: '#8fa3bf' } },
  };
  const chart = new ApexCharts(el, options);
  chart.render();
  return chart;
}

/* ── Sidebar slider wiring ────────────────────────────────── */
function wireSliders() {
  const sliders = [
    { id: 'slider-ai',         valId: 'val-ai',         key: 'adoptionSpeed',  scale: 1 },
    { id: 'slider-automation', valId: 'val-automation',  key: 'automationRate', scale: 1 },
    { id: 'slider-horizon',    valId: 'val-horizon',     key: 'horizon',        scale: 1 },
  ];
  sliders.forEach(({ id, valId, key, scale }) => {
    const el = document.getElementById(id);
    const vl = document.getElementById(valId);
    if (!el || !vl) return;
    el.addEventListener('input', () => {
      const v = parseFloat(el.value) * scale;
      vl.textContent = key === 'adoptionSpeed'  ? v.toFixed(1) :
                       key === 'automationRate' ? v + '%' : v + 'yr';
      window.SIM[key] = v;
    });
  });

  const scen = document.getElementById('select-scenario');
  if (scen) scen.addEventListener('change', () => { window.SIM.scenario = scen.value; });
}

/* ── Active nav link highlighting ────────────────────────── */
function highlightNav() {
  const page = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-link').forEach((a) => {
    const href = a.getAttribute('href') || '';
    a.classList.toggle('active', href === page || (page === '' && href === 'index.html'));
  });
}

/* ── DOM ready ────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  wireSliders();
  highlightNav();
});
