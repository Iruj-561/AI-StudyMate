const SYLLABUS = {
  papers: [
    {
      id: 'p1',
      code: 'Paper 1',
      name: 'Pure Mathematics 1',
      color: '#6366f1',
      icon: '📐',
      topics: [
        { id: 'quadratics', name: 'Quadratics', questions: 24, mastery: 72 },
        { id: 'functions', name: 'Functions', questions: 18, mastery: 45 },
        { id: 'coord-geom', name: 'Coordinate Geometry', questions: 22, mastery: 60 },
        { id: 'circular', name: 'Circular Measure', questions: 14, mastery: 30 },
        { id: 'trig', name: 'Trigonometry', questions: 28, mastery: 55 },
        { id: 'series', name: 'Series', questions: 20, mastery: 40 },
        { id: 'differentiation', name: 'Differentiation', questions: 32, mastery: 68 },
        { id: 'integration', name: 'Integration', questions: 26, mastery: 52 }
      ]
    },
    {
      id: 'p2',
      code: 'Paper 2',
      name: 'Pure Mathematics 2',
      color: '#818cf8',
      icon: '📊',
      topics: [
        { id: 'algebra-p2', name: 'Algebra', questions: 20, mastery: 38 },
        { id: 'log-exp-p2', name: 'Logarithmic & Exponential', questions: 24, mastery: 42 },
        { id: 'trig-p2', name: 'Trigonometry', questions: 22, mastery: 35 },
        { id: 'diff-p2', name: 'Differentiation', questions: 28, mastery: 50 },
        { id: 'int-p2', name: 'Integration', questions: 24, mastery: 44 },
        { id: 'numerical', name: 'Numerical Solutions', questions: 16, mastery: 25 }
      ]
    },
    {
      id: 'p3',
      code: 'Paper 3',
      name: 'Pure Mathematics 3',
      color: '#22d3ee',
      icon: '∫',
      topics: [
        { id: 'algebra-p3', name: 'Algebra', questions: 22, mastery: 20 },
        { id: 'log-exp-p3', name: 'Logarithmic & Exponential', questions: 20, mastery: 18 },
        { id: 'trig-p3', name: 'Trigonometry', questions: 26, mastery: 22 },
        { id: 'diff-p3', name: 'Differentiation', questions: 30, mastery: 28 },
        { id: 'int-p3', name: 'Integration', questions: 28, mastery: 15 },
        { id: 'vectors', name: 'Vectors', questions: 24, mastery: 10 },
        { id: 'diff-eq', name: 'Differential Equations', questions: 20, mastery: 8 },
        { id: 'complex', name: 'Complex Numbers', questions: 22, mastery: 12 }
      ]
    },
    {
      id: 'm1',
      code: 'Paper 4',
      name: 'Mechanics',
      color: '#f97316',
      icon: '⚙️',
      topics: [
        { id: 'forces', name: 'Forces & Equilibrium', questions: 20, mastery: 35 },
        { id: 'kinematics', name: 'Kinematics of Motion', questions: 24, mastery: 48 },
        { id: 'newton', name: "Newton's Laws", questions: 26, mastery: 40 },
        { id: 'energy', name: 'Energy, Work & Power', questions: 18, mastery: 32 },
        { id: 'momentum', name: 'Momentum', questions: 16, mastery: 28 }
      ]
    },
    {
      id: 's1',
      code: 'Paper 5',
      name: 'Probability & Statistics 1',
      color: '#34d399',
      icon: '📈',
      topics: [
        { id: 'data-rep', name: 'Representation of Data', questions: 16, mastery: 55 },
        { id: 'permutations', name: 'Permutations & Combinations', questions: 20, mastery: 42 },
        { id: 'probability', name: 'Probability', questions: 28, mastery: 50 },
        { id: 'drv', name: 'Discrete Random Variables', questions: 22, mastery: 38 },
        { id: 'normal', name: 'Normal Distribution', questions: 24, mastery: 45 }
      ]
    },
    {
      id: 's2',
      code: 'Paper 6',
      name: 'Probability & Statistics 2',
      color: '#a78bfa',
      icon: '🎲',
      topics: [
        { id: 'linear-comb', name: 'Linear Combinations', questions: 18, mastery: 15 },
        { id: 'poisson', name: 'Poisson Distribution', questions: 16, mastery: 12 },
        { id: 'continuous', name: 'Continuous Random Variables', questions: 20, mastery: 10 },
        { id: 'sampling', name: 'Sampling & Estimation', questions: 18, mastery: 8 },
        { id: 'hypothesis', name: 'Hypothesis Testing', questions: 22, mastery: 5 }
      ]
    }
  ]
};

