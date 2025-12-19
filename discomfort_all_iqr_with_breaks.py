import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load fresh upload
file_path = "df_ratings_all (2).xlsx"
df = pd.read_excel(file_path)

# Rating columns excluding tea breaks (index 8 = rating9, index 14 = rating15)
rating_cols_all = [c for c in df.columns if c.startswith("rating")]
rating_columns = [col for i, col in enumerate(rating_cols_all) if i not in [8, 14]]

# Time points
time_points = np.array([0,20,40,60,80,100,120,145,165,185,205,225,245,270,290,310,330,350,370])
time_hours = time_points/60
time_labels = ["0:00","0:20","0:40","1:00","1:20","1:40","2:00",
               "2:25","2:45","3:05","3:25","3:45","4:05",
               "4:30","4:50","5:10","5:30","5:50","6:10"]

# Median & IQR
ratings = df[rating_columns].to_numpy(float)
median = np.nanmedian(ratings, axis=0)
q1 = np.nanpercentile(ratings, 25, axis=0)
q3 = np.nanpercentile(ratings, 75, axis=0)
n = ratings.shape[0]

# Build figure (same colours: lightblue fill + blue median)
plt.figure(figsize=(8,6))
plt.fill_between(time_hours, q1, q3, color='lightblue', alpha=0.4)
plt.plot(time_hours, median, color='tab:blue', linewidth=2.5)

# Arrow positions for 2:25 (index 7) and 4:30 (index 13), higher arrows
x1, y1 = time_hours[7], float(median[7])
x2, y2 = time_hours[13], float(median[13])

plt.annotate("Dip due to toilet break", xy=(x1, y1+0.3), xytext=(x1, y1+11),
             arrowprops=dict(arrowstyle='-|>', lw=1.3, color='black'),
             ha='center', va='bottom', fontsize=10)

plt.annotate("Dip due to toilet break", xy=(x2, y2+0.3), xytext=(x2, y2+11),
             arrowprops=dict(arrowstyle='-|>', lw=1.3, color='black'),
             ha='center', va='bottom', fontsize=10)

plt.title(f"Average Discomfort Rating (n={n})")
plt.xlabel("Time (hours)")
plt.ylabel("Average Discomfort rating")
plt.grid(True, alpha=0.3)
plt.xticks(time_hours, time_labels, rotation=45)

plt.tight_layout()

# Save SVG
svg_path = "discomfort_all_iqr_with_breaks.svg"
plt.savefig(svg_path, format="svg")
svg_path
