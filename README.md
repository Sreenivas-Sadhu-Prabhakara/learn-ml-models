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
