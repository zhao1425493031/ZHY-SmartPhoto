// ---------- 图标 ----------
const ICONS = {
  lock: '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
  sliders: '<line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/><line x1="1" y1="14" x2="7" y2="14"/><line x1="9" y1="8" x2="15" y2="8"/><line x1="17" y1="16" x2="23" y2="16"/>',
  search: '<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>',
  rotate: '<polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/>',
  move: '<polyline points="5 9 2 12 5 15"/><polyline points="9 5 12 2 15 5"/><polyline points="15 19 12 22 9 19"/><polyline points="19 9 22 12 19 15"/><line x1="2" y1="12" x2="22" y2="12"/><line x1="12" y1="2" x2="12" y2="22"/>',
  upload: '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/>',
  download: '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>',
  image: '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/>',
  sun: '<circle cx="12" cy="12" r="4"/><line x1="12" y1="2" x2="12" y2="4"/><line x1="12" y1="20" x2="12" y2="22"/><line x1="4.93" y1="4.93" x2="6.34" y2="6.34"/><line x1="17.66" y1="17.66" x2="19.07" y2="19.07"/><line x1="2" y1="12" x2="4" y2="12"/><line x1="20" y1="12" x2="22" y2="12"/><line x1="4.93" y1="19.07" x2="6.34" y2="17.66"/><line x1="17.66" y1="6.34" x2="19.07" y2="4.93"/>',
  square: '<rect x="3" y="3" width="18" height="18" rx="3"/>',
  user: '<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
  maximize: '<path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"/>',
  alert: '<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>',
  crosshair: '<circle cx="12" cy="12" r="9"/><line x1="22" y1="12" x2="18" y2="12"/><line x1="6" y1="12" x2="2" y2="12"/><line x1="12" y1="6" x2="12" y2="2"/><line x1="12" y1="22" x2="12" y2="18"/>',
  eye: '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>',
  refresh: '<polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>',
  shield: '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
  shieldCheck: '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/>',
  shieldX: '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><line x1="9.5" y1="9.5" x2="14.5" y2="14.5"/><line x1="14.5" y1="9.5" x2="9.5" y2="14.5"/>',
  printer: '<polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/>',
  x: '<line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>',
  check: '<polyline points="20 6 9 17 4 12"/>',
  bang: '<line x1="12" y1="6" x2="12" y2="13"/><line x1="12" y1="18" x2="12.01" y2="18"/>',
  bookmark: '<path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>',
  trash: '<polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4h6v2"/>',
  info: '<circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/>',
  checkCircle: '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>',
  xCircle: '<circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/>',
};

const icon = (name) =>
  `<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${ICONS[name] || ''}</svg>`;

function hydrateIcons(root = document) {
  root.querySelectorAll('[data-icon]:not([data-ready])').forEach((el) => {
    el.insertAdjacentHTML('afterbegin', icon(el.dataset.icon));
    el.dataset.ready = '1';
  });
}

// ---------- 工具 ----------
const $ = (sel, root = document) => root.querySelector(sel);
const clamp = (v, lo, hi) => Math.min(hi, Math.max(lo, v));
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const fmt1 = (v) => (Math.abs(v - Math.round(v)) < 0.05 ? String(Math.round(v)) : v.toFixed(1));
const pct = (v) => +(v * 100).toFixed(2);
const clone = (o) => JSON.parse(JSON.stringify(o));
const store = {
  get(k, d) { try { const v = localStorage.getItem(`smartphoto.${k}`); return v == null ? d : JSON.parse(v); } catch { return d; } },
  set(k, v) { try { localStorage.setItem(`smartphoto.${k}`, JSON.stringify(v)); } catch { /* 隐私模式下忽略 */ } },
};

async function api(path, opts = {}) {
  let res;
  try {
    res = await fetch(path, opts);
  } catch {
    const err = new Error('无法连接到本地服务，请确认 SmartPhoto 仍在运行');
    err.status = 0;
    throw err;
  }
  let data = null;
  try { data = await res.json(); } catch { /* 非 JSON 响应 */ }
  if (!res.ok) {
    let msg = data?.detail;
    if (Array.isArray(msg)) msg = msg.map((d) => String(d.msg || '').replace(/^Value error, /, '')).join('；');
    const err = new Error(msg || `请求失败（${res.status}）`);
    err.status = res.status;
    throw err;
  }
  return data;
}

function toast(message, type = 'info', ms = 3200) {
  const el = document.createElement('div');
  el.className = `toast ${type}`;
  const name = type === 'success' ? 'checkCircle' : type === 'error' ? 'xCircle' : 'info';
  el.innerHTML = `${icon(name)}<span>${esc(message)}</span>`;
  $('#toasts').appendChild(el);
  setTimeout(() => { el.classList.add('out'); setTimeout(() => el.remove(), 220); }, ms);
}

// ---------- 状态 ----------
const state = {
  config: null,
  model: null,
  specKey: null,
  spec: null,
  specModified: false,
  color: '#FFFFFF',
  colorKey: 'white',
  gradient: false,
  zoom: 1,
  offsetX: 0,
  offsetY: 0,
  file: null,
  fileURL: null,
  session: null,
  analysis: null,
  result: null,
  frameSize: null,
  showGuides: true,
};

