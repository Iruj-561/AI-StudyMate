import os
import re
import time

import gradio as gr
from google import genai
import spaces

# Gemini setup

API_KEY = os.environ.get("GEMINI_API_KEY_3")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY_3 secret is missing from your Hugging Face Space."
    )

client = genai.Client(api_key=API_KEY)

# Primary model + fallback model
MODEL_NAMES = [
    "gemini-3.8-flash",
    "gemini-3.6-flash",
]


# Loading study notes

try:
    with open("notes.txt", "r", encoding="utf-8") as f:
        FULL_NOTES = f.read()

except FileNotFoundError:
    FULL_NOTES = ""

if not FULL_NOTES.strip():
    FULL_NOTES = "No study notes were found."


# Paper/component aliases

PAPER_ALIASES = {
    "P1": [
        "p1",
        "paper 1",
        "pure mathematics 1",
        "pure math 1",
    ],
    "P2": [
        "p2",
        "paper 2",
        "pure mathematics 2",
        "pure math 2",
    ],
    "P3": [
        "p3",
        "paper 3",
        "pure mathematics 3",
        "pure math 3",
    ],
    "M1": [
        "m1",
        "paper 4",
        "mechanics",
        "mechanics 1",
    ],
    "S1": [
        "s1",
        "paper 5",
        "statistics 1",
        "probability and statistics 1",
    ],
    "S2": [
        "s2",
        "paper 6",
        "statistics 2",
        "probability and statistics 2",
    ],
}


# Topic aliases

TOPIC_ALIASES = {

    # ---------------- P1 ----------------
    "quadratics": [
        "quadratic",
        "quadratics",
        "quadratic equations",
        "quadratic functions",
    ],

    "functions": [
        "function",
        "functions",
        "composite functions",
        "inverse functions",
    ],

    "coordinate geometry": [
        "coordinate geometry",
        "straight line",
        "straight lines",
        "gradient",
        "midpoint",
        "distance between points",
    ],

    "circular measure": [
        "circular measure",
        "radians",
        "radian",
        "arc length",
        "sector",
        "sector area",
    ],

    "trigonometry": [
        "trigonometry",
        "trig",
        "sine rule",
        "cosine rule",
        "sine",
        "cosine",
        "tangent",
        "trig identities",
    ],

    "series": [
        "series",
        "arithmetic progression",
        "arithmetic progressions",
        "geometric progression",
        "geometric progressions",
        "arithmetic sequence",
        "geometric sequence",
        "sum to infinity",
    ],

    "differentiation": [
        "differentiation",
        "differentiate",
        "derivative",
        "derivatives",
        "stationary points",
        "tangent",
        "normal",
        "rates of change",
    ],

    "integration": [
        "integration",
        "integrate",
        "integral",
        "integrals",
        "area under curve",
        "area under a curve",
    ],

    # ---------------- P2 ----------------
    "algebra": [
        "algebra",
        "algebraic manipulation",
        "partial fractions",
        "binomial expansion",
    ],

    "logarithms": [
        "logarithm",
        "logarithms",
        "log",
        "ln",
    ],

    "exponentials": [
        "exponential",
        "exponentials",
        "exponential functions",
    ],

    "numerical methods": [
        "numerical solution",
        "numerical solutions",
        "numerical methods",
        "iteration",
        "iterations",
        "root",
        "roots",
    ],

    # ---------------- P3 ----------------
    "complex numbers": [
        "complex number",
        "complex numbers",
        "complex",
        "argand diagram",
        "argand",
        "modulus",
        "argument",
    ],

    "matrices": [
        "matrix",
        "matrices",
        "determinant",
        "inverse matrix",
    ],

    "vectors": [
        "vector",
        "vectors",
        "vector geometry",
    ],

    "further differentiation": [
        "further differentiation",
        "implicit differentiation",
        "parametric differentiation",
    ],

    "further integration": [
        "further integration",
        "integration by parts",
        "substitution",
    ],

    # ---------------- M1 ----------------
    "kinematics": [
        "kinematics",
        "motion",
        "displacement",
        "velocity",
        "acceleration",
        "constant acceleration",
    ],

    "forces": [
        "forces",
        "force",
        "newton",
        "newton's laws",
        "resultant force",
    ],

    "friction": [
        "friction",
        "coefficient of friction",
        "limiting equilibrium",
    ],

    "moments": [
        "moments",
        "moment",
        "turning effect",
        "equilibrium",
    ],

    # ---------------- S1 ----------------
    "representation of data": [
        "representation of data",
        "histogram",
        "box plot",
        "box plots",
        "cumulative frequency",
        "stem and leaf",
        "stem-and-leaf",
    ],

    "probability": [
        "probability",
        "probabilities",
        "conditional probability",
        "independent events",
    ],

    "discrete random variables": [
        "discrete random variable",
        "discrete random variables",
        "binomial distribution",
        "geometric distribution",
        "expected value",
        "expectation",
        "variance of a random variable",
    ],

    "normal distribution": [
        "normal distribution",
        "normal distributions",
        "standard normal",
        "z score",
        "z-score",
    ],

    # ---------------- S2 ----------------
    "poisson distribution": [
        "poisson",
        "poisson distribution",
        "poisson distributions",
    ],

    "linear combinations of random variables": [
        "linear combinations of random variables",
        "linear combination",
        "random variables",
        "e(x)",
        "var(x)",
        "e(x+y)",
        "var(x+y)",
    ],

    "continuous random variables": [
        "continuous random variable",
        "continuous random variables",
        "probability density function",
        "probability density",
        "density function",
        "pdf",
    ],

    "sampling and estimation": [
        "sampling",
        "sampling and estimation",
        "estimation",
        "sample",
        "population",
        "confidence interval",
        "confidence intervals",
        "population mean",
        "population proportion",
    ],

    "hypothesis tests": [
        "hypothesis test",
        "hypothesis tests",
        "null hypothesis",
        "alternative hypothesis",
        "significance level",
        "critical region",
        "rejection region",
        "test statistic",
        "one tailed",
        "two tailed",
    ],
}


