import os
import numpy as np
import pandas as pd

def generate_housing_data(num_samples=1000, random_seed=42):
    """
    Generates a highly realistic synthetic housing dataset with correlated features.
    
    Features:
    - TotalSqFt: Total square footage of the house (500 to 5000 sq ft)
    - Bedrooms: Number of bedrooms (1 to 6)
    - Bathrooms: Number of bathrooms (1.0 to 4.5)
    - OverallQuality: Overall rating of the house (1 to 10)
    - YearBuilt: Year the house was built (1900 to 2026)
    - Price: Target variable (computed using a non-linear function with noise)
    """
    np.random.seed(random_seed)
    
    # 1. Generate Overall Quality (1 to 10, mean around 6)
    overall_quality = np.clip(np.random.normal(6.2, 1.8, num_samples).astype(int), 1, 10)
    
    # 2. Generate Total Square Footage (correlated with quality)
    # Higher quality houses tend to be larger
    base_sqft = np.random.uniform(500, 3500, num_samples)
    quality_sqft_bonus = (overall_quality - 1) * 150
    total_sqft = np.round(base_sqft + quality_sqft_bonus).astype(int)
    total_sqft = np.clip(total_sqft, 500, 5000)
    
    # 3. Generate Bedrooms (correlated with square footage)
    # Standard formula: 1 bedroom per ~800 sq ft, with some random variation
    bedrooms = np.round((total_sqft / 850) + np.random.normal(0, 0.6, num_samples)).astype(int)
    bedrooms = np.clip(bedrooms, 1, 6)
    
    # 4. Generate Bathrooms (correlated with bedrooms and square footage)
    # Bathrooms can be half baths (e.g. 1.5, 2.5)
    bathrooms_raw = (bedrooms * 0.7) + (total_sqft / 1500) + np.random.normal(0, 0.4, num_samples)
    # Round to nearest 0.5
    bathrooms = np.round(bathrooms_raw * 2) / 2
    bathrooms = np.clip(bathrooms, 1.0, 4.5)
    
    # 5. Generate Year Built (uniformly distributed or slightly skewed towards newer)
    year_built = np.random.randint(1900, 2027, num_samples)
    
    # 6. Generate House Price (with a realistic, non-linear function & interaction terms)
    # Base price: $40,000
    # SqFt price: $115 per sq ft
    # Quality price: $22,000 per quality level
    # Interaction: SqFt * Quality (larger, high-quality houses are exponentially more expensive)
    # Bathroom bonus: $18,000 per bathroom
    # Bedroom bonus: $10,000 per bedroom
    # Age factor: Newer houses have a premium. Let's add $900 per year since 1900
    base_price = 40000
    sqft_contrib = total_sqft * 115
    quality_contrib = overall_quality * 22000
    interaction_contrib = (total_sqft * overall_quality * 3.5)
    bathroom_contrib = bathrooms * 18000
    bedroom_contrib = bedrooms * 10000
    age_contrib = (year_built - 1900) * 950
    
    # Add random Gaussian noise (standard deviation of $25,000)
    noise = np.random.normal(0, 25000, num_samples)
    
    price = (
        base_price 
        + sqft_contrib 
        + quality_contrib 
        + interaction_contrib 
        + bathroom_contrib 
        + bedroom_contrib 
        + age_contrib 
        + noise
    )
    
    # Ensure minimum price is $30,000
    price = np.clip(price, 30000, None)
    price = np.round(price, -2) # Round to nearest hundred
    
    # Combine into a DataFrame
    df = pd.DataFrame({
        'TotalSqFt': total_sqft,
        'Bedrooms': bedrooms,
        'Bathrooms': bathrooms,
        'OverallQuality': overall_quality,
        'YearBuilt': year_built,
        'Price': price
    })
    
    # Save the data
    output_dir = 'data'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'housing_data.csv')
    df.to_csv(output_path, index=False)
    
    print(f"Successfully generated {num_samples} samples and saved to {output_path}")
    print(df.head())
    print("\nDataset Summary Statistics:")
    print(df.describe())

if __name__ == '__main__':
    generate_housing_data()
