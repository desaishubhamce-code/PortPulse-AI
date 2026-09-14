# 🚢 PortPulse AI

---

## 👥 Team

| Field | Value |
|---|---|
| **Team Name** | PortPulse |
| **Track** | AI |
| **Team Lead** | Manan Kanparia — 26ce035@charusat.edu.in |
| **Members** | Manan Kanparia, Shubham Desai, Deep Kathiriya |

---

## 🎯 Problem Statement

Ports face unpredictable berth congestion, causing ships to wait for hours or days without warning, leading to fuel waste, delayed cargo, and higher costs for shipping companies and port operators.

---

## 💡 Solution

PortPulse AI analyzes ship arrival times, cargo type, and current queue data to predict berth congestion in advance. It shows real-time utilization percentages and color-coded risk alerts (red/yellow/green) so port operators can proactively manage traffic instead of reacting after congestion happens.

---

## ✨ Key Features

- **Berth Utilisation Prediction:** Predicts berth utilization % for 0–24h and 24–72h windows
- **Congestion Alerts:** Color-coded alerts — red = overloaded, yellow = warning, green = safe
- **Interactive Dashboard:** Streamlit dashboard with ship-level detail table
- **Bar Chart Visualisation:** Utilization per berth across both prediction windows

---

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| **Languages** | Python |
| **Frameworks** | Streamlit |
| **IBM Technologies** | IBM Bob |
| **Other** | Pandas |

---

## 📁 Repository Structure

```
├── src/                  # All source code
│   ├── dashboard.py          # Streamlit dashboard
│   ├── predict_congestion.py # Core congestion prediction logic
│   └── port_congestion_data.csv  # Sample ship data
├── docs/                 # Written documentation
│   ├── problem-statement.md
│   ├── solution-overview.md
│   ├── architecture.md
│   └── setup-guide.md
├── demo/                 # Demo artifacts
│   ├── screenshots/      # App screenshots
│   └── demo-video-link.txt
├── presentation/         # Slide deck
└── submission.yaml       # Structured submission metadata
```

---

## ⚡ How to Run

```bash
# 1. Clone the repo
git clone https://github.com/desaishubhamce-code/PortPulse-AI.git
cd PortPulse-AI

# 2. Install dependencies
pip install streamlit pandas

# 3. Run the dashboard
streamlit run src/dashboard.py
```

---

## 🖥️ Demo

| Artifact | Link |
|---|---|
| 📹 Demo Video | [See demo/demo-video-link.txt](demo/demo-video-link.txt) |
| 🖼️ Screenshots | [See demo/screenshots/](demo/screenshots/) |
| 📊 Presentation | [See presentation/](presentation/) |

---

## ⚠️ Known Limitations

- Data is based on a sample CSV — not connected to a live port data feed yet
- Prediction model uses a rule-based heuristic; ML-based forecasting can be added in future
- Dashboard is optimised for desktop browsers

---

## 🏅 What We're Most Proud Of

The queue-aware wait-time simulation — instead of just counting ships per berth, PortPulse models the actual unloading backlog by chaining each ship's estimated start time to the previous ship's end time. This gives a realistic picture of congestion even when arrivals are staggered across the day.

---