# 5. Normalise text

def normalise(text):
    text = text.lower()
    text = text.replace("–", "-")
    text = text.replace("—", "-")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# Splitting notes into chunks

def split_into_chunks(text, max_chars=4500):

    paragraphs = re.split(r"\n\s*\n", text)

    chunks = []
    current = ""

    for paragraph in paragraphs:

        paragraph = paragraph.strip()

        if not paragraph:
            continue

        if len(paragraph) <= max_chars:

            if len(current) + len(paragraph) + 2 <= max_chars:
                current += paragraph + "\n\n"
            else:
                if current.strip():
                    chunks.append(current.strip())

                current = paragraph + "\n\n"

        else:

            if current.strip():
                chunks.append(current.strip())
                current = ""

            start = 0

            while start < len(paragraph):
                piece = paragraph[start:start + max_chars]
                chunks.append(piece.strip())
                start += max_chars

    if current.strip():
        chunks.append(current.strip())

    return chunks


NOTE_CHUNKS = split_into_chunks(FULL_NOTES)


# Detecting papers

def detect_papers(question):

    q = normalise(question)

    detected = []

    for paper, aliases in PAPER_ALIASES.items():

        for alias in aliases:

            if alias in q:
                detected.append(paper)
                break

    return detected


# Detect topics

def detect_topics(question):

    q = normalise(question)

    detected = []

    for topic, aliases in TOPIC_ALIASES.items():

        for alias in aliases:

            if alias in q:
                detected.append(topic)
                break

    return detected


# Score note chunks

def score_chunk(chunk, question, detected_topics, detected_papers):

    q = normalise(question)
    c = normalise(chunk)

    score = 0

    # Exact question words
    question_words = set(
        re.findall(r"[a-zA-Z]{3,}", q)
    )

    chunk_words = set(
        re.findall(r"[a-zA-Z]{3,}", c)
    )

    common_words = question_words.intersection(chunk_words)

    score += min(len(common_words), 20)

    # Topic matches are more important
    for topic in detected_topics:

        if normalise(topic) in c:
            score += 25

        for alias in TOPIC_ALIASES.get(topic, []):

            if normalise(alias) in c:
                score += 15

    # Paper matches
    for paper in detected_papers:

        for alias in PAPER_ALIASES.get(paper, []):

            if normalise(alias) in c:
                score += 10

    return score


