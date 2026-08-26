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

# Keeping Watch Over Odysseus ⛵

An Arduino-based embedded state machine simulation built in Tinkercad. This system monitors environmental threats to Odysseus's ship—such as impending storms and the mythical sea monster Charybdis—displaying status updates in real time on an LCD screen and allowing crew manual override controls via an anchor mechanism.

---

## 📌 Project Overview

The objective of this project is to implement an automated monitoring system using an **Arduino Uno** to track ship status through various environmental inputs and visual/auditory outputs.

### State Machine Architecture
The system operates using a multi-state finite state machine (FSM):

* **`OPEN SEA`** *(Default)*: The ship is sailing normally. This is the initial state.
* **`STORM`**: Triggered when the light sensor (LDR) falls below **50% threshold**. The onboard LED blinks continuously.
* **`CHARYBDIS`**: Triggered when the ultrasonic distance sensor detects an object closer than **100 cm**. The buzzer sounds continuously.
* **`ANCHOR DROPPED`**: Triggered by pressing the push button. The ship enters a protected state immune to all environmental hazards. Pressing the button again raises the anchor and returns to normal checks.
* **`WRECKED`**: If the ship remains in either `STORM` or `CHARYBDIS` continuously for **5 seconds**, it transitions to `WRECKED`. Once wrecked, the system locks until the simulation is restarted. (Dropping the anchor before 5 seconds resets the timer).

> **Conflict Resolution**: If `STORM` and `CHARYBDIS` conditions are met simultaneously at startup or during execution, whichever state is checked first in the FSM logic takes priority and holds active state.

---

## 🛠️ Hardware Component List

* **Microcontroller**: 1x Arduino Uno R3
* **Sensors**:
  * 1x Ultrasonic Distance Sensor (HC-SR04)
  * 1x Photoresistor (Light Sensor / LDR)
* **Outputs**:
  * 1x 16x2 LCD Display
  * 1x LED
  * 1x Piezo Buzzer
* **Inputs**:
  * 1x Push Button
* **Passive Components**:
  * 1x 10kΩ Potentiometer (LCD contrast control)
  * Current-limiting resistors (for LED & Push Button)

---

## 🔌 Sensor Thresholds

| Threat Parameter | Condition | Sensor Used | Active Output |
| :--- | :--- | :--- | :--- |
| **Storm** | Light level < 50% | Photoresistor (LDR) | LED Blinks |
| **Charybdis** | Distance < 100 cm | Ultrasonic Sensor | Buzzer Sounds |

---

## 🚀 How to Run (Tinkercad)

1. Open **Tinkercad Circuits** and create a new project.
2. Wire the hardware components to the Arduino Uno following standard pin assignments (or your specific schematic layout).
3. Paste the provided state machine source code (`.ino`) into the code editor.
4. Start the simulation.
5. Interact with the sensors (adjust LDR light levels or Ultrasonic distance slider) and push button to test state transitions.
