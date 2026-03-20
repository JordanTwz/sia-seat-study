import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.size"] = 14
import matplotlib.dates as mdates
from datetime import datetime, timedelta


def parse_time(time_str):
    return datetime.strptime(time_str, "%H:%M")

# Define key events with times
events = [
    ("Start protocol\n(CCTV, IFE, GCR timer)", "12:30"),
    ("Break 1 (2h)", "14:30"),
    ("Break 2 (4h 05m)", "16:35"),
    ("Session end\n(Final entry, stop devices)", "18:40")
]

# Convert to datetime objects
start_time = parse_time("12:30")
end_time = parse_time("18:40")

rating_time_strings = [
    "12:50",
    "13:10",
    "13:30",
    "13:50",
    "14:10",
    "14:35",
    "14:55",
    "15:15",
    "15:35",
    "15:55",
    "16:15",
    "16:40",
    "17:00",
    "17:20",
    "17:40",
    "18:00",
    "18:20",
]
rating_times = [parse_time(t) for t in rating_time_strings]


def format_elapsed_label(t):
    elapsed = t - start_time
    total_minutes = int(elapsed.total_seconds() // 60)
    hours, minutes = divmod(total_minutes, 60)
    return f"{hours}:{minutes:02d}"

# Plot setup
fig, ax = plt.subplots(figsize=(12, 3))

# Draw central timeline
ax.hlines(0, start_time, end_time, color="black", linewidth=1.5)

# Add main events (all above the line)
for label, t_str in events:
    t = parse_time(t_str)
    ax.plot(t, 0, "o", color="black", markersize=6, zorder=3)
    ax.vlines(t, 0, 1.0, color="black", linestyle="--", linewidth=0.8)
    ax.text(t, 1.2, label, ha="center", va="center",
            fontsize=13, bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="black"))

# Label the first and last black dots with elapsed timestamps.
for t in (start_time, end_time):
    ax.text(
        t,
        -0.16,
        format_elapsed_label(t),
        ha="center",
        va="top",
        fontsize=11,
        color="black",
    )

# Add discomfort rating indicators (primary DV)
ax.plot(rating_times, [0]*len(rating_times), "o", color="crimson", markersize=4, label="Discomfort Ratings", zorder=2)

# Label each red dot with its elapsed timestamp.
for t in rating_times:
    ax.text(
        t,
        -0.16,
        format_elapsed_label(t),
        ha="center",
        va="top",
        fontsize=11,
        color="black",
    )

# Add label for discomfort ratings (below the line)
ax.text(
    start_time + timedelta(minutes=10),
    -0.55,
    "Discomfort ratings (every 20 minutes)\nA total of 21 ratings per participant",
    ha="left",
    va="top",
    fontsize=13,
    color="crimson",
)

# Format x-axis
ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
ax.spines["bottom"].set_position(("outward", 24))
ax.tick_params(axis="x", pad=8)
ax.set_ylim(-0.8, 1.5)
ax.set_yticks([])
ax.set_title("Experimental Protocol Timeline", fontsize=16, pad=2)
ax.set_xlabel("Time", labelpad=10)

# Clean frame
for spine in ["left", "right", "top"]:
    ax.spines[spine].set_visible(False)

plt.tight_layout()
plt.savefig("timeline.svg", format="svg", bbox_inches="tight")
plt.close(fig)