# Retrieving relevant notes

def retrieve_relevant_notes(question, max_context_chars=15000):

    detected_topics = detect_topics(question)
    detected_papers = detect_papers(question)

    scored = []

    for index, chunk in enumerate(NOTE_CHUNKS):

        score = score_chunk(
            chunk,
            question,
            detected_topics,
            detected_papers
        )

        scored.append((score, index, chunk))

    scored.sort(
        key=lambda item: item[0],
        reverse=True
    )

    selected = []
    total_chars = 0

    # Take strongest chunks first
    for score, index, chunk in scored:

        if score <= 0:
            continue

        if total_chars + len(chunk) > max_context_chars:
            continue

        selected.append(chunk)
        total_chars += len(chunk)

        if total_chars >= max_context_chars:
            break

    # Fallback if nothing matched
    if not selected:

        for score, index, chunk in scored[:3]:

            if total_chars + len(chunk) <= max_context_chars:
                selected.append(chunk)
                total_chars += len(chunk)

    return "\n\n--- RELEVANT NOTES ---\n\n".join(selected)


# Detecting task

def detect_task(question):

    q = normalise(question)

    if (
        "mock exam" in q
        or "mock paper" in q
        or "full paper" in q
        or "practice paper" in q
        or "generate a paper" in q
        or "generate paper" in q
    ):
        return "mock"

    if (
        "practice question" in q
        or "practice questions" in q
        or "give me questions" in q
        or "give me a question" in q
        or "generate questions" in q
        or "generate a question" in q
        or "make questions" in q
    ):
        return "practice"

    if (
        "give me a hint" in q
        or "give hint" in q
        or "hint please" in q
        or "hint" == q
    ):
        return "hint"

    if (
        "check my answer" in q
        or "is my answer correct" in q
        or "check this answer" in q
    ):
        return "check"

    if (
        "summarise" in q
        or "summarize" in q
        or "summary" in q
        or "revision notes" in q
        or "make notes" in q
        or "detailed notes" in q
    ):
        return "notes"

    if (
        "explain" in q
        or "teach me" in q
        or "what is" in q
        or "what are" in q
        or "how does" in q
        or "how do" in q
    ):
        return "explain"

    return "general"


# Recent chat history

def get_recent_history(history, max_messages=4):

    if not history:
        return ""

    recent = history[-max_messages:]

    lines = []

    for item in recent:

        if isinstance(item, dict):

            role = item.get("role", "")
            content = item.get("content", "")

            if role and content:
                lines.append(
                    f"{role.upper()}: {content}"
                )

        elif isinstance(item, (list, tuple)) and len(item) >= 2:

            user_msg = item[0]
            assistant_msg = item[1]

            if user_msg:
                lines.append(
                    f"USER: {user_msg}"
                )

            if assistant_msg:
                lines.append(
                    f"ASSISTANT: {assistant_msg}"
                )

    return "\n".join(lines)


# Task instructions

TASK_INSTRUCTIONS = {

    "explain": """
Explain the concept clearly like a friendly A-Level tutor.
Start with the basic idea.
Then explain the important formulae or rules.
Then give a simple example where useful.
Break difficult ideas into small steps.
""",

    "notes": """
Create useful revision notes from the relevant material.
Use clear headings.
Include definitions, formulae, important rules, methods and examples.
Keep the notes organised and exam-focused.
Do not unnecessarily repeat information.
""",

    "practice": """
Generate the requested number of ORIGINAL A-Level Mathematics 9709 practice questions.
Match the requested paper/component and topic.
Vary the difficulty when the student requests mixed difficulty.
Do NOT copy or closely paraphrase past-paper questions.
Create new numerical values and/or contexts while testing the same syllabus skill.
Give the questions first.
Do not automatically reveal full solutions unless the student asks for them.
""",

    "mock": """
Create an ORIGINAL mock examination based on the student's requested component/topic.
Follow the style and difficulty of Cambridge International A-Level Mathematics 9709.
Use relevant syllabus skills from the supplied notes.
Do not copy or closely paraphrase past-paper questions.
Include:
- paper/component name
- instructions
- questions
- marks for each question
- a sensible total number of marks
Do not provide the mark scheme unless the student asks for it.
""",

    "hint": """
Give a useful hint without immediately giving the complete answer.
Point the student toward the correct formula, method or first step.
Let them do as much of the problem themselves as possible.
""",

    "check": """
Check the student's answer carefully.
State whether it is correct.
If it is incorrect, explain exactly where the mistake happened.
Then show the correct method clearly.
""",

    "general": """
Answer the student's question directly and clearly.
For mathematics questions, show the important working.
For simple questions such as arithmetic, answer simply.
"""
}


