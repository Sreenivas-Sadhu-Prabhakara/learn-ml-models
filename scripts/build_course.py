#!/usr/bin/env python3
"""Generate the static Bring Your Own Data course pages."""

from html import escape
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[1]


def clean(text: str) -> str:
    return dedent(text).strip()


def code_card(cell: str, title: str, code: str, checkpoint: str = "") -> str:
    receipt = ""
    if checkpoint:
        receipt = f"""
        <div class="checkpoint">
          <span>CHECKPOINT</span>
          <p>{checkpoint}</p>
        </div>
        """
    return f"""
    <div class="codecard">
      <div class="codecard-head">
        <span>{escape(cell)} · {escape(title)}</span>
        <button class="copy" type="button" aria-label="Copy {escape(title)} code">Copy</button>
      </div>
      <pre><code>{escape(clean(code))}</code></pre>
    </div>
    {receipt}
    """


def step(number: str, title: str, intro: str, content: str) -> str:
    return f"""
    <section class="step">
      <span class="step-chip">{escape(number)}</span>
      <h2>{title}</h2>
      {intro}
      {content}
    </section>
    """


def callout(title: str, text: str, kind: str = "") -> str:
    suffix = f" {kind}" if kind else ""
    return f'<div class="callout{suffix}"><h3>{title}</h3>{text}</div>'


def reflection(items: list[str]) -> str:
    questions = "".join(f"<li>{item}</li>" for item in items)
    return f"""
    <div class="reflection">
      <span>PAUSE &amp; WRITE</span>
      <ol>{questions}</ol>
    </div>
    """


def page(
    *,
    slug: str,
    title: str,
    description: str,
    lesson_tag: str,
    eyebrow: str,
    headline: str,
    lede: str,
    chips: list[str],
    body: str,
    previous: tuple[str, str] | None,
    next_page: tuple[str, str] | None,
) -> str:
    prefix = "../"
    chip_html = "".join(f'<span class="chip">{chip}</span>' for chip in chips)
    previous_html = (
        f'<a href="{previous[0]}">← {previous[1]}</a>' if previous else "<span></span>"
    )
    next_html = (
        f'<a href="{next_page[0]}">{next_page[1]} →</a>' if next_page else "<span></span>"
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)} · Learn ML Models</title>
  <meta name="description" content="{escape(description)}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&amp;family=IBM+Plex+Sans:wght@400;500;600&amp;family=IBM+Plex+Serif:wght@500;600&amp;display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{prefix}assets/course.css">
</head>
<body>
  <nav class="topbar" aria-label="Course navigation">
    <div class="topbar-inner">
      <a class="wordmark" href="{prefix}">LEARN<span>·</span>ML<span>·</span>MODELS</a>
      <span class="lesson-tag">{lesson_tag}</span>
    </div>
  </nav>

  <header class="hero wrap">
    <p class="eyebrow">{eyebrow}</p>
    <h1>{headline}</h1>
    <p class="lede">{lede}</p>
    <div class="meta-chips">{chip_html}</div>
  </header>

  <main class="wrap">
    {body}
    <section class="completion-card">
      <div>
        <p class="eyebrow">YOUR PACE, YOUR PROJECT</p>
        <h2>Save your work before moving on.</h2>
        <p>Your result is evidence about your dataset—not a grade. Record what changed, what improved, and what you still do not understand.</p>
      </div>
      <button class="complete-button" type="button" data-complete="{escape(slug)}">Mark complete</button>
    </section>
    <nav class="lesson-nav" aria-label="Previous and next lessons">
      {previous_html}
      {next_html}
    </nav>
  </main>

  <footer>
    <div class="foot-inner">
      <span>Bring your own tabular data. Keep your test set honest.</span>
      <a href="{prefix}">All lessons</a>
    </div>
  </footer>
  <script src="{prefix}assets/course.js"></script>
