# InsureAI User Guide

This guide explains how to navigate the Insurance Charges Prediction app, read each chart, generate a prediction, and download reports.

## 1. Open the app

For the deployed app, open the Streamlit URL supplied with the project. To run it locally from the project folder:

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app opens on the Executive Dashboard. On a first visit, a centered tour card offers **Take a quick tour** or **Skip tour**. During the tour, the sidebar remains usable; choosing a page in the sidebar changes the page and its explanation. Use **Back**, **Next**, **Finish**, or **Skip** as desired.

## 2. Navigate the five pages

Use the left sidebar to open:

1. **Executive Dashboard** — interactive summaries and ten analysis charts.
2. **Insurance Prediction** — estimate charges from an entered customer profile.
3. **Dataset Explorer** — inspect and filter the source records.
4. **Reports & Downloads** — export dataset and analysis reports.
5. **About Project** — review the current model evaluation and project details.

## 3. Executive Dashboard

### Apply dashboard filters

The dashboard has three filters: **Gender**, **Smoking Status**, and **Region**. They start with every available category selected. Change a selection to filter the records used by the dashboard KPIs, charts, insights, and CSV export. To restore the full view, select all available categories again. If the selection matches no records, the dashboard displays a warning.

### Read the KPI cards

- **Total Customers:** number of records remaining after the dashboard filters.
- **Average Charges:** mean observed charge among those records.
- **Highest Charges:** largest observed charge among those records.
- **Smoker Percentage:** percentage of the filtered records whose smoking status is yes.

These cards describe the dataset. They are not model predictions.

### Read the ten dashboard charts

All ten charts use the filtered records. Hover over a mark to see its exact values and any additional fields shown in the tooltip. On charts where the Plotly toolbar is available, use it to zoom or reset the view.

1. **Distribution of Insurance Charges — histogram**  
   The x-axis groups observed charges into 30 ranges; the y-axis counts customers in each range. Use it to see where charges cluster and whether the distribution has a long high-charge tail.

2. **Average Charges by Smoking Status — bar chart**  
   Each bar is the mean charge for the `yes` or `no` smoking group. Compare group averages; this summarizes association in the data and does not establish cause.

3. **Average Insurance Charges by Region — bar chart**  
   Each bar is the mean charge for a residential region. The result changes with the dashboard filters.

4. **Age vs Insurance Charges — bubble scatter plot**  
   Each point is a customer. Horizontal position is age, vertical position is observed charges, color indicates smoking status, and bubble size represents BMI. Hover to inspect sex, region, and number of children.

5. **BMI vs Insurance Charges — scatter plot**  
   Each point is a customer. Horizontal position is BMI, vertical position is observed charges, and color indicates smoking status. Hover to inspect age, sex, and region.

6. **Average Insurance Charges by Age Group — bar chart**  
   Bars show mean charges for age bands: 18–25, 26–35, 36–45, 46–55, 56–65, and 66+. The color intensity also represents the mean charge. Empty age groups are omitted.

7. **Average Charges by Number of Children — bar chart**  
   Each bar shows the mean charge for customers with that number of children. Compare group averages; the chart does not show that having children causes a charge change.

8. **Insurance Charges Distribution by Smoking Status — box plot**  
   Each box summarizes the charge distribution for smokers and non-smokers. The center line marks the median; the box spans the middle half of values; whiskers show the broader range; individual points beyond the whiskers are outliers.

9. **Average Charges by BMI Category — bar chart**  
   Bars show mean charges for the app’s categories: Underweight (BMI below 18.5), Normal (18.5 to below 25), Overweight (25 to below 30), and Obese (30 or higher). These are dataset groupings, not medical advice.

10. **Correlation Between Numerical Features — heatmap**  
    Each cell shows the Pearson correlation for a pair of numeric fields: age, BMI, children, and charges. Values range from -1 to +1; values near zero indicate a weaker linear relationship, while the sign indicates direction. Correlation does not imply causation.

### Read the Business Insights cards

The cards show the filtered mean charges for smokers and non-smokers and identify the region with the highest filtered mean charge. These values update with the three dashboard filters. A comparison is omitted when a smoking group has no matching records.

### Export dashboard data

Select **Download Filtered Dashboard Data (CSV)** to export the same filtered records used in the KPIs and charts.

## 4. Insurance Prediction