const el = {
  model: $('#model'),
  specSearch: $('#specSearch'),
  specList: $('#specList'),
  specNote: $('#specNote'),
  swatches: $('#swatches'),
  gradient: $('#gradient'),
  zoom: $('#zoom'), offX: $('#offX'), offY: $('#offY'),
  zoomOut: $('#zoomOut'), offXOut: $('#offXOut'), offYOut: $('#offYOut'),
  formatSeg: $('#formatSeg'),
  kbMin: $('#kbMin'), kbMax: $('#kbMax'),
  stage: $('#stage'),
  emptyView: $('#emptyView'), processingView: $('#processingView'), canvasView: $('#canvasView'),
  procCard: $('.proc-card'), procThumb: $('#procThumb'), procTitle: $('#procTitle'), procSteps: $('#procSteps'),
  procBar: $('#procBar'), procEta: $('#procEta'), procError: $('#procError'), procErrorMsg: $('#procErrorMsg'),
  canvasArea: $('#canvasArea'), frame: $('#frame'), photo: $('#photo'), guides: $('#guides'), original: $('#original'),
  frameHint: $('#frameHint'), frameBusy: $('#frameBusy'), photoMeta: $('#photoMeta'),
  guidesBtn: $('#guidesBtn'), compareBtn: $('#compareBtn'),
  statusCard: $('#statusCard'), statusIcon: $('#statusIcon'), statusTitle: $('#statusTitle'), statusSub: $('#statusSub'),
  checks: $('#checks'), checkBadge: $('#checkBadge'), tipsPanel: $('#tipsPanel'), notices: $('#notices'),
  infoSize: $('#infoSize'), infoMm: $('#infoMm'), infoFile: $('#infoFile'), infoDpi: $('#infoDpi'),
  downloadBtn: $('#downloadBtn'), sheetBtn: $('#sheetBtn'), sheetBtnText: $('#sheetBtnText'),
  sheetPreview: $('#sheetPreview'), sheetThumb: $('#sheetThumb'), sheetCaption: $('#sheetCaption'),
  fileInput: $('#fileInput'),
};

// ---------- 规格 ----------
const mmOf = (s) => s.size_mm || [s.size_px[0] / s.dpi * 25.4, s.size_px[1] / s.dpi * 25.4];
const specDim = (s) => {
  const [mw, mh] = mmOf(s);
  return `${fmt1(mw)}×${fmt1(mh)} mm · ${s.size_px[0]}×${s.size_px[1]} px`;
};
const colorByKey = (key) => state.config.colors.find((c) => c.key === key);

function renderSpecList() {
  const q = el.specSearch.value.trim().toLowerCase().replace(/[×*]/g, 'x');
  const groups = new Map();
  for (const s of state.config.specs) {
    const hay = `${s.name} ${s.size_px[0]}x${s.size_px[1]} ${s.group}`.toLowerCase();
    if (q && !hay.includes(q)) continue;
    const g = s.group || '其他';
    if (!groups.has(g)) groups.set(g, []);
    groups.get(g).push(s);
  }
  if (!groups.size) {
    el.specList.innerHTML = '<div class="spec-empty">没有匹配的规格，可以点击右上角“自定义”新建</div>';
    return;
  }
  let html = '';
  for (const [group, specs] of groups) {
    html += `<div class="spec-group">${esc(group)}</div>`;
    for (const s of specs) {
      const [w, h] = s.size_px;
      const k = Math.min(26 / w, 32 / h);
      const bg = colorByKey(s.background)?.hex || '#fff';
      const active = s.key === state.specKey;
      html += `<button class="spec-item${active ? ' active' : ''}" data-key="${esc(s.key)}" role="option" aria-selected="${active}">
        <span class="spec-thumb"><span style="width:${Math.round(w * k)}px;height:${Math.round(h * k)}px;background:${bg}"></span></span>
        <span class="spec-text"><span class="spec-name">${esc(s.name)}</span><span class="spec-dim">${specDim(s)}</span></span>
        ${s.user ? `<span class="spec-del" data-del="${esc(s.key)}" title="删除" role="button">${icon('trash')}</span>` : ''}
      </button>`;
    }
  }
  el.specList.innerHTML = html;
}

function renderSpecNote() {
  const notes = [];
  if (state.specModified) notes.push('当前使用的是修改过的参数。<a href="#" data-restore>恢复默认</a>');
  if (state.spec?.note) notes.push(esc(state.spec.note));
  el.specNote.hidden = !notes.length;
  el.specNote.innerHTML = notes.join('<br>');
}

function selectSpec(key, { keepColor = false } = {}) {
  const preset = state.config.specs.find((s) => s.key === key);
  if (!preset) return;
  state.specKey = key;
  state.spec = clone(preset);
  state.specModified = false;
  store.set('spec', key);
  if (!keepColor) {
    const c = colorByKey(preset.background);
    if (c) setColor(c.hex, c.key, { silent: true });
  }
  syncFileFields();
  renderSpecList();
  renderSpecNote();
  if (state.session) {
    fitFrame(state.spec.size_px);
    scheduleRender();
  }
}

function syncFileFields() {
  el.formatSeg.querySelectorAll('button').forEach((b) => {
    const on = b.dataset.value === state.spec.format;
    b.classList.toggle('active', on);
    b.setAttribute('aria-checked', on);
  });
  const [lo, hi] = state.spec.kb_range || [0, 0];
  el.kbMin.value = lo || '';
  el.kbMax.value = hi || '';
  el.kbMin.classList.remove('invalid');
  el.kbMax.classList.remove('invalid');
}

// ---------- 颜色 ----------
function isLight(hex) {
  const n = parseInt(hex.slice(1), 16);
  const [r, g, b] = [(n >> 16) & 255, (n >> 8) & 255, n & 255];
  return (0.299 * r + 0.587 * g + 0.114 * b) / 255 > 0.72;
}