const PRACTICE_QUESTIONS = [
  {
    id: 1,
    paper: 'p1',
    topic: 'quadratics',
    difficulty: 'medium',
    question: 'The quadratic equation x² − 5x + k = 0 has equal roots. Find the value of k.',
    options: ['k = 25/4', 'k = 5', 'k = 25/2', 'k = 6.25'],
    correct: 0,
    solution: [
      'For equal roots, the discriminant must equal zero: b² − 4ac = 0',
      'Here a = 1, b = −5, c = k',
      '(−5)² − 4(1)(k) = 0 → 25 − 4k = 0',
      '4k = 25 → k = 25/4 = 6.25'
    ]
  },
  {
    id: 2,
    paper: 'p1',
    topic: 'differentiation',
    difficulty: 'easy',
    question: 'Find dy/dx when y = 3x⁴ − 2x² + 7.',
    options: ['12x³ − 4x', '12x³ − 2x', '3x³ − 4x', '12x⁴ − 4x²'],
    correct: 0,
    solution: [
      'Differentiate each term using the power rule: d/dx(xⁿ) = nxⁿ⁻¹',
      'd/dx(3x⁴) = 12x³',
      'd/dx(−2x²) = −4x',
      'd/dx(7) = 0',
      'Therefore dy/dx = 12x³ − 4x'
    ]
  },
  {
    id: 3,
    paper: 'p1',
    topic: 'integration',
    difficulty: 'medium',
    question: 'Evaluate ∫(2x + 3) dx from x = 0 to x = 2.',
    options: ['10', '12', '14', '8'],
    correct: 0,
    solution: [
      '∫(2x + 3) dx = x² + 3x + C',
      'Definite integral from 0 to 2:',
      '[x² + 3x]₀² = (4 + 6) − (0 + 0) = 10'
    ]
  },
  {
    id: 4,
    paper: 'p3',
    topic: 'complex',
    difficulty: 'hard',
    question: 'Express (1 + i) / (1 − i) in the form a + bi.',
    options: ['i', '1 + i', '−i', '1 − i'],
    correct: 0,
    solution: [
      'Multiply numerator and denominator by the conjugate (1 + i):',
      '(1 + i)(1 + i) / (1 − i)(1 + i) = (1 + 2i + i²) / (1 − i²)',
      '= (1 + 2i − 1) / (1 + 1) = 2i / 2 = i'
    ]
  },
  {
    id: 5,
    paper: 's1',
    topic: 'probability',
    difficulty: 'medium',
    question: 'A bag contains 5 red and 3 blue balls. Two balls are drawn without replacement. Find P(both red).',
    options: ['5/14', '25/64', '10/28', '5/8'],
    correct: 0,
    solution: [
      'P(first red) = 5/8',
      'P(second red | first red) = 4/7',
      'P(both red) = (5/8) × (4/7) = 20/56 = 5/14'
    ]
  }
];

