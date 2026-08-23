"""
SEDS BPHC - Avionics Round 1 Induction Task
Task 1: Finding the Sea Floor

Name: <NITYA KAPOOR>
ID Number: <2025B5PS0551H>

What this script does
----------------------
1. Reads raw depth-sensor readings from Depth_Data.csv (one reading per second).
2. Cleans the data:
     - Any entry that isn't a valid number (e.g. "#VALUE!") is flagged as missing.
     - Any entry that is a physically implausible spike (a sudden jump that no
       real depth sensor would produce in one second) is also flagged as missing.
     - All flagged points are filled in by interpolating between their
       neighbours, so we never lose a timestamp, we just replace garbage
       with a sensible estimate.
3. Smooths the cleaned signal with a rolling-average low-pass filter to
   reduce the small random jitter that real sensors always add on top of
   the true signal ("brownie points" noise reduction).
4. Animates the depth-vs-time graph, revealing one new point per second,
   exactly like the ship's console would receive the data live.

Run it with:
    python depth_monitor.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# ---------------------------------------------------------------------------
# STEP 1: Grab the data
# ---------------------------------------------------------------------------
DATA_FILE = "Depth_Data.csv"
SAMPLE_RATE_HZ = 1  # sample data was recorded once every second

raw = pd.read_csv(DATA_FILE)

# The "Depth (m)" column is read as text because at least one row contains a
# corrupted string value instead of a number. Force it to numeric and turn
# anything that fails to parse (like "#VALUE!") into NaN so we can handle it
# the same way we handle any other bad reading.
depth_raw = pd.to_numeric(raw["Depth (m)"], errors="coerce")
time_s = np.arange(len(depth_raw)) / SAMPLE_RATE_HZ  # seconds since start

print(f"Loaded {len(depth_raw)} readings.")
print(f"Found {depth_raw.isna().sum()} unparseable (corrupted) reading(s).")

# ---------------------------------------------------------------------------
# STEP 2: Clean the erratic / corrupted data
# ---------------------------------------------------------------------------
# A depth sensor on a moving ship shouldn't jump by hundreds of metres in a
# single second. We flag any reading whose absolute change from the previous
# *valid* reading is unrealistically large, then treat it as missing data,
# exactly like the already-corrupted "#VALUE!" entries.
JUMP_THRESHOLD_M = 100  # max plausible change (m) between consecutive seconds

cleaned = depth_raw.copy()
diffs = cleaned.diff().abs()
outlier_mask = diffs > JUMP_THRESHOLD_M
print(f"Found {outlier_mask.sum()} outlier spike(s) beyond the {JUMP_THRESHOLD_M} m/s "
      f"jump threshold.")

cleaned[outlier_mask] = np.nan

# Fill every gap (corrupted values + spikes) by linearly interpolating
# between the nearest valid neighbours on either side. This keeps the
# timeline intact instead of deleting samples.
cleaned = cleaned.interpolate(method="linear", limit_direction="both")

# ---------------------------------------------------------------------------
# STEP 3: Reduce random sensor noise (brownie points)
# ---------------------------------------------------------------------------
# A rolling average smooths out the small random jitter that's always
# present in real sensor data, without lagging too far behind real changes
# in depth. Window of 5 seconds is a reasonable balance between smoothness
# and responsiveness for this data.
SMOOTH_WINDOW = 5
smoothed = cleaned.rolling(window=SMOOTH_WINDOW, center=True, min_periods=1).mean()

# ---------------------------------------------------------------------------
# STEP 4: Animate the depth-time graph, one new point per second
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6))

# Static (raw) line, shown faintly, so we can see how much cleaning helped.
raw_line, = ax.plot([], [], color="lightgray", linewidth=1, label="Raw sensor data")
smooth_line, = ax.plot([], [], color="#1f6feb", linewidth=2, label="Cleaned + smoothed depth")

ax.set_xlim(0, time_s[-1])
# Base the y-limits on the CLEANED data, not the raw data, so a single
# corrupted spike doesn't squash the whole graph.
ax.set_ylim(np.nanmin(cleaned) - 20, np.nanmax(cleaned) + 20)
ax.set_xlabel("Time (s)")
ax.set_ylabel("Depth (m, negative = below surface)")
ax.set_title("Odysseus' Ship - Sea Floor Depth Over Time")
ax.grid(True, alpha=0.3)
ax.legend(loc="upper right")

def init():
    raw_line.set_data([], [])
    smooth_line.set_data([], [])
    return raw_line, smooth_line

def update(frame):
    # frame goes from 0 to len(data)-1, revealing one extra point per call
    raw_line.set_data(time_s[:frame + 1], depth_raw.values[:frame + 1])
    smooth_line.set_data(time_s[:frame + 1], smoothed.values[:frame + 1])
    return raw_line, smooth_line

ani = animation.FuncAnimation(
    fig,
    update,
    frames=len(time_s),
    init_func=init,
    interval=1000,   # 1000 ms = 1 new point per second, matching the sample rate
    blit=True,
    repeat=False,
)

if __name__ == "__main__":
    # Save a GIF of the animation (useful for the README / submission)
    ani.save("depth_animation.gif", writer="pillow", fps=SAMPLE_RATE_HZ)

    # Save a final static snapshot showing the complete cleaned graph too
    raw_line.set_data(time_s, depth_raw.values)
    smooth_line.set_data(time_s, smoothed.values)
    ax.set_title("Odysseus' Ship - Sea Floor Depth Over Time (Full Journey)")
    fig.savefig("depth_full_graph.png", dpi=150, bbox_inches="tight")

    print("Saved depth_animation.gif and depth_full_graph.png")