function renderSwatches() {
  const presets = state.config.colors.map((c) => `
    <button class="swatch${isLight(c.hex) ? ' light' : ''}" data-key="${esc(c.key)}" data-hex="${c.hex}" style="--c:${c.hex}" title="${esc(c.name)} ${c.hex}">
      <span class="swatch-dot">${icon('check')}</span><span>${esc(c.name)}</span>
    </button>`).join('');
  el.swatches.innerHTML = `${presets}
    <label class="swatch swatch-custom" title="自定义颜色">
      <span class="swatch-dot">${icon('check')}</span><span>自定义</span>
      <input type="color" id="customColor" value="#4a90e2" aria-label="自定义颜色">
    </label>`;
  $('#customColor').addEventListener('input', (e) => setColor(e.target.value.toUpperCase(), 'custom'));
}

function setColor(hex, key, { silent = false } = {}) {
  state.color = hex;
  state.colorKey = key;
  store.set('color', { hex, key });
  el.swatches.querySelectorAll('.swatch').forEach((s) => {
    const custom = s.classList.contains('swatch-custom');
    const on = custom ? key === 'custom' : s.dataset.key === key;
    s.classList.toggle('active', on);
    if (custom) {
      s.style.setProperty('--c', hex);
      s.classList.toggle('light', on && isLight(hex));
    }
  });
  if (!silent) scheduleRender();
}

// ---------- 构图 ----------
function fillSlider(input) {
  const p = ((input.value - input.min) / (input.max - input.min)) * 100;
  input.style.setProperty('--pct', `${p}%`);
}

function syncSliders() {
  el.zoom.value = (state.zoom * 100).toFixed(1);
  el.offX.value = (state.offsetX * 100).toFixed(1);
  el.offY.value = (state.offsetY * 100).toFixed(1);
  el.zoomOut.textContent = `${Math.round(state.zoom * 100)}%`;
  const signed = (v) => (Math.abs(v) < 0.05 ? '0' : `${v > 0 ? '+' : ''}${v.toFixed(1)}`);
  el.offXOut.textContent = signed(state.offsetX * 100);
  el.offYOut.textContent = signed(state.offsetY * 100);
  [el.zoom, el.offX, el.offY].forEach(fillSlider);
}

function resetAdjust({ silent = false } = {}) {
  state.zoom = 1;
  state.offsetX = 0;
  state.offsetY = 0;
  syncSliders();
  if (!silent) scheduleRender();
}

// ---------- 视图 ----------
function showView(name) {
  el.emptyView.hidden = name !== 'empty';
  el.processingView.hidden = name !== 'processing';
  el.canvasView.hidden = name !== 'canvas';
}

function fitFrame(size) {
  if (!size || el.canvasView.hidden) return;
  state.frameSize = size;
  const [w, h] = size;
  const availW = el.canvasArea.clientWidth;
  const availH = el.canvasArea.clientHeight - 36;
  if (availW <= 0 || availH <= 0) return;
  let fh = Math.min(availH, 820);
  let fw = (fh * w) / h;
  if (fw > availW) { fw = availW; fh = (fw * h) / w; }
  el.frame.style.width = `${Math.round(fw)}px`;
  el.frame.style.height = `${Math.round(fh)}px`;
  if (state.result) drawGuides(state.result);
}

// ---------- 上传与分析 ----------
const STAGES = [
  ['load', '读取照片'],
  ['face', '检测人脸与头部姿态'],
  ['matting', '智能抠图'],
  ['refine', '边缘精修'],
];
let pollToken = 0;

function isImageFile(file) {
  return file && (file.type.startsWith('image/') || /\.(heic|heif)$/i.test(file.name));
}

async function handleFile(file) {
  if (!file) return;
  if (!isImageFile(file)) { toast('请选择图片文件', 'error'); return; }
  if (file.size > 30 * 1024 * 1024) { toast('图片超过 30MB，请压缩后再上传', 'error'); return; }

  state.file = file;
  if (state.fileURL) URL.revokeObjectURL(state.fileURL);
  state.fileURL = URL.createObjectURL(file);
  state.session = null;
  state.result = null;
  state.analysis = null;
  resetAdjust({ silent: true });
  renderIdleInspector();

  showView('processing');
  el.procCard.hidden = false;
  el.procError.hidden = true;
  el.procThumb.hidden = false;
  el.procThumb.src = state.fileURL;
  el.procThumb.onerror = () => { el.procThumb.hidden = true; };
  el.procTitle.textContent = '正在处理照片';
  updateProcessing('queue', 0, null);

  const token = ++pollToken;
  const fd = new FormData();
  fd.append('file', file);
  fd.append('model', state.model);
  try {
    const { job_id: jobId, eta } = await api('/api/jobs', { method: 'POST', body: fd });
    pollJob(jobId, eta, token);
  } catch (e) {
    showProcessingError(e.message);
  }
}

function updateProcessing(stage, progress, remaining) {
  const idx = stage === 'done' ? STAGES.length : Math.max(0, STAGES.findIndex(([k]) => k === stage));
  el.procSteps.innerHTML = STAGES.map(([, label], i) => {
    const cls = i < idx ? 'done' : i === idx ? 'active' : '';
    return `<li class="${cls}"><span class="dot">${i < idx ? icon('check') : ''}</span>${label}</li>`;
  }).join('');
  el.procBar.style.width = `${Math.round(clamp(progress, 0, 1) * 100)}%`;
  if (stage === 'queue') el.procEta.textContent = '正在准备…';
  else if (remaining == null) el.procEta.textContent = '正在处理…';
  else el.procEta.textContent = remaining > 1.5 ? `预计还需约 ${Math.ceil(remaining)} 秒` : '即将完成…';
}

