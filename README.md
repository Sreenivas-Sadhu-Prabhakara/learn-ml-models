# Learn ML Models

Hands-on machine learning lessons for friends learning together — plain language, real Indian stock-market data, and copyable code you paste into your own Google Colab notebook, one cell at a time.

**Course site:** https://sreenivas-sadhu-prabhakara.github.io/learn-ml-models/

## Lessons

| # | Model | Status | Guide |
|---|-------|--------|-------|
| 01 | K-Nearest Neighbours | ✅ Ready | [Step-by-step guide](https://sreenivas-sadhu-prabhakara.github.io/learn-ml-models/knn/) |
| 02 | Linear Regression (+ feature engineering, Ridge, Lasso) | 🔜 Coming soon | — |
| 03 | Logistic Regression | 🔜 Coming soon | — |
| 04 | Decision Trees | 🔜 Coming soon | — |
| 05 | Random Forests | 🔜 Coming soon | — |
| 06 | Gradient Boosting | 🔜 Coming soon | — |

## How the lessons work

Each lesson is a single web page of numbered steps. Every step has a copyable code cell and a "what you should see" slip showing the exact expected output (verified by actually running the code). Learners open a fresh notebook at [colab.research.google.com](https://colab.research.google.com), paste each cell, and run it — no installs, no downloads, no uploads.

## The dataset

`data/india_bulk_block_deals.csv` — 119,156 real bulk & block deals from the Indian exchanges (NSE & BSE, 2020 → July 2026): date, symbol, deal type (BULK/BLOCK), side (BUY/SELL), quantity, price, and trade value in ₹ crore. The code cells load it directly from this repo's raw URL.

## Repo layout

```
index.html          → course home page (GitHub Pages)
knn/index.html      → Lesson 01 guide page
data/               → the shared dataset
```

## Adding a lesson

1. Create `<lesson>/index.html` following the design system in `knn/index.html`, with copyable cells and receipts.
2. Run every code cell locally and paste the exact outputs into the receipts (`random_state=42` everywhere so everyone gets identical results).
3. Link it from `index.html` and this README.
