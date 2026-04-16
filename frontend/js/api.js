/**
 * api.js — CourierX Shared API Client
 * Central fetch wrapper used by every page.
 */

const BASE = '';   // Same origin — Flask serves both API and frontend

// ── Low-level fetch wrapper ──────────────────────────────────────────────────
async function apiFetch(method, path, body = null) {
  const opts = {
    method,
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
  };
  if (body) opts.body = JSON.stringify(body);

  const res  = await fetch(BASE + path, opts);
  const json = await res.json().catch(() => ({}));

  if (res.status === 401 && !path.includes('/api/auth/') && !path.includes('/api/admin/')) {
    // User session expired — redirect to user login (admin routes handle their own auth)
    window.location.href = '/index.html';
  }

  return { ok: res.ok, status: res.status, data: json };
}

// ── Convenience helpers ───────────────────────────────────────────────────────
const api = {
  get:    (path)        => apiFetch('GET',    path),
  post:   (path, body)  => apiFetch('POST',   path, body),
  put:    (path, body)  => apiFetch('PUT',    path, body),
  del:    (path, body)  => apiFetch('DELETE', path, body),
};

// ── Session helpers ──────────────────────────────────────────────────────────
async function requireAuth() {
  const r = await api.get('/api/auth/me');
  if (!r.ok) {
    window.location.href = '/index.html';
    return null;
  }
  return r.data;   // { userid, username }
}

async function requireAdmin() {
  const r = await api.get('/api/admin/users');
  if (!r.ok) {
    window.location.href = '/admin.html';
    return false;
  }
  return true;
}

// ── Toast notifications ──────────────────────────────────────────────────────
function showToast(message, type = 'info') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }

  const icons = { success: '✅', error: '❌', info: 'ℹ️' };
  const t = document.createElement('div');
  t.className = `toast toast-${type}`;
  t.innerHTML = `<span>${icons[type] || 'ℹ️'}</span><span>${message}</span>`;
  container.appendChild(t);

  setTimeout(() => {
    t.style.opacity = '0';
    t.style.transform = 'translateX(20px)';
    t.style.transition = 'all 0.3s';
    setTimeout(() => t.remove(), 300);
  }, 3500);
}

// ── Inline alert helpers ───────────────────────────────────────────────────
function setAlert(containerId, message, type = 'error') {
  const el = document.getElementById(containerId);
  if (!el) return;
  el.innerHTML = `<div class="alert alert-${type}">${message}</div>`;
}

function clearAlert(containerId) {
  const el = document.getElementById(containerId);
  if (el) el.innerHTML = '';
}

// ── Button loading state ─────────────────────────────────────────────────────
function setLoading(btn, loading, text = '') {
  if (loading) {
    btn.dataset.origText = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = `<span class="spinner"></span>`;
  } else {
    btn.disabled = false;
    btn.innerHTML = btn.dataset.origText || text;
  }
}

// ── Navbar active link ───────────────────────────────────────────────────────
function setActiveNav() {
  const page = window.location.pathname.split('/').pop() || 'dashboard.html';
  document.querySelectorAll('.nav-links a').forEach(a => {
    a.classList.toggle('active', a.getAttribute('href') === page);
  });
}

// ── Shared Navbar HTML (inserted by each page) ───────────────────────────────
function renderNavbar(username = '') {
  return `
  <nav class="navbar">
    <a href="/dashboard.html" class="nav-logo">📦 CourierX</a>
    <ul class="nav-links">
      <li><a href="/dashboard.html">Dashboard</a></li>
      <li><a href="/orders.html">Orders</a></li>
      <li><a href="/addresses.html">Addresses</a></li>
      <li><a href="/track.html">Track</a></li>
      <li><a href="/profile.html">Profile</a></li>
      <li><a href="/about.html">About</a></li>
    </ul>
    <div class="nav-right">
      <span class="nav-user">👤 ${username}</span>
      <button class="btn btn-ghost btn-sm" onclick="handleSignOut()">Sign Out</button>
    </div>
  </nav>`;
}

async function handleSignOut() {
  await api.post('/api/auth/signout');
  window.location.href = '/index.html';
}

// ── Format date helper ────────────────────────────────────────────────────────
function fmtDate(d) {
  if (!d) return '—';
  return d;
}

// ── Status badge helper ──────────────────────────────────────────────────────
function statusBadge(step) {
  const map = {
    0: ['badge-info',    'Processing'],
    1: ['badge-info',    'Packaging'],
    2: ['badge-warning', 'Ready to Ship'],
    3: ['badge-warning', 'Shipped'],
    4: ['badge-primary', 'Out for Delivery'],
    5: ['badge-success', 'Delivered'],
  };
  const [cls, label] = map[step] ?? ['badge-info', 'Unknown'];
  return `<span class="badge ${cls}">${label}</span>`;
}
