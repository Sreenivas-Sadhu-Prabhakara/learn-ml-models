# Learn ML Models

Hands-on machine learning lessons for friends learning together — plain language, real Indian stock-market data, and code you copy-paste into Google Colab.

**Course site:** https://sreenivas-sadhu-prabhakara.github.io/learn-ml-models/

## Lessons

| # | Model | Status | Guide | Notebook |
|---|-------|--------|-------|----------|
| 01 | K-Nearest Neighbours | ✅ Ready | [Step-by-step guide](https://sreenivas-sadhu-prabhakara.github.io/learn-ml-models/knn/) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Sreenivas-Sadhu-Prabhakara/learn-ml-models/blob/main/notebooks/knn_bulk_vs_block.ipynb) |
| 02 | Linear Regression | 🔜 Coming soon | — | — |
| 03 | Decision Trees | 🔜 Coming soon | — | — |
| 04 | K-Means | 🔜 Coming soon | — | — |

## The dataset

`data/india_bulk_block_deals.csv` — 119,156 real bulk & block deals from the NSE (2020 → July 2026): date, symbol, deal type (BULK/BLOCK), side (BUY/SELL), quantity, price, and trade value in ₹ crore. The notebooks load it directly from this repo's raw URL, so learners never need to download or upload anything.

## Repo layout

```
index.html          → course home page (GitHub Pages)
knn/index.html      → Lesson 01 guide page
notebooks/          → ready-to-run Colab notebooks
data/               → the shared dataset
```

## Adding a lesson

1. Add a notebook under `notebooks/` (load data from the raw GitHub URL, `random_state=42` everywhere so everyone gets identical results).
2. Add a guide page under `<lesson>/index.html` with copyable cells and "what you should see" outputs.
3. Link it from `index.html` and this README.
