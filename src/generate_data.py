import os
import numpy as np
import pandas as pd

def generate_bhaktapur_housing_data(num_samples=1000, random_seed=42):
    """
    Generates a highly realistic synthetic housing dataset tailored for the
    Bhaktapur & Kathmandu Valley real estate market, incorporating specific road features:
    - RoadWidth: Road width in feet (mostly 13ft, some 20ft)
    - RoadType_RCC: Binary indicator (1 for RCC, 0 for Blacktopped)
    
    Features generated:
    - TotalSqFt: Built-up area (approx. 900 to 4800 SqFt, correlated with Land Area in Anna)
    - Bedrooms: Number of bedrooms (2 to 8)
    - Bathrooms: Number of bathrooms (1.5 to 5.0)
    - OverallQuality: Overall rating of build quality & finishes (1 to 10 scale)
    - YearBuilt: Year constructed (1995 to 2026)
    - RoadWidth: Road width in feet (mostly 13ft, some 20ft)
    - RoadType_RCC: 1 if RCC road, 0 if Blacktopped
    - Price: Target variable (computed in NPR and converted to USD for standard pipeline compatibility)
    """
    np.random.seed(random_seed)
    
    # 1. Generate Land Area in Anna (2.0 to 6.5 Anna, average ~3.3 Anna)
    land_anna = np.random.normal(3.3, 0.7, num_samples)
    land_anna = np.clip(land_anna, 2.0, 6.5)
    
    # 2. Generate TotalSqFt (built-up area) based on Land Area and storeys
    storeys = np.random.choice([2.5, 3.0, 3.5], size=num_samples, p=[0.3, 0.5, 0.2])
    footprint_sqft = land_anna * 342.25 * np.random.uniform(0.7, 0.85, num_samples)
    total_sqft = np.round(footprint_sqft * storeys).astype(int)
    total_sqft = np.clip(total_sqft, 900, 4800)
    
    # 3. Generate Bedrooms
    bedrooms = np.round((total_sqft / 420) + np.random.normal(0, 0.7, num_samples)).astype(int)
    bedrooms = np.clip(bedrooms, 2, 8)
    
    # 4. Generate Bathrooms
    bathrooms = np.round((bedrooms * 0.7) + np.random.normal(0, 0.4, num_samples) * 2) / 2
    bathrooms = np.clip(bathrooms, 1.5, 5.0)
    
    # 5. Generate Overall Quality (1 to 10 scale)
    overall_quality = np.clip(np.random.normal(5.8, 1.5, num_samples).astype(int), 2, 10)
    
    # 6. Generate Year Built
    year_built = np.random.randint(1990, 2027, num_samples)
    
    # 7. Generate Road Width and Road Type based on user inputs:
    # "most have 13ft of black topped while some have 20 ft of rcc"
    # We will model 13ft (approx 75% of houses) and 20ft (approx 25% of houses) with slight variations
    road_class = np.random.choice(['13ft_blacktopped', '20ft_rcc'], size=num_samples, p=[0.75, 0.25])
    
    road_width = np.where(road_class == '13ft_blacktopped', 
                          np.random.choice([12, 13, 14], size=num_samples, p=[0.1, 0.8, 0.1]), 
                          np.random.choice([18, 20, 22], size=num_samples, p=[0.1, 0.8, 0.1]))
    
    road_type_rcc = np.where(road_class == '20ft_rcc', 1, 0)
    
    # 8. Generate Price in NPR based on Bhaktapur local market valuations
    # Base land price in Bhaktapur: रु. 35 Lakhs per Anna average
    land_price_per_anna = np.random.normal(3500000, 400000, num_samples)
    
    # Road Width & Type Premium: 
    # Wider roads increase land valuation. RCC roads also carry a premium.
    # 20ft road adds रु. 4 Lakhs per Anna to the base land price
    road_width_premium = np.where(road_width >= 18, 400000, 0)
    land_component = land_anna * (land_price_per_anna + road_width_premium)
    
    # Construction cost component
    construction_rate = 2800 + (overall_quality * 280)
    construction_component = total_sqft * construction_rate
    
    # Room bonuses
    room_bonus = (bedrooms * 200000) + (bathrooms * 150000)
    
    # Structural Earthquake premium (Post-2015)
    earthquake_premium = np.where(year_built >= 2015, 1500000, 0)
    
    # Road Type structural/infrastructure premium: RCC road adds a flat रु. 8 Lakhs premium
    rcc_premium = np.where(road_type_rcc == 1, 800000, 0)
    
    # Calculate price in NPR with random market noise
    market_noise = np.random.normal(0, 1200000, num_samples)
    
    price_npr = (
        land_component 
        + construction_component 
        + room_bonus 
        + earthquake_premium 
        + rcc_premium
        + market_noise
    )
    
    # Floor price at रु. 1.2 Crore
    price_npr = np.clip(price_npr, 12000000, None)
    price_npr = np.round(price_npr, -4)  # Round to nearest 10,000 NPR
    
    # Convert to USD using the pipeline exchange rate (135.0)
    price_usd = price_npr / 135.0
    price_usd = np.round(price_usd, -2)
    
    # Combine into standard DataFrame
    df = pd.DataFrame({
        'TotalSqFt': total_sqft,
        'Bedrooms': bedrooms,
        'Bathrooms': bathrooms,
        'OverallQuality': overall_quality,
        'YearBuilt': year_built,
        'RoadWidth': road_width,
        'RoadType_RCC': road_type_rcc,
        'Price': price_usd
    })
    
    # Save the data
    output_dir = 'data'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'housing_data.csv')
    df.to_csv(output_path, index=False)
    
    print(f"Successfully generated {num_samples} road-aware Bhaktapur samples and saved to {output_path}")
    print("\nSample Generated Records:")
    print(df.head())
    
    df_npr_stats = df.copy()
    df_npr_stats['Price_NPR_Crores'] = (df_npr_stats['Price'] * 135.0) / 10000000
    print("\nDataset Summary Statistics (Price in Crores NPR):")
    print(df_npr_stats[['TotalSqFt', 'RoadWidth', 'RoadType_RCC', 'Price_NPR_Crores']].describe())

if __name__ == '__main__':
    generate_bhaktapur_housing_data()