function pollJob(jobId, eta, token) {
  let mattingStart = null;
  const tick = async () => {
    if (token !== pollToken) return;
    let job;
    try {
      job = await api(`/api/jobs/${jobId}`);
    } catch (e) {
      showProcessingError(e.message);
      return;
    }
    if (token !== pollToken) return;
    if (job.status === 'error') { showProcessingError(job.error); return; }
    if (job.status === 'done') { onAnalyzed(job.result); return; }

    let progress = job.progress;
    let remaining = null;
    if (job.stage === 'matting') {
      mattingStart ??= performance.now();
      const t = (performance.now() - mattingStart) / 1000;
      progress = 0.3 + 0.55 * (1 - Math.exp(-t / Math.max(eta * 0.55, 0.5)));
      remaining = Math.max(0, eta - t);
    }
    updateProcessing(job.stage, progress, remaining);
    setTimeout(tick, 350);
  };
  tick();
}

function showProcessingError(message) {
  showView('processing');
  el.procCard.hidden = true;
  el.procError.hidden = false;
  el.procErrorMsg.textContent = message || '未知错误';
}

function onAnalyzed(result) {
  state.session = result.session_id;
  state.analysis = result;
  showView('canvas');
  el.frameHint.classList.remove('gone');
  requestAnimationFrame(() => {
    fitFrame(state.spec.size_px);
    scheduleRender();
  });
  toast(`照片分析完成，用时 ${result.elapsed} 秒`, 'success');
}

// ---------- 渲染 ----------
let inflight = false;
let pending = false;
let busyTimer = null;
let idleWaiters = [];

function specPayload() {
  const s = state.spec;
  return {
    key: s.key, name: s.name, size_px: s.size_px, size_mm: s.size_mm, dpi: s.dpi,
    head_height_ratio: s.head_height_ratio, top_margin_ratio: s.top_margin_ratio,
    eye_from_bottom_ratio: s.eye_from_bottom_ratio, background: s.background,
    format: s.format, kb_range: s.kb_range, note: s.note || '',
  };
}

function scheduleRender() {
  if (!state.session) return;
  if (inflight) { pending = true; return; }
  doRender();
}

function whenIdle() {
  if (!inflight && !pending) return Promise.resolve();
  return new Promise((resolve) => idleWaiters.push(resolve));
}