# System prompt

SYSTEM_PROMPT = """
You are StudyMate, an AI tutor for Cambridge International
A-Level Mathematics 9709.
Your job is to help students understand mathematics, practise
exam-style questions and revise the 9709 syllabus.
IMPORTANT RULES:
1. Stay focused on A-Level Mathematics 9709.
2. Use the supplied relevant study notes as the primary source
   whenever the question concerns syllabus content.
3. Never claim that an example question is copied from a
   Cambridge past paper.
4. Practice questions and mock papers must be ORIGINAL.
   Never reproduce, closely paraphrase, or merely change the
   numbers in a copyrighted past-paper question.
5. Explain mathematics in a clear student-friendly way.
6. Show calculations step by step when appropriate.
7. NEVER output raw LaTeX.
Do NOT use:
$
$$
\\frac
\\sqrt
\\theta
\\pi
\\Delta
\\text
\\left
\\right
\\times in LaTeX form
Use readable mathematical notation instead, such as:
x²
x³
√x
π
θ
Δ
≤
≥
≠
±
∞
×
→
dy/dx
∫
1/2
3/4
8. Do not add unnecessary disclaimers.
9. If a student asks for a number of questions, give exactly
   the requested number whenever practical.
10. If a student specifies a component such as P1, P2, P3,
    M1, S1 or S2, respect that component.
11. If a student specifies a topic such as Integration,
    Differentiation, Poisson distribution or Hypothesis tests,
    focus specifically on that topic.
12. If the question is outside 9709, politely explain that
    StudyMate is focused on Cambridge A-Level Mathematics 9709.
"""


# Clean gemini output

