import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.size"] = 14

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

# Divide x-axis values by 10 for plotting
slopes_nonsig_plot = slopes_nonsig / 10
slopes_sig_plot = slopes_sig / 10

# Bins
bins = np.linspace((df_clean['slope_hour'] / 10).min(), (df_clean['slope_hour'] / 10).max(), 20)

# Plot
plt.figure(figsize=(8, 6))
plt.hist(slopes_nonsig_plot, bins=bins, alpha=0.6, label='Not Significant', color='tab:red', edgecolor='black')
plt.hist(slopes_sig_plot, bins=bins, alpha=0.6, label='Significant', color='tab:blue', edgecolor='black')

plt.title('Distribution of Slopes')
plt.xlabel('Discomfort Accumulation Rate')
plt.ylabel('Frequency')
plt.legend()
plt.tight_layout()

# Save SVG
svg_path = "distribution_of_slopes.svg"
plt.savefig(svg_path, format="svg")

svg_path
