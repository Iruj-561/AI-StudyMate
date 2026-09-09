let currentQuestionIndex = 0;
let selectedOption = null;
let answered = false;

function getFilteredQuestions() {
  const params = new URLSearchParams(window.location.search);
  const topic = params.get('topic');
  if (topic) {
    return PRACTICE_QUESTIONS.filter(q => q.topic === topic);
  }
  return PRACTICE_QUESTIONS;
}

function renderQuestion() {
  const questions = getFilteredQuestions();
  if (!questions.length) {
    document.getElementById('practice-container').innerHTML = `
      <div class="card"><p>No questions available for this topic yet.</p></div>
    `;
    return;
  }

  const q = questions[currentQuestionIndex];
  selectedOption = null;
  answered = false;

  const paper = SYLLABUS.papers.find(p => p.id === q.paper);

  document.getElementById('practice-container').innerHTML = `
    <div class="flex-between mb-2">
      <div>
        <span class="badge badge-primary">${paper?.code || ''}</span>
        ${getDifficultyBadge(q.difficulty)}
      </div>
      <span class="text-muted">Question ${currentQuestionIndex + 1} of ${questions.length}</span>
    </div>

    <div class="card question-panel">
      <div class="question-text">${q.question}</div>
      <div class="options-list" id="options-list">
        ${q.options.map((opt, i) => `
          <button class="option-btn" data-index="${i}">
            <span class="option-letter">${String.fromCharCode(65 + i)}</span>
            <span>${opt}</span>
          </button>
        `).join('')}
      </div>

      <div id="solution-area"></div>

      <div class="flex-between mt-2">
        <button class="btn btn-secondary" id="prev-btn" ${currentQuestionIndex === 0 ? 'disabled' : ''}>← Previous</button>
        <div style="display:flex;gap:0.75rem">
          <button class="btn btn-ghost" id="hint-btn">💡 Get AI Hint</button>
          <button class="btn btn-primary" id="check-btn">Check Answer</button>
          <button class="btn btn-primary hidden" id="next-btn">Next →</button>
        </div>
      </div>
    </div>
  `;

  document.querySelectorAll('.option-btn').forEach(btn => {
    btn.addEventListener('click', () => selectOption(parseInt(btn.dataset.index)));
  });

  document.getElementById('check-btn').addEventListener('click', checkAnswer);
  document.getElementById('next-btn').addEventListener('click', nextQuestion);
  document.getElementById('prev-btn').addEventListener('click', prevQuestion);
  document.getElementById('hint-btn').addEventListener('click', showHint);
}

function selectOption(index) {
  if (answered) return;
  selectedOption = index;
  document.querySelectorAll('.option-btn').forEach((btn, i) => {
    btn.classList.toggle('selected', i === index);
  });
}

function checkAnswer() {
  if (selectedOption === null) return;
  answered = true;

  const questions = getFilteredQuestions();
  const q = questions[currentQuestionIndex];

  document.querySelectorAll('.option-btn').forEach((btn, i) => {
    btn.classList.remove('selected');
    if (i === q.correct) btn.classList.add('correct');
    else if (i === selectedOption) btn.classList.add('incorrect');
  });

  document.getElementById('solution-area').innerHTML = `
    <div class="solution-panel">
      <h4>✓ Step-by-Step Solution</h4>
      <div class="solution-steps">
        <ol>${q.solution.map(s => `<li>${s}</li>`).join('')}</ol>
      </div>
    </div>
  `;

  document.getElementById('check-btn').classList.add('hidden');
  document.getElementById('next-btn').classList.remove('hidden');
}

function showHint() {
  document.getElementById('solution-area').innerHTML = `
    <div class="solution-panel" style="background:rgba(99,102,241,0.08);border-color:rgba(99,102,241,0.2)">
      <h4 style="color:var(--primary-light)">💡 AI Hint</h4>
      <p style="font-size:0.925rem">Think about the key concept involved here. Try breaking the problem into smaller steps — what formula or rule applies to this type of question?</p>
    </div>
  `;
}

function nextQuestion() {
  const questions = getFilteredQuestions();
  if (currentQuestionIndex < questions.length - 1) {
    currentQuestionIndex++;
    renderQuestion();
  }
}

function prevQuestion() {
  if (currentQuestionIndex > 0) {
    currentQuestionIndex--;
    renderQuestion();
  }
}

function initPracticeFilters() {
  const paperSelect = document.getElementById('paper-filter');
  const diffSelect = document.getElementById('difficulty-filter');

  if (paperSelect) {
    SYLLABUS.papers.forEach(p => {
      const opt = document.createElement('option');
      opt.value = p.id;
      opt.textContent = `${p.code}: ${p.name}`;
      paperSelect.appendChild(opt);
    });
  }
}

document.addEventListener('DOMContentLoaded', () => {
  initPracticeFilters();
  renderQuestion();
});
