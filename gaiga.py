import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load your dataset (assuming a CSV or similar file)
data = pd.read_csv('gaia.csv')

# Basic settings for seaborn visualizations
sns.set(style="whitegrid")

# Filter relevant columns based on actual dataset column names
columns_of_interest = [
    'sy_snum', 'sy_pnum', 'pl_massj', 
    'pl_radj', 'pl_orbper', 'st_mass', 
    'st_rad', 'st_teff', 'pl_orbeccen'
]

# Drop any missing data rows for simplicity
data_filtered = data[columns_of_interest].dropna()

# Create a list to store the titles and plot functions
visualizations = [
    {
        'title': 'Distribution of Planet Mass (Jupiter Mass)',
        'plot_func': lambda ax: sns.histplot(data_filtered['pl_massj'], kde=True, color='skyblue', ax=ax)
    },
    {
        'title': 'Planet Mass vs Radius',
        'plot_func': lambda ax: sns.scatterplot(x='pl_massj', y='pl_radj', data=data_filtered, ax=ax)
    },
    {
        'title': 'Distribution of Orbital Period (days)',
        'plot_func': lambda ax: sns.histplot(data_filtered['pl_orbper'], kde=True, color='coral', ax=ax)
    },
    {
        'title': 'Correlation Heatmap of Stellar Properties',
        'plot_func': lambda ax: sns.heatmap(data_filtered[['st_mass', 'st_rad', 'st_teff', 'pl_orbeccen']].corr(), annot=True, cmap='coolwarm', ax=ax)
    },
    {
        'title': 'Stellar Mass vs Stellar Radius',
        'plot_func': lambda ax: sns.scatterplot(x='st_mass', y='st_rad', data=data_filtered, hue='pl_orbeccen', ax=ax)
    },
    {
        'title': 'Boxplot of Eccentricity Values',
        'plot_func': lambda ax: sns.boxplot(data=data_filtered, x='pl_orbeccen', ax=ax)
    },
    {
        'title': 'Distribution of Stellar Effective Temperature',
        'plot_func': lambda ax: sns.histplot(data_filtered['st_teff'], kde=True, color='purple', ax=ax)
    },
    {
        'title': 'Orbital Period vs Planet Radius',
        'plot_func': lambda ax: sns.scatterplot(x='pl_orbper', y='pl_radj', data=data_filtered, ax=ax)
    }
]

# Loop through each visualization and create separate figures
for viz in visualizations:
    plt.figure(figsize=(10, 8))
    ax = plt.gca()  # Get the current axis
    viz['plot_func'](ax)  # Call the plot function
    ax.set_title(viz['title'])
    plt.tight_layout()  # Adjust layout to prevent overlap

# Display all plots at once
plt.show()