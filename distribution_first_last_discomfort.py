import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.size"] = 14

# Load data
df = pd.read_excel('df_ratings_all (2).xlsx')

first = df['rating1'].dropna().to_numpy()
last  = df['rating21'].dropna().to_numpy()

median_first = int(np.median(first))
median_last  = int(np.median(last))

# 5-point bins from 10 to 80
bins = np.arange(10, 85, 5)

# Match reference aspect (983x629 @ 100 dpi)
fig, ax = plt.subplots(figsize=(9.83, 6.29), dpi=100)

# Blue = first, Red = last
ax.hist(first, bins=bins, color='tab:blue', edgecolor='black',
        alpha=0.35, label='First Rating')
ax.axvline(median_first, color='tab:blue', linestyle='--',
           linewidth=2, label=f'Median First = {median_first}')

ax.hist(last, bins=bins, color='tab:red', edgecolor='black',
        alpha=0.35, label='Last Rating')
ax.axvline(median_last, color='tab:red', linestyle='--',
           linewidth=2, label=f'Median Last = {median_last}')

ax.set_title('Distribution of First and Last Discomfort Ratings (n = 208)', fontsize=20)
ax.set_xlabel('Discomfort Rating', fontsize=16)
ax.set_ylabel('Number of Participants', fontsize=16)

ax.set_xticks(np.arange(10, 81, 5))
ax.set_xlim(8, 82)

ax.grid(True, which='both', linestyle=':', linewidth=1, alpha=0.5)
ax.legend(loc='upper right', frameon=True)

plt.savefig('distribution_first_last_discomfort.svg', format='svg', bbox_inches='tight')
plt.close(fig)