const QUIZ_QUESTIONS = [
  {
    question: 'What is the derivative of sin(2x)?',
    options: ['2cos(2x)', 'cos(2x)', '−2cos(2x)', '2sin(2x)'],
    correct: 0,
    topic: 'Differentiation'
  },
  {
    question: 'The sum of the first n terms of an AP is 3n² + 5n. Find the 10th term.',
    options: ['58', '62', '56', '60'],
    correct: 0,
    topic: 'Series'
  },
  {
    question: 'Solve: log₂(x) + log₂(x − 2) = 3',
    options: ['x = 4', 'x = 2', 'x = 8', 'x = 6'],
    correct: 0,
    topic: 'Logarithms'
  },
  {
    question: 'Find the magnitude of vector (3, −4).',
    options: ['5', '7', '1', '25'],
    correct: 0,
    topic: 'Vectors'
  },
  {
    question: 'P(X = 2) for Poisson(λ = 3) equals:',
    options: ['9e⁻³/2', '3e⁻³', 'e⁻³', '6e⁻³'],
    correct: 0,
    topic: 'Poisson'
  }
];

const MOCK_EXAM_QUESTIONS = Array.from({ length: 10 }, (_, i) => ({
  id: i + 1,
  question: `Question ${i + 1}: ${
    [
      'Find the set of values of k for which x² + kx + 9 = 0 has no real roots.',
      'The curve y = f(x) passes through (2, 5) and f\'(x) = 3x² − 2. Find f(x).',
      'Solve the equation 2 sin θ = cos θ for 0° ≤ θ ≤ 360°.',
      'A particle moves in a straight line with velocity v = 3t² − 12t + 9. Find when it is at rest.',
      'The heights of students are normally distributed with mean 165 cm and SD 8 cm. Find P(height > 175).',
      'Expand (1 + 2x)⁵ in ascending powers of x up to the term in x³.',
      'Find the area enclosed between y = x² and y = 2x.',
      'Given |a| = 3 and |b| = 4 and a · b = 6, find the angle between a and b.',
      'A fair die is rolled twice. Find the probability that the sum is at least 10.',
      'Test at 5% significance whether the mean has changed from 50, given x̄ = 52, n = 30, σ = 4.'
    ][i]
  }`,
  marks: [3, 5, 4, 4, 5, 3, 6, 4, 3, 5][i]
}));

const CHAT_SUGGESTIONS = [
  'Explain the discriminant',
  'Help with integration by parts',
  'What is a normal distribution?',
  'Step-by-step: chain rule'
];

const AI_RESPONSES = {
  discriminant: `The **discriminant** of a quadratic ax² + bx + c = 0 is **Δ = b² − 4ac**.

• **Δ > 0** → two distinct real roots
• **Δ = 0** → one repeated real root (equal roots)
• **Δ < 0** → no real roots (complex roots)

**Example:** For x² − 5x + 6 = 0, Δ = 25 − 24 = 1 > 0, so two roots: x = 2 and x = 3.`,

  integration: `**Integration by parts** uses: ∫u dv = uv − ∫v du

**Strategy:**
1. Choose u (use LIATE: Log, Inverse trig, Algebraic, Trig, Exponential)
2. Find du and dv
3. Apply the formula

**Example:** ∫x eˣ dx
• u = x, dv = eˣ dx
• du = dx, v = eˣ
• Result: x eˣ − eˣ + C = eˣ(x − 1) + C`,

  normal: `The **Normal Distribution** is a bell-shaped continuous probability distribution defined by:

• Mean μ (centre)
• Standard deviation σ (spread)

**Key facts for 9709:**
• ~68% of data within μ ± σ
• ~95% within μ ± 2σ
• Standardising: Z = (X − μ) / σ

Use standard normal tables for P(Z ≤ z).`,

  chain: `The **Chain Rule** for y = f(g(x)):

**dy/dx = f'(g(x)) · g'(x)**

**Example:** y = (3x² + 1)⁵
• Outer: u⁵ → 5u⁴
• Inner: 3x² + 1 → 6x
• **dy/dx = 5(3x² + 1)⁴ · 6x = 30x(3x² + 1)⁴**

Always identify the "outer" and "inner" functions first!`,

  default: `I'd be happy to help with your Cambridge 9709 Mathematics studies!

I can provide:
• **Step-by-step solutions** to problems
• **Concept explanations** tailored to your level
• **Exam tips** and common mistakes to avoid
• **Practice questions** on any topic

What specific topic or question would you like to explore? Try asking about quadratics, differentiation, vectors, or statistics!`
};
