import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.size"] = 14

# Load data
df = pd.read_excel('df_ratings_all (2).xlsx')

first = df['rating1'].dropna().to_numpy() / 10.0
last  = df['rating21'].dropna().to_numpy() / 10.0

median_first = np.median(first)
median_last  = np.median(last)

# 0.5-point bins from 1 to 8
bins = np.arange(1, 8.5, 0.5)

# Match reference aspect (983x629 @ 100 dpi)
fig, ax = plt.subplots(figsize=(9.83, 6.29), dpi=100)

# Blue = first, Red = last
ax.hist(first, bins=bins, color='tab:blue', edgecolor='black',
        alpha=0.35, label='First Rating')
ax.axvline(median_first, color='tab:blue', linestyle='--',
           linewidth=2, label=f'Median First = {median_first:.1f}')

ax.hist(last, bins=bins, color='tab:red', edgecolor='black',
        alpha=0.35, label='Last Rating')
ax.axvline(median_last, color='tab:red', linestyle='--',
           linewidth=2, label=f'Median Last = {median_last:.1f}')

ax.set_title('Distribution of First and Last Discomfort Ratings (n = 208)', fontsize=20)
ax.set_xlabel('Discomfort Rating', fontsize=16)
ax.set_ylabel('Number of Participants', fontsize=16)

ax.set_xticks(np.arange(1, 8.1, 0.5))
ax.set_xlim(0.8, 8.2)

ax.grid(True, which='both', linestyle=':', linewidth=1, alpha=0.5)
ax.legend(loc='upper right', frameon=True)

plt.savefig('distribution_first_last_discomfort.svg', format='svg', bbox_inches='tight')
plt.close(fig)