async function doRender() {
  inflight = true;
  pending = false;
  clearTimeout(busyTimer);
  busyTimer = setTimeout(() => el.frameBusy.classList.add('on'), 180);
  const body = {
    session_id: state.session,
    spec: specPayload(),
    color: state.color,
    gradient: state.gradient,
    zoom: state.zoom,
    offset_x: state.offsetX,
    offset_y: state.offsetY,
  };
  try {
    const r = await api('/api/render', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (body.session_id === state.session) applyResult(r);
  } catch (e) {
    if (e.status === 410 && state.file) {
      toast('照片会话已过期，正在重新分析…');
      handleFile(state.file);
    } else {
      toast(e.message, 'error', 4500);
    }
  } finally {
    inflight = false;
    clearTimeout(busyTimer);
    el.frameBusy.classList.remove('on');
    if (pending) doRender();
    else { idleWaiters.forEach((f) => f()); idleWaiters = []; }
  }
}

function applyResult(r) {
  state.result = r;
  const [w, h] = r.size;
  if (!state.frameSize || state.frameSize[0] !== w || state.frameSize[1] !== h) fitFrame(r.size);
  el.photo.src = r.image;
  drawGuides(r);
  const nFail = r.checks.filter((c) => c.status === 'fail').length;
  el.photoMeta.innerHTML = `<span class="meta-status ${r.ok ? 'ok' : 'fail'}">${r.ok ? '符合规格' : `${nFail} 项不合格`}</span><span>${w} × ${h} px</span><span>${fmt1(r.size_mm[0])} × ${fmt1(r.size_mm[1])} mm</span><span>${r.kb} KB</span>`;
  renderInspector(r);
  scheduleSheet();
}

function drawGuides(r) {
  const L = r.layout;
  const R = r.ranges;
  const W = L.width;
  const H = L.height;
  const status = Object.fromEntries(r.checks.map((c) => [c.key, c.status]));
  const unit = H / (el.frame.clientHeight || H);
  const fs = 11 * unit;
  const nse = 'vector-effect="non-scaling-stroke"';
  let svg = '';

  const hline = (cls, y) => `<line class="${cls}" x1="0" y1="${y}" x2="${W}" y2="${y}" ${nse}/>`;
  const band = (y0, y1) => {
    svg += `<rect class="g-band" x="0" y="${y0}" width="${W}" height="${Math.max(0, y1 - y0)}"/>`;
    svg += hline('g-edge', y0) + hline('g-edge', y1);
  };
  if (R.top) band(R.top[0] * H, R.top[1] * H);
  if (R.eye) band((1 - R.eye[1]) * H, (1 - R.eye[0]) * H);
  band(L.head_top + R.head[0] * H, L.head_top + R.head[1] * H);
  svg += `<line class="g-center" x1="${W / 2}" y1="0" x2="${W / 2}" y2="${H}" ${nse}/>`;

  const marker = (y, label, ok) => {
    const cls = ok ? 'ok' : 'bad';
    const tw = fs * label.length + 12 * unit;
    const th = fs + 8 * unit;
    const ty = clamp(y - th - 3 * unit, 0, H - th);
    const tx = W - tw - 6 * unit;
    svg += hline(`g-line ${cls}`, y);
    svg += `<g class="g-tag ${cls}"><rect x="${tx}" y="${ty}" width="${tw}" height="${th}" rx="${4 * unit}"/>`;
    svg += `<text x="${tx + tw / 2}" y="${ty + th / 2}" font-size="${fs}" text-anchor="middle" dominant-baseline="central">${label}</text></g>`;
  };
  marker(L.head_top, '头顶', status.top ? status.top === 'pass' : L.head_top >= 0);
  marker(L.chin, '下巴', status.head === 'pass');
  if (R.eye) marker(L.eye_y, '眼睛', status.eye === 'pass');

  el.guides.setAttribute('viewBox', `0 0 ${W} ${H}`);
  el.guides.innerHTML = svg;
}

// ---------- 右侧面板 ----------
function setStatus(kind, iconName, title, sub) {
  el.statusCard.className = `status-card ${kind}`;
  el.statusIcon.innerHTML = icon(iconName);
  el.statusTitle.textContent = title;
  el.statusSub.textContent = sub;
}

function renderIdleInspector() {
  setStatus('idle', 'shield', '等待照片', '上传后会按所选规格逐项校验');
  el.checkBadge.hidden = true;
  el.checks.innerHTML = '<li class="checks-empty">暂无数据</li>';
  el.tipsPanel.hidden = true;
  for (const k of ['infoSize', 'infoMm', 'infoFile', 'infoDpi']) el[k].textContent = '—';
  el.downloadBtn.disabled = true;
  el.sheetBtn.disabled = true;
  el.sheetBtnText.textContent = '下载六寸排版';
  el.sheetPreview.hidden = true;
}

function renderInspector(r) {
  const fails = r.checks.filter((c) => c.status === 'fail');
  const passed = r.checks.filter((c) => c.status === 'pass').length;
  if (r.ok) setStatus('ok', 'shieldCheck', '符合规格，可以上传', `${state.spec.name} · ${r.kb} KB`);
  else setStatus('fail', 'shieldX', `${fails.length} 项不符合要求`, `请调整：${fails.map((c) => c.name).join('、')}`);

  el.checkBadge.hidden = false;
  el.checkBadge.className = `badge ${r.ok ? 'ok' : 'fail'}`;
  el.checkBadge.textContent = `${passed} / ${r.checks.length} 通过`;

  const iconFor = { pass: 'check', fail: 'x', warn: 'bang' };
  el.checks.innerHTML = r.checks.map((c) => `
    <li>
      <span class="check-icon ${c.status}">${icon(iconFor[c.status])}</span>
      <div class="check-main">
        <div class="check-row"><span class="check-name">${esc(c.name)}</span><span class="check-value ${c.status}">${esc(c.value)}</span></div>
        ${c.requirement ? `<div class="check-req">要求 ${esc(c.requirement)}</div>` : ''}
      </div>
    </li>`).join('');

  const notices = [];
  const a = state.analysis;
  if (a && Math.abs(a.roll) >= 0.5) notices.push(['info', `已自动校正头部倾斜 ${Math.abs(a.roll).toFixed(1)}°`]);
  for (const w of new Set([...(a?.warnings || []), ...r.warnings])) notices.push(['warn', w]);
  el.tipsPanel.hidden = !notices.length;
  el.notices.innerHTML = notices.map(([kind, text]) =>
    `<li class="${kind}">${icon(kind === 'info' ? 'info' : 'alert')}<span>${esc(text)}</span></li>`).join('');

  const [w, h] = r.size;
  el.infoSize.textContent = `${w} × ${h} px`;
  el.infoMm.textContent = `${fmt1(r.size_mm[0])} × ${fmt1(r.size_mm[1])} mm`;
  el.infoFile.textContent = `${r.ext.toUpperCase()} · ${r.kb} KB`;
  el.infoFile.title = r.quality ? `JPEG 质量 ${r.quality}` : '';
  el.infoDpi.textContent = `${r.dpi} DPI`;
  el.downloadBtn.disabled = false;
  el.sheetBtn.disabled = r.sheet_count === 0;
  el.sheetBtnText.textContent = r.sheet_count ? `下载六寸排版（${r.sheet_count} 张）` : '尺寸过大，无法排版';
}

let sheetTimer = null;
function scheduleSheet() {
  clearTimeout(sheetTimer);
  sheetTimer = setTimeout(() => {
    const r = state.result;
    if (!r || !state.session || !r.sheet_count) { el.sheetPreview.hidden = true; return; }
    el.sheetThumb.src = `/api/sessions/${state.session}/sheet?rid=${r.render_id}`;
    el.sheetCaption.textContent = `六寸相纸 · ${r.sheet_count} 张 · 点击查看大图`;
    el.sheetPreview.hidden = false;
  }, 450);
}

function triggerDownload(url) {
  const a = document.createElement('a');
  a.href = url;
  a.download = '';
  document.body.appendChild(a);
  a.click();
  a.remove();
}

async function downloadPhoto() {
  await whenIdle();
  const r = state.result;
  if (!r) return;
  if (!r.ok) {
    const n = r.checks.filter((c) => c.status === 'fail').length;
    const go = await confirmDialog(`有 ${n} 项不符合规格`, '这样上传可能会被审核退回。确定仍要下载吗？', '仍要下载');
    if (!go) return;
  }
  triggerDownload(`/api/sessions/${state.session}/photo`);
  toast('已开始下载，文件同时保存在 outputs 文件夹', 'success');
}

async function downloadSheet() {
  await whenIdle();
  if (!state.result) return;
  triggerDownload(`/api/sessions/${state.session}/sheet?download=1`);
  toast('已开始下载排版图', 'success');
}

// ---------- 弹窗 ----------
function openModal(m) {
  m.hidden = false;
  hydrateIcons(m);
  setTimeout(() => m.querySelector('input, button:not([data-close])')?.focus(), 30);
}
function closeModal(m) { m.hidden = true; m.dispatchEvent(new Event('close')); }

function confirmDialog(title, message, okText = '确定') {
  const m = $('#confirmModal');
  $('#confirmTitle').textContent = title;
  $('#confirmMsg').textContent = message;
  const ok = $('#confirmOk');
  ok.textContent = okText;
  openModal(m);
  return new Promise((resolve) => {
    const done = (v) => {
      ok.removeEventListener('click', onOk);
      m.removeEventListener('close', onClose);
      if (!m.hidden) m.hidden = true;
      resolve(v);
    };
    const onOk = () => done(true);
    const onClose = () => done(false);
    ok.addEventListener('click', onOk);
    m.addEventListener('close', onClose);
  });
}

// 自定义规格
const specForm = $('#specForm');
let posMode = 'top';

function setPosMode(mode) {
  posMode = mode;
  $('#posSeg').querySelectorAll('button').forEach((b) => b.classList.toggle('active', b.dataset.value === mode));
  $('#posHelp').textContent = mode === 'top'
    ? '头顶（含头发）到照片上边缘的距离，占照片高度的比例'
    : '眼睛到照片下边缘的距离，占照片高度的比例（签证类常用）';
}

function updateMmPreview() {
  const w = +specForm.w.value; const h = +specForm.h.value; const dpi = +specForm.dpi.value;
  $('#mmPreview').textContent = w && h && dpi ? `${(w / dpi * 25.4).toFixed(1)} × ${(h / dpi * 25.4).toFixed(1)} mm` : '—';
}

function openSpecModal() {
  const s = state.spec;
  const f = specForm;
  f.specName.value = s.name;
  f.w.value = s.size_px[0];
  f.h.value = s.size_px[1];
  f.dpi.value = s.dpi;
  f.headMin.value = pct(s.head_height_ratio[0]);
  f.headMax.value = pct(s.head_height_ratio[1]);
  const usesEye = !s.top_margin_ratio && s.eye_from_bottom_ratio;
  setPosMode(usesEye ? 'eye' : 'top');
  const pos = (usesEye ? s.eye_from_bottom_ratio : s.top_margin_ratio) || [0.07, 0.11];
  f.posMin.value = pct(pos[0]);
  f.posMax.value = pct(pos[1]);
  $('#bgSelect').innerHTML = state.config.colors.map((c) => `<option value="${esc(c.key)}">${esc(c.name)}</option>`).join('');
  f.background.value = s.background;
  f.format.value = s.format;
  const [lo, hi] = s.kb_range || [0, 0];
  f.kbMin.value = lo || '';
  f.kbMax.value = hi || '';
  f.note.value = s.note || '';
  f.querySelectorAll('.invalid').forEach((i) => i.classList.remove('invalid'));
  $('#specFormError').hidden = true;
  $('#saveSpecBtn').innerHTML = `${icon('bookmark')}${s.user ? '更新我的规格' : '保存为我的规格'}`;
  updateMmPreview();
  openModal($('#specModal'));
}

function readSpecForm() {
  const f = specForm;
  const errors = [];
  f.querySelectorAll('.invalid').forEach((i) => i.classList.remove('invalid'));
  const num = (name) => { const v = f[name].value.trim(); return v === '' ? null : Number(v); };
  const bad = (names, msg) => { names.forEach((n) => f[n].classList.add('invalid')); errors.push(msg); };

  const name = f.specName.value.trim();
  if (!name) bad(['specName'], '请填写规格名称');
  const w = num('w'); const h = num('h'); const dpi = num('dpi');
  if (!Number.isInteger(w) || w < 50 || w > 4000) bad(['w'], '宽度需为 50～4000 的整数');
  if (!Number.isInteger(h) || h < 50 || h > 4000) bad(['h'], '高度需为 50～4000 的整数');
  if (!Number.isInteger(dpi) || dpi < 72 || dpi > 1200) bad(['dpi'], '分辨率需为 72～1200');
  const hMin = num('headMin'); const hMax = num('headMax');
  if (hMin == null || hMax == null || hMin <= 0 || hMax >= 100 || hMin > hMax) bad(['headMin', 'headMax'], '头部比例范围填写有误');
  const pMin = num('posMin'); const pMax = num('posMax');
  if (pMin == null || pMax == null || pMin < 0 || pMax >= 100 || pMin > pMax) bad(['posMin', 'posMax'], '纵向定位范围填写有误');
  const kMin = num('kbMin') || 0; const kMax = num('kbMax') || 0;
  if (kMin < 0 || kMax < 0 || (kMax && kMin > kMax)) bad(['kbMin', 'kbMax'], '文件大小范围填写有误');

  if (errors.length) {
    const box = $('#specFormError');
    box.textContent = errors.join('；');
    box.hidden = false;
    return null;
  }
  const s = state.spec;
  const sameSize = s.size_px[0] === w && s.size_px[1] === h && s.dpi === dpi;
  const pos = [pMin / 100, pMax / 100];
  return {
    ...s,
    name,
    size_px: [w, h],
    size_mm: sameSize ? s.size_mm : null,
    dpi,
    head_height_ratio: [hMin / 100, hMax / 100],
    top_margin_ratio: posMode === 'top' ? pos : null,
    eye_from_bottom_ratio: posMode === 'eye' ? pos : null,
    background: f.background.value,
    format: f.format.value,
    kb_range: kMin || kMax ? [kMin, kMax] : null,
    note: f.note.value.trim(),
  };
}

function applySpecForm() {
  const spec = readSpecForm();
  if (!spec) return;
  const bgChanged = spec.background !== state.spec.background;
  state.spec = spec;
  state.specModified = true;
  if (bgChanged) {
    const c = colorByKey(spec.background);
    if (c) setColor(c.hex, c.key, { silent: true });
  }
  syncFileFields();
  renderSpecNote();
  closeModal($('#specModal'));
  if (state.session) { fitFrame(spec.size_px); scheduleRender(); }
  toast('已应用自定义参数', 'success');
}

async function saveSpecForm() {
  const spec = readSpecForm();
  if (!spec) return;
  const payload = { ...specPayload(), ...spec, key: state.spec.user ? state.spec.key : 'custom' };
  delete payload.user;
  delete payload.group;
  try {
    const res = await api('/api/specs', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    state.config.specs = res.specs;
    closeModal($('#specModal'));
    el.specSearch.value = '';
    selectSpec(res.key);
    toast(`已保存到“我的规格”：${spec.name}`, 'success');
  } catch (e) {
    const box = $('#specFormError');
    box.textContent = e.message;
    box.hidden = false;
  }
}

async function deleteSpec(key) {
  const s = state.config.specs.find((x) => x.key === key);
  if (!s) return;
  const go = await confirmDialog('删除这个规格？', `“${s.name}”将从“我的规格”中移除，此操作无法撤销。`, '删除');
  if (!go) return;
  try {
    const res = await api(`/api/specs/${encodeURIComponent(key)}`, { method: 'DELETE' });
    state.config.specs = res.specs;
    if (state.specKey === key) {
      state.specKey = null;
      state.spec = { ...state.spec, key: 'custom', user: false };
    }
    renderSpecList();
    toast('已删除', 'success');
  } catch (e) {
    toast(e.message, 'error');
  }
}

// ---------- 事件 ----------
function bindEvents() {
  // 模型
  el.model.addEventListener('change', () => {
    state.model = el.model.value;
    store.set('model', state.model);
    if (state.file) {
      toast('正在用新的抠图引擎重新处理…');
      handleFile(state.file);
    }
  });

  // 规格
  el.specSearch.addEventListener('input', renderSpecList);
  el.specList.addEventListener('click', (e) => {
    const del = e.target.closest('[data-del]');
    if (del) { e.stopPropagation(); deleteSpec(del.dataset.del); return; }
    const item = e.target.closest('.spec-item');
    if (item) selectSpec(item.dataset.key);
  });
  el.specNote.addEventListener('click', (e) => {
    if (e.target.matches('[data-restore]')) {
      e.preventDefault();
      if (state.specKey) selectSpec(state.specKey);
    }
  });
  $('#editSpecBtn').addEventListener('click', openSpecModal);

  // 颜色
  el.swatches.addEventListener('click', (e) => {
    const sw = e.target.closest('.swatch:not(.swatch-custom)');
    if (sw) setColor(sw.dataset.hex, sw.dataset.key);
  });
  el.gradient.addEventListener('change', () => { state.gradient = el.gradient.checked; scheduleRender(); });

  // 构图
  el.zoom.addEventListener('input', () => { state.zoom = el.zoom.value / 100; syncSliders(); scheduleRender(); });
  el.offX.addEventListener('input', () => { state.offsetX = el.offX.value / 100; syncSliders(); scheduleRender(); });
  el.offY.addEventListener('input', () => { state.offsetY = el.offY.value / 100; syncSliders(); scheduleRender(); });
  $('#resetAdjustBtn').addEventListener('click', () => resetAdjust());

  // 文件要求
  el.formatSeg.addEventListener('click', (e) => {
    const b = e.target.closest('button');
    if (!b) return;
    state.spec.format = b.dataset.value;
    syncFileFields();
    scheduleRender();
  });
  const onKb = () => {
    const lo = Number(el.kbMin.value) || 0;
    const hi = Number(el.kbMax.value) || 0;
    const invalid = lo < 0 || hi < 0 || (hi && lo > hi);
    el.kbMin.classList.toggle('invalid', invalid);
    el.kbMax.classList.toggle('invalid', invalid);
    if (invalid) { toast('文件大小范围填写有误：最小值不能大于最大值', 'error'); return; }
    state.spec.kb_range = lo || hi ? [lo, hi] : null;
    scheduleRender();
  };
  el.kbMin.addEventListener('change', onKb);
  el.kbMax.addEventListener('change', onKb);

  // 上传
  const pick = () => el.fileInput.click();
  $('#pickBtn').addEventListener('click', (e) => { e.stopPropagation(); pick(); });
  $('#dropzone').addEventListener('click', pick);
  $('#dropzone').addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); pick(); } });
  $('#retryBtn').addEventListener('click', pick);
  $('#replaceBtn').addEventListener('click', pick);
  el.fileInput.addEventListener('change', () => {
    const file = el.fileInput.files[0];
    el.fileInput.value = '';
    handleFile(file);
  });

  let dragDepth = 0;
  const hasFiles = (e) => [...(e.dataTransfer?.types || [])].includes('Files');
  window.addEventListener('dragenter', (e) => { if (!hasFiles(e)) return; e.preventDefault(); dragDepth++; el.stage.classList.add('dragging'); });
  window.addEventListener('dragover', (e) => { if (hasFiles(e)) e.preventDefault(); });
  window.addEventListener('dragleave', () => { dragDepth = Math.max(0, dragDepth - 1); if (!dragDepth) el.stage.classList.remove('dragging'); });
  window.addEventListener('drop', (e) => {
    if (!hasFiles(e)) return;
    e.preventDefault();
    dragDepth = 0;
    el.stage.classList.remove('dragging');
    handleFile(e.dataTransfer.files[0]);
  });
  window.addEventListener('paste', (e) => {
    if (e.target.closest?.('input, textarea')) return;
    const item = [...(e.clipboardData?.items || [])].find((i) => i.type.startsWith('image/'));
    if (item) handleFile(item.getAsFile());
  });

  // 画布交互
  let drag = null;
  const hideHint = () => el.frameHint.classList.add('gone');
  el.frame.addEventListener('pointerdown', (e) => {
    if (!state.session || e.button !== 0) return;
    el.frame.setPointerCapture(e.pointerId);
    drag = { x: e.clientX, y: e.clientY, ox: state.offsetX, oy: state.offsetY };
    el.frame.classList.add('grabbing');
    hideHint();
  });
  el.frame.addEventListener('pointermove', (e) => {
    if (!drag) return;
    const rect = el.frame.getBoundingClientRect();
    state.offsetX = clamp(drag.ox + (e.clientX - drag.x) / rect.width, -0.25, 0.25);
    state.offsetY = clamp(drag.oy + (e.clientY - drag.y) / rect.height, -0.25, 0.25);
    syncSliders();
    scheduleRender();
  });
  const endDrag = () => { drag = null; el.frame.classList.remove('grabbing'); };
  el.frame.addEventListener('pointerup', endDrag);
  el.frame.addEventListener('pointercancel', endDrag);
  el.frame.addEventListener('wheel', (e) => {
    if (!state.session) return;
    e.preventDefault();
    state.zoom = clamp(state.zoom * Math.exp(-e.deltaY * 0.0012), 0.7, 1.3);
    syncSliders();
    scheduleRender();
    hideHint();
  }, { passive: false });
  el.frame.addEventListener('keydown', (e) => {
    if (!state.session) return;
    const step = e.shiftKey ? 0.02 : 0.004;
    const moves = { ArrowLeft: [-step, 0], ArrowRight: [step, 0], ArrowUp: [0, -step], ArrowDown: [0, step] };
    if (moves[e.key]) {
      state.offsetX = clamp(state.offsetX + moves[e.key][0], -0.25, 0.25);
      state.offsetY = clamp(state.offsetY + moves[e.key][1], -0.25, 0.25);
    } else if (e.key === '+' || e.key === '=') {
      state.zoom = clamp(state.zoom + 0.01, 0.7, 1.3);
    } else if (e.key === '-') {
      state.zoom = clamp(state.zoom - 0.01, 0.7, 1.3);
    } else if (e.key === '0') {
      resetAdjust();
      return;
    } else {
      return;
    }
    e.preventDefault();
    syncSliders();
    scheduleRender();
    hideHint();
  });

  // 工具栏
  el.guidesBtn.addEventListener('click', () => {
    state.showGuides = !state.showGuides;
    el.guidesBtn.setAttribute('aria-pressed', state.showGuides);
    el.guides.classList.toggle('off', !state.showGuides);
    store.set('guides', state.showGuides);
  });
  const showOriginal = (on) => {
    if (on && state.fileURL) el.original.src = state.fileURL;
    el.original.hidden = !on;
    el.compareBtn.setAttribute('aria-pressed', on);
  };
  el.compareBtn.addEventListener('pointerdown', () => showOriginal(true));
  ['pointerup', 'pointerleave', 'pointercancel'].forEach((t) => el.compareBtn.addEventListener(t, () => showOriginal(false)));

  new ResizeObserver(() => fitFrame(state.frameSize || state.spec?.size_px)).observe(el.canvasArea);

  // 导出
  el.downloadBtn.addEventListener('click', downloadPhoto);
  el.sheetBtn.addEventListener('click', downloadSheet);
  el.sheetPreview.addEventListener('click', () => {
    $('#sheetLarge').src = el.sheetThumb.src;
    $('#sheetModalTitle').textContent = `六寸相纸排版 · ${state.result?.sheet_count ?? ''} 张`;
    openModal($('#sheetModal'));
  });
  $('#sheetModalDownload').addEventListener('click', () => { closeModal($('#sheetModal')); downloadSheet(); });

  // 弹窗
  document.querySelectorAll('.modal').forEach((m) => {
    m.addEventListener('click', (e) => { if (e.target.closest('[data-close]')) closeModal(m); });
  });
  document.addEventListener('keydown', (e) => {
    if (e.key !== 'Escape') return;
    const open = [...document.querySelectorAll('.modal')].filter((m) => !m.hidden).pop();
    if (open) closeModal(open);
  });
  $('#posSeg').addEventListener('click', (e) => {
    const b = e.target.closest('button');
    if (!b || b.dataset.value === posMode) return;
    setPosMode(b.dataset.value);
    const s = state.spec;
    const pos = (posMode === 'eye' ? s.eye_from_bottom_ratio || [0.56, 0.69] : s.top_margin_ratio || [0.07, 0.11]);
    specForm.posMin.value = pct(pos[0]);
    specForm.posMax.value = pct(pos[1]);
  });
  ['w', 'h', 'dpi'].forEach((n) => specForm[n].addEventListener('input', updateMmPreview));
  specForm.addEventListener('submit', (e) => { e.preventDefault(); applySpecForm(); });
  $('#applySpecBtn').addEventListener('click', applySpecForm);
  $('#saveSpecBtn').addEventListener('click', saveSpecForm);
}

// ---------- 启动 ----------
async function init() {
  hydrateIcons();
  try {
    state.config = await api('/api/config');
  } catch (e) {
    showProcessingError(`无法加载配置：${e.message}`);
    return;
  }

  const savedModel = store.get('model', null);
  state.model = state.config.models.some((m) => m.key === savedModel) ? savedModel : state.config.default_model;
  el.model.innerHTML = state.config.models
    .map((m) => `<option value="${esc(m.key)}" title="${esc(m.desc)}">${esc(m.label)}（${esc(m.desc)}）</option>`)
    .join('');
  el.model.value = state.model;

  renderSwatches();
  const savedSpec = store.get('spec', null);
  const firstKey = state.config.specs.find((s) => s.key === savedSpec)?.key || state.config.specs.find((s) => !s.user)?.key;
  selectSpec(firstKey);
  const savedColor = store.get('color', null);
  if (savedColor?.hex) setColor(savedColor.hex, savedColor.key, { silent: true });

  state.showGuides = store.get('guides', true);
  el.guidesBtn.setAttribute('aria-pressed', state.showGuides);
  el.guides.classList.toggle('off', !state.showGuides);

  syncSliders();
  renderIdleInspector();
  bindEvents();
  showView('empty');
}

init();
