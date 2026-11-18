# Insurance Charges Prediction

An end-to-end regression project that explores medical insurance costs, compares machine-learning models, explains important features, and serves predictions through a Streamlit dashboard.

## Project goals

- Explore demographic, lifestyle, and cost patterns in the Medical Cost Personal Dataset.
- Build a reproducible regression pipeline for estimating individual insurance charges.
- Compare models with cross-validation and report final performance on a held-out test set.
- Interpret model behavior and provide an interactive dashboard for analysis and predictions.

## Dataset

`insurance.csv` contains 1,338 records and these seven fields:

| Field | Meaning | Role |
| --- | --- | --- |
| `age` | Age of the primary beneficiary | Input |
| `sex` | Recorded sex category | Input |
| `bmi` | Body mass index | Input |
| `children` | Number of covered dependents | Input |
| `smoker` | Smoking status | Input |
| `region` | Residential region | Input |
| `charges` | Individual medical insurance charges | Prediction target |

The notebook checks the data, removes duplicate records, and imputes missing values within the model pipeline. Dataset associations are descriptive and should not be interpreted as causal effects.

## Method

1. Inspect data types, summary statistics, missing values, duplicates, and distributions.
2. Explore feature relationships, outliers, and numerical correlations.
3. Split data into an 80% training partition and a 20% held-out test partition, preserving the smoker proportions.
4. Fit numerical imputation and scaling plus categorical imputation and one-hot encoding inside scikit-learn pipelines.
5. Compare Linear, Ridge, Lasso, Decision Tree, Random Forest, and Gradient Boosting regressors. XGBoost is included when installed.
6. Select the candidate using shuffled five-fold cross-validation on training data, tune its parameters with cross-validation, and evaluate the selected pipeline once on the held-out test data.
7. Report R², MAE, MSE, and RMSE; inspect actual-versus-predicted values and residuals; estimate a bootstrap 95% interval for holdout MAE; and calculate permutation importance.

The split and cross-validation use fixed random seeds for repeatability. The held-out test set is kept out of model selection and tuning.

## Current benchmark

On the included dataset, the notebook removed one duplicate and used 1,337 records. In the latest run, Gradient Boosting ranked first during training-only cross-validation and was tuned with GridSearchCV. The final results on the untouched 268-record test partition were:

| Metric | Holdout result |
| --- | ---: |
| R² | 0.9195 |
| MAE | $2,121.87 |
| RMSE | $3,407.36 |
| 95% bootstrap interval for MAE | $1,831.59–$2,455.14 |

These are results for the fixed seed and split in the current notebook. They are a benchmark, not a guarantee of performance on new populations.

## Run locally

Use Python 3.10 or newer, then install the packages:

```bash
pip install -r requirements.txt
```

Run the interactive application:

```bash
streamlit run app.py
```

Run the full modeling notebook from the project directory:

```bash
jupyter notebook insurance_prediction.ipynb
```

The notebook saves the fitted preprocessing-and-model pipeline to `insurance_charges_model.pkl`; the Streamlit prediction page loads that file. Run the notebook before launching the app if the model file is missing or you want to regenerate it.

## Streamlit app

- **Executive Dashboard:** filter and explore charges, demographics, smoking status, age, BMI, and regions.
- **Insurance Prediction:** estimate charges from entered customer attributes and review prediction history.
- **Dataset Explorer:** filter records and inspect summaries and missing values.
- **Reports & Downloads:** export analysis reports.
- **About Project:** review the project description, fields, model families, and evaluation metrics.

## Limitations and responsible use

This dataset is small and simplified relative to real insurance portfolios. Predictions reflect patterns in this dataset and may not generalize to other populations, locations, or time periods. The model is an educational estimation tool, not a medical or underwriting decision system. Feature importance describes predictive association, not causation. Any real deployment would need broader validation, privacy protections, and review for fairness and regulatory requirements.

## Future improvements

- Evaluate repeated or nested cross-validation for more robust model selection.
- Add prediction intervals and subgroup error analysis.
- Validate on newer and more representative data.
- Track model versions and data drift in a production deployment.
