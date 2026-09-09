function initSidebar() {
  const toggle = document.querySelector('.menu-toggle');
  const sidebar = document.querySelector('.sidebar');
  const overlay = document.querySelector('.sidebar-overlay');

  if (!toggle || !sidebar) return;

  toggle.addEventListener('click', () => {
    sidebar.classList.toggle('open');
    overlay?.classList.toggle('open');
  });

  overlay?.addEventListener('click', () => {
    sidebar.classList.remove('open');
    overlay.classList.remove('open');
  });
}

function setActiveNav() {
  const current = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-link').forEach(link => {
    const href = link.getAttribute('href');
    if (href === current || (current === '' && href === 'index.html')) {
      link.classList.add('active');
    }
  });
}

function renderSidebar(activePage) {
  const pages = [
    { href: 'dashboard.html', icon: '🏠', label: 'Dashboard' },
    { href: 'topics.html', icon: '📚', label: 'Syllabus Topics' },
    { href: 'practice.html', icon: '✏️', label: 'Practice' },
    { href: 'quiz.html', icon: '⚡', label: 'Quick Quiz' },
    { href: 'mock-exam.html', icon: '📝', label: 'Mock Exam' },
    { href: 'ai-chat.html', icon: '🤖', label: 'AI Tutor' }
  ];

  const nav = pages.map(p => `
    <a href="${p.href}" class="nav-link ${p.href === activePage ? 'active' : ''}">
      <span class="icon">${p.icon}</span>
      ${p.label}
    </a>
  `).join('');

  return `
    <aside class="sidebar">
      <a href="index.html" class="sidebar-logo">
        <div class="sidebar-logo-icon">🎓</div>
        <div class="sidebar-logo-text">
          AI StudyMate
          <span>Cambridge 9709</span>
        </div>
      </a>
      <nav class="sidebar-nav">${nav}</nav>
      <div class="sidebar-footer">
        <div class="user-chip">
          <div class="user-avatar">AS</div>
          <div class="user-info">
            <div class="name">Alex Student</div>
            <div class="role">A-Level Year 13</div>
          </div>
        </div>
      </div>
    </aside>
    <div class="sidebar-overlay"></div>
    <button class="menu-toggle" aria-label="Toggle menu">☰</button>
  `;
}

function getMasteryColor(mastery) {
  if (mastery >= 70) return 'var(--success)';
  if (mastery >= 40) return 'var(--warning)';
  return 'var(--danger)';
}

function getDifficultyBadge(difficulty) {
  const map = {
    easy: 'badge-success',
    medium: 'badge-warning',
    hard: 'badge-primary'
  };
  return `<span class="badge ${map[difficulty] || 'badge-muted'}">${difficulty}</span>`;
}

function animateProgressBars() {
  document.querySelectorAll('.progress-fill').forEach(bar => {
    const width = bar.dataset.width || bar.style.width;
    bar.style.width = '0';
    requestAnimationFrame(() => {
      bar.style.width = width;
    });
  });
}

document.addEventListener('DOMContentLoaded', () => {
  initSidebar();
  setActiveNav();
  animateProgressBars();
});
