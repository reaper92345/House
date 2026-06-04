import os
import pickle
import numpy as np
import pandas as pd
import streamlit as st

# Set page configuration with a premium look
st.set_page_config(
    page_title="GharVal AI - Nepal Real Estate Valuation",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for minimalist light theme tailored for Nepal (incorporating clean white/grey with soft Crimson/Blue highlights of Nepal flag)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Main Background & Light theme styling */
    .stApp {
        background-color: #f8fafc;
        color: #0f172a;
    }
    
    /* Sidebar styling override - Light Grey */
    [data-testid="stSidebar"] {
        background-color: #f1f5f9 !important;
        border-right: 1px solid #e2e8f0;
    }
    
    /* Minimalist Title Banner with Nepali Crimson Accent Line */
    .header-container {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 16px;
        margin-bottom: 25px;
        border: 1px solid #e2e8f0;
        border-top: 4px solid #dc2626; /* Crimson Red of Nepal Flag */
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        text-align: center;
    }
    .header-title {
        color: #0f172a;
        font-size: 2.8rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .header-subtitle {
        color: #475569;
        font-size: 1.1rem;
        font-weight: 300;
        margin-top: 10px;
        opacity: 0.9;
    }
    
    /* Premium Minimalist Cards for Metrics & Prediction */
    .card-glass {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    .card-glass:hover {
        transform: translateY(-4px);
        border-color: #1e3a8a; /* Deep Blue of Nepal Flag */
    }
    
    /* Dynamic Prediction Output Styling */
    .price-value {
        font-size: 3.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #10b981 0%, #059669 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
        line-height: 1.1;
    }
    .price-label {
        font-size: 1rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
    }
    
    /* Bullet points & indicators */
    .feature-indicator {
        display: inline-block;
        padding: 6px 12px;
        background-color: #f1f5f9;
        color: #334155;
        border-radius: 20px;
        font-size: 0.85rem;
        margin-right: 8px;
        margin-top: 8px;
        border: 1px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to load model and scaler
@st.cache_resource
def load_assets():
    model_path = 'models/best_model.pkl'
    scaler_path = 'models/scaler.pkl'
    
    if not os.path.exists(model_path) or not os.path.exists(scaler_path):
        return None, None
        
    with open(model_path, 'rb') as f:
        model_payload = pickle.load(f)
        
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)
        
    return model_payload, scaler

model_payload, scaler = load_assets()

# ----------------- UI Layout -----------------

# Header Banner customized for Nepal
st.markdown("""
<div class="header-container">
    <div class="header-title">🇳🇵 घर-मूल्य निर्धारण</div>
</div>
""", unsafe_allow_html=True)

if model_payload is None or scaler is None:
    st.warning("⚠️ Training Assets Not Found!")
    st.info("The model has not been trained yet. Please complete the model training step to proceed.")
    st.stop()

# Constants
NPR_EXCHANGE_RATE = 135.0  # Conversion rate to match Nepalese market pricing

# Sidebar - Core House Features with Nepalese conversions (Anna/Ropani)
st.sidebar.markdown("<h2 style='color:#1e3a8a;'>🔍 Property Specifications</h2>", unsafe_allow_html=True)
st.sidebar.write("Adjust the features below to dynamically calculate the house value.")

total_sqft = st.sidebar.slider("Total Area (Square Footage)", min_value=500, max_value=5000, value=1800, step=50)

# 1 Anna = 342.25 SqFt on standard Kathmandu Valley measurements
anna_equiv = total_sqft / 342.25
st.sidebar.caption(f"💡 Equivalent to approx. **{anna_equiv:.2f} Anna** (1 Anna ≈ 342.25 SqFt)")

bedrooms = st.sidebar.slider("Bedrooms", min_value=1, max_value=6, value=3, step=1)
bathrooms = st.sidebar.slider("Bathrooms", min_value=1.0, max_value=4.5, value=2.0, step=0.5)
overall_quality = st.sidebar.slider("Overall Quality (1-10 Scale)", min_value=1, max_value=10, value=6, step=1)
st.sidebar.caption("1-3: Simple brick-masonry, 4-7: RCC frame structure, 8-10: Luxury villa construction")

year_built = st.sidebar.slider("Year Built (B.S. / A.D.)", min_value=1950, max_value=2026, value=2018, step=1)

# Main Grid (2 Columns)
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("<h3 style='color:#1e3a8a; margin-bottom: 15px;'>🔮 Real-Time Valuation</h3>", unsafe_allow_html=True)
    
    # Prepare single data point for prediction
    input_data = pd.DataFrame([[total_sqft, bedrooms, bathrooms, overall_quality, year_built]], 
                              columns=['TotalSqFt', 'Bedrooms', 'Bathrooms', 'OverallQuality', 'YearBuilt'])
    
    # Preprocess
    input_scaled = scaler.transform(input_data)
    
    # Dynamic Prediction & conversion to NPR
    raw_pred = model_payload['model'].predict(input_scaled)[0]
    predicted_usd = max(30000.0, float(raw_pred)) # Floor
    predicted_npr = predicted_usd * NPR_EXCHANGE_RATE
    
    # Format to Lakhs and Crores for Nepalese standard notation
    # 1 Crore = 10,000,000. 1 Lakh = 100,000.
    if predicted_npr >= 10000000:
        crores = predicted_npr / 10000000
        nepali_notation = f"{crores:.2f} Crore NPR"
    else:
        lakhs = predicted_npr / 100000
        nepali_notation = f"{lakhs:.2f} Lakh NPR"
        
    # Minimalist Nepalese Rupees Price Valuation Card
    price_html = f"""
    <div class="card-glass">
        <div class="price-label">Estimated Market Price (NPR)</div>
        <div class="price-value">रु. {predicted_npr:,.0f}</div>
        <div style="font-size: 1.1rem; color:#475569; font-weight:600; margin-bottom: 15px;">
            Equivalent to Approx: <span style="color:#dc2626;">{nepali_notation}</span>
        </div>
        <div style="margin-top: 15px;">
            <span class="feature-indicator">📐 {total_sqft:,} SqFt ({anna_equiv:.1f} Anna)</span>
            <span class="feature-indicator">🛏️ {bedrooms} Bed</span>
            <span class="feature-indicator">🛁 {bathrooms} Bath</span>
            <span class="feature-indicator">⭐️ Quality: {overall_quality}/10</span>
            <span class="feature-indicator">📅 Built: {year_built}</span>
        </div>
    </div>
    """
    st.markdown(price_html, unsafe_allow_html=True)
    
    # Analytics section: Expandable insights customized for Nepal
    with st.expander("📈 Insights & Explainability (नेपाल घर-जग्गा विश्लेषण)", expanded=True):
        st.write("Below are the primary factors driving this valuation in Nepal:")
        
        # Calculate simplistic contributions based on feature inputs relative to average values
        avg_sqft = 2200
        avg_qual = 6
        
        sqft_diff = total_sqft - avg_sqft
        qual_diff = overall_quality - avg_qual
        
        st.markdown(f"- **Size Scale:** Your property is {abs(sqft_diff)} SqFt {'larger' if sqft_diff >= 0 else 'smaller'} than the median Kathmandu home (2,200 SqFt / 6.4 Anna), significantly influencing land base value.")
        st.markdown(f"- **Structure Rating:** A build quality rating of **{overall_quality}/10** indicates an **{'Earthquake-resistant Premium RCC structure' if overall_quality >= 6 else 'Standard brick masonry layout'}**, affecting structural valuation safety margins.")
        
        # Earthquake factor: major pricing driver in Nepal real estate
        if year_built >= 2015:
            st.markdown("- **Structural Vintage:** Built post **2015 (Gorkha Earthquake)**. Post-earthquake structures command a premium due to compliance with updated structural engineering guidelines and seismic safety measures in Nepal.")
        else:
            st.markdown("- **Structural Vintage:** Built pre **2015 (Gorkha Earthquake)**. Pre-earthquake structures may be subject to depreciation unless retrofitted and verified for structural integrity.")

with col2:
    st.markdown("<h3 style='color:#1e3a8a; margin-bottom: 15px;'>📊 Model Telemetry</h3>", unsafe_allow_html=True)
    
    # Performance Telemetry Card scaled to NPR
    npr_rmse = model_payload['rmse'] * NPR_EXCHANGE_RATE
    
    telemetry_html = f"""
    <div class="card-glass">
        <h4 style="margin: 0 0 15px 0; color:#10b981; font-weight: 600;">Champion ML Algorithm</h4>
        <div style="font-size: 1.6rem; font-weight: 700; color:#0f172a; margin-bottom:12px;">{model_payload['model_name']}</div>
        <table style="width:100%; border-collapse: collapse; font-size: 0.95rem; color:#475569;">
            <tr style="border-bottom: 1px solid #e2e8f0;">
                <td style="padding: 8px 0; font-weight:500;">Metric</td>
                <td style="padding: 8px 0; text-align: right; font-weight:600; color: #1e3a8a;">Value</td>
            </tr>
            <tr style="border-bottom: 1px solid #e2e8f0;">
                <td style="padding: 8px 0;">R² Coefficient</td>
                <td style="padding: 8px 0; text-align: right; font-weight:600; color: #0f172a;">{model_payload['r2']:.4f}</td>
            </tr>
            <tr>
                <td style="padding: 8px 0;">Test RMSE (NPR)</td>
                <td style="padding: 8px 0; text-align: right; font-weight:600; color: #0f172a;">रु. {npr_rmse:,.0f}</td>
            </tr>
        </table>
    </div>
    """
    st.markdown(telemetry_html, unsafe_allow_html=True)
    
    # Simulated Feature Importance chart
    if model_payload['model_name'] == "XGBoost" or model_payload['model_name'] == "Random Forest":
        # Get importances
        importances = model_payload['model'].feature_importances_
        feature_imp_df = pd.DataFrame({
            'Feature': model_payload['feature_names'],
            'Importance': importances
        }).sort_values(by='Importance', ascending=True)
        
        st.markdown("<p style='font-size:0.9rem; font-weight:600; margin-bottom: 5px; color:#475569;'>Model Feature Importance Profile</p>", unsafe_allow_html=True)
        st.bar_chart(feature_imp_df.set_index('Feature'), height=150)

# Section 3: Visual Analytics / EDA Plots
st.markdown("<h3 style='color:#1e3a8a; margin-top:20px; margin-bottom: 15px;'>📈 Visual Market Analytics</h3>", unsafe_allow_html=True)
img_col1, img_col2 = st.columns(2)

with img_col1:
    if os.path.exists("plots/price_vs_sqft.png"):
        st.image("plots/price_vs_sqft.png", caption="Linear Progression: Price vs. Total Square Footage", width='stretch')
    else:
        st.info("Price scatter plot asset not generated.")

with img_col2:
    if os.path.exists("plots/correlation_heatmap.png"):
        st.image("plots/correlation_heatmap.png", caption="Feature Correlation Matrix Heatmap", width='stretch')
    else:
        st.info("Correlation Matrix heatmap asset not generated.")
