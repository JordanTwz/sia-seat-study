import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.size"] = 14

# Load data
df = pd.read_excel("df_ratings_all (2).xlsx")

# Rating columns (include tea breaks)
rating_columns = [c for c in df.columns if c.startswith("rating")]

# Time points
time_labels = ["0:00","0:20","0:40","1:00","1:20","1:40","2:00",
               "2:05","2:25","2:45","3:05","3:25","3:45","4:05",
               "4:10","4:30","4:50","5:10","5:30","5:50","6:10"]
x_positions = np.arange(len(time_labels))

# WHO BMI grouping
df["BMI_group"] = np.where(df["BMI"] < 25, "Low BMI", "High BMI")

groups = [
    ("Female", "Low BMI"),
    ("Male", "Low BMI"),
    ("Female", "High BMI"),
    ("Male", "High BMI")
]

# Create 2x2 figure
fig, axes = plt.subplots(2, 2, figsize=(14, 8), sharey=True)

for ax, (gender, bmi_group) in zip(axes.flat, groups):
    subset = df[(df["Gender"] == gender) & (df["BMI_group"] == bmi_group)]
    data = subset[rating_columns].to_numpy(float)
    n = data.shape[0]

    median = np.nanmedian(data, axis=0) / 10.0
    q1 = np.nanpercentile(data, 25, axis=0) / 10.0
    q3 = np.nanpercentile(data, 75, axis=0) / 10.0

    ax.fill_between(x_positions, q1, q3, color="lightblue", alpha=0.4)
    ax.plot(x_positions, median, color="tab:blue", linewidth=2.5)

    ax.set_title(f"{gender} - {bmi_group} (n = {n})")
    ax.set_xticks(x_positions)
    ax.set_xticklabels(time_labels, rotation=45)
    ax.grid(True, alpha=0.3)

# Shared labels
fig.text(0.5, 0.04, "Time (hours)", ha="center")
fig.text(0.04, 0.5, "Average Discomfort rating",
         va="center", rotation="vertical")

plt.suptitle("Median Discomfort Trajectories by Gender and BMI Group")
plt.tight_layout(rect=[0.05, 0.05, 1, 0.95])

# Save as SVG
plt.savefig("median_iqr_2x2_gender_bmi.svg", format="svg")