</body>
</html>
"""


def lesson_card(
    slug: str,
    number: str,
    category: str,
    title: str,
    description: str,
    tags: list[str],
    status: str = "READY",
) -> str:
    tag_html = "".join(f'<span class="tag">{tag}</span>' for tag in tags)
    return f"""
    <a class="lesson-card" href="{slug}/" data-lesson-card="{slug}">
      <div class="card-topline">
        <span>{number} · {category}</span>
        <span class="progress-status" data-progress-for="{slug}">Not started</span>
      </div>
      <h3>{title}</h3>
      <p>{description}</p>
      <div class="lesson-meta"><span class="tag live">{status}</span>{tag_html}</div>
    </a>
    """


CSS = clean(r'''
:root {
  --paper: #f2f5f7;
  --card: #ffffff;
  --ink: #182a3a;
  --muted: #52657a;
  --green: #0e7c52;
  --green-dark: #095c3d;
  --green-soft: #e3f1ea;
  --saffron: #c77c11;
  --saffron-text: #925806;
  --saffron-soft: #f8eedd;
  --blue-soft: #e7eef6;
  --rule: #d9e2ea;
  --code: #0e1b26;
  --code-ink: #d9e6f2;
  --danger: #9b3a32;
}

* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background: var(--paper);
  color: var(--ink);
  font-family: "IBM Plex Sans", system-ui, sans-serif;
  font-size: 17px;
  line-height: 1.65;
}
a { color: var(--green); }
a:focus-visible, button:focus-visible {
  outline: 3px solid var(--saffron);
  outline-offset: 3px;
}
code, pre, .eyebrow, .step-chip, .wordmark, .lesson-tag, .tag,
.card-topline, .progress-status, .codecard-head, .checkpoint span,
.reflection > span {
  font-family: "IBM Plex Mono", monospace;
}

.wrap { max-width: 920px; margin: 0 auto; padding-left: 22px; padding-right: 22px; }
.topbar { background: rgba(255,255,255,.96); border-bottom: 1px solid var(--rule); }
.topbar-inner {
  max-width: 920px;
  margin: 0 auto;
  min-height: 58px;
  padding: 12px 22px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}
.wordmark { color: var(--ink); text-decoration: none; font-size: 13px; font-weight: 600; letter-spacing: .13em; }
.wordmark span { color: var(--green); }
.lesson-tag { color: var(--muted); font-size: 12px; letter-spacing: .08em; text-align: right; }

.hero { padding-top: 62px; padding-bottom: 42px; }
.hero-home { padding-top: 74px; padding-bottom: 34px; }
.eyebrow { margin: 0 0 9px; color: var(--saffron-text); font-size: 12.5px; font-weight: 600; letter-spacing: .14em; text-transform: uppercase; }
h1, h2, h3 { color: var(--ink); }
h1, .display-title { font-family: "IBM Plex Serif", Georgia, serif; }
h1 { max-width: 850px; margin: 0 0 20px; font-size: clamp(38px, 7vw, 62px); line-height: 1.08; letter-spacing: -.02em; }
h2 { margin: 0 0 12px; font-family: "IBM Plex Serif", Georgia, serif; font-size: clamp(25px, 4vw, 34px); line-height: 1.2; }
h3 { margin: 0 0 8px; font-size: 19px; line-height: 1.35; }
p { margin: 0 0 15px; }
.lede { max-width: 68ch; color: var(--muted); font-size: 19px; }
.lede strong { color: var(--ink); }
.meta-chips { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 22px; }
.chip, .tag {
  display: inline-flex;
  align-items: center;
  border: 1px solid var(--rule);
  border-radius: 999px;
  background: var(--card);
  color: var(--muted);
  font-size: 12px;
  padding: 5px 11px;
}

.scope-banner, .start-banner, .completion-card {
  border: 1px solid var(--green);
  border-radius: 16px;
  background: var(--green-soft);
  padding: 24px;
}
.start-banner { display: grid; grid-template-columns: 1fr auto; align-items: center; gap: 22px; margin-bottom: 38px; }
.start-banner h2, .completion-card h2 { font-size: 26px; }
.button, .complete-button {
  display: inline-flex;
  justify-content: center;
  align-items: center;
  min-height: 44px;
  border: 1px solid var(--green);
  border-radius: 9px;
  background: var(--green);
  color: white;
  cursor: pointer;
  font: 600 15px "IBM Plex Sans", sans-serif;
  padding: 10px 17px;
  text-decoration: none;
}
.button:hover, .complete-button:hover { background: var(--green-dark); }
.button.secondary { background: transparent; color: var(--green); }

.section-label { margin: 44px 0 15px; color: var(--muted); font: 600 13px "IBM Plex Mono", monospace; letter-spacing: .12em; text-transform: uppercase; }
.path-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 15px; }
.lesson-card {
  min-height: 245px;
  border: 1px solid var(--rule);
  border-radius: 15px;
  background: var(--card);
  color: var(--ink);
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 23px;
  text-decoration: none;
  transition: transform .15s ease, box-shadow .15s ease;
}
.lesson-card:hover { transform: translateY(-2px); box-shadow: 0 8px 22px rgba(24,42,58,.08); }
.lesson-card h3 { font-family: "IBM Plex Serif", Georgia, serif; font-size: 25px; }
.lesson-card p { color: var(--muted); font-size: 15.5px; }
.card-topline { display: flex; justify-content: space-between; gap: 12px; color: var(--saffron-text); font-size: 11.5px; font-weight: 600; letter-spacing: .06em; }
.progress-status { color: var(--muted); text-align: right; }
.progress-status.done { color: var(--green); }
.lesson-meta { display: flex; flex-wrap: wrap; gap: 7px; margin-top: auto; }
.tag.live { border-color: var(--green); background: var(--green-soft); color: var(--green); font-weight: 600; }
.lesson-card.soon { border-style: dashed; background: transparent; pointer-events: none; }

.course-rules, .decision-grid, .idea-grid { display: grid; gap: 14px; }
.course-rules { grid-template-columns: repeat(3, minmax(0, 1fr)); margin: 42px 0 64px; }
.rule-card, .decision-card, .idea-card {
  border: 1px solid var(--rule);
  border-radius: 13px;
  background: var(--card);
  padding: 20px;
}
.rule-card strong { display: block; margin-bottom: 7px; color: var(--green); }
.rule-card p, .decision-card p, .idea-card p { margin: 0; color: var(--muted); font-size: 15px; }
.decision-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); margin: 20px 0; }
.decision-card.selected { border-color: var(--green); background: var(--green-soft); }
.idea-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); margin: 20px 0; }

.step { margin: 0 0 28px; border: 1px solid var(--rule); border-radius: 16px; background: var(--card); padding: 27px; }
.step-chip { display: inline-block; margin-bottom: 12px; color: var(--saffron-text); font-size: 12px; font-weight: 600; letter-spacing: .1em; }
.step ul, .step ol { padding-left: 24px; }
.step li { margin-bottom: 7px; }
.step code:not(pre code) { border-radius: 5px; background: var(--blue-soft); padding: 1px 5px; font-size: .88em; }

.codecard { overflow: hidden; margin-top: 20px; border: 1px solid #24394a; border-radius: 11px; background: var(--code); }
.codecard-head { min-height: 44px; border-bottom: 1px solid #294153; display: flex; align-items: center; justify-content: space-between; gap: 16px; color: #9eb0bf; font-size: 11.5px; letter-spacing: .08em; padding: 8px 13px 8px 17px; }
.copy { border: 1px solid #506779; border-radius: 6px; background: transparent; color: #d9e6f2; cursor: pointer; font: 500 12px "IBM Plex Mono", monospace; padding: 6px 10px; }
.copy.done { border-color: #63c39e; color: #7ce0ba; }
pre { margin: 0; overflow-x: auto; color: var(--code-ink); font-size: 13.5px; line-height: 1.62; padding: 19px; tab-size: 4; }

.checkpoint { margin: 12px 0 0; border-left: 4px solid var(--green); background: var(--green-soft); padding: 13px 16px; }
.checkpoint span { color: var(--green); font-size: 11px; font-weight: 600; letter-spacing: .1em; }
.checkpoint p { margin: 4px 0 0; font-size: 14.5px; }
.callout { margin: 20px 0; border-left: 4px solid var(--saffron); background: var(--saffron-soft); padding: 18px 20px; }
.callout.green { border-color: var(--green); background: var(--green-soft); }
.callout.danger { border-color: var(--danger); background: #faecea; }
.callout p:last-child { margin-bottom: 0; }
.reflection { margin: 22px 0 0; border: 1px dashed var(--saffron); border-radius: 10px; background: #fffaf1; padding: 18px 20px; }
.reflection > span { color: var(--saffron-text); font-size: 11.5px; font-weight: 600; letter-spacing: .1em; }
.reflection ol { margin-bottom: 0; }

.tablewrap { overflow-x: auto; margin: 18px 0; }
table { width: 100%; border-collapse: collapse; background: var(--card); font-size: 15px; }
th, td { border: 1px solid var(--rule); padding: 12px 14px; text-align: left; vertical-align: top; }
th { background: var(--blue-soft); font-weight: 600; }
details { margin: 14px 0; border: 1px solid var(--rule); border-radius: 10px; background: var(--card); padding: 14px 17px; }
summary { cursor: pointer; font-weight: 600; }
details > *:not(summary) { margin-top: 12px; }

.completion-card { display: grid; grid-template-columns: 1fr auto; align-items: center; gap: 24px; margin: 46px 0 22px; }
.complete-button.is-done { background: var(--card); color: var(--green); }
.lesson-nav { display: flex; justify-content: space-between; gap: 18px; margin: 22px 0 64px; }
.lesson-nav a { font-weight: 600; text-decoration: none; }
footer { border-top: 1px solid var(--rule); background: var(--card); color: var(--muted); font-size: 14px; padding: 25px 0 42px; }
.foot-inner { max-width: 920px; margin: 0 auto; padding: 0 22px; display: flex; justify-content: space-between; gap: 20px; }

@media (max-width: 720px) {
  body { font-size: 16px; }
  .hero { padding-top: 44px; }
  .path-grid, .course-rules, .decision-grid, .idea-grid { grid-template-columns: 1fr; }
  .start-banner, .completion-card { grid-template-columns: 1fr; }
  .lesson-card { min-height: 0; }
  .step { padding: 21px 18px; }
  .lesson-tag { max-width: 45%; }
  .foot-inner { flex-direction: column; }
}

@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  * { transition: none !important; }
}
''')


JS = clean(r'''
(function () {
  document.querySelectorAll('.codecard').forEach(function (card) {
    var button = card.querySelector('.copy');
    var code = card.querySelector('code');
    if (!button || !code) return;

    button.addEventListener('click', function () {
      var text = code.innerText;
      function finished() {
        button.textContent = 'Copied ✓';
        button.classList.add('done');
        window.setTimeout(function () {
          button.textContent = 'Copy';
          button.classList.remove('done');
        }, 1600);
      }

      function fallback() {
        var area = document.createElement('textarea');
        area.value = text;
        area.setAttribute('readonly', '');
        area.style.position = 'fixed';
        area.style.opacity = '0';
        document.body.appendChild(area);
        area.select();
        document.execCommand('copy');
        area.remove();
        finished();
      }

      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(finished, fallback);
      } else {
        fallback();
      }
    });
  });

  var storagePrefix = 'learn-ml-models:';

  function readStatus(slug) {
    try { return window.localStorage.getItem(storagePrefix + slug) === 'done'; }
    catch (error) { return false; }
  }

  function writeStatus(slug, done) {
    try {
      if (done) window.localStorage.setItem(storagePrefix + slug, 'done');
      else window.localStorage.removeItem(storagePrefix + slug);
    } catch (error) {}
  }

  document.querySelectorAll('[data-complete]').forEach(function (button) {
    var slug = button.getAttribute('data-complete');
    function paint() {
      var done = readStatus(slug);
      button.textContent = done ? 'Completed ✓' : 'Mark complete';
      button.classList.toggle('is-done', done);
      button.setAttribute('aria-pressed', done ? 'true' : 'false');
    }
    button.addEventListener('click', function () {
      writeStatus(slug, !readStatus(slug));
      paint();
    });
    paint();
  });

  var lessonSlugs = ['start', 'knn', 'linear-regression', 'logistic-regression',
    'decision-trees', 'random-forests', 'gradient-boosting'];

  document.querySelectorAll('[data-progress-for]').forEach(function (label) {
    var slug = label.getAttribute('data-progress-for');
    var done = readStatus(slug);
    label.textContent = done ? 'Completed ✓' : 'Not started';
    label.classList.toggle('done', done);
  });

  document.querySelectorAll('[data-course-progress]').forEach(function (label) {
    var completed = lessonSlugs.filter(readStatus).length;
    label.textContent = completed + ' of ' + lessonSlugs.length + ' complete';
  });
})();
''')


HOME = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Learn ML Models · Bring Your Own Data</title>
  <meta name="description" content="A self-paced machine-learning course where you upload your own tabular dataset, define your own prediction problem, and learn one model at a time in Google Colab.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&amp;family=IBM+Plex+Sans:wght@400;500;600&amp;family=IBM+Plex+Serif:wght@500;600&amp;display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/course.css">
</head>
<body>
  <nav class="topbar" aria-label="Course navigation">
    <div class="topbar-inner">
      <a class="wordmark" href="./">LEARN<span>·</span>ML<span>·</span>MODELS</a>
      <span class="lesson-tag" data-course-progress>0 of 7 complete</span>
    </div>
  </nav>

  <header class="hero hero-home wrap">
    <p class="eyebrow">A bring-your-own-data course</p>
    <h1>Bring your dataset.<br>Learn the model.</h1>
    <p class="lede">You choose the question, target, features, and definition of success. The course gives you a reusable workflow in <strong>Google Colab</strong>, then helps you understand one model at a time—without prescribing one “correct” score.</p>
  </header>

  <main class="wrap">
    <section class="start-banner">
      <div>
        <p class="eyebrow">Required first stop</p>
        <h2>Turn your file into an honest ML experiment.</h2>
        <p>Frame the prediction problem, upload a CSV or Excel file, choose a realistic split, prepare mixed data safely, and build a baseline.</p>
      </div>
      <a class="button" href="start/">Start here →</a>
    </section>

    <div class="scope-banner">
      <h3>This course has a clear boundary</h3>
      <p>It is designed for <strong>tabular data</strong>: rows and columns in CSV or Excel, with one target column for supervised learning. If you have no target, the upcoming K-Means path will help. Images, raw text, audio, and forecasting need different workflows.</p>
    </div>

    <p class="section-label">Choose the next model that fits your task</p>
    <div class="path-grid">
      {lesson_card('start', 'START', 'FOUNDATION', 'Your problem, your data', 'Define what one row means, choose the target and features, upload your file, split honestly, and create the baseline every model must beat.', ['classification', 'regression', '~35 min'])}
      {lesson_card('knn', '01', 'CLASSIFICATION + REGRESSION', 'K-Nearest Neighbours', 'Predict from the most similar training rows. Learn why scaling matters and tune the number of neighbours with cross-validation.', ['both tasks', 'scaling', '~30 min'])}
      {lesson_card('linear-regression', '02', 'REGRESSION', 'Linear Regression', 'Predict a number with a weighted formula. Inspect coefficients, residuals, Ridge, Lasso, and the danger of target leakage.', ['numeric target', 'interpretable', '~35 min'])}
      {lesson_card('logistic-regression', '03', 'CLASSIFICATION', 'Logistic Regression', 'Predict a class and estimated probabilities. Inspect weights and learn why probability is not the same as certainty.', ['categorical target', 'probabilities', '~30 min'])}
      {lesson_card('decision-trees', '04', 'CLASSIFICATION + REGRESSION', 'Decision Trees', 'Let the model learn a sequence of yes/no questions, then control depth before memorisation takes over.', ['both tasks', 'no scaling', '~30 min'])}
      {lesson_card('random-forests', '05', 'CLASSIFICATION + REGRESSION', 'Random Forests', 'Combine many varied trees, tune on training folds, and measure feature importance without confusing association for cause.', ['both tasks', 'ensemble', '~30 min'])}
      {lesson_card('gradient-boosting', '06', 'CLASSIFICATION + REGRESSION', 'Gradient Boosting', 'Build trees in sequence so each round corrects earlier mistakes, then compare every suitable model in your own results log.', ['both tasks', 'ensemble', '~35 min'])}
      <div class="lesson-card soon" aria-disabled="true">
        <div class="card-topline"><span>07 · UNSUPERVISED</span><span>Coming soon</span></div>
        <h3>K-Means</h3>
        <p>No target column? Discover groups in your rows and learn how to judge clusters without a hidden answer sheet.</p>
        <div class="lesson-meta"><span class="tag">NO TARGET NEEDED</span></div>
      </div>
    </div>

    <section class="course-rules" aria-label="How the course works">
      <div class="rule-card"><strong>1 · Keep one notebook</strong><p>Build the foundation once, then append each model lesson. If Colab resets, use Runtime → Run all.</p></div>
      <div class="rule-card"><strong>2 · Expect different scores</strong><p>Your output is not supposed to match anyone else's. Compare against your baseline and the cost of mistakes.</p></div>
      <div class="rule-card"><strong>3 · Test once</strong><p>Choose dials with cross-validation on training data. The held-out test set is the final exam, not a practice sheet.</p></div>
    </section>
  </main>

  <footer>
    <div class="foot-inner">
      <span>Learn at your pace, on a problem you care about.</span>
      <a href="https://github.com/Sreenivas-Sadhu-Prabhakara/learn-ml-models">Source on GitHub</a>
    </div>
  </footer>
  <script src="assets/course.js"></script>
</body>
</html>
"""


