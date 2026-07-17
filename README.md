# Learn ML Models

Hands-on machine learning lessons for friends learning together — plain language, real Indian stock-market data, and copyable code you paste into your own Google Colab notebook, one cell at a time.

**Course site:** https://sreenivas-sadhu-prabhakara.github.io/learn-ml-models/

## Lessons

| # | Model | Status | Guide |
|---|-------|--------|-------|
| 01 | K-Nearest Neighbours | ✅ Ready | [Step-by-step guide](https://sreenivas-sadhu-prabhakara.github.io/learn-ml-models/knn/) |
| 02 | Linear Regression (two practical examples, feature engineering, Ridge L2, Lasso L1) | ✅ Ready | [Step-by-step guide](https://sreenivas-sadhu-prabhakara.github.io/learn-ml-models/linear-regression/) |
| 03 | Logistic Regression | ✅ Ready | [Step-by-step guide](https://sreenivas-sadhu-prabhakara.github.io/learn-ml-models/logistic-regression/) |
| 04 | Decision Trees | ✅ Ready | [Step-by-step guide](https://sreenivas-sadhu-prabhakara.github.io/learn-ml-models/decision-trees/) |
| 05 | Random Forests | ✅ Ready | [Step-by-step guide](https://sreenivas-sadhu-prabhakara.github.io/learn-ml-models/random-forests/) |
| 06 | Gradient Boosting (+ course leaderboard finale) | ✅ Ready | [Step-by-step guide](https://sreenivas-sadhu-prabhakara.github.io/learn-ml-models/gradient-boosting/) |
| 07 | K-Means | 🔜 Coming soon | — |

## How the lessons work

Each lesson is a single web page of numbered steps. Every step has a copyable code cell and a "what you should see" slip showing the exact expected output (verified by actually running the code). Learners open a fresh notebook at [colab.research.google.com](https://colab.research.google.com), paste each cell, and run it — no installs, no downloads, no uploads.

## The dataset

`data/india_bulk_block_deals.csv` — 119,156 real bulk & block deals from the Indian exchanges (NSE & BSE, 2020 → July 2026): date, symbol, deal type (BULK/BLOCK), side (BUY/SELL), quantity, price, and trade value in ₹ crore. The code cells load it directly from this repo's raw URL.

## Repo layout

```
index.html                     → course home page (GitHub Pages)
knn/                           → Lesson 01 · K-Nearest Neighbours
linear-regression/             → Lesson 02 · Linear Regression, feature engineering, Ridge & Lasso
logistic-regression/           → Lesson 03 · Logistic Regression
decision-trees/                → Lesson 04 · Decision Trees
random-forests/                → Lesson 05 · Random Forests
gradient-boosting/             → Lesson 06 · Gradient Boosting + course leaderboard
data/                          → the shared dataset
```

Lessons 03–06 use the identical balanced BULK/BLOCK split as Lesson 01 (`random_state=42`, 75/25), so every model's score is directly comparable. The course leaderboard in Lesson 06: Random Forest 83.8% · Decision Tree (unlimited) 83.0% · Gradient Boosting 80.4% · KNN 79.8% · Decision Tree (depth 3) 78.7% · Logistic Regression 75.3% · coin flip 50%.

## Adding a lesson

1. Create `<lesson>/index.html` following the design system in `knn/index.html`, with copyable cells and receipts.
2. Run every code cell locally and paste the exact outputs into the receipts (`random_state=42` everywhere so everyone gets identical results).
3. Link it from `index.html` and this README.