def clean_output(text):

    if not text:
        return "I couldn't generate a response."

    text = str(text)

    # Remove LaTeX delimiters
    text = text.replace("$$", "")
    text = text.replace("$", "")
    text = text.replace(r"\(", "")
    text = text.replace(r"\)", "")
    text = text.replace(r"\[", "")
    text = text.replace(r"\]", "")

    # Fractions
    fraction_pattern = r"\\frac\{([^{}]+)\}\{([^{}]+)\}"

    for _ in range(3):
        text = re.sub(
            fraction_pattern,
            r"\1/\2",
            text
        )

    # Square roots
    sqrt_pattern = r"\\sqrt\{([^{}]+)\}"

    text = re.sub(
        sqrt_pattern,
        r"√\1",
        text
    )

    # Common LaTeX symbols
    replacements = {
        r"\theta": "θ",
        r"\pi": "π",
        r"\Delta": "Δ",
        r"\lambda": "λ",
        r"\mu": "μ",
        r"\sigma": "σ",
        r"\alpha": "α",
        r"\beta": "β",
        r"\gamma": "γ",
        r"\infty": "∞",
        r"\leq": "≤",
        r"\le": "≤",
        r"\geq": "≥",
        r"\ge": "≥",
        r"\neq": "≠",
        r"\pm": "±",
        r"\times": "×",
        r"\cdot": "·",
        r"\rightarrow": "→",
        r"\to": "→",
        r"\sum": "Σ",
        r"\int": "∫",
        r"\approx": "≈",
        r"\ldots": "...",
        r"\cdots": "...",
        r"\text": "",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # Common superscripts
    superscript_map = {
        "0": "⁰",
        "1": "¹",
        "2": "²",
        "3": "³",
        "4": "⁴",
        "5": "⁵",
        "6": "⁶",
        "7": "⁷",
        "8": "⁸",
        "9": "⁹",
    }

    def convert_superscript(match):

        base = match.group(1)
        power = match.group(2)

        converted = "".join(
            superscript_map.get(char, "^" + char)
            for char in power
        )

        return base + converted

    text = re.sub(
        r"([A-Za-z0-9\)])\^([0-9]+)",
        convert_superscript,
        text
    )

    # Remove accidental double spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Clean excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


# Gemini request

@spaces.GPU
def ask_question(message, history):

    if not message or not message.strip():
        return "", history

    message = message.strip()

    task = detect_task(message)
    detected_papers = detect_papers(message)
    detected_topics = detect_topics(message)

    recent_history = get_recent_history(
        history,
        max_messages=4
    )

    papers_text = (
        ", ".join(detected_papers)
        if detected_papers
        else "Not explicitly specified"
    )

    topics_text = (
        ", ".join(detected_topics)
        if detected_topics
        else "Not explicitly specified"
    )

    task_instruction = TASK_INSTRUCTIONS.get(
        task,
        TASK_INSTRUCTIONS["general"]
    )

    # Try different context sizes if Gemini has a temporary
    # server problem

    context_sizes = [15000, 8500, 5000]

    last_error = None

    # Try the available models one by one.
    #
    # Important:
    # 429 = quota exhausted for that model
    # 503 = temporary model availability problem

    for model_index, model_name in enumerate(MODEL_NAMES):

        print(f"Trying Gemini model: {model_name}")

        for attempt in range(3):

            try:

                # Use smaller context on later attempts
                context_size = context_sizes[
                    min(attempt, len(context_sizes) - 1)
                ]

                relevant_notes = retrieve_relevant_notes(
                    message,
                    max_context_chars=context_size
                )

                prompt = f"""
{SYSTEM_PROMPT}
TASK TYPE:
{task}
REQUESTED PAPER / COMPONENT:
{papers_text}
REQUESTED TOPIC:
{topics_text}
TASK-SPECIFIC INSTRUCTIONS:
{task_instruction}
RECENT CONVERSATION:
{recent_history if recent_history else "No previous conversation."}
RELEVANT STUDY NOTES:
{relevant_notes}
STUDENT'S CURRENT QUESTION:
{message}
Now answer the student.
"""

                print(
                    f"Gemini request: model={model_name}, "
                    f"attempt={attempt + 1}, "
                    f"context={context_size}"
                )

                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )

                answer = response.text

                if not answer:
                    raise RuntimeError(
                        "Gemini returned an empty response."
                    )

                answer = clean_output(answer)

                print(
                    f"Gemini success using {model_name}"
                )

                # Add successful response to chat history

                new_history = list(history) if history else []

                new_history.append({
                    "role": "user",
                    "content": message
                })

                new_history.append({
                    "role": "assistant",
                    "content": answer
                })

                return "", new_history

            except Exception as error:

                last_error = error
                error_text = str(error).lower()

                print(
                    f"Gemini failed: model={model_name}, "
                    f"attempt={attempt + 1}"
                )
                print(repr(error))

                
                # QUOTA ERROR
                # Do NOT retry the same model if its quota is
                # exhausted. Move immediately to the fallback.
               

                is_quota_error = (
                    "429" in error_text
                    or "resource_exhausted" in error_text
                    or "quota" in error_text
                    or "exceeded your current quota" in error_text
                )

                if is_quota_error:

                    print(
                        f"Quota exhausted for {model_name}. "
                        f"Moving to next model."
                    )

                    break

              
                # TEMPORARY SERVER ERROR
              
                # Retry the same model up to 3 times
                

                is_temporary_error = (
                    "503" in error_text
                    or "unavailable" in error_text
                    or "high demand" in error_text
                    or "service unavailable" in error_text
                )

                if is_temporary_error:

                    if attempt < 2:

                        delay = 2 ** attempt

                        print(
                            f"Temporary Gemini error. "
                            f"Waiting {delay} seconds..."
                        )

                        time.sleep(delay)

                        continue

                    else:

                        print(
                            f"{model_name} still unavailable "
                            f"after 3 attempts."
                        )

                        # Move to fallback model
                        break

               
                # Other errors
   
                # Don't blindly retry things like invalid requests

                print(
                    f"Non-retryable Gemini error for "
                    f"{model_name}."
                )

                break


    # What to do if all models failed?

    print("FINAL GEMINI ERROR:", repr(last_error))

    error_text = str(last_error).lower() if last_error else ""

    # Give the user a more useful message
    if (
        "429" in error_text
        or "resource_exhausted" in error_text
        or "quota" in error_text
    ):

        error_message = (
            "StudyMate has temporarily reached the AI usage limit "
            "for the available Gemini models.\n\n"
            "Please try again later."
        )

    elif (
        "503" in error_text
        or "unavailable" in error_text
        or "high demand" in error_text
    ):

        error_message = (
            "The AI model is temporarily unavailable right now.\n\n"
            "Please try again in a little while."
        )

    else:

        error_message = (
            "StudyMate couldn't generate that response right now.\n\n"
            "Please try the question again."
        )

    new_history = list(history) if history else []

    new_history.append({
        "role": "user",
        "content": message
    })

    new_history.append({
        "role": "assistant",
        "content": error_message
    })

    return "", new_history

    # Retry strategy for temporary Gemini 503 errors

    retry_delays = [1, 2, 4]
    context_sizes = [15000, 8500, 5000]

    last_error = None

    for attempt in range(3):

        try:

            if attempt > 0:
                time.sleep(retry_delays[attempt - 1])

                # Retry with an even smaller context
                smaller_notes = retrieve_relevant_notes(
                    message,
                    max_context_chars=context_sizes[attempt]
                )

                prompt = f"""
{SYSTEM_PROMPT}
TASK TYPE:
{task}
REQUESTED PAPER / COMPONENT:
{papers_text}
REQUESTED TOPIC:
{topics_text}
TASK-SPECIFIC INSTRUCTIONS:
{task_instruction}
RECENT CONVERSATION:
{recent_history if recent_history else "No previous conversation."}
RELEVANT STUDY NOTES:
{smaller_notes}
STUDENT'S CURRENT QUESTION:
{message}
Now answer the student.
"""

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )

            answer = response.text

            if not answer:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            answer = clean_output(answer)

            # Gradio 6.26.0 uses message dictionaries here
            new_history = list(history) if history else []

            new_history.append({
                "role": "user",
                "content": message
            })

            new_history.append({
                "role": "assistant",
                "content": answer
            })

            return "", new_history

        except Exception as error:

            last_error = error

            error_text = str(error).lower()

            is_temporary_server_error = (
                "503" in error_text
                or "unavailable" in error_text
                or "high demand" in error_text
                or "service unavailable" in error_text
            )

            print(
                f"Gemini attempt {attempt + 1} failed: "
                f"{repr(error)}"
            )

            if not is_temporary_server_error:
                break

    # --------------------------------------------------------
    # Friendly final error
    # --------------------------------------------------------

    print("FINAL GEMINI ERROR:", repr(last_error))

    error_message = (
        "I'm having trouble generating that response right now.\n\n"
        "Please try the question again in a moment."
    )

    new_history = list(history) if history else []

    new_history.append({
        "role": "user",
        "content": message
    })

    new_history.append({
        "role": "assistant",
        "content": error_message
    })

    return "", new_history