UPLOAD_CODE = r'''
from google.colab import files
import io
import pandas as pd
import numpy as np

uploaded = files.upload()

if len(uploaded) != 1:
    raise ValueError("Please upload exactly one CSV or Excel file.")

file_name, file_bytes = next(iter(uploaded.items()))
lower_name = file_name.lower()

if lower_name.endswith(".csv"):
    df = pd.read_csv(io.BytesIO(file_bytes))
elif lower_name.endswith((".xlsx", ".xls")):
    df = pd.read_excel(io.BytesIO(file_bytes))
else:
    raise ValueError("Please upload a .csv, .xlsx, or .xls file.")

print(f"Loaded: {file_name}")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")
display(df.head())
'''


CONFIG_CODE = r'''
# Explain the project before configuring the model.
ROW_MEANING = "One row represents ..."
PREDICTION_GOAL = "I want to predict ..."
COSTLY_MISTAKE = "The most costly wrong prediction would be ..."

# Choose the task and columns from your uploaded file.
TASK = "classification"       # "classification" or "regression"
TARGET = "replace_with_your_target_column"
FEATURES = [
    "replace_with_a_feature_column",
    # "add_more_feature_columns",
]

# Choose the split that imitates how new data will arrive.
SPLIT_MODE = "random"         # "random", "time", or "group"
TIME_COLUMN = None             # example: "event_date"
GROUP_COLUMN = None            # example: "customer_id"
TEST_SIZE = 0.25
RANDOM_STATE = 42
'''


