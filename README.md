# Premium House Price Prediction Project

A production-grade, end-to-end Machine Learning pipeline and interactive Web Application for predicting house prices. This project demonstrates best practices in data science project scaffolding, exploratory data analysis (EDA), model training, evaluation, serialization, and UI development using Streamlit.

---

## 🏗️ Project Architecture

```text
d:\Rajendra\Datascience\
├── data/
│   └── housing_data.csv              # Synthetic/Real housing dataset
├── plots/
│   ├── correlation_heatmap.png       # Correlation matrix of features
│   ├── price_vs_sqft.png            # Scatter plot of Price vs. SqFt
│   └── price_vs_quality.png         # Boxplot/Scatter plot of Price vs. Quality
├── models/
│   ├── best_model.pkl                # Trained model pickle file (RF or XGBoost)
│   └── scaler.pkl                    # Saved feature scaler
├── src/
│   ├── __init__.py
│   ├── generate_data.py              # Script to generate realistic housing data
│   ├── eda.py                        # Script for exploratory data analysis
│   └── train.py                      # Training and evaluation pipeline
├── app.py                            # Streamlit web application
├── requirements.txt                  # Python dependencies
└── README.md                         # Project documentation
```

---

## 🛠️ Features & Pipeline

1. **Scaffolding**: Complete standard folder structures (`data/`, `src/`, `notebooks/`, `plots/`, `models/`).
2. **Environment Setup**: Fully documented virtual environment using python venv or conda.
3. **Data Generation & EDA**:
   - Generates 1,000 realistic records with features: `TotalSqFt`, `Bedrooms`, `Bathrooms`, `OverallQuality`, `YearBuilt`, and `Price`.
   - Performs advanced exploratory data analysis and exports high-quality visualization assets to `plots/`.
4. **Model Training & Evaluation**:
   - Cleans and prepares dataset, splits train/test partitions (80/20).
   - Trains and hyper-tunes a **Random Forest Regressor** and an **XGBoost Regressor**.
   - Evaluates performance metrics using **Root Mean Squared Error (RMSE)** and **$R^2$ Score**.
   - Saves the champion model and scaler to the `models/` directory.
5. **Interactive Web Interface**:
   - Premium Streamlit interface (`app.py`).
   - Sidebar sliders for custom configurations.
   - Dynamic inference showcasing the predicted house value immediately.
   - Visual model performance reporting.

---

## 🚀 Getting Started

### 1. Environment Setup

Create and activate a virtual environment named `house-price-env` using Python 3.11:

```bash
# Create environment
python -m venv house-price-env

# Activate on Windows (PowerShell)
.\house-price-env\Scripts\Activate.ps1

# Activate on Git Bash / Linux / macOS
source house-price-env/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

### 2. Generate Data & Perform EDA

Generate synthetic dataset and run exploratory analysis to generate plots:

```bash
# Generate the data
python src/generate_data.py

# Perform exploratory analysis (exports plots)
python src/eda.py
```

### 3. Model Training & Serialization

Train the Random Forest and XGBoost models, compare metrics, and export the best performer:

```bash
python src/train.py
```

### 4. Launch the Interactive Web UI

Launch the Streamlit web dashboard:

```bash
streamlit run app.py
```

---

## 📊 Feature Definitions

- **Total Square Footage**: Continuous metric representing the sum of all indoor space (sq ft).
- **Bedrooms**: Number of bedrooms (discrete, 1 to 6).
- **Bathrooms**: Number of bathrooms (continuous/half-bath format, 1.0 to 4.5).
- **Overall Quality**: Overall house rating from 1 (Poor) to 10 (Excellent).
- **Year Built**: House construction year (1900 to 2026).