# 17. Suggestion button helper

def set_prompt(text):
    return text

# CSS

css = """
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Patrick+Hand&display=swap');
.gradio-container {
    max-width: 1200px !important;
    margin: 0 auto !important;
    background: #fcfbff !important;
    font-family: 'DM Sans', sans-serif !important;
}
body {
    background: #fcfbff !important;
}
#main-card {
    max-width: 950px !important;
    margin: 25px auto !important;
}
#header {
    background: linear-gradient(135deg, #d9e8ff, #e9ddff);
    border-radius: 25px;
    padding: 26px 30px;
    margin-bottom: 18px;
    text-align: center;
}
.brand {
    font-family: 'Patrick Hand', cursive;
    font-size: 42px;
    font-weight: 700;
    color: #282543;
    margin-bottom: 4px;
}
.subtitle {
    font-size: 15px;
    color: #5f5b78;
}
.robot {
    width: 75px;
    height: 75px;
    border-radius: 50%;
    background: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 12px auto;
    font-size: 38px;
    box-shadow: 0 8px 25px rgba(75, 68, 120, 0.12);
}
#welcome {
    text-align: center;
    margin-bottom: 15px;
}
#welcome h2 {
    color: #292741;
    font-size: 24px;
    margin-bottom: 5px;
}
#welcome p {
    color: #77738b;
    font-size: 14px;
}
.suggestion-row {
    display: flex;
    justify-content: center;
    gap: 8px;
    flex-wrap: wrap;
    margin-bottom: 16px;
}
.suggestion button {
    border-radius: 18px !important;
    border: 1px solid #ddd7f4 !important;
    background: #ffffff !important;
    color: #4e4970 !important;
    font-size: 13px !important;
}
.suggestion button:hover {
    background: #f1edff !important;
}
#chatbot {
    border: 1px solid #e7e3f4 !important;
    border-radius: 20px !important;
    background: white !important;
    min-height: 430px !important;
}
.input-row {
    margin-top: 12px;
}
#message-box textarea {
    border-radius: 18px !important;
    border: 1px solid #ddd8ef !important;
    background: white !important;
    min-height: 55px !important;
}
#send-btn button {
    border-radius: 18px !important;
    font-weight: 700 !important;
    min-height: 55px !important;
}
.footer {
    text-align: center;
    color: #9995aa;
    font-size: 12px;
    margin-top: 14px;
}
"""

