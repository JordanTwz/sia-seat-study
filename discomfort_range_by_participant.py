import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.size"] = 14

# Load the uploaded Excel
file_path = "df_ratings_all (2).xlsx"
df = pd.read_excel(file_path, sheet_name="df_ratings_all")

# Compute min/max per participant from rating columns
rating_columns = [c for c in df.columns if c.startswith("rating")]
df["min"] = df[rating_columns].min(axis=1)
df["max"] = df[rating_columns].max(axis=1)

# Sort by maximum discomfort
df_sorted = df.sort_values(by="max", ascending=False).reset_index(drop=True)

# Create the plot
fig, ax = plt.subplots(figsize=(14, 6))
for idx, row in df_sorted.iterrows():
    if row["min"] == row["max"]:
        ax.hlines(y=row["min"], xmin=idx - 0.3, xmax=idx + 0.3,
                  color='black', linewidth=1.2, linestyle='dashed')
    else:
        ax.vlines(x=idx, ymin=row["min"], ymax=row["max"],
                  color='black', linewidth=1.5)

# Axis styling (axes a different color than lines)
ax.set_xlim(-0.5, len(df_sorted) - 0.5)
ax.set_ylim(5, 80)
ax.set_yticks([5, 10, 20, 30, 40, 50, 60, 70, 80])
ax.tick_params(axis='x', colors='black')
ax.tick_params(axis='y', colors='black')
ax.set_xlabel('Participant Number (ranked by maximum discomfort)', fontsize=18, color='black')
ax.set_ylabel('Subjective Discomfort Ratings', fontsize=18, color='black')
ax.set_title('Discomfort Range by Participant (n = 208)', fontsize=18, color='black')
ax.grid(axis='y', linestyle='--', alpha=0.4)

plt.tight_layout()

# Save as SVG
svg_path = "discomfort_range_by_participant.svg"
fig.savefig(svg_path, format="svg")

svg_path
