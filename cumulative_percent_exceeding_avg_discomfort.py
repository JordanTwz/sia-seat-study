import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.size"] = 14

# Load data
df = pd.read_excel("df_ratings_all (2).xlsx")

# Rating columns in session order
rating_cols = sorted(
    [c for c in df.columns if c.startswith("rating")],
    key=lambda c: int(c.replace("rating", ""))
)

# Session clock labels including the 5-minute tea breaks
time_labels = ["0:00", "0:20", "0:40", "1:00", "1:20", "1:40", "2:00",
               "2:05", "2:25", "2:45", "3:05", "3:25", "3:45", "4:05",
               "4:10", "4:30", "4:50", "5:10", "5:30", "5:50", "6:10"]

# Match the notebook onset rule: current rating must be >= 20 and the next
# rating must be > 20. This records one onset time per subject.
ratings = df[rating_cols].to_numpy(dtype=float)
threshold = 20.0
onset_indices = []
for subject_ratings in ratings:
    onset_idx = None
    for i in range(len(rating_cols) - 1):
        if subject_ratings[i] >= threshold and subject_ratings[i + 1] > threshold:
            onset_idx = i
            break
    onset_indices.append(onset_idx)

onset_series = pd.Series(onset_indices, dtype="Int64").dropna().astype(int)
onset_counts = onset_series.value_counts().sort_index().reindex(
    range(len(time_labels)),
    fill_value=0,
)
onset_time_labels = time_labels
frequency = onset_counts.to_numpy(dtype=int)
cum_freq = np.cumsum(frequency)
percent_reaching_onset = np.round(cum_freq / len(df) * 100, 0)
x_positions = np.arange(len(onset_time_labels))

# Plot
fig, ax = plt.subplots(figsize=(11, 6))
line_color = "#2E5E7E"

ax.plot(
    x_positions,
    percent_reaching_onset,
    color=line_color,
    linewidth=2.8,
    marker="o",
    markersize=8,
)

ax.set_xlabel("Onset time")
ax.set_ylabel("Cumulative % of subjects reaching onset")
ax.set_xticks(x_positions)
ax.set_xticklabels(onset_time_labels, rotation=45, ha="right")
ax.set_yticks(np.arange(0, 61, 5))
ax.set_yticklabels([f"{v}%" for v in range(0, 61, 5)])
ax.set_ylim(0, 60)
ax.set_xlim(-0.25, len(x_positions) - 0.75)
ax.grid(True, axis="y", color="#9EC7E6", linewidth=0.9)
ax.grid(True, axis="x", color="#D0D0D0", linewidth=0.8)

for x, y in zip(x_positions, percent_reaching_onset):
    ax.text(
        x,
        y + 1.3,
        f"{int(round(y))}%",
        ha="center",
        va="bottom",
        fontsize=9,
        color="#4C4C4C",
    )

fig.tight_layout()

# Save SVG
svg_path = "cumulative_percent_exceeding_avg_discomfort.svg"
fig.savefig(svg_path, format="svg")
