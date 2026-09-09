let examIndex = 0;
let examAnswers = new Array(MOCK_EXAM_QUESTIONS.length).fill('');
let flaggedQuestions = new Set();
let examTimer = null;
let examTimeLeft = 4500;

function formatExamTime(seconds) {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = seconds % 60;
  return `${h}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
}

function renderExamStart() {
  document.getElementById('exam-start-screen').classList.remove('hidden');
  document.getElementById('exam-active').classList.add('hidden');
}

function startExam() {
  document.getElementById('exam-start-screen').classList.add('hidden');
  document.getElementById('exam-active').classList.remove('hidden');

  examTimer = setInterval(() => {
    examTimeLeft--;
    const el = document.getElementById('exam-timer');
    if (el) {
      el.textContent = formatExamTime(examTimeLeft);
      el.classList.toggle('warning', examTimeLeft <= 600);
    }
    if (examTimeLeft <= 0) submitExam();
  }, 1000);

  renderExamQuestion();
  renderQuestionNav();
}

function renderExamQuestion() {
  const q = MOCK_EXAM_QUESTIONS[examIndex];

  document.getElementById('exam-question-area').innerHTML = `
    <div class="flex-between mb-2">
      <span class="badge badge-primary">${q.marks} marks</span>
      <button class="btn btn-ghost btn-sm" id="flag-btn">
        ${flaggedQuestions.has(examIndex) ? '🚩 Flagged' : '🏳️ Flag for review'}
      </button>
    </div>
    <div class="card">
      <div class="question-number">Question ${q.id}</div>
      <div class="question-text">${q.question}</div>
      <textarea
        id="exam-answer"
        rows="8"
        placeholder="Write your working and answer here..."
        style="width:100%;padding:1rem;background:var(--bg-elevated);border:1px solid var(--border);border-radius:var(--radius);resize:vertical;line-height:1.6"
      >${examAnswers[examIndex]}</textarea>
      <div class="flex-between mt-2">
        <button class="btn btn-secondary" id="exam-prev" ${examIndex === 0 ? 'disabled' : ''}>← Previous</button>
        <button class="btn btn-primary" id="exam-next">
          ${examIndex === MOCK_EXAM_QUESTIONS.length - 1 ? 'Review & Submit' : 'Next →'}
        </button>
      </div>
    </div>
  `;

  document.getElementById('exam-answer').addEventListener('input', e => {
    examAnswers[examIndex] = e.target.value;
    renderQuestionNav();
  });

  document.getElementById('flag-btn').addEventListener('click', () => {
    if (flaggedQuestions.has(examIndex)) flaggedQuestions.delete(examIndex);
    else flaggedQuestions.add(examIndex);
    renderExamQuestion();
    renderQuestionNav();
  });

  document.getElementById('exam-prev').addEventListener('click', () => {
    if (examIndex > 0) { examIndex--; renderExamQuestion(); renderQuestionNav(); }
  });

  document.getElementById('exam-next').addEventListener('click', () => {
    if (examIndex < MOCK_EXAM_QUESTIONS.length - 1) {
      examIndex++;
      renderExamQuestion();
      renderQuestionNav();
    } else {
      showSubmitConfirm();
    }
  });

  renderQuestionNav();
}

function renderQuestionNav() {
  const nav = document.getElementById('exam-q-nav');
  nav.innerHTML = MOCK_EXAM_QUESTIONS.map((_, i) => {
    let cls = 'exam-q-btn';
    if (i === examIndex) cls += ' current';
    if (examAnswers[i].trim()) cls += ' answered';
    if (flaggedQuestions.has(i)) cls += ' flagged';
    return `<button class="${cls}" data-q="${i}">${i + 1}</button>`;
  }).join('');

  nav.querySelectorAll('.exam-q-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      examIndex = parseInt(btn.dataset.q);
      renderExamQuestion();
    });
  });

  const answered = examAnswers.filter(a => a.trim()).length;
  document.getElementById('exam-progress-text').textContent = `${answered}/${MOCK_EXAM_QUESTIONS.length} answered`;
}

function showSubmitConfirm() {
  const unanswered = examAnswers.filter(a => !a.trim()).length;
  document.getElementById('exam-question-area').innerHTML = `
    <div class="card" style="max-width:560px;margin:0 auto;text-align:center;padding:2.5rem">
      <h2 style="font-family:var(--font-display);margin-bottom:1rem">Submit Exam?</h2>
      <p class="text-muted" style="margin-bottom:0.5rem">
        ${unanswered > 0 ? `${unanswered} question(s) unanswered.` : 'All questions answered!'}
      </p>
      <p class="text-muted" style="margin-bottom:2rem">Time remaining: ${formatExamTime(examTimeLeft)}</p>
      <div style="display:flex;gap:0.75rem;justify-content:center">
        <button class="btn btn-secondary" id="cancel-submit">Continue Exam</button>
        <button class="btn btn-primary btn-accent" id="confirm-submit">Submit Exam</button>
      </div>
    </div>
  `;

  document.getElementById('cancel-submit').addEventListener('click', renderExamQuestion);
  document.getElementById('confirm-submit').addEventListener('click', submitExam);
}

function submitExam() {
  clearInterval(examTimer);
  const answered = examAnswers.filter(a => a.trim()).length;

  document.getElementById('exam-active').innerHTML = `
    <div class="card" style="max-width:600px;margin:2rem auto;text-align:center;padding:3rem">
      <div style="font-size:3rem;margin-bottom:1rem">📝</div>
      <h2 style="font-family:var(--font-display);margin-bottom:0.75rem">Exam Submitted</h2>
      <p class="text-muted" style="margin-bottom:1.5rem">
        You answered ${answered} of ${MOCK_EXAM_QUESTIONS.length} questions.
        AI marking and detailed feedback coming soon!
      </p>
      <a href="dashboard.html" class="btn btn-primary">Back to Dashboard</a>
    </div>
  `;
}

document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('start-exam')?.addEventListener('click', startExam);
});