AUDIT_CODE = r'''
if TASK not in {"classification", "regression"}:
    raise ValueError("TASK must be 'classification' or 'regression'.")

if not 0 < TEST_SIZE < 1:
    raise ValueError("TEST_SIZE must be a number between 0 and 1.")

if TARGET not in df.columns:
    raise ValueError(f"TARGET '{TARGET}' is not a column in your file.")

if not FEATURES:
    raise ValueError("Choose at least one feature.")

if len(FEATURES) != len(set(FEATURES)):
    raise ValueError("Each feature should appear only once in FEATURES.")

if TARGET in FEATURES:
    raise ValueError("Remove TARGET from FEATURES. The answer cannot be a clue.")

extra_columns = [
    column for column in (TIME_COLUMN, GROUP_COLUMN)
    if column is not None
]
required_columns = list(dict.fromkeys(FEATURES + [TARGET] + extra_columns))
missing_columns = [column for column in required_columns if column not in df.columns]

if missing_columns:
    raise ValueError(f"These configured columns do not exist: {missing_columns}")

model_data = df[required_columns].dropna(subset=[TARGET]).copy()

if TASK == "regression":
    model_data[TARGET] = pd.to_numeric(model_data[TARGET], errors="raise")
    if not np.isfinite(model_data[TARGET]).all():
        raise ValueError("A regression target cannot contain infinity.")
elif model_data[TARGET].nunique() < 2:
    raise ValueError("Classification needs at least two target classes.")

numeric_input_features = model_data[FEATURES].select_dtypes(
    include="number"
).columns.tolist()
infinite_counts = np.isinf(model_data[numeric_input_features]).sum()
infinite_counts = infinite_counts[infinite_counts > 0]
if not infinite_counts.empty:
    print("Treating these infinite feature values as missing:")
    display(infinite_counts.to_frame("infinite_values"))
    model_data[numeric_input_features] = model_data[
        numeric_input_features
    ].replace([np.inf, -np.inf], np.nan)

print("One row:", ROW_MEANING)
print("Goal:", PREDICTION_GOAL)
print("Costly mistake:", COSTLY_MISTAKE)
print("Usable rows:", len(model_data))

profile = pd.DataFrame({
    "dtype": model_data[FEATURES].dtypes.astype(str),
    "missing": model_data[FEATURES].isna().sum(),
    "unique_values": model_data[FEATURES].nunique(dropna=True),
})
display(profile)

if TASK == "classification":
    target_profile = pd.DataFrame({
        "rows": model_data[TARGET].value_counts(dropna=False),
        "share": model_data[TARGET].value_counts(normalize=True, dropna=False),
    })
    display(target_profile)
else:
    display(model_data[TARGET].describe().to_frame("target"))

possible_identifiers = []
for column in FEATURES:
    name_looks_like_id = "id" in column.lower().replace("-", "_").split("_")
    mostly_unique_text = (
        not pd.api.types.is_numeric_dtype(model_data[column])
        and model_data[column].nunique(dropna=True) > 0.5 * len(model_data)
    )
    if name_looks_like_id or mostly_unique_text:
        possible_identifiers.append(column)

if possible_identifiers:
    print("Review these possible identifier/high-cardinality columns:", possible_identifiers)
'''


