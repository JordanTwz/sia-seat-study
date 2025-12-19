import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the file
df = pd.read_excel('df_ratings_all (2).xlsx')

# Compute slope_hour if necessary
if 'slope_hour' not in df.columns and 'slope' in df.columns:
    df['slope_hour'] = df['slope'] * 60

# Clean missing
df_clean = df[df['slope_hour'].notna() & df['significant'].notna()]

# Split groups
slopes_nonsig = df_clean[df_clean['significant'] == False]['slope_hour']
slopes_sig = df_clean[df_clean['significant'] == True]['slope_hour']

# Bins
bins = np.linspace(df_clean['slope_hour'].min(), df_clean['slope_hour'].max(), 20)

# Plot
plt.figure(figsize=(8, 6))
plt.hist(slopes_nonsig, bins=bins, alpha=0.6, label='Not Significant', color='tab:red', edgecolor='black')
plt.hist(slopes_sig, bins=bins, alpha=0.6, label='Significant', color='tab:blue', edgecolor='black')

plt.title('Distribution of Slopes')
plt.xlabel('Discomfort Accumulation Rate (points/hour)')
plt.ylabel('Frequency')
plt.legend()
plt.tight_layout()

# Save SVG
svg_path = "distribution_of_slopes.svg"
plt.savefig(svg_path, format="svg")

svg_path
