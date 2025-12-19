import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# Define key events with times (all above the line)
events = [
    ("Start protocol\n(CCTV, IFE, GCR timer)", "2025-10-01 12:30"),
    ("Break 1 (2h)", "2025-10-01 14:30"),
    ("Break 2 (4h 05m)", "2025-10-01 16:50"),  # align exactly with a 20-min interval
    ("Session end\n(Final entry, stop devices)", "2025-10-01 18:40")
]

# Convert to datetime objects
start_time = datetime.strptime("2025-10-01 12:30", "%Y-%m-%d %H:%M")
end_time = datetime.strptime("2025-10-01 18:40", "%Y-%m-%d %H:%M")

# Define break intervals (5 min duration each)
breaks = [
    (datetime.strptime("2025-10-01 14:30", "%Y-%m-%d %H:%M"),
     datetime.strptime("2025-10-01 14:35", "%Y-%m-%d %H:%M")),
    (datetime.strptime("2025-10-01 16:35", "%Y-%m-%d %H:%M"),
     datetime.strptime("2025-10-01 16:40", "%Y-%m-%d %H:%M"))
]

# Generate discomfort rating intervals every 20 minutes (excluding breaks)
rating_times = []
t = start_time + timedelta(minutes=20)
while t <= end_time:
    if not any(b[0] <= t <= b[1] for b in breaks):
        rating_times.append(t)
    t += timedelta(minutes=20)

# Find the nearest discomfort time for Break 2 (so it's exactly aligned)
break2_time = min(rating_times, key=lambda x: abs(x - datetime.strptime("2025-10-01 16:35", "%Y-%m-%d %H:%M")))
events[2] = ("Break 2 (4h 05m)", break2_time.strftime("%Y-%m-%d %H:%M"))

# Plot setup
fig, ax = plt.subplots(figsize=(12, 3))

# Draw central timeline
ax.hlines(0, start_time, end_time, color="black", linewidth=1.5)

# Add main events (all above the line)
for label, t_str in events:
    t = datetime.strptime(t_str, "%Y-%m-%d %H:%M")
    ax.plot(t, 0, "o", color="black", markersize=6, zorder=3)
    ax.vlines(t, 0, 1.0, color="black", linestyle="--", linewidth=0.8)
    ax.text(t, 1.2, label, ha="center", va="center",
            fontsize=9, bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="black"))

# Add discomfort rating indicators (primary DV)
ax.plot(rating_times, [0]*len(rating_times), "o", color="crimson", markersize=4, label="Discomfort Ratings", zorder=2)

# Add label for discomfort ratings (below the line)
ax.text(start_time + timedelta(minutes=60), -0.5, "Discomfort Ratings (every 20 min)",
        ha="left", va="center", fontsize=9, color="crimson")

# Format x-axis
ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
ax.set_ylim(-0.8, 1.5)
ax.set_yticks([])
ax.set_title("Experimental Protocol Timeline", fontsize=12)
ax.set_xlabel("Time")

# Clean frame
for spine in ["left", "right", "top"]:
    ax.spines[spine].set_visible(False)

plt.tight_layout()
plt.show()