SPLIT_CODE = r'''
from sklearn.model_selection import train_test_split, GroupShuffleSplit

if SPLIT_MODE == "random":
    stratify = None
    if TASK == "classification":
        class_counts = model_data[TARGET].value_counts()
        if class_counts.min() >= 2:
            stratify = model_data[TARGET]

    train_rows, test_rows = train_test_split(
        model_data,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=stratify,
    )

elif SPLIT_MODE == "time":
    if not TIME_COLUMN:
        raise ValueError("Set TIME_COLUMN before using a time split.")

    if model_data[TIME_COLUMN].isna().any():
        raise ValueError(
            f"TIME_COLUMN '{TIME_COLUMN}' contains missing values. "
            "Fill or remove them before splitting."
        )

    model_data[TIME_COLUMN] = pd.to_datetime(
        model_data[TIME_COLUMN], errors="raise"
    )
    ordered = model_data.sort_values(TIME_COLUMN)
    split_at = int(len(ordered) * (1 - TEST_SIZE))

    if split_at < 1 or split_at >= len(ordered):
        raise ValueError("TEST_SIZE leaves an empty train or test set.")

    # Keep identical timestamps on the same side of the boundary.
    test_start_time = ordered.iloc[split_at][TIME_COLUMN]
    train_rows = ordered[ordered[TIME_COLUMN] < test_start_time]
    test_rows = ordered[ordered[TIME_COLUMN] >= test_start_time]

    if train_rows.empty or test_rows.empty:
        raise ValueError(
            "The time boundary leaves an empty train or test set. "
            "Choose a different TEST_SIZE or review the timestamp values."
        )

elif SPLIT_MODE == "group":
    if not GROUP_COLUMN:
        raise ValueError("Set GROUP_COLUMN before using a group split.")

    if model_data[GROUP_COLUMN].isna().any():
        raise ValueError(
            f"GROUP_COLUMN '{GROUP_COLUMN}' contains missing values. "
            "Fill or remove them before splitting."
        )

    if model_data[GROUP_COLUMN].nunique() < 2:
        raise ValueError("A group split needs at least two distinct groups.")

    splitter = GroupShuffleSplit(
        n_splits=1,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
    )
    train_index, test_index = next(
        splitter.split(model_data, groups=model_data[GROUP_COLUMN])
    )
    train_rows = model_data.iloc[train_index]
    test_rows = model_data.iloc[test_index]

else:
    raise ValueError("SPLIT_MODE must be 'random', 'time', or 'group'.")

X_train = train_rows[FEATURES].copy()
X_test = test_rows[FEATURES].copy()
y_train = train_rows[TARGET].copy()
y_test = test_rows[TARGET].copy()

if TASK == "classification" and y_train.nunique() < 2:
    raise ValueError(
        "The training split contains fewer than two classes. "
        "Use more data or choose a different valid split."
    )

print("Training rows:", len(X_train))
print("Testing rows: ", len(X_test))
print("Split mode:   ", SPLIT_MODE)

if SPLIT_MODE == "time":
    print("Train ends:", train_rows[TIME_COLUMN].max())
    print("Test starts:", test_rows[TIME_COLUMN].min())
elif SPLIT_MODE == "group":
    overlap = set(train_rows[GROUP_COLUMN]) & set(test_rows[GROUP_COLUMN])
    print("Groups shared across train and test:", len(overlap))
'''


