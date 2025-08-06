# Airbnb Price Prediction Project

## Introduction
This project aims to analyze Airbnb property data and predict rental prices using machine learning techniques. The data was collected, cleaned, visually analyzed, and then predictive models were built to estimate prices based on property and host features.

---

## Workflow Steps

### 1. Data Import and Preparation
- Loaded property data from a CSV file.
- Handled missing values and converted numeric columns (such as price and service fee) to proper numeric format.
- Dropped irrelevant columns like property ID, host name, geographic location, etc.

### 2. Exploratory Data Analysis
- Displayed statistical summaries of the data.
- Plotted distributions of numeric columns such as price, service fee, construction year, etc.
- Analyzed categorical columns like room type, cancellation policy, host identity verification status.

### 3. Handling Missing Values
- Removed rows containing missing values to ensure data quality.

### 4. Encoding Categorical Columns
- Converted categorical columns to numeric using `LabelEncoder` for model compatibility.

### 5. Building Predictive Models
- Split the data into training and testing sets.
- Built three models:
    - Linear Regression
    - Decision Tree Regressor
    - Random Forest Regressor
- Evaluated model performance using R², MSE, and MAE metrics.

### 6. Price Prediction
- Tested the model on new data and predicted property prices based on their features.

### 7. Model Saving
- Saved the final model using `joblib` for future use.

---

## Results

- **Best Model:** Random Forest Regressor achieved the highest accuracy (R² > 0.99).
- **Most Influential Features:** Room type, construction year, host status, cancellation policy, service fee.
- **Price Distribution:** Most properties are priced between $200 and $1200.
- **Service Fee Distribution:** Most fees range between $0 and $250.

---

## Visualizations

- Price and service fee distribution plots.
- Room type and cancellation policy distribution charts.
- Correlation matrix of numeric features.
- Charts showing the impact of area and host type on price.

---

## Conclusion

This project demonstrates how machine learning can be used to analyze and accurately predict Airbnb property prices. The model can be further improved by including additional features or using more advanced techniques.

---

🖥️ Desktop Application:

The file airbnb_predictor.py is a desktop application built to allow users to easily interact with the trained model and predict Airbnb rental prices by entering property details.



## Project Links

- [GitHub Repository](https://github.com/SabryAlaa10/Airbnb-Prediction-Model)
- [LinkedIn Post](https://www.linkedin.com/in/sabry-mohmmed-56a5b4320)

---

## Tools and Technologies Used

- Python, Pandas, NumPy, Scikit-learn, Plotly, Seaborn
- Machine Learning Models: Linear Regression, Decision Tree, Random Forest

---

## Contact

For any inquiries or collaboration, feel free to reach out via [LinkedIn](https://www.linkedin.com/in/sabry-mohmmed-56a5b4320) or open an Issue on GitHub.

---

## Google Drive Link for Large Files

You can download the project files (Python code and CSV data file) from Google Drive using the following link:

[Google Drive Link](https://drive.google.com/drive/folders/13qXVTqeEIazpxBS3ZF-PKVBMEKMsknDB?usp=drive_link)

> **Note:** The files are large, so they have been uploaded to Google Drive for easier access and download.
