import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.size"] = 16

# Load data
df = pd.read_excel('df_ratings_all (2).xlsx')

# Define rating columns excluding tea-breaks
all_ratings = [f"rating{i}" for i in range(1, 22)]
rating_cols = [r for r in all_ratings if r not in ('rating8', 'rating15')]

# Custom timestamps
timestamps = [
    "0:00", "0:20", "0:40", "1:00", "1:20", "1:40", "2:00",
    "2:25", "2:45", "3:05", "3:25", "3:45", "4:05", "4:30",
    "4:50", "5:10", "5:30", "5:50", "6:10"
]
x = np.arange(len(rating_cols))

# Dip indices
dip_indices = {7: 0.1, 13: 0.1}
arrowprops = dict(arrowstyle='->', color='black', linewidth=1.6, shrinkA=0, shrinkB=0)

# Journal font sizes
TITLE_FONTSIZE = 25
LABEL_FONTSIZE = 23
TICK_FONTSIZE = 21
ANNOT_FONTSIZE = 21

# --- Split groups ---
df_scaled = df.copy()
df_scaled[rating_cols] = df_scaled[rating_cols] / 10.0

sig_pos = df_scaled[(df_scaled['significant'] == True) & (df_scaled['slope_hour'] > 0)]
sig_other = df_scaled[~((df_scaled['significant'] == True) & (df_scaled['slope_hour'] > 0))]

avg_pos = sig_pos[rating_cols].mean(axis=0)
avg_other = sig_other[rating_cols].mean(axis=0)

# Create SVG figure
fig, axes = plt.subplots(1, 2, figsize=(22, 9), sharey=True)

# ---- LEFT PANEL: significant ↑ ----
for _, row in sig_pos.iterrows():
    axes[0].plot(x, row[rating_cols], color='gray', linewidth=1, alpha=0.3)
axes[0].plot(x, avg_pos, color='green', linewidth=3, label='Average')

for idx, shift in dip_indices.items():
    xi = x[idx] + shift
    yi = avg_pos[idx]
    axes[0].annotate(
        "Dip due to toilet break", 
        xy=(xi, yi), 
        xytext=(xi, yi + 0.7),
        ha='center',
        fontsize=ANNOT_FONTSIZE,
        arrowprops=arrowprops
    )

axes[0].legend(frameon=False, fontsize=TICK_FONTSIZE)
axes[0].set_title("Subjects with Statistically Significant Increase (n = 152)", fontsize=TITLE_FONTSIZE)
axes[0].set_ylabel("Discomfort rating", fontsize=LABEL_FONTSIZE)
axes[0].tick_params(axis='both', labelsize=TICK_FONTSIZE)
axes[0].set_xticks(x)
axes[0].set_xticklabels(timestamps, rotation=45, fontsize=TICK_FONTSIZE)

# ---- RIGHT PANEL: non-significant/↓ ----
for _, row in sig_other.iterrows():
    axes[1].plot(x, row[rating_cols], color='gray', linewidth=1, alpha=0.3)
axes[1].plot(x, avg_other, color='red', linewidth=3, label='Average')

for idx, shift in dip_indices.items():
    xi = x[idx] + shift
    yi = avg_other[idx]
    axes[1].annotate(
        "Dip due to toilet break", 
        xy=(xi, yi), 
        xytext=(xi, yi + 0.7),
        ha='center',
        fontsize=ANNOT_FONTSIZE,
        arrowprops=arrowprops
    )

axes[1].legend(frameon=False, fontsize=TICK_FONTSIZE)
axes[1].set_title("Subjects with Non-Significant or Decreasing Discomfort (n = 56)", fontsize=TITLE_FONTSIZE)
axes[1].tick_params(axis='both', labelsize=TICK_FONTSIZE)
axes[1].set_xticks(x)
axes[1].set_xticklabels(timestamps, rotation=45, fontsize=TICK_FONTSIZE)

plt.tight_layout()

svg_path = "discomfort_significance.svg"
plt.savefig(svg_path, format="svg")
plt.close(fig)

svg_path