PREPROCESS_CODE = r'''
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

numeric_features = X_train.select_dtypes(include="number").columns.tolist()
categorical_features = [
    column for column in FEATURES
    if column not in numeric_features
]

print("Numeric features:", numeric_features)
print("Categorical features:", categorical_features)

high_cardinality = [
    column for column in categorical_features
    if X_train[column].nunique(dropna=True) > 100
]
if high_cardinality:
    print("Review high-cardinality features before continuing:", high_cardinality)

def make_encoder():
    try:
        return OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    except TypeError:  # Compatibility with older scikit-learn versions
        return OneHotEncoder(handle_unknown="ignore", sparse=False)

def make_preprocessor(scale_numeric=False):
    transformers = []

    if numeric_features:
        numeric_steps = [
            ("fill_missing", SimpleImputer(strategy="median")),
        ]
        if scale_numeric:
            numeric_steps.append(("scale", StandardScaler()))

        transformers.append((
            "numeric",
            Pipeline(numeric_steps),
            numeric_features,
        ))

    if categorical_features:
        categorical_steps = Pipeline([
            ("fill_missing", SimpleImputer(strategy="most_frequent")),
            ("encode", make_encoder()),
        ])
        transformers.append((
            "categorical",
            categorical_steps,
            categorical_features,
        ))

    return ColumnTransformer(
        transformers,
        remainder="drop",
        verbose_feature_names_out=False,
    )
'''


