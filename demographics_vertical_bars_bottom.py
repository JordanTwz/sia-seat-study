import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

DF_ALL_PATH  = "df_ratings_all (2).xlsx"   # has Age/Height/Weight/BMI + Gender
DF_MELT_PATH = "df_ratings_melt.xlsx"      # has subject, Gender, past_flights, sitting_duration

df = pd.read_excel(DF_ALL_PATH)
df_melt = pd.read_excel(DF_MELT_PATH)

colors = {'Female': '#FFA500', 'Male': '#ADD8E6'}  # orange, light blue (exact hex)
unit_map = {'Age': '(years)', 'Height': '(cm)', 'Weight': '(kg)', 'BMI': '(kg/m²)'}

past_counts = (
    df_melt.groupby(['past_flights', 'Gender'])['subject']
    .nunique()
    .unstack(fill_value=0)
)
sit_counts = (
    df_melt.groupby(['sitting_duration', 'Gender'])['subject']
    .nunique()
    .unstack(fill_value=0)
)

past_cats = past_counts.index.tolist()
sit_cats  = sit_counts.index.tolist()

metrics = ['Weight', 'BMI', 'Age', 'Height', 'Past Flights', 'Sitting Duration']

fig, axes = plt.subplots(nrows=6, ncols=2, figsize=(12, 24), constrained_layout=True)

for row_idx, metric in enumerate(metrics):

    # For continuous vars: precompute SHARED bins across sexes
    if metric not in ['Past Flights', 'Sitting Duration']:
        all_data = df[metric].dropna()
        shared_bins = np.histogram_bin_edges(all_data, bins=20)  # SAME breakpoints for both sexes

    for col_idx, gender in enumerate(['Female', 'Male']):
        ax = axes[row_idx, col_idx]

        if metric == 'Past Flights':
            x = np.arange(len(past_cats))
            ax.bar(x, past_counts[gender].reindex(past_cats).values,
                   color=colors[gender], edgecolor='black')
            ax.set_xticks(x)
            ax.set_xticklabels(past_cats, rotation=45, ha='right')
            ax.set_xlabel('Past Flights')
            ax.set_ylabel('Number of Participants')

        elif metric == 'Sitting Duration':
            x = np.arange(len(sit_cats))
            ax.bar(x, sit_counts[gender].reindex(sit_cats).values,
                   color=colors[gender], edgecolor='black')
            ax.set_xticks(x)
            ax.set_xticklabels(sit_cats, rotation=45, ha='right')
            ax.set_xlabel('Sitting Duration')
            ax.set_ylabel('Number of Participants')

        else:
            data = df[df['Gender'] == gender][metric].dropna()

            # SAME bins + SAME x-range across sexes
            ax.hist(data, bins=shared_bins, color=colors[gender], edgecolor='black')
            ax.set_xlim(shared_bins[0], shared_bins[-1])

            # Median line + numeric label
            med = data.median()
            ax.axvline(med, color='red', linestyle='--', linewidth=1.5)
            y_max = ax.get_ylim()[1]
            ax.text(med, y_max * 0.9, f'{med:.1f}',
                    color='red', rotation=90,
                    ha='right', va='center',
                    backgroundcolor='white')

            ax.set_xlabel(f'{metric} {unit_map.get(metric, "")}')
            ax.set_ylabel('Count')

        ax.set_title(f'{metric} ({gender})')


    # Align Y-scale within each row (Female vs Male)
    ax_f = axes[row_idx, 0]
    ax_m = axes[row_idx, 1]
    ymax = max(ax_f.get_ylim()[1], ax_m.get_ylim()[1])
    ax_f.set_ylim(0, ymax)
    ax_m.set_ylim(0, ymax)

fig.savefig("demographics_vertical_bars_bottom.svg", format="svg", bbox_inches="tight")