# Gradio UI

with gr.Blocks() as demo:

    with gr.Column(elem_id="main-card"):

        gr.HTML(
            """
            <div id="header">
                <div class="robot">🤖</div>
                <div class="brand">
                    StudyMate
                </div>
                <div class="subtitle">
                    Your A-Level Mathematics 9709 study buddy
                </div>
            </div>
            """
        )

        gr.HTML(
            """
            <div id="welcome">
                <h2>Hey! What are we learning today?</h2>
                <p>
                    Ask a question, get an explanation, practise,
                    or build a mock paper.
                </p>
            </div>
            """
        )

        with gr.Row(elem_classes="suggestion-row"):

            explain_btn = gr.Button(
                "Explain a concept",
                elem_classes="suggestion"
            )

            solve_btn = gr.Button(
                "Solve a problem",
                elem_classes="suggestion"
            )

            notes_btn = gr.Button(
                "Summarise notes",
                elem_classes="suggestion"
            )

            revision_btn = gr.Button(
                "Give revision tips",
                elem_classes="suggestion"
            )

            ask_btn = gr.Button(
                "Ask a question",
                elem_classes="suggestion"
            )

        chatbot = gr.Chatbot(
            show_label=False,
            elem_id="chatbot",
            height=430
        )

        with gr.Row(elem_classes="input-row"):

            message_box = gr.Textbox(
                show_label=False,
                placeholder="Ask StudyMate anything about A-Level Mathematics 9709...",
                lines=2,
                elem_id="message-box",
                scale=8
            )

            send_button = gr.Button(
                "Send ✦",
                variant="primary",
                elem_id="send-btn",
                scale=1
            )

        gr.HTML(
            """
            <div class="footer">
                StudyMate • Cambridge International A-Level Mathematics 9709
            </div>
            """
        )

    # Suggestion buttons

    explain_btn.click(
        fn=lambda: "Explain the Poisson distribution.",
        outputs=message_box
    )

    solve_btn.click(
        fn=lambda: "Solve this problem step by step: ",
        outputs=message_box
    )

    notes_btn.click(
        fn=lambda: "Make detailed revision notes on ",
        outputs=message_box
    )

    revision_btn.click(
        fn=lambda: "Give me revision tips for A-Level Mathematics 9709.",
        outputs=message_box
    )

    ask_btn.click(
        fn=lambda: "",
        outputs=message_box
    )

    # Send button
   
    send_button.click(
        fn=ask_question,
        inputs=[message_box, chatbot],
        outputs=[message_box, chatbot]
    )

    message_box.submit(
        fn=ask_question,
        inputs=[message_box, chatbot],
        outputs=[message_box, chatbot]
    )



# launch

demo.queue()

demo.launch(
    css=css,
    show_error=True
)