EVALUATION_CODE = r'''
import matplotlib.pyplot as plt
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
    ConfusionMatrixDisplay,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.model_selection import (
    GroupKFold,
    KFold,
    StratifiedKFold,
    TimeSeriesSplit,
)

results_log = []

# Pass this dictionary into every cross-validation search's fit() call.
# Group labels are needed while folds are constructed, but are never features.
CV_FIT_PARAMS = (
    {"groups": train_rows[GROUP_COLUMN].to_numpy()}
    if SPLIT_MODE == "group"
    else {}
)

def make_cv():
    if SPLIT_MODE == "time":
        folds = min(5, len(y_train) - 1)
        if folds < 2:
            raise ValueError(
                "Time-based CV needs at least three training rows."
            )
        return TimeSeriesSplit(n_splits=folds)

    if SPLIT_MODE == "group":
        groups = train_rows[GROUP_COLUMN]
        folds = min(5, groups.nunique())
        if folds < 2:
            raise ValueError(
                "Group-based CV needs at least two training groups."
            )
        return GroupKFold(n_splits=folds)

    if TASK == "classification":
        folds = min(5, int(y_train.value_counts().min()))
        if folds < 2:
            raise ValueError("Every class needs at least two training rows for CV.")
        return StratifiedKFold(
            n_splits=folds,
            shuffle=True,
            random_state=RANDOM_STATE,
        )

    folds = min(5, len(y_train))
    if folds < 2:
        raise ValueError("Regression needs at least two training rows for CV.")
    return KFold(
        n_splits=folds,
        shuffle=True,
        random_state=RANDOM_STATE,
    )

PRIMARY_SCORING = (
    "balanced_accuracy" if TASK == "classification"
    else "neg_mean_absolute_error"
)

def evaluate_predictions(name, y_true, y_pred, show_details=True):
    if TASK == "classification":
        row = {
            "model": name,
            "accuracy": accuracy_score(y_true, y_pred),
            "balanced_accuracy": balanced_accuracy_score(y_true, y_pred),
            "macro_f1": f1_score(
                y_true, y_pred, average="macro", zero_division=0
            ),
        }
    else:
        row = {
            "model": name,
            "MAE": mean_absolute_error(y_true, y_pred),
            "RMSE": np.sqrt(mean_squared_error(y_true, y_pred)),
            "R2": r2_score(y_true, y_pred),
        }

    results_log[:] = [item for item in results_log if item["model"] != name]
    results_log.append(row)
    display(pd.DataFrame(results_log))

    if show_details and TASK == "classification":
        print(classification_report(y_true, y_pred, zero_division=0))
        ConfusionMatrixDisplay.from_predictions(
            y_true, y_pred, xticks_rotation=45
        )
        plt.show()

    return row

dummy_train = np.zeros((len(y_train), 1))
dummy_test = np.zeros((len(y_test), 1))

if TASK == "classification":
    baseline_model = DummyClassifier(strategy="most_frequent")
else:
    baseline_model = DummyRegressor(strategy="mean")

baseline_model.fit(dummy_train, y_train)
baseline_predictions = baseline_model.predict(dummy_test)
evaluate_predictions("Baseline", y_test, baseline_predictions, show_details=False)
'''


START_BODY = f"""
<section class="scope-banner">
  <h3>Do not start by choosing a model</h3>
  <p>Start by defining what one row represents, what must be predicted, what information will exist at prediction time, and which mistake costs more. Those choices determine the target, features, split, and metric.</p>
</section>

<section class="step">
  <span class="step-chip">DECISION 1</span>
  <h2>Which learning path fits your target?</h2>
  <div class="decision-grid">
    <div class="decision-card"><h3>Classification</h3><p>The target is a category: approved/declined, species, status, segment, or another finite label.</p></div>
    <div class="decision-card"><h3>Regression</h3><p>The target is a measured number: time, amount, demand, score, temperature, or another continuous quantity.</p></div>
    <div class="decision-card"><h3>No target</h3><p>You have no answer column. This supervised path is not the right one; use the upcoming clustering path.</p></div>
  </div>
</section>

<section class="step">
  <span class="step-chip">DECISION 2</span>
  <h2>Choose an exam that resembles reality</h2>
  <div class="decision-grid">
    <div class="decision-card"><h3>Random</h3><p>Use when rows are independent and future rows come from the same process as past rows.</p></div>
    <div class="decision-card"><h3>Time</h3><p>Use when the real job predicts later events from earlier events. Training must come before testing.</p></div>
    <div class="decision-card"><h3>Group</h3><p>Use when the same person, device, company, patient, or case can appear in several rows.</p></div>
  </div>
  {callout('Why this matters', '<p>A random split can leak information when related rows land on both sides. A high score from the wrong exam is worse than a modest score from the right one.</p>', 'danger')}
</section>

{step('CELL 1 OF 6', 'Upload your data into Colab', '<p>Open a new Colab notebook and keep it for the whole course. Upload one CSV or Excel file; the code reads the uploaded bytes directly.</p>', code_card('CELL 1', 'UPLOAD + LOAD', UPLOAD_CODE, 'You should see your own file name, row count, column count, and first five rows. There is no course-wide expected number.'))}

{step('CELL 2 OF 6', 'Write your project card', '<p>Replace every placeholder. Feature selection is deliberately explicit: automatic “use everything” code would quietly include IDs, future information, or the answer under another name.</p>', code_card('CELL 2', 'PROJECT CONFIGURATION', CONFIG_CODE, 'Read the three sentences aloud. If the goal or costly mistake still sounds vague, pause before modelling.'))}

{step('CELL 3 OF 6', 'Validate and inspect before modelling', '<p>This cell catches missing configuration, removes rows with no target, profiles feature types and missingness, and flags possible identifiers. A warning is a prompt to think, not an automatic deletion.</p>', code_card('CELL 3', 'DATA AUDIT', AUDIT_CODE, 'Explain the target distribution and name any feature that might leak the answer or identify a row rather than describe it.'))}

{callout('Keep the real class distribution', '<p>Do not force every classification dataset to be 50/50. Preserve the distribution by default, use stratification where possible, and inspect balanced accuracy and macro-F1 alongside accuracy. Class weights or resampling can help when the costs justify them, but they belong inside training folds—never in the held-out test set.</p>', 'green')}

{step('CELL 4 OF 6', 'Create the honest train/test split', '<p>The learner—not the library—chooses the split mode. Classification uses stratification when possible; time and group modes protect their real-world boundaries.</p>', code_card('CELL 4', 'TRAIN / TEST SPLIT', SPLIT_CODE, 'Training rows plus testing rows should equal the usable rows. A group split should report zero shared groups. A time split should put all test dates after the training boundary.'))}

{step('CELL 5 OF 6', 'Prepare mixed data without leakage', '<p>The reusable preprocessor learns medians, categories, encodings, and scales from the training fold only. Numeric and categorical columns can coexist; unseen categories are handled safely.</p>', code_card('CELL 5', 'PREPROCESSOR FACTORY', PREPROCESS_CODE, 'Review the detected numeric and categorical lists. Raw dates, free text, and high-cardinality labels usually need deliberate feature engineering before continuing.'))}

{step('CELL 6 OF 6', 'Build the baseline and results log', '<p>A baseline is the simplest defensible strategy: always predict the most frequent training class or the training mean. Every later model will be measured against it using the same held-out rows. The cross-validation helper also preserves your random, time, or group boundary while models are tuned; model lessons pass <code>**CV_FIT_PARAMS</code> when fitting each search.</p>', code_card('CELL 6', 'EVALUATION + BASELINE', EVALUATION_CODE, 'Your baseline score is not supposed to be 50%. Record what it reveals about class imbalance or target variation.'))}

<section class="step">
  <span class="step-chip">FOUNDATION COMPLETE</span>
  <h2>Keep this notebook</h2>
  <p>Each model lesson adds cells beneath these six. If Colab disconnects, choose <strong>Runtime → Run all</strong> to rebuild the variables. Do not create a new train/test split for each model; a fair comparison requires the same exam.</p>
  {reflection([
      'What information will genuinely be available when this prediction is made?',
      'Which wrong prediction is more expensive, and does your chosen metric reflect that?',
      'What would make a result suspiciously good?',
  ])}
</section>
"""


