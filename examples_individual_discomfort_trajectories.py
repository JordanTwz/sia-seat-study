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
                  "2:05", "2:25", "2:45", "3:05", "3:25", "3:45", "4:05",
                  "4:10", "4:30", "4:50", "5:10", "5:30", "5:50", "6:10"]

timestamps_hours = []
for t in timestamps_str:
    minutes = int(t.split(":")[0]) * 60 + int(t.split(":")[1])
    timestamps_hours.append(minutes / 60)

x_positions = np.arange(len(timestamps_str))

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
    ratings = row[timepoints].values.flatten() / 10.0
    legend_slope = row['slope_hour'].values[0] / 10.0
    plt.plot(x_positions, ratings, 'o-', color=colours[label],
             label=f"{label} (slope = {legend_slope:.2f}/hr)")
    
    slope = row['slope_hour'].values[0] / 10.0
    intercept = row['intercept'].values[0] / 10.0
    y_start = slope * timestamps_hours[0] + intercept
    y_end = slope * timestamps_hours[-1] + intercept
    y_line = np.linspace(y_start, y_end, len(x_positions))
    plt.plot(x_positions, y_line, '--',
             color=colours[label], alpha=0.8)

plt.xticks(x_positions, timestamps_str, rotation=45)
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
