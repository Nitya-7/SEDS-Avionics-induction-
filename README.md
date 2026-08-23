# SEDS-Avionics-induction
induction task 
# SEDS BPHC — Avionics Round 1 Induction Task: Athena's Intern

**NITYA KAPOOR:** <YOUR NAME HERE>
**2025B5A3PS0551H:** <YOUR ID HERE>

## Task 1: Finding the Sea Floor (`depth_monitor.py`)

- **Grab the data:** `Depth_Data.csv` is loaded with pandas. The `Depth (m)` column
  is read as text because one row (`Point 97`) contains a corrupted `#VALUE!`
  entry instead of a number — this is coerced to `NaN` with `pd.to_numeric(...,
  errors="coerce")`.
- **Handle erratic data:** Beyond the one corrupted cell, the raw data also has a
  few physically impossible spikes (e.g. a jump to −1271 m and a snap to 0 m in a
  single second — no real ship depth-sounder would do that). Any reading whose
  change from the previous point exceeds a 100 m/s jump threshold is flagged and
  treated as missing, then filled in with linear interpolation from its
  neighbours so the timeline stays continuous.
- **Noise reduction (brownie points):** After cleaning, a 5-second centered
  rolling average is applied to smooth out the small random jitter that's
  always present in real sensor readings.
- **Animation:** `matplotlib.animation.FuncAnimation` reveals one new data point
  per second (`interval=1000`), matching the stated 1 Hz sample rate — both the
  raw signal (faint gray) and the cleaned/smoothed signal (blue) are shown so the
  effect of the cleaning step is visible.
- **Outputs:** `depth_full_graph.png` (final static graph) and
  `depth_animation.gif` (recording of the live animation), both attached as
  screenshots per the submission instructions.

Run it with:

pip install pandas numpy matplotlib
python depth_monitor.py


## Task 2: Keeping Watch Over Odysseus (`odysseus_watch.ino`)

*(coming soon)*

## Repo contents
