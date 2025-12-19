import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.size"] = 14

# Load dataset
file_path = 'df_ratings_all (2).xlsx'
data = pd.read_excel(file_path, sheet_name='df_ratings_all')

# Identify rating columns
timepoints = [col for col in data.columns if col.startswith('rating') and col[6:].isdigit()]

# Custom timestamps
timestamps_str = ["0:00", "0:20", "0:40", "1:00", "1:20", "1:40", "2:00",
                  "2:25", "2:45", "3:05", "3:25", "3:45", "4:05", "4:30",
                  "4:50", "5:10", "5:30", "5:50", "6:10"]

timestamps_hours = []
for t in timestamps_str:
    minutes = int(t.split(":")[0]) * 60 + int(t.split(":")[1])
    timestamps_hours.append(minutes / 60)

# Remove tea break ratings: rating8, rating14
rating_cols_no_breaks = timepoints.copy()
rating_cols_no_breaks.pop(7)   # rating8
rating_cols_no_breaks.pop(13)  # rating14

# Select representative examples
examples = {}
examples['Strong positive'] = data.loc[data['slope_hour'] == data['slope_hour'].max()]
examples['Mild positive']   = data.iloc[(data['slope_hour'] - data['slope_hour'].median()).abs().argsort()[:1]]
examples['Zero slope']      = data.iloc[(data['slope_hour']).abs().argsort()[:1]]
examples['Negative']        = data.loc[data['slope_hour'] == data['slope_hour'].min()]

# Colours consistent with earlier
colours = {
    'Strong positive': 'tab:blue',
    'Mild positive': 'tab:orange',
    'Zero slope': 'tab:green',
    'Negative': 'tab:red'
}

# Generate figure
plt.figure(figsize=(10,7))
for label, row in examples.items():
    ratings = row[rating_cols_no_breaks].values.flatten()
    plt.plot(timestamps_hours, ratings, 'o-', color=colours[label],
             label=f"{label} (slope={row['slope_hour'].values[0]:.2f}/hr)")
    
    slope = row['slope_hour'].values[0]
    intercept = row['intercept'].values[0]
    plt.plot(timestamps_hours, slope*np.array(timestamps_hours) + intercept, '--',
             color=colours[label], alpha=0.8)

plt.xticks(timestamps_hours, timestamps_str, rotation=45)
plt.xlabel('Time')
plt.ylabel('Discomfort Rating')
plt.title('Examples of Individual Discomfort Trajectories')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)

# Save as SVG
svg_path = 'examples_individual_discomfort_trajectories.svg'
plt.savefig(svg_path, format='svg', bbox_inches='tight')
plt.close()

svg_path
