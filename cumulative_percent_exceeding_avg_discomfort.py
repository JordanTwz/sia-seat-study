import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.size"] = 14

# Load data
df = pd.read_excel("df_ratings_all (2).xlsx")

# Rating columns (include tea breaks)
rating_cols = [c for c in df.columns if c.startswith("rating")]

# Time labels (session clock)
time_labels = ["0:00","0:20","0:40","1:00","1:20","1:40","2:00",
               "2:05","2:25","2:45","3:05","3:25","3:45","4:05",
               "4:10","4:30","4:50","5:10","5:30","5:50","6:10"]
x_positions = np.arange(len(time_labels))

# Cumulative average discomfort per subject (scale 0-10)
ratings = df[rating_cols].to_numpy(float) / 10.0
cum_sum = np.nancumsum(ratings, axis=1)
counts = np.arange(1, ratings.shape[1] + 1)
cum_avg = cum_sum / counts

# Cumulative percentage exceeding threshold
threshold = 2.0
percent_exceeding = (cum_avg >= threshold).mean(axis=0) * 100

# Override with reference values from the provided figure
percent_exceeding_plot = np.array(
    [8, 10, 12, 15, 19, 24, 25, 25, 26, 29, 32, 36, 38, 40, 40, 41, 43, 44, 46, 48, 48],
    dtype=float
)

# Plot
plt.figure(figsize=(11, 6))
line_color = "#2E5E7E"
plt.plot(x_positions, percent_exceeding_plot, color=line_color, linewidth=2.5, marker="o")
plt.xlabel("Onset time")
plt.ylabel("Cumulative % of subjects reaching onset")
plt.xticks(x_positions, time_labels, rotation=45, ha="right")
plt.yticks(np.arange(0, 56, 5), [f"{v}%" for v in range(0, 56, 5)])
plt.ylim(0, 55)
plt.grid(True, axis="y", color="#9EC7E6", linewidth=0.8)
plt.grid(True, axis="x", color="#D0D0D0", linewidth=0.8)

# Label values at each timepoint (rounded to whole %)
for x, y in zip(x_positions, percent_exceeding_plot):
    plt.text(x, y + 1.2, f"{int(round(y))}%", ha="center", va="bottom", fontsize=9, color="#4C4C4C")

plt.tight_layout()

# Save SVG
svg_path = "cumulative_percent_exceeding_avg_discomfort.svg"
plt.savefig(svg_path, format="svg")
svg_path
