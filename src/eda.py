import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def perform_eda():
    """
    Performs Exploratory Data Analysis (EDA) on the housing dataset.
    Generates and saves premium visualizations.
    """
    # Load dataset
    input_path = 'data/housing_data.csv'
    if not os.path.exists(input_path):
        print(f"Error: Dataset {input_path} not found. Please run generate_data.py first.")
        return

    df = pd.read_csv(input_path)
    
    # Ensure plots directory exists
    plots_dir = 'plots'
    os.makedirs(plots_dir, exist_ok=True)
    
    # Set seaborn style and palette for premium aesthetics
    sns.set_theme(style="whitegrid")
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
    
    # Define harmonious dark-palette colors
    primary_color = "#1f77b4" # Premium blue
    accent_color = "#ff7f0e"  # Soft orange/coral
    
    # ----------------------------------------------------
    # Plot 1: Correlation Matrix Heatmap
    # ----------------------------------------------------
    plt.figure(figsize=(8, 6))
    corr = df.corr()
    mask = corr.copy()
    
    # Draw correlation heatmap
    sns.heatmap(
        corr, 
        annot=True, 
        fmt=".2f", 
        cmap="coolwarm", 
        linewidths=1, 
        cbar=True,
        square=True
    )
    plt.title('Feature Correlation Matrix Heatmap', fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()
    heatmap_path = os.path.join(plots_dir, 'correlation_heatmap.png')
    plt.savefig(heatmap_path, dpi=300)
    plt.close()
    print(f"Saved correlation heatmap to {heatmap_path}")
    
    # ----------------------------------------------------
    # Plot 2: Price vs. TotalSqFt Scatter Plot
    # ----------------------------------------------------
    plt.figure(figsize=(9, 6))
    
    # Scatter plot with regression line and transparency for high density
    sns.regplot(
        data=df, 
        x='TotalSqFt', 
        y='Price', 
        scatter_kws={'alpha':0.5, 'color': primary_color, 'edgecolor': 'w', 'linewidths': 0.5},
        line_kws={'color': accent_color, 'linewidth': 2}
    )
    
    # Formatting
    plt.title('House Price vs. Total Square Footage', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Total Square Footage (SqFt)', fontsize=11)
    plt.ylabel('Price ($)', fontsize=11)
    
    # Format y-axis values with currency format
    ax = plt.gca()
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    
    plt.tight_layout()
    scatter_path = os.path.join(plots_dir, 'price_vs_sqft.png')
    plt.savefig(scatter_path, dpi=300)
    plt.close()
    print(f"Saved scatter plot to {scatter_path}")
    
    # ----------------------------------------------------
    # Plot 3: Price vs. OverallQuality Boxplot/Scatter
    # ----------------------------------------------------
    plt.figure(figsize=(9, 6))
    
    # Combining Boxplot with Stripplot for premium visualization
    sns.boxplot(
        data=df, 
        x='OverallQuality', 
        y='Price', 
        palette="Blues",
        fliersize=0, # Hide outliers in boxplot to avoid double drawing
        linewidth=1.2
    )
    
    # Overlay individual data points
    sns.stripplot(
        data=df, 
        x='OverallQuality', 
        y='Price', 
        color="#17a2b8", 
        alpha=0.3, 
        jitter=0.2, 
        size=4,
        linewidth=0
    )
    
    plt.title('House Price Distribution by Overall Quality Rating', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Overall Quality Rating (1 - 10)', fontsize=11)
    plt.ylabel('Price ($)', fontsize=11)
    
    ax = plt.gca()
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    
    plt.tight_layout()
    quality_path = os.path.join(plots_dir, 'price_vs_quality.png')
    plt.savefig(quality_path, dpi=300)
    plt.close()
    print(f"Saved quality distribution plot to {quality_path}")
    
    print("\nEDA Completed successfully. All plots have been generated.")

if __name__ == '__main__':
    perform_eda()