1. Enter **Age** (18–100), **Gender**, **BMI** (10–60), **Number of Children** (0–10), **Smoking Status**, and **Region**.
2. Select **Predict Insurance Charges**.
3. Read the estimated charge and the BMI category and smoking status in the prediction summary.
4. Review saved predictions under **Prediction History**.
5. Select **Download Prediction History (Excel)** to export the current session’s history. Select **Clear Prediction History** to remove it.

The model accepts those input bounds, but the training data covers narrower ranges (for example, ages 18–64 and 0–5 children). Estimates for profiles beyond the training data’s observed ranges may be less reliable. A prediction is an estimate, not an insurance quotation.

BMI categories shown in the prediction summary are Underweight (below 18.5), Normal (18.5 to below 25), Overweight (25 to below 30), and Obesity range (30 or higher).

## 5. Dataset Explorer

### Overview cards

- **Total Records:** number of records in the loaded dataset after duplicate removal.
- **Total Features:** number of columns, including the `charges` target.
- **Missing Values:** total missing cells in the loaded dataset.

These three cards describe the complete dataset, not the current filtered subset.

### Filter and inspect records

1. Choose one or more values under **Gender**, **Smoking Status**, and **Region**.
2. Set the **Age Range** slider. Unlike the Executive Dashboard, this page includes an age filter.
3. The **Filtered Dataset** table and record count update to match all four filters together.
4. Use **Download Filtered Data (CSV)** or **Download Filtered Data (Excel)** to export the selected rows.
5. Review **Descriptive Statistics** for numeric columns in the filtered data. If no rows match, the app explains that statistics are unavailable.
6. Review **Column Information** for each column’s data type, missing-value count, and number of unique values. This table describes the complete dataset.

## 6. Reports & Downloads

This page provides reports from the loaded dataset after duplicate removal:

- **Dataset Summary Report:** descriptive statistics for numeric columns; download as Excel.
- **Complete Dataset:** export all records as CSV or Excel.
- **Smoking Analysis Report:** customer count and average, minimum, and maximum charges by smoking status; download as CSV.
- **Regional Analysis Report:** customer count, average charges, and maximum charges by region; download as Excel.
- **Prediction History Report:** displays and exports predictions made in the current app session. It appears after a prediction has been generated.

## 7. About Project: model results and charts

The page reads the latest results saved by the modeling notebook. If the evaluation file is missing or stale, run all cells in `insurance_prediction.ipynb` to regenerate the model and evaluation artifact.

### Holdout KPI cards

The selected model is chosen using cross-validation on training data. The page shows its R-squared, MAE, MSE, and RMSE measured on a separate holdout test partition. MAE also includes a bootstrap 95% interval.

- **R-squared:** higher is better; 1 is ideal, and a negative score is possible.
- **MAE:** average absolute error in charge units; lower is better.
- **MSE:** average squared error; lower is better, and larger misses receive more weight.
- **RMSE:** square root of MSE in charge units; lower is better.

### Cross-Validated Model Comparison chart

The table compares only the algorithms trained in the latest notebook run. It reports five-fold training cross-validation means for R-squared, MAE, MSE, and RMSE. The R-squared column highlights the highest mean. The chart’s **Compare models by** selector changes the plotted metric; the best model on that selected metric is shown in navy and the others in light blue. These are training cross-validation scores, not separate test scores for every model.

### Feature Importance chart

The horizontal bar chart shows importance calculated from the latest selected pipeline. Tree models use native feature importance, with encoded categories combined back into their original fields; models without native importance use permutation importance. The method is named above the chart. The largest bar has the highest calculated predictive contribution in this model. Importance and correlations show association, not causation.

## 8. Interpreting results responsibly

The dataset is small and simplified. Real insurance pricing may use information not present here, and patterns may differ for other populations or time periods. Predictions may be less reliable outside the ranges represented in the training data. Do not treat a prediction as a quote, medical assessment, underwriting decision, or substitute for professional insurance advice.

## 9. Quick troubleshooting

- **The tour appears again:** the tour choice is stored for the current Streamlit session. Select **Skip** or **Finish** to dismiss it for that session.
- **Model results are missing:** run all cells in `insurance_prediction.ipynb` from the project folder to create `insurance_charges_model.pkl` and `model_evaluation.json`.
- **Prediction fails:** check that the model artifact exists and the input values are within the form’s allowed ranges.
- **A dashboard chart is empty:** check that the Gender, Smoking Status, and Region filters still include records.
- **Prediction history is empty:** history is created after a successful prediction and is kept in the current app session.