START_PAGE = page(
    slug="start",
    title="Start with Your Problem",
    description="Upload your own tabular dataset, frame a prediction task, split it honestly, prepare mixed columns, and build a baseline in Google Colab.",
    lesson_tag="START / FOUNDATION",
    eyebrow="Start here · before every model",
    headline="Make the course yours.",
    lede="Bring one tabular dataset and one question you care about. You will turn them into a reusable, leakage-safe Colab workflow—then keep the same notebook and swap models one lesson at a time.",
    chips=["CSV or Excel", "classification or regression", "~35 minutes"],
    body=START_BODY,
    previous=("../", "Course home"),
    next_page=("../knn/", "Lesson 01 · KNN"),
)


README = clean('''
# Learn ML Models

A self-paced, bring-your-own-data machine-learning course for tabular CSV and
Excel datasets. Learners define their own prediction problem, upload their own
file in Google Colab, choose a realistic split, build a baseline, and then add
one model at a time to the same notebook.

**Course site:** https://sreenivas-sadhu-prabhakara.github.io/learn-ml-models/

## Learning path

| # | Lesson | Supported tasks |
|---|---|---|
| Start | Problem framing, upload, audit, split, preprocessing, baseline | Classification + regression |
| 01 | K-Nearest Neighbours | Classification + regression |
| 02 | Linear Regression, Ridge, and Lasso | Regression |
| 03 | Logistic Regression | Classification |
| 04 | Decision Trees | Classification + regression |
| 05 | Random Forests | Classification + regression |
| 06 | Gradient Boosting and the learner's results table | Classification + regression |
| 07 | K-Means | Coming soon · unsupervised |

## Course principles

- Learners select `TARGET`, `FEATURES`, and the task explicitly.
- Data is uploaded into Colab; no course dataset or fixed output is required.
- Random, time-based, and group-based train/test splits are supported.
- Missing numeric and categorical values are handled inside scikit-learn
  pipelines, so preprocessing is learned from training data only.
- Every model is compared with a problem-appropriate dummy baseline.
- Hyperparameters are selected with cross-validation on training data. The
  held-out test set is used as the final exam.
- Model searches call `.fit(X_train, y_train, **CV_FIT_PARAMS)` so grouped
  cross-validation receives group labels without using them as model features.
- “What you should see” means a structural checkpoint or interpretation
  question, not an exact score.

## Scope

The course covers supervised learning on tabular rows and columns. Images, raw
text, audio, and forecasting need specialised workflows. Datasets without a
target belong to the upcoming clustering path.

## Repository layout

```text
index.html                    course home
start/                        shared bring-your-own-data foundation
knn/                          Lesson 01
linear-regression/            Lesson 02
logistic-regression/          Lesson 03
decision-trees/               Lesson 04
random-forests/               Lesson 05
gradient-boosting/            Lesson 06
assets/                       shared design and course interactions
scripts/build_course.py       static page generator
```

## Rebuilding the static pages

Run `python3 scripts/build_course.py`. The generator writes the shared assets,
home page, and foundation page. Model lesson pages are maintained in their own
directories and are not overwritten by this script.
''')


# The live pages under the repo root are hand-tuned for readability and are the
# source of truth. This generator now writes into scripts/preview/ only, so it
# can be used as a scaffold reference without ever clobbering the live course.
PREVIEW = "scripts/preview"


def write(relative: str, content: str) -> None:
    destination = ROOT / PREVIEW / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    lines = (line.rstrip() for line in content.rstrip().splitlines())
    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build() -> None:
    write("assets/course.css", CSS)
    write("assets/course.js", JS)
    write("index.html", HOME)
    write("start/index.html", START_PAGE)
    write("README.md", README)


if __name__ == "__main__":
    build()
    print(f"Wrote scaffold reference into {PREVIEW}/ (live pages untouched).")
